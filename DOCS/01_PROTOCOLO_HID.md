# Protocolo HID - Mini Controlador USB (3 Botones + 1 Knob)

## Dispositivo

| Campo | Valor |
|-------|-------|
| Vendor ID (VID) | `0x1189` (4489 decimal) |
| Product ID (PID) | `0x8890` (34960 decimal) |
| Interface Configuracion | `mi_01` |
| Interface Teclas (Consumer) | `mi_02` |
| Protocolo | Extended (Version 1) |
| Report ID | `0x03` |
| Tamanio Report | 65 bytes (1 Report ID + 64 payload) |

## Canales HID

### Canal 1: Configuracion (mi_01)
- **UsagePage**: `0xFF00` (Vendor-defined)
- **Usage**: `0x0001`
- **InputReportByteLength**: 65
- **OutputReportByteLength**: 65
- **FeatureReportByteLength**: 0
- **Proposito**: Enviar configuracion de atajos al dispositivo

### Canal 2: Consumer Control (mi_02)
- **UsagePage**: `0x000C` (Consumer Control)
- **Usage**: `0x0001`
- **InputReportByteLength**: 3
- **OutputReportByteLength**: 0
- **Proposito**: Emite teclas multimedia (volumen, play/pause, etc.)

## Formato del Paquete de Configuracion (Extended Protocol)

El paquete se construye asi (65 bytes total):

```
Byte  0: Report ID = 0x03
Byte  1: 0xFE (Magic byte / comando)
Byte  2: Action (indice del boton/knob)
Byte  3: Layer number (0, 1, 2...)
Byte  4: Key Type (0=None, 1=Basic, 2=Multimedia, 3=Mouse, 8=LED)
Byte  5: Delay (low byte)
Byte  6: Delay (high byte)
Byte  7: 0 (reservado)
Byte  8: 0 (reservado)
Byte  9: 0 (reservado)
Byte 10: Key count (cantidad de pares modifier+key)
Byte 11+: Key data (pares de [modifier, keycode])
```

### Acciones (InputAction enum)

| Valor | Nombre | Descripcion |
|-------|--------|-------------|
| 0 | None | Sin accion |
| 1 | Key1 | Boton 1 |
| 2 | Key2 | Boton 2 |
| 3 | Key3 | Boton 3 |
| 23 | Knob1Left | Knob izquierda (counter-clockwise) |
| 24 | Knob1Push | Knob presion |
| 25 | Knob1Right | Knob derecha (clockwise) |

### KeyCode (HID Usage Page Keyboard)

Los keycodes usan los codigos estandar USB HID:

| Tecla | Valor | Tecla | Valor |
|-------|-------|-------|-------|
| A | 4 | N | 17 |
| B | 5 | O | 18 |
| C | 6 | P | 19 |
| D | 7 | Q | 20 |
| E | 8 | R | 21 |
| F | 9 | S | 22 |
| G | 10 | T | 23 |
| H | 11 | U | 24 |
| I | 12 | V | 25 |
| J | 13 | W | 26 |
| K | 14 | X | 27 |
| L | 15 | Y | 28 |
| M | 16 | Z | 29 |
| D1 | 30 | F1 | 58 |
| D2 | 31 | F2 | 59 |
| D3 | 32 | F3 | 60 |
| D4 | 33 | F4 | 61 |
| D5 | 34 | F5 | 62 |
| D6 | 35 | F6 | 63 |
| D7 | 36 | F7 | 64 |
| D8 | 37 | F8 | 65 |
| D9 | 38 | F9 | 66 |
| D0 | 39 | F10 | 67 |
| Enter | 40 | F11 | 68 |
| Esc | 41 | F12 | 69 |
| Backspace | 42 | PrtSc | 70 |
| Tab | 43 | ScrollLock | 71 |
| Space | 44 | PauseBreak | 72 |
| Minus | 45 | Insert | 73 |
| Plus | 46 | Home | 74 |
| OpenBracket | 47 | PgUp | 75 |
| CloseBracket | 48 | Del | 76 |
| Pipe | 49 | End | 77 |
| Tilde | 53 | PgDn | 78 |
| Colon | 51 | ArrowRight | 79 |
| Backslash | 50 | ArrowLeft | 80 |
| Clear | 54 | ArrowDown | 81 |
| Period | 55 | ArrowUp | 82 |
| Question | 56 | Num | 83 |
| CapsLock | 57 | App | 101 |

### Modifier Flags (bitmask)

| Flag | Valor |
|------|-------|
| None | 0 |
| Ctrl | 1 |
| Shift | 2 |
| Alt | 4 |
| Win | 8 |
| RightCtrl | 16 |
| RightShift | 32 |
| RightAlt | 64 |
| RightWin | 128 |

### Media Keys (Extended Protocol)

Para tipo Multimedia (KeyType=2), el payload es 4 bytes:

```
[0, B1, B2, 0]
```

| Media Key | B1 | B2 |
|-----------|----|----|
| PlayPause | 205 | 0 |
| NextTrack | 181 | 0 |
| PrevTrack | 182 | 0 |
| VolMute | 226 | 0 |
| VolUp | 233 | 0 |
| VolDn | 234 | 0 |

## Ejemplo: Enviar "CTRL + C" al Boton 1

```python
packet = [
    0x03,        # Report ID
    0xFE,        # Magic
    0x01,        # Action = Key1 (Boton 1)
    0x00,        # Layer 0
    0x01,        # KeyType = Basic
    0x00, 0x00,  # Delay = 0
    0x00, 0x00, 0x00,  # Reservado
    0x01,        # Key count = 1 par
    0x01,        # Modifier = Ctrl
    0x06,        # KeyCode = C (valor 6)
    # ... resto rellenado con ceros hasta 65 bytes
]
```

## Como Enviar el Paquete en Python

```python
import ctypes
from ctypes import wintypes

# Abrir dispositivo
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
OPEN_EXISTING = 3

device_path = r"\\?\hid#vid_1189&pid_8890&mi_01#..."

handle = ctypes.windll.kernel32.CreateFileW(
    device_path,
    GENERIC_READ | GENERIC_WRITE,
    FILE_SHARE_READ | FILE_SHARE_WRITE,
    None,
    OPEN_EXISTING,
    0,
    None
)

# Construir paquete de 65 bytes
packet = [0x03, 0xFE, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x06]
packet += [0x00] * (65 - len(packet))

# Enviar
buf = (ctypes.c_ubyte * 65)(*packet)
bytes_written = wintypes.DWORD()
ctypes.windll.kernel32.WriteFile(handle, ctypes.byref(buf), 65, ctypes.byref(bytes_written), None)

# Cerrar
ctypes.windll.kernel32.CloseHandle(handle)
```

## Metodo de Escritura en RSoft.MacroPad.BLL (referencia C#)

```csharp
public Hid.HID_RETURN Write(report r)
{
    byte[] array = new byte[this.outputReportLength];  // 65 bytes
    array[0] = r.reportID;  // 0x03
    int num = ((r.reportBuff.Length >= this.outputReportLength - 1)
        ? (this.outputReportLength - 1)
        : r.reportBuff.Length);
    for (int i = 1; i <= num; i++)
    {
        array[i] = r.reportBuff[i - 1];
    }
    this.hidDevice.Write(array, 0, 65);
    return Hid.HID_RETURN.SUCCESS;
}
```

## Notas Importantes

1. **Report ID**: Siempre `0x03` para este dispositivo
2. **Magic byte**: Siempre `0xFE` en la posicion 1 del payload
3. **Key count**: En la posicion 10 del payload (Byte 10 del array total), indica cuantos pares modifier+key se envian
4. **Relleno**: El paquete siempre debe ser exactamente 65 bytes
5. **Origen de datos**: Los keycodes son HID Usage Page Keyboard estandar (USB HID spec)

## Limitaciones del Dispositivo

Segun `layouts.txt` (RSoft.MacroPad):

```
Layout: 3 buttons 1 knob
    4489:34960
    1:5:0:0:3   <-- 1 layer, max 5 chars, no delay, no LED color, 3 LED modes
    B1,5,5
    B2,25,5
    B3,45,5
    K1,70,5
```

- **Layers**: Solo 1 layer (no hay layers multiples)
- **Max caracteres**: 5 caracteres maximo por secuencia
- **Delay**: No soporta delay configurado (siempre 0)
- **LED Color**: No soporta color configurable
- **LED Modes**: 3 modos disponibles
