#!/bin/bash

# Eliminar dist/ y las carpetas .egg-info
echo "Eliminando dist/ y .egg-info..."
rm -rf dist/ *.egg-info

# Crear una nueva build
echo "Creando nueva build..."
python -m build

# Desinstalar pybcradata de pip
echo "Desinstalando pybcradata..."
pip uninstall -y pybcradata

# Instalar el paquete desde el archivo .whl generado
echo "Instalando el paquete desde dist/*.whl..."
pip install dist/*.whl

echo "Proceso de build e instalación completado."
