import time
import asyncio
import tkinter

import customtkinter

from application_utilities import *

__all__ = (
    "sending",
    "rcon_query_button_function",
    "check_command",
    "login_handler",
    "login_button_function"
)


def sending(creds, command, *args):

    loop = asyncio.get_event_loop()

    async def run_sending():
        if not loop.is_running():
            result = loop.run_until_complete(async_send_command(creds, command, *args))
            return result
        else:
            result = await async_send_command(creds, command, *args)
            return result

    if not loop.is_running():
        return loop.run_until_complete(run_sending())
    else:
        return asyncio.create_task(run_sending())


def rcon_query_button_function(screen, rcon_credentials):

    current_time = time.time()
    local_time_struct = time.localtime(current_time)
    formatted_local_time = time.strftime("%H:%M:%S", local_time_struct)
    screen.error_label.configure(text="")  # Reset error text
    entry_text = screen.command_entry.get()
    try:
        command, arguments = check_command(entry_text)
        if not command:
            screen.error_label.configure(text="[ ERROR ]\nCommand not valid. Type Help for info\n")
            return

        print(f"Command: {command} Arguments: {arguments}")

        if command.lower() != "help":
            result = sending(rcon_credentials, command, arguments)
        else:
            result = "Server Commands\n" + "\n".join([f"{key}: {value}" for key, value in config.valid_commands.items()])

        text_entry = f"[ {formatted_local_time} ] - {result}\n"
        screen.text_box.configure(state="normal")
        screen.text_box.insert(tkinter.END, text_entry)
        screen.text_box.see(tkinter.END)
        screen.text_box.configure(state="disabled")
        screen.command_entry.delete(0, len(screen.command_entry.get()))

    except ValueError as err:
        screen.error_label.configure(text=f"[ ERROR ]\nNo command entered. Type Help for info\n{err}")
    except Exception as err:
        screen.error_label.configure(text=f"[ ERROR ]\nUnexpected error. Please report on GitHub\n{err}")


def check_command(entry: str) -> tuple:
    valid_commands = [key.lower() for key in config.valid_commands.keys()]

    if " " in entry:
        command, arguments = entry.split(" ", maxsplit=1)
    else:
        command, arguments = entry, ""

    if command.lower() in valid_commands:
        return command, arguments
    else:
        return None, None


def login_button_function(screen: customtkinter.CTk):

    async def run_login_handler():
        await login_handler(screen, rcon_credentials)
    screen.error_label.configure(text="")
    screen.ipaddr_entry.configure(border_color=("#979DA2", "#565B5E"), placeholder_text='IP Address')
    screen.port_entry.configure(border_color=("#979DA2", "#565B5E"), placeholder_text='Port')
    rcon_credentials = {
        "ipaddr": screen.ipaddr_entry.get(),
        "port": screen.port_entry.get(),
        "password": screen.password_entry.get()
    }

    loop = asyncio.get_event_loop()

    if not loop.is_running():
        print("No event loop running")
        loop.run_until_complete(run_login_handler())
    else:
        print("Event loop running")
        asyncio.create_task(run_login_handler())


# Handles login asynchronously. May move this functionality to a more general handler
async def login_handler(screen, rcon_credentials):

    if await valid_input(screen, rcon_credentials):
        rcon_credentials = {
            "ipaddr": screen.ipaddr_entry.get(),
            "port": int(screen.port_entry.get()),
            "password": screen.password_entry.get()
        }

        print("Can connect")
        rcon_command_screen(screen, rcon_credentials)
    else:
        screen.login_button.configure(state="normal")
        print("Cannot connect")
