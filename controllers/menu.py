class MenuController:

    @staticmethod
    def get_menu_options(user_session):
        options = []

        if user_session.has_permission("can_create_client"):
            options.append(("1", "Créer un client"))

        if user_session.has_permission("can_create_contract"):
            options.append(("2", "Créer un contrat"))

        if user_session.has_permission("can_create_event"):
            options.append(("3", "Créer un événement"))

        options.append(("0", "Déconnexion"))

        return options
