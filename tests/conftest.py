import pytest
from .context import cbook
from cbook.datamanager import Contact
import datetime


@pytest.fixture
def dummy_contacts():
    contacts = [
        Contact(db_id=1, first_name='Aayushman', last_name='Kumar', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768149),
                phone_personal='+633347347957', phone_work='+894107995871', phone_home='81999863748', email='adf@xx.com', address='Mohan nagar'),
        Contact(db_id=2, first_name='Aayushman', last_name='Gupta', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768192),
                phone_personal='+139944532028', phone_work='+845351532923', phone_home='+527326624931', email='asdf2s@s.cc', address='Boring road'),
        Contact(db_id=3, first_name='Aayushman', last_name='Yadav', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768222),
                phone_personal='+989374294952', phone_work='+438791346098', phone_home='+677578651270', email='clock@main.py', address='Bus stand'),
        Contact(db_id=4, first_name='Hemant', last_name='Kumar', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768237),
                phone_personal='+855087558021', phone_work='+774513224102', phone_home='+303970699565', email=None, address=None),
        Contact(db_id=5, first_name='Hemant', last_name='Sharma', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768267),
                phone_personal='+361763952441', phone_work='31606219484', phone_home='+723073860281', email=None, address=None),
        Contact(db_id=6, first_name='Hemant', last_name='Yadav', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768282),
                phone_personal='20915283486', phone_work='+980401256522', phone_home='+763256536527', email=None, address=None),
        Contact(db_id=7, first_name='Kunal', last_name='Kumar', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768297),
                phone_personal='+806381926645', phone_work='+589945314183', phone_home='+848470781181', email=None, address=None),
        Contact(db_id=8, first_name='Kunal', last_name='Gupta', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768313),
                phone_personal='+617719886100', phone_work='+388958212153', phone_home='+754020906463', email=None, address=None),
        Contact(db_id=9, first_name='Kunal', last_name='Sharma', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768329),
                phone_personal='+844163312809', phone_work='+465358830965', phone_home='+120132815699', email=None, address=None),
        Contact(db_id=10, first_name='Kunal', last_name='Yadav', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768345),
                phone_personal='+702288195975', phone_work='+808831891248', phone_home='+335815989437', email=None, address=None),
        Contact(db_id=11, first_name='Neha', last_name='Kumari', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768360),
                phone_personal='+826563004656', phone_work='+994976425718', phone_home='+562810359287', email=None, address=None),
        Contact(db_id=12, first_name='Neha', last_name='Gupta', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768376),
                phone_personal='+565863716953', phone_work='+219037370698', phone_home='+320540603165', email=None, address=None),
        Contact(db_id=13, first_name='Neha', last_name='Sharma', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768391),
                phone_personal='+559251065028', phone_work='+441666907077', phone_home='+948832615961', email=None, address=None),
        Contact(db_id=14, first_name='Neha', last_name='Yadav', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768406),
                phone_personal='+534134297431', phone_work='+827086346467', phone_home='+455806456664', email=None, address=None),
        Contact(db_id=15, first_name='Raju', last_name='Kumar', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768421),
                phone_personal='+741923905397', phone_work='+410175019672', phone_home='+978724714319', email=None, address=None),
        Contact(db_id=16, first_name='Raju', last_name='Gupta', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768436),
                phone_personal='+863423061671', phone_work='+820350746219', phone_home='+106098617743', email=None, address=None),
        Contact(db_id=17, first_name='Raju', last_name='Sharma', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768451),
                phone_personal='+737734798870', phone_work='+128147792149', phone_home='+189437044707', email=None, address=None),
        Contact(db_id=18, first_name='Raju', last_name='Yadav', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768466),
                phone_personal='+935655382084', phone_work='+741923905397', phone_home='+815262102012', email=None, address=None),
        Contact(db_id=19, first_name='Prakash', last_name='Kumar', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768480),
                phone_personal='+525523099014', phone_work='+345194225580', phone_home='+863423061671', email=None, address=None),
        Contact(db_id=20, first_name='Prakash', last_name='Gupta', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768495),
                phone_personal='+688532624571', phone_work='+648202864525', phone_home='+720360101603', email=None, address=None),
        Contact(db_id=21, first_name='Prakash', last_name='Sharma', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768509),
                phone_personal='+195415237966', phone_work='+261265201364', phone_home='27102888955', email=None, address=None),
        Contact(db_id=22, first_name='Prakash', last_name='Yadav', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768531),
                phone_personal='+232352703805', phone_work='+614990337892', phone_home='+453378820359', email=None, address=None),
        Contact(db_id=23, first_name='Riya', last_name='Kumar', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768548),
                phone_personal='+390163754537', phone_work='+941803752209', phone_home='+399028666446', email=None, address=None),
        Contact(db_id=24, first_name='Riya', last_name='Gupta', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768563),
                phone_personal='+732711052267', phone_work='+678073557096', phone_home='+812974700165', email=None, address=None),
        Contact(db_id=25, first_name='Riya', last_name='Sharma', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768579),
                phone_personal='+430931315521', phone_work='+953963611419', phone_home='+575821153719', email=None, address=None),
        Contact(db_id=26, first_name='Riya', last_name='Yadav', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768594),
                phone_personal='+155209150184', phone_work='+866926198169', phone_home='+235749313068', email=None, address=None),
        Contact(db_id=27, first_name='Raju', last_name='Kumar', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768608),
                phone_personal='+538522025146', phone_work='+413168623692', phone_home='+618038517242', email=None, address=None),
        Contact(db_id=28, first_name='Raju', last_name='Gupta', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768623),
                phone_personal='+463139323987', phone_work='+905435935049', phone_home='+466798934595', email=None, address=None),
        Contact(db_id=29, first_name='Raju', last_name='Sharma', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768638),
                phone_personal='11486393352', phone_work='+605018235650', phone_home='+875966293289', email=None, address=None),
        Contact(db_id=30, first_name='Raju', last_name='Yadav', date_added=datetime.datetime(2022, 10, 23, 14, 44, 19, 768653),
                phone_personal='+373407716174', phone_work='+669097721795', phone_home='+890588447298', email=None, address=None)
    ]
    return contacts