from models.event import Event
from database.session import SessionLocal
from utils.permissions import permission_required

from views.utils import Utils
from views.event import EventView


class EventController:
    def __init__(self, user_session):
        self.user_session = user_session
        self.session = None
        self.view = EventView()

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def event_menu(self):
        while True:
            choice = self.view.event_options(self.user_session)

            try:
                match choice:
                    case "1":
                        pass
                    case "2":
                        pass
                    case "3":
                        pass
                    case "4":
                        pass
                    case "0":
                        break

            except PermissionError:
                Utils.show_permission_error()
