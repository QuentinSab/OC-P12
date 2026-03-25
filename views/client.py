from views.utils import Utils


def prompt_create_client():
    Utils.clear()
    print("--- Création d'un client ---\n")

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


def show_clients(clients):
    Utils.clear()
    print("\n--- Liste des clients ---\n")

    for client in clients:
        print(f"{client.id} : {client.full_name} | {client.email} | {client.company_name}")

    Utils.temporisation()


def show_no_client_found():
    print("Aucun client n'a été trouvé.")
    Utils.temporisation()


def prompt_client_id():
    while True:
        Utils.clear()
        value = input("ID du client à modifier : ").strip()

        if value.isdigit():
            return int(value)


def prompt_update_client(client):
    Utils.clear()
    print(f"--- Modification du client : {client.full_name} ---\n")

    full_name = input(f"Nom complet ({client.full_name}) : ").strip()
    email = input(f"Email ({client.email}) : ").strip()
    phone = input(f"Téléphone ({client.phone}) : ").strip()
    company_name = input(f"Entreprise ({client.company_name}) : ").strip()
    information = input(f"Infos ({client.information}) : ").strip()

    print("")

    return {
        "full_name": full_name or client.full_name,
        "email": email or client.email,
        "phone": phone or client.phone,
        "company_name": company_name or client.company_name,
        "information": information or client.information
    }


def show_client_not_found():
    print("Client introuvable.")
    Utils.temporisation()


def show_client_modification_success():
    print("Client modifié avec succès.")
    Utils.temporisation()


def show_client_modification_error():
    print("Erreur lors de la modification du client.")
    Utils.temporisation()
