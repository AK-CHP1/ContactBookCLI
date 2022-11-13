from datetime import datetime
from typing import Union

from tabulate import tabulate

from datamanager import Contact, DataManager
from data_display import format_for_display, display_full, display_table
from input_handlers import ask_int, ask_email, ask_phone_no, ask_text

dmgr = DataManager()

OPTIONS = dict()    # keys: Help text, values: function responsible


def _select_contact() -> Union[Contact, None]:  # type: ignore[return]
    """Prompts the user to search for a contact by name and then
    select one from the found contacts, it finally returns the
     selected contact"""

    search_name = ask_text("Enter the name: ", True)
    contacts = dmgr.fetch_by_name(search_name) # type: ignore
    print(f"Found {len(contacts)} contacts")
    if contacts:
        tb_data = format_for_display(contacts)
        display_table(tb_data)  # type: ignore[arg-type]
        index = ask_int("Enter the index: ",
                        required=True, low=0, high=len(contacts)-1)
        return contacts[index]


def create_contact():
    """Prompts the user for required details and creates an appropriate
    contact"""

    # Asking user for input
    fname = ask_text("Enter first name(Required): ", True)
    lname = ask_text("Enter last name: ")
    ph_personal = ask_phone_no("Enter personal phone no.(Required): ", True)
    ph_work = ask_phone_no("Enter work phone no.: ")
    ph_home = ask_phone_no("Enter home phone no.:")
    email = ask_email("Enter email: ")
    address = ask_text("Enter address: ")

    # Creating and storing the contact into database
    cid = dmgr.get_new_id()
    current_time = datetime.now()
    contact = Contact(cid, fname, lname, current_time,
                      ph_personal, ph_work, ph_home, email, address)

    if dmgr.create_contact(contact):
        print("Contact created successfully")
    else:
        print("Couldn't create the contact")
        print("No two contacts can have following details same")
        print(
                "Personal phone no."
                "Work phone no."
                "Home phone no.",
                sep='\n'
            )


def view_contact():
    """Prompts the user to select a contact by name, then displays
    the full information of the contact"""

    contact = _select_contact()
    if not contact: 
        return
    tb_data = format_for_display([contact], full=True)
    display_full(tb_data[0])


def edit_contact():
    """Prompts the user to update an existing contact"""

    contact = _select_contact()

    if not contact:
        return

    # Getting the new details for the contact
    print("Enter the new details for this contact"
          " or just press <Enter> to leave the defaults")
    fname = ask_text("Enter first name(Required): ",
                     default=contact.first_name)
    lname = ask_text("Enter last name: ", default=contact.last_name)
    ph_personal = ask_phone_no(
        "Enter personal phone no.(Required): ", default=contact.phone_personal)
    ph_work = ask_phone_no("Enter work phone no.: ",
                           default=contact.phone_work)
    ph_home = ask_phone_no("Enter home phone no.:", default=contact.phone_home)
    email = ask_email("Enter email: ", default=contact.email)
    address = ask_text("Enter your address: ", default=contact.address)

    # Updating the contact
    new_contact = Contact(contact.db_id, fname, lname, contact.date_added,
                          ph_personal, ph_work, ph_home, email, address)
    if dmgr.update_contact(new_contact):
        print("Contact updated successfully")


def print_contacts_by_name():
    """Prompts the user to search for a matching name and shows
    the related contacts"""

    search_name = ask_text("Enter the name: ", True)
    data = dmgr.fetch_by_name(search_name)
    tb_data = format_for_display(data)
    display_table(tb_data)
    print(f"\nFound {len(data)} contacts")


def print_contacts_by_phone():
    """Prompts the user to enter a phone number and the shows all the matching
    contacts with that number
    """

    search_phone = ask_text("Enter phone number: ", True)
    data = dmgr.fetch_by_phone_no(search_phone)
    tb_data = format_for_display(data)
    display_table(tb_data)
    print(f"\nFound {len(data)} contacts")


def print_available_contacts():
    """Prints all the available contacts"""

    total_contacts = dmgr.get_contact_count()
    n = ask_int("Enter the number of contacts: ",
                low=0, high=total_contacts)
    data = dmgr.fetch_contacts(n)
    tb_data = format_for_display(data)
    display_table(tb_data)
    print(f"Showing {len(data)} contacts out of {total_contacts}.")


def _select_group():
    """Prompts the user to select a group
    from the given options"""

    groups = dmgr.fetch_groups()
    
    print(f"Found {len(groups)} groups")
    if groups:
        tb_data = tabulate(
                [group[1:] for group in groups],
                headers=["Group name"],
                tablefmt="mixed_grid",
                showindex=True
            )
        print(tb_data)
        i = ask_int("Select group no.: ", low=0, high=len(tb_data)-1)
        return groups[i]


def show_groups():
    """Shows the groups created by the user"""

    groups = dmgr.fetch_groups()

    if groups:
        tb_data = tabulate(
                [group[1:] for group in groups],
                headers=["Group name"],
                tablefmt="mixed_grid",
                showindex=True
            )
        print(tb_data)
    print(f"Found {len(groups)} groups")


def create_group():
    """Prompts the user to enter a group name
    and creates a group with that name into the 
    database"""

    name = ask_text("Enter a group name: ", required=True)
    dmgr.create_group(name)


def add_contact_to_group():
    """Prompts the user to select a group and
    a contact and adds the contact to that group
    in the database"""

    g_info = _select_group()
    if not g_info:
        return
    g_id = g_info[0]

    contact = _select_contact()
    if not contact:
        return

    if dmgr.add_contacts_to_group(g_id, contact.db_id):
        print("Contact added successfully")
    else:
        print("Contact already present in the group")


def remove_contact_from_group():
    """Prompts the user to select a group and then 
    prompts to chosse from the available contacts to
    remove"""

    g_info = _select_group()
    if not g_info:
        return
    g_id = g_info[0]
    contacts = dmgr.get_contacts_from_group(g_id)
    tb_data = format_for_display(contacts)
    display_table(tb_data)
    index = ask_int("Choose the contact to remove: ",
                    low=0, high=len(contacts)-1)
    contact = contacts[index]
    dmgr.remove_contacts_from_group(g_id, contact.db_id)


def view_group():
    """Lists all the contacts from a chosen group"""

    g_info = _select_group()
    if not g_info:
        return
    g_id, group = g_info
    print("Group:", group)
    contacts = dmgr.get_contacts_from_group(g_id)
    tb_data = format_for_display(contacts)
    display_table(tb_data)
    print(f"Found {len(contacts)} contacts.")


def delete_group():
    """Prompts the user to select a group and then
    deletes it from the database (but doesn't deletes
    the associated contacts)"""

    g_info = _select_group()
    if not g_info:
        return
    g_id = g_info[0]
    dmgr.delete_group(g_id)
    print("Group deleted")


def delete_contact():
    """Prompts the user to select a contact and then deletes
    it from the database, also deletes the associated phone numbers
    and removes it from any of the groups"""

    contact = _select_contact()
    if not contact:
        return
    dmgr.delete_contact(contact)
    print("Contact deleted.")


def quit_program():
    """Exits the application"""
    exit(0)


# Registering all the options
OPTIONS["Create new contact"] = create_contact
OPTIONS["List contacts"] = print_available_contacts
OPTIONS["Search contacts by name"] = print_contacts_by_name
OPTIONS["Search contacts by phone number"] = print_contacts_by_phone
OPTIONS["View a contact's info"] = view_contact
OPTIONS["Edit an existing contact"] = edit_contact
OPTIONS["Create a group"] = create_group
OPTIONS["Show groups"] = show_groups
OPTIONS["Add contacts to a group"] = add_contact_to_group
OPTIONS["Remove contact from a group"] = remove_contact_from_group
OPTIONS["View contact from a group"] = view_group
OPTIONS["Delete a group"] = delete_group
OPTIONS["Delete a contact"] = delete_contact
OPTIONS["Exit"] = quit_program
