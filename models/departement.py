from sqlalchemy import Column, Integer, String, Boolean
from database.base import Base
from sqlalchemy.orm import relationship


class Departement(Base):
    __tablename__ = "departements"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    # Permissions
    can_create_user = Column(Boolean, default=False)
    can_read_user = Column(Boolean, default=False)
    can_modify_user = Column(Boolean, default=False)
    can_delete_user = Column(Boolean, default=False)

    can_create_client = Column(Boolean, default=False)
    can_read_client = Column(Boolean, default=False)
    can_modify_client = Column(Boolean, default=False)
    can_delete_client = Column(Boolean, default=False)

    can_create_contract = Column(Boolean, default=False)
    can_read_contract = Column(Boolean, default=False)
    can_modify_contract = Column(Boolean, default=False)
    can_delete_contract = Column(Boolean, default=False)

    can_create_event = Column(Boolean, default=False)
    can_read_event = Column(Boolean, default=False)
    can_modify_event = Column(Boolean, default=False)
    can_delete_event = Column(Boolean, default=False)

    users = relationship("User", back_populates="departement")

    def __repr__(self):
        return f"<Departement {self.name}>"
