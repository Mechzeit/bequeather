import socketserver, re, json, threading

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