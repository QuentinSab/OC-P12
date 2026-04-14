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

    @permission_required("can_create_event")
    def create_event(self):
        try:
            data = self.view.prompt_create_event()

            event = Event(**data)

            self.session.add(event)
            self.session.commit()
            self.view.show_event_creation_success()

        except Exception:
            self.session.rollback()
            self.view.show_event_creation_error()

    @permission_required("can_read_event")
    def list_events(self):
        try:
            events = self.session.query(Event).all()

            if not events:
                raise ValueError

            self.view.show_events(events)

        except ValueError:
            self.view.show_no_event_found()
        except Exception:
            self.view.show_event_list_error()

    @permission_required("can_read_event")
    def show_event(self):
        try:
            event_id = self.view.prompt_event_id()
            event = self.session.query(Event).filter_by(id=event_id).first()

            if not event:
                raise ValueError

            self.view.show_event_detail(event)

        except ValueError:
            self.view.show_event_not_found()
        except Exception:
            self.view.show_event_detail_error()

    @permission_required("can_modify_event")
    def update_event(self):
        try:
            event_id = self.view.prompt_event_id()
            event = self.session.query(Event).filter_by(id=event_id).first()

            if not event:
                raise ValueError

            data = self.view.prompt_update_event(event)

            event.contract_id = data["contract_id"]
            event.start_date = data["start_date"]
            event.end_date = data["end_date"]
            event.location = data["location"]
            event.attendees = data["attendees"]
            event.information = data["information"]

            self.session.commit()
            self.view.show_event_modification_success()

        except ValueError:
            self.view.show_event_not_found()
        except Exception:
            self.session.rollback()
            self.view.show_event_modification_error()

    def event_menu(self):
        while True:
            choice = self.view.event_options(self.user_session)

            try:
                match choice:
                    case "1":
                        self.list_events()
                    case "2":
                        self.show_event()
                    case "3":
                        self.create_event()
                    case "4":
                        self.update_event()
                    case "0":
                        break

            except PermissionError:
                Utils.show_permission_error()
