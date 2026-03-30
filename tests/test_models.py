"""
Tests para los modelos.
"""

import pytest
from pathlib import Path
from src.models.transcription import TranscriptionTask

def test_transcription_task_creation():
    """Prueba la creación de una tarea de transcripción."""
    task = TranscriptionTask(id="test-1", audio_path=Path("test.mp3"))
    
    assert task.id == "test-1"
    assert task.status == "pending"
    assert task.transcript is None
    assert task.error_message is None

def test_transcription_task_completed():
    """Prueba marcar una tarea como completada."""
    task = TranscriptionTask(id="test-1", audio_path=Path("test.mp3"))
    transcript = "Hola mundo"
    
    task.mark_completed(transcript)
    
    assert task.status == "completed"
    assert task.transcript == transcript
    assert task.is_completed() is True

def test_transcription_task_error():
    """Prueba marcar una tarea con error."""
    task = TranscriptionTask(id="test-1", audio_path=Path("test.mp3"))
    error = "Archivo corrupto"
    
    task.mark_error(error)
    
    assert task.status == "error"
    assert task.error_message == error
    assert task.has_error() is True
