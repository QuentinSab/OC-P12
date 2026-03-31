from controllers.authentication import AuthenticationController
from controllers.client import ClientController
from controllers.menu import MenuController

from views.menu import show_menu


def main():
    while True:
        authentication_controller = AuthenticationController()
        user_session = authentication_controller.login()

        menu_controller = MenuController()

        # Main menu
        while user_session.is_authenticated:

            options = menu_controller.get_options()
            choice = show_menu(user_session, options)

            match choice:
                case "1":  # Client
                    with ClientController(user_session) as client_controller:
                        client_controller.client_menu()

                case "0":
                    user_session.logout()
                    break


if __name__ == "__main__":
    main()
