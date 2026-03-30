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
    service = TranscriptionService(transcription_engine="google_cloud")
    audio_file = Path(__file__)

    monkeypatch.setattr(service, "_prepare_audio", lambda _: (audio_file, None))
    monkeypatch.setattr(service, "_cleanup_temp", lambda _: None)
    monkeypatch.setattr(
        service,
        "_recognize_in_chunks",
        lambda _path, _lang, _on_progress=None, _include_timestamps=False: "hola equipo",
    )

    result = service.transcribe(audio_file)

    assert result == "hola equipo"


def test_transcription_service_raises_when_file_missing() -> None:
    """Verifica error de formato cuando el archivo no existe."""
    service = TranscriptionService(transcription_engine="google_cloud")

    with pytest.raises(AudioFormatError):
        service.transcribe(Path("no_existe.wav"))


def test_transcription_service_configures_audio_converter() -> None:
    """Verifica que el servicio resuelva una ruta válida de ffmpeg."""
    service = TranscriptionService(transcription_engine="google_cloud")

    assert service.ffmpeg_path


def test_recognize_chunk_skips_unknown_value_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verifica que un bloque irreconocible se omita sin abortar el proceso."""
    service = TranscriptionService(transcription_engine="google_cloud")
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
    service = TranscriptionService(transcription_engine="google_cloud")
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
    service = TranscriptionService(transcription_engine="google_cloud")
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
    service = TranscriptionService(chunk_duration_seconds=25, transcription_engine="google_cloud")
    fake_path = Path(__file__)

    monkeypatch.setattr(service, "_get_audio_duration", lambda _path: 60)
    chunk_map = {
        0: "bloque uno",
        25: "bloque dos",
        50: "bloque tres",
    }
    monkeypatch.setattr(
        service,
        "_recognize_chunk",
        lambda audio_path, language, offset_seconds, duration_seconds: chunk_map[offset_seconds],
    )

    progress_events: list[tuple[int, int]] = []

    def on_progress(current_chunk: int, total_chunks: int) -> None:
        progress_events.append((current_chunk, total_chunks))

    result = service._recognize_in_chunks(fake_path, "es-ES", on_progress)

    assert result == "bloque uno bloque dos bloque tres"
    assert progress_events == [(1, 3), (2, 3), (3, 3)]


def test_create_preview_clip_invokes_ffmpeg(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Verifica que se genere un clip de prueba en la ruta de salida esperada."""
    service = TranscriptionService(transcription_engine="google_cloud")
    source = tmp_path / "source.mp3"
    source.write_bytes(b"fake")
    output = tmp_path / "preview.wav"

    import src.services.transcription_service as module

    def fake_run(command: list[str], check: bool, capture_output: bool, text: bool) -> None:
        output.write_bytes(b"wav")

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    result = service.create_preview_clip(source, output, 60)

    assert result == output
    assert output.exists()


def test_map_language_to_whisper_uses_iso_base() -> None:
    """Verifica mapeo de códigos regionales a códigos compatibles con Whisper."""
    service = TranscriptionService(transcription_engine="google_cloud")

    assert service._map_language_to_whisper("ca-ES") == "ca"
    assert service._map_language_to_whisper("es-ES") == "es"
    assert service._map_language_to_whisper("zh-TW") == "zh"


def test_format_timestamp_mm_ss() -> None:
    """Verifica conversión de segundos a formato mm:ss."""
    service = TranscriptionService(transcription_engine="google_cloud")

    assert service._format_timestamp(0) == "00:00"
    assert service._format_timestamp(65) == "01:05"
    assert service._format_timestamp(600) == "10:00"


def test_recognize_in_chunks_includes_timestamps(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verifica salida con prefijo de tiempo cuando include_timestamps=True."""
    service = TranscriptionService(transcription_engine="google_cloud", chunk_duration_seconds=25)
    fake_path = Path(__file__)

    monkeypatch.setattr(service, "_get_audio_duration", lambda _path: 60)
    chunk_map = {
        0: "hola",
        25: "equipo",
        50: "fin",
    }
    monkeypatch.setattr(
        service,
        "_recognize_chunk",
        lambda audio_path, language, offset_seconds, duration_seconds: chunk_map[offset_seconds],
    )

    result = service._recognize_in_chunks(fake_path, "es-ES", include_timestamps=True)

    assert result == "[00:00] hola\n[00:25] equipo\n[00:50] fin"
