"""
Diagnostico interactivo de LEDs.
Envia comandos uno por uno y espera tu confirmacion.
Todo se guarda en un log automaticamente.

Flujo:
  1. Muestra Prueba X (descripcion de lo que deberia hacer)
  2. Envia el comando al dispositivo
  3. Pregunta: SI / NO / describe / R (repetir)
  4. SI/NO: guarda en log y pasa a la siguiente prueba
  5. describe: guarda descripcion + pregunta para continuar
  6. R: repite la prueba actual
"""
import sys
import os
from datetime import datetime
sys.path.insert(0, r"h:\PROGRAMAS\PROGRAMAS PAGADOS\MINI CONTROLADORA USB\drive-download-20230810T081045Z-001\mini_configurator")
from hid_device import HidDevice
import time

LOG_FILE = r"h:\PROGRAMAS\PROGRAMAS PAGADOS\MINI CONTROLADORA USB\drive-download-20230810T081045Z-001\TESTS\led_test_log.txt"

# ============================================
# LOG
# ============================================
log_entries = []

def log_write(entry):
    log_entries.append(entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

# Header del log
log_write("=" * 70)
log_write(f"LOG INICIADO: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log_write("=" * 70)

# ============================================
# DISPOSITIVO
# ============================================
print("=" * 70)
print(" DIAGNOSTICO INTERACTIVO DE LEDs")
print("=" * 70)
print("Instrucciones:")
print("  - SI    : el LED reacciono como se describe")
print("  - NO    : no paso nada")
print("  - describe : escribe lo que viste")
print("  - R     : repetir esta prueba")
print("=" * 70)

dev = HidDevice()
dev.open()
print("[OK] Dispositivo conectado\n")

def send_raw(payload):
    while len(payload) < 64:
        payload.append(0)
    dev.write_report(payload[:64])

# ============================================
# FLUJO INTERACTIVO
# ============================================
results = []

def ask_user(name, expected):
    """Pide respuesta interactiva. Retorna (resp_code, resp_text)"""
    while True:
        print(f"\n  >> ¿Reacciono como se describe?")
        print(f"     [S] SI  |  [N] NO  |  [D] Describe  |  [R] Repetir")
        ans = input("  >> Respuesta: ").strip().lower()

        if ans in ("s", "si", "y", "yes"):
            return "si", "SI"
        elif ans in ("n", "no"):
            return "no", "NO"
        elif ans in ("d", "describe", "desc"):
            desc = input("  >> Describe lo que viste: ").strip()
            cont = input("  >> ¿Continuar a la siguiente prueba? [S/N]: ").strip().lower()
            if cont in ("s", "si", "y", "yes"):
                return "describe", desc
            else:
                print("  >> Repitiendo descripcion...")
                return "describe_repeat", desc
        elif ans in ("r", "repeat", "repetir"):
            return "repeat", "REPETIR"
        else:
            print("  [!] Opcion no valida. Intenta de nuevo.")


def run_test(name, visual_desc, commands, wait=3):
    """Ejecuta una prueba con flujo interactivo completo"""
    print("\n" + "=" * 70)
    print(f" {name}")
    print("=" * 70)
    print(f"\n  Observa tu controlador USB y dime:")
    print(f"  -> {visual_desc}")

    log_write(f"\n--- PRUEBA: {name} ---")
    log_write(f"Visual: {visual_desc}")

    while True:
        # Enviar comandos (silencioso en consola, logueado en archivo)
        print("\n  [Enviando comando...]")
        for cmd_name, payload in commands:
            send_raw(payload)
            log_write(f"CMD: {cmd_name} -> {payload[:8]}")
            time.sleep(0.5)

        print(f"\n  [Espera {wait}s... observa ahora]")
        time.sleep(wait)

        # Preguntar al usuario
        code, text = ask_user(name, visual_desc)

        if code == "repeat":
            print("  >> Repitiendo prueba...")
            log_write("ACCION: Repetir prueba")
            continue

        # Guardar resultado
        results.append((name, code, text))
        log_write(f"RESULTADO: {code.upper()} -> {text}")
        print(f"  [Guardado] {code.upper()}: {text}")
        break


# ============================================
# PRUEBAS DEFINIDAS
# ============================================
# Cada tupla: (nombre_corto, payload, descripcion_visual)
PRUEBAS = [
    ("Prueba 1: Apagar LEDs", [0xB0, 0x08, 0x00], "Los LEDs del controlador deberian APAGARSE (quedar oscuros)"),
    ("Prueba 2: Modo respirar", [0xB0, 0x08, 0x01], "Los LEDs deberian PRENDERSE y APAGARSE suavemente (efecto respirar)"),
    ("Prueba 3: Modo carrusel", [0xB0, 0x08, 0x02], "Los LEDs deberian moverse de un boton a otro (efecto carrusel/onda)"),
    ("Prueba 4: Color ROJO fijo", [0xB0, 0x08, 0x10], "Todos los LEDs deberian quedar ROJO encendido fijo (sin parpadear)"),
    ("Prueba 5: Color VERDE fijo", [0xB0, 0x08, 0x40], "Todos los LEDs deberian quedar VERDE encendido fijo"),
    ("Prueba 6: Color AZUL fijo", [0xB0, 0x08, 0x60], "Todos los LEDs deberian quedar AZUL encendido fijo"),
    ("Prueba 7: Color MORADO fijo", [0xB0, 0x08, 0x70], "Todos los LEDs deberian quedar MORADO/PURPURA encendido fijo"),
    ("Prueba 8: Color CYAN fijo", [0xB0, 0x08, 0x50], "Todos los LEDs deberian quedar CYAN (azul claro) encendido fijo"),
    ("Prueba 9: Color NARANJA fijo", [0xB0, 0x08, 0x20], "Todos los LEDs deberian quedar NARANJA encendido fijo"),
    ("Prueba 10: Color AMARILLO fijo", [0xB0, 0x08, 0x30], "Todos los LEDs deberian quedar AMARILLO encendido fijo"),
    ("Prueba 11: Respirar en ROJO", [0xB0, 0x08, 0x11], "Los LEDs deberian respirar (prender/apagar suave) pero en color ROJO"),
    ("Prueba 12: Carrusel en VERDE", [0xB0, 0x08, 0x42], "Los LEDs deberian moverse de boton en boton pero en color VERDE"),
    ("Prueba 13: Apagar de nuevo", [0xB0, 0x08, 0x00], "Los LEDs deberian APAGARSE definitivamente"),
]

# Ejecutar cada prueba: LedFunction + WriteFlash
for nombre, payload, visual in PRUEBAS:
    run_test(nombre, visual, [("LedFunction", payload), ("WriteFlash", [0xAA, 0xA1])], wait=3)

dev.close()

# ============================================
# RESUMEN FINAL
# ============================================
print("\n" + "=" * 70)
print(" RESUMEN DE RESULTADOS")
print("=" * 70)

for name, code, text in results:
    icon = "[OK]" if code == "si" else "[NO]" if code == "no" else "[DESC]"
    print(f"  {icon} {name}: {text}")

print("=" * 70)
print(f" Log guardado en: {LOG_FILE}")
print("=" * 70)

# Guardar resumen en log
log_write("\n" + "=" * 70)
log_write("RESUMEN:")
for name, code, text in results:
    log_write(f"  {code.upper()}: {name} -> {text}")
log_write("=" * 70)

