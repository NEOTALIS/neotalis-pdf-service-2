from http.server import BaseHTTPRequestHandler
import json
import base64
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from neotalis_pdf import build_pdf

LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "neotalis_logo.jpeg")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))

            candidate_name = body.get("candidate_name", "Candidat")
            position       = body.get("position", "")
            date           = body.get("date", "")
            results        = body.get("results", [])

            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp_path = tmp.name

            build_pdf(tmp_path, LOGO_PATH, candidate_name, position, date, results)

            with open(tmp_path, "rb") as f:
                pdf_b64 = base64.b64encode(f.read()).decode()

            os.unlink(tmp_path)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"pdf": pdf_b64}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
