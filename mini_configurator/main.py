# /// script
# requires-python = ">=3.10"
# dependencies = ["pywinusb", "pynput"]
# ///

# -*- coding: utf-8 -*-
"""
Mini Configurator — Aplicación moderna para configurar Mini Controlador USB
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
import ctypes

# Ocultar ventana de consola en Windows
if sys.platform == "win32":
    _hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if _hwnd:
        ctypes.windll.user32.ShowWindow(_hwnd, 0)

# Agregar directorio actual al path para imports
if getattr(sys, 'frozen', False):
    sys.path.insert(0, sys._MEIPASS)
else:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from hid_device import HidDevice, test_connection
from keyboard_detector import KeyboardDetector
from ui_styles import setup_styles
from ui_panels import UIBuilder


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

        # Snapshot of last successfully saved state (for Cancel)
        self._config_saved = {byte: [] for byte, _ in config.CONTROLS}

        # Controles modificados en esta sesion (solo estos se envian al device)
        self._modified_controls = set()

        # LED active mode
        self._led_active_mode = None
        self._led_sending = False

        # Estilos
        setup_styles(root)

        # UI Builder — toda la construccion de paneles esta aqui
        self.ui = UIBuilder(self, root)
        self.ui.build_all()
        self.ui.disable_save_btn()

        # Verificar conexion
        self._check_device()

        # Limpiar detector al cerrar
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ═══════════════════════════════════════════════════════════════════════
    # CIERRE
    # ═══════════════════════════════════════════════════════════════════════
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

    # ═══════════════════════════════════════════════════════════════════════
    # SELECCION DE CONTROL
    # ═══════════════════════════════════════════════════════════════════════
    def _select_control(self, action_byte, name):
        """Select a control — highlight device visual, rebuild right panel."""
        self.current_control = (action_byte, name)
        # Auto-expand KNOB tabs when a knob action is chosen
        if action_byte in {13, 14, 15}:
            if hasattr(self.ui, '_knob_tabs_outer') and self.ui._knob_tabs_outer:
                self.ui._knob_tabs_outer.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        else:
            if hasattr(self.ui, '_knob_tabs_outer') and self.ui._knob_tabs_outer:
                self.ui._knob_tabs_outer.place_forget()
        self.ui.update_device_highlight(action_byte)
        self.ui.build_config_panel(self.current_control, self.current_config)

    # ═══════════════════════════════════════════════════════════════════════
    # CALLBACKS DESDE UI BUILDER
    # ═══════════════════════════════════════════════════════════════════════
    def _on_shortcut_text_parsed(self, seq):
        """Called from UIBuilder when SHORTCUT text is parsed."""
        if not self.current_control:
            return
        action_byte, _ = self.current_control
        if seq != self.current_config.get(action_byte, []):
            self.current_config[action_byte] = seq
            self._refresh_all_chips()
            self._modified_controls.add(action_byte)
            self._mark_dirty()

    def _on_slots_changed(self):
        """Called from UIBuilder when ADD SHORTCUT KEY slots change."""
        if not self.current_control:
            return
        action_byte, _ = self.current_control
        seq = self.ui.get_seq_from_slots()
        if seq != self.current_config.get(action_byte, []):
            self.current_config[action_byte] = seq
            self._refresh_all_chips()
            self._modified_controls.add(action_byte)
            self._mark_dirty()

    # ═══════════════════════════════════════════════════════════════════════
    # REFRESH CHIPS
    # ═══════════════════════════════════════════════════════════════════════
    def _refresh_all_chips(self):
        """Refresh all chip displays (ASSIGNED SHORTCUT + manual seq chips)."""
        if not self.current_control:
            return
        action_byte, _ = self.current_control
        self.ui.render_keycap_chips(self.ui._shortcut_chip, action_byte, self.current_config)
        self.ui.refresh_seq_chips(action_byte, self.current_config)

    def _refresh_shortcut_chip(self):
        """Refresh the ASSIGNED SHORTCUT chips row only."""
        if hasattr(self.ui, '_shortcut_chip') and self.ui._shortcut_chip.winfo_exists():
            if not self.current_control:
                return
            action_byte, _ = self.current_control
            self.ui.render_keycap_chips(self.ui._shortcut_chip, action_byte, self.current_config)

    # ═══════════════════════════════════════════════════════════════════════
    # DIRTY / CLEAN
    # ═══════════════════════════════════════════════════════════════════════
    def _mark_dirty(self):
        """Signal unsaved changes — turn CTA button amber + show Cancel."""
        self.ui.enable_save_btn()
        self._config_dirty = True
        self.ui.update_save_btn("  ↑  Send to Device",
                                config.Colors.WARNING, config.Colors.BG_DARK)
        self.ui.show_cancel_btn(True)

    def _mark_clean(self):
        """Config saved — CTA goes green, hide Cancel, snapshot saved state."""
        self._modified_controls.clear()
        self._config_dirty = False
        self._config_saved = {k: list(v) for k, v in self.current_config.items()}
        self.ui.show_cancel_btn(False)
        self.ui.update_save_btn("  ✓  Saved", config.Colors.SUCCESS, config.Colors.BG_DARK)
        self.ui.disable_save_btn()
        self.root.after(2000, lambda: (
            self.ui.disable_save_btn() or
            self.ui.update_save_btn("  ↑  Send to Device",
                                    config.Colors.ACCENT, config.Colors.BG_DARK)
            if self.ui._save_btn and self.ui._save_btn.winfo_exists() else None))

    def _cancel_changes(self):
        """Discard unsaved changes — revert to last saved state."""
        saved = getattr(self, '_config_saved', {})
        for byte, _ in config.CONTROLS:
            self.current_config[byte] = list(saved.get(byte, []))
        self._modified_controls.clear()
        self._config_dirty = False
        self.ui.disable_save_btn()
        self.ui.show_cancel_btn(False)
        self.ui.update_save_btn("  ↑  Send to Device",
                                config.Colors.ACCENT, config.Colors.BG_DARK)
        self.ui.build_config_panel(self.current_control, self.current_config)

    # ═══════════════════════════════════════════════════════════════════════
    # TOGGLE MANUAL
    # ═══════════════════════════════════════════════════════════════════════
    def _toggle_manual(self):
        """Expand/collapse the manual section."""
        if self.ui._manual_open:
            self.ui.toggle_manual_ui(False)
        else:
            self.ui.toggle_manual_ui(True)

    # ═══════════════════════════════════════════════════════════════════════
    # TOGGLE LED PANEL
    # ═══════════════════════════════════════════════════════════════════════
    def _toggle_led_panel(self):
        self.ui.toggle_led_panel()

    # ═══════════════════════════════════════════════════════════════════════
    # AUTO DETECT
    # ═══════════════════════════════════════════════════════════════════════
    def _toggle_detection(self):
        if self._detecting:
            self._stop_detection(confirmed=False)
        else:
            self._start_detection()

    def _start_detection(self):
        if not self.current_control:
            return
        self._detecting = True
        self._pending_sequence = []
        self.ui.toggle_detection_ui(True)
        self.ui.set_detect_hint("  ● Listening — press keys now", config.Colors.SUCCESS)
        self.ui.set_detect_display("— press a key —", config.Colors.TEXT_DIM)
        self.ui.set_detect_confirm_enabled(False)
        self._detector = KeyboardDetector()
        self._detector.start(on_key=self._on_key_detected, on_stop=self._on_detection_stop)

    def _on_key_detected(self, mod_byte, hid_code, display):
        """Called from pynput thread — use root.after for UI update."""
        def update():
            if not self._detecting:
                return
            pair = (mod_byte, hid_code)
            if pair not in self._pending_sequence:
                if len(self._pending_sequence) < config.MAX_SEQUENCE_LENGTH:
                    self._pending_sequence.append(pair)
            self.ui.set_detect_display(display, config.Colors.ACCENT)
            self.ui.set_detect_confirm_enabled(True)
        self.root.after(0, update)

    def _on_detection_stop(self, confirmed):
        self.root.after(0, lambda: self._stop_detection(confirmed=confirmed))

    def _stop_detection(self, confirmed):
        if self._detector:
            self._detector.stop()
            self._detector = None
        self._detecting = False

        if confirmed and self._pending_sequence and self.current_control:
            action_byte, _ = self.current_control
            new_seq = list(self._pending_sequence)
            if new_seq != self.current_config.get(action_byte, []):
                self.current_config[action_byte] = new_seq
                self._refresh_all_chips()
                self._modified_controls.add(action_byte)
                self._mark_dirty()

        self._pending_sequence = []
        self.ui.toggle_detection_ui(False)
        self.ui.set_detect_hint("  Click to start listening for key presses",
                                config.Colors.TEXT_DIM)

    # ═══════════════════════════════════════════════════════════════════════
    # CLEAR KEYS
    # ═══════════════════════════════════════════════════════════════════════
    def _clear_keys(self):
        if not self.current_control:
            return
        action_byte, _ = self.current_control
        if self.current_config.get(action_byte, []):
            self.current_config[action_byte] = []
            self._refresh_all_chips()
            self._modified_controls.add(action_byte)
            self._mark_dirty()

    # ═══════════════════════════════════════════════════════════════════════
    # LED
    # ═══════════════════════════════════════════════════════════════════════
    def _set_led_mode(self, target_mode):
        if not self.device_connected:
            self.ui.update_led_status("No device", config.Colors.ERROR)
            return

        if getattr(self, '_led_sending', False):
            return
        self._led_sending = True
        self.ui.update_led_status("Sending...", config.Colors.WARNING)
        for lbl in self.ui._led_mode_btns.values():
            lbl.config(fg=config.Colors.BORDER, cursor="")

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
        _, label = config.LED_MODE_NAMES[active_mode]
        self.ui.update_led_status("✓ Applied", config.Colors.SUCCESS)
        self.ui.set_led_current_label(label.strip())
        self._led_sending = False
        self.ui.update_led_btn_visuals(active_mode)
        for lbl in self.ui._led_mode_btns.values():
            lbl.config(cursor="hand2")

    def _on_led_error(self, err):
        self._led_sending = False
        for lbl in self.ui._led_mode_btns.values():
            lbl.config(fg=config.Colors.TEXT_DIM, cursor="hand2")
        if hasattr(self, '_led_active_mode') and self._led_active_mode is not None:
            self.ui.update_led_btn_visuals(self._led_active_mode)
        self.ui.update_led_status(f"Error: {err[:40]}", config.Colors.ERROR)

    # ═══════════════════════════════════════════════════════════════════════
    # SAVE TO DEVICE
    # ═══════════════════════════════════════════════════════════════════════
    def _save_to_device(self):
        if not self.device_connected:
            self.ui.update_status_pill("No device", config.Colors.ERROR)
            self.root.after(2000, self._check_device)
            return

        # Lock button while sending
        self.ui.update_save_btn("  ⟳  Sending...", config.Colors.WARNING, config.Colors.BG_DARK)
        self.ui._save_btn.unbind("<Button-1>")
        self.ui._save_btn.unbind("<Enter>")
        self.ui._save_btn.unbind("<Leave>")

        snapshot = {k: list(self.current_config[k]) for k in self._modified_controls}
        path = self.device_path

        def _do_send():
            try:
                with HidDevice(path) as dev:
                    for action_byte, sequence in snapshot.items():
                        dev.send_config(action_byte=action_byte, key_sequence=sequence)
                        time.sleep(0.1)
                self.root.after(0, self._mark_clean)
            except Exception as e:
                self.root.after(0, lambda err=str(e): self._save_failed(err))

        threading.Thread(target=_do_send, daemon=True).start()

    def _save_failed(self, err):
        self.ui.update_save_btn("  ✕  Error", config.Colors.ERROR, config.Colors.BG_DARK)
        self.ui.enable_save_btn()
        self.root.after(3000, lambda: (
            self.ui.update_save_btn("  ↑  Send to Device",
                                    config.Colors.ACCENT, config.Colors.BG_DARK)
            if self.ui._save_btn and self.ui._save_btn.winfo_exists() else None))
        self.ui.update_status_pill(f"Error: {err[:28]}", config.Colors.ERROR)

    # ═══════════════════════════════════════════════════════════════════════
    # PRESETS
    # ═══════════════════════════════════════════════════════════════════════
    def _save_preset(self):
        path = filedialog.asksaveasfilename(
            initialdir=self.presets_dir, defaultextension=".json",
            filetypes=[("Preset JSON", "*.json")], title="Save Preset")
        if not path:
            return
        data = {
            "name": os.path.splitext(os.path.basename(path))[0],
            "config": {str(k): [(m, key) for m, key in v]
                       for k, v in self.current_config.items()}
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        messagebox.showinfo("Saved", f"Preset saved to:\n{path}")

    def _load_preset(self):
        path = filedialog.askopenfilename(
            initialdir=self.presets_dir, defaultextension=".json",
            filetypes=[("Preset JSON", "*.json")], title="Load Preset")
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
                self._refresh_all_chips()
            self._mark_dirty()
            messagebox.showinfo("Loaded", f"Preset '{data.get('name', 'unknown')}' loaded.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load preset: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # DEVICE CONNECTION
    # ═══════════════════════════════════════════════════════════════════════
    def _check_device(self):
        self.ui.update_status_pill("Verifying...", config.Colors.TEXT_DIM)
        self.root.update_idletasks()
        ok, info = test_connection()
        if ok:
            self.device_connected = True
            self.device_path = info
            self.ui.update_status_pill("CONNECTED", config.Colors.SUCCESS)
        else:
            self.device_connected = False
            self.device_path = None
            self.ui.update_status_pill("DISCONNECTED", config.Colors.ERROR)

    # ═══════════════════════════════════════════════════════════════════════
    # HELPERS (modifier string, shortcut summary — logic only)
    # ═══════════════════════════════════════════════════════════════════════
    def _modifier_str(self, mod_byte):
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

    def _shortcut_summary(self, action_byte):
        seq = self.current_config.get(action_byte, [])
        if not seq:
            return "  (none)"
        parts = []
        for mod, key in seq:
            if mod == 0xFE:
                label = next((n for n, v in config.MEDIA_KEYS.items()
                              if v["b1"] == key), f"Media({key})")
                parts.append(label)
            else:
                mod_str = self._modifier_str(mod)
                key_str = config.KEYCODE_NAMES.get(key, f"Key{key}")
                parts.append(f"{mod_str}+{key_str}" if mod_str else key_str)
        return "  " + "  →  ".join(parts)


# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════
def _base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def main():
    root = tk.Tk()
    root.configure(bg=config.Colors.BG_DARK)
    icon_path = os.path.join(_base_dir(), "assets", "icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    app = MiniConfiguratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        log_path = os.path.join(_base_dir(), "error.log")
        with open(log_path, "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        raise