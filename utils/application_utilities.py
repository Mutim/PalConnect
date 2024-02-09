import re
import webbrowser
import asyncio
import concurrent.futures
from logging import getLogger

import customtkinter
import rcon
from rcon.source.client import Client, Packet

from utils.pal_exceptions import *
import config

__all__ = (
    "async_send_command",
    "valid_input",
    "is_valid_ip",
    "center_window",
    "format_message",
    "open_site",
    "get_player_list"
)


LOGGER = getLogger(__file__)


class MyClient(Client):
    # Palworld does not respond, so was killing the program. Have to make our own
    def read(self):
        with self._socket.makefile("rb") as file:
            response = Packet.read(file)
            return response


async def async_send_command(credentials: dict, command: str, *arguments: str) -> str:
    """
    Send an RCON command to a server.

    Args:
    - credentials (dict): Dictionary containing RCON connection details (ipaddr, port, password).
    - command (str): RCON command to be executed.
    - arguments (str): Arguments for the command.

    Internal Functions:
    - run_command() -> None: Function that allows async operation of the RCON connection on a separate thread.
    """
    ipaddr = credentials['ipaddr']
    port = credentials['port']
    password = credentials['password']

    command, arguments = sanitize_input(command, arguments)

    response = ""

    def run_command():
        """
        Internal function to execute the RCON command in a separate thread.

        Returns:
        - bool: True if the command is successfully sent, False otherwise.
        """
        nonlocal response

        print(f"Starting Communication to Server...\nCommand: {command}\nArguments: {arguments if arguments else 'None Provided'}\nConnecting to: {credentials['ipaddr']}:{credentials['port']}")

        try:
            with Client(ipaddr, port, passwd=password) as client:
                request = client.run(command, *arguments, encoding="ISO-8859-1", enforce_id=False)
                # request = Packet.make_command(command, *arguments, encoding="ISO-8859-1")
                # client.send(request)

            print(request)
            response = request
            return response
        except rcon.exceptions.WrongPassword as err:
            print(err)
            raise rcon.exceptions.WrongPassword
        except rcon.exceptions.SessionTimeout as err:
            print(f"Session Timed Out - {err}")
            raise rcon.exceptions.SessionTimeout
        except TimeoutError as err:
            print(f"Request Timed Out - {err}")
            raise TimeoutError
        except asyncio.CancelledError as err:
            print(f"Request Cancelled - {err}")
            return asyncio.CancelledError
        except Exception as err:
            print(f"Unhandled Exception: {err}")
            raise Exception
        finally:
            print("Finished Communication to Server. Closing connection")

    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            return await loop.run_in_executor(executor, run_command)
        except asyncio.CancelledError:
            print("Task Cancelled (outside run_in_executor)")

    return response


def sanitize_input(command: str, args: tuple) -> tuple:
    """Sanitizes the input of the `async_send_command()` function. This is to prevent arbitrary input,
        and verify that only correct commands are being served. Handles each command differently.

    Args:
        command: (str): The command that should be checked.
        args: (tuple): A tuple of arguments. This is passed as (args,).

    Returns:
        tuple: Will return a tuple of (command, args) to be passed to rcon

    Note:
    - If a new command is added to config.valid_commands, a new check must be added here. This might not be the best way.
    """
    if command.lower() == "broadcast":
        message_raw = args[0]
        if len(message_raw) > 39:
            message = format_message(message_raw, max_length=40, ret="\n")  # Breaks message into 40 character long strings with newlines to fit in PalWorld chat
            message = message.replace(" ", "\u00A0")
        else:
            message = message_raw.replace(" ", "\u00A0")

        return "Broadcast", (message,)

    elif command.lower() == "info":
        return "Info", ""

    elif command.lower() == "kickplayer":
        return "KickPlayer", args

    elif command.lower() == "showplayers":
        return "ShowPlayers", ""

    elif command.lower() == "shutdown":
        message_raw = args[0]
        message_split = message_raw.split(maxsplit=1)
        time = message_split[0]
        try:
            time = int(time)
        except ValueError:
            return "Info", ""  # Returning info until we get a way to communicate
        message = message_split[1].replace(" ", "\u00A0")
        message = (time, message)

        return "Shutdown", message


async def valid_input(screen: customtkinter.CTk, credentials: dict) -> bool | str:
    """Test if the provided credentials were accurate, and of correct type.

    Args:
        screen: (customtkinter.CTk): The main application window.
        credentials: (dict): A dictionary containing RCON login credentials.

    Returns:
        bool: True if a connection to the RCON server can be established, False otherwise.

    This function performs several checks to validate the provided RCON credentials, including:
    - Validating the IP address.
    - Validating the port number.
    - Sending an "Info" command to the server to check connectivity.
    - Handling errors such as invalid IP, invalid port, wrong password, timeout, or general exceptions.

    Note:
    - If all checks pass, the function returns True; otherwise, it returns False and updates the error labels
      on the application screen accordingly.

    """

    valid_cred = []
    result = ""

    try:
        a = is_valid_ip(credentials['ipaddr'])
        valid_cred.append(True)
    except InvalidIpAddress as err:
        screen.ipaddr_entry.delete(0, len(screen.ipaddr_entry.get()))
        screen.ipaddr_entry.configure(border_color='#E53030')
        screen.error_label.configure(text=f"[ Error ]\nNot a Valid IP Address")
        valid_cred.append(False)

    try:
        b = int(credentials['port'])
        valid_cred.append(True)
    except ValueError as err:
        screen.port_entry.delete(0, len(screen.port_entry.get()))
        screen.port_entry.configure(border_color='#E53030')
        screen.error_label.configure(text=f"[ Error ]\nInvalid Port Number")
        valid_cred.append(False)

    if all(valid_cred):
        credentials = {
            "ipaddr": credentials['ipaddr'],
            "port": int(credentials['port']),
            "password": credentials['password']}

        try:
            result = await async_send_command(credentials, "Info")
            config.welcome_text = f'Connected to PalConnect server!\n{result}\n\n________________________________________\n\n'
            print(f"Result is: {result}")
            if result:
                valid_cred.append(True)
                print("Appending True")
            else:
                valid_cred.append(False)
                print("Appending False")
        except rcon.exceptions.WrongPassword as err:
            screen.password_entry.delete(0, len(screen.password_entry.get()))
            screen.password_entry.configure(border_color='#E53030')
            screen.error_label.configure(text="[ Error ]\nInvalid Password")
            valid_cred.append(False)
        except (TimeoutError, OSError) as err:
            screen.error_label.configure(text="[ Error ]\nCould not communicate with the server")
            valid_cred.append(False)
        except Exception as err:
            screen.error_label.configure(text=f"[ General Error ]\nPlease report this on Github.")
            valid_cred.append(False)
            print(f"**Log This** - {err}")
    print(valid_cred)
    if all(valid_cred):
        return result

    return False


async def get_player_list(credentials) -> list[tuple]:

    players_online = []

    player_info_string = await async_send_command(credentials, "ShowPlayers")

    lines = player_info_string.split("\n")

    header = lines[0].split(",")
    lines = lines[1:]

    for line in lines:
        values = line.split(",")
        player_info = tuple(values)
        players_online.append(player_info)

    return players_online[:-1]


def is_valid_ip(ip) -> bool:
    expression = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if re.search(expression, ip):
        return True
    else:
        raise InvalidIpAddress


def center_window(screen: customtkinter.CTk, width: int, height: int, scale_factor: float = 1.0) -> str:
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)

    return f"{width}x{height}+{x}+{y}"


def format_message(message, max_length=40, ret="\n") -> str:
    """
    Break a message into lines, ensuring each line is no longer than the specified maximum length.

    Parameters:
    - message (str): The input message to be broken into lines.
    - max_length (int): The maximum length for each line (default is 40).
    - ret (str): The string used to separate lines (default is "\n").

    Returns:
    - str: The formatted message with lines no longer than max_length.
    """
    result = []
    current_line = ""

    for word in message.split():
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += f"{word} "
        else:
            result.append(current_line.strip())
            current_line = f"{word} "

    if current_line:
        result.append(current_line.strip())
    current = ""
    for line in result:
        current = f"{current + line}{ret}"
    return current


def open_site(url):
    """ Opens provided website """
    webbrowser.open_new(url)
