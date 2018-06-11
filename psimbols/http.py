
import http.server

class Handler(http.server.BaseHTTPRequestHandler):

    server_version = '1.0'
    sys_version = ''
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')  
        self.end_headers()
        self.wfile.write(b'Hello\n')
        
    def do_POST(self):
        self.send_error(401)    # unauthorised

