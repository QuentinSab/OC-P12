from views.utils import Utils


class ContractView:
    def prompt_create_contract(self):
        Utils.clear()
        print("--- Création d'un contrat ---\n")

        client_id = input("ID du client : ").strip()
        total_amount = input("Montant total (€) : ").strip()
        payed_amount = input("Montant payé (€) : ").strip()
        is_signed = input("Contrat signé (oui/non) : ").strip().lower()

        return {
            "client_id": client_id,
            "total_amount": total_amount,
            "payed_amount": payed_amount,
            "is_signed": is_signed == "oui",
        }

    def show_contract_creation_error(self):
        print("\nUne erreur s'est produite lors de la création du contrat.")
        Utils.temporisation()

    def show_contract_creation_success(self):
        print("\nLe contrat a été créé avec succès.")
        Utils.temporisation()

    def show_contracts(self, contracts):
        Utils.clear()
        print("--- Liste des contrats ---\n")

        for contract in contracts:
            client = contract.client
            contact = client.contact
            contact_name = f"{contact.firstname} {contact.name}"

            print(
                f"{contract.id} - "
                f"Client: {client.full_name} | "
                f"Contact: {contact_name} | "
                f"Total: {contract.total_amount}€ | "
                f"Payé: {contract.payed_amount}€ | "
                f"Restant: {contract.remaining_amount}€ | "
                f"Signé: {'Oui' if contract.is_signed else 'Non'}"
            )

    def prompt_contract_filter(self):
        print("\n--- Filtres contrats ---\n")
        print("1: Tous les contrats")
        print("2: Contrats non entièrement payés")
        print("3: Contrats non signés")
        print("4: Mes contrats (contact client)")
        print("0: Retour")

        return input("\nChoix: ").strip()

    def show_no_contract_found(self):
        print("\nAucun contrat n'a été trouvé.")
        Utils.temporisation()

    def show_contract_list_error(self):
        print("\nUne erreur s'est produite lors de la récupération de la liste des contrats.")
        Utils.temporisation()

    def show_contract_detail(self, contract):
        Utils.clear()
        print("--- Détail du contrat ---\n")

        client = contract.client
        contact = client.contact
        contact_name = f"{contact.firstname} {contact.name}"

        print(f"ID: {contract.id}")
        print(f"Client: {client.full_name}")
        print(f"Contact: {contact_name}")
        print(f"Total: {contract.total_amount}€")
        print(f"Payé: {contract.payed_amount}€")
        print(f"Restant: {contract.remaining_amount}€")
        print(f"Signé: {'Oui' if contract.is_signed else 'Non'}")
        print(f"Créé le: {contract.created_at}")

        Utils.temporisation()

    def prompt_contract_id(self):
        while True:
            Utils.clear()
            value = input("ID du contrat à selectionner : ").strip()

            if value.isdigit():
                return int(value)

    def show_contract_not_found(self):
        print("\nContrat introuvable.")
        Utils.temporisation()

    def show_contract_detail_error(self):
        print("\nUne erreur s'est produite lors de la récupération des informations du contrat.")
        Utils.temporisation()

    def prompt_update_contract(self, contract):
        Utils.clear()
        print(f"--- Modification du contrat : {contract.id} ---\n")

        client_id = input(f"Client ID ({contract.client_id} - {contract.client.full_name}) : ").strip()
        total_amount = input(f"Total ({contract.total_amount}€) : ").strip()
        payed_amount = input(f"Payé ({contract.payed_amount}€) : ").strip()
        is_signed_input = input(f"Signé (oui/non) ({contract.is_signed}) : ").strip().lower()

        if is_signed_input == "oui":
            is_signed = True
        elif is_signed_input == "non":
            is_signed = False
        else:
            is_signed = contract.is_signed

        return {
            "client_id": client_id or contract.client_id,
            "total_amount": total_amount or contract.total_amount,
            "payed_amount": payed_amount or contract.payed_amount,
            "is_signed": is_signed,
        }

    def show_not_client_contact_error(self):
        print("\nModification impossible, vous n'êtes pas le contact du client de ce contrat.")
        Utils.temporisation()

    def show_contract_modification_error(self):
        print("\nErreur lors de la modification du contrat.")
        Utils.temporisation()

    def show_contract_modification_success(self):
        print("\nContrat modifié avec succès.")
        Utils.temporisation()

    def contract_options(self, user_session):
        Utils.clear()
        if user_session.has_permission("can_read_contract"):
            print("1 : Voir la liste des contrats")

        if user_session.has_permission("can_read_contract"):
            print("2 : Voir les détails d'un contrat")

        if user_session.has_permission("can_create_contract"):
            print("3 : Créer un contrat")

        if user_session.has_permission("can_modify_contract"):
            print("4 : Modifier un contrat")

        print("0 : Retour")

        choice = input("\nChoix: ")
        return choice
