from database.session import SessionLocal
from sqlalchemy.orm import joinedload

from models.user import User
from controllers.session import UserSession
from models.departement import Departement  # noqa: F401
from utils.password import verify_password
from views.authentication import prompt_login, show_login_error


class AuthenticationController:

    def authenticate(self, email: str, password: str):
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

    def login(self):
        user = None
        while not user:
            email, password = prompt_login()
            user = self.authenticate(email, password)

            if not user:
                show_login_error()

        return UserSession(user)
