from views.utils import Utils
from getpass import getpass


class UserView:
    def prompt_create_user(self):
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

    def show_user_creation_error(self):
        print("\nUne erreur s'est produite lors de l'ajout de l'utilisateur.")
        Utils.temporisation()

    def show_user_creation_success(self):
        print("\nL'utilisateur a été ajouté avec succès.")
        Utils.temporisation()

    def show_users(self, users):
        Utils.clear()
        print("--- Liste des utilisateurs ---\n")

        for user in users:
            print(
                f"{user.id} : {user.firstname} {user.name} | "
                f"{user.email} | "
                f"{user.departement.name}"
            )

        Utils.temporisation()

    def show_no_user_found(self):
        print("\nAucun utilisateur n'a été trouvé.")
        Utils.temporisation()

    def show_user_list_error(self):
        print("\nUne erreur s'est produite lors de la récupération de la liste des utilisateurs.")
        Utils.temporisation()

    def show_user_detail(self, user):
        Utils.clear()
        print("--- Détail de l'utilisateur ---\n")

        print(f"ID : {user.id}")
        print(f"Prénom : {user.firstname}")
        print(f"Nom : {user.name}")
        print(f"Email : {user.email}")
        print(f"Téléphone : {user.phone}")
        print(f"Département : {user.departement.name}")

        Utils.temporisation()

    def prompt_user_id(self):
        while True:
            Utils.clear()
            value = input("ID de l'utilisateur à selectionner : ").strip()

            if value.isdigit():
                return int(value)

    def show_user_not_found(self):
        print("\nUtilisateur introuvable.")
        Utils.temporisation()

    def show_user_detail_error(self):
        print("\nUne erreur s'est produite lors de la récupération des informations de l'utilisateur.")
        Utils.temporisation()

    def prompt_update_user(self, user):
        Utils.clear()
        print(f"--- Modification de l'utilisateur : {user.firstname} {user.name} ---\n")

        firstname = input(f"Prénom ({user.firstname}) : ").strip()
        name = input(f"Nom ({user.name}) : ").strip()
        email = input(f"Email ({user.email}) : ").strip()
        phone = input(f"Téléphone ({user.phone}) : ").strip()
        departement_id = input(
            f"ID du département (GESTION - 1, COMMERCIAL - 2, SUPPORT - 3) ({user.departement.name}): "
        ).strip()

        return {
            "firstname": firstname or user.firstname,
            "name": name or user.name,
            "email": email or user.email,
            "phone": phone or user.phone,
            "departement_id": int(departement_id) if departement_id else user.departement_id
        }

    def show_user_modification_error(self):
        print("\nErreur lors de la modification de l'utilisateur.")
        Utils.temporisation()

    def show_user_has_client_error(self):
        print("\nAction impossible, l'utilisateur est le contact d'un client.")
        Utils.temporisation()

    def show_user_modification_success(self):
        print("\nUtilisateur modifié avec succès.")
        Utils.temporisation()

    def confirm_user_deletion(self, user):
        Utils.clear()
        print("--- Confirmation de suppression ---\n")

        print(f"Utilisateur : {user.firstname} {user.name}")
        print(f"Email : {user.email}")

        choice = input("\nTapez \"SUPPRIMER\" pour supprimer cet utilisateur : ").strip()

        return choice == "SUPPRIMER"

    def show_user_deletion_success(self):
        print("\nUtilisateur supprimé avec succès.")
        Utils.temporisation()

    def show_user_deletion_error(self):
        print("\nErreur lors de la suppression de l'utilisateur.")
        Utils.temporisation()

    def show_user_deletion_cancel(self):
        print("\nL'utilisateur n'a pas été supprimé.")
        Utils.temporisation()

    def user_options(self, user_session):
        Utils.clear()
        if user_session.has_permission("can_read_user"):
            print("1 : Voir la liste des utilisateurs")

        if user_session.has_permission("can_read_user"):
            print("2 : Voir les détails d'un utilisateur")

        if user_session.has_permission("can_create_user"):
            print("3 : Ajouter un utilisateur")

        if user_session.has_permission("can_modify_user"):
            print("4 : Modifier un utilisateur")

        if user_session.has_permission("can_delete_user"):
            print("5 : Supprimer un utilisateur")

        print("0 : Retour")

        choice = input("\nChoix: ")
        return choice
