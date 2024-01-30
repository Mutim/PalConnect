import re
import webbrowser
import asyncio
import concurrent.futures

import customtkinter
import rcon
from rcon.source import Client
from rcon.source.proto import Packet

from utils.pal_exceptions import *
import config

__all__ = (
    "rcon_send_command",
    "valid_input",
    "is_valid_ip",
    "center_window",
    "open_site"
)


class MyClient(Client):
    # Palworld does not respond, so was killing the program. Have to make our own
    def read(self):
        with self._socket.makefile("rb") as file:
            response = Packet.read(file)
            return response


valid_palword_commands = """
/Shutdown {Seconds} {MessageText}	The server is shut down after the number of Seconds
Will be notified of your MessageText.
/DoExit	Force stop the server.
/Broadcast {MessageText}	Send message to all player in the server.
/KickPlayer {SteamID}	Kick player from the server.
/BanPlayer {SteamID}	BAN player from the server.
/TeleportToPlayer {SteamID}	Teleport to current location of target player.
/TeleportToMe {SteamID}	Target player teleport to your current location
/ShowPlayers	Show information on all connected players.
/Info	Show server information.
/Save	Save the world data.
"""


async def rcon_send_command(credentials: dict, command: str, *arguments: str) -> None:
    """
    Send an RCON command to a server.

    Args:
    - credentials (dict): Dictionary containing RCON connection details (ipaddr, port, password).
    - command (str): RCON command to be executed.
    - arguments (str): Additional arguments for the command.

    Returns:
    - bool: True if the command is successfully sent, False otherwise.
    """
    ipaddr = credentials['ipaddr']
    port = credentials['port']
    password = credentials['password']

    def run_command():
        """
        Internal function to execute the RCON command in a separate thread.
        """
        print(f"Starting Communication to Server...\nCommand: {command}\nArguments: {arguments}\n{credentials}")
        try:
            with MyClient(ipaddr, port, passwd=password) as client:
                request = Packet.make_command(command, *arguments, encoding="ISO-8859-1")
                client.send(request)

            print(request)
            print("Finished Communication to Server. Closing connection")
        except rcon.exceptions.WrongPassword as err:
            print(f"Wrong Password Supplied - {err}")
            return False
        except rcon.exceptions.SessionTimeout as err:
            print(f"Session Timed Out - {err}")
            return False
        except TimeoutError as err:
            print(f"Request Timed Out - {err}")
            return False
        except asyncio.CancelledError as err:
            print(f"Request Cancelled - {err}")
            return False
        except Exception as err:
            print(f"Unhandled Exception: {err}")
            return False
        finally:
            # May need to close connections...I dunno
            pass

        return True

    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            await loop.run_in_executor(executor, run_command)
        except asyncio.CancelledError:
            print("Task Cancelled (outside run_in_executor)")


async def valid_input(screen: customtkinter.CTk, credentials: dict) -> bool:
    """Test if the provided credentials were accurate, and of correct type.

    Args:
        screen (customtkinter.CTk): The main application window.
        credentials (dict): A dictionary containing RCON login credentials.

    Returns:
        bool: True if a connection to the RCON server can be established, False otherwise.

    This function performs several checks to validate the provided RCON credentials, including:
    - Validating the IP address.
    - Validating the port number.
    - Sending an "Info" command to the server to check connectivity.
    - Handling errors such as invalid IP, invalid port, wrong password, timeout, or general exceptions.

    Note:
    - The "Info" command is currently designed to check connectivity and will be enhanced in the future
      when PalWorld fixes their RCON implementation.

    - If all checks pass, the function returns True; otherwise, it returns False and updates the error labels
      on the application screen accordingly.

    """
    valid_cred = []
    try:
        a = is_valid_ip(credentials['ipaddr'])
        valid_cred.append(True)
    except InvalidIpAddress as err:
        screen.ipaddr_entry.delete(0, len(screen.ipaddr_entry.get()))
        screen.ipaddr_entry.configure(border_color='#E53030', placeholder_text='Invalid IP Address')
        screen.error_label.configure(text=f"[ Error ]\nNot a Valid IP Address")
        valid_cred.append(False)
        print(f"\nIP Address is invalid - {err}")
    try:
        b = int(credentials['port'])
        valid_cred.append(True)
    except ValueError as err:
        screen.port_entry.delete(0, len(screen.port_entry.get()))
        screen.port_entry.configure(border_color='#E53030', placeholder_text='Invalid Port Number')
        screen.error_label.configure(text=f"[ Error ]\nInvalid Port Number")
        valid_cred.append(False)
        print(f"Invalid Port Number - {err}")

    if all(valid_cred):
        credentials = {
            "ipaddr": credentials['ipaddr'],
            "port": int(credentials['port']),
            "password": credentials['password']}
        try:
            # TODO: In the future, when PalWorld fixes their RCON, this will provide server info, as well as checking a connection.
            if await rcon_send_command(credentials, "Info"):
                valid_cred.append(True)
            else:
                screen.error_label.configure(text="[ Error ]\nCannot connect. Check your login credentials")
                valid_cred.append(False)
        except rcon.exceptions.WrongPassword as err:
            screen.password_entry.delete(0, len(screen.password_entry.get()))
            screen.password_entry.configure(border_color='#E53030', placeholder_text='Invalid Password')
            screen.error_label.configure(text="[ Error ]\nInvalid Password")
            valid_cred.append(False)
            print("\nPassword is incorrect - Error code")
        except (TimeoutError, OSError) as err:
            print(f"Connection error: {err}")
            screen.error_label.configure(text=f"[ Error ]\nRequest timed out. Are you using the correct credentials?")
            valid_cred.append(False)

        except Exception as err:
            screen.error_label.configure(text=f"[ General Error ]\nPlease report this on Github.")
            valid_cred.append(False)
            print(f"**Log This** - {err}")

    if all(valid_cred):
        return True

    return False


def is_valid_ip(ip) -> bool:
    """
    Check if the given IP address is valid.

    Parameters:
    - ip (str): The IP address to be validated.

    Returns:
    - bool: True if the IP address is valid, False otherwise.

    Raises:
    - InvalidIpAddress: If the IP address is not in a valid format.
    """
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


def break_message(message, max_length=40, ret="\n") -> str:
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
