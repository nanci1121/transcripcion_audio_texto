"""
Servicio de transcripción.
"""

from pathlib import Path


class TranscriptionService:
    """Encapsula la lógica de transcripción de audio."""

    def transcribe(self, audio_path: Path) -> str:
        """
        Genera una transcripción para un archivo de audio.

        Args:
            audio_path: Ruta del archivo de audio.

        Returns:
            Texto transcrito simulado.
        """
        file_name = audio_path.name
        return (
            "Transcripción generada por TranscriptionService.\n\n"
            f"Archivo procesado: {file_name}\n"
            "Nota: esta es una implementación base y aún no usa un motor real."
        )
