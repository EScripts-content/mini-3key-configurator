"""
Prueba manual de escritura KNOB con action bytes correctos (13,14,15).
Sin UI — directo al HID.

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

def send(action_byte, sequence):
    """sequence: lista de (modifier, keycode)"""
    dev.send_config(action_byte=action_byte, key_sequence=sequence)
    time.sleep(0.05)
    dev.write_report([0xAA, 0xAA])
    time.sleep(0.15)
    print(f"  [OK] action={action_byte} seq={sequence}")

print("=" * 50)
print("PASO 1: Borrar funciones del KNOB")
print("=" * 50)
input("[ENTER] para borrar KNOB LEFT...")
send(13, [])
input("[ENTER] para borrar KNOB CLICK...")
send(14, [])
input("[ENTER] para borrar KNOB RIGHT...")
send(15, [])
print("\n>> Prueba el knob — debe estar en blanco.")
input("[ENTER] para continuar...")

print()
print("=" * 50)
print("PASO 2: Escribir atajos en el KNOB")
print("=" * 50)
input("[ENTER] para escribir SHIFT+Z en KNOB CLICK (14)...")
send(14, [(0x02, 0x1D)])   # Shift + Z

input("[ENTER] para escribir CTRL+(-) en KNOB LEFT (13)...")
send(13, [(0x01, 0x2D)])   # Ctrl + Minus

input("[ENTER] para escribir CTRL+(=) en KNOB RIGHT (15)...")
send(15, [(0x01, 0x2E)])   # Ctrl + Equal

print("\n>> Prueba ahora el knob:")
print("   - Click  = Shift+Z")
print("   - Left   = Ctrl+Minus")
print("   - Right  = Ctrl+Equal")
input("[ENTER] para terminar...")

dev.close()
print("[Listo]")
