
import http.server
import json

import psimbols.err
import psimbols.message

MIN_LENGTH = 32
MAX_LENGTH = 1024

processor = psimbols.message.Processor()

class Handler(http.server.BaseHTTPRequestHandler):

    server_version = 'Psimbols/1.0'
    sys_version = ''
            
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')  
        self.end_headers()
        self.wfile.write(b'Hello\n')
        
    def do_POST(self):
        content_length = self.headers['Content-Length']
        length = int(content_length) if content_length else 0
        
        if length < MIN_LENGTH:
            self.send_error(400, "Content-Length is too small")
            return

        if length > MAX_LENGTH:
            self.send_error(400, "Content-Length is too big")
            return
            
        posted_bytes = self.rfile.read(length)
        
        if len(posted_bytes) != length:
            self.send_error(400, "Data is shorter than Content-Length")
            return
        
        posted_string = posted_bytes.decode('utf-8')
        try:
            message = json.loads(posted_string)
            
        except json.JSONDecodeError:
            self.send_error(400, "Data is not in JSON format")
            return

        try:
            response = processor.process(message)
                 
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')  
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except psimbols.err.BadMessageFormat:
            self.send_error(400, "Message format is not correct")

        except psimbols.err.ClientUnauthorised:
            self.send_error(401, "Client is not authorised")

        except:
            self.send_error(500, "Uncaught exception")

