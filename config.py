import os
import shutil


### - URLs and Links
gitgub_url = 'https://github.com/'
discord_url = 'https://www.discord.gg/'


## - Customize Message Options
default_textbox_text = f"""
Enter your message here!

\t—————[ Information ]—————
Everything typed in this box will be typed automatically with the settings on the
right. If you would like to reset these options to the default, click on the
"Typer Options" button above the options. Alternatively, if you want to change
any tool options, navigate to the "Settings" section on the left side panel.

If you have any issues with the tool, please contact me by following the social
links on the main page, or visiting them here: 

Github: {gitgub_url}
Discord: {discord_url}

Clear this textbox by clicking the "Clear Texbox" button below. 

Happy Typing!
"""

### - Image Options
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
logo_png = os.path.join(image_path, "logo.png")
logo_ico = os.path.join(image_path, "logo.ico")

## - Dark Theme Images
dark_image_home = os.path.join(image_path, "dark", "home_dark.png")
dark_image_search = os.path.join(image_path, "dark", "search_dark.png")
dark_image_convert = os.path.join(image_path, "dark", "converter_dark.png")
dark_image_clicker = os.path.join(image_path, "dark", "auto_clicker_dark.png")
dark_image_typer = os.path.join(image_path, "dark", "typer_dark.png")
dark_image_pattern = os.path.join(image_path, "dark", "pattern_dark.png")
dark_image_settings = os.path.join(image_path, "dark", "settings_dark.png")

## - Light Theme Image
light_image_home = os.path.join(image_path, "light", "home_light.png")
light_image_search = os.path.join(image_path, "light", "search_light.png")
light_image_convert = os.path.join(image_path, "light", "converter_light.png")
light_image_clicker = os.path.join(image_path, "light", "auto_clicker_light.png")
light_image_typer = os.path.join(image_path, "light", "typer_light.png")
light_image_settings = os.path.join(image_path, "light", "settings_light.png")
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
