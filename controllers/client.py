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
