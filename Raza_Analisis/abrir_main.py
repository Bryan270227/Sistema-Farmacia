import http.server
import socketserver
import webbrowser
import threading
import os

PORT = 5500

# Ruta base del proyecto (donde está este archivo .py)
raiz = os.path.dirname(os.path.abspath(__file__))
os.chdir(raiz)

# Servidor HTTP simple
def servidor():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"✅ Servidor corriendo en http://localhost:{PORT}/frontend/main.html")
        httpd.serve_forever()

# Abrir automáticamente el main.html dentro de /frontend
threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{PORT}/frontend/main.html")).start()

# Ejecutar servidor
servidor()
