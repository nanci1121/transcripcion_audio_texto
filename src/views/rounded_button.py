"""
Componente RoundedButton - Botón con esquinas redondeadas para tkinter.
"""

import tkinter as tk
from typing import Callable, Optional


class RoundedButton(tk.Canvas):
    """Botón con esquinas redondeadas y estados hover/pressed.

    Compatible con pack/grid/place y acepta config(command=...) para
    encajar en el mismo flujo que ttk.Button.
    """

    _STYLES: dict = {
        "primary": {
            "bg": "#0078d4",
            "fg": "#ffffff",
            "hover": "#106ebe",
            "pressed": "#005a9e",
            "font_weight": "bold",
        },
        "secondary": {
            "bg": "#c7e0f4",
            "fg": "#004578",
            "hover": "#a2c9e8",
            "pressed": "#7db3d4",
            "font_weight": "normal",
        },
        "accent": {
            "bg": "#d83b01",
            "fg": "#ffffff",
            "hover": "#b83000",
            "pressed": "#9a2800",
            "font_weight": "normal",
        },
    }

    def __init__(
        self,
        parent: tk.Widget,
        text: str,
        style: str = "primary",
        radius: int = 12,
        btn_width: int = 120,
        btn_height: int = 34,
        parent_bg: str = "#f3f2f1",
        command: Optional[Callable] = None,
        **kwargs: object,
    ) -> None:
        """Inicializa el botón redondeado.

        Args:
            parent: Widget contenedor.
            text: Texto visible del botón.
            style: "primary", "secondary" o "accent".
            radius: Radio de las esquinas en píxeles.
            btn_width: Ancho en píxeles.
            btn_height: Alto en píxeles.
            parent_bg: Color de fondo del padre para el anti-alias de esquinas.
            command: Función a ejecutar al hacer click.
        """
        super().__init__(
            parent,
            width=btn_width,
            height=btn_height,
            highlightthickness=0,
            bd=0,
            bg=parent_bg,
            **kwargs,
        )
        self._text = text
        self._colors = self._STYLES.get(style, self._STYLES["primary"])
        self._radius = radius
        self._btn_width = btn_width
        self._btn_height = btn_height
        self._command = command
        self._pressed = False
        self._disabled = False

        self._draw(self._colors["bg"])
        self._bind_events()

    # ── Dibujo ────────────────────────────────────────────────────────────

    def _draw(self, fill_color: str) -> None:
        """Redibuja el botón con el color de fondo indicado."""
        self.delete("all")
        r = self._radius
        w = self._btn_width
        h = self._btn_height

        color = fill_color if not self._disabled else "#bdbdbd"
        text_color = self._colors["fg"] if not self._disabled else "#ffffff"

        # Rectángulo redondeado usando arcos y líneas
        self.create_arc(0, 0, 2 * r, 2 * r,
                        start=90, extent=90, fill=color, outline="")
        self.create_arc(w - 2 * r, 0, w, 2 * r,
                        start=0, extent=90, fill=color, outline="")
        self.create_arc(0, h - 2 * r, 2 * r, h,
                        start=180, extent=90, fill=color, outline="")
        self.create_arc(w - 2 * r, h - 2 * r, w, h,
                        start=270, extent=90, fill=color, outline="")

        # Rectángulos de relleno entre arcos
        self.create_rectangle(r, 0, w - r, h, fill=color, outline="")
        self.create_rectangle(0, r, w, h - r, fill=color, outline="")

        # Texto centrado
        font_weight = self._colors.get("font_weight", "normal")
        self.create_text(
            w // 2, h // 2,
            text=self._text,
            fill=text_color,
            font=("Segoe UI", 10, font_weight),
        )

    # ── Eventos ───────────────────────────────────────────────────────────

    def _bind_events(self) -> None:
        """Registra los eventos del ratón."""
        for widget in (self,):
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<ButtonPress-1>", self._on_press)
            widget.bind("<ButtonRelease-1>", self._on_release)

        # Propagar eventos desde el texto al Canvas
        self.tag_bind("all", "<Enter>", self._on_enter)
        self.tag_bind("all", "<Leave>", self._on_leave)
        self.tag_bind("all", "<ButtonPress-1>", self._on_press)
        self.tag_bind("all", "<ButtonRelease-1>", self._on_release)

    def _on_enter(self, _event: object = None) -> None:
        if not self._pressed and not self._disabled:
            self._draw(self._colors["hover"])

    def _on_leave(self, _event: object = None) -> None:
        self._pressed = False
        self._draw(self._colors["bg"])

    def _on_press(self, _event: object = None) -> None:
        if self._disabled:
            return
        self._pressed = True
        self._draw(self._colors["pressed"])

    def _on_release(self, _event: object = None) -> None:
        if self._disabled:
            return
        self._pressed = False
        self._draw(self._colors["hover"])
        if self._command:
            self._command()

    # ── API compatible con ttk.Button ─────────────────────────────────────

    def config(self, command: Optional[Callable] = None,  # type: ignore[override]
               state: Optional[str] = None, **kwargs: object) -> None:
        """Permite vincular command y state igual que en ttk.Button."""
        if command is not None:
            self._command = command
        if state is not None:
            self._disabled = (state == tk.DISABLED)
            self._draw(self._colors["bg"])
        if kwargs:
            super().config(**kwargs)
