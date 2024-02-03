"""
Custom RCON Source

This module provides a custom RCON client class, 'MyClient',
which extends the functionality of the base 'Client' class from the 'rcon' library.
The custom client is designed to handle scenarios where the server does not respond appropriately,
preventing the program from being terminated.

Classes:
- MyClient(Client): Custom RCON client class with enhanced response handling.

Dependencies:
- rcon: Core RCON library for server communication.

"""


import rcon
from rcon.source import Client
from rcon.source.proto import Packet


class MyClient(Client):
    def read(self):
        with self._socket.makefile("rb") as file:
            response = Packet.read(file)
            return response
