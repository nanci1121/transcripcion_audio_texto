"""
Modelo de Transcripción - Lógica de negocio.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from datetime import datetime

@dataclass
class TranscriptionTask:
    """
    Representa una tarea de transcripción de audio a texto.
    
    Attributes:
        id: Identificador único de la tarea
        audio_path: Ruta del archivo de audio
        status: Estado actual (pending, processing, completed, error)
        transcript: Texto transcrito (None si no se ha procesado)
        error_message: Mensaje de error (None si no hay error)
        created_at: Fecha/hora de creación
        completed_at: Fecha/hora de finalización
    """
    
    id: str
    audio_path: Path
    status: str = "pending"
    transcript: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def mark_processing(self) -> None:
        """Marca la tarea como en procesamiento."""
        self.status = "processing"
    
    def mark_completed(self, transcript: str) -> None:
        """
        Marca la tarea como completada.
        
        Args:
            transcript: Texto de la transcripción
        """
        self.status = "completed"
        self.transcript = transcript
        self.completed_at = datetime.now()
        self.error_message = None
    
    def mark_error(self, error: str) -> None:
        """
        Registra un error en la transcripción.
        
        Args:
            error: Descripción del error
        """
        self.status = "error"
        self.error_message = error
        self.completed_at = datetime.now()
    
    def is_completed(self) -> bool:
        """Verifica si la tarea está completada."""
        return self.status == "completed"
    
    def has_error(self) -> bool:
        """Verifica si la tarea tiene un error."""
        return self.status == "error"
