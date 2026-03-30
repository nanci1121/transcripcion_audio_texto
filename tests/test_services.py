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
    monkeypatch.setattr(
        service,
        "_recognize_in_chunks",
        lambda _path, _lang, _on_progress=None: "hola equipo",
    )

    result = service.transcribe(audio_file)

    assert result == "hola equipo"


def test_transcription_service_raises_when_file_missing() -> None:
    """Verifica error de formato cuando el archivo no existe."""
    service = TranscriptionService()

    with pytest.raises(AudioFormatError):
        service.transcribe(Path("no_existe.wav"))


def test_transcription_service_configures_audio_converter() -> None:
    """Verifica que el servicio resuelva una ruta válida de ffmpeg."""
    service = TranscriptionService()

    assert service.ffmpeg_path


def test_recognize_chunk_skips_unknown_value_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verifica que un bloque irreconocible se omita sin abortar el proceso."""
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
        def record(
            self,
            _source: object,
            offset: int = 0,
            duration: int | None = None,
        ) -> str:
            return "audio"

        def recognize_google(self, _audio_data: str, language: str) -> str:
            raise module.sr.UnknownValueError()

    monkeypatch.setattr(module.sr, "AudioFile", FakeAudioFile)
    monkeypatch.setattr(module.sr, "Recognizer", FakeRecognizer)

    assert service._recognize_chunk(fake_path, "es-ES", 0, 25) == ""


def test_recognize_chunk_maps_request_error(monkeypatch: pytest.MonkeyPatch) -> None:
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
        def record(
            self,
            _source: object,
            offset: int = 0,
            duration: int | None = None,
        ) -> str:
            return "audio"

        def recognize_google(self, _audio_data: str, language: str) -> str:
            raise module.sr.RequestError("down")

    monkeypatch.setattr(module.sr, "AudioFile", FakeAudioFile)
    monkeypatch.setattr(module.sr, "Recognizer", FakeRecognizer)

    with pytest.raises(TranscriptionEngineError):
        service._recognize_chunk(fake_path, "es-ES", 0, 25)


def test_recognize_in_chunks_joins_non_empty_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verifica que la transcripción final una bloques útiles y omita vacíos."""
    service = TranscriptionService()
    fake_path = Path(__file__)

    monkeypatch.setattr(service, "_get_audio_duration", lambda _path: 60)

    chunk_map = {
        0: "hola",
        25: "",
        50: "equipo",
    }

    monkeypatch.setattr(
        service,
        "_recognize_chunk",
        lambda audio_path, language, offset_seconds, duration_seconds: chunk_map[offset_seconds],
    )

    result = service._recognize_in_chunks(fake_path, "es-ES")

    assert result == "hola equipo"


def test_recognize_in_chunks_reports_progress(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verifica que la transcripción por bloques reporte progreso incremental."""
    service = TranscriptionService(chunk_duration_seconds=25)
    fake_path = Path(__file__)

    monkeypatch.setattr(service, "_get_audio_duration", lambda _path: 60)
    monkeypatch.setattr(
        service,
        "_recognize_chunk",
        lambda audio_path, language, offset_seconds, duration_seconds: "ok",
    )

    progress_events: list[tuple[int, int]] = []

    def on_progress(current_chunk: int, total_chunks: int) -> None:
        progress_events.append((current_chunk, total_chunks))

    result = service._recognize_in_chunks(fake_path, "es-ES", on_progress)

    assert result == "ok ok ok"
    assert progress_events == [(1, 3), (2, 3), (3, 3)]
