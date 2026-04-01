from sqlalchemy.orm import joinedload

from models.user import User
from database.session import SessionLocal
from utils.permissions import permission_required
from utils.password import hash_password

from views.menu import show_menu
from views.utils import Utils
import views.user as user_view


class UserController:
    def __init__(self, user_session):
        self.user_session = user_session
        self.session = None

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @permission_required("can_create_user")
    def create_user(self, data):
        try:
            user = User(
                name=data["name"],
                firstname=data["firstname"],
                email=data["email"],
                phone=data["phone"],
                password=hash_password(data["password"]),
                departement_id=data["departement_id"],
            )

            self.session.add(user)
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

    @permission_required("can_read_user")
    def get_users(self):
        users = self.session.query(User).options(joinedload(User.departement)).all()
        return users

    @permission_required("can_read_user")
    def get_user_by_id(self, user_id):
        user = self.session.query(User).filter_by(id=user_id).first()

        if not user:
            raise ValueError

        return user

    @permission_required("can_modify_user")
    def update_user(self, user, data):
        try:
            if (user.departement_id != data["departement_id"] and user.clients):
                raise Exception

            user.name = data["name"]
            user.firstname = data["firstname"]
            user.email = data["email"]
            user.phone = data["phone"]
            user.departement_id = data["departement_id"]

            if data.get("password"):
                user.password = hash_password(data["password"])

            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

    @permission_required("can_delete_user")
    def delete_user(self, user):
        try:
            if user.clients:
                raise Exception

            self.session.delete(user)
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

    def get_options(self):
        options = []

        if self.user_session.has_permission("can_read_user"):
            options.append(("1", "Voir la liste des utilisateurs"))

        if self.user_session.has_permission("can_read_user"):
            options.append(("2", "Voir les détails d'un utilisateur"))

        if self.user_session.has_permission("can_create_user"):
            options.append(("3", "Ajouter un utilisateur"))

        if self.user_session.has_permission("can_modify_user"):
            options.append(("4", "Modifier un utilisateur"))

        if self.user_session.has_permission("can_delete_user"):
            options.append(("5", "Supprimer un utilisateur"))

        options.append(("0", "Retour"))
        return options

    def user_menu(self):
        while True:
            options = self.get_options()
            choice = show_menu(self.user_session, options)

            match choice:
                case "1":
                    self.list_users_action()
                case "2":
                    self.show_user_action()
                case "3":
                    self.create_user_action()
                case "4":
                    self.update_user_action()
                case "5":
                    self.delete_user_action()
                case "0":
                    break

    def create_user_action(self):
        try:
            data = user_view.prompt_create_user()
            self.create_user(data)
            user_view.show_user_creation_success()

        except PermissionError:
            Utils.show_permission_error()
        except Exception:
            user_view.show_user_creation_error()

    def list_users_action(self):
        try:
            users = self.get_users()
            user_view.show_users(users)

        except PermissionError:
            Utils.show_permission_error()
        except Exception:
            user_view.show_no_user_found()

    def show_user_action(self):
        try:
            user_id = user_view.prompt_user_id()
            user = self.get_user_by_id(user_id)
            user_view.show_user_detail(user)

        except PermissionError:
            Utils.show_permission_error()
        except Exception:
            user_view.show_user_not_found()

    def update_user_action(self):
        try:
            user_id = user_view.prompt_user_id()
            user = self.get_user_by_id(user_id)

            data = user_view.prompt_update_user(user)
            self.update_user(user, data)
            user_view.show_user_modification_success()

        except PermissionError:
            Utils.show_permission_error()
        except ValueError:
            user_view.show_user_not_found()
        except Exception:
            user_view.show_user_modification_error()

    def delete_user_action(self):
        try:
            user_id = user_view.prompt_user_id()
            user = self.get_user_by_id(user_id)

            if not user_view.confirm_user_deletion(user):
                user_view.show_user_deletion_cancel()
                return

            self.delete_user(user)
            user_view.show_user_deletion_success()

        except PermissionError:
            Utils.show_permission_error()
        except ValueError:
            user_view.show_user_not_found()
        except Exception:
            user_view.show_user_deletion_error()
