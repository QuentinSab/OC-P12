from database.session import SessionLocal
from models.user import User
from models.departement import Departement  # noqa: F401
from utils.password import hash_password

session = SessionLocal()

test_user = User(
    name="Dupont",
    firstname="Jeanne",
    email="jeanne.dupont@test.com",
    phone="0123456789",
    password=hash_password("secret123"),
    departement_id=2
)

session.add(test_user)
session.commit()

test_user_db = session.query(User).filter_by(email="jeanne.dupont@test.com").first()
print(test_user_db)

session.close()
