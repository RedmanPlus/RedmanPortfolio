from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint 

from portfolio.db.models.base import Base


SkillUserM2M = Table("skill_user_m2m",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user_info.info_id")),
    Column("skill_id", Integer, ForeignKey("skill.skill_id")),
    Column("skill_lvl", String(12))
)


class Skill(Base):

    __tablename__ = "skill"

    __table_args__ = (
        UniqueConstraint("skill_name", name="uix_2"),
    )

    skill_id = Column(Integer, primary_key=True)
    skill_name = Column(String)

    users = relationship("UserInfo", secondary=SkillUserM2M, backref="Skill")
