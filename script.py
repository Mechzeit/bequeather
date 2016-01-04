import sys, socket, threading, socketserver, re, json
from server.TCP import TCP as TCPServer
from server.TCPRequestHandler import TCPRequestHandler
from Client import Client
print(dir(socketserver.BaseRequestHandler))

bufferSize = 1024

if __name__ == "__main__":
    HOST, PORT = "localhost", 0

    serverInstance = TCPServer((HOST, PORT), TCPRequestHandler)
    ip, port = serverInstance.server_address

    serverThread = threading.Thread(target = serverInstance.serve_forever)
    serverThread.daemon = True
    serverThread.start()

    print("Server loop running in thread:", serverThread.name)

    Client(ip, port, "requestFile", file = "IMG_20141104_181531.jpg")

    serverInstance.shutdown()
    serverInstance.server_close()