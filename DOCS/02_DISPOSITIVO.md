# Especificaciones del Dispositivo

## Informacion General

| Campo | Valor |
|-------|-------|
| Nombre | Mini USB Controller (3 botones + 1 knob) |
| Vendor ID | `0x1189` (4489) |
| Product ID | `0x8890` (34960) |
| Revision | 0x0000 |
| Fabricante | Desconocido (genrico chino) |
| Driver | input.inf (Microsoft HID estandar) |
| Class GUID | {745a17a0-74d3-11d0-b6fe-00a0c90f57da} |

## Hardware IDs Detectados

```
HID\VID_1189&PID_8890&REV_0000&MI_02&Col01
HID\VID_1189&PID_8890&MI_02&Col01
HID\VID_1189&UP:0001_U:0006
HID_DEVICE_SYSTEM_KEYBOARD
HID_DEVICE_UP:0001_U:0006
HID_DEVICE
```

## Interfaces

El dispositivo presenta 2 interfaces HID:

### Interface mi_01 - Canal de Configuracion
- **UsagePage**: 0xFF00 (Vendor-defined)
- **Usage**: 0x0001
- **InputReportByteLength**: 65 bytes
- **OutputReportByteLength**: 65 bytes
- **FeatureReportByteLength**: 0
- **Funcion**: Recibe comandos de configuracion para asignar atajos

### Interface mi_02 - Consumer Control
- **UsagePage**: 0x000C (Consumer)
- **Usage**: 0x0001
- **InputReportByteLength**: 3 bytes
- **Funcion**: Emite teclas multimedia (volumen, play/pause, etc.)

## Controles Fisicos

| Control | Tipo | ID en Protocolo |
|---------|------|-----------------|
| Boton 1 | Push | Key1 (1) |
| Boton 2 | Push | Key2 (2) |
| Boton 3 | Push | Key3 (3) |
| Knob | Rotar izquierda | Knob1Left (13) |
| Knob | Presionar | Knob1Push (14) |
| Knob | Rotar derecha | Knob1Right (15) |

## Capacidades segun layouts.txt

```
Layout: 3 buttons 1 knob
    4489:34960
    1:5:0:0:3
    B1,5,5
    B2,25,5
    B3,45,5
    K1,70,5
```

Interpretacion de `1:5:0:0:3`:
- **1 layer**: Solo 1 capa de configuracion
- **5 caracteres maximo**: Cada atajo puede tener hasta 5 teclas en secuencia
- **0 delay**: No soporta configuracion de delay
- **0 LED color**: No soporta configuracion de color RGB
- **3 LED modes**: 3 modos de iluminacion disponibles

## LEDs

El dispositivo tiene LEDs pero:
- No soporta color personalizado
- No hay configuracion de color RGB
- Hay 3 modos de iluminacion posibles

## Limitaciones

1. **Sin memoria de perfiles**: No hay multiples perfiles/presets en el dispositivo
2. **Sin layers multiples**: Solo 1 layer de configuracion
3. **Sin delay**: No se puede agregar delay entre pulsaciones
4. **Secuencia corta**: Maximo 5 teclas por atajo
5. **Sin retroalimentacion de estado**: El dispositivo no responde con la configuracion actual almacenada
6. **No se puede leer config**: Solo se puede escribir, no leer lo que tiene guardado

## Requisitos del Sistema

- Windows 10 o 11 (64-bit)
- Driver HID estandar de Microsoft (input.inf)
- No requiere driver adicional
- Se comunica via HID reports de 65 bytes
