import configparser as cfg
from pathlib import Path

import pyfiglet as pfg  # type: ignore

from input_handlers import ask_text
from options import OPTIONS


def show_help():
    """Shows a list of available options and other helpful
    information"""

    print("OPTIONS")
    print("-------")
    options = OPTIONS.keys()
    for i, opt in enumerate(options):
        text = f"{i+1}. {opt}"
        print(text)
    print("Press Ctrl-C to cancel an option in the middle.")


def setup():
    """Prompt's the user for his details and set's up
    the configuration file used by the program"""

    conf_path = Path.home() / ".cbook_conf.ini"
    if not conf_path.exists():
        full_name = ask_text("Please provide your full name: ", True)
        country_code = ask_text(
            "Please specify the default country code: ", True)
        with conf_path.open("w") as cf:
            parser = cfg.ConfigParser()
            parser.add_section("USER")
            parser.set("USER", "name", full_name)
            parser.set("USER", "country_code", str(country_code))
            parser.write(cf)
    

def greet_user():
    """Greets the user by showing the application name
    with figlet fonts, and displaying the user's name"""

    # Displaying the application name
    greet_text = "ContactBookCLI"
    figlet = pfg.Figlet()
    figlet.setFont(font="big")
    formatted_text = figlet.renderText(greet_text)
    print(formatted_text)

    # Displaying the user's name
    conf_path = Path.home() / ".cbook_conf.ini"
    with conf_path.open() as cfile:
        parser = cfg.ConfigParser()
        parser.read_file(cfile)
        name = parser.get("USER", "name")
    print(f"Welcome, {name}!")

