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
        print("")
        input("Entrée pour continuer...")
