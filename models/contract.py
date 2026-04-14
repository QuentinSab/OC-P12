from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime

from database.base import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="contracts")

    total_amount = Column(Numeric(12, 2), nullable=False)
    payed_amount = Column(Numeric(12, 2), default=0, nullable=False)

    is_signed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    events = relationship("Event", back_populates="contract")

    def __repr__(self):
        return f"<Contrat #{self.id} - Client {self.client_id} - Signé: {self.is_signed}>"

    @property
    def remaining_amount(self):
        return self.total_amount - self.payed_amount
