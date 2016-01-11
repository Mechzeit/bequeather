import inspect

class BaseAction():
	command = None
	args = None
	responseData = None

	def setArguments(self, **kwargs):
		self.args = kwargs

	def getArgument(self, key = None):
		if key:
			return self.args.get(key)
		else:
			return self.args

	def __init__(self, connection):
		self.connection = connection

	def getConnection(self):
		return self.connection

	def setResponse(self, **kwargs):
		self.responseData = kwargs
		return self

	def getResponse(self):
		return self.responseData

	def getMethodName(self):
		return lambda: inspect.stack()[1][3]
