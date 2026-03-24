class MenuController:

    def __init__(self, user_session):
        self.user_session = user_session

    def get_main_menu(self):
        options = []

        if self.user_session.has_permission("can_create_client"):
            options.append(("1", "Ajouter un client"))

        options.append(("0", "Déconnexion"))

        return options
