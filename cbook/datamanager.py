from datetime import datetime
import sqlite3
from pathlib import Path
from typing import List, NamedTuple, Tuple, Union, Optional

DATA_PATH = Path.home() / ".cbook_contacts.sqlite"


class Contact(NamedTuple):
    """Represents the contact data which is stored into the
    database"""

    db_id: int
    first_name: str
    last_name: str
    date_added: datetime
    phone_personal: str
    phone_work: Optional[str] = None
    phone_home: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


SCHEMA = """
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS Contacts(
        id INTEGER PRIMARY KEY,
        first_name VARCHAR(15) NOT NULL,
        last_name VARCHAR(15),
        email VARCHAR(40),
        address VARCHAR(50),
        date_added TIMESTAMP NOT NULL
    );
    CREATE TABLE IF NOT EXISTS Phone_numbers(
        c_id INTEGER,
        personal VARCHAR(15) UNIQUE NOT NULL,
        work VARCHAR(15) UNIQUE,
        home VARCHAR(15) UNIQUE,
        FOREIGN KEY(c_id) REFERENCES Contacts(id)
            ON DELETE RESTRICT,
        PRIMARY KEY(personal, work, home)
    );
    
    CREATE TABLE IF NOT EXISTS Groups(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Group_members(
        g_id INTEGER NOT NULL,
        c_id INTEGER NOT NULL,
        FOREIGN KEY(g_id) REFERENCES Groups(id) ON DELETE RESTRICT,
        FOREIGN KEY(c_id) REFERENCES Contacts(id) ON DELETE RESTRICT,
        PRIMARY KEY(g_id, c_id)
    );
"""


class DataManager:
    """This class is responsible for maintaining the sqlite database
    used by the application"""

    def __init__(self):

        self.__conn = sqlite3.connect(
            DATA_PATH,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = self.__conn.cursor()
        cur.executescript(SCHEMA)

    def fetch_by_name(self, name: str) -> List[Contact]:
        """Fetches and returns all the contacts from the database whose
        name matches `name` (i.e. first_name + last_name)

        :param name: name to search for
        :type name: str

        :returns: List of found contacts
        :rtype: List[Contact]
        """

        cur = self.__conn.cursor()
        query = """
            SELECT id, first_name, last_name, date_added, personal, work, home, email, address
            FROM Contacts JOIN Phone_numbers ON Contacts.id = Phone_numbers.c_id
            WHERE first_name LIKE ? OR last_name LIKE ?
            ORDER BY first_name, last_name;
        """
        param = f"%{name}%"
        cur.execute(query, (param, param))
        data = [Contact(*row) for row in cur]
        return data

    def fetch_by_phone_no(self, phone: str) -> List[Contact]:
        """Fetches and returns all the contacts with either
        phone_no1 or phone_no2
        equal to `phone` from the database

        :param phone: Phone no. to search for
        :type phone: str
        .. No math is to be done with phone numbers

        :returns: List of found contacts
        :rtype: List[Contact]
        """

        cur = self.__conn.cursor()
        query = """
            SELECT id, first_name, last_name, date_added, personal, work, home, email, address
            FROM Contacts JOIN Phone_numbers ON Contacts.id = Phone_numbers.c_id
            WHERE personal LIKE ? OR work LIKE ? OR home LIKE ?
            ORDER BY first_name, last_name;
        """
        param = f"%{phone}%"
        cur.execute(query, (param, param, param))
        data = [Contact(*row) for row in cur]
        return data

    def fetch_contacts(self, limit: int = 10) -> List[Contact]:
        """Fetches and returns a maximum of `limit` contacts in sorted order

        :param limit: Maximum number of contacts to fetch
        :type limit: int

        :returns: List of contacts found
        :rtype: List[Contact]
        """

        cur = self.__conn.cursor()
        query = """
                SELECT id, first_name, last_name, date_added, personal, work, home, email, address
                FROM Contacts JOIN Phone_numbers ON Contacts.id = Phone_numbers.c_id
                ORDER BY first_name, last_name LIMIT ?
            """
        cur.execute(query, (limit,))
        contacts = [Contact(*row) for row in cur]
        return contacts

    def get_contact_count(self) -> int:
        """Returns the total number of contacts present in the database

        :returns: no. of contacts
        :rtype: int
        """
        cur = self.__conn.cursor()
        query = "SELECT COUNT(*) FROM Contacts"
        cur.execute(query)
        data = cur.fetchone()
        if data:
            return data[0]
        return 0

    def create_contact(self, contact: Contact) -> bool:
        """Creates and stores a new contact into the database, returns 
        `True` if contact is created successfully `False` otherwise

        :param contact: The contact to create
        :type contact: Contact

        :returns: Status of creation
        :rtype: bool
        """
        try:
            cur = self.__conn.cursor()
            query = "INSERT INTO Contacts VALUES(?, ?, ?, ?, ?, ?)"
            params = (contact.db_id, contact.first_name, contact.last_name,
                      contact.email, contact.address, contact.date_added)
            cur.execute(query, params)
            query = "INSERT INTO Phone_numbers VALUES(?, ?, ?, ?)"
            params = (contact.db_id, contact.phone_personal,
                      contact.phone_work, contact.phone_home)
            cur.execute(query, params)
            return True
        except sqlite3.Error:
            return False

    def update_contact(self, contact: Contact) -> bool:
        """Updates the contact in the database with new
        contact details in `contact`
         where `contact.db_id` matches the contact id in the database, returns
        `True` if updates successfully `False` otherwise

        :param cid: The id of the contact to be updated
        :type cid: bool

        :returns: True if updates successfully
        :rtype: bool
        """

        try:
            cur = self.__conn.cursor()
            # Updating the Contacts table
            query = """UPDATE Contacts
                    SET first_name = ?, last_name = ?, email = ?, address = ?
                    WHERE id = ?"""
            params = (contact.first_name, contact.last_name,
                      contact.email, contact.address, contact.db_id)
            cur.execute(query, params)

            # Updating the Phone_numbers table
            query = """UPDATE Phone_numbers
                    SET personal = ?, work = ?, home =?
                    WHERE c_id = ?"""
            params = (contact.phone_personal, contact.phone_work,
                      contact.phone_home, contact.db_id)
            cur.execute(query, params)
            return True
        except sqlite3.Error:
            return False

    def delete_contact(self, contact: Contact) -> None:
        """Deletes a given contact from the database"""

        cur = self.__conn.cursor()

        # Deleting the phone numbers from Phone_numbers table
        query = "DELETE FROM Phone_numbers WHERE c_id = ?"
        cur.execute(query, (contact.db_id, ))
        # Removing the user from all groups
        query = "DELETE FROM Group_members WHERE c_id = ?"
        cur.execute(query, (contact.db_id, ))
        # Deleting the actual contact
        query = "DELETE FROM Contacts WHERE id = ?"
        cur.execute(query, (contact.db_id, ))

    def get_new_id(self) -> int:
        """Returns a new id for the contact to use

        :returns: new id
        :rtype: int
        """
        cur = self.__conn.cursor()
        cur.execute("SELECT id FROM Contacts")
        data = cur.fetchall()
        # Select the last id from contact
        # Generate new id by adding 1 to it
        if data:
            new_id = data[-1][0] + 1
        else:
            new_id = 1
        return new_id

    def create_group(self, name: str) -> None:
        """Creates a group in the contact database

        :param name: Name of the group
        :type name: str

        :rtype: NoneType"""

        cur = self.__conn.cursor()
        query = "INSERT INTO Groups(name) VALUES(?)"
        cur.execute(query, (name,))

    def fetch_groups(self) -> List[Tuple[Union[int, str]]]:
        """Fetches and returns a list of groups in a database"""

        cur = self.__conn.cursor()
        query = "SELECT * FROM Groups"
        cur.execute(query)
        return cur.fetchall()

    def add_contacts_to_group(self, group_id: int, contact_id: int) -> bool:
        """Updates the Group members table, adds contacts with id `contact_id`
        to group with id `group_id`. Returns `True` if
        successful `False` otherwise

        :param group_id: Group ID
        :type group_id: int
        :param contact_id: Contact ID
        :type contact_id: int"""
        try:
            cur = self.__conn.cursor()
            query = "INSERT INTO Group_members VALUES(?, ?)"
            cur.execute(query, (group_id, contact_id))
            return True
        except sqlite3.Error:
            return False

    def remove_contacts_from_group(
            self, group_id: int, contact_id: int) -> None:
        """Removes a contact with id `contact_id` from group
        with id `group_id`"""

        cur = self.__conn.cursor()
        query = "DELETE FORM Group_members WHERE g_id = ? AND c_id = ?"
        cur.execute(query, (group_id, contact_id))

    def get_contacts_from_group(self, group_id: int) -> List[Contact]:
        """Fetches and returns all the contacts from group with id `group_id`

        :param group_id: The group_id from which to fetch contacts
        :type group_id: int
        :returns: List of present contacts
        :rtype: List[Contact]"""

        cur = self.__conn.cursor()
        query = """
            SELECT id, first_name, last_name, date_added, personal, work, home, email, address
            FROM Contacts JOIN Phone_numbers ON Contacts.id = Phone_numbers.c_id
            WHERE id IN (SELECT c_id FROM Group_members WHERE g_id = ?)
        """
        cur.execute(query, (group_id, ))
        contacts = [Contact(*row) for row in cur]
        return contacts

    def delete_group(self, group_id: int) -> None:
        """Deletes a group with id `group_id`"""

        cur = self.__conn.cursor()
        query1 = "DELETE FROM Group_members WHERE g_id = ?"
        query2 = "DELETE FROM Groups WHERE id = ?"
        cur.execute(query1, (group_id,))
        cur.execute(query2, (group_id,))

    def __del__(self):
        self.__conn.commit()
