import socketserver

class TCP(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass