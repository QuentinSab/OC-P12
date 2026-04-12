from views.utils import Utils


def main_options(user_session):

    Utils.clear()
    print(f"{user_session.get_fullname()}")
    print(f"Département: {user_session.user.departement.name}\n")

    print("1 : Gérer les clients")
    print("2 : Gérer les contrats")
    print("3 : Gérer les événements")
    print("4 : Gérer les utilisateurs")
    print("0 : Déconnexion")

    choice = input("\nChoix: ")
    return choice
