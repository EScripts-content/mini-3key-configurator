# -*- coding: utf-8 -*-
"""
UI Styles — Colores, estilos ttk y helpers de canvas para Mini Configurator.
Separado de la lógica de negocio.
"""

import tkinter as tk
from tkinter import ttk
import config


def setup_styles(root):
    """Configure Industrial Zen ttk styles."""
    C = config.Colors
    style = ttk.Style(root)
    style.theme_use("clam")

    # ── Primary CTA ─────────────────────────────────────────────────────
    style.configure("Accent.TButton",
                    background=C.ACCENT,
                    foreground=C.BG_DARK,
                    font=("Segoe UI", 10, "bold"),
                    padding=(20, 10),
                    borderwidth=0, relief="flat")
    style.map("Accent.TButton",
              background=[("active", C.ACCENT_SECONDARY),
                          ("disabled", C.BG_BUTTON)],
              foreground=[("active", C.BG_DARK),
                          ("disabled", C.TEXT_DIM)])

    # ── Ghost ────────────────────────────────────────────────────────────
    style.configure("Ghost.TButton",
                    background=C.BG_CARD,
                    foreground=C.TEXT_DIM,
                    font=("Segoe UI", 9),
                    padding=(12, 6),
                    borderwidth=0, relief="flat")
    style.map("Ghost.TButton",
              background=[("active", C.BG_BUTTON)],
              foreground=[("active", C.TEXT)])

    # ── Secondary ────────────────────────────────────────────────────────
    style.configure("Secondary.TButton",
                    background=C.BG_BUTTON,
                    foreground=C.TEXT_DIM,
                    font=("Segoe UI", 9),
                    padding=(14, 7),
                    borderwidth=0, relief="flat")
    style.map("Secondary.TButton",
              background=[("active", C.BG_BUTTON_HOVER)],
              foreground=[("active", C.TEXT)])

    # ── Combobox ─────────────────────────────────────────────────────────
    style.configure("Modern.TCombobox",
                    fieldbackground=C.BG_BUTTON,
                    background=C.BG_BUTTON,
                    foreground=C.TEXT,
                    selectbackground=C.ACCENT,
                    selectforeground=C.BG_DARK,
                    arrowcolor=C.TEXT_DIM,
                    borderwidth=0,
                    font=("Segoe UI", 9))
    style.map("Modern.TCombobox",
              fieldbackground=[("readonly", C.BG_BUTTON)],
              foreground=[("readonly", C.TEXT)],
              selectbackground=[("readonly", C.BG_BUTTON)])

    # ── Entry ─────────────────────────────────────────────────────────────
    style.configure("Modern.TEntry",
                    fieldbackground=C.BG_BUTTON,
                    foreground=C.TEXT,
                    insertcolor=C.TEXT,
                    borderwidth=0,
                    font=("Segoe UI", 9))

    # ── Scrollbar ─────────────────────────────────────────────────────────
    style.configure("Modern.Vertical.TScrollbar",
                    background=C.BG_BUTTON,
                    troughcolor=C.BG_CARD,
                    bordercolor=C.BG_CARD,
                    arrowcolor=C.TEXT_DIM,
                    borderwidth=0)

    # ── Radio-style LabelFrame ────────────────────────────────────────────
    style.configure("Radio.TLabelframe",
                    background=C.BG_BUTTON,
                    foreground=C.TEXT,
                    relief="flat",
                    borderwidth=1)
    style.configure("Radio.TLabelframe.Label",
                    background=C.BG_BUTTON,
                    foreground=C.TEXT_DIM,
                    font=("Segoe UI", 7))


def draw_cta_btn(canvas, text, bg, fg, w=160, h=34, r=6):
    """Redraw the CTA canvas button. Returns None, modifies canvas in place."""
    canvas.delete("all")
    pts = [r,0, w-r,0, w,0, w,r, w,h-r, w,h, w-r,h, r,h, 0,h, 0,h-r, 0,r, 0,0]
    canvas.create_polygon(pts, smooth=True, fill=bg, outline="")
    canvas.create_text(w//2, h//2, text=text, fill=fg,
                       font=("Segoe UI", 9, "bold"))