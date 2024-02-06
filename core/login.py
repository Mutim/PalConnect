import os
import sys
import asyncio

import customtkinter as ctk
from PIL import Image

from utils.application_utilities import *
from core.app import console_screen
import config


class ServerConnectionScreen(ctk.CTk):

    def __init__(self, loop, interval=1 / 120):
        super().__init__()
        self.loop = loop
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.tasks = []
        self.tasks.append(loop.create_task(self.updater(interval)))

        ctk.set_appearance_mode(config.default_theme)
        ctk.set_default_color_theme(config.custom_theme)  # Themes: config.themes

        self.toplevel_window = None
        self.title('PalConnect - Console tool for PalWorld')
        self.geometry(center_window(self, 1280, 550, self._get_window_scaling()))
        if not os.name == 'posix':
            self.iconbitmap(config.logo_ico)

        # This assumes that the light and dark image are the same size (Which, they should be)
        bg_dimensions = Image.open(config.dark_image_pattern).size  # -> Returns a tuple as (w, h)

        # Sets the maximum and minimum sizes
        max_w, max_h = bg_dimensions
        self.maxsize(max_w, max_h)
        self.minsize(920, 480)
        self.logo_image = ctk.CTkImage(Image.open(config.logo_png),
                                                 size=(56, 56))
        self.background_image = ctk.CTkImage(light_image=Image.open(config.light_image_pattern),
                                                       dark_image=Image.open(config.dark_image_pattern),
                                                       size=bg_dimensions)
        self.label_1 = ctk.CTkLabel(master=self, image=self.background_image, text="")
        self.label_1.pack()

        # Credentials Frame
        self.frame = ctk.CTkFrame(
            master=self.label_1,
            width=320,
            height=360,
            corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label_2 = ctk.CTkLabel(
            master=self.frame,
            text=" Palworld Server Info",
            font=('Expose', 20),
            anchor="center",
            justify="center",
            compound="left",
            image=self.logo_image)
        self.label_2.place(x=20, y=20)

        self.error_label = ctk.CTkLabel(
            master=self.frame,
            text="",
            font=("Times Bold", 12),
            text_color="#E22323",

            )
        self.error_label.place(relx=0.5, y=338, anchor="center")

        self.ipaddr_entry = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='IP Address', border_color=("#979DA2", "#565B5E"))
        self.ipaddr_entry.place(x=50, y=100)
        self.ipaddr_entry.bind("<Return>", lambda event, screen=self: login_button_function(screen))

        self.port_entry = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='Port', border_color=("#979DA2", "#565B5E"))
        self.port_entry.place(x=50, y=145)
        self.port_entry.bind("<Return>", lambda event, screen=self: login_button_function(screen))

        self.password_entry = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='Password', show="*", border_color=("#979DA2", "#565B5E"))
        self.password_entry.place(x=50, y=190)
        self.password_entry.bind("<Return>", lambda event, screen=self: login_button_function(screen))

        # Create buttons
        self.login_button = ctk.CTkButton(master=self.frame, width=220, text="Login", command=lambda: login_button_function(self), corner_radius=6)
        self.login_button.place(x=50, y=240)

        github_image = ctk.CTkImage(
            Image.open(config.github_image).resize((20, 20), Image.Resampling.LANCZOS))
        discord_image = ctk.CTkImage(
            Image.open(config.discord_image).resize((20, 20), Image.Resampling.LANCZOS))
        github_button = ctk.CTkButton(master=self.frame, image=github_image, text="Github", width=100, height=20,
                                      compound="left", command=lambda: open_site(config.gitgub_url),
                                      fg_color='white', text_color='black', hover_color='#AFAFAF')
        github_button.place(x=50, y=290)

        discord_button = ctk.CTkButton(master=self.frame, image=discord_image, text="Discord", width=100,
                                       height=20, compound="left", command=lambda: open_site(config.discord_url),
                                       fg_color='white', text_color='black', hover_color='#AFAFAF')
        discord_button.place(x=170, y=290)

    async def updater(self, interval):
        while True:
            self.update()
            await asyncio.sleep(interval)

    def close(self):
        # Put close confirmation window here?
        for task in self.tasks:
            task.cancel()

        self.loop.stop()
        self.destroy()


def login_button_function(screen: ctk.CTk):

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
        await console_screen(screen, rcon_credentials)
    else:
        screen.login_button.configure(state="normal")
        print("Cannot connect")
