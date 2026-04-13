from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from database.base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="events")

    support_contact_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    support_contact = relationship("User", back_populates="events")

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    location = Column(String(255), nullable=False)
    attendees = Column(Integer, nullable=False)
    information = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Event #{self.id} - Client {self.client_id} - {self.start_date} → {self.end_date}>"
