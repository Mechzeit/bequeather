import threading
from .server import TCP as TCPServer
from .handler import TCPRequestHandler

class TCPAdapter:
	serverThread = None

	def getThread(self):
		return self.serverThread

	# Open socket
	def listen(self):
		HOST, PORT = "", 666

		serverProtocol = TCPServer
		serverProtocol.allow_reuse_address = True 
		self.serverInstance = serverProtocol((HOST, PORT), TCPRequestHandler)

		self.serverThread = threading.Thread(target = self.serverInstance.serve_forever)
		self.serverThread.daemon = True
		self.serverThread.start()

		ip, port = self.serverInstance.server_address

		print("Server loop running in thread: %s" % (self.serverThread))
		print("IP: %s" % ip)
		print("Port: %s" % port)
		pass

	# Close socket
	def close(self):
		self.serverInstance.shutdown()
		self.serverInstance.server_close()

	# Send data
	def send(self, bytes: bytes):
		pass

	# Receive data
	def receive(self):
		pass