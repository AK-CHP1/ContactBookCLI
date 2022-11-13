import datetime
import sqlite3
import pytest

from .context import cbook
from cbook.datamanager import DataManager, SCHEMA, Contact


@pytest.fixture(autouse=True)
def mock_connection(monkeypatch, dummy_contacts):
    conn = sqlite3.connect(
        ":memory:", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    phone_numbers = [
        (c.db_id, c.phone_personal, c.phone_work, c.phone_home) for c in dummy_contacts
    ]
    contact_info = [
        (c.db_id, c.first_name, c.last_name, c.email, c.address, c.date_added)
        for c in dummy_contacts
    ]

    query = """INSERT INTO Contacts(id, first_name, last_name, email, address, date_added)
    VALUES(?, ?, ?, ?, ?, ?)"""
    cur.executemany(query, contact_info)
    query = """INSERT INTO Phone_numbers(c_id, personal, work, home)
    VALUES(?, ?, ?, ?)"""
    cur.executemany(query, phone_numbers)
    query = "INSERT INTO Groups(name) VALUES('family'), ('servants')"
    cur.execute(query)

    group_members = [(1, 1), (1, 4), (1, 7), (2, 12), (2, 10)]
    query = "INSERT INTO Group_members VALUES(?, ?)"
    cur.executemany(query, group_members)
    conn.commit()
    monkeypatch.setattr(
        cbook.datamanager.sqlite3, "connect", lambda *args, **kwargs: conn
    )


def test_get_new_id():
    mgr = DataManager()
    new_id = mgr.get_new_id()
    # The fixture moxk database has 30 contact records
    # So 31 should be the next id
    assert new_id == 31


def test_fetch_by_name():
    mgr = DataManager()
    assert mgr.fetch_by_name("Aayushman") == [
        Contact(
            db_id=2,
            first_name="Aayushman",
            last_name="Gupta",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768192),
            phone_personal="+139944532028",
            phone_work="+845351532923",
            phone_home="+527326624931",
            email="asdf2s@s.cc",
            address="Boring road",
        ),
        Contact(
            db_id=1,
            first_name="Aayushman",
            last_name="Kumar",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768149),
            phone_personal="+633347347957",
            phone_work="+894107995871",
            phone_home="81999863748",
            email="adf@xx.com",
            address="Mohan nagar",
        ),
        Contact(
            db_id=3,
            first_name="Aayushman",
            last_name="Yadav",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768222),
            phone_personal="+989374294952",
            phone_work="+438791346098",
            phone_home="+677578651270",
            email="clock@main.py",
            address="Bus stand",
        ),
    ]
    assert mgr.fetch_by_name("Hemant") == [
        Contact(
            db_id=4,
            first_name="Hemant",
            last_name="Kumar",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768237),
            phone_personal="+855087558021",
            phone_work="+774513224102",
            phone_home="+303970699565",
            email=None,
            address=None,
        ),
        Contact(
            db_id=5,
            first_name="Hemant",
            last_name="Sharma",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768267),
            phone_personal="+361763952441",
            phone_work="31606219484",
            phone_home="+723073860281",
            email=None,
            address=None,
        ),
        Contact(
            db_id=6,
            first_name="Hemant",
            last_name="Yadav",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768282),
            phone_personal="20915283486",
            phone_work="+980401256522",
            phone_home="+763256536527",
            email=None,
            address=None,
        ),
    ]
    assert mgr.fetch_by_name("Neha") == [
        Contact(
            db_id=12,
            first_name="Neha",
            last_name="Gupta",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768376),
            phone_personal="+565863716953",
            phone_work="+219037370698",
            phone_home="+320540603165",
            email=None,
            address=None,
        ),
        Contact(
            db_id=11,
            first_name="Neha",
            last_name="Kumari",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768360),
            phone_personal="+826563004656",
            phone_work="+994976425718",
            phone_home="+562810359287",
            email=None,
            address=None,
        ),
        Contact(
            db_id=13,
            first_name="Neha",
            last_name="Sharma",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768391),
            phone_personal="+559251065028",
            phone_work="+441666907077",
            phone_home="+948832615961",
            email=None,
            address=None,
        ),
        Contact(
            db_id=14,
            first_name="Neha",
            last_name="Yadav",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768406),
            phone_personal="+534134297431",
            phone_work="+827086346467",
            phone_home="+455806456664",
            email=None,
            address=None,
        ),
    ]
    assert mgr.fetch_by_name("Kumari") == [
        Contact(
            db_id=11,
            first_name="Neha",
            last_name="Kumari",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768360),
            phone_personal="+826563004656",
            phone_work="+994976425718",
            phone_home="+562810359287",
            email=None,
            address=None,
        )
    ]
    assert mgr.fetch_by_name("Reshma") == []


def test_get_contact_count():
    mgr = DataManager()
    mgr.get_contact_count() == 30


def test_fetch_by_phone_no_unique():
    mgr = DataManager()
    assert mgr.fetch_by_phone_no("+808831891248") == [
        Contact(
            db_id=10,
            first_name="Kunal",
            last_name="Yadav",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768345),
            phone_personal="+702288195975",
            phone_work="+808831891248",
            phone_home="+335815989437",
            email=None,
            address=None,
        )
    ]
    assert mgr.fetch_by_phone_no("+826563004656") == [
        Contact(
            db_id=11,
            first_name="Neha",
            last_name="Kumari",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768360),
            phone_personal="+826563004656",
            phone_work="+994976425718",
            phone_home="+562810359287",
            email=None,
            address=None,
        )
    ]
    assert mgr.fetch_by_phone_no("+763256536527") == [
        Contact(
            db_id=6,
            first_name="Hemant",
            last_name="Yadav",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768282),
            phone_personal="20915283486",
            phone_work="+980401256522",
            phone_home="+763256536527",
            email=None,
            address=None,
        )
    ]


def test_fetch_by_phone_multiple():
    # Tests for multiple contacts with same phone numbers
    mgr = DataManager()
    assert mgr.fetch_by_phone_no("+741923905397") == [
        Contact(
            db_id=15,
            first_name="Raju",
            last_name="Kumar",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768421),
            phone_personal="+741923905397",
            phone_work="+410175019672",
            phone_home="+978724714319",
            email=None,
            address=None,
        ),
        Contact(
            db_id=18,
            first_name="Raju",
            last_name="Yadav",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768466),
            phone_personal="+935655382084",
            phone_work="+741923905397",
            phone_home="+815262102012",
            email=None,
            address=None,
        ),
    ]

    assert mgr.fetch_by_phone_no("+863423061671") == [
        Contact(
            db_id=19,
            first_name="Prakash",
            last_name="Kumar",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768480),
            phone_personal="+525523099014",
            phone_work="+345194225580",
            phone_home="+863423061671",
            email=None,
            address=None,
        ),
        Contact(
            db_id=16,
            first_name="Raju",
            last_name="Gupta",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768436),
            phone_personal="+863423061671",
            phone_work="+820350746219",
            phone_home="+106098617743",
            email=None,
            address=None,
        ),
    ]


def test_fetch_by_phone_no_partial():
    # Tests for contacts with incomplete phone numbers
    mgr = DataManager()
    assert mgr.fetch_by_phone_no("192390") == [
        Contact(
            db_id=15,
            first_name="Raju",
            last_name="Kumar",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768421),
            phone_personal="+741923905397",
            phone_work="+410175019672",
            phone_home="+978724714319",
            email=None,
            address=None,
        ),
        Contact(
            db_id=18,
            first_name="Raju",
            last_name="Yadav",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768466),
            phone_personal="+935655382084",
            phone_work="+741923905397",
            phone_home="+815262102012",
            email=None,
            address=None,
        ),
    ]


def test_create_contact():
    mgr = DataManager()
    init_count = mgr.get_contact_count()
    contact = Contact(
        init_count + 1, "Rahul", "Verma", datetime.datetime.now(), "+321894123572"
    )
    assert mgr.create_contact(contact)
    assert mgr.get_contact_count() == init_count + 1
    contact = Contact(
        init_count + 2,
        "Kunal",
        "Verma",
        datetime.datetime.now(),
        "+321894123372",
        "+321894123572",
    )
    assert mgr.create_contact(contact)
    assert mgr.get_contact_count() == init_count + 2


def test_update_contact():
    mgr = DataManager()
    contact = Contact(
        db_id=20,
        first_name="Prakash",
        last_name="Gupta",
        date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768495),
        phone_personal="+688532624571",
        phone_work="+648202864525",
        phone_home="+720360101603",
        email="parkash@gmail.com",
        address=None,
    )
    assert mgr.update_contact(contact)

    # Failing phone no. length constraint
    contact = Contact(
        db_id=20,
        first_name="Prakash",
        last_name="Gupta",
        date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768495),
        phone_personal="+688532624571",
        phone_work="+648202864525",
        phone_home="+720360101603",
        email=None,
        address=None,
    )
    assert mgr.update_contact(contact)


def test_fetch_contacts():
    mgr = DataManager()
    assert mgr.fetch_contacts() == [
        Contact(
            db_id=2,
            first_name="Aayushman",
            last_name="Gupta",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768192),
            phone_personal="+139944532028",
            phone_work="+845351532923",
            phone_home="+527326624931",
            email="asdf2s@s.cc",
            address="Boring road",
        ),
        Contact(
            db_id=1,
            first_name="Aayushman",
            last_name="Kumar",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768149),
            phone_personal="+633347347957",
            phone_work="+894107995871",
            phone_home="81999863748",
            email="adf@xx.com",
            address="Mohan nagar",
        ),
        Contact(
            db_id=3,
            first_name="Aayushman",
            last_name="Yadav",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768222),
            phone_personal="+989374294952",
            phone_work="+438791346098",
            phone_home="+677578651270",
            email="clock@main.py",
            address="Bus stand",
        ),
        Contact(
            db_id=4,
            first_name="Hemant",
            last_name="Kumar",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768237),
            phone_personal="+855087558021",
            phone_work="+774513224102",
            phone_home="+303970699565",
            email=None,
            address=None,
        ),
        Contact(
            db_id=5,
            first_name="Hemant",
            last_name="Sharma",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768267),
            phone_personal="+361763952441",
            phone_work="31606219484",
            phone_home="+723073860281",
            email=None,
            address=None,
        ),
        Contact(
            db_id=6,
            first_name="Hemant",
            last_name="Yadav",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768282),
            phone_personal="20915283486",
            phone_work="+980401256522",
            phone_home="+763256536527",
            email=None,
            address=None,
        ),
        Contact(
            db_id=8,
            first_name="Kunal",
            last_name="Gupta",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768313),
            phone_personal="+617719886100",
            phone_work="+388958212153",
            phone_home="+754020906463",
            email=None,
            address=None,
        ),
        Contact(
            db_id=7,
            first_name="Kunal",
            last_name="Kumar",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768297),
            phone_personal="+806381926645",
            phone_work="+589945314183",
            phone_home="+848470781181",
            email=None,
            address=None,
        ),
        Contact(
            db_id=9,
            first_name="Kunal",
            last_name="Sharma",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768329),
            phone_personal="+844163312809",
            phone_work="+465358830965",
            phone_home="+120132815699",
            email=None,
            address=None,
        ),
        Contact(
            db_id=10,
            first_name="Kunal",
            last_name="Yadav",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768345),
            phone_personal="+702288195975",
            phone_work="+808831891248",
            phone_home="+335815989437",
            email=None,
            address=None,
        ),
    ]

    assert mgr.fetch_contacts(6) == [
        Contact(
            db_id=2,
            first_name="Aayushman",
            last_name="Gupta",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768192),
            phone_personal="+139944532028",
            phone_work="+845351532923",
            phone_home="+527326624931",
            email="asdf2s@s.cc",
            address="Boring road",
        ),
        Contact(
            db_id=1,
            first_name="Aayushman",
            last_name="Kumar",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768149),
            phone_personal="+633347347957",
            phone_work="+894107995871",
            phone_home="81999863748",
            email="adf@xx.com",
            address="Mohan nagar",
        ),
        Contact(
            db_id=3,
            first_name="Aayushman",
            last_name="Yadav",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768222),
            phone_personal="+989374294952",
            phone_work="+438791346098",
            phone_home="+677578651270",
            email="clock@main.py",
            address="Bus stand",
        ),
        Contact(
            db_id=4,
            first_name="Hemant",
            last_name="Kumar",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768237),
            phone_personal="+855087558021",
            phone_work="+774513224102",
            phone_home="+303970699565",
            email=None,
            address=None,
        ),
        Contact(
            db_id=5,
            first_name="Hemant",
            last_name="Sharma",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768267),
            phone_personal="+361763952441",
            phone_work="31606219484",
            phone_home="+723073860281",
            email=None,
            address=None,
        ),
        Contact(
            db_id=6,
            first_name="Hemant",
            last_name="Yadav",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768282),
            phone_personal="20915283486",
            phone_work="+980401256522",
            phone_home="+763256536527",
            email=None,
            address=None,
        ),
    ]


def test_fetch_groups():
    mgr = DataManager()
    assert mgr.fetch_groups() == [(1, "family"), (2, "servants")]


def test_add_contacts_to_group():
    mgr = DataManager()

    assert mgr.add_contacts_to_group(1, 22)
    assert mgr.add_contacts_to_group(2, 18)
    # Foreign key fails
    assert not mgr.add_contacts_to_group(3, 1)
    assert not mgr.add_contacts_to_group(1, 99)
    # Primary key fails
    assert not mgr.add_contacts_to_group(1, 1)
    assert not mgr.add_contacts_to_group(1, 4)
    assert not mgr.add_contacts_to_group(1, 22)


def test_get_contacts_from_group():
    mgr = DataManager()
    assert mgr.get_contacts_from_group(1) == [
        Contact(
            db_id=1,
            first_name="Aayushman",
            last_name="Kumar",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768149),
            phone_personal="+633347347957",
            phone_work="+894107995871",
            phone_home="81999863748",
            email="adf@xx.com",
            address="Mohan nagar",
        ),
        Contact(
            db_id=4,
            first_name="Hemant",
            last_name="Kumar",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768237),
            phone_personal="+855087558021",
            phone_work="+774513224102",
            phone_home="+303970699565",
            email=None,
            address=None,
        ),
        Contact(
            db_id=7,
            first_name="Kunal",
            last_name="Kumar",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768297),
            phone_personal="+806381926645",
            phone_work="+589945314183",
            phone_home="+848470781181",
            email=None,
            address=None,
        ),
    ]
    assert mgr.get_contacts_from_group(2) == [
        Contact(
            db_id=10,
            first_name="Kunal",
            last_name="Yadav",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768345),
            phone_personal="+702288195975",
            phone_work="+808831891248",
            phone_home="+335815989437",
            email=None,
            address=None,
        ),
        Contact(
            db_id=12,
            first_name="Neha",
            last_name="Gupta",
            date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768376),
            phone_personal="+565863716953",
            phone_work="+219037370698",
            phone_home="+320540603165",
            email=None,
            address=None,
        ),
    ]
