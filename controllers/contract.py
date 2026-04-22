from models.contract import Contract
from database.session import SessionLocal
from utils.permissions import permission_required
import sentry_sdk
from decimal import Decimal
from utils.sentry import log_event

from views.utils import Utils
from views.contract import ContractView


class ContractController:
    def __init__(self, user_session):
        self.user_session = user_session
        self.session = None
        self.view = ContractView()

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @permission_required("can_create_contract")
    def create_contract(self):
        try:
            data = self.view.prompt_create_contract()

            total_amount = Decimal(data["total_amount"])
            payed_amount = Decimal(data["payed_amount"])

            if payed_amount > total_amount:
                self.view.show_invalid_amount_error()
                return

            contract = Contract(**data)

            self.session.add(contract)
            self.session.commit()
            if contract.is_signed:
                log_event(
                    "Signature d'un contrat",
                    contract_id=contract.id,
                    client_id=contract.client_id,
                    user_id=self.user_session.user.id,
                )
            self.view.show_contract_creation_success()

        except Exception as exception:
            self.session.rollback()
            sentry_sdk.capture_exception(exception)
            self.view.show_contract_creation_error()

    @permission_required("can_read_contract")
    def list_contracts(self):
        try:
            query = self.session.query(Contract)
            contracts = query.all()

            if not contracts:
                raise ValueError

            self.view.show_contracts(contracts)

            while True:
                choice = self.view.prompt_contract_filter()

                match choice:
                    case "1":
                        contracts = query.all()
                    case "2":  # Contracts not fully paid
                        contracts = query.filter(Contract.payed_amount < Contract.total_amount).all()
                    case "3":  # Contracts not signed
                        contracts = query.filter_by(is_signed=False).all()
                    case "4":  # User client contracts
                        contracts = query.join(Contract.client).filter_by(contact_id=self.user_session.user.id).all()
                    case "0":
                        break

                if contracts:
                    self.view.show_contracts(contracts)
                else:
                    self.view.show_no_contract_found()

        except ValueError:
            self.view.show_no_contract_found()
        except Exception as exception:
            sentry_sdk.capture_exception(exception)
            self.view.show_contract_list_error()

    @permission_required("can_read_contract")
    def show_contract(self):
        try:
            contract_id = self.view.prompt_contract_id()
            contract = self.session.query(Contract).filter_by(id=contract_id).first()

            if not contract:
                raise ValueError

            self.view.show_contract_detail(contract)

        except ValueError:
            self.view.show_contract_not_found()
        except Exception as exception:
            sentry_sdk.capture_exception(exception)
            self.view.show_contract_detail_error()

    @permission_required("can_modify_contract")
    def update_contract(self):
        try:
            contract_id = self.view.prompt_contract_id()
            contract = self.session.query(Contract).filter_by(id=contract_id).first()

            if not contract:
                raise ValueError
            if (
                self.user_session.user.departement.name == "COMMERCIAL"
                and contract.client.contact_id != self.user_session.user.id
            ):
                self.view.show_not_client_contact_error()
                return

            was_signed = contract.is_signed
            data = self.view.prompt_update_contract(contract)

            total_amount = Decimal(data["total_amount"])
            payed_amount = Decimal(data["payed_amount"])

            if payed_amount > total_amount:
                self.view.show_invalid_amount_error()
                return

            contract.client_id = data["client_id"]
            contract.total_amount = data["total_amount"]
            contract.payed_amount = data["payed_amount"]
            contract.is_signed = data["is_signed"]

            self.session.commit()
            if not was_signed and contract.is_signed:
                log_event(
                    "Signature d'un contrat",
                    contract_id=contract.id,
                    client_id=contract.client_id,
                    user_id=self.user_session.user.id,
                )
            self.view.show_contract_modification_success()

        except ValueError:
            self.view.show_contract_not_found()
        except Exception as exception:
            self.session.rollback()
            sentry_sdk.capture_exception(exception)
            self.view.show_contract_modification_error()

    def contract_menu(self):
        while True:
            choice = self.view.contract_options(self.user_session)

            try:
                match choice:
                    case "1":
                        self.list_contracts()
                    case "2":
                        self.show_contract()
                    case "3":
                        self.create_contract()
                    case "4":
                        self.update_contract()
                    case "0":
                        break

            except PermissionError:
                Utils.show_permission_error()
