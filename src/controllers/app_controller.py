"""
Controlador Principal - Orquestación entre Modelo y Vista.
"""

from pathlib import Path
from typing import Optional

from src.models.transcription import TranscriptionTask
from src.services.transcription_service import (
    AudioConversionError,
    TranscriptionEngineError,
    TranscriptionService,
    TranscriptionServiceError,
)
from src.views.main_window import MainWindow
from src.utils.config import Config
from src.utils.validators import Validators

class AppController:
    """
    Controlador principal que orquesta la interacción entre Modelo y Vista.
    
    Gestiona la lógica de flujo de la aplicación sin contener lógica de negocio.
    """
    
    def __init__(self, view: MainWindow) -> None:
        """
        Inicializa el controlador.
        
        Args:
            view: Instancia de la ventana principal
        """
        self.view = view
        self.current_task: Optional[TranscriptionTask] = None
        self.transcription_service = TranscriptionService()
        self._connect_signals()
        Config.create_directories()
    
    def _connect_signals(self) -> None:
        """Conecta eventos de UI con métodos del controlador."""
        self.view.set_on_file_selected(self.on_file_selected)
        self.view.set_on_transcribe(self.on_transcribe)
        self.view.set_on_export(self.on_export)
        
        # Conectar botón Limpiar
        self.view.btn_clear.config(command=self.on_clear)
    
    def on_file_selected(self, file_path: Path) -> None:
        """
        Maneja la selección de archivo de audio.
        
        Args:
            file_path: Ruta del archivo seleccionado
        """
        # Validar el archivo
        if not Validators.is_valid_audio_file(file_path, Config.SUPPORTED_FORMATS):
            self.view.show_error("Error", "El archivo no es válido o no existe.")
            return
        
        if not Validators.is_valid_file_size(file_path, Config.MAX_FILE_SIZE_MB):
            self.view.show_error(
                "Error",
                f"El archivo excede el tamaño máximo de {Config.MAX_FILE_SIZE_MB} MB."
            )
            return
        
        # Crear tarea de transcripción
        import uuid
        self.current_task = TranscriptionTask(
            id=str(uuid.uuid4()),
            audio_path=file_path
        )
        
        self.view.set_file_label(f"📁 {file_path.name}")
        self.view.set_status(f"Archivo cargado: {file_path.name}")
        self.view.clear_transcription()
    
    def on_transcribe(self) -> None:
        """Maneja el evento de transcripción."""
        if self.current_task is None:
            self.view.show_error("Error", "Por favor selecciona un archivo de audio primero.")
            return
        
        self.current_task.mark_processing()
        self.view.set_status("Transcribiendo...")
        
        try:
            transcript = self._perform_transcription()
            self.current_task.mark_completed(transcript)
            self.view.set_transcription_text(transcript)
            self.view.set_status("Transcripción completada ✓")
            self.view.show_info("Éxito", "Archivo transcrito correctamente.")
        except AudioConversionError as error:
            self.current_task.mark_error(str(error))
            self.view.show_error(
                "Error de conversión",
                f"{error}\n\nInstala o configura ffmpeg para procesar MP3, M4A u otros formatos comprimidos."
            )
            self.view.set_status("Error de conversión de audio")
        except TranscriptionEngineError as error:
            self.current_task.mark_error(str(error))
            self.view.show_error("Servicio no disponible", str(error))
            self.view.set_status("Error del motor de transcripción")
        except TranscriptionServiceError as error:
            self.current_task.mark_error(str(error))
            self.view.show_error("Error en transcripción", str(error))
            self.view.set_status("Error en transcripción")
        except Exception as error:
            self.current_task.mark_error(str(error))
            self.view.show_error("Error inesperado", str(error))
            self.view.set_status("Error inesperado")
    
    def _perform_transcription(self) -> str:
        """
        Realiza la transcripción del audio.
        
        Returns:
            Texto transcrito
        
        Raises:
            Exception: Si ocurre un error en la transcripción
        """
        if self.current_task is None:
            raise ValueError("No existe una tarea de transcripción activa.")

        return self.transcription_service.transcribe(self.current_task.audio_path)
    
    def on_export(self, file_path: Path) -> None:
        """
        Maneja la exportación de la transcripción.
        
        Args:
            file_path: Ruta de destino para guardar el archivo
        """
        text = self.view.get_transcription_text()
        
        if not text:
            self.view.show_error("Error", "No hay transcripción para exportar.")
            return
        
        try:
            file_path.write_text(text, encoding="utf-8")
            self.view.set_status(f"Guardado en: {file_path.name}")
            self.view.show_info("Éxito", f"Archivo exportado a:\n{file_path}")
        except Exception as e:
            self.view.show_error("Error al guardar", str(e))
    
    def on_clear(self) -> None:
        """Limpia los datos de la aplicación."""
        self.current_task = None
        self.view.clear_transcription()
        self.view.set_file_label("No se ha seleccionado archivo")
        self.view.set_status("Datos limpiados")
