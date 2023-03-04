from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from portfolio.db.models.base import Base
from portfolio.db.models.skill import SkillUserM2M


class UserInfo(Base):

    __tablename__ = "user_info"

    info_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    first_name = Column(String)
    last_name = Column(String)
    description = Column(String)
    
    user = relationship("User", uselist=False, back_populates="info")
    _skills = relationship("Skill", secondary=SkillUserM2M, backref="UserInfo")
    _links = relationship("Link", backref="Link")
