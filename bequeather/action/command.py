from .base import BaseAction
import os, subprocess, logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

class ShellCommand(BaseAction):

	def execute(self):
		"""Executes a remote shell command

		"""
		logger.debug("Executing shell command {}".format(self.command))
		command = self.getArgument('command')
		kwargs = self.getArgument('args')

		if isinstance(kwargs, list):
			#parse args
			process = subprocess.Popen([command] + kwargs, env = os.environ.copy(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			try:
				out, err = process.communicate(timeout = 10)
			except subprocess.TimeoutExpired:
				process.kill()
				out, err = process.communicate()

			self.setResponse(stderr = err.decode('utf-8'), stdout = out.decode('utf-8'), returnCode = process.returncode)
		else:
			raise Exception('Nope') # Pick a better Exception.

		return bool(process.returncode)