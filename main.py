from database.session import SessionLocal

from controllers.authentication import AuthenticationController
from controllers.session import UserSession
from controllers.client import ClientController
from controllers.menu import MenuController

from views.authentication import prompt_login, show_login_error, show_login_success
from views.menu import show_menu
import views.client as client_view


def main():
    while True:
        user = None

        # Authentication
        while not user:
            email, password = prompt_login()
            user = AuthenticationController.login(email, password)

            if not user:
                show_login_error()

        show_login_success()
        user_session = UserSession(user)
        menu_controller = MenuController(user_session)

        # Main menu
        while user_session.is_authenticated:

            options = menu_controller.get_main_menu()
            choice = show_menu(user_session, options)

            match choice:
                case "1":  # Client creation
                    session = SessionLocal()
                    client_controller = ClientController(user_session, session)

                    data = client_view.prompt_create_client()
                    success = client_controller.create_client(data)

                    if success:
                        client_view.show_client_creation_success()
                    else:
                        client_view.show_client_creation_error()

                    session.close()

                case "2":  # Clients list
                    session = SessionLocal()
                    client_controller = ClientController(user_session, session)

                    clients = client_controller.get_clients()
                    client_view.show_clients(clients)

                    session.close()

                case "3":  # Client update
                    session = SessionLocal()

                    client_controller = ClientController(user_session, session)

                    client_id = client_view.prompt_client_id()
                    client = client_controller.get_client_by_id(client_id)

                    if not client:
                        client_view.show_client_not_found()
                    else:
                        data = client_view.prompt_update_client(client)
                        success = client_controller.update_client(client_id, data)

                        if success:
                            client_view.show_client_modification_success()
                        else:
                            client_view.show_client_modification_error()

                    session.close()

                case "logout":
                    user_session.logout()
                    break


if __name__ == "__main__":
    main()
