# Mini Configurator

Aplicacion moderna para configurar el Mini Controlador USB (3 botones + 1 knob).

## Caracteristicas

- **UI Moderna**: Diseno minimalista y oscuro inspirado en apps contemporaneas
- **Deteccion Automatica**: Encuentra el dispositivo USB al iniciar
- **6 Controles**: 3 botones + 3 acciones del knob (click, izquierda, derecha)
- **Deteccion de Teclas**: Presiona las teclas fisicamente y se capturan automaticamente
- **Entrada Manual**: Selecciona teclas y modificadores desde listas
- **Guardar Presets**: Guarda configuraciones locales en archivos JSON
- **Enviar a Dispositivo**: Escribe la configuracion directamente al controlador via HID

## Requisitos

- Windows 10/11
- Python 3.10+
- pywinusb (instalado automaticamente con uv)

## Como Ejecutar

```bash
cd mini_configurator
python main.py
```

O con uv:

```bash
uv run main.py
```

## Uso

1. **Conecta tu dispositivo** USB
2. **Selecciona un control** en el panel izquierdo (boton o accion del knob)
3. **Configura el atajo**:
   - Haz clic en "Detectar Teclas" y presiona la combinacion deseada
   - O usa "Agregar Manual" para seleccionar tecla y modificadores
4. **Guarda en el dispositivo** con el boton "Guardar en Dispositivo"
5. Opcional: Guarda un preset local con "Guardar Preset" para usarlo despues

## Estructura

| Archivo | Proposito |
|---------|-----------|
| `main.py` | Punto de entrada y UI completa |
| `config.py` | Constantes, keycodes, mapeos del protocolo HID |
| `hid_device.py` | Comunicacion HID nativa con Win32 API |
| `assets/` | Iconos e imagenes |
| `presets/` | Configuraciones guardadas localmente |

## Protocolo HID

Basado en el analisis del codigo descompilado de RSoft.MacroPad.BLL.dll:

- **VID**: 0x1189 | **PID**: 0x8890
- **Report ID**: 0x03
- **Tamano**: 65 bytes
- **Magic byte**: 0xFE

Formato del paquete:
```
[0x03, 0xFE, Action, Layer, KeyType, DelayLo, DelayHi, 0,0,0, KeyCount, mod1, key1, mod2, key2, ...]
```

## Limitaciones del Dispositivo

- Maximo 5 teclas por atajo
- Solo 1 layer de configuracion
- No soporta delay configurable
- LEDs solo con modos (no colores RGB)
- No permite leer la configuracion actual (solo escribir)

## Creditos

Protocolo descifrado del software RSoft.MacroPad v1.0.1 usando dnSpyEx.
