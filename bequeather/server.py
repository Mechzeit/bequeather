import sys, signal, threading, os, importlib
from .protocol.TCP.server import TCP as TCPServer
from .protocol.TCP.handler import TCPRequestHandler
from .protocol.TCP.adapter import TCPAdapter
from bequeather.settings import get as getSettings

bufferSize = 1024

class Server():

	serverInstance = None
	serverThread = None

	def __init__(self):
		signal.signal(signal.SIGINT, self.signal_handler)

		HOST, PORT = "", 666

		Server.serverInstance = TCPAdapter()
		Server.serverInstance.listen()

		Routines.preloadAll()

		while Server.serverInstance.getThread().isAlive():
			pass

#        serverThread.wait()

		print("Goblins")

	def signal_handler(self, signal, frame):
		print("Shutting TCP Server down")
		Server.serverInstance.close()

		# Exit thread


		sys.exit(0)

class Routines():
	Imported = {}

	@staticmethod
	def getRoutine(routine, function):
		print(Routines.Imported)
		print("GET IN MY BELLY", routine, function)
		return getattr(Routines.Imported[routine], function)

	@staticmethod
	def preloadAll():
		modules = {}
		# Scan 'routines' defined director(y/ies)
		for routineModule in os.listdir(getSettings().get('routines').get('dir')):
			# Cherry pick .py files only for time being
			# Potentially support for routines to be created in other languages in the future.
			if routineModule.endswith('.py'):
				# Strip the file extension
				moduleName = routineModule[:-3]
				print("Loading routines from module %s" % (routineModule))
				# Dynamically import the module via the file location
				spec = importlib.util.spec_from_file_location("module.name", os.path.join(getSettings().get('routines').get('dir'), "{}.py".format(moduleName)))
				modules[moduleName] = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(modules[moduleName])
				# Iterate through all classes in module to see if any match the client 'routine'
				for className in modules[moduleName].classes:
					print(" - Mapping class %s" % (className))

					Routines.Imported[className] = getattr(modules[moduleName], className)(Server.serverInstance)
					#if className == routine:1
					#    return getattr(Routines.Imported[moduleName], routine)
		modules = None
		print(Routines.Imported)
		return False

if __name__ == "__main__":
	bequeatherServer = Server()