"""
Prueba directa de escritura de atajos al dispositivo.
Sin UI — directo al HID.

Tecla 1 = action_byte 1
Tecla 2 = action_byte 2
Tecla 3 = action_byte 3

HID keycodes:
  C = 0x06, V = 0x19, Z = 0x1D
  Ctrl = 0x01
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
    # WriteFlash — igual que Legacy, por si el firmware Extended también lo requiere
    dev.write_report([0xAA, 0xAA])
    time.sleep(0.15)
    print(f"  [OK] action={action_byte} seq={sequence}")

print("=" * 50)
print("PASO 1: Borrar teclas 1, 2, 3 (dejar en blanco)")
print("=" * 50)
input("[ENTER] para borrar tecla 1...")
send(1, [])
input("[ENTER] para borrar tecla 2...")
send(2, [])
input("[ENTER] para borrar tecla 3...")
send(3, [])
print("\n>> Prueba ahora las 3 teclas — deben estar en blanco.")
input("[ENTER] para continuar...")

print()
print("=" * 50)
print("PASO 2: Escribir Ctrl+C, Ctrl+V, Ctrl+Z")
print("=" * 50)
input("[ENTER] para escribir Ctrl+C en tecla 1...")
send(1, [(0x01, 0x06)])   # Ctrl + C
input("[ENTER] para escribir Ctrl+V en tecla 2...")
send(2, [(0x01, 0x19)])   # Ctrl + V
input("[ENTER] para escribir Ctrl+Z en tecla 3...")
send(3, [(0x01, 0x1D)])   # Ctrl + Z
print("\n>> Prueba ahora las 3 teclas — deben funcionar.")
input("[ENTER] para terminar...")

dev.close()
print("[Listo]")
