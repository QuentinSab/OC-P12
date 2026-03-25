from models.client import Client


class ClientController:

    def __init__(self, user_session, session):
        self.user_session = user_session
        self.session = session

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
            return True

        except Exception:
            self.session.rollback()
            return False

    def get_clients(self):
        try:
            clients = self.session.query(Client).all()
            return clients

        except Exception:
            return []

    def update_client(self, client_id, data):
        try:
            client = self.session.query(Client).filter_by(id=client_id).first()

            if not client:
                return False

            client.full_name = data["full_name"]
            client.email = data["email"]
            client.phone = data["phone"]
            client.company_name = data["company_name"]
            client.information = data["information"]

            self.session.commit()

            return True

        except Exception:
            self.session.rollback()
            return False

    def get_client_by_id(self, client_id):
        return self.session.query(Client).filter_by(id=client_id).first()
