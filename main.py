from controllers.authentication import AuthenticationController
from controllers.session import UserSession
from controllers.menu import MenuController
from views.authentication import prompt_login, show_login_error, show_login_success
from views.menu import show_menu


def main():
    while True:
        user = None

        while not user:
            email, password = prompt_login()
            user = AuthenticationController.login(email, password)

            if not user:
                show_login_error()

        show_login_success()
        user_session = UserSession(user)

        while True:
            options = MenuController.get_menu_options(user_session)
            choice = show_menu(user_session, options)

            if choice == "logout":
                user_session.is_authenticated = False
                break


if __name__ == "__main__":
    main()
