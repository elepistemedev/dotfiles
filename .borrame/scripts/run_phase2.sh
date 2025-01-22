#!/bin/bash

# Obtener la ruta absoluta de la carpeta raíz del proyecto
PROJECT_DIR=$(dirname "$(dirname "$(realpath "$0")")")

# Configurar PYTHONPATH como la raíz del proyecto
export PYTHONPATH="$PROJECT_DIR"

# Ejecutar el script main.py desde phase2
python "$PROJECT_DIR/phase2/main.py"
