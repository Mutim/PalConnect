import os
import shutil


### - URLs and Links
gitgub_url = 'https://github.com/'
discord_url = 'https://www.discord.gg/'


## - Customize Message Options
default_textbox_text = f"""

"""
# Key: Value must be a combined length of less than 95 characters to fit on screen
valid_commands = {
    "Broadcast": "{MessageText}	Send message to all player in the server.",
    "Info": "Returns server info",
    "Shutdown": "{Seconds} {MessageText} Shut down the after {Seconds}, and display {MessageText}",
    "DoExit": "Force stop the server with no warning text",
    "KickPlayer": "	Kick player from the server.",
    "BanPlayer": "{SteamID}	BAN player from the server.",
    "TelePortToPlayer": "{SteamID}	Teleport to current location of target player.",
    "TeleportToMe": "{SteamID}	Target player teleport to your current location",
    "ShowPlayers": "Show information on all connected players.",
    "Save": "Save the world data.",
    "Help": "Serve this page"
}

### - Image Options
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
logo_png = os.path.join(image_path, "logo.png")
logo_ico = os.path.join(image_path, "logo.ico")

## - Dark Theme Images
dark_image_pattern = os.path.join(image_path, "dark", "pattern_dark.png")

## - Light Theme Image
light_image_pattern = os.path.join(image_path, "light", "pattern_light.png")

## - Social Images
google_image = os.path.join(image_path, "social", "google_logo.png")
github_image = os.path.join(image_path, "social", "github_logo.png")
discord_image = os.path.join(image_path, "social", "discord_logo.png")


### Theme Options
# Create a custom theme by following the template in "./themes_path/custom_theme".
#   TIP: Lists of color options in themes (ex: "text_color": ["#DCE4EE", "#DCE4EE"]) are ordered as such
#   that the first index is to be used in 'light' mode, while the second index is used in 'dark mode.
themes_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "themes")

# Add new themes here, and within the themes' directory.
custom_theme = os.path.join(themes_path, "custom_theme.json")

# Default theme the system will use.
default_theme = "custom_theme"


### - Terminal Options
terminal_size = shutil.get_terminal_size()
terminal_h = shutil.get_terminal_size().columns
terminal_w = shutil.get_terminal_size().lines


### - Window Options
login_menu_size = "600x440"
menu_size_w = "1280"
menu_size_h = "550"
menu_size = f"{menu_size_w}x{menu_size_h}"
