from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):

    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    email = Column(String, nullable=True)
    is_anonymous = Column(Boolean)

    sessions = relationship("Session", back_populates="user")
    

class Session(Base):

    __tablename__ = "session"

    session_id = Column(Integer, primary_key=True)
    session_key = Column(String, unique=True)
    uid = Column(Integer, ForeignKey("user.user_id"))

    user = relationship("User", back_populates="sessions")
