from database.session import SessionLocal
from sqlalchemy.orm import joinedload

from models.user import User
from models.departement import Departement  # noqa: F401
from utils.password import verify_password


class AuthenticationController:

    @staticmethod
    def login(email: str, password: str):
        session = SessionLocal()

        user = (
            session.query(User)
            .options(joinedload(User.departement))
            .filter_by(email=email)
            .first()
        )

        session.close()

        if user and verify_password(password, user.password):
            return user

        return None
