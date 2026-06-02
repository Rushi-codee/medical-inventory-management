import http.server
import socketserver
import json
import urllib.parse
import subprocess
import os
import csv
import webbrowser
import threading
import sys

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'web')
EXE_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'MedicalInventory.exe'))
CSV_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'data', 'inventory.csv'))

class APIHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Decode and clean path to get real filesystem resource
        path_without_query = urllib.parse.urlparse(path).path
        decoded_path = urllib.parse.unquote(path_without_query)
        
        if decoded_path == '/':
            return os.path.join(WEB_DIR, 'index.html')
        
        # Check if path starts with api namespace
        if decoded_path.startswith('/api/'):
            return decoded_path
            
        # Strip leading slash to serve static files from WEB_DIR
        relative_path = decoded_path.lstrip('/')
        return os.path.join(WEB_DIR, relative_path)

    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        url_path = url_parsed.path
        decoded_path = urllib.parse.unquote(url_path)
        query_params = urllib.parse.parse_qs(url_parsed.query)
        
        if decoded_path == '/api/inventory':
            self.handle_get_inventory()
        elif decoded_path == '/api/reports':
            self.handle_list_reports(query_params)
        elif decoded_path == '/api/reports/view':
            self.handle_view_report(query_params)
        else:
            # Fall back to standard static files serving from WEB_DIR
            super().do_GET()

    def do_POST(self):
        url_path = urllib.parse.urlparse(self.path).path
        decoded_path = urllib.parse.unquote(url_path)
        
        # Read incoming payload
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            payload = json.loads(post_data) if post_data else {}
        except Exception:
            payload = {}

        if decoded_path == '/api/authenticate':
            self.handle_authenticate(payload)
        elif decoded_path == '/api/execute':
            self.handle_execute(payload)
        elif decoded_path == '/api/reports/delete':
            self.handle_delete_report(payload)
        else:
            self.send_error(404, "Endpoint not found")

    def handle_get_inventory(self):
        try:
            inventory = []
            if os.path.exists(CSV_PATH):
                with open(CSV_PATH, 'r', encoding='utf-8', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Extract data and clean numeric values
                        qty = row.get('qty', '0')
                        price = row.get('price', '0.0')
                        threshold = row.get('threshold', '0')
                        
                        inventory.append({
                            'name': row.get('name', ''),
                            'batch': row.get('batch', ''),
                            'expiry': row.get('expiry', ''),
                            'qty': int(qty) if qty.isdigit() else 0,
                            'price': float(price) if price.replace('.', '', 1).isdigit() else 0.0,
                            'threshold': int(threshold) if threshold.isdigit() else 0
                        })
            self.send_json_response(200, inventory)
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})

    def handle_authenticate(self, payload):
        username = payload.get('username', '')
        password = payload.get('password', '')
        
        try:
            result = subprocess.run([EXE_PATH, "authenticate", username, password],
                                   capture_output=True, text=True, cwd=os.path.dirname(EXE_PATH))
            if result.returncode == 0 and "Authentication successful" in result.stdout:
                self.send_json_response(200, {"success": True, "message": "Authentication successful"})
            else:
                self.send_json_response(200, {"success": False, "message": "Invalid username or password"})
        except Exception as e:
            self.send_json_response(500, {"success": False, "error": str(e)})

    def handle_execute(self, payload):
        args = payload.get('args', [])
        # Ensure all args are strings
        args = [str(a) for a in args]
        try:
            # Execute command on MedicalInventory.exe
            result = subprocess.run([EXE_PATH] + args, capture_output=True, text=True, cwd=os.path.dirname(EXE_PATH))
            self.send_json_response(200, {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            })
        except Exception as e:
            self.send_json_response(500, {
                "success": False,
                "error": str(e)
            })

    def handle_list_reports(self, query_params):
        report_type = query_params.get('type', [''])[0]
        reports_dir = os.path.abspath(os.path.join(BASE_DIR, '..', 'reports'))
        
        try:
            reports = []
            if os.path.exists(reports_dir) and os.path.isdir(reports_dir):
                files = os.listdir(reports_dir)
                for f in files:
                    # Match expired report filename prefix
                    if report_type == 'expired' and f.startswith('expired report_') and f.endswith('.txt'):
                        ts = self.parse_timestamp_from_filename(f, 'expired report_')
                        reports.append({"filename": f, "timestamp": ts})
                    # Match low stock report filename prefix
                    elif report_type == 'lowstock' and f.startswith('lowstockreport_') and f.endswith('.txt'):
                        ts = self.parse_timestamp_from_filename(f, 'lowstockreport_')
                        reports.append({"filename": f, "timestamp": ts})
                
                # Sort descending by filename so most recent is at the top
                reports.sort(key=lambda x: x['filename'], reverse=True)
                
            self.send_json_response(200, reports)
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})

    def parse_timestamp_from_filename(self, filename, prefix):
        # filename is e.g. "expired report_2025-11-18_15-08-48.txt"
        try:
            parts = filename.replace(prefix, '').replace('.txt', '').split('_')
            date_part = parts[0]
            time_part = parts[1].replace('-', ':')
            return f"{date_part} {time_part}"
        except Exception:
            return filename

    def handle_view_report(self, query_params):
        filename = query_params.get('file', [''])[0]
        # Safety validation to prevent directory traversal
        if not filename or '/' in filename or '\\' in filename or '..' in filename:
            self.send_json_response(400, {"error": "Invalid filename"})
            return
            
        reports_dir = os.path.abspath(os.path.join(BASE_DIR, '..', 'reports'))
        filepath = os.path.join(reports_dir, filename)
        
        try:
            if os.path.exists(filepath) and os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.send_json_response(200, {"content": content})
            else:
                self.send_json_response(404, {"error": "Report file not found"})
        except Exception as e:
            self.send_json_response(500, {"error": str(e)})

    def handle_delete_report(self, payload):
        filename = payload.get('file', '')
        # Safety validation to prevent directory traversal
        if not filename or '/' in filename or '\\' in filename or '..' in filename:
            self.send_json_response(400, {"success": False, "error": "Invalid filename"})
            return
            
        reports_dir = os.path.abspath(os.path.join(BASE_DIR, '..', 'reports'))
        filepath = os.path.join(reports_dir, filename)
        
        try:
            if os.path.exists(filepath) and os.path.isfile(filepath):
                os.remove(filepath)
                self.send_json_response(200, {"success": True, "message": "Report deleted successfully"})
            else:
                self.send_json_response(404, {"success": False, "error": "Report file not found"})
        except Exception as e:
            self.send_json_response(500, {"success": False, "error": str(e)})

    def send_json_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        # Setup basic CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        # Preflight checks handler
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def start_server():
    # Setup standard socket reuse
    socketserver.TCPServer.allow_reuse_address = True
    handler = APIHandler
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"Medical Inventory Portal: http://localhost:{PORT}")
            print("Press Ctrl+C to stop the local server.")
            
            # Delay browser launch slightly to ensure port is listening
            threading.Timer(0.8, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
            
            httpd.serve_forever()
    except Exception as e:
        print(f"Server execution error: {e}", file=sys.stderr)

if __name__ == "__main__":
    start_server()
