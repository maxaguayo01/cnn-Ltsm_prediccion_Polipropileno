import json
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "localhost"
PORT = 8765

PP_DATA = []   # Aquí se guarda lo que lo mande Tampermonkey

class Handler(BaseHTTPRequestHandler):
    
    def _set_headers(self, code=200, content="application/json"):
        self.send_response(code)
        self.send_header("Content-type", content)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        if self.path == "/pp":
            self._set_headers()
            self.wfile.write(json.dumps(PP_DATA).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(b"Not found")

    def do_POST(self):
        global PP_DATA
        
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len)
        
        try:
            PP_DATA = json.loads(body)
            print(">> Datos PP actualizados correctamente ({:,} registros)".format(len(PP_DATA)))
            self._set_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            self._set_headers(400)
            self.wfile.write(str(e).encode("utf-8"))

server = HTTPServer((HOST, PORT), Handler)
print(f">> Servidor corriendo en http://{HOST}:{PORT}/pp")
server.serve_forever()
