# Analisis del Software Existente

## Software Descargado

### 1. RSoft.MacroPad v1.0.1
**Ubicacion**: `RSoft.MacroPad.v1.0.1/`

| Campo | Valor |
|-------|-------|
| Plataforma | .NET 6.0 |
| Tipo | Aplicacion de escritorio |
| Libreria HID | HID.dll (custom) |
| Estado | **FUNCIONA** (con correccion de config.txt) |

**Correccion necesaria**:
El archivo `config.txt` apuntaba a `mi_00` pero el dispositivo real usa `mi_01`.

Cambio realizado:
```
# Antes (NO funcionaba)
4489:34960,mi_00,1

# Despues (FUNCIONA)
4489:34960,mi_01,1
```

**Protocolo soportado**: Extended (Version 1)

**Archivos clave**:
- `config.txt`: Configuracion de dispositivos soportados
- `layouts.txt`: Definicion de layouts visuales
- `RSoft.MacroPad.BLL.dll`: Logica de negocio (descompilada)

**Codigo descompilado encontrado**:
- `ExtendedReport.cs`: Constructor de paquetes HID
- `ExtendedReportComposer.cs`: Compositor de reports
- `Hid.cs`: Comunicacion HID nativa
- `InputAction.cs`: Enumeracion de acciones (botones/knobs)
- `KeyCode.cs`: Codigos de teclas HID
- `Modifier.cs`: Flags de modificadores (Ctrl, Shift, Alt, Win)

---

### 2. MINI KeyBoard Tool V1 (C#)
**Ubicacion**: `MINI KEYBOARD TOOL V1/Release/`

| Campo | Valor |
|-------|-------|
| Plataforma | .NET Framework |
| Libreria | HidLibrary.dll (terceros) |
| Estado | Varias versiones, algunas con errores conocidos |

**Errores conocidos**:
- `errorLog.txt` muestra excepcion `InvalidOperationException` en `Dispose()`
- Problema al cerrar la ventana cuando se esta creando un handle

**Notas**:
- Usa HidLibrary.dll para comunicacion HID
- Tiene soporte para multiples modelos
- Incluye traducciones zh-CN y en-US

---

### 3. MINI KeyBoard (Qt5 - Version Vieja)
**Ubicacion**: `Software old version/`

| Campo | Valor |
|-------|-------|
| Framework | Qt5.14.2 / Qt5.12.2 |
| Compilador | MinGW (libgcc, libstdc++) |
| Libreria HID | hidapi.dll |
| Estado | **Compilado, funciona standalone** |

**Strings encontrados en binario**:
- `receiveData the value is` - Confirma protocolo bidireccional
- `command` / `Right command` - Comandos especificos
- `pushButton_K1` a `pushButton_K15` - Soporta hasta 15 teclas
- `MiNi KeyBoard` - Nombre del programa

**Notas**:
- Es un programa Qt5 compilado con MinGW
- Requiere DLLs de Qt5 para ejecutarse
- El codigo fuente original esta en los archivos `.o` y `moc_*.cpp`
- Dialog2 tiene funciones `sendData` y `receiveData`

---

### 4. MINI_KEYBOARD (Qt5 - Nov 2025)
**Ubicacion**: `New_Software nov 2025/AX18.../`

| Campo | Valor |
|-------|-------|
| Modelo | AX18 - 15 teclas |
| Framework | Qt5 |
| Estado | **Probablemente NO es para este dispositivo** |

**Notas**:
- Este software es para el modelo AX18 con 15 teclas
- Probablemente incompatible con el dispositivo de 3 botones + knob

---

## Comparativa

| Software | Funciona | Protocolo | UI | Estabilidad |
|----------|----------|-----------|-----|-------------|
| RSoft.MacroPad | Si (con fix) | Extended | Moderna | Buena |
| MINI KeyBoard (C#) | Parcial | Desconocido | Basica | Con errores |
| MINI KeyBoard (Qt5) | Probablemente | Legacy | Qt5 | Desconocida |
| AX18 (Qt5) | No | - | Qt5 | - |

## Conclusion del Analisis

**RSoft.MacroPad es la mejor opcion** porque:
1. Ya soporta exactamente nuestro modelo (3 botones + 1 knob)
2. Usa el protocolo Extended que desciframos
3. Tiene codigo .NET descompilable para entender el protocolo
4. Solo requeria un fix menor en config.txt
5. Tiene UI mas moderna que los otros

**Para crear nuevo software**:
- Usar el protocolo Extended descifrado de RSoft.MacroPad
- Implementar comunicacion HID directa con Win32 API
- Crear UI moderna en Python con tkinter o similar
- Soportar los 6 controles (3 botones + 3 acciones del knob)
