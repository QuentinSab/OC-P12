from views.utils import Utils


def prompt_login():
    Utils.clear()
    print("CRM Epic Events\n")
    email = input("Email : ")
    password = input("Mot de passe : ")
    return email, password


def show_login_error():
    print("\nIdentifiants incorrects.")
    Utils.temporisation()


def show_login_success():
    print("Connexion réussie.")
