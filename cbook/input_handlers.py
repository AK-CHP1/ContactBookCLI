"""This file contains input functions 
beginning with `ask_*` used by different other
functions"""
import configparser as cf
from pathlib import Path
import re
from typing import Optional


def ask_int(
    prompt: str = "",
    required: bool = False,
    low: Optional[int] = None,
    high: Optional[int] = None,
    default=0
) -> int:
    """Ask's the user for an integer between `low` and `high`
    (inclusive)"""

    while True:

        inp = input(prompt)
        # If user just pressed enter and field is required
        # Then inform the user
        if required and (not inp):
            print("This field is required.")
            continue

        # If the user didn't entered anything and the field is 
        # not required, then return the default
        if not (required or inp):
            break

        # Checking if the user provided a valid integer
        try:
            data = int(inp)
        except ValueError:
            print("Invalid integer")
            continue
        # Chiecking for low and high if defined
        if low and data < low:
            print(f"Minimum: {low}")
            continue

        if high and data > high:
            print(f"Maximum: {high}")
            continue

        return data
    return default


def ask_email(
    prompt: str = "", required: bool = False, default=None
) -> str:
    """Prompts the user to enter a valid email and, if required
    if `False` returns the `default` value

    :param prompt: Prompt to display user
    :type prompt: str
    :param required: If `True` the user will be reprompted until
     the correct input is entered
    :type required: boo.
    :param: default; Default value to return if `required` is `False`
    :type default: Union[str, None]

    :returns: provided email address
    :rtype: Union[str, None]"""

    while True:
        inp = input(prompt)
        # Checks if email is not required and no input is entered
        if not (inp or required):
            break

        # If user didn't entered anything and the field is required
        # Then inform the user
        if required and (not inp):
            print("This field is required.")
            continue

        # Otherwise check for correctness of email
        if match := re.search(r"^[a-zA-Z0-9_.]+@(?:\w+\.){1,}\w+", inp):
            return match.group(0)
        print("Invalid email")
    return default


def ask_phone_no(
    prompt: str = "",
    required: bool = False,
    default: Optional[str] = None
) -> Optional[str]:
    """Prompts the user for a valid phone no., also formats it
    to include a proper country code. If the `required` is `False`
    and no proper input is given `default` value is returned

    :param prompt: Prompt to display the user
    :type prompt: str

    :param required: if False the prompt will occur only once
    :type required: bool

    :returns: a valid phone no.
    :rtype: str
    """

    while True:
        inp = input(prompt)
        # If user just pressed <Enter> and phone no. is not required
        # In this case the function will return `None`
        if not (inp or required):
            break

        # If user didn't entered anything and the field is required
        # Then inform the user
        if required and (not inp):
            print("This field is required.")
            continue

        # Checks if input matches the phone no. format
        if match := re.search(r"^(\+\d{1,3})?(\d{10})$", inp):
            # If the number is in correct format
            # Checking for the presence of country code
            code, ph_no = match.groups()
            if not code:
                # If country code is not present, it will be added
                conf_path = Path.home() / ".cbook_conf.ini"
                with conf_path.open() as cfile:
                    parser = cf.ConfigParser()
                    parser.read_file(cfile)
                    code = '+' + parser.get("USER", "country_code")
            ph_no = f"{code}-{ph_no}"
            return ph_no
        print("Invalid phone no.")
        print(
            "Phone no. should be 10-digit long and may include"
            "additional country code at the beginning"
            "(starting with + sign)."
        )
    return default


def ask_text(
        prompt: str = "",
        required: bool = False,
        default: Optional[str] = None) -> Optional[str]:
    """Prompts the user to enter a text, if no text is entered
    and required is False, returns default otherwise text"""

    while True:
        text = input(prompt)
        # Checking for empty string
        if not text:
            if required:
                print("This field is required.")
                continue
            else:
                return default
        else:
            return text
