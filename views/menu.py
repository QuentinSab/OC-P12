from views.utils import Utils


def show_menu(user_session, options):

    Utils.clear()
    print(f"Bienvenue {user_session.get_fullname()}.")
    print(f"Département: {user_session.user.departement.name}\n")

    print("Menu:\n")

    for key, label in options:
        print(f"{key}: {label}")

    choice = input("\nChoix: ")

    if choice == "0":
        return "logout"

    return choice
