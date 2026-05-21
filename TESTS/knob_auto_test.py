"""
Prueba AUTOMAICA de escritura KNOB con action bytes correctos (13,14,15).
No requiere input del usuario. Solo prueba fisicamente el knob al final.

RIGHT  (15) = CTRL + =
LEFT   (13) = CTRL + -
CLICK  (14) = SHIFT + Z

HID keycodes:  - = 0x2D, = = 0x2E, Z = 0x1D
Modifiers:     Ctrl = 0x01, Shift = 0x02
"""
import sys, time
sys.path.insert(0, r"H:\PROGRAMAS\PROGRAMAS PAGADOS\MINI CONTROLADORA USB\drive-download-20230810T081045Z-001\mini_configurator")
from hid_device import HidDevice

dev = HidDevice()
dev.open()
print("[OK] Dispositivo conectado\n")

def send(action_byte, sequence, label):
    """sequence: lista de (modifier, keycode)"""
    print(f"  Enviando {label} (action={action_byte})...")
    dev.send_config(action_byte=action_byte, key_sequence=sequence)
    time.sleep(0.05)
    dev.write_report([0xAA, 0xAA])
    time.sleep(0.5)
    print(f"  [OK] {label} enviado.")

print("=" * 50)
print("PASO 1: Borrar funciones del KNOB")
print("=" * 50)
send(13, [], "KNOB LEFT (borrar)")
send(14, [], "KNOB CLICK (borrar)")
send(15, [], "KNOB RIGHT (borrar)")
print("\n>> Prueba el knob ahora — debe estar en blanco.")
print("   (Esperando 3 segundos...)")
time.sleep(3)

print()
print("=" * 50)
print("PASO 2: Escribir atajos en el KNOB")
print("=" * 50)
send(14, [(0x02, 0x1D)], "KNOB CLICK = Shift+Z")      # Shift + Z
send(13, [(0x01, 0x2D)], "KNOB LEFT = Ctrl+Minus")     # Ctrl + -
send(15, [(0x01, 0x2E)], "KNOB RIGHT = Ctrl+Equal")   # Ctrl + =

print("\n" + "=" * 50)
print("LISTO. Prueba ahora el knob fisicamente:")
print("   - Click  = Shift+Z")
print("   - Left   = Ctrl+Minus")
print("   - Right  = Ctrl+Equal")
print("=" * 50)

dev.close()
print("[Listo]")
