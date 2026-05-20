# Mini 3Key Configurator

Configurador para el mini controlador USB de 3 botones + 1 knob (VID=0x1189, PID=0x8890).  
Protocolo HID descifrado por reverse engineering del software original.

[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://paypal.me/ESpayments)

## Caracteristicas

- **UI moderna** oscura y minimalista
- **Deteccion automatica** del dispositivo al conectar
- **3 botones + knob** (click, izquierda, derecha) — 6 controles en total
- **Captura de teclas fisica** — presiona la combinacion y se detecta sola
- **Entrada manual** — selecciona tecla y modificadores desde listas
- **Presets JSON** — guarda y carga configuraciones locales
- **Modos LED** — Off, Mode 1, Mode 2
- **Protocolo confirmado** — mismo paquete que el software chino original

## Requisitos

- Windows 10/11
- Python 3.10+
- `pip install pynput hidapi`

## Como Ejecutar

```bash
cd mini_configurator
python main.py
```

## Como Usar

1. Conecta el dispositivo USB
2. Selecciona un boton o accion del knob en el panel izquierdo
3. Presiona **Detectar Teclas** y luego la combinacion fisica (ej. Ctrl+C)
4. Click **Guardar en Dispositivo**
5. Opcional: guarda un preset con **Guardar Preset**

## Estructura

| Archivo | Proposito |
|---------|-----------|
| `main.py` | UI completa (tkinter) |
| `hid_device.py` | Comunicacion HID via Win32 API |
| `config.py` | Keycodes, modificadores, constantes del protocolo |
| `keyboard_detector.py` | Captura de teclas con pynput (independiente del layout) |

## Protocolo HID

Confirmado por reverse engineering de `MINI KeyBoard.exe`:

- **VID/PID**: 0x1189 / 0x8890, interfaz `mi_01`
- **Report ID**: 0x03, 65 bytes
- **Paquete tecla**: `[key_index, key_type, num_keys, loop, modifier, keycode]`
- **WriteFlash teclas**: `[0xAA, 0xAA]`
- **WriteFlash LEDs**: `[0xAA, 0xA1]`

Ver `DOCS/PROTOCOLO_HID.md` para documentacion completa.

## Limitaciones

- Maximo 5 teclas por atajo
- Solo 3 modos LED (0=Off, 1, 2)
- No permite leer configuracion actual del dispositivo (solo escribir)

## Contribuir

Pull requests bienvenidos. Para cambios grandes abre un issue primero.

## Donar

Si te fue util, puedes invitarme un cafe:  
👉 [paypal.me/ESpayments](https://paypal.me/ESpayments)
