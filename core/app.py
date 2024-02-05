import os
import sys
import time
import asyncio

import tkinter
import customtkinter
from PIL import Image

from utils.application_utilities import *
from utils.button_functions import *
from widgets.scrollable_frames import ScrollableRadiobuttonFrame
import config


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, closing_event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.geometry("500x300")
        self.closing_event = closing_event

        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)

    def closing(self):
        self.destroy()
        if self.closing_event is not None:
            self.closing_event()


class ServerConnectionScreen(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customtkinter.set_appearance_mode(config.default_theme)
        customtkinter.set_default_color_theme(config.custom_theme)  # Themes: config.themes

        self.toplevel_window = None
        self.title('PalConnect - RCON Connection tool for PalWorld')
        self.geometry(center_window(self, 1280, 550, self._get_window_scaling()))
        if not os.name == 'posix':
            self.iconbitmap(config.logo_ico)

        # This assumes that the light and dark image are the same size (Which, they should be)
        bg_dimensions = Image.open(config.dark_image_pattern).size  # -> Returns a tuple as (w, h)

        # Sets the maximum and minimum sizes
        max_w, max_h = bg_dimensions
        self.maxsize(max_w, max_h)
        self.minsize(920, 480)
        self.logo_image = customtkinter.CTkImage(Image.open(config.logo_png),
                                                 size=(56, 56))
        self.background_image = customtkinter.CTkImage(light_image=Image.open(config.light_image_pattern),
                                                       dark_image=Image.open(config.dark_image_pattern),
                                                       size=bg_dimensions)
        self.label_1 = customtkinter.CTkLabel(master=self, image=self.background_image, text="")
        self.label_1.pack()

        # Credentials Frame
        self.frame = customtkinter.CTkFrame(
            master=self.label_1,
            width=320,
            height=360,
            corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label_2 = customtkinter.CTkLabel(
            master=self.frame,
            text=" Palworld Server Info",
            font=('Expose', 20),
            anchor="center",
            justify="center",
            compound="left",
            image=self.logo_image)
        self.label_2.place(x=20, y=20)

        self.error_label = customtkinter.CTkLabel(
            master=self.frame,
            text="",
            font=("Times Bold", 12),
            text_color="#E22323",

            )
        self.error_label.place(relx=0.5, y=338, anchor="center")

        self.ipaddr_entry = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='IP Address', border_color=("#979DA2", "#565B5E"))
        self.ipaddr_entry.place(x=50, y=100)
        self.ipaddr_entry.bind("<Return>", lambda event, screen=self: login_button_function(screen))

        self.port_entry = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Port', border_color=("#979DA2", "#565B5E"))
        self.port_entry.place(x=50, y=145)
        self.port_entry.bind("<Return>", lambda event, screen=self: login_button_function(screen))

        self.password_entry = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Password', show="*", border_color=("#979DA2", "#565B5E"))
        self.password_entry.place(x=50, y=190)
        self.password_entry.bind("<Return>", lambda event, screen=self: login_button_function(screen))

        # Create buttons
        self.login_button = customtkinter.CTkButton(master=self.frame, width=220, text="Login",
                                                    command=lambda: login_button_function(self),
                                                    corner_radius=6)
        self.login_button.place(x=50, y=240)

        github_image = customtkinter.CTkImage(
            Image.open(config.github_image).resize((20, 20), Image.Resampling.LANCZOS))
        discord_image = customtkinter.CTkImage(
            Image.open(config.discord_image).resize((20, 20), Image.Resampling.LANCZOS))
        github_button = customtkinter.CTkButton(master=self.frame, image=github_image, text="Github", width=100, height=20,
                                                compound="left", command=lambda: open_site(config.gitgub_url),
                                                fg_color='white', text_color='black', hover_color='#AFAFAF')
        github_button.place(x=50, y=290)

        discord_button = customtkinter.CTkButton(master=self.frame, image=discord_image, text="Discord", width=100,
                                                 height=20,
                                                 compound="left", command=lambda: open_site(config.discord_url),
                                                 fg_color='white', text_color='black', hover_color='#AFAFAF')
        discord_button.place(x=170, y=290)

    def open_toplevel(self):
        if self.toplevel_window is None:  # create toplevel window only if not already open
            self.toplevel_window = ToplevelWindow(self, closing_event=self.toplevel_close_event)

    def toplevel_close_event(self):
        self.toplevel_window = None

    # modify update function to allow threading
    def update(self):
        if self._window_exists is False:
            if sys.platform.startswith("win"):
                if not self._withdraw_called_before_window_exists and not self._iconify_called_before_window_exists:
                    self.deiconify()

            self._window_exists = True
        print("Update")
        super().update()


def rcon_command_screen(screen: customtkinter.CTk, rcon_credentials: dict):
    """Main command screen for sending RCON commands. This is where all functionality lives"""

    screen.frame.destroy()
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

    # Column 1
    screen.column_1 = customtkinter.CTkFrame(
        master=screen.main_frame,
        width=315,
        height=460,
        corner_radius=6)
    screen.column_1.place(x=10, y=10)

    screen.player_config_frame = ScrollableRadiobuttonFrame(master=screen.column_1, width=285, command=None, corner_radius=5, height=200,
                                                            item_list=[f"item {i}" for i in asyncio.run(get_player_list(rcon_credentials))],
                                                            label_text="ScrollableRadiobuttonFrame")
    screen.player_config_frame.place(x=5, y=5)
    # screen.player_config_frame.remove_item("item 3")  # Remove items from the list

    # Column 2
    screen.column_2 = customtkinter.CTkFrame(
        master=screen.main_frame,
        width=605,
        height=460,
        corner_radius=6)
    screen.column_2.place(x=330, y=10)

    screen.text_box = customtkinter.CTkTextbox(master=screen.column_2, width=585, height=370, border_width=2, border_color=("#3E454A", "#949A9F"), bg_color="transparent", state="disabled")
    screen.text_box.place(x=10, y=10)
    screen.text_box.tag_config("center", justify="center")

    screen.command_entry = customtkinter.CTkEntry(master=screen.column_2, width=469, placeholder_text='Command',
                                                  border_color=("#979DA2", "#565B5E"))
    screen.command_entry.place(x=15, y=386)
    screen.command_entry.bind("<Return>", lambda event: rcon_query_button_function(screen, rcon_credentials))

    send_button = customtkinter.CTkButton(master=screen.column_2, width=91, text="Send Command",
                                          command=lambda: rcon_query_button_function(screen, rcon_credentials),
                                          corner_radius=6)
    send_button.place(x=489, y=386)

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

