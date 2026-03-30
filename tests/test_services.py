"""
Tests para servicios.
"""

from types import SimpleNamespace
from pathlib import Path

import pytest

from src.services.transcription_service import (
    AudioFormatError,
    TranscriptionEngineError,
    TranscriptionService,
    TranscriptionServiceError,
)


def test_transcription_service_success_with_mocked_engine(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verifica una transcripción exitosa sin depender de red/API externa."""
    service = TranscriptionService()
    audio_file = Path(__file__)

    monkeypatch.setattr(service, "_prepare_audio", lambda _: (audio_file, None))
    monkeypatch.setattr(service, "_cleanup_temp", lambda _: None)
    monkeypatch.setattr(service, "_recognize", lambda _path, _lang: "hola equipo")

    result = service.transcribe(audio_file)

    assert result == "hola equipo"


def test_transcription_service_raises_when_file_missing() -> None:
    """Verifica error de formato cuando el archivo no existe."""
    service = TranscriptionService()

    with pytest.raises(AudioFormatError):
        service.transcribe(Path("no_existe.wav"))


def test_recognize_maps_unknown_value_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verifica que UnknownValueError se traduzca a error de dominio."""
    service = TranscriptionService()
    fake_path = Path(__file__)

    import src.services.transcription_service as module

    class FakeAudioFile:
        def __init__(self, _path: str) -> None:
            self.path = _path

        def __enter__(self) -> SimpleNamespace:
            return SimpleNamespace()

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

    class FakeRecognizer:
        def record(self, _source: object) -> str:
            return "audio"

        def recognize_google(self, _audio_data: str, language: str) -> str:
            raise module.sr.UnknownValueError()

    monkeypatch.setattr(module.sr, "AudioFile", FakeAudioFile)
    monkeypatch.setattr(module.sr, "Recognizer", FakeRecognizer)

    with pytest.raises(TranscriptionServiceError):
        service._recognize(fake_path, "es-ES")


def test_recognize_maps_request_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verifica que RequestError se traduzca a error de motor."""
    service = TranscriptionService()
    fake_path = Path(__file__)

    import src.services.transcription_service as module

    class FakeAudioFile:
        def __init__(self, _path: str) -> None:
            self.path = _path

        def __enter__(self) -> SimpleNamespace:
            return SimpleNamespace()

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

    class FakeRecognizer:
        def record(self, _source: object) -> str:
            return "audio"

        def recognize_google(self, _audio_data: str, language: str) -> str:
            raise module.sr.RequestError("down")

    monkeypatch.setattr(module.sr, "AudioFile", FakeAudioFile)
    monkeypatch.setattr(module.sr, "Recognizer", FakeRecognizer)

    with pytest.raises(TranscriptionEngineError):
        service._recognize(fake_path, "es-ES")
