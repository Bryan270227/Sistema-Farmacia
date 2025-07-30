# run.py
import sys
import os
from app.app import app
# Agrega el directorio raíz al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    app.run(debug=True)