"""
Ventana Principal - Interfaz Gráfica (tkinter).
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Callable, Optional

from src.utils.config import Config
from src.views.rounded_button import RoundedButton

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
        self._on_preview_callback: Optional[Callable[[], None]] = None
        self._on_export_callback: Optional[Callable[[Path], None]] = None
        self.language_var = tk.StringVar(value=Config.DEFAULT_TRANSCRIPTION_LANGUAGE)
        self.engine_var = tk.StringVar(value=self._resolve_default_engine_label())
        self.include_timestamps_var = tk.BooleanVar(value=Config.INCLUDE_TIMESTAMPS_BY_DEFAULT)
        
        self._setup_ui()
    
    # ── Paleta Office 365 ──────────────────────────────────────────────────
    _BG          = "#f3f2f1"   # fondo general
    _SURFACE     = "#ffffff"   # superficie de frames
    _BLUE        = "#0078d4"   # azul primario
    _BLUE_HOVER  = "#106ebe"   # azul oscuro hover
    _BLUE_LIGHT  = "#c7e0f4"   # azul claro selección
    _TEXT        = "#323130"   # texto principal
    _TEXT_MUTED  = "#605e5c"   # texto secundario
    _BORDER      = "#edebe9"   # bordes frames
    _STATUS_BG   = "#0078d4"   # barra de estado
    _BTN_ACCENT  = "#d83b01"   # botón limpiar (acento naranja)
    _FONT        = ("Segoe UI", 10)
    _FONT_SMALL  = ("Segoe UI", 9)
    _FONT_BOLD   = ("Segoe UI", 10, "bold")

    def _apply_office365_style(self) -> None:
        """Configura el tema visual inspirado en Office 365."""
        self.root.configure(bg=self._BG)
        style = ttk.Style()
        style.theme_use("clam")

        # Fondo general
        style.configure(".", background=self._BG, foreground=self._TEXT,
                        font=self._FONT, borderwidth=0)

        # LabelFrame
        style.configure("TLabelframe", background=self._SURFACE,
                        foreground=self._BLUE, relief="flat",
                        borderwidth=1, bordercolor=self._BORDER)
        style.configure("TLabelframe.Label", background=self._SURFACE,
                        foreground=self._BLUE, font=self._FONT_BOLD)

        # Frame normal
        style.configure("TFrame", background=self._SURFACE)

        # Labels
        style.configure("TLabel", background=self._SURFACE,
                        foreground=self._TEXT, font=self._FONT)
        style.configure("Status.TLabel", background=self._STATUS_BG,
                        foreground="#ffffff", font=self._FONT_SMALL,
                        padding=(6, 3))

        # Botones principales (azul)
        style.configure("Primary.TButton",
                        background=self._BLUE, foreground="#ffffff",
                        font=self._FONT_BOLD, relief="flat",
                        padding=(10, 6), borderwidth=0)
        style.map("Primary.TButton",
                  background=[("active", self._BLUE_HOVER),
                              ("pressed", self._BLUE_HOVER)],
                  foreground=[("active", "#ffffff")])

        # Botones secundarios (blanco con borde azul)
        style.configure("Secondary.TButton",
                        background=self._SURFACE, foreground=self._BLUE,
                        font=self._FONT, relief="flat",
                        padding=(10, 6), borderwidth=1)
        style.map("Secondary.TButton",
                  background=[("active", self._BLUE_LIGHT)],
                  foreground=[("active", self._BLUE)])

        # Botón limpiar (naranja)
        style.configure("Accent.TButton",
                        background=self._BTN_ACCENT, foreground="#ffffff",
                        font=self._FONT, relief="flat",
                        padding=(10, 6), borderwidth=0)
        style.map("Accent.TButton",
                  background=[("active", "#b83000"), ("pressed", "#b83000")],
                  foreground=[("active", "#ffffff")])

        # Combobox
        style.configure("TCombobox", fieldbackground=self._SURFACE,
                        background=self._SURFACE, foreground=self._TEXT,
                        selectbackground=self._BLUE_LIGHT,
                        selectforeground=self._TEXT, arrowcolor=self._BLUE)

        # Checkbutton
        style.configure("TCheckbutton", background=self._SURFACE,
                        foreground=self._TEXT, font=self._FONT)
        style.map("TCheckbutton",
                  background=[("active", self._SURFACE)],
                  indicatorcolor=[("selected", self._BLUE), ("", "#ffffff")])

        # Scrollbar
        style.configure("TScrollbar", background=self._BORDER,
                        troughcolor=self._SURFACE, arrowcolor=self._TEXT_MUTED)
        style.map("TScrollbar",
                  background=[("active", self._BLUE_LIGHT)])

    def _setup_ui(self) -> None:
        """Construye los elementos de la interfaz gráfica."""
        self._apply_office365_style()

        # Frame superior - Selección de archivo
        top_frame = ttk.LabelFrame(self.root, text="Archivo de Audio", padding=10)
        top_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.file_label = ttk.Label(top_frame, text="No se ha seleccionado archivo",
                                     foreground=self._TEXT_MUTED)
        self.file_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.btn_select = RoundedButton(
            top_frame, text="Seleccionar", style="primary",
            btn_width=130, btn_height=34, parent_bg=self._SURFACE,
        )
        self.btn_select.pack(side=tk.RIGHT, padx=5)

        # Selector de idioma y motor
        language_frame = ttk.Frame(top_frame)
        language_frame.pack(side=tk.RIGHT, padx=10)

        ttk.Label(language_frame, text="Idioma:").pack(side=tk.LEFT, padx=(0, 5))
        self.cmb_language = ttk.Combobox(
            language_frame,
            textvariable=self.language_var,
            values=list(Config.TRANSCRIPTION_LANGUAGES.keys()),
            state="readonly",
            width=12,
        )
        self.cmb_language.pack(side=tk.LEFT)

        ttk.Label(language_frame, text="Motor:").pack(side=tk.LEFT, padx=(10, 5))
        self.cmb_engine = ttk.Combobox(
            language_frame,
            textvariable=self.engine_var,
            values=list(Config.TRANSCRIPTION_ENGINES.keys()),
            state="readonly",
            width=24,
        )
        self.cmb_engine.pack(side=tk.LEFT)

        self.chk_timestamps = ttk.Checkbutton(
            language_frame,
            text="Incluir minuto",
            variable=self.include_timestamps_var,
        )
        self.chk_timestamps.pack(side=tk.LEFT, padx=(10, 0))
        
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
            yscrollcommand=scrollbar.set,
            background=self._SURFACE,
            foreground=self._TEXT,
            font=self._FONT,
            relief="flat",
            padx=8,
            pady=6,
            selectbackground=self._BLUE_LIGHT,
            selectforeground=self._TEXT,
            insertbackground=self._BLUE,
        )
        self.text_transcription.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_transcription.yview)
        
        # Frame inferior - Botones de acción
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.btn_transcribe = RoundedButton(
            bottom_frame, text="Transcribir", style="primary",
            btn_width=120, btn_height=34, parent_bg=self._SURFACE,
        )
        self.btn_transcribe.pack(side=tk.LEFT, padx=5)

        self.btn_preview = RoundedButton(
            bottom_frame, text="Probar 60s", style="secondary",
            btn_width=110, btn_height=34, parent_bg=self._SURFACE,
        )
        self.btn_preview.pack(side=tk.LEFT, padx=5)

        self.btn_export = RoundedButton(
            bottom_frame, text="Exportar", style="secondary",
            btn_width=100, btn_height=34, parent_bg=self._SURFACE,
        )
        self.btn_export.pack(side=tk.LEFT, padx=5)

        self.btn_clear = RoundedButton(
            bottom_frame, text="Limpiar", style="accent",
            btn_width=100, btn_height=34, parent_bg=self._SURFACE,
        )
        self.btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var,
                                    style="Status.TLabel")
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def set_on_file_selected(self, callback: Callable[[Path], None]) -> None:
        """Vincula callback al evento de selección de archivo."""
        self._on_file_selected_callback = callback
        self.btn_select.config(command=self._handle_file_selection)
    
    def set_on_transcribe(self, callback: Callable[[], None]) -> None:
        """Vincula callback al evento de transcripción."""
        self._on_transcribe_callback = callback
        self.btn_transcribe.config(command=callback)

    def set_on_preview(self, callback: Callable[[], None]) -> None:
        """Vincula callback al evento de prueba rápida de 60 segundos."""
        self._on_preview_callback = callback
        self.btn_preview.config(command=callback)
    
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

    def get_selected_language_code(self) -> str:
        """Obtiene el codigo de idioma seleccionado para transcribir."""
        selected = self.language_var.get()
        return Config.TRANSCRIPTION_LANGUAGES.get(
            selected,
            Config.TRANSCRIPTION_LANGUAGES[Config.DEFAULT_TRANSCRIPTION_LANGUAGE],
        )

    def get_selected_transcription_engine(self) -> str:
        """Obtiene el motor de transcripción seleccionado en la interfaz."""
        selected = self.engine_var.get()
        return Config.TRANSCRIPTION_ENGINES.get(selected, Config.TRANSCRIPTION_ENGINE)

    def should_include_timestamps(self) -> bool:
        """Indica si se deben incluir marcas de tiempo en la transcripción."""
        return bool(self.include_timestamps_var.get())

    def _resolve_default_engine_label(self) -> str:
        """Resuelve la etiqueta mostrada para el motor por defecto."""
        for label, engine_code in Config.TRANSCRIPTION_ENGINES.items():
            if engine_code == Config.TRANSCRIPTION_ENGINE:
                return label
        return next(iter(Config.TRANSCRIPTION_ENGINES))
    
    def set_buttons_enabled(self, enabled: bool) -> None:
        """Habilita o deshabilita todos los botones de acción."""
        state = tk.NORMAL if enabled else tk.DISABLED
        for btn in (self.btn_select, self.btn_transcribe, self.btn_preview,
                    self.btn_export, self.btn_clear):
            btn.config(state=state)

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
