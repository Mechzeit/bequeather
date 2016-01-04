import sys, socket, threading, socketserver, re, json

print(dir(socketserver.BaseRequestHandler))

bufferSize = 1024

class TCPRequestHandler(socketserver.BaseRequestHandler):

    def matchAction(self, message):
        self.patterns = {"request": re.compile("(request)(.*)")}
        for function, item in self.patterns.items():
            match = item.match(message)
            if match:
                print("MATCH...")

    def handle(self):
        self.matchAction('Hello!')
        data = self.request.recv(bufferSize)
        print("Type: %s (%s)" % (type(data), data))

        data = json.loads(str(data, 'ascii'))
        cur_thread = threading.current_thread()
        f = open(data['file'], 'rb')
        part = f.read(bufferSize)
        while(part):
            print("Sending %d bytes" % bufferSize)
            self.request.send(part)
            part = f.read(bufferSize)
        f.close()
        self.request.close()

class TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class Client():

    actionMap = {"requestFile": lambda: "TBA..."}

    def __init__(self, ip, port, action, **args):
        function = self.actionMap.get(action, lambda: None)()

        if function is None:
            raise Exception("No action defined'")

        self.connectSocket()
        try:
            self.socketConnection.sendall(bytes(json.dumps({**{"action": action}, **args}), 'ascii'))
            response = self.socketConnection.recv(bufferSize)
            f = open('proof-of-working.jpg', 'wb')
            while(response):
                print("Wrote %d bytes" % bufferSize)
                f.write(response)
                response = self.socketConnection.recv(bufferSize)
            f.close()
            print("Response complete.".format(response))
        finally:
            self.socketConnection.close()

    def connectSocket(self):
        self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketConnection.connect((ip, port))

if __name__ == "__main__":
    HOST, PORT = "localhost", 0

    server = TCPServer((HOST, PORT), TCPRequestHandler)
    ip, port = server.server_address

    serverThread = threading.Thread(target = server.serve_forever)
    serverThread.daemon = True
    serverThread.start()

    print("Server loop running in thread:", serverThread.name)

    Client(ip, port, "requestFile", file = "IMG_20141104_181531.jpg")

    server.shutdown()
    server.server_close()