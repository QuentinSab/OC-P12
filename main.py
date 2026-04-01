from controllers.authentication import AuthenticationController
from controllers.client import ClientController
from controllers.user import UserController
from controllers.menu import MenuController

from views.menu import show_menu


def main():
    while True:
        authentication_controller = AuthenticationController()
        user_session = authentication_controller.login()

        menu_controller = MenuController()

        # Main menu
        while user_session.is_authenticated:

            choice = show_menu(user_session, menu_controller.get_options())

            match choice:
                case "1":  # Client
                    with ClientController(user_session) as client_controller:
                        client_controller.client_menu()

                case "4":  # User
                    with UserController(user_session) as user_controller:
                        user_controller.user_menu()

                case "0":
                    user_session.logout()
                    break


if __name__ == "__main__":
    main()
