import sys, signal, threading
from .protocol.TCP.server import TCP as TCPServer
from .protocol.TCP.handler import TCPRequestHandler

bufferSize = 1024

def signal_handler(signal, frame):
	print("Shutting TCP Server down")
	serverInstance.shutdown()
	serverInstance.server_close()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class Server():
    def __init__(self):
        HOST, PORT = "", 666

        TCPServer.allow_reuse_address = True 
        serverInstance = TCPServer((HOST, PORT), TCPRequestHandler)
        ip, port = serverInstance.server_address

        serverThread = threading.Thread(target = serverInstance.serve_forever)
        serverThread.daemon = True
        serverThread.start()

        print("Server loop running in thread: %s", serverThread.name)
        print("IP: %s" % ip)
        print("Port: %s" % port)

        while True:
            pass

if __name__ == "__main__":
    bequeatherServer = Server()