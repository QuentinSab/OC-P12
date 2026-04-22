from database.session import SessionLocal
from models.user import User
from models.departement import Departement
from models.client import Client # noqa: F401 E261
from models.event import Event # noqa: F401 E261
from utils.password import hash_password

session = SessionLocal()

gestion = Departement(
    id=1,
    name="GESTION",

    can_create_user=True,
    can_read_user=True,
    can_modify_user=True,
    can_delete_user=True,

    can_create_client=False,
    can_read_client=True,
    can_modify_client=False,
    can_delete_client=False,

    can_create_contract=True,
    can_read_contract=True,
    can_modify_contract=True,
    can_delete_contract=False,

    can_create_event=False,
    can_read_event=True,
    can_modify_event=True,
    can_delete_event=False,
)

commercial = Departement(
    id=2,
    name="COMMERCIAL",

    can_create_user=False,
    can_read_user=True,
    can_modify_user=False,
    can_delete_user=False,

    can_create_client=True,
    can_read_client=True,
    can_modify_client=True,
    can_delete_client=False,

    can_create_contract=False,
    can_read_contract=True,
    can_modify_contract=True,
    can_delete_contract=False,

    can_create_event=True,
    can_read_event=True,
    can_modify_event=False,
    can_delete_event=False,
)

support = Departement(
    id=3,
    name="SUPPORT",

    can_create_user=False,
    can_read_user=True,
    can_modify_user=False,
    can_delete_user=False,

    can_create_client=False,
    can_read_client=False,
    can_modify_client=True,
    can_delete_client=False,

    can_create_contract=False,
    can_read_contract=True,
    can_modify_contract=False,
    can_delete_contract=False,

    can_create_event=False,
    can_read_event=True,
    can_modify_event=True,
    can_delete_event=False,
)

session.add_all([gestion, commercial, support])
session.commit()

user = User(
    name="user_name",
    firstname="user_firstname",
    email="user@mail.com",
    phone="user_phone",
    password=hash_password("password"),
    departement_id=1
)

session.add(user)
session.commit()
session.close()

print("Données initialisées.")
