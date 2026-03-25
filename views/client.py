from views.utils import Utils


def prompt_create_client():
    print("\n--- Création d'un client ---")

    full_name = input("Nom complet : ")
    email = input("Email : ")
    phone = input("Téléphone : ")
    company_name = input("Nom de l'entreprise : ")
    information = input("Informations (optionnel) : ")

    return {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "company_name": company_name,
        "information": information if information else None
    }


def show_client_creation_error():
    print("\nUne erreur s'est produite lors de l'ajout du client.")
    Utils.temporisation()


def show_client_creation_success():
    print("\nLe client a été ajouté avec succès.")
    Utils.temporisation()
