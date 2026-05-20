"""
KeyboardDetector - Deteccion de teclas usando pynput.

Detecta por VK scancode (posicion fisica) en lugar de caracter producido,
lo que hace la deteccion independiente del layout de teclado activo.
"""
import threading
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config

# Mapa VK (Windows Virtual Key) -> HID Usage code
# Fuente: USB HID Usage Tables + Windows VK codes
_VK_TO_HID = {
    0x41: 4,   0x42: 5,   0x43: 6,   0x44: 7,   0x45: 8,
    0x46: 9,   0x47: 10,  0x48: 11,  0x49: 12,  0x4A: 13,
    0x4B: 14,  0x4C: 15,  0x4D: 16,  0x4E: 17,  0x4F: 18,
    0x50: 19,  0x51: 20,  0x52: 21,  0x53: 22,  0x54: 23,
    0x55: 24,  0x56: 25,  0x57: 26,  0x58: 27,  0x59: 28,
    0x5A: 29,                                              # A-Z
    0x31: 30,  0x32: 31,  0x33: 32,  0x34: 33,  0x35: 34,
    0x36: 35,  0x37: 36,  0x38: 37,  0x39: 38,  0x30: 39, # 1-9, 0
    0x0D: 40,  0x1B: 41,  0x08: 42,  0x09: 43,  0x20: 44, # Enter Esc Bksp Tab Space
    0xBD: 45,  0xBB: 46,  0xDB: 47,  0xDD: 48,  0xDC: 49, # - = [ ] \
    0xBA: 51,  0xDE: 52,  0xC0: 53,  0xBC: 54,  0xBE: 55, # ; ' ` , .
    0xBF: 56,  0x14: 57,                                   # / CapsLock
    0x70: 58,  0x71: 59,  0x72: 60,  0x73: 61,  0x74: 62,
    0x75: 63,  0x76: 64,  0x77: 65,  0x78: 66,  0x79: 67,
    0x7A: 68,  0x7B: 69,                                   # F1-F12
    0x2C: 70,  0x91: 71,  0x13: 72,  0x2D: 73,  0x24: 74,
    0x21: 75,  0x2E: 76,  0x23: 77,  0x22: 78,            # PrtSc ScrLk Pause Ins Home PgUp Del End PgDn
    0x27: 79,  0x25: 80,  0x28: 81,  0x26: 82,            # Right Left Down Up
    0x90: 83,  0x6F: 84,  0x6A: 85,  0x6D: 86,  0x6B: 87,# NumLock Num/ Num* Num- Num+
    0x61: 89,  0x62: 90,  0x63: 91,  0x64: 92,  0x65: 93,
    0x66: 94,  0x67: 95,  0x68: 96,  0x69: 97,  0x60: 98,
    0x6E: 99,  0x6C: 100,                                  # Num1-9, Num0, Num. NumEnter
    0x5D: 101,                                             # App/Menu
    0xE2: 102,                                             # ISO extra key
}

# VKs que son modificadores (no se registran como tecla principal)
_MODIFIER_VKS = {
    0x10, 0x11, 0x12,        # Shift, Ctrl, Alt (genericos)
    0xA0, 0xA1,              # LShift, RShift
    0xA2, 0xA3,              # LCtrl, RCtrl
    0xA4, 0xA5,              # LAlt, RAlt
    0x5B, 0x5C,              # LWin, RWin
}

def vk_to_hid(vk):
    """Convertir VK code a HID usage code. Retorna None si no tiene mapeo."""
    return _VK_TO_HID.get(vk)


def vk_to_modifier(key):
    """
    Extraer flag de modificador de una pynput Key.
    Retorna config.Modifier.* o 0.
    """
    from pynput.keyboard import Key
    _MOD_MAP = {
        Key.ctrl:        config.Modifier.CTRL,
        Key.ctrl_l:      config.Modifier.CTRL,
        Key.ctrl_r:      config.Modifier.RIGHT_CTRL,
        Key.shift:       config.Modifier.SHIFT,
        Key.shift_l:     config.Modifier.SHIFT,
        Key.shift_r:     config.Modifier.RIGHT_SHIFT,
        Key.alt:         config.Modifier.ALT,
        Key.alt_l:       config.Modifier.ALT,
        Key.alt_r:       config.Modifier.RIGHT_ALT,
        Key.alt_gr:      config.Modifier.RIGHT_ALT,
        Key.cmd:         config.Modifier.WIN,
        Key.cmd_l:       config.Modifier.WIN,
        Key.cmd_r:       config.Modifier.RIGHT_WIN,
    }
    return _MOD_MAP.get(key, 0)


class KeyboardDetector:
    """
    Detecta combinaciones de teclas usando pynput.
    
    - Detecta por VK scancode (independiente del layout)
    - Soporta modificadores: Ctrl, Shift, Alt, Win
    - Llama a on_key(mod_byte, hid_keycode, display_str) al detectar una tecla no-modificadora
    - Llama a on_stop() al presionar Escape o Enter
    """

    def __init__(self):
        self._listener = None
        self._active_mods = 0
        self._on_key = None
        self._on_stop = None
        self._lock = threading.Lock()

    def start(self, on_key, on_stop=None):
        """
        Iniciar escucha.
        on_key(mod_byte, hid_code, display): llamado al detectar tecla principal
        on_stop(confirmed): llamado al presionar Enter (confirmed=True) o Esc (False)
        """
        self._on_key = on_key
        self._on_stop = on_stop
        self._active_mods = 0

        from pynput.keyboard import Listener
        self._listener = Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        )
        self._listener.daemon = True
        self._listener.start()

    def stop(self):
        """Detener escucha."""
        if self._listener:
            self._listener.stop()
            self._listener = None
        self._active_mods = 0

    def _on_press(self, key):
        from pynput.keyboard import Key, KeyCode
        with self._lock:
            mod = vk_to_modifier(key)
            if mod:
                self._active_mods |= mod
                return

            if key == Key.esc:
                if self._on_stop:
                    self._on_stop(confirmed=False)
                self.stop()
                return

            if key == Key.enter:
                if self._on_stop:
                    self._on_stop(confirmed=True)
                self.stop()
                return

            vk = None
            if isinstance(key, KeyCode):
                vk = key.vk
            elif hasattr(key, 'value') and hasattr(key.value, 'vk'):
                vk = key.value.vk

            if vk is None:
                return

            hid = vk_to_hid(vk)
            if hid is None:
                return

            display = self._build_display(self._active_mods, hid)
            if self._on_key:
                self._on_key(self._active_mods, hid, display)

    def _on_release(self, key):
        from pynput.keyboard import Key
        with self._lock:
            mod = vk_to_modifier(key)
            if mod:
                self._active_mods &= ~mod

    def _build_display(self, mod_byte, hid_code):
        """Construir string legible: 'Ctrl + C', 'Shift + F5', etc."""
        parts = []
        if mod_byte & config.Modifier.CTRL or mod_byte & config.Modifier.RIGHT_CTRL:
            parts.append("Ctrl")
        if mod_byte & config.Modifier.SHIFT or mod_byte & config.Modifier.RIGHT_SHIFT:
            parts.append("Shift")
        if mod_byte & config.Modifier.ALT or mod_byte & config.Modifier.RIGHT_ALT:
            parts.append("Alt")
        if mod_byte & config.Modifier.WIN or mod_byte & config.Modifier.RIGHT_WIN:
            parts.append("Win")
        key_name = config.KEYCODE_NAMES.get(hid_code, f"Key{hid_code}")
        parts.append(key_name)
        return " + ".join(parts)