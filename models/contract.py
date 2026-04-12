from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from database.base import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="contracts")

    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)

    is_signed = Column(Boolean, default=False, nullable=False)
    signed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Contrat #{self.id} - Client {self.client_id} - Signé: {self.is_signed}>"
