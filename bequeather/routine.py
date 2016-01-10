
class UserRoutine:
	connection = None

	def __init__(self, connection):
		self.connection = connection

	def getConnection(self):
		return self.connection