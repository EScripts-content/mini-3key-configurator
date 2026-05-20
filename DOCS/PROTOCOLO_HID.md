# Protocolo HID — Mini Controladora USB (VID=0x1189, PID=0x8890)

Confirmado por reverse engineering de `MINI KeyBoard.exe` (software chino) con ILSpy.

---

## Comunicación básica

- **Report ID:** `0x03`
- **Tamaño paquete:** 65 bytes (`[ReportID, payload[0..63]]`)
- **Apertura:** `CreateFile` con `FILE_SHARE_READ | FILE_SHARE_WRITE`
- **Escritura:** `WriteFile` con 65 bytes

---

## Asignación de tecla (KeyType = Basic = 0x01)

Se envían **`num_keycodes + 1` paquetes** en loop, luego WriteFlash.

### Estructura de cada paquete:
| Byte | Valor | Descripción |
|------|-------|-------------|
| `[0]` | key_index | 1=Key1, 2=Key2, 3=Key3 |
| `[1]` | `KeyType & 0x0F` | 1=basic, 2=multimedia, 3=mouse, 8=LED |
| `[2]` | num_keycodes | Cantidad de keycodes (KeyGroupCharNum) |
| `[3]` | b | Loop counter (0..num_keycodes) |
| `[4]` | modifier | HID modifier del keycode b-1 (0 si b==0) |
| `[5]` | keycode | HID keycode del keycode b-1 (0 si b==0) |
| `[6..64]` | 0 | Padding |

### Modifiers HID:
| Tecla | Valor |
|-------|-------|
| Ctrl  | `0x01` |
| Shift | `0x02` |
| Alt   | `0x04` |
| Win   | `0x08` |

### Keycodes HID comunes:
| Tecla | Código |
|-------|--------|
| A | `0x04` |
| C | `0x06` |
| V | `0x19` |
| Z | `0x1D` |
| Tab | `0x2B` |

### Ejemplo — Ctrl+C en tecla 1:
```
PKT 1 (b=0): 03 01 01 01 00 01 00 ...
PKT 2 (b=1): 03 01 01 01 01 01 06 ...
WriteFlash:  03 AA AA 00 ...
```

---

## WriteFlash (persistir en flash)

| Comando | Paquete |
|---------|---------|
| Teclas  | `[0xAA, 0xAA, 0x00, ...]` |
| LEDs    | `[0xAA, 0xA1, 0x00, ...]` |

---

## LEDs (KeyType = 0x08)

**El hardware solo soporta 3 modos (0, 1, 2).** Confirmado por `LEDkey.cs` del software chino — solo tiene 3 botones: `KEY_LEDMode0`, `KEY_LEDMode1`, `KEY_LEDMode2`. Los modos 3, 4, 5 no existen en el dispositivo.

Paquete único + WriteFlashLED:

| Byte | Valor | Descripción |
|------|-------|-------------|
| `[0]` | `0xB0` | Key index fijo para LED (176 = `KeySet_KeyNum` para LED) |
| `[1]` | `0x08` | KeyType LED |
| `[2]` | mode | **Solo 0, 1, o 2** |

```
PKT LED:     03 B0 08 mode 00 ...
WriteFlash:  03 AA A1 00 ...
```

---

## Borrar tecla

`Key_Clear_Fun()` pone `Data_Send_Buff[KeySet_KeyNum] = 0`.  
Para borrar desde Python: enviar `send_config(key_index, key_sequence=[])`.
Con `num_keycodes=0` se envía 1 paquete `[key, 0x01, 0, 0, 0, 0]` + WriteFlash.

---

## Fuentes

- `MINI KeyBoard.exe` decompilado con ILSpy 10
- `HIDTester/FormMain.cs` — `Download_Click`, `Send_WriteFlash_Cmd`, `Send_WriteFlashLED_Cmd`
- `HIDTester/BasicKeys.cs` — `Key_Ctrl_Click`, `General_Char_Set`, `KEY_C_Click`
- `HIDTester/LEDkey.cs` — `KEY_LEDMode0_Click`, `LEDGeneral_Char_Set`
