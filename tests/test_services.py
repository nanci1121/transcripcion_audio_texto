"""
Tests para servicios.
"""

from pathlib import Path

from src.services.transcription_service import TranscriptionService


def test_transcription_service_includes_file_name() -> None:
    """Verifica que la transcripción incluya el nombre del archivo."""
    service = TranscriptionService()

    result = service.transcribe(Path("audio_demo.mp3"))

    assert "audio_demo.mp3" in result
    assert "TranscriptionService" in result
