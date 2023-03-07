from sqlalchemy import Column, Integer, String, ForeignKey 
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint 

from portfolio.db.models.base import Base


class SkillUserM2M(Base):

    __tablename__ = "skill_user_m2m"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("user_info.info_id"))
    user = relationship("UserInfo", back_populates="skills", lazy="joined")

    skill_id = Column(Integer, ForeignKey("skill.skill_id"))
    skill = relationship("Skill", back_populates="users", lazy="joined")

    skill_lvl = Column(String(12))


class SkillBlockM2M(Base):

    __tablename__ = "skill_block_m2m"

    id = Column(Integer, primary_key=True)

    block_id = Column(Integer, ForeignKey("project_block.block_id"))
    block = relationship(
        "ProjectBlock", back_populates="skills", lazy="joined"
    )

    skill_id = Column(Integer, ForeignKey("skill.skill_id"))
    skill = relationship("Skill", back_populates="blocks", lazy="joined") 


class Skill(Base):

    __tablename__ = "skill"

    __table_args__ = (
        UniqueConstraint("skill_name", name="uix_2"),
    )

    skill_id = Column(Integer, primary_key=True)
    skill_name = Column(String)

    users = relationship(
        "SkillUserM2M", back_populates="skill", lazy="joined"
    )
    blocks = relationship(
        "SkillBlockM2M", back_populates="skill", lazy="joined"
    )
