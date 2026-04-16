from controllers.authentication import AuthenticationController
from controllers.event import EventController
from controllers.contract import ContractController
from controllers.client import ClientController
from controllers.user import UserController

from views.menu import main_options

import os
import sentry_sdk
from dotenv import load_dotenv


def main():
    load_dotenv()

    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        send_default_pii=True,
        enable_logs=True,
    )

    while True:
        authentication_controller = AuthenticationController()
        user_session = authentication_controller.login()

        # Main menu
        while user_session.is_authenticated:
            choice = main_options(user_session)

            match choice:
                case "1":  # Client
                    with ClientController(user_session) as client_controller:
                        client_controller.client_menu()

                case "2":  # Contract
                    with ContractController(user_session) as contract_controller:
                        contract_controller.contract_menu()

                case "3":  # Event
                    with EventController(user_session) as event_controller:
                        event_controller.event_menu()

                case "4":  # User
                    with UserController(user_session) as user_controller:
                        user_controller.user_menu()

                case "0":
                    user_session.logout()
                    break


if __name__ == "__main__":
    main()
