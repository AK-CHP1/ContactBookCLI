"""
This module contains helper functions used by
functions defined in `options.py`
"""
from datetime import datetime
from typing import List, Dict, Optional, Union
from tabulate import tabulate
from datamanager import Contact


def format_for_display(
        contact_list: List[Contact], full: bool = False
        ) -> List[Dict]:
    """Formats the contact as an appropriate dict to display as a table"""
    
    display_list = []
    for contact in contact_list:
        display_data: Dict[str, Union[Optional[str], datetime]] = dict()

        # If last_name is None, it won't concate with string
        # So using empty string
        last_name = contact.last_name if contact.last_name else ""
        display_data["Name"] = contact.first_name + ' ' + last_name  
        display_data["Personal phone"] = contact.phone_personal
        display_data["Address"] = contact.address

        if full:
            display_data["Phone work"] = contact.phone_work
            display_data["Phone home"] = contact.phone_home
            display_data["Email"] = contact.email
            display_data["Added on"] = contact.date_added
        display_list.append(display_data)

    return display_list


def display_table(data: List[Dict]):
    """Display's the table for the given list"""

    if data:
        tb_data = tabulate(
            data, headers="keys", tablefmt="mixed_grid", showindex=True)
        print(tb_data)


def display_full(data: Dict):
    """Displays a the given data as a card"""

    col1 = ["\033[1;37m" + item + "\033[0m" for item in data.keys()]
    col2 = [value for value in data.values()]
    table = list(zip(col1, col2))
    tb_str = tabulate(table, tablefmt="simple_grid")
    print(tb_str)
