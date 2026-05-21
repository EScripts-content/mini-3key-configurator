# SHORTCUT Text Parsing — Lógica Completa

## Descripción General

El campo **SHORTCUT** en el panel MANUAL MODE permite al usuario escribir combinaciones de teclas de forma natural usando texto. El sistema parsea en tiempo real (por cada tecla presionada) y actualiza los chips visuales inmediatamente.

---

## Arquitectura

```
[Entry Widget] → <KeyRelease> → _on_man_key_release()
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
               Backspace/Del    Abrev. 2 letras   Texto normal
                    │               │               │
               tokenize()      replace word +     tokenize()
                    │           tokenize()           │
                    │               │               │
               chips ←──── app._on_shortcut_text_parsed(seq)
```

---

## 1. Evento Principal: `_on_man_key_release`

```python
def _on_man_key_release(self, event):
```

### Ignora teclas de navegación:
- Left, Right, Up, Down, Home, End
- Shift_L/R, Control_L/R, Alt_L/R, Win_L/R
- Caps_Lock

### Guard contra recursión:
```python
prev = getattr(self, '_man_prev_text', '')
if text == prev:
    return           # ← tkinter lanza KeyRelease extra tras insert()
self._man_prev_text = text   # ← se actualiza ANTES de cualquier parsing
```

### 3 caminos posibles:

---

## 2. Camino A — Backspace / Delete

```python
if event.keysym in ('BackSpace', 'Delete'):
    seq = self._tokenize_shortcut_text(text)
    self.app._on_shortcut_text_parsed(seq)
    return
```

Simplemente tokeniza el texto restante y actualiza chips. No intenta autocompletar.

---

## 3. Camino B — Autocompletar abreviatura de 2 letras

```python
# REGEX de modificadores reconocidos:
# "ct" → Ctrl, "sh" → Shift, "al" → Alt, "wi" → Win, "ag" → AltGr

if last_word and last_word.lower() in self.MOD_AC_MAP:
    expanded = self.MOD_AC_MAP[last_word.lower()]
    if last_word != expanded:
        last_idx = text.rfind(last_word)
        widget.delete(0, tk.END)
        widget.insert(0, new_text)
        widget.icursor(last_idx + len(expanded))
        self._man_prev_text = widget.get()   # ← evita recursión
```

### Estrategia cursor-safe:
1. Encuentra la última palabra en el texto original
2. Reemplaza SOLO esa palabra (no todo el entry)
3. Coloca el cursor exactamente después de la palabra expandida
4. Actualiza `_man_prev_text` inmediatamente para que el KeyRelease recursivo que lanza tkinter sea ignorado

### Después del autocomplete, se parsea inmediatamente:
```python
seq = self._tokenize_shortcut_text(new_text)
self.app._on_shortcut_text_parsed(seq)
```

---

## 4. Camino C — Texto normal (sin autocompletar)

```python
seq = self._tokenize_shortcut_text(text)
self.app._on_shortcut_text_parsed(seq)
```

Simplemente tokeniza y actualiza chips.

---

## 5. Tokenización: `_tokenize_shortcut_text`

Reglas en orden de prioridad:

```
Para cada token (separado por espacio):

1. ¿Es nombre completo de modificador? ("Ctrl", "Shift", "Alt", "Win", "AltGr")
   → [(mod_byte, 0)]

2. ¿Es abreviatura de 2 letras? ("ct", "sh", "al", "wi", "ag")
   → [(mod_byte, 0)]

3. ¿Es nombre completo de tecla conocido? ("Enter", "F1", "Space", "Backspace", "ArrowUp", etc.)
   → [(0, hid_code)]

4. ¿Los primeros 2 caracteres son abreviatura de modificador? ("ct+", "sh a")
   → [mod] + [resto como teclas individuales]

5. Cada carácter es una tecla individual
   → [(0, hid_code)] para cada char
```

### Función `_find_key_entry_for_full_name`

Busca el token completo en:
1. `config.KEYCODES` — maneja "Enter", "Space", "F1".."F12", "Esc", "Tab", etc.
2. `KEY_GROUPS` — busca en Letters, Symbols, Nav, Numpad, F-keys
3. `config.KEYCODES` case-insensitive

### Función `_find_key_entry_for_token`

Para caracteres individuales (solo se llama después de fallar la búsqueda de nombre completo):
1. `config.KEYCODES` con uppercase — maneja letras, números
2. `KEY_GROUPS` — busca símbolos ("+", "-", "=", etc.) con soporte de Shift implícito
3. Fallback: `(0, 0)` para caracteres desconocidos

---

## 6. Símbolos con Shift implícito

```python
SYMBOLS_NEED_SHIFT = {"_", "+", "{", "}", "|", ":", '"', "~", "<", ">", "?"}
```

Si el token es un símbolo que requiere Shift (ej: "+" viene de "=" con Shift), el parser automáticamente:
```python
mod = config.Modifier.SHIFT if lbl in self.SYMBOLS_NEED_SHIFT else 0
```

---

## 7. Datos Clave

| Mapa | Propósito |
|------|-----------|
| `MOD_AC_MAP` | `{"ct": "Ctrl", "sh": "Shift", "al": "Alt", "wi": "Win", "ag": "AltGr"}` |
| `MOD_BYTES` | `{"Ctrl": 1, "Shift": 2, "Alt": 4, "Win": 8, "AltGr": 64}` |
| `KEY_GROUPS` | Letters, Symbols, F-keys, Nav, Numpad, Multimedia |
| `SYMBOLS_NEED_SHIFT` | Símbolos que requieren Shift implícito |

---

## 8. Pruebas

Existen dos test suites:

- **`test_parse.py`** — Tests de lógica pura (no requiere tkinter):
  ```bash
  python mini_configurator/test_parse.py
  ```
  28 tests: empty, single letter, uppercase, abbreviation, full name, space-separated, multi-mod, symbols, merged tokens, function keys, named keys, overflow, etc.

- **`test_interactive.py`** — Test con UI real (requiere tkinter):
  ```bash
  python mini_configurator/test_interactive.py
  ```
  Muestra entry + chips + debug panel. ESC para cerrar.

---

## 9. Bugs Encontrados y Corregidos

| Bug | Síntoma | Fix |
|-----|---------|-----|
| Cursor salta al inicio | Al escribir "ct" el cursor iba al principio | Usar `delete+insert` específico, no `StringVar.set('')` |
| Recursión infinita | KeyRelease se dispara tras `insert()` | Actualizar `_man_prev_text` después de `insert()` |
| "Enter" se fragmenta | `[E][N][T][E][R]` en lugar de `[Enter]` | `_find_key_entry_for_full_name()` ANTES de dividir en chars |
| "F1" se fragmenta | `[F][1]` en lugar de `[F1]` | mismo fix |
| Backspace no actualiza chips | Chips quedan con el valor anterior | Parsear también en Backspace/Delete |
| Autocomplete no actualiza chips | Chips no reflejan el cambio hasta la siguiente tecla | Parsear después del autocomplete |