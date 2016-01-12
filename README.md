# Bequeather - Server
A(*nother*) abstracted TCP Socket server which will be used to transmit files - written for Python 3.5 and above

## Install
TBA.

## Routines
Routines are defined on a per server instance basis, the directory is configured in the settings.yml file as 'dir', under the key 'routines'.

Routines must extend from the 'UserRoutine' class defined in 'bequeather.routine', and only they're expected to implement bequeather commands.

```python
#Example Routine "ip.py"
from bequeather.routine import UserRoutine
from bequeather.action.command import ShellCommand

class IPAddress(UserRoutine):
    def get(self):
        command = ShellCommand(self.getConnection())
        command.setArguments(command ='/bin/ip', args = ['addr'])
        command.execute()
        return command.getResponse()
```
The connected client would then proceed to request the routine 'IPAddress' & function 'get'.

Expected output would be:
```python
# TBA
```

### Commands
There is two command submodules available at this point in time.
- command
  - ShellCommand
- request
  - RequestFileStream
  - RequestWeb (TBA)

## Settings
TBA.

Sample settings.yml
```yaml
routines:
    dir: "/home/user/routines" # Absolute path only

chunkSize: 10240 #bytes
```

## Usage
TBA.

## Why?
1. I may have a constant hankering to ensure my garage door is closed; armed with a webcam & Raspberry Pi this server will enable me to mentally soothe my garage door related woes.
2. It's a relatively simple project to bring myself back into Python-mode after too working with too much PHP.

## Roadmap/Ideas
* Authentication - via users, or key 
* ACL for users/keys
* Support streaming from a live feed and/or streaming video formats
* Support TLS for socket
* Different server 'adapters'
  * Web Socket
  * UDP(Anyone?)
  * HTTP
* Support for Python >= 2

## Notes
* This will be my first publically available Python 3 module
* Also my first time jumping back into Python after an unintended hiatus. Please be gentle :)