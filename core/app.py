import asyncio
import tkinter
import threading

import customtkinter

from utils.button_functions import *
from utils.application_utilities import *
from widgets.scrollable_frames import ScrollableRadiobuttonFrame
import config

__all__ = (
    "console_screen"
)


def column_1(screen, rcon_credentials):
    """
    Start of column_1
    """

    screen.main_frame = customtkinter.CTkFrame(
        master=screen.label_1,
        width=945,
        height=480,
        corner_radius=15,
        border_width=2,
        background_corner_colors=("#d4dbe3", "#d4dbe3", "#6c7850", "#455c42"),
        border_color=("#3E454A", "#949A9F"),
        bg_color="#DEDEDE")
    screen.main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    loop = asyncio.get_event_loop()
    update_players_thread = threading.Thread(target=update_players, args=(screen, rcon_credentials, loop))
    update_players_thread.start()
    # Column 1
    screen.column_1 = customtkinter.CTkFrame(
        master=screen.main_frame,
        width=315,
        height=460,
        corner_radius=6)
    screen.column_1.place(x=10, y=10)

    screen.player_config_frame = ScrollableRadiobuttonFrame(master=screen.column_1, width=285, command=None,
                                                            corner_radius=5, height=125,
                                                            item_list=None,  # fetch_online_players(rcon_credentials)
                                                            label_text="Players Online")
    screen.player_config_frame._scrollbar.configure(height=0)
    screen.player_config_frame.place(x=5, y=5)

    screen.ban_player_button = customtkinter.CTkButton(master=screen.column_1, width=50, text="Ban Player",
                                                       command=lambda: testing(screen),
                                                       corner_radius=6)

    screen.ban_player_button.place(x=25, y=183)

    screen.kick_player_button = customtkinter.CTkButton(master=screen.column_1, width=50, text="Kick Player",
                                                        command=lambda: kick_player(screen, rcon_credentials, screen.player_config_frame.get_checked_item(), loop),
                                                        corner_radius=6)

    screen.kick_player_button.place(x=105, y=183)


def column_2(screen, rcon_credentials):
    """
    Start of column_2
    """

    screen.column_2 = customtkinter.CTkFrame(
        master=screen.main_frame,
        width=605,
        height=460,
        corner_radius=6)
    screen.column_2.place(x=330, y=10)

    screen.text_box = customtkinter.CTkTextbox(master=screen.column_2, width=585, height=370, border_width=2,
                                               border_color=("#3E454A", "#949A9F"), bg_color="transparent",
                                               state="disabled")
    screen.text_box.place(x=10, y=10)
    screen.text_box.tag_config("center", justify="center")

    screen.command_entry = customtkinter.CTkEntry(master=screen.column_2, width=469, placeholder_text='Command',
                                                  border_color=("#979DA2", "#565B5E"))
    screen.command_entry.place(x=15, y=386)
    screen.command_entry.bind("<Return>", lambda event: rcon_query_button_function(screen, rcon_credentials))

    screen.send_button = customtkinter.CTkButton(master=screen.column_2, width=91, text="Send Command",
                                                 command=lambda: rcon_query_button_function(screen, rcon_credentials),
                                                 corner_radius=6)
    screen.send_button.place(x=489, y=386)

    screen.error_label = customtkinter.CTkLabel(
        master=screen.column_2,
        text="",
        font=("Times Bold", 12),
        text_color="#E22323"
    )
    screen.error_label.place(relx=0.5, y=437, anchor="center")

    screen.text_box.configure(state="normal")
    screen.text_box.insert(tkinter.END, config.welcome_text, "center")
    screen.text_box.configure(state="disabled")


def console_screen(screen: customtkinter.CTk, rcon_credentials: dict):
    """Main command screen for sending RCON commands."""

    screen.frame.destroy()
    column_1(screen, rcon_credentials)
    column_2(screen, rcon_credentials)
