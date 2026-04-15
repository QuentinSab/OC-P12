from views.utils import Utils


class EventView:
    def prompt_create_event(self):
        Utils.clear()
        print("--- Création d'un évènement ---\n")

        contract_id = input("ID du contrat : ").strip()
        start_date = input("Date de début (jj/mm/aaaa hh:mm:ss) : ").strip()
        end_date = input("Date de fin (jj/mm/aaaa hh:mm:ss) : ").strip()
        location = input("Localisation : ").strip()
        attendees = input("Nombre de participants : ").strip()
        information = input("Information : ").strip()

        return {
            "contract_id": contract_id,
            "start_date": start_date,
            "end_date": end_date,
            "location": location,
            "attendees": attendees,
            "information": information,
        }

    def show_event_creation_error(self):
        print("\nUne erreur s'est produite lors de la création de l'évènement.")
        Utils.temporisation()

    def show_not_client_contact_error(self):
        print("\nCréation de l'évènement impossible, vous n'êtes pas le contact client du client de ce contrat.")
        Utils.temporisation()

    def show_contract_not_found(self):
        print("\nContrat introuvable.")
        Utils.temporisation()

    def show_contract_not_signed_error(self):
        print("\nCréation de l'évènement impossible, le contrat sélectionné n'est pas signé.")
        Utils.temporisation()

    def show_event_creation_success(self):
        print("\nL'évènement a été créé avec succès.")
        Utils.temporisation()

    def show_events(self, events):
        Utils.clear()
        print("--- Liste des évènements ---\n")

        for event in events:
            client = event.contract.client
            client_contact_name = f"{client.contact.firstname} {client.contact.name}"

            support_contact = event.support_contact
            support_contact_name = (
                f"{support_contact.firstname} {support_contact.name}" if support_contact else "Non assigné"
                )

            print(
                f"{event.id} - "
                f"Client: {client.full_name} | "
                f"Contact client: {client_contact_name} | "
                f"Contact support: {support_contact_name} | "
                f"Date: {event.start_date} -> {event.end_date}"
            )

        Utils.temporisation()

    def show_no_event_found(self):
        print("\nAucun évènement n'a été trouvé.")
        Utils.temporisation()

    def show_event_list_error(self):
        print("\nUne erreur s'est produite lors de la récupération de la liste des évènements.")
        Utils.temporisation()

    def show_event_detail(self, event):
        Utils.clear()
        print("--- Détail de l'évènement ---\n")

        client = event.contract.client
        client_contact_name = f"{client.contact.firstname} {client.contact.name}"

        support_contact = event.support_contact
        support_contact_name = (
            f"{support_contact.firstname} {support_contact.name}" if support_contact else "Non assigné"
            )

        print(f"ID: {event.id}")
        print(f"ID contrat: {event.contract_id}")
        print(f"Client: {client.full_name}")
        print(f"Contact client: {client_contact_name}")
        print(f"Date de début: {event.start_date}")
        print(f"Date de fin: {event.end_date}")
        print(f"Contact support: {support_contact_name}")
        print(f"Localisation: {event.location}")
        print(f"Nombre de participants: {event.attendees}")
        print(f"Information: {event.information}")

        Utils.temporisation()

    def prompt_event_id(self):
        while True:
            Utils.clear()
            value = input("ID de l'évènement à selectionner : ").strip()

            if value.isdigit():
                return int(value)

    def show_event_not_found(self):
        print("\nÉvènement introuvable.")
        Utils.temporisation()

    def show_event_detail_error(self):
        print("\nUne erreur s'est produite lors de la récupération des informations de l'évènement.")
        Utils.temporisation()

    def prompt_assign_event_support(self, event):
        Utils.clear()
        print(f"--- Attribution du contact support pour l'évènement : {event.id} ---\n")

        if event.support_contact:
            support_contact = (f"{event.support_contact.firstname} {event.support_contact.name}")
        else:
            support_contact = "Non assigné"

        support_contact_id = input(f"ID du contact support ({event.support_contact_id} - {support_contact}): ").strip()

        if support_contact_id:
            return {"support_contact_id": int(support_contact_id)}
        return {"support_contact_id": event.support_contact_id}

    def prompt_update_event(self, event):
        Utils.clear()
        print(f"--- Modification de l'évènement : {event.id} ---\n")

        start_date = input(f"Date de début (jj/mm/aaaa hh:mm:ss) ({event.start_date}) : ").strip()
        end_date = input(f"Date de fin (jj/mm/aaaa hh:mm:ss) ({event.end_date}) : ").strip()
        location = input("Localisation : ").strip()
        attendees = input(f"Nombre de participants ({event.attendees}): ").strip()
        information = input("Information : ").strip()

        return {
            "support_contact_id": event.support_contact_id,
            "start_date": start_date or event.start_date,
            "end_date": end_date or event.end_date,
            "location": location or event.location,
            "attendees": attendees or event.attendees,
            "information": information or event.information,
        }

    def show_event_modification_error(self):
        print("\nErreur lors de la modification de l'évènement.")
        Utils.temporisation()

    def show_not_support_user_error(self):
        print("\nAssignation impossible, l'utilisateur sélectionné n'est pas du département SUPPORT.")
        Utils.temporisation()

    def show_event_modification_success(self):
        print("\nÉvènement modifié avec succès.")
        Utils.temporisation()

    def event_options(self, user_session):
        Utils.clear()
        if user_session.has_permission("can_read_event"):
            print("1 : Voir la liste des évènements")

        if user_session.has_permission("can_read_event"):
            print("2 : Voir les détails d'un évènement")

        if user_session.has_permission("can_create_event"):
            print("3 : Créer un évènement")

        if user_session.has_permission("can_modify_event"):
            print("4 : Modifier un évènement")

        print("0 : Retour")

        choice = input("\nChoix: ")
        return choice
