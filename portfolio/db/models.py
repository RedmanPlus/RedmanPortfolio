from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.schema import UniqueConstraint 


Base = declarative_base()


class User(Base):

    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    email = Column(String, nullable=True)
    is_anonymous = Column(Boolean)

    sessions = relationship("Session", back_populates="user")
    email_token = relationship("EmailToken", uselist=False, back_populates="user")


class Session(Base):

    __tablename__ = "session"

    session_id = Column(Integer, primary_key=True)
    session_key = Column(String, unique=True)
    uid = Column(Integer, ForeignKey("user.user_id"))

    user = relationship("User", back_populates="sessions")


class EmailToken(Base):

    __tablename__ = "email_token"

    __table_args__ = (
        UniqueConstraint("key", name="uix_1"),
    )

    token_id = Column(Integer, primary_key=True)
    bearer = Column(Integer, ForeignKey("user.user_id"))
    key = Column(String)

    user = relationship("User", back_populates="email_token")
