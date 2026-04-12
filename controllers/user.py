from sqlalchemy.orm import joinedload

from models.user import User
from database.session import SessionLocal
from utils.permissions import permission_required
from utils.password import hash_password

from views.utils import Utils
from views.user import UserView


class UserController:
    def __init__(self, user_session):
        self.user_session = user_session
        self.session = None
        self.view = UserView()

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @permission_required("can_create_user")
    def create_user(self):
        try:
            data = self.view.prompt_create_user()

            data["password"] = hash_password(data["password"])
            user = User(**data)

            self.session.add(user)
            self.session.commit()
            self.view.show_user_creation_success()

        except Exception:
            self.session.rollback()
            self.view.show_user_creation_error()

    @permission_required("can_read_user")
    def list_users(self):
        try:
            users = self.session.query(User).options(joinedload(User.departement)).all()

            if not users:
                self.view.show_no_user_found()
                return

            self.view.show_users(users)

        except Exception:
            self.view.show_no_user_found()

    @permission_required("can_read_user")
    def show_user(self):
        try:
            user_id = self.view.prompt_user_id()
            user = self.session.query(User).filter_by(id=user_id).first()

            if not user:
                raise ValueError

            self.view.show_user_detail(user)

        except ValueError:
            self.view.show_user_not_found()
        except Exception:
            self.view.show_user_not_found()

    @permission_required("can_modify_user")
    def update_user(self):
        try:
            user_id = self.view.prompt_user_id()
            user = self.session.query(User).filter_by(id=user_id).first()

            if not user:
                raise ValueError

            data = self.view.prompt_update_user(user)

            if user.departement_id != data["departement_id"] and user.clients:
                raise Exception

            user.name = data["name"]
            user.firstname = data["firstname"]
            user.email = data["email"]
            user.phone = data["phone"]
            user.departement_id = data["departement_id"]

            if data.get("password"):
                user.password = hash_password(data["password"])

            self.session.commit()
            self.view.show_user_modification_success()

        except ValueError:
            self.view.show_user_not_found()
        except Exception:
            self.session.rollback()
            self.view.show_user_modification_error()

    @permission_required("can_delete_user")
    def delete_user(self):
        try:
            user_id = self.view.prompt_user_id()
            user = self.session.query(User).filter_by(id=user_id).first()

            if not user:
                raise ValueError
            if not self.view.confirm_user_deletion(user):
                self.view.show_user_deletion_cancel()
                return
            if user.clients:
                raise Exception

            self.session.delete(user)
            self.session.commit()
            self.view.show_user_deletion_success()

        except ValueError:
            self.view.show_user_not_found()
        except Exception:
            self.session.rollback()
            self.view.show_user_deletion_error()

    def user_menu(self):
        while True:
            choice = self.view.user_options(self.user_session)

            try:
                match choice:
                    case "1":
                        self.list_users()
                    case "2":
                        self.show_user()
                    case "3":
                        self.create_user()
                    case "4":
                        self.update_user()
                    case "5":
                        self.delete_user()
                    case "0":
                        break

            except PermissionError:
                Utils.show_permission_error()
