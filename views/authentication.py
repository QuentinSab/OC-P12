from getpass import getpass

from views.utils import Utils


def prompt_login():
    Utils.clear()
    print("CRM Epic Events\n")

    email = input("Email : ")
    password = getpass("Mot de passe : ")

    return email, password


def show_login_error():
    print("\nIdentifiants incorrects.")
    Utils.temporisation()
