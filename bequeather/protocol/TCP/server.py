import socketserver

class TCP(socketserver.ThreadingMixIn, socketserver.TCPServer):

	def get_request(self):
		return super(TCP, self).get_request()
