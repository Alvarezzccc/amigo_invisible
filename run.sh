#!/bin/bash

echo "🔧 Creando entorno virtual..."

# Crear entorno si no existe
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

echo "🔧 Activando entorno virtual..."
source venv/bin/activate

echo "⬇️ Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🚀 Ejecutando servidor..."
python3 app.py