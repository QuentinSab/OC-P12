from database.session import SessionLocal

from controllers.authentication import AuthenticationController
from controllers.session import UserSession
from controllers.client import ClientController
from controllers.menu import MenuController

from views.authentication import prompt_login, show_login_error, show_login_success
from views.menu import show_menu
from views.client import prompt_create_client, show_client_creation_error, show_client_creation_success


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
                case "1":
                    session = SessionLocal()

                    client_controller = ClientController(user_session, session)

                    data = prompt_create_client()
                    success = client_controller.create_client(data)

                    if success:
                        show_client_creation_success()
                    else:
                        show_client_creation_error()

                    session.close()

                case "logout":
                    user_session.logout()
                    break


if __name__ == "__main__":
    main()
