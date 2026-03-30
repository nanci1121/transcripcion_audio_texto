"""
Servicio de transcripción.
"""

import subprocess
import tempfile
import wave
from pathlib import Path
from typing import Callable, Optional

import imageio_ffmpeg
import speech_recognition as sr
from pydub.utils import which

try:
    from faster_whisper import WhisperModel
except ImportError:  # pragma: no cover - dependencia opcional
    WhisperModel = None  # type: ignore[assignment]


class TranscriptionServiceError(Exception):
    """Error base del servicio de transcripción."""


class AudioFormatError(TranscriptionServiceError):
    """Error de formato de audio no soportado o inválido."""


class TranscriptionEngineError(TranscriptionServiceError):
    """Error al comunicarse con el motor de transcripción."""


class AudioConversionError(TranscriptionServiceError):
    """Error al convertir audio por falta de herramientas o codecs."""


class TranscriptionService:
    """Encapsula la lógica de transcripción de audio."""

    def __init__(
        self,
        chunk_duration_seconds: int = 25,
        chunk_overlap_seconds: int = 0,
        transcription_engine: str = "google_cloud",
        whisper_model_size: str = "small",
        whisper_compute_type: str = "int8",
    ) -> None:
        """Configura herramientas externas necesarias para procesar audio."""
        self.chunk_duration_seconds = max(5, chunk_duration_seconds)
        self.chunk_overlap_seconds = max(0, min(chunk_overlap_seconds, self.chunk_duration_seconds - 1))
        self.transcription_engine = transcription_engine
        self.whisper_model_size = whisper_model_size
        self.whisper_compute_type = whisper_compute_type
        self._whisper_model: Optional[WhisperModel] = None
        self.ffmpeg_path = self._configure_audio_converter()

    def transcribe(
        self,
        audio_path: Path,
        language: str = "es-ES",
        on_progress: Optional[Callable[[int, int], None]] = None,
        include_timestamps: bool = False,
    ) -> str:
        """
        Genera una transcripción real para un archivo de audio.

        Args:
            audio_path: Ruta del archivo de audio.
            language: Código de idioma (ej. es-ES, en-US).
            on_progress: Callback opcional con (bloque_actual, bloques_totales).
            include_timestamps: Si incluye prefijo [mm:ss] en cada segmento/bloque.

        Returns:
            Texto transcrito.

        Raises:
            AudioFormatError: Si el audio no es válido.
            TranscriptionServiceError: Si no se entiende el audio.
            TranscriptionEngineError: Si falla el motor de reconocimiento.
        """
        if not audio_path.exists() or not audio_path.is_file():
            raise AudioFormatError(f"No se encontró el archivo de audio: {audio_path}")

        prepared_path, temp_path = self._prepare_audio(audio_path)
        try:
            if self.transcription_engine == "whisper_local":
                return self._transcribe_with_local_whisper(
                    prepared_path,
                    language,
                    on_progress,
                    include_timestamps,
                )
            return self._recognize_in_chunks(
                prepared_path,
                language,
                on_progress,
                include_timestamps,
            )
        finally:
            self._cleanup_temp(temp_path)

    def _transcribe_with_local_whisper(
        self,
        audio_path: Path,
        language: str,
        on_progress: Optional[Callable[[int, int], None]] = None,
        include_timestamps: bool = False,
    ) -> str:
        """Transcribe en local con Whisper sin depender de red."""
        model = self._get_whisper_model()
        whisper_language = self._map_language_to_whisper(language)

        try:
            segments_iterator, _info = model.transcribe(
                str(audio_path),
                language=whisper_language,
                vad_filter=True,
            )
            segments = list(segments_iterator)
        except Exception as error:
            raise TranscriptionEngineError(
                "No fue posible transcribir en local con Whisper."
            ) from error

        total_segments = len(segments)
        if total_segments == 0:
            raise TranscriptionServiceError("La transcripción resultó vacía.")

        chunk_texts: list[str] = []
        for index, segment in enumerate(segments, start=1):
            if on_progress is not None:
                on_progress(index, total_segments)
            segment_text = segment.text.strip()
            if segment_text:
                if include_timestamps:
                    minute_mark = self._format_timestamp(segment.start)
                    segment_text = f"[{minute_mark}] {segment_text}"
                chunk_texts.append(segment_text)

        joiner = "\n" if include_timestamps else " "
        transcript = joiner.join(chunk_texts).strip()
        if not transcript:
            raise TranscriptionServiceError("La transcripción resultó vacía.")
        return transcript

    def _get_whisper_model(self) -> WhisperModel:
        """Inicializa y cachea el modelo Whisper local."""
        if WhisperModel is None:
            raise TranscriptionEngineError(
                "Falta la dependencia faster-whisper. Instálala para usar transcripción local."
            )

        if self._whisper_model is None:
            try:
                self._whisper_model = WhisperModel(
                    self.whisper_model_size,
                    device="cpu",
                    compute_type=self.whisper_compute_type,
                )
            except Exception as error:
                raise TranscriptionEngineError(
                    "No se pudo inicializar el modelo local de Whisper."
                ) from error

        return self._whisper_model

    def _map_language_to_whisper(self, language_code: str) -> str:
        """Convierte códigos regionales (ca-ES) a códigos ISO esperados por Whisper."""
        normalized = language_code.split("-")[0].lower()
        aliases = {
            "zh": "zh",
            "ca": "ca",
            "es": "es",
            "en": "en",
        }
        return aliases.get(normalized, normalized)

    def create_preview_clip(
        self,
        audio_path: Path,
        output_path: Path,
        preview_seconds: int,
    ) -> Path:
        """Genera un clip corto en WAV para pruebas rápidas de transcripción."""
        if not audio_path.exists() or not audio_path.is_file():
            raise AudioFormatError(f"No se encontró el archivo de audio: {audio_path}")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        preview_length = max(5, preview_seconds)

        try:
            command = [
                self.ffmpeg_path,
                "-y",
                "-i",
                str(audio_path),
                "-ss",
                "0",
                "-t",
                str(preview_length),
                str(output_path),
            ]
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as error:
            raise AudioConversionError(
                "No fue posible generar el clip de prueba del audio."
            ) from error

        return output_path

    def _prepare_audio(self, audio_path: Path) -> tuple[Path, Optional[Path]]:
        """Prepara audio para reconocimiento y devuelve ruta lista para procesar."""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_path = Path(temp_file.name)
            temp_file.close()
            command = [
                self.ffmpeg_path,
                "-y",
                "-i",
                str(audio_path),
                "-ac",
                "1",
                "-ar",
                "16000",
                "-vn",
                "-sn",
                "-dn",
                str(temp_path),
            ]
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )
            return temp_path, temp_path
        except subprocess.CalledProcessError as error:
            raise AudioConversionError(
                "No fue posible convertir el audio a WAV. Verifica que el archivo use un codec compatible."
            ) from error
        except Exception as error:
            raise AudioConversionError(
                "No fue posible preparar el audio para transcripción."
            ) from error

    def _recognize_in_chunks(
        self,
        audio_path: Path,
        language: str,
        on_progress: Optional[Callable[[int, int], None]] = None,
        include_timestamps: bool = False,
    ) -> str:
        """Transcribe un audio largo en bloques pequeños y une el resultado."""
        duration_seconds = self._get_audio_duration(audio_path)
        offsets = self._build_chunk_offsets(duration_seconds)
        total_chunks = len(offsets)
        transcript = ""
        timestamped_chunks: list[str] = []

        for current_chunk, offset_seconds in enumerate(offsets, start=1):
            if on_progress is not None:
                on_progress(current_chunk, total_chunks)

            chunk_text = self._recognize_chunk(
                audio_path=audio_path,
                language=language,
                offset_seconds=offset_seconds,
                duration_seconds=self.chunk_duration_seconds,
            )
            if chunk_text:
                if include_timestamps:
                    minute_mark = self._format_timestamp(offset_seconds)
                    timestamped_chunks.append(f"[{minute_mark}] {chunk_text}")
                else:
                    transcript = self._merge_chunk_texts(transcript, chunk_text)

        if include_timestamps:
            transcript = "\n".join(timestamped_chunks).strip()

        if not transcript:
            raise TranscriptionServiceError("La transcripción resultó vacía.")
        return transcript

    def _build_chunk_offsets(self, duration_seconds: int) -> list[int]:
        """Calcula offsets de inicio para cada bloque con solape opcional."""
        step_seconds = max(1, self.chunk_duration_seconds - self.chunk_overlap_seconds)
        offsets: list[int] = []
        offset = 0
        while offset < duration_seconds:
            offsets.append(offset)
            offset += step_seconds
        return offsets

    def _merge_chunk_texts(self, current_transcript: str, new_chunk_text: str) -> str:
        """Une bloques evitando duplicados simples en frontera por solape."""
        if not current_transcript:
            return new_chunk_text.strip()

        previous_words = current_transcript.split()
        new_words = new_chunk_text.strip().split()
        if not new_words:
            return current_transcript

        max_overlap_words = min(8, len(previous_words), len(new_words))
        overlap_size = 0
        for size in range(max_overlap_words, 0, -1):
            if self._normalize_words(previous_words[-size:]) == self._normalize_words(new_words[:size]):
                overlap_size = size
                break

        merged_tail = " ".join(new_words[overlap_size:]).strip()
        if not merged_tail:
            return current_transcript

        return f"{current_transcript} {merged_tail}".strip()

    def _normalize_words(self, words: list[str]) -> list[str]:
        """Normaliza palabras para comparación tolerante de fronteras."""
        punctuation = ".,;:!?¡¿\"'()[]{}"
        return [word.lower().strip(punctuation) for word in words]

    def _format_timestamp(self, seconds_value: float) -> str:
        """Convierte segundos a formato mm:ss."""
        safe_seconds = max(0, int(seconds_value))
        minutes = safe_seconds // 60
        seconds = safe_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def _recognize_chunk(
        self,
        audio_path: Path,
        language: str,
        offset_seconds: int,
        duration_seconds: int,
    ) -> str:
        """Transcribe un bloque concreto del audio."""
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(str(audio_path)) as source:
                audio_data = recognizer.record(
                    source,
                    offset=offset_seconds,
                    duration=duration_seconds,
                )
            transcript = recognizer.recognize_google(audio_data, language=language)
        except sr.UnknownValueError as error:
            return ""
        except sr.RequestError as error:
            raise TranscriptionEngineError(
                "No hay conexión con el servicio de transcripción."
            ) from error

        return transcript.strip()

    def _cleanup_temp(self, temp_path: Optional[Path]) -> None:
        """Elimina archivo temporal si fue creado durante la conversión."""
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)

    def _configure_audio_converter(self) -> str:
        """Resuelve la ruta a ffmpeg usando PATH o el binario empaquetado por Python."""
        converter_path = which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()
        if not converter_path:
            raise AudioConversionError(
                "No se encontró ffmpeg. Instala ffmpeg o agrega imageio-ffmpeg a tu entorno."
            )
        return converter_path

    def _get_audio_duration(self, audio_path: Path) -> int:
        """Obtiene la duración total del WAV en segundos enteros."""
        with wave.open(str(audio_path), "rb") as audio_file:
            frame_count = audio_file.getnframes()
            frame_rate = audio_file.getframerate()

        if frame_rate <= 0:
            raise AudioFormatError("No fue posible leer la duración del audio.")

        duration = frame_count / frame_rate
        return max(1, int(duration) + (1 if duration % 1 else 0))
