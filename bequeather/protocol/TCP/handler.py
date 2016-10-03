import socketserver, re, json, threading, logging, subprocess, os, importlib.util
import bequeather

bufferSize = 1024 * 100
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

class TCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(bufferSize)
        logger.info('Received data: (%s) %dB', data, len(data))
        print(dir(bequeather.server.Routines))
        try:
            self.data = json.loads(str(data, 'ascii'))

            action = bequeather.server.Routines.getRoutine(self.data.get('routine'), self.data.get('function'))
            if(action):
                #cur_thread = threading.current_thread()
                ##if self.requestFile(data):
                result = action()
                print("RESULT")
                print(result)
                #execution = getattr(result, self.data.get('function'))
                #if execution:
                #    print(execution())
                #    logger.debug("Success!")
                #else:
                #    logger.error("Action failed to execute")
                return result
            else:
                logger.warning('Unable to match action "%s"', action)

        except json.decoder.JSONDecodeError:
            logger.warning('Client data received was malformed (not JSON)')

        self.request.close()