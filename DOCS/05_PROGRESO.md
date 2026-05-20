# Log de Progreso - Mini Controlador USB

## 2026-05-19 - Sesion 1

### Inicio de Sesion
- Usuario solicita ayuda con mini controlador USB (3 botones + 1 knob)
- Descargo multiples controladores sin lograr configurarlo
- Objetivo: Encontrar driver correcto + redisenar UI

### Fase 1: Inventario de Archivos
- **Directorio**: `H:\PROGRAMAS\PROGRAMAS PAGADOS\MINI CONTROLADORA USB\drive-download-20230810T081045Z-001`
- **Archivos encontrados**:
  - `RSoft.MacroPad.v1.0.1/` - Software .NET 6.0
  - `MINI KEYBOARD TOOL V1/` - Software C# con HidLibrary
  - `Software old version/` - Software Qt5 (MinGW)
  - `New_Software nov 2025/` - Software Qt5 para modelo AX18 (15 teclas)
  - `Latest version-En-If your computer is not compatible.../` - Version alternativa C#
  - `3 key keyboard software-20251111.../` - Otra version del software C#
  - `Mini Keyboard Software Setting Manual.pdf` - Manual

### Fase 2: Analisis con Narsil MCP
- Estructura de directorios mapeada
- Archivos `config.txt` y `layouts.txt` de RSoft.MacroPad leidos
- Se identifica que el dispositivo del usuario tiene PID `34960` (decimal)
- Layout exacto encontrado: `3 buttons 1 knob` con VID=4489, PID=34960

### Fase 3: Identificacion del Dispositivo
- Usuario proporciona Hardware IDs:
  ```
  HID\VID_1189&PID_8890&REV_0000&MI_02&Col01
  HID\VID_1189&PID_8890&MI_02&Col01
  ```
- Confirma VID=0x1189, PID=0x8890
- Driver: `input.inf` de Microsoft (HID estandar)

### Fase 4: Diagnostico HID con Python
- Creado `hid_diagnose.py` usando `pywinusb`
- **Resultado**: 2 dispositivos encontrados
  - Device 1 (mi_01): Vendor-defined, Input=1, Output=1
  - Device 2 (mi_02): Consumer Control (0x000C:0x0001), Input=1
- Problema: Handler de input no se pudo configurar con pywinusb

### Fase 5: Capabilities HID via Windows API
- Creado `get_hid_descriptor.py` usando `ctypes` + `hid.dll`
- **Resultados criticos obtenidos**:
  - **Device 1 (mi_01)**:
    - UsagePage: 0xFF00, Usage: 0x0001
    - InputReportByteLength: 65
    - OutputReportByteLength: 65
    - NumberInputValueCaps: 1
    - NumberOutputButtonCaps: 1
  - **Device 2 (mi_02)**:
    - UsagePage: 0x000C, Usage: 0x0001
    - InputReportByteLength: 3

### Fase 6: Pruebas de Protocolo (Fallidas)
- Creado `hid_protocol_test.py` y `hid_protocol_probe.py`
- Intentados multiples comandos de lectura (0x01, 0x02, 0xFF, etc.)
- **Problema**: pywinusb no recibe datos asincronos del dispositivo
- **Problema**: Los paquetes de 65 bytes enviados no generan respuesta
- **Hipotesis**: El dispositivo no responde a comandos de lectura, solo a escritura

### Fase 7: Interaccion con Usuario
- Usuario confirma que **alguno de los programas funciono anteriormente**
- No recuerda cual fue
- Usuario desea redisenar la UI lo mas moderno posible
- Entrega documento `UI de suenos.md` con requisitos detallados

### Fase 8: Instalacion de Herramientas
- Usuario instala dnSpyEx y Procmon en:
  `J:\SCRIPTS LEO\MULTIAGENTES windsurf\Tools\`

### Fase 9: Descompilacion con dnSpyEx
- Ejecutado dnSpy.Console.exe exitosamente
- Descompilados todos los DLLs de RSoft.MacroPad
- **Directorio de salida**: `decompiled/RSoft.MacroPad.BLL/`

### Fase 10: Descifrado del Protocolo HID
**Archivos clave analizados**:
- `ExtendedReport.cs` - Constructor de paquetes HID
- `ExtendedReportComposer.cs` - Compositor
- `Hid.cs` - Metodo Write() revela formato exacto
- `report.cs` - Estructura del report
- `InputAction.cs` - Mapeo de botones/knobs a bytes
- `KeyCode.cs` - Codigos de teclas HID
- `Modifier.cs` - Flags de modificadores
- `MediaKey.cs` - Teclas multimedia
- `KeyType.cs` - Tipos de configuracion

**Descubrimientos clave**:
1. Paquete de 65 bytes: `[ReportID=0x03, 0xFE, Action, Layer, KeyType, DelayLo, DelayHi, 0,0,0, KeyCount, ...keys]`
2. Botones: Key1=1, Key2=2, Key3=3
3. Knob: Left=23, Push=24, Right=25
4. Keycodes estandar HID (A=4, B=5, etc.)
5. Modifiers: Ctrl=1, Shift=2, Alt=4, Win=8
6. Media keys con valores especificos (PlayPause=205, etc.)
7. Metodo Write() en C# escribe exactamente 65 bytes via FileStream

### Fase 11: Correccion de RSoft.MacroPad
- Editado `config.txt` linea 12: cambiado `mi_00` a `mi_01`
- **Resultado**: RSoft.MacroPad ahora detecta el dispositivo
- Usuario confirma: "Abre bien dice conected"

### Fase 12: Documentacion
Creada carpeta `DOCS/` con 5 archivos markdown:
1. `01_PROTOCOLO_HID.md` - Protocolo completo descifrado
2. `02_DISPOSITIVO.md` - Especificaciones del hardware
3. `03_ANALISIS_SOFTWARE.md` - Analisis de software existente
4. `04_UI_REQUERIMIENTOS.md` - Requisitos de UI del usuario
5. `05_PROGRESO.md` - Este log

### Pendientes para Siguiente Sesion
- [ ] Implementar aplicacion Python con UI moderna (tkinter)
- [ ] Implementar comunicacion HID nativa con Win32 API (ctypes)
- [ ] Implementar captura de teclas automatica
- [ ] Probar envio de configuracion al dispositivo real
- [ ] Validar que los atajos funcionan correctamente

### Herramientas Disponibles
- Python 3.14.0
- pywinusb 0.4.2
- dnSpyEx (descompilador .NET)
- Procmon (monitor de procesos Windows)
- Protocolo HID completamente documentado

### Archivos Creados en esta Sesion
| Archivo | Proposito |
|---------|-----------|
| `hid_diagnose.py` | Diagnostico HID basico |
| `get_hid_descriptor.py` | Obtener capabilities HID via Windows API |
| `hid_protocol_test.py` | Pruebas de protocolo |
| `hid_protocol_probe.py` | Probar paquetes de configuracion |
| `hid_config_probe.py` | Probar comando 0xFE basado en hid.log |
| `extract_strings.py` | Extraer strings de binarios |
| `inspect_net.ps1` | Inspeccionar assembly .NET |
| `DOCS/01_PROTOCOLO_HID.md` | Documentacion de protocolo |
| `DOCS/02_DISPOSITIVO.md` | Especificaciones hardware |
| `DOCS/03_ANALISIS_SOFTWARE.md` | Analisis software |
| `DOCS/04_UI_REQUERIMIENTOS.md` | Requisitos UI |
| `DOCS/05_PROGRESO.md` | Log de progreso |

## 2026-05-19 - Sesion 2 (Investigacion LED)

### Fase 13: HID Report Descriptor Completo
- Creado `extract_hid_descriptor_v2.py` con parsing profundo de HIDP_CAPS, ButtonCaps, ValueCaps y raw descriptor
- **Resultado critico**:
  - **mi_01**: NO hay Feature Reports (FeatureReportByteLength=0, 0 Feature caps)
  - **mi_01**: Input=ReportID=3, UsagePage=0xFF00, Usage=0x0002, array de 64 bytes (BitSize=8, ReportCount=64)
  - **mi_01**: Output=ReportID=3, UsagePage=0xFF00, Usage=0x0002, array de 64 bytes
  - **mi_02**: Consumer Control, Input=ReportID=2, 3 bytes
  - **No hay LED usages en el descriptor HID**

### Fase 14: Feature Reports Ocultos
- Creado `probe_feature_reports.py` que prueba HidD_GetFeature y HidD_SetFeature con 256 ReportIDs
- **Resultado**: Ningun ReportID responde a GetFeature. SetFeature falla para TODOS los payloads LED probados.
- **Conclusion**: NO hay feature reports ocultos.

### Fase 15: Codigo Descompilado LED (Hallazgo Critico)
**Archivos analizados en profundidad**:
- `Infrasturture/Model/LedMode.cs` - Enum: Mode0..Mode5
- `Infrasturture/Model/LedColor.cs` - Enum: Random, Red=16, Orange=32, ..., Purple=112
- `Infrasturture/Protocol/Legacy/LedFunctionReport.cs` - Data=[0xB0, 0x08, mode|color]
- `Infrasturture/Protocol/Legacy/WriteFlashReport.cs` - Data=[0xAA, led?0xA1:0xAA]
- `Infrasturture/Protocol/ExtendedReport.cs` - CreateLed(action=0xB0, keytype=8, data=[layer, mode|color])
- `Infrasturture/Protocol/LegacyReportComposer.cs` - Led() envia LedFunction + WriteFlash
- `Infrasturture/UsbDevice/DeviceSample.cs` - CONFIRMA: nuestro dispositivo es (4489,34960,"mi_01",ProtocolType.Legacy)
- `Infrasturture/UsbDevice/UsbBase.cs` - KeyBoardVersionCheck() envia VersionCheck(0) luego (2), fallback a Version=3
- `HID/Hid.cs` - Write() exacto: paquete de 65 bytes [ReportId, Data...0s] via FileStream

**Protocolo Legacy LED exacto**:
```
Paquete 1: [0x03, 0xB0, 0x08, mode|color, 0x00...] (65 bytes)
Paquete 2: [0x03, 0xAA, 0xA1, 0x00...] (65 bytes)
```

**Protocolo Extended LED exacto**:
```
Paquete: [0x03, 0xFE, 0xB0, layer, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, layer, mode|color, 0x00...] (65 bytes)
```

### Fase 16: Prueba Exhaustiva LED
- Creado `probe_led_exhaustive.py` probando:
  - Legacy exacto (modos 0-5 + WriteFlash)
  - Extended exacto (modos 0-5)
  - Sin WriteFlash
  - WriteFlash led=false (0xAA,0xAA)
  - Diferentes ReportIDs (solo 0x03 funciona)
  - Brute force de 40+ magic bytes
  - Modos fuera de rango (3-255)
  - Payloads cortos (3-8 bytes)
  - LayerSelect + LED (layers 0-3)
- **Resultado**: WriteFile OK=1 para TODOS los paquetes con ReportID=3, pero el firmware NO reacciona.

### Fase 17: Flujo Exacto RSoft.MacroPad
- Creado `test_led_exact_rsoft.py` que replica 100% el flujo de conexion de RSoft:
  - Abre con FILE_FLAG_OVERLAPPED + shareMode=0 (exacto como RSoft)
  - Envio VersionCheck(0) -> falla (OK=0)
  - Envio VersionCheck(2) -> falla (OK=0)
  - Version=3 (igual que RSoft)
  - Luego envio LED Legacy exacto
- **Resultado sorpresa**: Con shareMode=0 (exclusivo), los writes FALLAN (OK=0) incluso para LED. Esto sugiere que otro proceso (driver/sistema) ya tiene el handle abierto.
- **Nota**: Con FILE_SHARE_READ|FILE_SHARE_WRITE (como mini_configurator), los writes SI funcionan.

### Fase 18: Monitor RSoft.MacroPad
- Creado `monitor_rsoft.ps1` para capturar trafico HID con Procmon
- Requiere ejecucion manual por el usuario mientras cambia LEDs en RSoft.MacroPad
- Pendiente de ejecucion por el usuario.

### Hallazgo Critico sobre LEDs
**Los comandos LED SI funcionan — el usuario confirmo ver los LEDs prender y cambiar durante las pruebas.**

Esto significa que:
1. El firmware SI tiene handler para comandos LED (via paquetes Output Report de 65 bytes)
2. El protocolo Legacy es el correcto: `Data=[0xB0, 0x08, mode|color]` seguido de `WriteFlash=[0xAA, 0xA1]`
3. La falta de Feature Reports no impide el control LED (se hace via Output Reports)
4. El `layouts.txt` (`1:5:0:0:3`) indica 3 modos y sin color configurable, pero los colores del enum `LedColor` (Red=16, Green=64, etc.) parecen tener efecto

**Pendiente**: Determinar exactamente que combinaciones de mode+color producen que efectos visuales. El usuario observo LEDs prendiendo "uno por uno", combinando, pulsando, y colores fijos.

### Pendientes
- [ ] Ejecutar `monitor_rsoft.ps1` para confirmar que RSoft.MacroPad no hace nada diferente
- [ ] Implementar aplicacion Python con UI moderna (tkinter) para configurar atajos
- [ ] Validar que la configuracion de atajos (key/mouse/media) SI funciona correctamente

### Archivos Creados en esta Sesion
| Archivo | Proposito |
|---------|-----------|
| `TESTS/extract_hid_descriptor_v2.py` | Descriptor HID completo con ButtonCaps/ValueCaps |
| `TESTS/probe_feature_reports.py` | Buscar Feature Reports ocultos |
| `TESTS/probe_led_exhaustive.py` | Prueba exhaustiva de todos los comandos LED |
| `TESTS/test_led_exact_rsoft.py` | Flujo EXACTO de RSoft.MacroPad |
| `TESTS/monitor_rsoft.ps1` | Capturar trafico HID de RSoft con Procmon |
