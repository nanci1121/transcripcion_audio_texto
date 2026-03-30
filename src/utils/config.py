"""
Configuración de la aplicación.
"""

from pathlib import Path
from typing import Any, Dict

class Config:
    """
    Gestiona la configuración de la aplicación.
    
    Centraliza valores de configuración para evitar hardcoding.
    """
    
    # Directorios
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    AUDIO_DIR: Path = PROJECT_ROOT / "audio_files"
    OUTPUT_DIR: Path = PROJECT_ROOT / "output"
    
    # Parámetros de la aplicación
    APP_TITLE: str = "Transcriptor de Audio"
    APP_VERSION: str = "0.1.0"
    WINDOW_WIDTH: int = 900
    WINDOW_HEIGHT: int = 700
    
    # Parámetros de transcripción
    SUPPORTED_FORMATS: tuple = (".mp3", ".wav", ".m4a", ".flac", ".ogg")
    MAX_FILE_SIZE_MB: int = 500
    TRANSCRIPTION_CHUNK_SECONDS: int = 25
    TRANSCRIPTION_CHUNK_OVERLAP_SECONDS: int = 2
    TRANSCRIPTION_ENGINE: str = "whisper_local"
    TRANSCRIPTION_ENGINES: Dict[str, str] = {
        "Whisper local (offline)": "whisper_local",
        "Google (requiere internet)": "google_cloud",
    }
    WHISPER_MODEL_SIZE: str = "small"
    WHISPER_COMPUTE_TYPE: str = "int8"
    INCLUDE_TIMESTAMPS_BY_DEFAULT: bool = True
    PREVIEW_CLIP_SECONDS: int = 60
    TRANSCRIPTION_LANGUAGES: Dict[str, str] = {
        "Espanol": "es-ES",
        "Catalan": "ca-ES",
        "Ingles": "en-US",
        "Chino tradicional": "zh-TW",
    }
    DEFAULT_TRANSCRIPTION_LANGUAGE: str = "Catalan"
    
    # Parámetros de UI
    THEME: str = "clam"
    FONT_FAMILY: str = "Segoe UI"
    FONT_SIZE: int = 10
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Retorna un diccionario con toda la configuración."""
        return {
            "app_title": cls.APP_TITLE,
            "window_width": cls.WINDOW_WIDTH,
            "window_height": cls.WINDOW_HEIGHT,
            "supported_formats": cls.SUPPORTED_FORMATS,
        }
    
    @classmethod
    def create_directories(cls) -> None:
        """Crea los directorios necesarios si no existen."""
        cls.AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
