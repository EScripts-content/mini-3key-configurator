# -*- coding: utf-8 -*-
"""
UI Panels — Construcción de todos los paneles de la interfaz Mini Configurator.
Separado de la lógica de negocio. No contiene callbacks de lógica.
"""

import tkinter as tk
from tkinter import ttk
import math
import config
from ui_styles import draw_cta_btn


class UIBuilder:
    """Constructs all panels of the Mini Configurator UI.
    
    All UI elements are stored as instance attributes.
    The 'app' reference provides callbacks to the main business logic.
    """

    # ── Cascading key data ────────────────────────────────────────────────
    KEY_GROUPS = {
        "Letters":   [(c, config.KEYCODES[c]) for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"],
        "F-keys":    [(f"F{i}", config.KEYCODES[f"F{i}"]) for i in range(1, 13)],
        "Nav":       [(k, config.KEYCODES[k]) for k in (
                         "ArrowUp","ArrowDown","ArrowLeft","ArrowRight",
                         "Home","End","PgUp","PgDn",
                         "Insert","Del","Esc","Tab","Enter","Backspace","Space")],
        "Numpad":    [(k, config.KEYCODES[k]) for k in (
                         "Num0","Num1","Num2","Num3","Num4",
                         "Num5","Num6","Num7","Num8","Num9",
                         "NumAdd","NumSub","NumMul","NumDiv","NumDec","NumEnter")],
        "Symbols":   [(char, config.KEYCODES[base]) for char, base in [
                         ("-", "-"), ("_", "-"),
                         ("=", "="), ("+", "="),
                         ("[", "["), ("{", "["),
                         ("]", "]"), ("}", "]"),
                         ("\\", "\\"), ("|", "\\"),
                         (";", ";"), (":", ";"),
                         ("'", "'"), ('"', "'"),
                         ("`", "`"), ("~", "`"),
                         (",", ","), ("<", ","),
                         (".", "."), (">", "."),
                         ("/", "/"), ("?", "/"),
                     ] if base in config.KEYCODES],
        "Multimedia": [(k, 0xFE00 | v["b1"]) for k, v in config.MEDIA_KEYS.items()],
    }
    SYMBOLS_NEED_SHIFT = {"_", "+", "{", "}", "|", ":", '"', "~", "<", ">", "?"}

    MODIFIER_NAMES = ["none", "Ctrl", "Shift", "Alt", "AltGr", "Win"]
    MOD_BYTES = {
        "none": 0,
        "Ctrl": config.Modifier.CTRL,
        "Shift": config.Modifier.SHIFT,
        "Alt": config.Modifier.ALT,
        "AltGr": config.Modifier.RIGHT_ALT,
        "Win": config.Modifier.WIN,
    }
    MOD_AC_MAP = {
        "ct": "Ctrl", "sh": "Shift", "al": "Alt", "wi": "Win", "ag": "AltGr",
    }

    def __init__(self, app, root):
        self.app = app  # reference to MiniConfiguratorApp (for callbacks)
        self.root = root
        self.C = config.Colors

        # Widget references to be populated by build methods
        self._dev_canvas = None
        self._dev_faces = {}
        self._dev_labels = {}
        self._dev_knob_body = None
        self._dev_knob_ring = None
        self._dev_knob_dot = None
        self._knob_tab_btns = {}
        self._knob_tabs_outer = None

        # LED panel
        self._led_toggle_btn = None
        self._led_body = None
        self._led_hdr_row = None
        self._led_current_lbl = None
        self._led_mode_btns = {}
        self._led_status = None
        self._led_panel_open = False

        # Detection panel
        self._detect_toggle_btn = None
        self._detect_hint = None
        self._detect_body = None
        self._detect_status_dot = None
        self._detect_display = None
        self._detect_confirm_btn = None
        self._detect_frame = None

        # Manual panel
        self._manual_toggle_btn = None
        self._manual_frame = None
        self._manual_body = None
        self._manual_open = False
        self._man_text_var = None
        self._man_parsing = False
        self._seq_chips_frame = None

        # ASSIGNED SHORTCUT chips row
        self._shortcut_chip = None

        # ADD SHORTCUT KEY horizontal slots
        self._man_slots_frame = None
        self._man_slot_count_lbl = None
        self._man_slots = []

        # Footer
        self._save_btn = None
        self._cancel_btn = None
        self._preset_lbl = None
        self._pill_dot_lbl = None
        self._pill_text_lbl = None

        # Config panel
        self.right_panel = None
        self.keys_listbox = None

    # ═══════════════════════════════════════════════════════════════════════
    # TOP BUILD ENTRY
    # ═══════════════════════════════════════════════════════════════════════
    def build_all(self):
        """Build the complete interface."""
        self._build_top_row()
        tk.Frame(self.root, bg=self.C.BORDER, height=1).pack(fill=tk.X)
        self._build_hero_area()
        tk.Frame(self.root, bg=self.C.BORDER, height=1).pack(fill=tk.X)
        self._build_config_panel_outer()
        tk.Frame(self.root, bg=self.C.BORDER, height=1).pack(fill=tk.X)
        self._build_footer()

    # ═══════════════════════════════════════════════════════════════════════
    # TOP ROW
    # ═══════════════════════════════════════════════════════════════════════
    def _build_top_row(self):
        top_row = tk.Frame(self.root, bg=self.C.BG_DARK)
        top_row.pack(fill=tk.X, padx=20, pady=(14, 6))

        tk.Label(top_row, text="MINI CONFIGURATOR",
                 bg=self.C.BG_DARK, fg=self.C.TEXT,
                 font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT)

        status_block = tk.Frame(top_row, bg=self.C.BG_DARK)
        status_block.pack(side=tk.RIGHT)

        pill_row = tk.Frame(status_block, bg=self.C.BG_DARK)
        pill_row.pack(anchor=tk.E)

        self._pill_dot_lbl = tk.Label(pill_row, text="●",
                                       bg=self.C.BG_DARK, fg=self.C.TEXT_DIM,
                                       font=("Segoe UI", 9))
        self._pill_dot_lbl.pack(side=tk.LEFT, padx=(0, 4))

        self._pill_text_lbl = tk.Label(pill_row, text="Verificando...",
                                        bg=self.C.BG_DARK, fg=self.C.TEXT_DIM,
                                        font=("Segoe UI", 9, "bold"))
        self._pill_text_lbl.pack(side=tk.LEFT)

        tk.Button(
            pill_row, text="↺",
            bg=self.C.BG_DARK, fg=self.C.TEXT_DIM,
            activebackground=self.C.BG_BUTTON, activeforeground=self.C.ACCENT,
            font=("Segoe UI", 11), relief=tk.FLAT, bd=0,
            cursor="hand2", padx=6, pady=0,
            command=self.app._check_device).pack(side=tk.LEFT, padx=(8, 0))

        info_text = f"VID: {config.VID:#06x}   PID: {config.PID:#06x}   Protocol: HID"
        tk.Label(status_block, text=info_text,
                 bg=self.C.BG_DARK, fg=self.C.TEXT_DIM,
                 font=("Segoe UI", 7)).pack(anchor=tk.E)
        tk.Label(status_block, text="Firmware: 1.0",
                 bg=self.C.BG_DARK, fg=self.C.TEXT_DIM,
                 font=("Segoe UI", 7)).pack(anchor=tk.E)

    # ═══════════════════════════════════════════════════════════════════════
    # HERO AREA
    # ═══════════════════════════════════════════════════════════════════════
    def _build_hero_area(self):
        hero_area = tk.Frame(self.root, bg=self.C.BG_DARK, height=200)
        hero_area.pack(fill=tk.X)
        hero_area.pack_propagate(False)

        center_wrap = tk.Frame(hero_area, bg=self.C.BG_DARK)
        center_wrap.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # LED col (left)
        led_col = tk.Frame(center_wrap, bg=self.C.BG_DARK, width=108)
        led_col.pack(side=tk.LEFT, fill=tk.Y)
        led_col.pack_propagate(False)
        self._build_led_panel(led_col)

        # Device canvas (center)
        canvas_frame = tk.Frame(center_wrap, bg=self.C.BG_DARK, width=480, height=200)
        canvas_frame.pack(side=tk.LEFT, fill=tk.Y)
        canvas_frame.pack_propagate(False)
        self._build_device_panel(canvas_frame)

        # Knob tabs (right)
        knob_col = tk.Frame(center_wrap, bg=self.C.BG_DARK, width=88)
        knob_col.pack(side=tk.LEFT, fill=tk.Y)
        knob_col.pack_propagate(False)
        self._build_knob_tabs(knob_col)

    # ═══════════════════════════════════════════════════════════════════════
    # DEVICE CANVAS
    # ═══════════════════════════════════════════════════════════════════════
    def _build_device_panel(self, parent):
        canvas = tk.Canvas(parent, bg=self.C.BG_DARK, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        self._dev_canvas = canvas
        self._dev_faces = {}
        self._dev_labels = {}

        def rrect(x1, y1, x2, y2, r, **kw):
            pts = [
                x1+r,y1, x2-r,y1, x2,y1, x2,y1+r,
                x2,y2-r, x2,y2, x2-r,y2, x1+r,y2,
                x1,y2, x1,y2-r, x1,y1+r, x1,y1,
            ]
            return canvas.create_polygon(pts, smooth=True, **kw)

        def draw(event=None):
            canvas.delete("all")
            W = canvas.winfo_width() or 700
            H = canvas.winfo_height() or 210
            C = self.C

            # Device body
            dw, dh = 460, 130
            dx = (W - dw) // 2
            dy = (H - dh) // 2

            rrect(dx+4, dy+6, dx+dw+4, dy+dh+6, 14, fill="#070809", outline="")
            rrect(dx, dy, dx+dw, dy+dh, 14, fill="#161b22", outline="#2b3440", width=2)
            rrect(dx+8, dy+8, dx+dw-8, dy+dh-8, 10, fill="#0f1318", outline="#1e2530", width=1)
            rrect(dx+12, dy+10, dx+dw-12, dy+22, 4, fill="#1e2836", outline="")

            for sx, sy in [(dx+18, dy+18), (dx+dw-18, dy+18),
                           (dx+18, dy+dh-18), (dx+dw-18, dy+dh-18)]:
                canvas.create_oval(sx-4, sy-4, sx+4, sy+4,
                                   fill="#1a1f26", outline="#2b3440", width=1)
                canvas.create_line(sx-2, sy, sx+2, sy, fill="#3a4555", width=1)
                canvas.create_line(sx, sy-2, sx, sy+2, fill="#3a4555", width=1)

            px, py = dx - 2, dy + dh//2
            rrect(px-6, py-8, px+4, py+8, 3, fill="#1a1f26", outline="#3a4555", width=1)
            canvas.create_rectangle(px-4, py-5, px+2, py+5, fill="#080a0c", outline="")

            led_y = dy + dh - 22
            led_x0 = dx + 22
            for i in range(3):
                lx = led_x0 + i * 110 + 10
                canvas.create_rectangle(lx, led_y, lx+70, led_y+4, fill="#0a1520", outline="")
                canvas.create_rectangle(lx+2, led_y+1, lx+68, led_y+3, fill="#1a3a5c", outline="")

            B, bpad = 72, 14
            by = dy + (dh - B) // 2 - 4
            bxs = [dx + 22 + i*(B + bpad) for i in range(3)]

            self._dev_faces = {}
            self._dev_labels = {}

            for i, (ab, name) in enumerate(config.CONTROLS[:3]):
                x = bxs[i]
                tag = f"ctrl_{ab}"
                canvas.create_rectangle(x+3, by+5, x+B+2, by+B+4,
                                        fill="#040608", outline="", tags=tag)
                fid = rrect(x, by, x+B, by+B, 8, fill="#c8cdd4",
                            outline="#9aa0a8", width=1, tags=tag)
                rrect(x+4, by+4, x+B-4, by+18, 4, fill="#e8ecf0", outline="", tags=tag)
                rrect(x+4, by+B-14, x+B-4, by+B-4, 3, fill="#a8aeb6", outline="", tags=tag)
                lid = canvas.create_text(x+B//2, by+B//2+2, text=str(i+1),
                                         fill="#2a2e36", font=("Segoe UI", 16, "bold"), tags=tag)
                self._dev_faces[ab] = fid
                self._dev_labels[ab] = lid
                canvas.tag_bind(tag, "<Button-1>",
                                lambda e, b=ab, n=name: self.app._select_control(b, n))
                canvas.tag_bind(tag, "<Enter>", lambda e: canvas.config(cursor="hand2"))
                canvas.tag_bind(tag, "<Leave>", lambda e: canvas.config(cursor=""))

            kr, kx, ky = 42, dx + dw - 70, dy + dh // 2
            canvas.create_oval(kx-kr-10, ky-kr-10, kx+kr+10, ky+kr+10,
                               fill="#0c1018", outline="#1e2530", width=2)
            self._dev_knob_ring = canvas.create_oval(
                kx-kr-4, ky-kr-4, kx+kr+4, ky+kr+4,
                fill="#161b22", outline="#39c0ff", width=1)
            canvas.create_oval(kx-kr, ky-kr, kx+kr, ky+kr,
                               fill="#2a3040", outline="#3a4555", width=2)
            self._dev_knob_body = canvas.create_oval(
                kx-kr+3, ky-kr+3, kx+kr-3, ky+kr-3,
                fill="#222834", outline="#2e3848", width=1)
            for a in range(0, 360, 20):
                r1, r2 = kr-10, kr-4
                rad = math.radians(a)
                canvas.create_line(kx+r1*math.cos(rad), ky+r1*math.sin(rad),
                                   kx+r2*math.cos(rad), ky+r2*math.sin(rad),
                                   fill="#333d4e", width=1)
            canvas.create_line(kx, ky, kx, ky-kr+8, fill="#e0e4ea", width=3, capstyle=tk.ROUND)
            canvas.create_oval(kx-8, ky-8, kx+8, ky+8, fill="#1a1f26", outline="#2b3440", width=1)
            self._dev_knob_dot = canvas.create_oval(kx-5, ky-5, kx+5, ky+5, fill=C.ACCENT, outline="")

            tk_knob = "ctrl_knob"
            canvas.addtag_overlapping(tk_knob, kx-kr-15, ky-kr-15, kx+kr+15, ky+kr+15)
            if config.CONTROLS[3:]:
                first_ab, first_name = config.CONTROLS[3]
                canvas.tag_bind(tk_knob, "<Button-1>",
                                lambda e, b=first_ab, n=first_name: self.app._select_control(b, n))
                canvas.tag_bind(tk_knob, "<Enter>", lambda e: canvas.config(cursor="hand2"))
                canvas.tag_bind(tk_knob, "<Leave>", lambda e: canvas.config(cursor=""))

            canvas.create_text(W//2, H-16, text="Select a control to configure",
                               fill=C.TEXT_DIM, font=("Segoe UI", 8))

        canvas.bind("<Configure>", draw)
        canvas.after(50, draw)

    def update_device_highlight(self, selected_ab):
        """Refresh canvas keycaps and knob tab buttons for selection."""
        C = self.C
        if not hasattr(self, '_dev_canvas') or not self._dev_canvas.winfo_exists():
            return
        canvas = self._dev_canvas

        for fid in self._dev_faces.values():
            canvas.itemconfig(fid, fill="#c8cdd4", outline="#9aa0a8")
        for lid in self._dev_labels.values():
            canvas.itemconfig(lid, fill="#2a2e36")
        if self._dev_knob_body:
            canvas.itemconfig(self._dev_knob_body, fill="#222834", outline="#2e3848")
        if self._dev_knob_ring:
            canvas.itemconfig(self._dev_knob_ring, outline="#39c0ff", width=1)
        if self._dev_knob_dot:
            canvas.itemconfig(self._dev_knob_dot, fill=C.ACCENT)

        for btn in self._knob_tab_btns.values():
            btn.config(bg=C.BG_BUTTON, fg=C.TEXT_DIM)

        if selected_ab in self._dev_faces:
            canvas.itemconfig(self._dev_faces[selected_ab], fill=C.ACCENT, outline=C.ACCENT_SECONDARY)
            canvas.itemconfig(self._dev_labels[selected_ab], fill=C.BG_DARK)
        elif selected_ab in self._knob_tab_btns:
            if self._dev_knob_body:
                canvas.itemconfig(self._dev_knob_body, fill="#1a3a5c", outline=C.ACCENT)
            if self._dev_knob_ring:
                canvas.itemconfig(self._dev_knob_ring, outline=C.ACCENT, width=2)
            if self._dev_knob_dot:
                canvas.itemconfig(self._dev_knob_dot, fill=C.ACCENT_SECONDARY)
            self._knob_tab_btns[selected_ab].config(bg=C.ACCENT, fg=C.BG_DARK)

    # ═══════════════════════════════════════════════════════════════════════
    # LED PANEL
    # ═══════════════════════════════════════════════════════════════════════
    def _build_led_panel(self, parent):
        C = self.C

        tk.Frame(parent, bg=C.BG_DARK).pack(side=tk.TOP, expand=True, fill=tk.Y)

        hdr_row = tk.Frame(parent, bg=C.BG_DARK)
        hdr_row.pack(side=tk.TOP, anchor=tk.E, padx=2)
        self._led_hdr_row = hdr_row

        self._led_current_lbl = tk.Label(
            hdr_row, text="", bg=C.BG_DARK, fg=C.ACCENT, font=("Segoe UI", 7))
        self._led_current_lbl.pack(side=tk.RIGHT)

        self._led_toggle_btn = tk.Button(
            hdr_row, text="▶  LIGHTING", bg=C.BG_DARK, fg=C.TEXT_DIM,
            activebackground=C.BG_DARK, activeforeground=C.ACCENT,
            font=("Segoe UI", 7, "bold"), relief=tk.FLAT, cursor="hand2", bd=0,
            anchor=tk.E, command=self.app._toggle_led_panel)
        self._led_toggle_btn.pack(side=tk.RIGHT)

        self._led_body = tk.Frame(parent, bg=C.BG_BUTTON)
        inner = tk.Frame(self._led_body, bg=C.BG_BUTTON)
        inner.pack(fill=tk.X, padx=4, pady=2)

        MODE_DESCRIPTIONS = ["Off", "Pulse", "Carousel"]
        self._led_mode_btns = {}
        for mode_idx, label in config.LED_MODE_NAMES:
            desc = MODE_DESCRIPTIONS[mode_idx] if mode_idx < len(MODE_DESCRIPTIONS) else label
            lbl = tk.Label(inner, text=desc, bg=C.BG_BUTTON, fg=C.TEXT_DIM,
                           font=("Segoe UI", 8), relief=tk.FLAT,
                           anchor=tk.E, padx=4, pady=1, cursor="hand2")
            lbl.pack(anchor=tk.E, pady=0, fill=tk.X)
            lbl.bind("<Button-1>", lambda e, m=mode_idx: self.app._set_led_mode(m))
            lbl.bind("<Enter>", lambda e, l=lbl: l.config(fg=C.TEXT))
            lbl.bind("<Leave>", lambda e, l=lbl, m=mode_idx: l.config(
                fg=C.TEXT if m == getattr(self.app, '_led_active_mode', None) else C.TEXT_DIM))
            self._led_mode_btns[mode_idx] = lbl

        self._led_status = tk.Label(self._led_body, text="", bg=C.BG_BUTTON,
                                     fg=C.TEXT_DIM, font=("Segoe UI", 7), padx=4)
        self._led_status.pack(anchor=tk.E, pady=(0, 2))
        tk.Frame(parent, bg=C.BG_DARK).pack(side=tk.TOP, expand=True, fill=tk.Y)

    def toggle_led_panel(self):
        if self._led_panel_open:
            self._led_body.pack_forget()
            self._led_toggle_btn.config(text="▶  LIGHTING")
            self._led_panel_open = False
        else:
            self._led_body.pack(anchor=tk.E, fill=tk.X, pady=(0, 2), after=self._led_hdr_row)
            self._led_toggle_btn.config(text="▼  LIGHTING")
            self._led_panel_open = True

    def update_led_btn_visuals(self, active_mode):
        C = self.C
        for mi, btn in self._led_mode_btns.items():
            if mi == active_mode:
                btn.config(fg=C.TEXT, bg=C.BG_BUTTON_ACTIVE)
            else:
                btn.config(fg=C.TEXT_DIM, bg=C.BG_BUTTON)

    # ═══════════════════════════════════════════════════════════════════════
    # KNOB TABS
    # ═══════════════════════════════════════════════════════════════════════
    def _build_knob_tabs(self, parent):
        C = self.C
        self._knob_tab_btns = {}
        ctrl_dict = dict(config.CONTROLS)

        outer = tk.Frame(parent, bg=C.BG_DARK)
        self._knob_tabs_outer = outer

        knob_info = [(13, "↺  LEFT"), (14, "●  PRESS"), (15, "↻  RIGHT")]
        for ab, cap_text in knob_info:
            name = ctrl_dict.get(ab, "Knob")
            btn = tk.Button(outer, text=cap_text, bg=C.BG_BUTTON, fg=C.TEXT_DIM,
                           activebackground=C.ACCENT, activeforeground=C.BG_DARK,
                           font=("Segoe UI", 7, "bold"), relief=tk.FLAT,
                           cursor="hand2", bd=0, padx=8, pady=4, width=7,
                           command=lambda b=ab, n=name: self.app._select_control(b, n))
            btn.pack(pady=2)
            self._knob_tab_btns[ab] = btn

    # ═══════════════════════════════════════════════════════════════════════
    # CONFIG PANEL (outer wrapper + scroll)
    # ═══════════════════════════════════════════════════════════════════════
    def _build_config_panel_outer(self):
        C = self.C
        self.right_panel = tk.Frame(self.root, bg=C.BG_DARK)
        self.right_panel.pack(fill=tk.BOTH, expand=True)

    def build_config_panel(self, current_control, current_config):
        """Build contextual editor panel. Pure UI: receives data, returns nothing.
        
        current_control: (action_byte, name) or None
        current_config: dict[action_byte, list[(mod, key)]]
        """
        C = self.C
        for w in self.right_panel.winfo_children():
            w.destroy()
        self._manual_open = False
        self._man_slots = []

        if current_control is None:
            outer = tk.Frame(self.right_panel, bg=C.BG_DARK)
            outer.pack(expand=True)
            tk.Label(outer, text="Select a control",
                     bg=C.BG_DARK, fg=C.TEXT_DIM,
                     font=("Segoe UI", 13)).pack(pady=(0, 4))
            tk.Label(outer, text="Click any button or knob action\nto view and configure its shortcut",
                     bg=C.BG_DARK, fg=C.TEXT_DIM,
                     font=("Segoe UI", 9), justify=tk.CENTER).pack()
            return

        action_byte, name = current_control

        # Scrollable container
        sc_wrap = tk.Frame(self.right_panel, bg=C.BG_DARK)
        sc_wrap.pack(fill=tk.BOTH, expand=True)
        vbar = ttk.Scrollbar(sc_wrap, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_canvas = tk.Canvas(sc_wrap, bg=C.BG_DARK, highlightthickness=0, yscrollcommand=vbar.set)
        scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vbar.config(command=scroll_canvas.yview)
        inner_root = tk.Frame(scroll_canvas, bg=C.BG_DARK)
        win_id = scroll_canvas.create_window((0, 0), window=inner_root, anchor=tk.NW)

        def _on_frame_configure(e):
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        inner_root.bind("<Configure>", _on_frame_configure)

        def _on_canvas_configure(e):
            scroll_canvas.itemconfig(win_id, width=e.width)
        scroll_canvas.bind("<Configure>", _on_canvas_configure)

        def _on_mousewheel(e):
            scroll_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        scroll_canvas.bind("<MouseWheel>", _on_mousewheel)
        inner_root.bind("<MouseWheel>", _on_mousewheel)

        # ── HEADER ────────────────────────────────────────────────────────
        hdr = tk.Frame(inner_root, bg=C.BG_DARK)
        hdr.pack(fill=tk.X, padx=16, pady=(10, 2))
        tk.Label(hdr, text=name.upper(), bg=C.BG_DARK, fg=C.TEXT,
                 font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT)
        tk.Button(hdr, text="Clear", bg=C.BG_DARK, fg=C.TEXT_DIM,
                  activebackground=C.BG_DARK, activeforeground=C.ERROR,
                  font=("Segoe UI", 8), relief=tk.FLAT, bd=0,
                  cursor="hand2", padx=4,
                  command=self.app._clear_keys).pack(side=tk.RIGHT)
        tk.Frame(inner_root, bg=C.BORDER, height=1).pack(fill=tk.X, padx=16, pady=(2, 6))

        # ── CURRENT ACTION / ASSIGNED SHORTCUT ────────────────────────────
        tk.Label(inner_root, text="ASSIGNED SHORTCUT",
                 bg=C.BG_DARK, fg=C.TEXT_DIM,
                 font=("Segoe UI", 7, "bold")).pack(anchor=tk.W, padx=16)

        card_action = tk.Frame(inner_root, bg=C.BG_CARD,
                               highlightthickness=1, highlightbackground=C.BORDER)
        card_action.pack(fill=tk.X, padx=16, pady=(3, 8))

        chips_outer = tk.Frame(card_action, bg=C.BG_CARD)
        chips_outer.pack(fill=tk.X, padx=10, pady=7)
        self._shortcut_chip = chips_outer
        self.render_keycap_chips(chips_outer, action_byte, current_config)

        # ── AUTO DETECT ───────────────────────────────────────────────────
        self._detect_frame = tk.Frame(inner_root, bg=C.BG_DARK)
        self._detect_frame.pack(fill=tk.X, padx=20, pady=(0, 6))
        detect_hdr = tk.Frame(self._detect_frame, bg=C.BG_DARK)
        detect_hdr.pack(fill=tk.X)

        self._detect_toggle_btn = tk.Button(
            detect_hdr, text="▶  AUTO DETECT", bg=C.BG_DARK, fg=C.TEXT_DIM,
            activebackground=C.BG_DARK, activeforeground=C.ACCENT,
            font=("Segoe UI", 7, "bold"), relief=tk.FLAT, cursor="hand2", bd=0,
            anchor=tk.W, command=self.app._toggle_detection)
        self._detect_toggle_btn.pack(side=tk.LEFT)

        self._detect_hint = tk.Label(
            detect_hdr, text="  press keys, confirm with Enter",
            bg=C.BG_DARK, fg=C.TEXT_DIM, font=("Segoe UI", 7))
        self._detect_hint.pack(side=tk.LEFT)

        self._detect_body = tk.Frame(self._detect_frame, bg=C.BG_CARD,
                                     highlightthickness=1, highlightbackground=C.BORDER)
        inner_det = tk.Frame(self._detect_body, bg=C.BG_CARD)
        inner_det.pack(fill=tk.X, padx=14, pady=10)

        self._detect_status_dot = tk.Label(
            inner_det, text="●  Listening...", bg=C.BG_CARD, fg=C.SUCCESS,
            font=("Segoe UI", 8, "bold"))
        self._detect_status_dot.pack(anchor=tk.W, pady=(0, 4))

        self._detect_display = tk.Label(
            inner_det, text="— press a key —", bg=C.BG_CARD, fg=C.TEXT_DIM,
            font=("Segoe UI", 14, "bold"))
        self._detect_display.pack(anchor=tk.W, pady=(0, 8))

        det_btns = tk.Frame(inner_det, bg=C.BG_CARD)
        det_btns.pack(fill=tk.X)
        self._detect_confirm_btn = ttk.Button(
            det_btns, text="✓  Confirm  (Enter)", style="Accent.TButton",
            command=lambda: self.app._stop_detection(confirmed=True))
        self._detect_confirm_btn.pack(side=tk.LEFT, padx=(0, 8))
        self._detect_confirm_btn.config(state=tk.DISABLED)
        ttk.Button(det_btns, text="✕  Cancel  (Esc)", style="Secondary.TButton",
                   command=lambda: self.app._stop_detection(confirmed=False)).pack(side=tk.LEFT)

        # ── MANUAL MODE ────────────────────────────────────────────────────
        self._manual_frame = tk.Frame(inner_root, bg=C.BG_DARK)
        self._manual_frame.pack(fill=tk.X, padx=20, pady=(0, 6))

        manual_hdr = tk.Frame(self._manual_frame, bg=C.BG_DARK)
        manual_hdr.pack(fill=tk.X)

        self._manual_toggle_btn = tk.Button(
            manual_hdr, text="▶  MANUAL MODE", bg=C.BG_DARK, fg=C.TEXT_DIM,
            activebackground=C.BG_DARK, activeforeground=C.ACCENT,
            font=("Segoe UI", 7, "bold"), relief=tk.FLAT, cursor="hand2", bd=0,
            anchor=tk.W, command=self.app._toggle_manual)
        self._manual_toggle_btn.pack(side=tk.LEFT)

        self._manual_body = tk.Frame(self._manual_frame, bg=C.BG_CARD,
                                     highlightthickness=1, highlightbackground=C.BORDER)
        self._build_manual_body_inner(self._manual_body, action_byte, current_config)

    # ═══════════════════════════════════════════════════════════════════════
    # MANUAL MODE BODY
    # ═══════════════════════════════════════════════════════════════════════
    def _build_manual_body_inner(self, parent, action_byte, current_config):
        C = self.C
        bg = C.BG_CARD
        inner = tk.Frame(parent, bg=bg)
        inner.pack(fill=tk.X, padx=12, pady=10)

        lbl_kw = dict(bg=bg, fg=C.TEXT_DIM, font=("Segoe UI", 8, "bold"))

        # ── SHORTCUT: chips + live text entry ────────────────────────────
        tk.Label(inner, text="SHORTCUT", **lbl_kw).pack(anchor=tk.W)
        self._seq_chips_frame = tk.Frame(inner, bg=bg)
        self._seq_chips_frame.pack(fill=tk.X, pady=(4, 6))
        self.refresh_seq_chips(action_byte, current_config)

        self._man_text_var = tk.StringVar()
        entry_row = tk.Frame(inner, bg=bg)
        entry_row.pack(fill=tk.X, pady=(0, 2))
        self._man_entry = ttk.Entry(entry_row, textvariable=self._man_text_var,
                                    style="Modern.TEntry", width=20)
        self._man_entry.pack(side=tk.LEFT)
        tk.Label(entry_row, text="ct→Ctrl  sh→Shift  al→Alt  wi→Win  ag→AltGr  space=key",
                 bg=bg, fg=C.TEXT_DIM, font=("Segoe UI", 7)).pack(side=tk.LEFT, padx=(4, 0))
        # Bind <KeyRelease> instead of trace — gives us control over cursor position
        self._man_entry.bind("<KeyRelease>", self._on_man_key_release)

        # ── ADD SHORTCUT KEY: horizontal slot chain ──────────────────────
        tk.Frame(inner, bg=C.BORDER, height=1).pack(fill=tk.X, pady=(0, 8))
        add_header = tk.Frame(inner, bg=bg)
        add_header.pack(fill=tk.X, pady=(0, 4))
        tk.Label(add_header, text="Add Shortcut Key", **lbl_kw).pack(side=tk.LEFT)
        self._man_slot_count_lbl = tk.Label(
            add_header, text=f"0 / {config.MAX_SEQUENCE_LENGTH}",
            bg=bg, fg=C.TEXT_DIM, font=("Segoe UI", 8))
        self._man_slot_count_lbl.pack(side=tk.RIGHT)

        self._man_slots_frame = tk.Frame(inner, bg=bg)
        self._man_slots_frame.pack(fill=tk.X, pady=(0, 4))

        # Populate slots from current sequence, or start with one empty slot
        seq = current_config.get(action_byte, [])
        if seq:
            for mod, key in seq:
                if key == 0 and mod != 0:
                    mod_name = self._byte_to_mod_name(mod)
                    self._man_add_slot("mod", mod_name, "", "", _skip_refresh=True)
                else:
                    grp, lbl = self._hid_to_group_label(key, bool(mod & config.Modifier.SHIFT))
                    self._man_add_slot("key", "none", grp, lbl, _skip_refresh=True)
        else:
            # Start with one empty slot ready to configure
            self._man_add_initial_slot()

        self._man_update_slot_count()
        self.refresh_seq_chips(action_byte, current_config)

    # ═══════════════════════════════════════════════════════════════════════
    # SHORTCUT TEXT ENTRY LIVE PARSE (KeyRelease-based, cursor-safe)
    # ═══════════════════════════════════════════════════════════════════════
    def _on_man_key_release(self, event):
        """Called on <KeyRelease>. Auto-complete + parse SHORTCUT text.
        
        The critical challenge is avoiding cursor jumps + recursive events.
        After a delete+insert, tkinter fires another <KeyRelease> event.
        We prevent reprocessing by updating _man_prev_text BEFORE the guard.
        """
        if getattr(self, '_man_parsing', False):
            return

        # Ignore navigation and modifier keys
        nav_keys = {'Left', 'Right', 'Up', 'Down', 'Home', 'End',
                    'Shift_L', 'Shift_R', 'Control_L', 'Control_R',
                    'Alt_L', 'Alt_R', 'Win_L', 'Win_R',
                    'Caps_Lock'}
        if event.keysym in nav_keys:
            return

        widget = event.widget
        text = widget.get()

        # ── Guard: skip if content didn't change ────────────────────────
        prev = getattr(self, '_man_prev_text', '')
        if text == prev:
            return
        self._man_prev_text = text

        # ── Find last word ────────────────────────────────────────────────
        stripped = text.rstrip()
        if not stripped:
            self.app._on_shortcut_text_parsed([])
            return

        words = stripped.split(' ')
        last_word = words[-1] if words else ''

        # ── If Backspace or Delete — parse and update chips in real time ─
        if event.keysym in ('BackSpace', 'Delete'):
            seq = self._tokenize_shortcut_text(text)
            self.app._on_shortcut_text_parsed(seq)
            return

        # ── Auto-complete if last word is a 2-letter abbreviation ───────
        if last_word and last_word.lower() in self.MOD_AC_MAP:
            expanded = self.MOD_AC_MAP[last_word.lower()]
            if last_word != expanded:
                last_idx = text.rfind(last_word)
                if last_idx >= 0:
                    self._man_parsing = True
                    try:
                        # Compute new text: replace just the last word
                        new_text = text[:last_idx] + expanded + text[last_idx + len(last_word):]
                        widget.delete(0, tk.END)
                        widget.insert(0, new_text)
                        # Cursor goes right after expanded word
                        widget.icursor(last_idx + len(expanded))
                        # Update prev_text to prevent the recursive KeyRelease
                        # that tkinter fires after insert
                        self._man_prev_text = widget.get()
                    finally:
                        self._man_parsing = False
                    # After autocomplete, also parse so chips update immediately
                    # (not waiting for next keystroke)
                    seq = self._tokenize_shortcut_text(new_text)
                    self.app._on_shortcut_text_parsed(seq)
                    return

        # ── Parse and update chips ──────────────────────────────────────
        seq = self._tokenize_shortcut_text(text)
        self.app._on_shortcut_text_parsed(seq)

    def _tokenize_shortcut_text(self, text):
        """Convert typed text into HID sequence list.
        Each token separated by space. First 2 chars of a token can be modifier.
        Before splitting into individual characters, checks if the whole token
        matches a valid key name (KEYCODES, KEY_GROUPS, function keys, nav keys, etc).
        """
        result = []
        tokens = text.split()
        for tok in tokens:
            if len(result) >= config.MAX_SEQUENCE_LENGTH:
                break
            # 1) Try full modifier name
            mod_byte = self.MOD_BYTES.get(tok, 0)
            if mod_byte:
                result.append((mod_byte, 0))
                continue
            # 2) Try abbreviation
            full_name = self.MOD_AC_MAP.get(tok.lower())
            if full_name:
                mod_byte = self.MOD_BYTES.get(full_name, 0)
                if mod_byte:
                    result.append((mod_byte, 0))
                    continue
            # 3) Try if the whole token is a known key name (KEYCODES or KEY_GROUPS)
            entry = self._find_key_entry_for_full_name(tok)
            if entry:
                result.append(entry)
                continue
            # 4) Check if first 2 chars form a modifier (e.g. "ct+" → ct=mod, +=key)
            if len(tok) >= 3:
                prefix = tok[:2].lower()
                remainder = tok[2:]
                full_name = self.MOD_AC_MAP.get(prefix)
                if full_name:
                    mod_byte = self.MOD_BYTES.get(full_name, 0)
                    if mod_byte:
                        result.append((mod_byte, 0))
                        # Process remainder chars as individual keys
                        for ch in remainder:
                            if len(result) >= config.MAX_SEQUENCE_LENGTH:
                                break
                            entry = self._find_key_entry_for_token(ch)
                            if entry:
                                result.append(entry)
                        continue
            # 5) Every character is an individual key
            for ch in tok:
                if len(result) >= config.MAX_SEQUENCE_LENGTH:
                    break
                entry = self._find_key_entry_for_token(ch)
                if entry:
                    result.append(entry)
        return result

    def _find_key_entry_for_full_name(self, tok):
        """Try to match the whole token as a known key name.
        Returns (mod_byte, hid_code) or None.
        """
        # Check KEYCODES first (handles "Enter", "Space", "F1".."F12", etc.)
        if tok in config.KEYCODES:
            return (0, config.KEYCODES[tok])
        # Check all KEY_GROUPS (except Multimedia — needs 0xFE sentinel)
        for grp, entries in self.KEY_GROUPS.items():
            if grp == "Multimedia":
                continue
            for lbl, code in entries:
                if lbl == tok:
                    mod = config.Modifier.SHIFT if lbl in self.SYMBOLS_NEED_SHIFT else 0
                    return (mod, code & 0xFF)
        # Check KEYCODES case-insensitive
        upper = tok.upper()
        if upper in config.KEYCODES:
            return (0, config.KEYCODES[upper])
        return None

    def _find_key_entry_for_token(self, tok):
        """Find (mod_byte, hid_code) for a single character token.
        This is only called AFTER checking full-name matches,
        so single characters like '+', '-', 'A', '?' are resolved here.
        """
        upper = tok.upper()
        # Exact match in KEYCODES (for single letters, numbers, etc.)
        if upper in config.KEYCODES:
            return (0, config.KEYCODES[upper])
        # Search all key groups for single-char labels
        for grp, entries in self.KEY_GROUPS.items():
            if grp == "Multimedia":
                continue
            for lbl, code in entries:
                if lbl == tok.upper() or lbl == tok:
                    mod = config.Modifier.SHIFT if lbl in self.SYMBOLS_NEED_SHIFT else 0
                    return (mod, code & 0xFF)
        # Case-insensitive KEYCODES lookup
        for name, code in config.KEYCODES.items():
            if name.upper() == upper:
                return (0, code)
        # Last resort: return mod=0, hid=0 for unknown chars so they appear
        return (0, 0)

    # ═══════════════════════════════════════════════════════════════════════
    # KEYCAP CHIPS
    # ═══════════════════════════════════════════════════════════════════════
    def render_keycap_chips(self, parent, action_byte, current_config):
        """Draw physical keycap-style chips for ASSIGNED SHORTCUT."""
        C = self.C
        for w in parent.winfo_children():
            w.destroy()

        seq = current_config.get(action_byte, [])
        if not seq:
            tk.Label(parent, text="(none assigned)",
                     bg=C.BG_CARD, fg=C.TEXT_DIM,
                     font=("Segoe UI", 9)).pack(side=tk.LEFT)
            return

        for mod, key in seq:
            for part in self._chip_labels_for_entry(mod, key):
                cap = tk.Frame(parent, bg=C.BG_BUTTON,
                               highlightthickness=1, highlightbackground=C.BORDER)
                cap.pack(side=tk.LEFT, padx=(0, 3))
                tk.Label(cap, text=part, bg=C.BG_BUTTON, fg=C.TEXT,
                         font=("Segoe UI", 9, "bold"), padx=8, pady=4).pack()

    def _chip_labels_for_entry(self, mod, key):
        """Return list of display strings (one per chip) for a stored (mod, key) pair."""
        if mod == 0xFE:
            return [next((n for n, v in config.MEDIA_KEYS.items() if v["b1"] == key), "Media")]
        chips = []
        sym_entries = self.KEY_GROUPS.get("Symbols", [])
        has_shift = bool(mod & (config.Modifier.SHIFT | config.Modifier.RIGHT_SHIFT))
        shifted_char = next((lbl for lbl, code in sym_entries
                             if code == key and lbl in self.SYMBOLS_NEED_SHIFT), None)
        base_char = next((lbl for lbl, code in sym_entries
                          if code == key and lbl not in self.SYMBOLS_NEED_SHIFT), None)
        MOD_FLAGS = [("Ctrl", config.Modifier.CTRL | config.Modifier.RIGHT_CTRL),
                     ("Shift", config.Modifier.SHIFT | config.Modifier.RIGHT_SHIFT),
                     ("Alt", config.Modifier.ALT | config.Modifier.RIGHT_ALT),
                     ("Win", config.Modifier.WIN | config.Modifier.RIGHT_WIN)]
        if key == 0:
            for name, byte in MOD_FLAGS:
                if mod & byte:
                    chips.append(name)
            return chips if chips else ["?"]
        if has_shift and shifted_char:
            clean = mod & ~config.Modifier.SHIFT & ~config.Modifier.RIGHT_SHIFT
            for name, byte in MOD_FLAGS:
                if name != "Shift" and (clean & byte):
                    chips.append(name)
            chips.append(shifted_char)
            return chips
        for name, byte in MOD_FLAGS:
            if mod & byte:
                chips.append(name)
        chips.append(base_char if base_char else config.KEYCODE_NAMES.get(key, f"Key{key}"))
        return chips

    def refresh_seq_chips(self, action_byte, current_config):
        """Rebuild the sequence chip row in the manual panel."""
        C = self.C
        if not hasattr(self, '_seq_chips_frame') or not self._seq_chips_frame.winfo_exists():
            return
        for w in self._seq_chips_frame.winfo_children():
            w.destroy()
        seq = current_config.get(action_byte, [])
        bg = C.BG_BUTTON
        if not seq:
            tk.Label(self._seq_chips_frame, text="(empty)", bg=bg,
                     fg=C.TEXT_DIM, font=("Segoe UI", 8)).pack(side=tk.LEFT)
            return
        for mod, key in seq:
            for chip_text in self._chip_labels_for_entry(mod, key):
                chip = tk.Frame(self._seq_chips_frame, bg=C.BG_BUTTON,
                                highlightthickness=1, highlightbackground=C.BORDER)
                chip.pack(side=tk.LEFT, padx=(0, 3))
                tk.Label(chip, text=chip_text, bg=C.BG_BUTTON, fg=C.TEXT,
                         font=("Segoe UI", 8, "bold"), padx=6, pady=2).pack()

    # ═══════════════════════════════════════════════════════════════════════
    # SLOT CHAIN (ADD SHORTCUT KEY — horizontal inline)
    # ═══════════════════════════════════════════════════════════════════════
    def _man_add_initial_slot(self):
        """Add the first slot automatically when building the panel."""
        if not getattr(self, '_man_slots', []):
            self._man_add_slot("key", "none", "Letters", "", _skip_refresh=True)
        self._man_update_slot_count()
        self._rebuild_add_button()

    def _man_add_slot(self, slot_type="key", mod_val="none",
                      grp_val="Letters", key_val="", _skip_refresh=False):
        """Append one modern inline slot to the horizontal chain.
        
        Layout: [▾Actuator/Key] [value combobox] (×)
        After slot, an [Add] button appears if slots < MAX.
        """
        C = self.C
        if len(getattr(self, '_man_slots', [])) >= config.MAX_SEQUENCE_LENGTH:
            return
        if not hasattr(self, '_man_slots_frame') or not self._man_slots_frame.winfo_exists():
            return

        slot_state = {
            "type_var": tk.StringVar(value=slot_type),
            "mod_var": tk.StringVar(value=mod_val),
            "grp_var": tk.StringVar(value=grp_val),
            "key_var": tk.StringVar(value=key_val),
        }

        bg = C.BG_BUTTON
        slot_frame = tk.Frame(self._man_slots_frame, bg=bg,
                              highlightthickness=1, highlightbackground=C.BORDER)
        slot_frame.pack(side=tk.LEFT, padx=(0, 3))
        slot_state["frame"] = slot_frame

        # ── TYPE SELECTOR: Combobox with ["Actuator", "Key"] ──────────────
        type_vals = ["Actuator", "Key"]
        type_display = "Key" if slot_type == "key" else "Actuator"
        slot_state["type_display_var"] = tk.StringVar(value=type_display)
        type_cb = ttk.Combobox(slot_frame, textvariable=slot_state["type_display_var"],
                               values=type_vals, state="readonly", style="Modern.TCombobox",
                               width=8, font=("Segoe UI", 8))
        type_cb.pack(side=tk.LEFT, padx=(2, 0), pady=2)
        slot_state["_type_cb"] = type_cb

        # ── VALUE AREA ────────────────────────────────────────────────────
        val_frame = tk.Frame(slot_frame, bg=bg)
        val_frame.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.X, expand=True)
        slot_state["_val_frame"] = val_frame

        # ── (×) DELETE/CLEAN ──────────────────────────────────────────────
        del_lbl = tk.Label(slot_frame, text="×", bg=bg, fg=C.TEXT_DIM,
                           font=("Segoe UI", 11), cursor="hand2", padx=4)
        del_lbl.pack(side=tk.RIGHT, pady=2)
        del_lbl.bind("<Enter>", lambda e: del_lbl.config(fg=C.ERROR))
        del_lbl.bind("<Leave>", lambda e: del_lbl.config(fg=C.TEXT_DIM))
        del_lbl.bind("<Button-1>", lambda e, s=slot_state: self._man_clean_or_delete(s))

        # ── REFRESH UI based on type ──────────────────────────────────────
        cb_kw = dict(state="readonly", style="Modern.TCombobox", font=("Segoe UI", 8))

        def _refresh_slot_ui():
            t = slot_state["type_display_var"].get()
            # Map display back to internal type
            inner_type = "mod" if t == "Actuator" else "key"
            slot_state["type_var"].set(inner_type)
            for w in slot_state["_val_frame"].winfo_children():
                w.destroy()
            if inner_type == "mod":
                mod_vals = [k for k in self.MOD_BYTES if k != "none"]
                if slot_state["mod_var"].get() not in mod_vals:
                    slot_state["mod_var"].set(mod_vals[0] if mod_vals else "Ctrl")
                cb = ttk.Combobox(slot_state["_val_frame"],
                                  textvariable=slot_state["mod_var"],
                                  values=mod_vals, width=7, **cb_kw)
                cb.pack(side=tk.LEFT)
                cb.bind("<<ComboboxSelected>>", lambda e: self._man_refresh_from_slots())
            else:
                grp_cb = ttk.Combobox(slot_state["_val_frame"],
                                      textvariable=slot_state["grp_var"],
                                      values=list(self.KEY_GROUPS.keys()),
                                      width=10, **cb_kw)
                grp_cb.pack(side=tk.LEFT, padx=(0, 2))
                labels = self._key_labels_for(slot_state["grp_var"].get(), "none")
                if not slot_state["key_var"].get() or \
                        slot_state["key_var"].get() not in labels:
                    slot_state["key_var"].set(labels[0] if labels else "")
                key_cb = ttk.Combobox(slot_state["_val_frame"],
                                      textvariable=slot_state["key_var"],
                                      values=labels, width=8, **cb_kw)
                key_cb.pack(side=tk.LEFT)

                def on_grp(e):
                    new_lbl = self._key_labels_for(slot_state["grp_var"].get(), "none")
                    key_cb.config(values=new_lbl)
                    if slot_state["key_var"].get() not in new_lbl:
                        slot_state["key_var"].set(new_lbl[0] if new_lbl else "")
                    self._man_refresh_from_slots()
                grp_cb.bind("<<ComboboxSelected>>", on_grp)
                key_cb.bind("<<ComboboxSelected>>", lambda e: self._man_refresh_from_slots())

        slot_state["_refresh_ui"] = _refresh_slot_ui

        # ── Bind type change ──────────────────────────────────────────────
        type_cb.bind("<<ComboboxSelected>>", lambda e: (_refresh_slot_ui(), self._man_refresh_from_slots()))

        self._man_slots.append(slot_state)
        self._man_update_slot_count()
        self._rebuild_add_button()
        _refresh_slot_ui()
        if not _skip_refresh:
            self._man_refresh_from_slots()

    def _rebuild_add_button(self):
        """Show or hide the [Add] button after the last slot."""
        # Remove existing add button if any
        if hasattr(self, '_man_add_btn') and self._man_add_btn and self._man_add_btn.winfo_exists():
            self._man_add_btn.destroy()
        self._man_add_btn = None

        if len(self._man_slots) >= config.MAX_SEQUENCE_LENGTH:
            return
        if not hasattr(self, '_man_slots_frame') or not self._man_slots_frame.winfo_exists():
            return

        self._man_add_btn = tk.Button(
            self._man_slots_frame, text="[Add]", bg=self.C.BG_BUTTON, fg=self.C.ACCENT,
            activebackground=self.C.BG_BUTTON_HOVER, activeforeground=self.C.ACCENT_SECONDARY,
            font=("Segoe UI", 8, "bold"), relief=tk.FLAT, bd=0,
            cursor="hand2", padx=6, pady=4,
            command=self._man_add_empty_slot)
        self._man_add_btn.pack(side=tk.LEFT, padx=(0, 3))

    def _man_add_empty_slot(self):
        """Add a new empty slot and refresh chips."""
        self._man_add_slot("key", "none", "Letters", "", _skip_refresh=False)

    def _man_update_slot_count(self):
        if hasattr(self, '_man_slot_count_lbl') and self._man_slot_count_lbl.winfo_exists():
            n = len(self._man_slots)
            lim = config.MAX_SEQUENCE_LENGTH
            self._man_slot_count_lbl.config(
                text=f"{n} / {lim}",
                fg=self.C.WARNING if n >= lim else self.C.TEXT_DIM)

    def _man_refresh_from_slots(self):
        """Write current slot selections to config and refresh all chip displays."""
        self.app._on_slots_changed()
        self._rebuild_add_button()

    def get_seq_from_slots(self):
        """Extract sequence from current slots."""
        seq = []
        for slot in getattr(self, '_man_slots', []):
            t = slot["type_var"].get()
            if t == "mod":
                mod_byte = self.MOD_BYTES.get(slot["mod_var"].get(), 0)
                if mod_byte:
                    seq.append((mod_byte, 0))
            else:
                entry = self._resolve_manual_entry(
                    "none", slot["grp_var"].get(), slot["key_var"].get())
                if entry:
                    seq.append(entry)
        return seq

    def _resolve_manual_entry(self, mod_name, grp, key_label):
        """Resolve (mod_byte, hid_code) from dropdown selections."""
        if not key_label:
            return None
        entries = self.KEY_GROUPS.get(grp, [])
        if grp == "Multimedia":
            for lbl, code in entries:
                if lbl == key_label:
                    return (0xFE, code & 0xFF)
            return None
        hid_code = next((code for lbl, code in entries if lbl == key_label), None)
        if hid_code is None:
            hid_code = config.KEYCODES.get(key_label)
        if hid_code is None:
            return None
        mod_byte = self.MOD_BYTES.get(mod_name, 0)
        if grp == "Symbols" and key_label in self.SYMBOLS_NEED_SHIFT:
            mod_byte |= config.Modifier.SHIFT
        return (mod_byte, hid_code)

    def _key_labels_for(self, grp, mod):
        entries = self.KEY_GROUPS.get(grp, [])
        return [lbl for lbl, _ in entries]

    def _byte_to_mod_name(self, mod_byte):
        for name, byte in [("Ctrl", config.Modifier.CTRL | config.Modifier.RIGHT_CTRL),
                            ("Shift", config.Modifier.SHIFT | config.Modifier.RIGHT_SHIFT),
                            ("Alt", config.Modifier.ALT | config.Modifier.RIGHT_ALT),
                            ("Win", config.Modifier.WIN | config.Modifier.RIGHT_WIN)]:
            if mod_byte & byte:
                return name
        return "Ctrl"

    def _hid_to_group_label(self, hid_code, has_shift=False):
        for grp, entries in self.KEY_GROUPS.items():
            if grp == "Multimedia":
                continue
            for lbl, code in entries:
                if code == hid_code:
                    if grp == "Symbols":
                        needs_shift = lbl in self.SYMBOLS_NEED_SHIFT
                        if needs_shift == has_shift:
                            return grp, lbl
                    else:
                        return grp, lbl
        return "Letters", config.KEYCODE_NAMES.get(hid_code, f"Key{hid_code}")

    def _man_clean_or_delete(self, slot_state):
        """Show context menu: Clean (reset) or Delete."""
        menu = tk.Menu(self.root, tearoff=0, bg=self.C.BG_BUTTON, fg=self.C.TEXT,
                       activebackground=self.C.ACCENT, activeforeground=self.C.BG_DARK,
                       font=("Segoe UI", 9))
        menu.add_command(label="Clean", command=lambda: self._man_clean_slot(slot_state))
        menu.add_command(label="Delete", command=lambda: self._man_delete_slot(slot_state))
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())

    def _man_clean_slot(self, slot_state):
        """Reset slot to default values."""
        slot_state["type_var"].set("key")
        slot_state["type_display_var"].set("Key")
        slot_state["mod_var"].set("none")
        slot_state["grp_var"].set("Letters")
        slot_state["key_var"].set("")
        slot_state["_refresh_ui"]()
        self._man_refresh_from_slots()

    def _man_delete_slot(self, slot_state):
        slots = getattr(self, '_man_slots', [])
        if slot_state in slots:
            slot_state["frame"].destroy()
            slots.remove(slot_state)
            self._man_update_slot_count()
            self._man_refresh_from_slots()

    def _man_populate_from_seq(self, current_config):
        """Load the current sequence into the SHORTCUT text field."""
        if not hasattr(self, '_man_text_var'):
            return
        action_byte, _ = self.app.current_control
        seq = current_config.get(action_byte, [])
        MOD_TEXT = {
            config.Modifier.CTRL: "ctrl",
            config.Modifier.SHIFT: "shift",
            config.Modifier.ALT: "alt",
            config.Modifier.RIGHT_ALT: "altgr",
            config.Modifier.WIN: "win",
        }
        parts = []
        for mod, key in seq:
            if mod == 0xFE:
                lbl = next((n for n, v in config.MEDIA_KEYS.items() if v["b1"] == key), f"media{key}")
                parts.append(lbl)
            elif key == 0 and mod != 0:
                parts.append(MOD_TEXT.get(mod, "mod"))
            else:
                key_str = config.KEYCODE_NAMES.get(key, "").lower() or f"key{key}"
                mod_str = MOD_TEXT.get(mod, "")
                parts.append(f"{mod_str}+{key_str}" if mod_str else key_str)
        self._man_parsing = True
        try:
            self._man_text_var.set("  ".join(parts))
        finally:
            self._man_parsing = False

    # ═══════════════════════════════════════════════════════════════════════
    # DETECTION UI HELPERS
    # ═══════════════════════════════════════════════════════════════════════
    def toggle_detection_ui(self, open_):
        if open_:
            self._detect_toggle_btn.config(text="▼  AUTO DETECT")
            self._detect_body.pack(fill=tk.X, pady=(6, 0))
        else:
            self._detect_toggle_btn.config(text="▶  AUTO DETECT")
            self._detect_body.pack_forget()

    def set_detect_hint(self, text, color=None):
        if hasattr(self, '_detect_hint') and self._detect_hint.winfo_exists():
            self._detect_hint.config(text=text, fg=color or self.C.TEXT_DIM)

    def set_detect_display(self, text, color=None):
        if hasattr(self, '_detect_display') and self._detect_display.winfo_exists():
            self._detect_display.config(text=text, fg=color or self.C.TEXT_DIM)

    def set_detect_confirm_enabled(self, enabled):
        if hasattr(self, '_detect_confirm_btn') and self._detect_confirm_btn.winfo_exists():
            self._detect_confirm_btn.config(state=tk.NORMAL if enabled else tk.DISABLED)

    # ═══════════════════════════════════════════════════════════════════════
    # MANUAL UI HELPERS
    # ═══════════════════════════════════════════════════════════════════════
    def toggle_manual_ui(self, open_):
        if open_:
            if self._detect_frame and self._detect_body.winfo_ismapped():
                self.app._stop_detection(confirmed=False)
            self._manual_body.pack(fill=tk.X, pady=(4, 0))
            self._manual_toggle_btn.config(text="▼  MANUAL MODE")
            self._manual_open = True
            self._man_populate_from_seq(self.app.current_config)
            self.refresh_seq_chips(
                self.app.current_control[0] if self.app.current_control else None,
                self.app.current_config)
        else:
            self._manual_body.pack_forget()
            self._manual_toggle_btn.config(text="▶  MANUAL MODE")
            self._manual_open = False

    # ═══════════════════════════════════════════════════════════════════════
    # FOOTER
    # ═══════════════════════════════════════════════════════════════════════
    def _build_footer(self):
        C = self.C

        footer = tk.Frame(self.root, bg=C.BG_CARD, height=52)
        footer.pack(fill=tk.X)
        footer.pack_propagate(False)

        inner_ftr = tk.Frame(footer, bg=C.BG_CARD)
        inner_ftr.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        # Save button (canvas)
        self._save_btn = tk.Canvas(inner_ftr, width=160, height=34,
                                   bg=C.BG_CARD, highlightthickness=0, cursor="hand2")
        self._save_btn.pack(side=tk.RIGHT)
        draw_cta_btn(self._save_btn, "  ↑  Send to Device", C.ACCENT, C.BG_DARK)
        self._save_btn.bind("<Button-1>", lambda e: self.app._save_to_device())
        self._save_btn.bind("<Enter>",
            lambda e: draw_cta_btn(self._save_btn, "  ↑  Send to Device",
                                   C.ACCENT_SECONDARY, C.BG_DARK))
        self._save_btn.bind("<Leave>",
            lambda e: draw_cta_btn(self._save_btn, "  ↑  Send to Device",
                                   C.ACCENT, C.BG_DARK))

        # Cancel button
        self._cancel_btn = tk.Button(
            inner_ftr, text="✕  Cancel", bg=C.BG_BUTTON, fg=C.TEXT_DIM,
            activebackground=C.BG_BUTTON_HOVER, activeforeground=C.ERROR,
            font=("Segoe UI", 9), relief=tk.FLAT, bd=0,
            cursor="hand2", padx=12, pady=6, command=self.app._cancel_changes)

        # Preset buttons
        for txt, cmd in [("Load", self.app._load_preset), ("Save", self.app._save_preset)]:
            tk.Button(inner_ftr, text=txt, bg=C.BG_BUTTON, fg=C.TEXT_DIM,
                      activebackground=C.BG_BUTTON_HOVER, activeforeground=C.TEXT,
                      font=("Segoe UI", 8), relief=tk.FLAT, bd=0,
                      cursor="hand2", padx=12, pady=6,
                      command=cmd).pack(side=tk.LEFT, padx=(0, 4))

        self._preset_lbl = tk.Label(inner_ftr, text="No preset loaded",
                                    bg=C.BG_CARD, fg=C.TEXT_DIM, font=("Segoe UI", 8))
        self._preset_lbl.pack(side=tk.LEFT, padx=(4, 0))

    def update_save_btn(self, text, bg, fg):
        if self._save_btn and self._save_btn.winfo_exists():
            draw_cta_btn(self._save_btn, text, bg, fg)

    def rebind_save_btn(self):
        """Restore click/hover bindings on CTA button."""
        if not self._save_btn or not self._save_btn.winfo_exists():
            return
        C = self.C
        self._save_btn.bind("<Button-1>", lambda e: self.app._save_to_device())
        self._save_btn.bind("<Enter>",
            lambda e: draw_cta_btn(self._save_btn, "  ↑  Send to Device",
                                   C.ACCENT_SECONDARY, C.BG_DARK))
        self._save_btn.bind("<Leave>",
            lambda e: draw_cta_btn(self._save_btn, "  ↑  Send to Device",
                                   C.ACCENT, C.BG_DARK))

    def enable_save_btn(self):
        """Enable save button — full click/hover response."""
        if not self._save_btn or not self._save_btn.winfo_exists():
            return
        self._save_btn.config(cursor="hand2")
        self.rebind_save_btn()

    def disable_save_btn(self):
        """Disable save button — no click response, keep visuals."""
        if not self._save_btn or not self._save_btn.winfo_exists():
            return
        self._save_btn.config(cursor="")
        self._save_btn.unbind("<Button-1>")

    def show_cancel_btn(self, show=True):
        if self._cancel_btn and self._cancel_btn.winfo_exists():
            if show:
                self._cancel_btn.pack(side=tk.RIGHT, padx=(0, 6))
            else:
                self._cancel_btn.pack_forget()

    def update_status_pill(self, text, color):
        if hasattr(self, '_pill_dot_lbl') and self._pill_dot_lbl.winfo_exists():
            self._pill_dot_lbl.config(fg=color)
        if hasattr(self, '_pill_text_lbl') and self._pill_text_lbl.winfo_exists():
            self._pill_text_lbl.config(text=text, fg=color)

    def update_led_status(self, text, color):
        if hasattr(self, '_led_status') and self._led_status.winfo_exists():
            self._led_status.config(text=text, fg=color)

    def set_led_current_label(self, text):
        if hasattr(self, '_led_current_lbl') and self._led_current_lbl.winfo_exists():
            self._led_current_lbl.config(text=f"— {text}")