"""
Lee continuamente del dispositivo HID y muestra todos los paquetes recibidos.
Corre esto MIENTRAS usas el RSoft para grabar una tecla.
Así vemos exactamente qué manda el RSoft.
"""
import sys, ctypes, time
from ctypes import wintypes
sys.path.insert(0, r"H:\PROGRAMAS\PROGRAMAS PAGADOS\MINI CONTROLADORA USB\drive-download-20230810T081045Z-001\mini_configurator")
import config

GENERIC_READ       = 0x80000000
GENERIC_WRITE      = 0x40000000
FILE_SHARE_READ    = 0x00000001
FILE_SHARE_WRITE   = 0x00000002
OPEN_EXISTING      = 3
FILE_FLAG_OVERLAPPED = 0x40000000

def find_path():
    from hid_device import _find_device_path
    return _find_device_path(config.VID, config.PID, config.INTERFACE_CONFIG)

path = find_path()
print(f"[OK] Device: {path}\n")
print("Abre el RSoft y graba una tecla ahora. Presiona Ctrl+C para parar.\n")

# Abrir sin OVERLAPPED para lectura bloqueante simple
h = ctypes.windll.kernel32.CreateFileW(
    path,
    GENERIC_READ | GENERIC_WRITE,
    FILE_SHARE_READ | FILE_SHARE_WRITE,
    None, OPEN_EXISTING, 0, None
)

PACKET = 65
buf = (ctypes.c_ubyte * PACKET)()
read = wintypes.DWORD(0)

try:
    while True:
        ok = ctypes.windll.kernel32.ReadFile(h, ctypes.byref(buf), PACKET, ctypes.byref(read), None)
        if ok and read.value > 0:
            data = list(buf[:read.value])
            hex_str = ' '.join(f'{b:02X}' for b in data[:16])
            print(f"  RX ({read.value}b): {hex_str}")
except KeyboardInterrupt:
    pass

ctypes.windll.kernel32.CloseHandle(h)
print("\n[Listo]")
