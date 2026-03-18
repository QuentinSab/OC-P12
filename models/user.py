from sqlalchemy import Column, Integer, String, ForeignKey
from database.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)
    firstname = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)

    password = Column(String(100), nullable=False)

    departement_id = Column(Integer, ForeignKey("departements.id"), nullable=False)
    departement = relationship("Departement", back_populates="users")

    def __repr__(self):
        return f"<User {self.id} {self.email}>"
