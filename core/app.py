import os
import time
import asyncio

import tkinter
import customtkinter
from PIL import Image

from utils.application_utilities import *
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

    # Column 2
    screen.column_2 = customtkinter.CTkFrame(
        master=screen.main_frame,
        width=605,
        height=460,
        corner_radius=6)
    screen.column_2.place(x=330, y=10)

    screen.text_box = customtkinter.CTkTextbox(master=screen.column_2, width=585, height=370, border_width=2, border_color=("#3E454A", "#949A9F"), bg_color="transparent", state="disabled")
    screen.text_box.place(x=10, y=10)

    screen.command_entry = customtkinter.CTkEntry(master=screen.column_2, width=469, placeholder_text='Command',
                                                  border_color=("#979DA2", "#565B5E"))
    screen.command_entry.place(x=15, y=386)
    screen.command_entry.bind("<Return>", lambda event: rcon_query_button_function(screen, rcon_credentials))
    screen.text_box.insert(tkinter.END, sending(rcon_credentials, "Info"))
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


def sending(creds, command, *args):

    async def run_sending():
        if not asyncio.get_event_loop().is_running():
            print("No event loop running")
            result = await async_send_command(creds, command, *args)
            return result
        else:
            print("Event loop running")
            asyncio.create_task(async_send_command(creds, command, *args))

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(run_sending())
    # result = asyncio.run(run_sending())
    return result


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
            sending(rcon_credentials, command, arguments)
            if len(arguments) > 40:
                arguments = break_message(arguments, max_length=60)
        else:
            arguments = "\n" + "\n".join([f"{key}: {value}" for key, value in config.valid_commands.items()])

        text_entry = f"[ {formatted_local_time} ] - {command}: {arguments}\n"
        screen.text_box.configure(state="normal")
        screen.text_box.insert(tkinter.END, text_entry)
        screen.text_box.configure(state="disabled")
        screen.command_entry.delete(0, len(screen.command_entry.get()))

    except ValueError as err:
        screen.error_label.configure(text=f"[ ERROR ]\nNo command entered. Type Help for info\n{err}")
    except Exception as err:
        screen.error_label.configure(text=f"[ ERROR ]\nUnexpected error. Please report on GitHub\n{err}")


def check_command(entry: str) -> tuple:

    # returns true if valid command, regardless of split. If more than 1 word, it will only check the fist word.
    # If only 1 word is passed, it will check that word, and return true if it's in valid commands
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

        rcon_command_screen(screen, rcon_credentials)
        print("Can connect")
    else:
        screen.login_button.configure(state="normal")
        print("Cannot connect")
