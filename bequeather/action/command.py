from .base import BaseAction
import os, subprocess, logging, json

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

class ShellCommand(BaseAction):

	def execute(self):
		"""Executes a remote shell command

		"""
		logger.debug("Executing shell command {}".format(self.command))
		command = self.getArgument('command')
		kwargs = self.getArgument('args')
		if kwargs is None:
			kwargs = []

		# TODO: Abstract the sending method - for handling with other protocols in the future
		self.getConnection().send(bytes(json.dumps({"routine": self.__class__.__name__, "function": self.getMethodName()(), "type": "json"}), 'ascii'))

		#if isinstance(kwargs, list):
			#parse args
		process = subprocess.Popen([command] + kwargs, env = os.environ.copy(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		try:
			out, err = process.communicate(timeout = 10)
		except subprocess.TimeoutExpired:
			process.kill()
			out, err = process.communicate()

		self.getConnection().send(bytes(json.dumps( {"stderr": err.decode('utf-8'), "stdout": out.decode('utf-8'), "returnCode": process.returncode}  ), 'ascii'))

		self.setResponse(stderr = err.decode('utf-8'), stdout = out.decode('utf-8'), returnCode = process.returncode)
		#else:
		#	raise Exception('Nope') # Pick a better Exception.

		return bool(process.returncode)