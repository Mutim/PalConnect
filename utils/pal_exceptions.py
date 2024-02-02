"""
pal_exceptions

This package includes exception classes for handling various error scenarios related PalConnect

Classes:
- ConfigReadError: Indicates an error while reading the configuration.
- EmptyResponse: Indicates an empty response from the server.
- SessionTimeout: Indicates that the session timed out.
- UserAbort: Indicates that a required action has been aborted by the user.
- WrongPassword: Indicates a wrong password.
- InvalidIpAddress: Raised when an invalid IP address is found.

Dependencies:
- rcon: Core RCON library for server communication.

"""


import rcon
import rcon.exceptions


# RCON Exceptions. Will call these explicitly when recreating RCON
class ConfigReadError(Exception):
    """Indicates an error while reading the configuration."""


class EmptyResponse(Exception):
    """Indicates an empty response from the server."""


class SessionTimeout(Exception):
    """Indicates that the session timed out."""


class UserAbort(Exception):
    """Indicates that a required action has been aborted by the user."""


class WrongPassword(Exception):
    """Indicates a wrong password."""


# Custom Exceptions
class InvalidIpAddress(Exception):
    """ Raised when an invalid IP address is found """
    pass
