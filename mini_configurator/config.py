# -*- coding: utf-8 -*-
"""
Configuracion y constantes del protocolo HID para Mini Controlador USB.
Basado en el codigo descompilado de RSoft.MacroPad.BLL.dll
"""

# ============================================
# IDENTIFICACION DEL DISPOSITIVO
# ============================================
VID = 0x1189
PID = 0x8890
INTERFACE_CONFIG = "mi_01"
REPORT_ID = 0x03
PACKET_SIZE = 65

# ============================================
# MAGIC BYTES
# ============================================
MAGIC_BYTE = 0xFE

# ============================================
# KEY TYPE
# ============================================
class KeyType:
    NONE = 0
    BASIC = 1
    MULTIMEDIA = 2
    MOUSE = 3
    LED = 8

# ============================================
# INPUT ACTION (botones y acciones del knob)
# ============================================
INPUT_ACTIONS = {
    1:  "Boton 1",
    2:  "Boton 2",
    3:  "Boton 3",
    13: "Knob - Izquierda",
    14: "Knob - Presionar",
    15: "Knob - Derecha",
}

# Inverso: nombre -> byte
ACTION_BYTES = {v: k for k, v in INPUT_ACTIONS.items()}

# Controles disponibles para la UI (en orden logico)
CONTROLS = [
    (1,  "Boton 1"),
    (2,  "Boton 2"),
    (3,  "Boton 3"),
    (14, "Knob - Click"),
    (13, "Knob - Izquierda"),
    (15, "Knob - Derecha"),
]

# ============================================
# KEYCODES HID (USB HID Usage Page 0x07)
# ============================================
# Fuente: RSoft.MacroPad.BLL descompilado + USB HID spec
KEYCODES = {
    # Letras
    "A": 4, "B": 5, "C": 6, "D": 7, "E": 8, "F": 9,
    "G": 10, "H": 11, "I": 12, "J": 13, "K": 14, "L": 15,
    "M": 16, "N": 17, "O": 18, "P": 19, "Q": 20, "R": 21,
    "S": 22, "T": 23, "U": 24, "V": 25, "W": 26, "X": 27,
    "Y": 28, "Z": 29,
    # Numeros
    "1": 30, "2": 31, "3": 32, "4": 33, "5": 34,
    "6": 35, "7": 36, "8": 37, "9": 38, "0": 39,
    # Especiales
    "Enter": 40, "Return": 40,
    "Esc": 41, "Escape": 41,
    "Backspace": 42, "Bksp": 42,
    "Tab": 43,
    "Space": 44,
    "Spacebar": 44,
    "-": 45, "Minus": 45, "Guion": 45,
    "=": 46, "Plus": 46, "Igual": 46,
    "[": 47, "OpenBracket": 47, "CorcheteAbre": 47,
    "]": 48, "CloseBracket": 48, "CorcheteCierra": 48,
    "\\": 49, "Pipe": 49, "Barra": 49,
    "#": 50, "Backslash": 50,
    ";": 51, "Colon": 51, "PuntoYComa": 51,
    "'": 52, "Quote": 52, "Comilla": 52,
    "`": 53, "Tilde": 53, "Acento": 53,
    ",": 54, "Clear": 54, "Comma": 54, "Coma": 54,
    ".": 55, "Period": 55, "Dot": 55, "Punto": 55,
    "/": 56, "Question": 56, "Slash": 56, "BarraIncl": 56,
    "CapsLock": 57, "Mayus": 57,
    # F keys
    "F1": 58, "F2": 59, "F3": 60, "F4": 61, "F5": 62,
    "F6": 63, "F7": 64, "F8": 65, "F9": 66, "F10": 67,
    "F11": 68, "F12": 69,
    # Navegacion
    "PrtSc": 70, "PrintScreen": 70,
    "ScrollLock": 71,
    "PauseBreak": 72, "Pause": 72,
    "Insert": 73,
    "Home": 74, "Inicio": 74,
    "PgUp": 75, "PageUp": 75,
    "Del": 76, "Delete": 76,
    "End": 77, "Fin": 77,
    "PgDn": 78, "PageDown": 78,
    "ArrowRight": 79, "Right": 79, "Derecha": 79,
    "ArrowLeft": 80, "Left": 80, "Izquierda": 80,
    "ArrowDown": 81, "Down": 81, "Abajo": 81,
    "ArrowUp": 82, "Up": 82, "Arriba": 82,
    # Numpad
    "Num": 83, "NumLock": 83,
    "NumDiv": 84, "Numpad/": 84,
    "NumMul": 85, "Numpad*": 85,
    "NumSub": 86, "Numpad-": 86,
    "NumAdd": 87, "Numpad+": 87,
    "Num1": 89, "Num2": 90, "Num3": 91, "Num4": 92,
    "Num5": 93, "Num6": 94, "Num7": 95, "Num8": 96,
    "Num9": 97, "Num0": 98,
    "NumDec": 99, "NumEnter": 100,
    # Otros
    "App": 101, "Menu": 101, "Apps": 101,
    # Spanish / ISO
    "IsoPlus1": 102,
}

# Inverso: byte -> nombre principal
KEYCODE_NAMES = {v: k for k, v in KEYCODES.items() if len(k) == 1}
for name in ["Enter", "Esc", "Backspace", "Tab", "Space", "CapsLock",
             "F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12",
             "Insert","Home","PgUp","Del","End","PgDn",
             "ArrowRight","ArrowLeft","ArrowDown","ArrowUp",
             "NumLock","NumDiv","NumMul","NumSub","NumAdd",
             "Num1","Num2","Num3","Num4","Num5","Num6","Num7","Num8","Num9","Num0",
             "NumDec","NumEnter",
             "PrtSc","ScrollLock","PauseBreak",
             "App"]:
    if name in KEYCODES:
        KEYCODE_NAMES[KEYCODES[name]] = name

# ============================================
# MODIFIER FLAGS
# ============================================
class Modifier:
    NONE = 0
    CTRL = 1
    SHIFT = 2
    ALT = 4
    WIN = 8
    RIGHT_CTRL = 16
    RIGHT_SHIFT = 32
    RIGHT_ALT = 64
    RIGHT_WIN = 128

MODIFIER_NAMES = {
    Modifier.CTRL:  "Ctrl",
    Modifier.SHIFT: "Shift",
    Modifier.ALT:   "Alt",
    Modifier.WIN:   "Win",
}

# ============================================
# MEDIA KEYS (Extended Protocol)
# ============================================
# Formato: [0, B1, B2, 0]
MEDIA_KEYS = {
    "PlayPause":   {"b1": 205, "b2": 0},
    "NextTrack":   {"b1": 181, "b2": 0},
    "PrevTrack":   {"b1": 182, "b2": 0},
    "VolMute":     {"b1": 226, "b2": 0},
    "VolUp":       {"b1": 233, "b2": 0},
    "VolDn":       {"b1": 234, "b2": 0},
}

# ============================================
# LAYOUTS DE TECLADO SOPORTADOS
# ============================================
KEYBOARD_LAYOUTS = {
    "US": "US English (QWERTY)",
    "ES": "Spanish (QWERTY)",
    "LATAM": "Latin American (QWERTY)",
}

# ============================================
# LIMITES DEL DISPOSITIVO
# ============================================
MAX_SEQUENCE_LENGTH = 5   # Maximo 5 teclas por atajo
MAX_LAYERS = 1            # Solo 1 layer
SUPPORTS_DELAY = False    # No soporta delay configurable
SUPPORTS_LED_COLOR = False # No soporta color RGB
LED_MODES = 3             # 3 modos de iluminacion confirmados por software chino

# Nombres de modos LED (confirmados por reverse engineering MINI KeyBoard.exe)
LED_MODE_NAMES = [
    (0, "○  Off"),
    (1, "◐  Mode 1"),
    (2, "◑  Mode 2"),
]

# ============================================
# COLORES DE UI
# ============================================
class Colors:
    BG_DARK        = "#0d0f12"
    BG_CARD        = "#13161b"
    BG_BUTTON      = "#1a1f26"
    BG_BUTTON_HOVER= "#1f2530"
    BG_BUTTON_ACTIVE="#252d38"
    ACCENT         = "#39c0ff"
    ACCENT_SECONDARY="#6ad7ff"
    TEXT           = "#f2f5f7"
    TEXT_DIM       = "#8b98a7"
    SUCCESS        = "#32d17c"
    WARNING        = "#f0b429"
    ERROR          = "#ff5f56"
    BORDER         = "#2b3440"
    KNOB           = "#3a4555"
