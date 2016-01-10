import socketserver, re, json, threading, logging, subprocess, os, importlib.util
#from ..request import RequestFile as RequestFileCommand
from bequeather.settings import get as getSettings

bufferSize = 1024 * 100
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

class TCPRequestHandler(socketserver.BaseRequestHandler):

    def getRoutine(self, routine, function):
        importedRoutines = {}
        # Scan 'routines' defined director(y/ies)
        for routineModule in os.listdir(getSettings().get('routines').get('dir')):
            # Cherry pick .py files only for time being
            # Potentially support for routines to be created in other languages in the future.
            if routineModule.endswith('.py'):
                # Strip the file extension
                moduleName = routineModule[:-3]

                # Dynamically import the module via the file location
                spec = importlib.util.spec_from_file_location("module.name", os.path.join(getSettings().get('routines').get('dir'), "{}.py".format(moduleName)))
                importedRoutines[moduleName] = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(importedRoutines[moduleName])

                # Iterate through all classes in module to see if any match the client 'routine'
                for className in importedRoutines[moduleName].classes:
                    if className == routine:
                        return getattr(importedRoutines[moduleName], routine)

        return False

    def handle(self):
        data = self.request.recv(bufferSize)
        logger.info('Received data: (%s) %dB', data, len(data))

        try:
            self.data = json.loads(str(data, 'ascii'))

            action = self.getRoutine(self.data.get('routine'), self.data.get('function'))
            if(action):
                #cur_thread = threading.current_thread()
                ##if self.requestFile(data):
                result = action(self.request)

                execution = getattr(result, self.data.get('function'))()
                if execution:
                    print(execution)
                    logger.debug("Success!")
                else:
                    logger.error("Action failed to execute")
            else:
                logger.warning('Unable to match action "%s"', action)

        except json.decoder.JSONDecodeError:
            logger.warning('Client data received was malformed (not JSON)')

        self.request.close()