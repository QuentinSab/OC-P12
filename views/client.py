from views.utils import Utils


def prompt_create_client():
    Utils.clear()
    print("--- Création d'un client ---\n")

    full_name = input("Nom complet : ").strip()
    email = input("Email : ").strip()
    phone = input("Téléphone : ").strip()
    company_name = input("Nom de l'entreprise : ").strip()
    information = input("Informations (optionnel) : ").strip()

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
    print("--- Liste des clients ---\n")

    for client in clients:
        contact_name = f"{client.contact.firstname} {client.contact.name}"

        print(
            f"{client.id} : {client.full_name} | "
            f"{client.email} | "
            f"{client.company_name} | "
            f"{contact_name}"
        )

    Utils.temporisation()


def show_no_client_found():
    print("\nAucun client n'a été trouvé.")
    Utils.temporisation()


def show_client_detail(client):
    Utils.clear()
    print("--- Détail du client ---\n")

    print(f"ID: {client.id}")
    print(f"Nom: {client.full_name}")
    print(f"Email: {client.email}")
    print(f"Téléphone: {client.phone}")
    print(f"Société: {client.company_name}")
    print(f"Information: {client.information}")
    print(f"Créé le: {client.created_at}")
    print(f"Modifié le: {client.updated_at}")
    print(f"Contact interne: {client.contact.firstname} {client.contact.name}")

    Utils.temporisation()


def prompt_client_id():
    while True:
        Utils.clear()
        value = input("ID du client à selectionner : ").strip()

        if value.isdigit():
            return int(value)


def show_client_not_found():
    print("\nClient introuvable.")
    Utils.temporisation()


def prompt_update_client(client):
    Utils.clear()
    print(f"--- Modification du client : {client.full_name} ---\n")

    full_name = input(f"Nom complet ({client.full_name}) : ").strip()
    email = input(f"Email ({client.email}) : ").strip()
    phone = input(f"Téléphone ({client.phone}) : ").strip()
    company_name = input(f"Entreprise ({client.company_name}) : ").strip()
    information = input(f"Infos ({client.information}) : ").strip()

    return {
        "full_name": full_name or client.full_name,
        "email": email or client.email,
        "phone": phone or client.phone,
        "company_name": company_name or client.company_name,
        "information": information or client.information
    }


def show_client_modification_error():
    print("\nErreur lors de la modification du client.")
    Utils.temporisation()


def show_client_modification_success():
    print("\nClient modifié avec succès.")
    Utils.temporisation()
