# Analisis del Software Existente

## Software Principal: MINI KeyBoard (Firmware Original)

**Ubicacion**: `VERSIONES DESCARGDAS/3 key keyboard software-.../Release/`

| Campo | Valor |
|-------|-------|
| Nombre | MINI KeyBoard.exe |
| Plataforma | .NET Framework (C#) |
| Libreria HID | HidLibrary.dll (terceros) |
| Estado | **FUNCIONA** (software oficial del fabricante chino) |
| Modelo | 3 botones + 1 knob (encoder) |

Este es el **software original del dispositivo**. Se descompilo con herramientas .NET para entender el protocolo HID exacto que usa el firmware del controlador.

---

### Archivos Descompilados Clave

| Archivo | Que contiene |
|---------|-------------|
| `HIDTester/FormMain.cs` | UI principal, logica de Download, configuracion de controles |
| `HIDTester/BasicKeys.cs` | Configuracion de teclas basicas (asignacion de shortcuts) |
| `HIDTester/FunKey.cs` | Teclas de funcion multimedia |
| `HIDTester/MULKey.cs` | Teclas multi-funcion (macros) |
| `HIDTester/MouseKey.cs` | Teclas de raton (click, scroll) |
| `HIDTester/LEDkey.cs` | Control de LEDs del dispositivo |
| `HIDTester/LayerFun.cs` | Funciones de capas (layers) |
| `HIDTester/HidLib.cs` | Wrapper sobre HidLibrary.dll |

---

### Descubrimientos del Codigo Descompilado

#### 1. Bytes de Accion (Action Bytes)

El software confirma los indices exactos usados para cada control:

| Control | Action Byte | Nombre en codigo |
|---------|-------------|------------------|
| Boton 1 | 1 | Key 1 |
| Boton 2 | 2 | Key 2 |
| Boton 3 | 3 | Key 3 |
| Knob Left | 13 | K1 Left |
| Knob Press | 14 | K1 Centre |
| Knob Right | 15 | K1 Right |

**Codigo descompilado**:
```csharp
private void K1_Left_Click(object sender, EventArgs e) {
    KeyParam.Data_Send_Buff[KeyParam.KeySet_KeyNum] = 13; // Knob Left
}

private void K1_Centre_Click(object sender, EventArgs e) {
    KeyParam.Data_Send_Buff[KeyParam.KeySet_KeyNum] = 14; // Knob Press
}

private void K1_Right_Click(object sender, EventArgs e) {
    KeyParam.Data_Send_Buff[KeyParam.KeySet_KeyNum] = 15; // Knob Right
}
```

> **Nota**: En versiones anteriores del firmware se habian visto bytes 23/24/25, pero el software oficial del fabricante usa **13/14/15**. Esto confirma que el firmware correcto para este dispositivo usa 13/14/15.

#### 2. Estructura del Paquete HID

```csharp
private void Download_Click(object sender, EventArgs e) {
    byte[] array = new byte[65];      // Report de 65 bytes
    array[0] = KeyParam.Data_Send_Buff[KeyParam.KeySet_KeyNum]; // Action byte
    // ... construccion del paquete segun tipo de tecla
}
```

**Buffer de envio** (`Data_Send_Buff`):
- Indice 0: Action byte (1-3, 13-15)
- Indice 1: KeyType (1=basic, 2=media, 3=mouse, 4=multi)
- Indices siguientes: keycodes y modifiers

#### 3. Tipos de Tecla Soportados

| KeyType | Valor | Descripcion |
|---------|-------|-------------|
| Basic Key | 0x01 | Teclas estandar + modificadores |
| Media Key | 0x02 | Play, Pause, Vol+, Vol-, Mute |
| Mouse Key | 0x03 | Click, scroll, move |
| Multi Key | 0x04 | Macros de multiples teclas |

#### 4. Secuencia de Envio (Download_Click)

El metodo `Download_Click` en `FormMain.cs` revela la secuencia exacta:

**Paso 1: Preparar el buffer de 65 bytes**
```csharp
byte[] array = new byte[65];
array[0] = KeyParam.Data_Send_Buff[KeyParam.KeySet_KeyNum];  // Action byte (1-3, 13-15)
```

**Paso 2: Enviar paquetes en bucle**

Para cada tecla en la secuencia, se envia un paquete con:
- `array[0]` = Action byte (indice del control)
- `array[1]` = KeyType (1=basic, 2=media, 3=mouse, 4=multi)
- `array[2]` = Numero de keycodes en la secuencia
- `array[3]` = Indice del paquete actual (0, 1, 2...)
- `array[4]` = Modifier del keycode actual
- `array[5]` = Keycode actual

**Ejemplo: Enviar Ctrl+C al Boton 1**
```csharp
// Paquete 0 (primer keycode)
array[0] = 1;   // Action = Boton 1
array[1] = 1;   // KeyType = Basic
array[2] = 1;   // 1 keycode total
array[3] = 0;   // Paquete 0
array[4] = 1;   // Modifier = Ctrl
array[5] = 6;   // Keycode = C
myHidLib.WriteData(array, 65);  // Enviar 65 bytes
```

**Paso 3: Comando WriteFlash (guardar en memoria)**

Despues de enviar todos los paquetes, se manda el comando especial para guardar permanentemente:
```csharp
// Comando WriteFlash
array[0] = 0xAA;
array[1] = 0xAA;
myHidLib.WriteData(array, 65);
```

> **Nota**: Este `0xAA 0xAA` es el comando que confirma la escritura en la memoria flash del dispositivo. Sin este comando, los cambios se pierden al desconectar.

#### 5. Tipos de Tecla y Payloads

| KeyType | Valor | Como se envia |
|---------|-------|---------------|
| Basic | 0x01 | Modifier + Keycode (pairs) |
| Media | 0x02 | 4 bytes especiales (play, vol, etc.) |
| Mouse | 0x03 | Click/scroll/move |
| Multi | 0x04 | Hasta 5 keycodes consecutivos |

**Basic Key (ejemplo: Ctrl+Shift+T)**:
```csharp
array[0] = action;      // 1-3 o 13-15
array[1] = 1;           // KeyType = Basic
array[2] = 3;           // 3 keycodes
array[3] = 0;           // Paquete 0
array[4] = 0x03;        // Ctrl+Shift (modifiers OR)
array[5] = 20;          // T
myHidLib.WriteData(array, 65);
```

---

## Software de Referencia: RSoft.MacroPad v1.0.1

**Ubicacion**: `RSoft.MacroPad.v1.0.1/`

| Campo | Valor |
|-------|-------|
| Plataforma | .NET 6.0 |
| Tipo | Aplicacion de escritorio de terceros |
| Libreria HID | HID.dll (custom) |
| Estado | **FUNCIONA** (con correccion de config.txt) |

**Nota**: Este software NO es del fabricante original. Es un software de terceros que resulto compatible con el dispositivo y sirvio como **referencia cruzada** para confirmar el protocolo.

**Correccion necesaria**:
El archivo `config.txt` apuntaba a `mi_00` pero el dispositivo real usa `mi_01`.

```
# Antes (NO funcionaba)
4489:34960,mi_00,1

# Despues (FUNCIONA)
4489:34960,mi_01,1
```

**Archivos descompilados utiles**:
- `ExtendedReport.cs`: Confirma estructura de paquetes HID
- `InputAction.cs`: Confirma enumeracion de acciones
- `KeyCode.cs`: Confirma mapeo de teclas HID

---

## Otros Softwares Analizados

### MINI KeyBoard Tool V1 (C#)
**Ubicacion**: `MINI KEYBOARD TOOL V1/Release/`

Version anterior/alternativa del software oficial. Tiene errores conocidos (`InvalidOperationException` en `Dispose()`). Usa `HidLibrary.dll`.

### MINI KeyBoard (Qt5 - Version Vieja)
**Ubicacion**: `Software old version/`

Software legacy en Qt5 con `hidapi.dll`. Probablemente para modelos antiguos.

### AX18 (Qt5 - Nov 2025)
**Ubicacion**: `New_Software nov 2025/AX18.../`

Software para modelo AX18 (15 teclas), **incompatible** con dispositivo de 3 botones + knob.

---

## Comparativa

| Software | Origen | Funciona | Protocolo | Utilidad |
|----------|--------|----------|-----------|----------|
| **MINI KeyBoard** | **Fabricante chino** | **Si** | **Extended** | **Principal: codigo descompilado usado para ingenieria inversa** |
| RSoft.MacroPad | Terceros | Si (con fix) | Extended | Referencia cruzada |
| MINI KeyBoard Tool V1 | Fabricante | Parcial | Desconocido | Obsoleto |
| MINI KeyBoard (Qt5) | Fabricante | Probablemente | Legacy | Obsoleto |
| AX18 (Qt5) | Fabricante | No | - | Modelo diferente |

---

## Conclusion del Analisis

**MINI KeyBoard (software oficial descompilado) es la fuente principal** porque:
1. Es el software del fabricante del dispositivo
2. Confirmo los action bytes correctos: **13/14/15 para knob**
3. Revelo la estructura exacta del paquete HID (65 bytes, buffer Data_Send_Buff)
4. Documento los 4 tipos de tecla (Basic, Media, Mouse, Multi)
5. Confirmo el comando WriteFlash (`0xAA 0xAA`)

**RSoft.MacroPad sirvio como validacion cruzada** para confirmar que el protocolo es estandar Extended y no algo propietario del fabricante.
