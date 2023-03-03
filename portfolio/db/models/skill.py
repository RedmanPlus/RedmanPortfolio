from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint 

from portfolio.db.models.base import Base


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
