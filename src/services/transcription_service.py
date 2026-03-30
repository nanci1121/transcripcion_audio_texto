"""
Servicio de transcripción.
"""

import tempfile
from pathlib import Path
from typing import Optional

import speech_recognition as sr
from pydub import AudioSegment


class TranscriptionServiceError(Exception):
    """Error base del servicio de transcripción."""


class AudioFormatError(TranscriptionServiceError):
    """Error de formato de audio no soportado o inválido."""


class TranscriptionEngineError(TranscriptionServiceError):
    """Error al comunicarse con el motor de transcripción."""


class TranscriptionService:
    """Encapsula la lógica de transcripción de audio."""

    def transcribe(self, audio_path: Path, language: str = "es-ES") -> str:
        """
        Genera una transcripción real para un archivo de audio.

        Args:
            audio_path: Ruta del archivo de audio.
            language: Código de idioma (ej. es-ES, en-US).

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
            return self._recognize(prepared_path, language)
        finally:
            self._cleanup_temp(temp_path)

    def _prepare_audio(self, audio_path: Path) -> tuple[Path, Optional[Path]]:
        """Prepara audio para reconocimiento y devuelve ruta lista para procesar."""
        valid_direct_formats = {".wav", ".aiff", ".aif", ".flac"}
        if audio_path.suffix.lower() in valid_direct_formats:
            return audio_path, None

        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_path = Path(temp_file.name)
            temp_file.close()
            AudioSegment.from_file(audio_path).export(temp_path, format="wav")
            return temp_path, temp_path
        except Exception as error:
            raise AudioFormatError(
                "No fue posible convertir el audio a WAV. Verifica formato y codec."
            ) from error

    def _recognize(self, audio_path: Path, language: str) -> str:
        """Transcribe un archivo de audio usando Google Speech Recognition."""
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(str(audio_path)) as source:
                audio_data = recognizer.record(source)
            transcript = recognizer.recognize_google(audio_data, language=language)
        except sr.UnknownValueError as error:
            raise TranscriptionServiceError(
                "No se pudo reconocer el contenido del audio."
            ) from error
        except sr.RequestError as error:
            raise TranscriptionEngineError(
                "No hay conexión con el servicio de transcripción."
            ) from error

        if not transcript.strip():
            raise TranscriptionServiceError("La transcripción resultó vacía.")
        return transcript

    def _cleanup_temp(self, temp_path: Optional[Path]) -> None:
        """Elimina archivo temporal si fue creado durante la conversión."""
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)
