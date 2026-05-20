# Requisitos de la UI - Mini Controlador USB

## Fuente de Requisitos

Basado en el documento del usuario: `UI de suenos.md`

## Filosofia

> "Menos es mas"

La interfaz debe ser minimalista, moderna y enfocada en la funcionalidad esencial.

---

## Modos de Operacion

### Modo 1: Estado (Read-Only)

**Proposito**: Mostrar la configuracion actual del dispositivo sin permitir cambios.

**Funcionalidades**:
- Detectar y mostrar si el dispositivo esta conectado
- Mostrar visualmente los 3 botones y el knob
- Al seleccionar un control, mostrar que atajo tiene asignado:
  - Teclas configuradas
  - Modificadores (Ctrl, Shift, Alt, Win)
  - Delay (si aplica)
  - Tipo de atajo (basico, multimedia, mouse)
- **Limitacion importante**: El dispositivo **no permite leer** su configuracion actual. Este modo solo puede mostrar la configuracion que fue guardada previamente en la aplicacion.

### Modo 2: Configuracion (Read-Write)

**Proposito**: Permitir modificar y guardar atajos.

**Funcionalidades**:
- Seleccionar el control a configurar (boton o accion del knob)
- Definir el atajo de dos formas:
  1. **Manual**: Escribir el atajo en un campo de texto (ej: "CTRL + C")
  2. **Automatico**: Boton "Detectar" - el usuario presiona las teclas fisicamente y se capturan
- **Importante**: Debe considerar el layout de teclado e idioma del usuario
- Configurar el knob (3 funciones independientes):
  - Rotar izquierda
  - Presionar
  - Rotar derecha
- Guardar la configuracion
- Guardar presets/perfiles (en la PC, no en el dispositivo)

---

## Flujo de Configuracion

### Paso 1: Seleccionar Control
El usuario selecciona visualmente uno de los controles:
- Boton 1, Boton 2, Boton 3
- Knob izquierda, Knob presion, Knob derecha

### Paso 2: Definir Atajo
Opciones:
- **Entrada manual**: Campo de texto con formato amigable
- **Deteccion automatica**: Boton que captura las teclas fisicas presionadas

**Consideraciones**:
- Detectar el layout del teclado del usuario (español, ingles, etc.)
- Mostrar advertencia si el layout afecta el resultado
- Permitir combinaciones de hasta 5 teclas (limite del dispositivo)

### Paso 3: Configuracion del Knob
El knob tiene 3 funciones separadas que se configuran independientemente:
- Rotar izquierda (Knob1Left)
- Presionar (Knob1Push)
- Rotar derecha (Knob1Right)

### Paso 4: LEDs
- El dispositivo tiene LEDs pero con limitaciones:
  - No soporta color personalizado
  - 3 modos de iluminacion disponibles
- Opciones sugeridas:
  - Encender al presionar
  - Quedar encendido
  - Apagado
  - (Nota: Limitado por el hardware)

### Paso 5: Guardar
- Enviar configuracion al dispositivo via HID
- Guardar preset/perfil en archivo local (JSON o similar)
- Confirmar escritura exitosa

---

## Elementos Visuales Deseados

### Representacion del Dispositivo
- Visualizacion esquematica del controlador
- 3 botones representados como botones clickeables
- 1 knob representado como circulo o dial
- Estado visual (conectado/desconectado)

### Panel de Configuracion
- **Control seleccionado**: Nombre y tipo
- **Tipo de atajo**: Basic, Multimedia, Mouse, LED
- **Entrada de atajo**: Campo de texto + boton detectar
- **Preview**: Mostrar que se enviara al dispositivo
- **Teclas especiales**: Botones rapidos para Ctrl, Shift, Alt, Win

### Barra de Estado
- Estado de conexion del dispositivo
- Ultima accion realizada
- Indicador de cambios sin guardar

---

## Consideraciones Tecnicas

### Limitaciones del Dispositivo
- **Sin lectura**: No se puede leer la configuracion actual del dispositivo
- **Sin layers**: Solo 1 capa de configuracion
- **Max 5 teclas**: Secuencias cortas unicamente
- **Sin delay**: No hay configuracion de delay
- **LEDs limitados**: Solo modos, no colores

### Persistencia Local
Como el dispositivo no permite leer su configuracion, la app debe:
- Guardar presets en archivos locales (JSON)
- Cargar el ultimo preset usado al iniciar
- Mostrar claramente que lo que se ve es el preset local, no la config del dispositivo

### Deteccion de Teclas
- Usar hook de teclado global en Windows
- Capturar Virtual Keys (VK_)
- Mapear a HID Usage Page Keyboard codes
- Considerar el layout de teclado del sistema

---

## Mockup Conceptual

```
+-----------------------------------------------------------+
|  Mini Configurator                              [Conectado]|
+-----------------------------------------------------------+
|                                                           |
|   [Boton 1]   [Boton 2]   [Boton 3]                     |
|                                                           |
|                    [  KNOB  ]                             |
|                     (O)                                   |
|                                                           |
+-----------------------------------------------------------+
|  Control seleccionado: Boton 1                            |
|                                                           |
|  Atajo actual: Ctrl + C                                   |
|                                                           |
|  [Detectar teclas]  o  escribir manualmente: [______]   |
|                                                           |
|  Teclas especiales: [Ctrl] [Shift] [Alt] [Win]           |
|                                                           |
|  [Guardar en dispositivo]  [Guardar preset]  [Cargar]     |
+-----------------------------------------------------------+
```
