# -*- coding: utf-8 -*-
"""
Interactive test for SHORTCUT text entry — run this, don't run cmd after.
Probar como USUARIO REAL escribiendo en el entry de SHORTCUT.
"""
import tkinter as tk
from tkinter import ttk
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import config
from ui_styles import setup_styles

# ── Copy the relevant logic from UIBuilder (same methods) ──────────────
from ui_panels import UIBuilder

class FakeApp:
    """Fake app to provide callbacks that UIBuilder expects."""
    def __init__(self):
        self._led_active_mode = None
        self.current_control = (1, "Boton 1")
        self.current_config = {1: []}
        
    def _check_device(self):
        pass
    def _toggle_led_panel(self):
        pass
    def _set_led_mode(self, m):
        pass
    def _toggle_detection(self):
        pass
    def _toggle_manual(self):
        pass
    def _stop_detection(self, confirmed):
        pass
    def _clear_keys(self):
        pass
    def _save_to_device(self):
        pass
    def _cancel_changes(self):
        pass
    def _load_preset(self):
        pass
    def _save_preset(self):
        pass
    def _on_shortcut_text_parsed(self, seq):
        """Real callback — prints parsed result."""
        from ui_panels import UIBuilder
        ui = self._ui_ref
        action_byte, _ = self.current_control
        old = self.current_config.get(action_byte, [])
        self.current_config[action_byte] = seq
        # Show chips
        if ui:
            ui.render_keycap_chips(ui._shortcut_chip, action_byte, self.current_config)
            ui.refresh_seq_chips(action_byte, self.current_config)
        display_parts = []
        for mod, key in seq:
            if mod == 0xFE:
                display_parts.append(f"[Media]")
            elif key == 0 and mod != 0:
                parts = []
                if mod & (config.Modifier.CTRL | config.Modifier.RIGHT_CTRL): parts.append("Ctrl")
                if mod & (config.Modifier.SHIFT | config.Modifier.RIGHT_SHIFT): parts.append("Shift")
                if mod & (config.Modifier.ALT | config.Modifier.RIGHT_ALT): parts.append("Alt")
                if mod & (config.Modifier.WIN | config.Modifier.RIGHT_WIN): parts.append("Win")
                display_parts.append(f"[{' + '.join(parts)}]")
            else:
                mod_s = ""
                if mod & (config.Modifier.CTRL | config.Modifier.RIGHT_CTRL): mod_s += "Ctrl+"
                if mod & (config.Modifier.SHIFT | config.Modifier.RIGHT_SHIFT): mod_s += "Shift+"
                if mod & (config.Modifier.ALT | config.Modifier.RIGHT_ALT): mod_s += "Alt+"
                if mod & (config.Modifier.WIN | config.Modifier.RIGHT_WIN): mod_s += "Win+"
                key_name = config.KEYCODE_NAMES.get(key, f"Key{key}")
                display_parts.append(f"[{mod_s}{key_name}]")
        print(f"\n>>> PARSED: {' '.join(display_parts)}")
        print(f">>> SEQ: {seq}")
        
    def _on_slots_changed(self):
        pass

def run_test():
    root = tk.Tk()
    root.title("SHORTCUT Test — Type in the entry below")
    root.geometry("600x400")
    root.configure(bg=config.Colors.BG_DARK)
    setup_styles(root)
    
    C = config.Colors
    main = tk.Frame(root, bg=C.BG_DARK)
    main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    tk.Label(main, text="SHORTCUT LIVE TEST", bg=C.BG_DARK, fg=C.TEXT,
             font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
    
    # Instructions
    tk.Label(main, text="Escribe en el cuadro. Prueba: ct, sh, al, ct c, ct+, F1, Enter, Space, ctrl c, etc",
             bg=C.BG_DARK, fg=C.TEXT_DIM, font=("Segoe UI", 8), wraplength=500, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 10))
    
    # Entry area
    entry_frame = tk.Frame(main, bg=C.BG_CARD, highlightthickness=1, highlightbackground=C.BORDER)
    entry_frame.pack(fill=tk.X, pady=(0, 10))
    
    inner = tk.Frame(entry_frame, bg=C.BG_CARD)
    inner.pack(fill=tk.X, padx=10, pady=10)
    
    fake = FakeApp()
    ui = UIBuilder(fake, root)
    fake._ui_ref = ui  # circular ref so callbacks work
    
    # Build the shortcut entry just like the real UI
    lbl_kw = dict(bg=C.BG_CARD, fg=C.TEXT_DIM, font=("Segoe UI", 8, "bold"))
    tk.Label(inner, text="SHORTCUT", **lbl_kw).pack(anchor=tk.W)
    
    # Sequence chips
    seq_frame = tk.Frame(inner, bg=C.BG_CARD)
    seq_frame.pack(fill=tk.X, pady=(4, 6))
    ui._seq_chips_frame = seq_frame  # hook for refresh_seq_chips
    ui._shortcut_chip = seq_frame    # hook for render_keycap_chips
    ui.refresh_seq_chips(1, {1: []})
    ui.render_keycap_chips(seq_frame, 1, {1: []})
    
    # Text entry
    ui._man_text_var = tk.StringVar()
    entry_row = tk.Frame(inner, bg=C.BG_CARD)
    entry_row.pack(fill=tk.X, pady=(0, 2))
    entry = ttk.Entry(entry_row, textvariable=ui._man_text_var,
                      style="Modern.TEntry", width=25, font=("Segoe UI", 11))
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    ui._man_entry = entry  # needed for KeyRelease handler
    
    # Label with hints
    hint = tk.Label(entry_row, text="ct→Ctrl  sh→Shift  al→Alt  wi→Win  ag→AltGr  space=key",
                    bg=C.BG_CARD, fg=C.TEXT_DIM, font=("Segoe UI", 7))
    hint.pack(side=tk.LEFT, padx=(4, 0))
    
    # Bind the key release (same as UIBuilder)
    entry.bind("<KeyRelease>", ui._on_man_key_release)
    
    # Debug: show current text
    debug_frame = tk.Frame(main, bg=C.BG_DARK)
    debug_frame.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(debug_frame, text="DEBUG — current text:", bg=C.BG_DARK, fg=C.TEXT_DIM,
             font=("Segoe UI", 7)).pack(anchor=tk.W)
    
    debug_text = tk.Text(debug_frame, bg=C.BG_BUTTON, fg=C.TEXT, 
                         font=("Consolas", 10), height=4, relief=tk.FLAT, bd=0)
    debug_text.pack(fill=tk.BOTH, expand=True, pady=(2, 0))
    
    def update_debug(*args):
        t = repr(ui._man_text_var.get())
        debug_text.delete(1.0, tk.END)
        debug_text.insert(1.0, f"text: {t}\n")
        debug_text.insert(tk.END, f"len: {len(t)} chars\n")
        debug_text.insert(tk.END, f"cursor: {entry.index(tk.INSERT)}\n")
        # Show current config
        seq = fake.current_config.get(1, [])
        debug_text.insert(tk.END, f"parsed: {seq}\n")
        root.after(100, update_debug)
    
    root.after(200, update_debug)
    
    # Focus the entry
    entry.focus_set()
    
    # Bind Escape to close
    root.bind("<Escape>", lambda e: root.destroy())
    
    print("="*60)
    print("  TEST INTERACTIVO DE SHORTCUT")
    print("  Escribe en el campo de texto")
    print("  Prueba: ct, sh, al, ct c, ct+, F1, Enter")
    print("  Presiona ESC para salir")
    print("="*60)
    
    root.mainloop()

if __name__ == "__main__":
    run_test()