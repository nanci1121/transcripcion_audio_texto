"""
Validadores de entrada.
"""

from pathlib import Path
from typing import Tuple

class Validators:
    """
    Contiene funciones estáticas para validar entrada de usuario.
    """
    
    @staticmethod
    def is_valid_audio_file(file_path: Path, supported_formats: Tuple[str, ...]) -> bool:
        """
        Valida si un archivo es un archivo de audio válido.
        
        Args:
            file_path: Ruta del archivo
            supported_formats: Tuple con extensiones permitidas
        
        Returns:
            True si es válido, False en caso contrario
        """
        if not file_path.exists():
            return False
        
        if not file_path.is_file():
            return False
        
        if file_path.suffix.lower() not in supported_formats:
            return False
        
        return True
    
    @staticmethod
    def is_valid_file_size(file_path: Path, max_size_mb: int) -> bool:
        """
        Valida el tamaño del archivo.
        
        Args:
            file_path: Ruta del archivo
            max_size_mb: Tamaño máximo en MB
        
        Returns:
            True si el tamaño es válido, False en caso contrario
        """
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        return file_size_mb <= max_size_mb
    
    @staticmethod
    def is_valid_text(text: str, min_length: int = 1, max_length: int = 10000) -> bool:
        """
        Valida que el texto esté dentro de los límites.
        
        Args:
            text: Texto a validar
            min_length: Longitud mínima
            max_length: Longitud máxima
        
        Returns:
            True si es válido, False en caso contrario
        """
        if not isinstance(text, str):
            return False
        
        text_length = len(text.strip())
        return min_length <= text_length <= max_length
