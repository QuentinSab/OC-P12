from views.utils import Utils


class ContractView:
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
