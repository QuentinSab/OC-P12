from models.client import Client
from database.session import SessionLocal
from utils.permissions import permission_required

from views.utils import Utils
from views.client import ClientView


class ClientController:
    def __init__(self, user_session):
        self.user_session = user_session
        self.session = None
        self.view = ClientView()

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @permission_required("can_create_client")
    def create_client(self):
        try:
            data = self.view.prompt_create_client()

            data["contact_id"] = self.user_session.user.id
            client = Client(**data)

            self.session.add(client)
            self.session.commit()
            self.view.show_client_creation_success()

        except Exception:
            self.session.rollback()
            self.view.show_client_creation_error()

    @permission_required("can_read_client")
    def list_clients(self):
        try:
            clients = self.session.query(Client).all()

            if not clients:
                raise ValueError

            self.view.show_clients(clients)

        except ValueError:
            self.view.show_no_client_found()
        except Exception:
            self.view.show_client_list_error()

    @permission_required("can_read_client")
    def show_client(self):
        try:
            client_id = self.view.prompt_client_id()
            client = self.session.query(Client).filter_by(id=client_id).first()

            if not client:
                raise ValueError

            self.view.show_client_detail(client)

        except ValueError:
            self.view.show_client_not_found()
        except Exception:
            self.view.show_client_detail_error()

    @permission_required("can_modify_client")
    def update_client(self):
        try:
            client_id = self.view.prompt_client_id()
            client = self.session.query(Client).filter_by(id=client_id).first()

            if not client:
                raise ValueError
            if client.contact_id != self.user_session.user.id:
                self.view.show_not_client_contact_error()
                return

            data = self.view.prompt_update_client(client)

            client.full_name = data["full_name"]
            client.email = data["email"]
            client.phone = data["phone"]
            client.company_name = data["company_name"]
            client.information = data["information"]

            self.session.commit()
            self.view.show_client_modification_success()

        except ValueError:
            self.view.show_client_not_found()
        except Exception:
            self.session.rollback()
            self.view.show_client_modification_error()

    def client_menu(self):
        while True:
            choice = self.view.client_options(self.user_session)

            try:
                match choice:
                    case "1":
                        self.list_clients()
                    case "2":
                        self.show_client()
                    case "3":
                        self.create_client()
                    case "4":
                        self.update_client()
                    case "0":
                        break

            except PermissionError:
                Utils.show_permission_error()
