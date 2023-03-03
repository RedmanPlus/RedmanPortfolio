from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from portfolio.db.models.base import Base


class Session(Base):

    __tablename__ = "session"

    session_id = Column(Integer, primary_key=True)
    session_key = Column(String, unique=True)
    uid = Column(Integer, ForeignKey("user.user_id"))

    user = relationship("User", back_populates="sessions")
