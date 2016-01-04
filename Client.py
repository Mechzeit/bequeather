import socket, json

bufferSize = 1024

class Client():

    actionMap = {"requestFile": lambda: "TBA..."}

    def __init__(self, ip, port, action, **args):
        function = self.actionMap.get(action, lambda: None)()

        if function is None:
            raise Exception("No action defined'")

        self.connectSocket(ip, port)
        
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

    def connectSocket(self, ip, port):
        self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketConnection.connect((ip, port))