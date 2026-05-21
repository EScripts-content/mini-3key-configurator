# -*- coding: utf-8 -*-
"""
Mini Configurator - Punto de entrada sin consola (.pyw)
Importa y ejecuta main.py como windowed app.
"""

import runpy
import sys
import os

# Ensure the package directory is on the path so main.py can import its siblings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

runpy.run_module("main", run_name="__main__")
