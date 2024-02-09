import time
import asyncio
import tkinter
import threading

import customtkinter

from utils.application_utilities import *
import config

__all__ = (
    "sending",
    "rcon_query_button_function",
    "check_command",
    "on_button_click",
    "fetch_online_players",
    "update_players",
    "kick_player"
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

        text_entry = f"\n[ {formatted_local_time} ] - {result}\n"
        screen.text_box.configure(state="normal")
        screen.text_box.insert(tkinter.END, text_entry)
        screen.text_box.see(tkinter.END)
        screen.text_box.configure(state="disabled")
        screen.command_entry.delete(0, len(screen.command_entry.get()))

    except ValueError as err:
        screen.error_label.configure(text=f"[ ERROR ]\nNo command entered. Type Help for info\n{err}")
    except Exception as err:
        screen.error_label.configure(text=f"[ ERROR ]\nUnexpected error. Please report on GitHub\n{err}")


def on_button_click(screen, rcon_credentials):
    rcon_query_button_function(screen, rcon_credentials)


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


# update_players loop updates every 30 seconds. Makes call to the server to see who's online
def update_players(screen, rcon_credentials, loop):
    time.sleep(5)
    while True:
        try:
            fetch_online_players(screen, rcon_credentials, loop)
        except (IOError, TimeoutError) as err:
            print(f"Timed out. Retrying in 30 seconds")
        time.sleep(30)
        print("Update Players Loop - Updating")


players_shown = []


def fetch_online_players(screen, rcon_credentials, loop):

    async def run_get_players():
        players = await get_player_list(rcon_credentials)
        return players

    if not loop.is_running():
        print("No event loop running")
        result = loop.run_until_complete(run_get_players())
    else:
        print("Event loop running")
        result = asyncio.run_coroutine_threadsafe(run_get_players(), loop).result()
    current_players = []

    for player in result:
        if player not in current_players:
            current_players.append(player)

    for player in players_shown:
        if player not in current_players:
            players_shown.remove(player)
            screen.player_config_frame.remove_item(f"{player[0]} - {player[2]}")

    for player in current_players:
        if player not in players_shown and player in result:
            screen.player_config_frame.add_item(f"{player[0]} - {player[2]}")
            players_shown.append(player)
    print(f"Current Players: {current_players}")
    print(f"Players Shown: {players_shown}")
    print(f"Result: {result}")


def kick_player(screen, rcon_credentials, player_info, loop):

    current_time = time.time()
    local_time_struct = time.localtime(current_time)
    formatted_local_time = time.strftime("%H:%M:%S", local_time_struct)
    screen.error_label.configure(text="")  # Reset error text
    player_name = player_info.split(' - ')[0]
    player_uuid = player_info.split(' - ')[1]

    async def run_kick_players():
        message = format_message(f"{player_name} was kicked from the server")
        result = await async_send_command(rcon_credentials, "KickPlayer", f"{player_uuid}")
        await async_send_command(rcon_credentials, "Broadcast", message)
        return result

    if not loop.is_running():
        result = loop.run_until_complete(run_kick_players())
    else:
        result = asyncio.run_coroutine_threadsafe(run_kick_players(), loop).result()

    kicked = f"\n[ {formatted_local_time} ] - Kicked {player_name} from the server!\n"
    screen.text_box.configure(state="normal")
    screen.text_box.insert(tkinter.END, kicked)
    screen.text_box.see(tkinter.END)
    screen.text_box.configure(state="disabled")
