# /// script
# requires-python = ">=3.10"
# dependencies = ["pywinusb", "pynput"]
# ///

# -*- coding: utf-8 -*-
"""
Mini Configurator - Aplicacion moderna para configurar Mini Controlador USB
3 botones + 1 knob | VID=0x1189 PID=0x8890

Basado en el protocolo HID descifrado de RSoft.MacroPad.BLL.dll
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import sys
import threading
import time

# Agregar directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from hid_device import HidDevice, test_connection
from keyboard_detector import KeyboardDetector


# ============================================
# ESTILOS MODERNOS
# ============================================
def setup_styles(root):
    """Configure modern ttk styles."""
    style = ttk.Style(root)
    style.theme_use("clam")

    # ── Buttons ─────────────────────────────────────────────────────────
    style.configure("Accent.TButton",
                    background=config.Colors.ACCENT,
                    foreground=config.Colors.BG_DARK,
                    font=("Segoe UI", 10, "bold"),
                    padding=(18, 9),
                    borderwidth=0, relief="flat")
    style.map("Accent.TButton",
              background=[("active", config.Colors.ACCENT_SECONDARY),
                          ("disabled", config.Colors.BG_BUTTON)],
              foreground=[("active", config.Colors.BG_DARK),
                          ("disabled", config.Colors.TEXT_DIM)])

    style.configure("Ghost.TButton",
                    background=config.Colors.BG_CARD,
                    foreground=config.Colors.TEXT_DIM,
                    font=("Segoe UI", 9),
                    padding=(12, 6),
                    borderwidth=0, relief="flat")
    style.map("Ghost.TButton",
              background=[("active", config.Colors.BG_BUTTON)],
              foreground=[("active", config.Colors.TEXT)])

    # keep Secondary for any remaining usages
    style.configure("Secondary.TButton",
                    background=config.Colors.BG_BUTTON,
                    foreground=config.Colors.TEXT,
                    font=("Segoe UI", 9),
                    padding=(14, 7),
                    borderwidth=0, relief="flat")
    style.map("Secondary.TButton",
              background=[("active", config.Colors.BG_BUTTON_HOVER)],
              foreground=[("active", config.Colors.TEXT)])

    # ── Combobox ────────────────────────────────────────────────────────
    style.configure("Modern.TCombobox",
                    fieldbackground=config.Colors.BG_BUTTON,
                    background=config.Colors.BG_BUTTON,
                    foreground=config.Colors.TEXT,
                    selectbackground=config.Colors.ACCENT,
                    selectforeground=config.Colors.BG_DARK,
                    arrowcolor=config.Colors.TEXT_DIM,
                    borderwidth=0,
                    font=("Segoe UI", 10))
    style.map("Modern.TCombobox",
              fieldbackground=[("readonly", config.Colors.BG_BUTTON)],
              foreground=[("readonly", config.Colors.TEXT)],
              selectbackground=[("readonly", config.Colors.BG_BUTTON)])

    # ── Entry ───────────────────────────────────────────────────────────
    style.configure("Modern.TEntry",
                    fieldbackground=config.Colors.BG_BUTTON,
                    foreground=config.Colors.TEXT,
                    insertcolor=config.Colors.TEXT,
                    borderwidth=0,
                    font=("Segoe UI", 10))

    # ── Scrollbar ───────────────────────────────────────────────────────
    style.configure("Modern.Vertical.TScrollbar",
                    background=config.Colors.BG_BUTTON,
                    troughcolor=config.Colors.BG_CARD,
                    bordercolor=config.Colors.BG_CARD,
                    arrowcolor=config.Colors.TEXT_DIM,
                    borderwidth=0)


# ============================================
# APLICACION PRINCIPAL
# ============================================
class MiniConfiguratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Configurator")
        self.root.configure(bg=config.Colors.BG_DARK)
        self.root.geometry("920x680")
        self.root.minsize(800, 580)

        # Estado
        self.device_connected = False
        self.device_path = None
        self.current_control = None  # (action_byte, nombre)
        self.presets_dir = os.path.join(os.path.dirname(__file__), "presets")
        os.makedirs(self.presets_dir, exist_ok=True)

        # Detector de teclado
        self._detector = None
        self._detecting = False

        # Secuencia detectada pendiente de confirmar
        self._pending_sequence = []

        # Configuracion en memoria: {action_byte: [(mod, key), ...]}
        self.current_config = {}
        for byte, name in config.CONTROLS:
            self.current_config[byte] = []

        # Dirty flag: config has unsaved changes
        self._config_dirty = False

        # Estilos
        setup_styles(root)

        # UI
        self._build_ui()

        # Verificar conexion
        self._check_device()

        # Limpiar detector al cerrar
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        if self._config_dirty:
            if not messagebox.askyesno(
                    "Unsaved Changes",
                    "There are unsaved changes that haven't been sent to the device.\n\nExit anyway?",
                    icon="warning"):
                return
        if self._detector:
            self._detector.stop()
        self.root.destroy()

    def _build_ui(self):
        """Construir la interfaz completa."""
        # ============ HEADER ============
        header = tk.Frame(self.root, bg=config.Colors.BG_DARK, height=55)
        header.pack(fill=tk.X, padx=20, pady=(12, 8))
        header.pack_propagate(False)

        tk.Label(header, text="Mini Configurator",
                 bg=config.Colors.BG_DARK, fg=config.Colors.TEXT,
                 font=("Segoe UI", 20, "bold")).pack(side=tk.LEFT)

        tk.Label(header, text="VID:1189 PID:8890",
                 bg=config.Colors.BG_DARK, fg=config.Colors.TEXT_DIM,
                 font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(12, 0), pady=(6, 0))

        # Status pill (derecha)
        self.status_label = tk.Label(header, text="● Verificando...",
                                     bg=config.Colors.BG_DARK, fg=config.Colors.TEXT_DIM,
                                     font=("Segoe UI", 10, "bold"))
        self.status_label.pack(side=tk.RIGHT)

        ttk.Button(header, text="Reconectar",
                   style="Secondary.TButton",
                   command=self._check_device).pack(side=tk.RIGHT, padx=(0, 10))

        # ============ CONTENIDO PRINCIPAL ============
        content = tk.Frame(self.root, bg=config.Colors.BG_DARK)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 8))

        # --- Panel izquierdo ---
        left_panel = tk.Frame(content, bg=config.Colors.BG_CARD,
                              highlightthickness=1, highlightbackground=config.Colors.BORDER)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=(0, 10))
        left_panel.configure(width=280)
        left_panel.pack_propagate(False)

        # Ilustracion interactiva del dispositivo
        self._build_device_panel(left_panel)

        # Separador
        tk.Frame(left_panel, bg=config.Colors.BORDER, height=1).pack(
            fill=tk.X, padx=12, pady=(12, 8))

        # Seccion LED
        self._build_led_panel(left_panel)

        # --- Panel derecho: Configuracion ---
        right_panel = tk.Frame(content, bg=config.Colors.BG_CARD,
                               highlightthickness=1, highlightbackground=config.Colors.BORDER)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_panel = right_panel
        self._build_config_panel()

        # ============ FOOTER ============
        footer = tk.Frame(self.root, bg=config.Colors.BG_DARK, height=48)
        footer.pack(fill=tk.X, padx=20, pady=(0, 12))
        footer.pack_propagate(False)

        self._save_btn = tk.Button(
            footer, text="Save to Device",
            bg=config.Colors.BG_BUTTON, fg=config.Colors.TEXT,
            activebackground=config.Colors.ACCENT,
            activeforeground=config.Colors.BG_DARK,
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT, cursor="hand2", bd=0, padx=20, pady=8,
            command=self._save_to_device)
        self._save_btn.pack(side=tk.RIGHT, padx=4)

        tk.Button(footer, text="Guardar Preset",
                  bg=config.Colors.BG_BUTTON, fg=config.Colors.TEXT,
                  activebackground=config.Colors.BG_BUTTON_HOVER,
                  activeforeground=config.Colors.TEXT,
                  font=("Segoe UI", 10),
                  relief=tk.FLAT, cursor="hand2", bd=0, padx=15, pady=6,
                  command=self._save_preset).pack(side=tk.RIGHT, padx=4)

        tk.Button(footer, text="Cargar Preset",
                  bg=config.Colors.BG_BUTTON, fg=config.Colors.TEXT,
                  activebackground=config.Colors.BG_BUTTON_HOVER,
                  activeforeground=config.Colors.TEXT,
                  font=("Segoe UI", 10),
                  relief=tk.FLAT, cursor="hand2", bd=0, padx=15, pady=6,
                  command=self._load_preset).pack(side=tk.RIGHT, padx=4)

    def _build_device_panel(self, parent):
        """Canvas-based interactive device illustration (3 keys + knob on right)."""
        import math

        W, H = 248, 100
        BG = config.Colors.BG_CARD

        canvas = tk.Canvas(parent, width=W, height=H, bg=BG, highlightthickness=0)
        canvas.pack(padx=16, pady=(14, 0))
        self._dev_canvas   = canvas
        self._dev_faces    = {}   # action_byte -> polygon item id (keycap face)
        self._dev_labels   = {}   # action_byte -> text item id
        self._dev_knob_body = None
        self._dev_knob_dot  = None
        self._knob_tab_btns = {}

        def rrect(x1, y1, x2, y2, r, **kw):
            """Smooth rounded-rectangle polygon."""
            pts = [
                x1+r, y1,   x2-r, y1,   x2,   y1,     x2,   y1+r,
                x2,   y2-r, x2,   y2,   x2-r, y2,     x1+r, y2,
                x1,   y2,   x1,   y2-r, x1,   y1+r,   x1,   y1,
            ]
            return canvas.create_polygon(pts, smooth=True, **kw)

        # ── Case shell ──
        rrect(3, 3, W-3, H-3, 10, fill="#1e1e20", outline="#3a3a3e", width=2)
        rrect(8, 7, W-8, H-7, 7,  fill="#161618", outline="#252528", width=1)

        # USB-C port (left edge)
        canvas.create_rectangle(3, H//2-7, 14, H//2+7,
                               fill="#1c1c1e", outline="#484848", width=1)
        canvas.create_rectangle(5, H//2-4, 12, H//2+4, fill="#090909", outline="")

        # ── Three keycaps ──
        B = 44      # keycap size px
        by = H//2 - B//2
        bxs = [16, 64, 112]

        for i, (ab, name) in enumerate(config.CONTROLS[:3]):
            x = bxs[i]
            tag = f"ctrl_{ab}"

            # Drop shadow
            canvas.create_rectangle(x+2, by+4, x+B+1, by+B+3,
                                   fill="#080808", outline="", tags=tag)
            # Keycap face
            fid = rrect(x, by, x+B, by+B, 5,
                       fill="#dcdcdc", outline="#aaaaaa", width=1, tags=tag)
            # Shine line
            canvas.create_line(x+5, by+6, x+B-8, by+6,
                              fill="#f2f2f2", width=1, tags=tag)
            # Number legend
            lid = canvas.create_text(x + B//2, by + B//2 + 1,
                                    text=str(i + 1),
                                    fill="#1a1a1a",
                                    font=("Segoe UI", 13, "bold"),
                                    tags=tag)
            self._dev_faces[ab]  = fid
            self._dev_labels[ab] = lid

            canvas.tag_bind(tag, "<Button-1>",
                           lambda e, b=ab, n=name: self._select_control(b, n))
            canvas.tag_bind(tag, "<Enter>",
                           lambda e: canvas.config(cursor="hand2"))
            canvas.tag_bind(tag, "<Leave>",
                           lambda e: canvas.config(cursor=""))

        # ── Knob ──
        kx, ky, kr = W - 38, H // 2, 26
        tk_knob = "ctrl_knob"

        # Outer base ring
        canvas.create_oval(kx-kr-5, ky-kr-5, kx+kr+5, ky+kr+5,
                          fill="#0d0d0d", outline="#282828", tags=tk_knob)
        # Knob body
        self._dev_knob_body = canvas.create_oval(
            kx-kr, ky-kr, kx+kr, ky+kr,
            fill="#333336", outline="#555558", width=2, tags=tk_knob)
        # Tick marks
        for a in range(0, 360, 30):
            r1, r2 = kr - 8, kr - 3
            rad = math.radians(a)
            canvas.create_line(
                kx + r1*math.cos(rad), ky + r1*math.sin(rad),
                kx + r2*math.cos(rad), ky + r2*math.sin(rad),
                fill="#404044", width=1, tags=tk_knob)
        # Pointer line (pointing up)
        canvas.create_line(kx, ky, kx, ky - kr + 5,
                          fill="#c8c8cc", width=2, tags=tk_knob)
        # Center dot (accent)
        self._dev_knob_dot = canvas.create_oval(
            kx-5, ky-5, kx+5, ky+5,
            fill=config.Colors.ACCENT, outline="", tags=tk_knob)

        # Knob click → select first knob action
        if config.CONTROLS[3:]:
            first_ab, first_name = config.CONTROLS[3]
            canvas.tag_bind(tk_knob, "<Button-1>",
                           lambda e, b=first_ab, n=first_name: self._select_control(b, n))
            canvas.tag_bind(tk_knob, "<Enter>",
                           lambda e: canvas.config(cursor="hand2"))
            canvas.tag_bind(tk_knob, "<Leave>",
                           lambda e: canvas.config(cursor=""))

        # ── Knob action tab pills ──
        tabs_frame = tk.Frame(parent, bg=BG)
        tabs_frame.pack(fill=tk.X, padx=20, pady=(8, 0))

        for ab, name in config.CONTROLS[3:]:
            short = name.split(" - ")[-1] if " - " in name else name
            btn = tk.Button(
                tabs_frame, text=short,
                bg=config.Colors.BG_BUTTON, fg=config.Colors.TEXT_DIM,
                activebackground=config.Colors.ACCENT,
                activeforeground=config.Colors.BG_DARK,
                font=("Segoe UI", 8, "bold"),
                relief=tk.FLAT, cursor="hand2", bd=0,
                padx=10, pady=5,
                command=lambda b=ab, n=name: self._select_control(b, n))
            btn.pack(side=tk.LEFT, padx=(0, 4))
            self._knob_tab_btns[ab] = btn

    def _update_device_highlight(self, selected_ab):
        """Refresh canvas keycap + knob + tab button visuals for current selection."""
        if not hasattr(self, '_dev_canvas') or not self._dev_canvas.winfo_exists():
            return
        canvas = self._dev_canvas

        # Reset all keycap faces & labels
        for fid in self._dev_faces.values():
            canvas.itemconfig(fid, fill="#dcdcdc", outline="#aaaaaa")
        for lid in self._dev_labels.values():
            canvas.itemconfig(lid, fill="#1a1a1a")

        # Reset knob body & center dot
        if self._dev_knob_body:
            canvas.itemconfig(self._dev_knob_body, fill="#333336", outline="#555558")
        if self._dev_knob_dot:
            canvas.itemconfig(self._dev_knob_dot, fill=config.Colors.ACCENT)

        # Reset knob tab pills
        for btn in self._knob_tab_btns.values():
            btn.config(bg=config.Colors.BG_BUTTON, fg=config.Colors.TEXT_DIM)

        # Apply highlight to the selected control
        if selected_ab in self._dev_faces:
            # One of the 3 keycaps
            canvas.itemconfig(self._dev_faces[selected_ab],
                             fill=config.Colors.ACCENT, outline=config.Colors.ACCENT_SECONDARY)
            canvas.itemconfig(self._dev_labels[selected_ab],
                             fill=config.Colors.BG_DARK)
        elif selected_ab in self._knob_tab_btns:
            # A knob action — glow the knob body and highlight the tab
            if self._dev_knob_body:
                canvas.itemconfig(self._dev_knob_body,
                                 fill=config.Colors.ACCENT,
                                 outline=config.Colors.ACCENT_SECONDARY)
            if self._dev_knob_dot:
                canvas.itemconfig(self._dev_knob_dot, fill=config.Colors.BG_DARK)
            self._knob_tab_btns[selected_ab].config(
                bg=config.Colors.ACCENT, fg=config.Colors.BG_DARK)

    def _build_led_panel(self, parent):
        """LED panel — toggle expands 6 radio buttons with mode names."""
        self._led_active_mode = None
        self._led_panel_open = False
        self._led_var = tk.IntVar(value=-1)

        hdr_row = tk.Frame(parent, bg=config.Colors.BG_CARD)
        hdr_row.pack(fill=tk.X, padx=16, pady=(0, 2))

        self._led_toggle_btn = tk.Button(
            hdr_row, text="▶  LED",
            bg=config.Colors.BG_CARD, fg=config.Colors.ACCENT,
            activebackground=config.Colors.BG_CARD,
            activeforeground=config.Colors.ACCENT_SECONDARY,
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT, cursor="hand2", bd=0, anchor=tk.W,
            command=self._toggle_led_panel)
        self._led_toggle_btn.pack(side=tk.LEFT)

        self._led_current_lbl = tk.Label(
            hdr_row, text="",
            bg=config.Colors.BG_CARD, fg=config.Colors.TEXT_DIM,
            font=("Segoe UI", 8))
        self._led_current_lbl.pack(side=tk.LEFT, padx=(8, 0))

        # Collapsible body
        self._led_body = tk.Frame(parent, bg=config.Colors.BG_BUTTON)

        inner = tk.Frame(self._led_body, bg=config.Colors.BG_BUTTON)
        inner.pack(fill=tk.X, padx=14, pady=8)

        MODE_DESCRIPTIONS = [
            "Off — LEDs apagados",
            "Mode 1 — efecto 1",
            "Mode 2 — efecto 2",
        ]

        self._led_radio_btns = []
        for mode_idx, label in config.LED_MODE_NAMES:
            desc = MODE_DESCRIPTIONS[mode_idx] if mode_idx < len(MODE_DESCRIPTIONS) else label
            rb = tk.Radiobutton(
                inner, text=desc, variable=self._led_var, value=mode_idx,
                bg=config.Colors.BG_BUTTON, fg=config.Colors.TEXT,
                selectcolor=config.Colors.BG_BUTTON,
                activebackground=config.Colors.BG_BUTTON,
                activeforeground=config.Colors.ACCENT,
                font=("Segoe UI", 9), relief=tk.FLAT, bd=0,
                command=lambda m=mode_idx: self._set_led_mode(m))
            rb.pack(anchor=tk.W, pady=2)
            self._led_radio_btns.append(rb)

        self._led_status = tk.Label(
            self._led_body, text="",
            bg=config.Colors.BG_BUTTON, fg=config.Colors.TEXT_DIM,
            font=("Segoe UI", 8), padx=14)
        self._led_status.pack(anchor=tk.W, pady=(0, 6))

    def _toggle_led_panel(self):
        """Expand/collapse the LED mode panel."""
        if self._led_panel_open:
            self._led_body.pack_forget()
            self._led_toggle_btn.config(text="▶  LED")
            self._led_panel_open = False
        else:
            self._led_body.pack(fill=tk.X, padx=8, pady=(0, 8))
            self._led_toggle_btn.config(text="▼  LED")
            self._led_panel_open = True

    def _set_led_mode(self, target_mode):
        """Send LED mode to device."""
        if not self.device_connected:
            self._led_status.config(text="No device", fg=config.Colors.ERROR)
            return

        self._led_status.config(text="Sending...", fg=config.Colors.WARNING)
        for rb in self._led_radio_btns:
            rb.config(state=tk.DISABLED)

        def worker():
            try:
                with HidDevice(self.device_path) as dev:
                    dev.set_led(target_mode)
                self.root.after(0, lambda: self._on_led_done(target_mode))
            except Exception as e:
                self.root.after(0, lambda err=str(e): self._on_led_error(err))

        threading.Thread(target=worker, daemon=True).start()

    def _on_led_done(self, active_mode):
        self._led_active_mode = active_mode
        self._led_var.set(active_mode)
        _, label = config.LED_MODE_NAMES[active_mode]
        self._led_status.config(text=f"✓ Applied", fg=config.Colors.SUCCESS)
        self._led_current_lbl.config(text=f"— {label.strip()}")
        for rb in self._led_radio_btns:
            rb.config(state=tk.NORMAL)

    def _on_led_error(self, err):
        for rb in self._led_radio_btns:
            rb.config(state=tk.NORMAL)
        self._led_status.config(text=f"Error: {err[:40]}", fg=config.Colors.ERROR)

    def _draw_knob(self):
        """Dibujar representacion visual del knob (compacto 90x90)."""
        import math
        c = self.knob_canvas
        cx, cy = 45, 45
        r = 30

        c.create_oval(cx-r, cy-r, cx+r, cy+r,
                     fill=config.Colors.BG_BUTTON, outline=config.Colors.BORDER, width=2)
        c.create_oval(cx-8, cy-8, cx+8, cy+8,
                     fill=config.Colors.ACCENT, outline="")

        for angle in [0, 60, 120, 180, 240, 300]:
            rad = math.radians(angle)
            x1 = cx + (r-8) * math.cos(rad)
            y1 = cy + (r-8) * math.sin(rad)
            x2 = cx + (r-2) * math.cos(rad)
            y2 = cy + (r-2) * math.sin(rad)
            c.create_line(x1, y1, x2, y2, fill=config.Colors.TEXT_DIM, width=1)

        # Marcas
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            rad = math.radians(angle)
            x1 = cx + (r-15) * math.cos(rad)
            y1 = cy + (r-15) * math.sin(rad)
            x2 = cx + (r-5) * math.cos(rad)
            y2 = cy + (r-5) * math.sin(rad)
            c.create_line(x1, y1, x2, y2, fill=config.Colors.TEXT_DIM, width=2)

    def _build_config_panel(self):
        """Build right configuration panel."""
        for w in self.right_panel.winfo_children():
            w.destroy()

        if self._detecting:
            self._stop_detection(confirmed=False)
        self._manual_open = False

        if self.current_control is None:
            outer = tk.Frame(self.right_panel, bg=config.Colors.BG_CARD)
            outer.pack(expand=True)
            tk.Label(outer, text="← Select a control",
                    bg=config.Colors.BG_CARD, fg=config.Colors.TEXT_DIM,
                    font=("Segoe UI", 14)).pack()
            tk.Label(outer,
                    text="Click a button or knob action\nto view and edit its shortcut",
                    bg=config.Colors.BG_CARD, fg=config.Colors.TEXT_DIM,
                    font=("Segoe UI", 10), justify=tk.CENTER).pack(pady=8)
            return

        action_byte, name = self.current_control

        # ── Header ──
        hdr = tk.Frame(self.right_panel, bg=config.Colors.BG_CARD)
        hdr.pack(fill=tk.X, padx=20, pady=(18, 2))
        tk.Label(hdr, text=name,
                bg=config.Colors.BG_CARD, fg=config.Colors.TEXT,
                font=("Segoe UI", 16, "bold")).pack(side=tk.LEFT)
        tk.Frame(self.right_panel, bg=config.Colors.BORDER, height=1).pack(
            fill=tk.X, padx=20, pady=(6, 14))

        # ── Current shortcut chip ──
        chip_frame = tk.Frame(self.right_panel, bg=config.Colors.BG_CARD)
        chip_frame.pack(fill=tk.X, padx=20, pady=(0, 4))
        tk.Label(chip_frame, text="CURRENT SHORTCUT",
                bg=config.Colors.BG_CARD, fg=config.Colors.TEXT_DIM,
                font=("Segoe UI", 8, "bold")).pack(anchor=tk.W)

        chip_row = tk.Frame(chip_frame, bg=config.Colors.BG_BUTTON)
        chip_row.pack(fill=tk.X, pady=(4, 0))

        self._shortcut_chip = tk.Label(
            chip_row, text=self._shortcut_summary(action_byte),
            bg=config.Colors.BG_BUTTON, fg=config.Colors.TEXT,
            font=("Consolas", 12), anchor=tk.W, padx=10, pady=8)
        self._shortcut_chip.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(chip_row, text="Clear",
                  bg=config.Colors.BG_BUTTON, fg=config.Colors.TEXT_DIM,
                  activebackground=config.Colors.BG_BUTTON,
                  activeforeground=config.Colors.ERROR,
                  font=("Segoe UI", 8), relief=tk.FLAT, bd=0,
                  cursor="hand2", padx=8,
                  command=self._clear_keys).pack(side=tk.RIGHT)

        tk.Frame(self.right_panel, bg=config.Colors.BORDER, height=1).pack(
            fill=tk.X, padx=20, pady=(12, 0))

        # ── Auto-detect section (collapsible) ──
        self._detect_frame = tk.Frame(self.right_panel, bg=config.Colors.BG_CARD)
        self._detect_frame.pack(fill=tk.X, padx=20, pady=(10, 0))

        # Section header row with left accent bar
        detect_hdr = tk.Frame(self._detect_frame, bg=config.Colors.BG_CARD)
        detect_hdr.pack(fill=tk.X)
        tk.Frame(detect_hdr, bg=config.Colors.ACCENT, width=3).pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))

        self._detect_toggle_btn = tk.Button(
            detect_hdr,
            text="▶  Auto Detect",
            bg=config.Colors.BG_CARD, fg=config.Colors.ACCENT,
            activebackground=config.Colors.BG_CARD,
            activeforeground=config.Colors.ACCENT_SECONDARY,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, cursor="hand2", bd=0, anchor=tk.W,
            command=self._toggle_detection)
        self._detect_toggle_btn.pack(fill=tk.X)

        # Helper text always visible under the toggle
        self._detect_hint = tk.Label(
            self._detect_frame,
            text="  Click to start listening for key presses",
            bg=config.Colors.BG_CARD, fg=config.Colors.TEXT_DIM,
            font=("Segoe UI", 8), anchor=tk.W)
        self._detect_hint.pack(fill=tk.X)

        self._detect_body = tk.Frame(self._detect_frame, bg=config.Colors.BG_BUTTON)

        inner = tk.Frame(self._detect_body, bg=config.Colors.BG_BUTTON)
        inner.pack(fill=tk.X, padx=12, pady=10)

        # Status indicator row
        status_row = tk.Frame(inner, bg=config.Colors.BG_BUTTON)
        status_row.pack(fill=tk.X, pady=(0, 6))
        self._detect_status_dot = tk.Label(
            status_row, text="●  Listening...",
            bg=config.Colors.BG_BUTTON, fg=config.Colors.SUCCESS,
            font=("Segoe UI", 9, "bold"))
        self._detect_status_dot.pack(side=tk.LEFT)

        self._detect_display = tk.Label(
            inner, text="— press a key —",
            bg=config.Colors.BG_BUTTON, fg=config.Colors.TEXT_DIM,
            font=("Segoe UI", 16, "bold"))
        self._detect_display.pack(anchor=tk.W, pady=(0, 8))

        det_btns = tk.Frame(inner, bg=config.Colors.BG_BUTTON)
        det_btns.pack(fill=tk.X)
        self._detect_confirm_btn = ttk.Button(
            det_btns, text="✓  Confirm  (Enter)",
            style="Accent.TButton",
            command=lambda: self._stop_detection(confirmed=True))
        self._detect_confirm_btn.pack(side=tk.LEFT, padx=(0, 8))
        self._detect_confirm_btn.config(state=tk.DISABLED)
        ttk.Button(det_btns, text="✕  Cancel  (Esc)",
                   style="Secondary.TButton",
                   command=lambda: self._stop_detection(confirmed=False)).pack(side=tk.LEFT)

        tk.Frame(self.right_panel, bg=config.Colors.BORDER, height=1).pack(
            fill=tk.X, padx=20, pady=(10, 0))

        # ── Manual section (collapsible) ──
        self._manual_frame = tk.Frame(self.right_panel, bg=config.Colors.BG_CARD)
        self._manual_frame.pack(fill=tk.X, padx=20, pady=(10, 4))

        # Section header row with left accent bar
        manual_hdr = tk.Frame(self._manual_frame, bg=config.Colors.BG_CARD)
        manual_hdr.pack(fill=tk.X)
        tk.Frame(manual_hdr, bg=config.Colors.ACCENT, width=3).pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))

        self._manual_toggle_btn = tk.Button(
            manual_hdr,
            text="▶  Manual",
            bg=config.Colors.BG_CARD, fg=config.Colors.ACCENT,
            activebackground=config.Colors.BG_CARD,
            activeforeground=config.Colors.ACCENT_SECONDARY,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, cursor="hand2", bd=0, anchor=tk.W,
            command=self._toggle_manual)
        self._manual_toggle_btn.pack(fill=tk.X)

        self._manual_body = tk.Frame(self._manual_frame, bg=config.Colors.BG_BUTTON)
        self._build_manual_body(self._manual_body)

    def _mark_dirty(self):
        """Signal unsaved changes — turn Save button yellow."""
        self._config_dirty = True
        if hasattr(self, '_save_btn') and self._save_btn.winfo_exists():
            self._save_btn.config(
                bg="#e5c07b", fg=config.Colors.BG_DARK,
                text="↑ Save to Device")

    def _mark_clean(self):
        """Config saved — turn Save button green briefly, then normal."""
        self._config_dirty = False
        if hasattr(self, '_save_btn') and self._save_btn.winfo_exists():
            self._save_btn.config(
                bg=config.Colors.SUCCESS, fg=config.Colors.BG_DARK,
                text="✓ Saved")
            self.root.after(2000, lambda: (
                self._save_btn.config(
                    bg=config.Colors.BG_BUTTON, fg=config.Colors.TEXT,
                    text="Save to Device")
                if self._save_btn.winfo_exists() else None))

    def _shortcut_summary(self, action_byte):
        """Return a one-line human-readable summary of the current shortcut."""
        seq = self.current_config.get(action_byte, [])
        if not seq:
            return "  (none)"
        parts = []
        for mod, key in seq:
            if mod == 0xFE:  # multimedia
                label = next((n for n, v in config.MEDIA_KEYS.items()
                              if v["b1"] == key), f"Media({key})")
                parts.append(label)
            else:
                mod_str = self._modifier_str(mod)
                key_str = config.KEYCODE_NAMES.get(key, f"Key{key}")
                parts.append(f"{mod_str}+{key_str}" if mod_str else key_str)
        return "  " + "  →  ".join(parts)

    def _refresh_shortcut_chip(self):
        """Refresh the current-shortcut chip label after an edit."""
        if hasattr(self, '_shortcut_chip') and self._shortcut_chip.winfo_exists():
            action_byte, _ = self.current_control
            self._shortcut_chip.config(text=self._shortcut_summary(action_byte))

    # ── Cascading key data ────────────────────────────────────────────────
    # Maps (modifier_name, group_name) -> [(label, hid_code), ...]
    # modifier_name is one of: none, Ctrl, Shift, Alt, AltGr, Win
    # For Multimedia group, modifier is ignored.
    _KEY_GROUPS = {
        "Letters": [(c, config.KEYCODES[c]) for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"],
        "F-keys":  [(f"F{i}", config.KEYCODES[f"F{i}"]) for i in range(1, 13)],
        "Nav":     [(k, config.KEYCODES[k]) for k in (
                        "ArrowUp","ArrowDown","ArrowLeft","ArrowRight",
                        "Home","End","PgUp","PgDn",
                        "Insert","Del","Esc","Tab","Enter","Backspace","Space")],
        "Numpad":  [(k, config.KEYCODES[k]) for k in (
                        "Num0","Num1","Num2","Num3","Num4",
                        "Num5","Num6","Num7","Num8","Num9",
                        "NumAdd","NumSub","NumMul","NumDiv","NumDec","NumEnter")],
        # Symbols: base keys — label changes with modifier
        "Symbols": [(lbl, config.KEYCODES[key]) for lbl, key in [
            ("-","-"), ("=","="), ("[","["), ("]","]"),
            ("\\", "Backslash"), (";",";"), ("'","Apostrophe"),
            ("`","Grave"), (",",","), (".","."), ("/","/"),
        ] if key in config.KEYCODES],
        "Multimedia": [(k, 0xFE00 | v["b1"]) for k, v in config.MEDIA_KEYS.items()],
    }
    # Shift layer labels for Symbols
    _SYMBOLS_SHIFT = {
        "-":"_", "=":"+", "[":"{", "]":"}", "\\": "|",
        ";":":", "'":'"', "`":"~", ",":"<", ".":">", "/":"?",
    }
    _MODIFIERS = ["none", "Ctrl", "Shift", "Alt", "AltGr", "Win"]
    _MOD_BYTES = {
        "none": 0,
        "Ctrl": config.Modifier.CTRL,
        "Shift": config.Modifier.SHIFT,
        "Alt": config.Modifier.ALT,
        "AltGr": config.Modifier.RIGHT_ALT,
        "Win": config.Modifier.WIN,
    }

    def _build_manual_body(self, parent):
        """Manual shortcut builder: chips at top, 3-dropdown cascade, optional Composed."""
        bg = config.Colors.BG_BUTTON
        inner = tk.Frame(parent, bg=bg)
        inner.pack(fill=tk.X, padx=12, pady=10)

        lbl_kw = dict(bg=bg, fg=config.Colors.TEXT_DIM, font=("Segoe UI", 8, "bold"))
        cb_kw  = dict(state="readonly", style="Modern.TCombobox")

        # ── 1. Shortcut chips (current assignment) ──
        tk.Label(inner, text="ASSIGNED SHORTCUT", **lbl_kw).pack(anchor=tk.W)
        self._seq_chips_frame = tk.Frame(inner, bg=bg)
        self._seq_chips_frame.pack(fill=tk.X, pady=(4, 10))

        tk.Frame(inner, bg=config.Colors.BORDER, height=1).pack(fill=tk.X, pady=(0, 10))

        # ── 2. Single row: Modifier ▶ Group ▶ Key ▶ [+ Add] ──
        tk.Label(inner, text="ADD KEY", **lbl_kw).pack(anchor=tk.W, pady=(0, 6))

        pick_row = tk.Frame(inner, bg=bg)
        pick_row.pack(fill=tk.X, pady=(0, 4))

        self._man_mod_var = tk.StringVar(value="none")
        self._man_mod_cb = ttk.Combobox(
            pick_row, textvariable=self._man_mod_var,
            values=self._MODIFIERS, width=7, **cb_kw)
        self._man_mod_cb.pack(side=tk.LEFT, padx=(0, 4))
        self._man_mod_cb.bind("<<ComboboxSelected>>", lambda e: self._man_cascade())

        tk.Label(pick_row, text="+", bg=bg, fg=config.Colors.TEXT_DIM,
                font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 4))

        self._man_grp_var = tk.StringVar(value="Letters")
        self._man_grp_cb = ttk.Combobox(
            pick_row, textvariable=self._man_grp_var,
            values=list(self._KEY_GROUPS.keys()), width=10, **cb_kw)
        self._man_grp_cb.pack(side=tk.LEFT, padx=(0, 4))
        self._man_grp_cb.bind("<<ComboboxSelected>>", lambda e: self._man_cascade())

        tk.Label(pick_row, text="/", bg=bg, fg=config.Colors.TEXT_DIM,
                font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 4))

        self._man_key_var = tk.StringVar()
        self._man_key_cb = ttk.Combobox(
            pick_row, textvariable=self._man_key_var,
            values=[], width=10, **cb_kw)
        self._man_key_cb.pack(side=tk.LEFT, padx=(0, 8))

        ttk.Button(pick_row, text="+ Add",
                   style="Accent.TButton",
                   command=self._manual_add_key).pack(side=tk.LEFT)
        tk.Label(pick_row, text=f"max {config.MAX_SEQUENCE_LENGTH}",
                bg=bg, fg=config.Colors.TEXT_DIM,
                font=("Segoe UI", 7)).pack(side=tk.LEFT, padx=(6, 0))

        # ── 3. Composed toggle ──
        comp_toggle_row = tk.Frame(inner, bg=bg)
        comp_toggle_row.pack(fill=tk.X, pady=(10, 0))
        self._man_composed = tk.BooleanVar(value=False)
        tk.Checkbutton(
            comp_toggle_row, text="Composed key  (add modifier + key in one click)",
            variable=self._man_composed,
            bg=bg, fg=config.Colors.TEXT_DIM,
            selectcolor=bg,
            activebackground=bg, activeforeground=config.Colors.TEXT,
            font=("Segoe UI", 8), relief=tk.FLAT, bd=0,
            command=self._man_toggle_composed).pack(side=tk.LEFT)

        # Composed sub-panel (hidden by default)
        self._man_composed_frame = tk.Frame(inner, bg=bg)

        pick_row2 = tk.Frame(self._man_composed_frame, bg=bg)
        pick_row2.pack(fill=tk.X, pady=(6, 0))

        self._man_comp_mod_var = tk.StringVar(value="none")
        cm = ttk.Combobox(pick_row2, textvariable=self._man_comp_mod_var,
                          values=self._MODIFIERS, width=7, **cb_kw)
        cm.pack(side=tk.LEFT, padx=(0, 4))
        cm.bind("<<ComboboxSelected>>", lambda e: self._man_comp_cascade())

        tk.Label(pick_row2, text="+", bg=bg, fg=config.Colors.TEXT_DIM,
                font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 4))

        self._man_comp_grp_var = tk.StringVar(value="Letters")
        cg = ttk.Combobox(pick_row2, textvariable=self._man_comp_grp_var,
                          values=list(self._KEY_GROUPS.keys()), width=10, **cb_kw)
        cg.pack(side=tk.LEFT, padx=(0, 4))
        cg.bind("<<ComboboxSelected>>", lambda e: self._man_comp_cascade())

        tk.Label(pick_row2, text="/", bg=bg, fg=config.Colors.TEXT_DIM,
                font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 4))

        self._man_comp_key_var = tk.StringVar()
        self._man_comp_key_cb = ttk.Combobox(
            pick_row2, textvariable=self._man_comp_key_var,
            values=[], width=10, **cb_kw)
        self._man_comp_key_cb.pack(side=tk.LEFT)

        # Populate
        self._man_cascade()
        self._man_comp_cascade()
        self._refresh_seq_chips()

    def _man_cascade(self):
        """Regenerate Key dropdown based on current Modifier + Group."""
        grp = self._man_grp_var.get()
        mod = self._man_mod_var.get()
        labels = self._key_labels_for(grp, mod)
        self._man_key_cb.config(values=labels)
        if labels:
            self._man_key_var.set(labels[0])
        # Disable Modifier if Multimedia
        state = "disabled" if grp == "Multimedia" else "readonly"
        self._man_mod_cb.config(state=state)
        if grp == "Multimedia":
            self._man_mod_var.set("none")

    def _man_comp_cascade(self):
        """Regenerate Composed Key dropdown."""
        grp = self._man_comp_grp_var.get()
        mod = self._man_comp_mod_var.get()
        labels = self._key_labels_for(grp, mod)
        self._man_comp_key_cb.config(values=labels)
        if labels:
            self._man_comp_key_var.set(labels[0])
        state = "disabled" if grp == "Multimedia" else "readonly"
        if grp == "Multimedia":
            self._man_comp_mod_var.set("none")

    def _key_labels_for(self, grp, mod):
        """Return display labels for the Key dropdown given group and modifier."""
        entries = self._KEY_GROUPS.get(grp, [])
        if grp == "Symbols" and mod == "Shift":
            return [self._SYMBOLS_SHIFT.get(lbl, lbl) for lbl, _ in entries]
        return [lbl for lbl, _ in entries]

    def _man_toggle_composed(self):
        """Show/hide the Composed sub-panel."""
        if self._man_composed.get():
            self._man_composed_frame.pack(fill=tk.X, pady=(0, 4))
        else:
            self._man_composed_frame.pack_forget()

    def _on_manual_type_changed(self):
        pass  # replaced by cascade system

    def _toggle_manual(self):
        """Expand/collapse the manual section."""
        if self._manual_open:
            self._manual_body.pack_forget()
            self._manual_toggle_btn.config(text="▶  Manual")
            self._manual_open = False
        else:
            if self._detecting:
                self._stop_detection(confirmed=False)
            self._manual_body.pack(fill=tk.X, pady=(4, 0))
            self._manual_toggle_btn.config(text="▼  Manual")
            self._manual_open = True

    def _manual_add_key(self):
        """Add entry/entries from the 3-dropdown cascade to the sequence."""
        if not self.current_control:
            return
        action_byte, _ = self.current_control
        seq = self.current_config.get(action_byte, [])

        entries_to_add = [self._resolve_manual_entry(
            self._man_mod_var.get(), self._man_grp_var.get(), self._man_key_var.get())]

        if self._man_composed.get():
            entries_to_add.append(self._resolve_manual_entry(
                self._man_comp_mod_var.get(), self._man_comp_grp_var.get(),
                self._man_comp_key_var.get()))

        for entry in entries_to_add:
            if entry is None:
                continue
            if len(seq) >= config.MAX_SEQUENCE_LENGTH:
                break
            seq.append(entry)

        self.current_config[action_byte] = seq
        self._refresh_keys_list()
        self._refresh_seq_chips()
        self._refresh_shortcut_chip()
        self._mark_dirty()

    def _resolve_manual_entry(self, mod_name, grp, key_label):
        """Resolve (mod_byte, hid_code) from dropdown selections."""
        if not key_label:
            return None
        entries = self._KEY_GROUPS.get(grp, [])
        if grp == "Multimedia":
            for lbl, code in entries:
                if lbl == key_label:
                    return (0xFE, code & 0xFF)
            return None
        if grp == "Symbols" and mod_name == "Shift":
            reverse = {v: k for k, v in self._SYMBOLS_SHIFT.items()}
            base_label = reverse.get(key_label, key_label)
        else:
            base_label = key_label
        hid_code = next((code for lbl, code in entries if lbl == base_label), None)
        if hid_code is None:
            hid_code = config.KEYCODES.get(base_label)
        if hid_code is None:
            return None
        mod_byte = self._MOD_BYTES.get(mod_name, 0)
        return (mod_byte, hid_code)

    def _refresh_seq_chips(self):
        """Rebuild the sequence chip row in the manual panel."""
        if not hasattr(self, '_seq_chips_frame') or \
                not self._seq_chips_frame.winfo_exists():
            return
        for w in self._seq_chips_frame.winfo_children():
            w.destroy()
        if not self.current_control:
            return
        action_byte, _ = self.current_control
        seq = self.current_config.get(action_byte, [])
        bg = config.Colors.BG_BUTTON
        if not seq:
            tk.Label(self._seq_chips_frame, text="(empty)",
                    bg=bg, fg=config.Colors.TEXT_DIM,
                    font=("Segoe UI", 8)).pack(side=tk.LEFT)
            return
        for i, (mod, key) in enumerate(seq):
            if mod == 0xFE:
                label = next((n for n, v in config.MEDIA_KEYS.items()
                              if v["b1"] == key), f"Media({key})")
            else:
                mod_str = self._modifier_str(mod)
                key_str = config.KEYCODE_NAMES.get(key, f"Key{key}")
                label = f"{mod_str}+{key_str}" if mod_str else key_str
            chip = tk.Frame(self._seq_chips_frame,
                           bg=config.Colors.BG_CARD,
                           highlightthickness=1,
                           highlightbackground=config.Colors.BORDER)
            chip.pack(side=tk.LEFT, padx=(0, 4))
            tk.Label(chip, text=label,
                    bg=config.Colors.BG_CARD, fg=config.Colors.TEXT,
                    font=("Segoe UI", 8), padx=6, pady=3).pack(side=tk.LEFT)
            idx = i
            tk.Button(chip, text="×",
                     bg=config.Colors.BG_CARD, fg=config.Colors.TEXT_DIM,
                     activebackground=config.Colors.BG_CARD,
                     activeforeground=config.Colors.ERROR,
                     font=("Segoe UI", 8), relief=tk.FLAT, bd=0,
                     cursor="hand2", padx=2,
                     command=lambda ix=idx: self._remove_chip(ix)).pack(side=tk.LEFT)

    def _remove_chip(self, idx):
        """Remove one chip from the sequence by index."""
        if not self.current_control:
            return
        action_byte, _ = self.current_control
        seq = self.current_config.get(action_byte, [])
        if 0 <= idx < len(seq):
            seq.pop(idx)
            self.current_config[action_byte] = seq
            self._refresh_keys_list()
            self._refresh_seq_chips()
            self._refresh_shortcut_chip()
            self._mark_dirty()

    def _select_control(self, action_byte, name):
        """Select a control — highlight device visual, rebuild right panel."""
        self.current_control = (action_byte, name)
        self._update_device_highlight(action_byte)
        self._build_config_panel()
        # Both sections stay collapsed — CURRENT SHORTCUT already shows local config

    def _refresh_keys_list(self):
        """Update the sequence listbox in the UI."""
        if not hasattr(self, 'keys_listbox') or not self.current_control:
            return
        action_byte, _ = self.current_control
        sequence = self.current_config.get(action_byte, [])
        self.keys_listbox.delete(0, tk.END)
        if not sequence:
            self.keys_listbox.insert(tk.END, "  (empty)")
            self.keys_listbox.itemconfig(0, {"fg": config.Colors.TEXT_DIM})
            return
        for i, (mod, key) in enumerate(sequence):
            if mod == 0xFE:  # multimedia sentinel
                name = next((n for n, v in config.MEDIA_KEYS.items()
                             if v["b1"] == key), f"Media({key})")
                text = f"  {i+1}.  [Multimedia]  {name}"
            else:
                mod_str = self._modifier_str(mod)
                key_str = config.KEYCODE_NAMES.get(key, f"Key{key}")
                text = f"  {i+1}.  {mod_str}+{key_str}" if mod_str else f"  {i+1}.  {key_str}"
            self.keys_listbox.insert(tk.END, text)

    def _modifier_str(self, mod_byte):
        """Convertir byte de modifier a string legible."""
        parts = []
        if mod_byte & (config.Modifier.CTRL | config.Modifier.RIGHT_CTRL):
            parts.append("Ctrl")
        if mod_byte & (config.Modifier.SHIFT | config.Modifier.RIGHT_SHIFT):
            parts.append("Shift")
        if mod_byte & (config.Modifier.ALT | config.Modifier.RIGHT_ALT):
            parts.append("Alt")
        if mod_byte & (config.Modifier.WIN | config.Modifier.RIGHT_WIN):
            parts.append("Win")
        return " + ".join(parts)

    # ── Detección inline colapsable ──────────────────────────────────────

    def _toggle_detection(self):
        """Expandir o colapsar el panel de detección."""
        if self._detecting:
            self._stop_detection(confirmed=False)
        else:
            self._start_detection()

    def _start_detection(self):
        """Abrir panel y arrancar KeyboardDetector."""
        if not self.current_control:
            return
        self._detecting = True
        self._pending_sequence = []

        self._detect_toggle_btn.config(text="▼  Auto Detect")
        if hasattr(self, '_detect_hint') and self._detect_hint.winfo_exists():
            self._detect_hint.config(
                text="  ● Listening — press keys now",
                fg=config.Colors.SUCCESS)
        self._detect_body.pack(fill=tk.X, pady=(6, 0))
        self._detect_display.config(text="— press a key —", fg=config.Colors.TEXT_DIM)
        self._detect_confirm_btn.config(state=tk.DISABLED)

        self._detector = KeyboardDetector()
        self._detector.start(
            on_key=self._on_key_detected,
            on_stop=self._on_detection_stop,
        )

    def _on_key_detected(self, mod_byte, hid_code, display):
        """Llamado desde hilo pynput — usar root.after para actualizar UI."""
        def update():
            if not self._detecting:
                return
            pair = (mod_byte, hid_code)
            if pair not in self._pending_sequence:
                if len(self._pending_sequence) < config.MAX_SEQUENCE_LENGTH:
                    self._pending_sequence.append(pair)
            self._detect_display.config(text=display, fg=config.Colors.ACCENT)
            self._detect_confirm_btn.config(state=tk.NORMAL)
        self.root.after(0, update)

    def _on_detection_stop(self, confirmed):
        """Llamado desde hilo pynput al presionar Enter o Esc."""
        self.root.after(0, lambda: self._stop_detection(confirmed=confirmed))

    def _stop_detection(self, confirmed):
        """Detener detección y opcionalmente guardar resultado."""
        if self._detector:
            self._detector.stop()
            self._detector = None

        self._detecting = False

        if confirmed and self._pending_sequence and self.current_control:
            action_byte, _ = self.current_control
            self.current_config[action_byte] = list(self._pending_sequence)
            self._refresh_keys_list()
            self._refresh_shortcut_chip()
            self._mark_dirty()

        self._pending_sequence = []

        if hasattr(self, '_detect_toggle_btn') and self._detect_toggle_btn.winfo_exists():
            self._detect_toggle_btn.config(text="▶  Auto Detect")
        if hasattr(self, '_detect_hint') and self._detect_hint.winfo_exists():
            self._detect_hint.config(
                text="  Click to start listening for key presses",
                fg=config.Colors.TEXT_DIM)
        if hasattr(self, '_detect_body') and self._detect_body.winfo_exists():
            self._detect_body.pack_forget()

    # ── Edición de lista ─────────────────────────────────────────────────

    def _remove_key(self):
        """Eliminar tecla seleccionada de la lista."""
        if not self.current_control:
            return
        selection = self.keys_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        action_byte, _ = self.current_control
        seq = self.current_config.get(action_byte, [])
        if 0 <= idx < len(seq):
            seq.pop(idx)
            self._refresh_keys_list()
            self._refresh_shortcut_chip()
            self._mark_dirty()

    def _clear_keys(self):
        """Clear all keys for the current control."""
        if not self.current_control:
            return
        action_byte, _ = self.current_control
        self.current_config[action_byte] = []
        self._refresh_keys_list()
        self._refresh_shortcut_chip()
        self._mark_dirty()

    def _save_to_device(self):
        """Guardar configuracion actual en el dispositivo HID."""
        if not self.device_connected:
            messagebox.showwarning("Sin dispositivo", "El dispositivo no esta conectado.")
            return

        try:
            with HidDevice(self.device_path) as dev:
                for action_byte, sequence in self.current_config.items():
                    dev.send_config(action_byte=action_byte,
                                   key_sequence=sequence)
                    time.sleep(0.1)  # Pequena pausa entre envios

            self._mark_clean()
            messagebox.showinfo("Saved", "Configuration saved to device.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def _save_preset(self):
        """Guardar configuracion actual como archivo JSON."""
        path = filedialog.asksaveasfilename(
            initialdir=self.presets_dir,
            defaultextension=".json",
            filetypes=[("Preset JSON", "*.json")],
            title="Guardar Preset"
        )
        if not path:
            return

        data = {
            "name": os.path.splitext(os.path.basename(path))[0],
            "config": {str(k): [(m, key) for m, key in v]
                       for k, v in self.current_config.items()}
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        messagebox.showinfo("Guardado", f"Preset guardado en:\n{path}")

    def _load_preset(self):
        """Cargar configuracion desde archivo JSON."""
        path = filedialog.askopenfilename(
            initialdir=self.presets_dir,
            defaultextension=".json",
            filetypes=[("Preset JSON", "*.json")],
            title="Cargar Preset"
        )
        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            loaded = data.get("config", {})
            for k_str, seq in loaded.items():
                action_byte = int(k_str)
                self.current_config[action_byte] = [(m, key) for m, key in seq]

            if self.current_control:
                self._refresh_shortcut_chip()
                self._refresh_seq_chips()
            self._refresh_keys_list()
            self._mark_dirty()
            messagebox.showinfo("Cargado", f"Preset '{data.get('name', 'unknown')}' cargado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar: {e}")

    def _check_device(self):
        """Verificar si el dispositivo esta conectado."""
        self.status_label.config(text="● Verificando...", fg=config.Colors.TEXT_DIM)
        self.root.update_idletasks()
        ok, info = test_connection()
        if ok:
            self.device_connected = True
            self.device_path = info
            self.status_label.config(text="● Conectado", fg=config.Colors.SUCCESS)
        else:
            self.device_connected = False
            self.device_path = None
            self.status_label.config(text="● Sin dispositivo", fg=config.Colors.ERROR)


# ============================================
# PUNTO DE ENTRADA
# ============================================
def main():
    root = tk.Tk()
    root.configure(bg=config.Colors.BG_DARK)

    # Icono (si existe)
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    app = MiniConfiguratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
