from views.utils import Utils
from getpass import getpass


def prompt_create_user():
    Utils.clear()
    print("--- Création d'un utilisateur ---\n")

    firstname = input("Prénom : ").strip()
    name = input("Nom : ").strip()
    email = input("Email : ").strip()
    phone = input("Téléphone : ").strip()
    password = getpass("Mot de passe : ").strip()
    departement_id = input("ID du département (GESTION - 1, COMMERCIAL - 2, SUPPORT - 3): ").strip()

    return {
        "firstname": firstname,
        "name": name,
        "email": email,
        "phone": phone,
        "password": password,
        "departement_id": int(departement_id)
    }


def show_user_creation_error():
    print("\nUne erreur s'est produite lors de l'ajout de l'utilisateur.")
    Utils.temporisation()


def show_user_creation_success():
    print("\nL'utilisateur a été ajouté avec succès.")
    Utils.temporisation()


def show_users(users):
    Utils.clear()
    print("--- Liste des utilisateurs ---\n")

    for user in users:
        print(
            f"{user.id} : {user.firstname} {user.name} | "
            f"{user.email} | "
            f"{user.departement.name}"
        )

    Utils.temporisation()


def show_no_user_found():
    print("\nAucun utilisateur n'a été trouvé.")
    Utils.temporisation()


def show_user_detail(user):
    Utils.clear()
    print("--- Détail de l'utilisateur ---\n")

    print(f"ID : {user.id}")
    print(f"Prénom : {user.firstname}")
    print(f"Nom : {user.name}")
    print(f"Email : {user.email}")
    print(f"Téléphone : {user.phone}")
    print(f"Département : {user.departement.name}")

    Utils.temporisation()


def prompt_user_id():
    while True:
        Utils.clear()
        value = input("ID de l'utilisateur à selectionner : ").strip()

        if value.isdigit():
            return int(value)


def show_user_not_found():
    print("\nUtilisateur introuvable.")
    Utils.temporisation()


def prompt_update_user(user):
    Utils.clear()
    print(f"--- Modification de l'utilisateur : {user.firstname} {user.name} ---\n")

    firstname = input(f"Prénom ({user.firstname}) : ").strip()
    name = input(f"Nom ({user.name}) : ").strip()
    email = input(f"Email ({user.email}) : ").strip()
    phone = input(f"Téléphone ({user.phone}) : ").strip()
    departement_id = input(f"ID du département ({user.departement.name}) : ").strip()

    return {
        "firstname": firstname or user.firstname,
        "name": name or user.name,
        "email": email or user.email,
        "phone": phone or user.phone,
        "departement_id": int(departement_id) if departement_id else user.departement_id
    }


def show_user_modification_error():
    print("\nErreur lors de la modification de l'utilisateur.")
    Utils.temporisation()


def show_user_modification_success():
    print("\nUtilisateur modifié avec succès.")
    Utils.temporisation()


def confirm_user_deletion(user):
    Utils.clear()
    print("--- Confirmation de suppression ---\n")

    print(f"Utilisateur : {user.firstname} {user.name}")
    print(f"Email : {user.email}")

    choice = input("\nTapez \"SUPPRIMER\" pour supprimer cet utilisateur : ").strip()

    return choice == "SUPPRIMER"


def show_user_deletion_success():
    print("\nUtilisateur supprimé avec succès.")
    Utils.temporisation()


def show_user_deletion_error():
    print("\nErreur lors de la suppression de l'utilisateur.")
    Utils.temporisation()


def show_user_deletion_cancel():
    print("\nL'utilisateur n'a pas été supprimé.")
    Utils.temporisation()
