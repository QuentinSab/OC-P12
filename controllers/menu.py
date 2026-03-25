class MenuController:

    def __init__(self, user_session):
        self.user_session = user_session

    def get_main_menu(self):
        options = []

        if self.user_session.has_permission("can_create_client"):
            options.append(("1", "Ajouter un client"))

        if self.user_session.has_permission("can_read_client"):
            options.append(("2", "Voir la liste des clients"))

        if self.user_session.has_permission("can_modify_client"):
            options.append(("3", "Modifier un client"))

        options.append(("0", "Déconnexion"))

        return options
