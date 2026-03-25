import os


class Utils:

    @staticmethod
    def clear():
        """Clear the console based on the operating system"""
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def temporisation():
        """Pause execution until the user make an input"""

        input("\nEntrée pour continuer...")

    @staticmethod
    def show_permission_error():
        print("\nVous n'avez pas les droits pour effectuer cette action.")
        Utils.temporisation()
