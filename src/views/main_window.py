"""
Ventana Principal - Interfaz Gráfica (tkinter).
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Callable, Optional

from src.utils.config import Config

class MainWindow:
    """
    Ventana principal de la aplicación de transcripción.
    
    Gestiona la interfaz gráfica sin lógica de negocio.
    """
    
    def __init__(self, root: tk.Tk) -> None:
        """
        Inicializa la ventana principal.
        
        Args:
            root: Ventana raíz de tkinter
        """
        self.root = root
        self.root.title(Config.APP_TITLE)
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        
        # Callbacks
        self._on_file_selected_callback: Optional[Callable[[Path], None]] = None
        self._on_transcribe_callback: Optional[Callable[[], None]] = None
        self._on_export_callback: Optional[Callable[[Path], None]] = None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Construye los elementos de la interfaz gráfica."""
        # Aplicar estilo
        style = ttk.Style()
        style.theme_use(Config.THEME)
        
        # Frame superior - Selección de archivo
        top_frame = ttk.LabelFrame(self.root, text="Archivo de Audio", padding=10)
        top_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.file_label = ttk.Label(top_frame, text="No se ha seleccionado archivo")
        self.file_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.btn_select = ttk.Button(top_frame, text="Seleccionar", width=15)
        self.btn_select.pack(side=tk.RIGHT, padx=5)
        
        # Frame central - Transcripción
        center_frame = ttk.LabelFrame(self.root, text="Transcripción", padding=10)
        center_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar para el texto
        scrollbar = ttk.Scrollbar(center_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_transcription = tk.Text(
            center_frame,
            height=15,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set
        )
        self.text_transcription.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_transcription.yview)
        
        # Frame inferior - Botones de acción
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.btn_transcribe = ttk.Button(bottom_frame, text="Transcribir", width=15)
        self.btn_transcribe.pack(side=tk.LEFT, padx=5)
        
        self.btn_export = ttk.Button(bottom_frame, text="Exportar", width=15)
        self.btn_export.pack(side=tk.LEFT, padx=5)
        
        self.btn_clear = ttk.Button(bottom_frame, text="Limpiar", width=15)
        self.btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def set_on_file_selected(self, callback: Callable[[Path], None]) -> None:
        """Vincula callback al evento de selección de archivo."""
        self._on_file_selected_callback = callback
        self.btn_select.config(command=self._handle_file_selection)
    
    def set_on_transcribe(self, callback: Callable[[], None]) -> None:
        """Vincula callback al evento de transcripción."""
        self._on_transcribe_callback = callback
        self.btn_transcribe.config(command=callback)
    
    def set_on_export(self, callback: Callable[[Path], None]) -> None:
        """Vincula callback al evento de exportación."""
        self._on_export_callback = callback
        self.btn_export.config(command=self._handle_export)
    
    def _handle_file_selection(self) -> None:
        """Maneja la selección de archivo."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=[("Audio Files", " ".join(Config.SUPPORTED_FORMATS))]
        )
        
        if file_path and self._on_file_selected_callback:
            self._on_file_selected_callback(Path(file_path))
    
    def _handle_export(self) -> None:
        """Maneja la exportación de transcripción."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path and self._on_export_callback:
            self._on_export_callback(Path(file_path))
    
    def set_file_label(self, filename: str) -> None:
        """Actualiza la etiqueta del archivo seleccionado."""
        self.file_label.config(text=filename)
    
    def set_transcription_text(self, text: str) -> None:
        """Establece el texto de la transcripción."""
        self.text_transcription.delete(1.0, tk.END)
        self.text_transcription.insert(1.0, text)
    
    def get_transcription_text(self) -> str:
        """Obtiene el texto de la transcripción."""
        return self.text_transcription.get(1.0, tk.END).strip()
    
    def set_status(self, message: str) -> None:
        """Actualiza la barra de estado."""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def show_error(self, title: str, message: str) -> None:
        """Muestra un diálogo de error."""
        messagebox.showerror(title, message)
    
    def show_info(self, title: str, message: str) -> None:
        """Muestra un diálogo de información."""
        messagebox.showinfo(title, message)
    
    def clear_transcription(self) -> None:
        """Limpia el área de transcripción."""
        self.text_transcription.delete(1.0, tk.END)
    
    def run(self) -> None:
        """Inicia la aplicación."""
        self.root.mainloop()
