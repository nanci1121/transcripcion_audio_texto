"""
Controlador Principal - Orquestación entre Modelo y Vista.
"""

import threading
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
        self.transcription_service = self._create_transcription_service(Config.TRANSCRIPTION_ENGINE)
        self._connect_signals()
        Config.create_directories()
    
    def _connect_signals(self) -> None:
        """Conecta eventos de UI con métodos del controlador."""
        self.view.set_on_file_selected(self.on_file_selected)
        self.view.set_on_transcribe(self.on_transcribe)
        self.view.set_on_preview(self.on_preview)
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
        """Maneja el evento de transcripción (no bloquea el hilo de UI)."""
        if self.current_task is None:
            self.view.show_error("Error", "Por favor selecciona un archivo de audio primero.")
            return

        self.current_task.mark_processing()
        self.view.set_status("Transcribiendo...")
        self.view.set_buttons_enabled(False)

        def _worker() -> None:
            try:
                transcript = self._perform_transcription()
                self.view.root.after(0, lambda: self._on_transcribe_done(transcript))
            except Exception as error:  # noqa: BLE001
                self.view.root.after(0, lambda e=error: self._on_transcribe_error(e))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_transcribe_done(self, transcript: str) -> None:
        """Callback en hilo principal tras transcripción exitosa."""
        if self.current_task:
            self.current_task.mark_completed(transcript)
        self.view.set_transcription_text(transcript)
        self.view.set_status("Transcripción completada ✓")
        self.view.set_buttons_enabled(True)
        self.view.show_info("Éxito", "Archivo transcrito correctamente.")

    def _on_transcribe_error(self, error: Exception) -> None:
        """Callback en hilo principal tras error de transcripción."""
        if self.current_task:
            self.current_task.mark_error(str(error))
        self.view.set_buttons_enabled(True)
        if isinstance(error, AudioConversionError):
            self.view.show_error(
                "Error de conversión",
                f"{error}\n\nInstala o configura ffmpeg para procesar MP3, M4A u otros formatos comprimidos.",
            )
            self.view.set_status("Error de conversión de audio")
        elif isinstance(error, TranscriptionEngineError):
            self.view.show_error("Servicio no disponible", str(error))
            self.view.set_status("Error del motor de transcripción")
        elif isinstance(error, TranscriptionServiceError):
            self.view.show_error("Error en transcripción", str(error))
            self.view.set_status("Error en transcripción")
        else:
            self.view.show_error("Error inesperado", str(error))
            self.view.set_status("Error inesperado")

    def on_preview(self) -> None:
        """Genera y transcribe un clip corto (no bloquea el hilo de UI)."""
        if self.current_task is None:
            self.view.show_error("Error", "Por favor selecciona un archivo de audio primero.")
            return

        self._refresh_transcription_engine()
        language_code = self.view.get_selected_language_code()
        preview_path = self._build_preview_path(self.current_task.audio_path)
        self.view.set_status("Generando clip de prueba...")
        self.view.set_buttons_enabled(False)

        def _worker() -> None:
            try:
                clip_path = self.transcription_service.create_preview_clip(
                    audio_path=self.current_task.audio_path,  # type: ignore[union-attr]
                    output_path=preview_path,
                    preview_seconds=Config.PREVIEW_CLIP_SECONDS,
                )
                transcript = self.transcription_service.transcribe(
                    clip_path,
                    language=language_code,
                    on_progress=self._on_preview_progress,
                    include_timestamps=self.view.should_include_timestamps(),
                )
                self.view.root.after(0, lambda: self._on_preview_done(transcript, clip_path))
            except Exception as error:  # noqa: BLE001
                self.view.root.after(0, lambda e=error: self._on_preview_error(e))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_preview_done(self, transcript: str, clip_path: Path) -> None:
        """Callback en hilo principal tras preview exitoso."""
        self.view.set_transcription_text(transcript)
        self.view.set_status("Prueba de 60s completada ✓")
        self.view.set_buttons_enabled(True)
        self.view.show_info("Prueba completada", f"Clip generado en:\n{clip_path}")

    def _on_preview_error(self, error: Exception) -> None:
        """Callback en hilo principal tras error en preview."""
        self.view.set_buttons_enabled(True)
        if isinstance(error, AudioConversionError):
            self.view.show_error("Error de conversión", str(error))
            self.view.set_status("Error al generar clip de prueba")
        elif isinstance(error, TranscriptionEngineError):
            self.view.show_error("Servicio no disponible", str(error))
            self.view.set_status("Error del motor de transcripción")
        elif isinstance(error, TranscriptionServiceError):
            self.view.show_error("Error en transcripción", str(error))
            self.view.set_status("Error en la prueba de 60s")
        else:
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

        self._refresh_transcription_engine()
        language_code = self.view.get_selected_language_code()

        return self.transcription_service.transcribe(
            self.current_task.audio_path,
            language=language_code,
            on_progress=self._on_transcription_progress,
            include_timestamps=self.view.should_include_timestamps(),
        )

    def _on_transcription_progress(self, current_chunk: int, total_chunks: int) -> None:
        """Actualiza la UI con el progreso por bloques de transcripción."""
        percent = int((current_chunk / total_chunks) * 100)
        status_msg = f"Transcribiendo... bloque {current_chunk}/{total_chunks} ({percent}%)"
        self.view.root.after(0, lambda msg=status_msg: self.view.set_status(msg))

    def _on_preview_progress(self, current_chunk: int, total_chunks: int) -> None:
        """Actualiza la UI con el progreso del clip de prueba."""
        percent = int((current_chunk / total_chunks) * 100)
        status_msg = f"Probando 60s... bloque {current_chunk}/{total_chunks} ({percent}%)"
        self.view.root.after(0, lambda msg=status_msg: self.view.set_status(msg))

    def _create_transcription_service(self, engine: str) -> TranscriptionService:
        """Construye el servicio de transcripción con el motor indicado."""
        return TranscriptionService(
            chunk_duration_seconds=Config.TRANSCRIPTION_CHUNK_SECONDS,
            chunk_overlap_seconds=Config.TRANSCRIPTION_CHUNK_OVERLAP_SECONDS,
            transcription_engine=engine,
            whisper_model_size=Config.WHISPER_MODEL_SIZE,
            whisper_compute_type=Config.WHISPER_COMPUTE_TYPE,
        )

    def _refresh_transcription_engine(self) -> None:
        """Actualiza el servicio cuando cambia el motor seleccionado en UI."""
        selected_engine = self.view.get_selected_transcription_engine()
        if self.transcription_service.transcription_engine != selected_engine:
            self.transcription_service = self._create_transcription_service(selected_engine)

    def _build_preview_path(self, audio_path: Path) -> Path:
        """Construye la ruta de salida para el clip corto de prueba."""
        file_name = f"{audio_path.stem}_preview_{Config.PREVIEW_CLIP_SECONDS}s.wav"
        return Config.OUTPUT_DIR / file_name
    
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
