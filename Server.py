#!/usr/bin/env python
import sys, signal, threading
from server.TCP import TCP as TCPServer
from server.TCPRequestHandler import TCPRequestHandler

bufferSize = 1024

def signal_handler(signal, frame):
	print("Shutting TCP Server down")
	serverInstance.shutdown()
	serverInstance.server_close()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    HOST, PORT = "localhost", 0

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