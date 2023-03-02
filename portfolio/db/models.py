from collections import namedtuple
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


class UserInfo(Base):

    __tablename__ = "user_info"

    info_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    first_name = Column(String)
    last_name = Column(String)
    description = Column(String)
    
    skills = relationship("SkillUserM2M", back_populates="skill_user_m2m.user")
    links = relationship("Link", back_populates="link.user")


class Skill(Base):

    __tablename__ = "skill"

    __table_args__ = (
        UniqueConstraint("skill_name", name="uix_2"),
    )

    skill_id = Column(Integer, primary_key=True)
    skill_name = Column(String)

    users = relationship("SkillUserM2M", back_populates="skill_user_m2m.skill")


class SkillUserM2M(Base):

    __tablename__ = "skill_user_m2m"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_info.info_id"))
    skill_id = Column(Integer, ForeignKey("skill.skill_id"))

    user = relationship("UserInfo", back_populates="user_info.skills")
    skill = relationship("Skill", back_populates="skill.users")


class Link(Base):

    __tablename__ = "link"

    link_id = Column(Integer, primary_key=True)
    resource = Column(String)
    url = Column(String)
    user_id = Column(Integer, ForeignKey("user_info.info_id"))

    user = relationship("UserInfo", back_populates="user_info.links")


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
