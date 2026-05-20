# -*- coding: utf-8 -*-
"""
Comunicacion HID con el Mini Controlador USB.

- Enumeracion de dispositivos: pywinusb (confiable, ya probado)
- Escritura HID: Win32 API directa (ctypes) para enviar paquetes de 65 bytes
"""

import ctypes
from ctypes import wintypes
import config

# Win32 constants
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
OPEN_EXISTING = 3
FILE_FLAG_OVERLAPPED = 0x40000000
INVALID_HANDLE_VALUE = -1


def _find_device_path(vid=config.VID, pid=config.PID, interface_fragment=config.INTERFACE_CONFIG):
    """
    Buscar el path del dispositivo HID usando pywinusb (confiable).
    """
    try:
        from pywinusb.hid import HidDeviceFilter
    except ImportError:
        raise RuntimeError("pywinusb no esta instalado. Ejecuta: pip install pywinusb")

    devices = HidDeviceFilter(vendor_id=vid, product_id=pid).get_devices()
    if not devices:
        return None

    for dev in devices:
        if interface_fragment.lower() in dev.device_path.lower():
            return dev.device_path

    return None


def find_config_device(vid=config.VID, pid=config.PID, interface_fragment=config.INTERFACE_CONFIG):
    """Buscar el dispositivo de configuracion (mi_01)."""
    return _find_device_path(vid, pid, interface_fragment)


class HidDevice:
    """Maneja la comunicacion HID con el dispositivo mini controlador."""

    def __init__(self, device_path=None):
        self.device_path = device_path
        self._handle = None
        self._output_report_length = config.PACKET_SIZE

    def open(self):
        """Abrir conexion con el dispositivo via Win32 CreateFileW."""
        if self._handle is not None:
            return True

        if not self.device_path:
            self.device_path = find_config_device()
            if not self.device_path:
                raise RuntimeError(
                    "Dispositivo no encontrado. "
                    "Asegurate de que este conectado al puerto USB."
                )

        self._handle = ctypes.windll.kernel32.CreateFileW(
            self.device_path,
            GENERIC_READ | GENERIC_WRITE,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            None,
            OPEN_EXISTING,
            0,
            None
        )

        if self._handle == INVALID_HANDLE_VALUE:
            err = ctypes.windll.kernel32.GetLastError()
            self._handle = None
            raise RuntimeError(
                f"No se pudo abrir el dispositivo (Win32 error {err}). "
                f"Puede que otro programa lo este usando."
            )

        return True

    def close(self):
        """Cerrar conexion."""
        if self._handle is not None:
            ctypes.windll.kernel32.CloseHandle(self._handle)
            self._handle = None

    def is_open(self):
        return self._handle is not None

    def write_report(self, payload):
        """
        Escribir un report HID al dispositivo.

        Args:
            payload: lista de bytes del payload (sin Report ID). Max 64 bytes.

        El paquete final sera: [ReportID] + payload, rellenado a PACKET_SIZE.
        """
        if self._handle is None:
            raise RuntimeError("Dispositivo no abierto. Llama a open() primero.")

        # Construir paquete de 65 bytes
        packet = [config.REPORT_ID]
        packet.extend(payload)

        # Rellenar con ceros hasta PACKET_SIZE
        while len(packet) < config.PACKET_SIZE:
            packet.append(0)

        if len(packet) > config.PACKET_SIZE:
            packet = packet[:config.PACKET_SIZE]

        print(f"  PKT: {' '.join(f'{b:02X}' for b in packet[:16])}")

        buf = (ctypes.c_ubyte * config.PACKET_SIZE)(*packet)
        written = wintypes.DWORD(0)

        ok = ctypes.windll.kernel32.WriteFile(
            self._handle,
            ctypes.byref(buf),
            config.PACKET_SIZE,
            ctypes.byref(written),
            None
        )

        if not ok:
            err = ctypes.windll.kernel32.GetLastError()
            raise RuntimeError(f"Error al escribir al dispositivo (Win32 error {err})")

        return written.value

    def send_config(self, action_byte, layer=0, key_type=config.KeyType.BASIC,
                    delay=0, key_sequence=None):
        """
        Enviar configuracion de un atajo al dispositivo.

        Protocolo confirmado por reverse engineering del software chino (MINI KeyBoard.exe):
          - Data_Send_Buff[0] = key_index  (KeySet_KeyNum)
          - Data_Send_Buff[1] = KeyType    (1=basic, 2=multimedia, 3=mouse, 8=LED)
          - Data_Send_Buff[2] = num_keycodes (KeyGroupCharNum)
          - Data_Send_Buff[4] = modifier del primer keycode
          - Data_Send_Buff[5] = keycode del primer keycode
          - Data_Send_Buff[6] = modifier del segundo keycode, etc.

        Se envian (num_keycodes+1) paquetes en loop (b=0..num_keycodes):
          array[0]=key_index, array[1]=KeyType&0xF, array[2]=num_keycodes,
          array[3]=b, array[4]=modifier_b, array[5]=keycode_b
        Luego WriteFlash [0xAA, 0xAA].

        Args:
            action_byte: indice de tecla (1=Key1, 2=Key2, 3=Key3, ...)
            key_sequence: lista de tuplas (modifier, keycode). Max 6 keycodes.
        """
        import time

        if key_sequence is None:
            key_sequence = []

        # Construir Data_Send_Buff[4..] = [mod0, key0, mod1, key1, ...]
        # segun General_Char_Set: KEY_Char_Num empieza en 5, keycode en [5], mod en [6]
        # Para simplicidad: buff[4+2*i] = modifier[i], buff[5+2*i] = keycode[i]
        buff = [0] * 20
        num_keycodes = len(key_sequence)
        for i, (mod, key) in enumerate(key_sequence):
            buff[4 + i * 2] = mod & 0xFF
            buff[5 + i * 2] = key & 0xFF

        key_type_byte = 0x01  # basic keyboard

        # Loop b=0..num_keycodes (igual que el software chino)
        for b in range(num_keycodes + 1):
            if b == 0:
                mod_b = buff[4]
                key_b = 0
            else:
                mod_b = buff[4 + (b - 1) * 2]
                key_b = buff[5 + (b - 1) * 2]
            payload = [
                action_byte,       # [0] key index
                key_type_byte,     # [1] KeyType & 0x0F
                num_keycodes,      # [2] KeyGroupCharNum
                b,                 # [3] loop counter
                mod_b,             # [4] modifier
                key_b,             # [5] keycode
            ]
            self.write_report(payload)
            time.sleep(0.05)

        # WriteFlash para persistir
        self.write_report([0xAA, 0xAA])
        time.sleep(0.1)

    def set_led(self, mode, color=0, layer=0):
        """
        Establecer modo LED — protocolo Legacy confirmado por logs reales.

        Packet 1 — LedFunction:  [B0, 08, mode|color]
        Packet 2 — WriteFlash:   [AA, A1]

        mode:  0=Off 1=Respirar 2=Carrusel 3=Mode3 4=Mode4 5=Mode5
        color: 0=Random (los modos con color fijo no responden en este HW)
        """
        import time
        mode_byte = (mode | color) & 0xFF
        self.write_report([0xB0, 0x08, mode_byte])
        time.sleep(0.05)
        self.write_report([0xAA, 0xA1])
        time.sleep(0.05)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


def test_connection():
    """Prueba rapida de conexion con el dispositivo."""
    try:
        path = find_config_device()
        if path:
            return True, path
        return False, "Dispositivo no encontrado. Asegurate de que este conectado."
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    # Prueba
    ok, info = test_connection()
    if ok:
        print(f"[OK] Dispositivo encontrado: {info}")
    else:
        print(f"[ERROR] {info}")
