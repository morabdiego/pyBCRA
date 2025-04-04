#!/bin/bash

# Eliminar dist/, carpetas .egg-info y __pycache__
echo "Eliminando dist/, .egg-info y __pycache__..."
rm -rf dist/ *.egg-info
find . -type d -name "__pycache__" -exec rm -r {} +

# Desinstalar pybcradata de pip
echo "Desinstalando pybcradata..."
pip uninstall -y pybcradata

# Crear una nueva build
echo "Creando nueva build..."
python -m build

# Instalar el paquete desde el archivo .whl generado
echo "Instalando el paquete desde dist/*.whl..."
pip install dist/*.whl

echo "Proceso de build e instalación completado."
