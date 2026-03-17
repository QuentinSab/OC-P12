from sqlalchemy import Column, Integer, String, Enum
import enum
from database.base import Base


class Departement(enum.Enum):
    COMMERCIAL = "COMMERCIAL"
    SUPPORT = "SUPPORT"
    GESTION = "GESTION"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)
    firstname = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)

    password = Column(String(100), nullable=False)

    departement = Column(Enum(Departement, name="departement_enum"), nullable=False)

    def __repr__(self):
        return f"<User {self.id} {self.email} ({self.departement.value})>"
