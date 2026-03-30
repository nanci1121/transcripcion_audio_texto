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

    def __init__(self, chunk_duration_seconds: int = 25) -> None:
        """Configura herramientas externas necesarias para procesar audio."""
        self.chunk_duration_seconds = max(5, chunk_duration_seconds)
        self.ffmpeg_path = self._configure_audio_converter()

    def transcribe(
        self,
        audio_path: Path,
        language: str = "es-ES",
        on_progress: Optional[Callable[[int, int], None]] = None,
    ) -> str:
        """
        Genera una transcripción real para un archivo de audio.

        Args:
            audio_path: Ruta del archivo de audio.
            language: Código de idioma (ej. es-ES, en-US).
            on_progress: Callback opcional con (bloque_actual, bloques_totales).

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
            return self._recognize_in_chunks(prepared_path, language, on_progress)
        finally:
            self._cleanup_temp(temp_path)

    def _prepare_audio(self, audio_path: Path) -> tuple[Path, Optional[Path]]:
        """Prepara audio para reconocimiento y devuelve ruta lista para procesar."""
        valid_direct_formats = {".wav"}
        if audio_path.suffix.lower() in valid_direct_formats:
            return audio_path, None

        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_path = Path(temp_file.name)
            temp_file.close()
            command = [
                self.ffmpeg_path,
                "-y",
                "-i",
                str(audio_path),
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
    ) -> str:
        """Transcribe un audio largo en bloques pequeños y une el resultado."""
        duration_seconds = self._get_audio_duration(audio_path)
        chunk_texts: list[str] = []
        offset_seconds = 0
        total_chunks = max(
            1,
            (duration_seconds + self.chunk_duration_seconds - 1) // self.chunk_duration_seconds,
        )
        current_chunk = 0

        while offset_seconds < duration_seconds:
            current_chunk += 1
            if on_progress is not None:
                on_progress(current_chunk, total_chunks)

            chunk_text = self._recognize_chunk(
                audio_path=audio_path,
                language=language,
                offset_seconds=offset_seconds,
                duration_seconds=self.chunk_duration_seconds,
            )
            if chunk_text:
                chunk_texts.append(chunk_text)
            offset_seconds += self.chunk_duration_seconds

        transcript = " ".join(chunk_texts).strip()
        if not transcript:
            raise TranscriptionServiceError("La transcripción resultó vacía.")
        return transcript

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
