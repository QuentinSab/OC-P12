from models.client import Client
from database.session import SessionLocal
from utils.permissions import permission_required

from views.menu import show_menu
from views.utils import Utils
import views.client as client_view


class ClientController:
    def __init__(self, user_session):
        self.user_session = user_session
        self.session = None

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @permission_required("can_create_client")
    def create_client(self, data):
        try:
            client = Client(
                full_name=data["full_name"],
                email=data["email"],
                phone=data["phone"],
                company_name=data["company_name"],
                information=data["information"],
                contact_id=self.user_session.user.id
            )

            self.session.add(client)
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

    @permission_required("can_read_client")
    def get_clients(self):
        clients = self.session.query(Client).all()
        return clients

    @permission_required("can_read_client")
    def get_client_by_id(self, client_id):
        client = self.session.query(Client).filter_by(id=client_id).first()

        if not client:
            raise ValueError

        return client

    @permission_required("can_modify_client")
    def update_client(self, client_id, data):
        try:
            client = self.session.query(Client).filter_by(id=client_id).first()

            if client.contact_id != self.user_session.user.id:
                raise PermissionError

            client.full_name = data["full_name"]
            client.email = data["email"]
            client.phone = data["phone"]
            client.company_name = data["company_name"]
            client.information = data["information"]

            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

    def get_options(self):
        options = []

        if self.user_session.has_permission("can_read_client"):
            options.append(("1", "Voir la liste des clients"))

        if self.user_session.has_permission("can_read_client"):
            options.append(("2", "Voir les détails d'un client"))

        if self.user_session.has_permission("can_create_client"):
            options.append(("3", "Ajouter un client"))

        if self.user_session.has_permission("can_modify_client"):
            options.append(("4", "Modifier un client"))

        options.append(("0", "Retour"))
        return options

    def client_menu(self):
        while True:
            options = self.get_options()
            choice = show_menu(self.user_session, options)

            match choice:
                case "1":
                    self.list_clients_action()
                case "2":
                    self.show_client_action()
                case "3":
                    self.create_client_action()
                case "4":
                    self.update_client_action()
                case "0":
                    break

    def create_client_action(self):
        try:
            data = client_view.prompt_create_client()
            self.create_client(data)
            client_view.show_client_creation_success()

        except PermissionError:
            Utils.show_permission_error()
        except Exception:
            client_view.show_client_creation_error()

    def list_clients_action(self):
        try:
            clients = self.get_clients()
            client_view.show_clients(clients)

        except PermissionError:
            Utils.show_permission_error()
        except Exception:
            client_view.show_no_client_found()

    def show_client_action(self):
        try:
            client_id = client_view.prompt_client_id()
            client = self.get_client_by_id(client_id)
            client_view.show_client_detail(client)

        except PermissionError:
            Utils.show_permission_error()
        except Exception:
            client_view.show_client_not_found()

    def update_client_action(self):
        try:
            client_id = client_view.prompt_client_id()
            client = self.get_client_by_id(client_id)

            data = client_view.prompt_update_client(client)
            self.update_client(client_id, data)
            client_view.show_client_modification_success()

        except PermissionError:
            Utils.show_permission_error()
        except ValueError:
            client_view.show_client_not_found()
        except Exception:
            client_view.show_client_modification_error()
