from views.utils import Utils


class EventView:
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
