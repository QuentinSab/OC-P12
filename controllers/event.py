from models.event import Event
from models.contract import Contract
from models.user import User
from database.session import SessionLocal
from utils.permissions import permission_required
import sentry_sdk
from dateutil.parser import parse

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

            contract = self.session.query(Contract).filter_by(id=data["contract_id"]).first()

            if not contract:
                raise ValueError
            if contract.client.contact_id != self.user_session.user.id:
                self.view.show_not_client_contact_error()
                return
            if not contract.is_signed:
                self.view.show_contract_not_signed_error()
                return

            start_date = parse(data["start_date"], dayfirst=True)
            end_date = parse(data["end_date"], dayfirst=True)

            if start_date >= end_date:
                self.view.show_start_date_event_error()
                return

            event = Event(**data)

            self.session.add(event)
            self.session.commit()
            self.view.show_event_creation_success()

        except ValueError:
            self.view.show_contract_not_found()
        except Exception as exception:
            self.session.rollback()
            sentry_sdk.capture_exception(exception)
            self.view.show_event_creation_error()

    @permission_required("can_read_event")
    def list_events(self):
        try:
            query = self.session.query(Event)
            events = query.all()

            if not events:
                raise ValueError

            self.view.show_events(events)

            while True:
                choice = self.view.prompt_event_filter()

                match choice:
                    case "1":
                        events = query.all()
                    case "2":  # Events without support contact
                        events = query.filter_by(support_contact_id=None).all()
                    case "3":  # User events
                        events = query.filter_by(support_contact_id=self.user_session.user.id).all()
                    case "0":
                        break

                if events:
                    self.view.show_events(events)
                else:
                    self.view.show_no_event_found()

        except ValueError:
            self.view.show_no_event_found()
        except Exception as exception:
            sentry_sdk.capture_exception(exception)
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
        except Exception as exception:
            sentry_sdk.capture_exception(exception)
            self.view.show_event_detail_error()

    @permission_required("can_modify_event")
    def update_event(self):
        try:
            event_id = self.view.prompt_event_id()
            event = self.session.query(Event).filter_by(id=event_id).first()

            if not event:
                raise ValueError

            user_session_departement = self.user_session.user.departement.name
            if user_session_departement == "GESTION":
                data = self.view.prompt_assign_event_support(event)

                selected_user = (self.session.query(User).filter_by(id=data["support_contact_id"]).first())
                if not selected_user or selected_user.departement.name != "SUPPORT":
                    self.view.show_not_support_user_error()
                    return

                event.support_contact_id = data["support_contact_id"]

            elif user_session_departement == "SUPPORT":
                data = self.view.prompt_update_event(event)

                start_date = parse(data["start_date"], dayfirst=True)
                end_date = parse(data["end_date"], dayfirst=True)

                if start_date >= end_date:
                    self.view.show_start_date_event_error()
                    return

                event.start_date = data["start_date"]
                event.end_date = data["end_date"]
                event.location = data["location"]
                event.attendees = data["attendees"]
                event.information = data["information"]

            self.session.commit()
            self.view.show_event_modification_success()

        except ValueError:
            self.view.show_event_not_found()
        except Exception as exception:
            self.session.rollback()
            sentry_sdk.capture_exception(exception)
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
