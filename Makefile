.PHONY: clean uninstall build install test smoke all

PACKAGE_NAME=pybcradata
SMOKE_OUTPUT=test/smoke_test_output.txt

clean:
	echo "🧹 Limpiando dist/, egg-info, __pycache__, pytest_cache y smoke output..."
	rm -rf dist/ *.egg-info src/pyBCRAdata.egg-info $(SMOKE_OUTPUT) .pytest_cache
	find . -type d -name "__pycache__" -exec rm -r {} + || true

uninstall:
	echo "❌ Desinstalando paquete si está instalado..."
	pip uninstall -y $(PACKAGE_NAME) || true

build: clean
	echo "📦 Construyendo paquete..."
	python -m build

install: uninstall build
	echo "📥 Instalando paquete desde dist/*.whl..."
	pip install dist/*.whl

test:
	echo "🧪 Corriendo tests con pytest..."
	pytest test/test_methods.py

smoke:
	echo "🚬 Corriendo smoke test (test/smoketest.py) y guardando salida..."
	python test/smoketest.py > $(SMOKE_OUTPUT) 2>&1
	echo "✅ Salida guardada en $(SMOKE_OUTPUT)"

all: install test smoke
	echo "🏁 Proceso completo (build, install, test, smoke) terminado."
