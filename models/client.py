from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database.base import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)

    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)

    company_name = Column(String(255), nullable=False)

    information = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )

    contact_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact = relationship("User", back_populates="clients")

    def __repr__(self):
        return f"<Client {self.full_name} ({self.email})>"
