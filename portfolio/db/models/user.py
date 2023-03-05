from sqlalchemy import Column, Integer, String, Boolean 
from sqlalchemy.orm import  relationship

from portfolio.db.models.base import Base


class User(Base):

    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    email = Column(String, nullable=True)
    is_anonymous = Column(Boolean)

    info = relationship(
        "UserInfo", uselist=False, back_populates="user", lazy="joined"
    )
    sessions = relationship("Session", back_populates="user")
    email_token = relationship(
        "EmailToken", uselist=False, back_populates="user"
    )
