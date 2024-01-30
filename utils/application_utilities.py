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


# async def rcon_send_command(error_label: customtkinter.CTk, credentials: dict, command: str, *arguments: str):
#     ipaddr = credentials['ipaddr']
#     port = credentials['port']
#     password = credentials['password']
#     try:
#         with Client(ipaddr, port, passwd=password) as client:
#             response = client.run(command, *arguments, encoding="ISO-8859-1")
#
#         print(response.encode('utf8'))
#     except rcon.exceptions.WrongPassword as err:
#         error_label.configure(text=f"[ Error ]\n{err}\n")
#         print(err)
#     except rcon.exceptions.SessionTimeout as err:
#         error_label.configure(text=f"[ Error ]\n{err}")
#         print(err)
#     except TimeoutError as err:
#         error_label.configure(text=f"[ Error ]\n{err}\n")
#         print(err)
#     except Exception as err:
#         print(f"Unhandled Exception in {repr(rcon_send_command)}")
async def rcon_send_command(error_label: customtkinter.CTk, credentials: dict, command: str, *arguments: str):
    ipaddr = credentials['ipaddr']
    port = credentials['port']
    password = credentials['password']

    def run_command():
        print("Starting Communication to Server")
        print(command)
        print(arguments)
        try:
            print("Before RCON Package")
            with MyClient(ipaddr, port, passwd=password) as client:
                request = Packet.make_command(command, *arguments, encoding="ISO-8859-1")
                client.send(request)

            # print(response)
            print("Finished Communication to Server")
        except rcon.exceptions.WrongPassword as err:
            error_label.configure(text=f"[ Error ]\n{err}\n")
            print(err)
        except rcon.exceptions.SessionTimeout as err:
            error_label.configure(text=f"[ Error ]\n{err}")
            print(err)
        except TimeoutError as err:
            error_label.configure(text=f"[ Error ]\n{err}\n")
            print(err)
        except asyncio.CancelledError:
            print("Task Cancelled")
        except Exception as err:
            print(f"Unhandled Exception in {err}")

    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print("Executing Run Command")
        try:
            await loop.run_in_executor(executor, run_command)
        except asyncio.CancelledError:
            print("Task Cancelled (outside run_in_executor)")


async def valid_input(screen: customtkinter.CTk, credentials: dict) -> bool:
    """Test the connection to an RCON server. Returns True if connection can be made"""
    print("Called valid_input")
    valid_cred = []
    try:
        print("Try 1")
        a = is_valid_ip(credentials['ipaddr'])
        valid_cred.append(True)
    except InvalidIpAddress as err:
        screen.ipaddr_entry.delete(0, len(screen.ipaddr_entry.get()))
        screen.ipaddr_entry.configure(border_color='#E53030', placeholder_text='Invalid IP Address')
        screen.error_label.configure(text=f"[ Error ]\nNot a Valid IP Address")
        valid_cred.append(False)
        print("\nIP Address is invalid - Error Code")
    try:
        print("Try 2")
        b = int(credentials['port'])
        valid_cred.append(True)
    except ValueError as err:
        screen.port_entry.delete(0, len(screen.port_entry.get()))
        screen.port_entry.configure(border_color='#E53030', placeholder_text='Invalid Port Number')
        screen.error_label.configure(text=f"[ Error ]\nInvalid Port Number")
        valid_cred.append(False)

    if all(valid_cred):
        print("IP and Port Valid. Checking Creds")
        credentials = {
            "ipaddr": credentials['ipaddr'],
            "port": int(credentials['port']),
            "password": credentials['password']}
        try:
            print("Sending Info command to server")
            await rcon_send_command(screen, credentials, "Info")
            valid_cred.append(True)
        except rcon.exceptions.WrongPassword as err:
            screen.password_entry.delete(0, len(screen.password_entry.get()))
            screen.password_entry.configure(border_color='#E53030', placeholder_text='Invalid Password')
            screen.error_label.configure(text="[ Error ]\nInvalid Password")
            valid_cred.append(False)
            print("\nPassword is incorrect - Error code")
        except TimeoutError as err:
            screen.error_label.configure(text=f"[ Error ]\nRequest timed out. Are you using the correct credentials?")
            valid_cred.append(False)
        except Exception as err:
            screen.error_label.configure(text=f"[ General Error ]\nPlease report this on Github.")
            valid_cred.append(False)
            print(err)

    if all(valid_cred):
        return True

    return False


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


def open_site(url):
    webbrowser.open_new(url)