from models.client import Client
from utils.permissions import permission_required


class ClientController:

    def __init__(self, user_session, session):
        self.user_session = user_session
        self.session = session

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

    @permission_required("can_modify_client")
    def update_client(self, client_id, data):
        try:
            client = self.session.query(Client).filter_by(id=client_id).first()

            if not client:
                raise ValueError

            client.full_name = data["full_name"]
            client.email = data["email"]
            client.phone = data["phone"]
            client.company_name = data["company_name"]
            client.information = data["information"]

            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

    @permission_required("can_read_client")
    def get_client_by_id(self, client_id):
        return self.session.query(Client).filter_by(id=client_id).first()
