from models.contract import Contract
from database.session import SessionLocal
from utils.permissions import permission_required

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

            contract = Contract(**data)

            self.session.add(contract)
            self.session.commit()
            self.view.show_contract_creation_success()

        except Exception:
            self.session.rollback()
            self.view.show_contract_creation_error()

    @permission_required("can_read_contract")
    def list_contracts(self):
        try:
            contracts = self.session.query(Contract).all()

            if not contracts:
                raise ValueError

            self.view.show_contracts(contracts)

        except ValueError:
            self.view.show_no_contract_found()
        except Exception:
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
        except Exception:
            self.view.show_contract_detail_error()

    @permission_required("can_modify_contract")
    def update_contract(self):
        try:
            contract_id = self.view.prompt_contract_id()
            contract = self.session.query(Contract).filter_by(id=contract_id).first()

            if not contract:
                raise ValueError
            if not (self.user_session.user.departement_id == 1  # not from GESTION department
                    or contract.client.contact_id == self.user_session.user.id):  # nor client contact
                self.view.show_not_client_contact_error()
                return

            data = self.view.prompt_update_contract(contract)

            contract.client_id = data["client_id"]
            contract.total_amount = data["total_amount"]
            contract.payed_amount = data["payed_amount"]
            contract.is_signed = data["is_signed"]

            self.session.commit()
            self.view.show_contract_modification_success()

        except ValueError:
            self.view.show_contract_not_found()
        except Exception:
            self.session.rollback()
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
