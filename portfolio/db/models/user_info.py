from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from portfolio.db.models.base import Base


class UserInfo(Base):

    __tablename__ = "user_info"

    info_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    first_name = Column(String)
    last_name = Column(String)
    description = Column(String)
    
    user = relationship("User", uselist=False, back_populates="info")
    skills = relationship("SkillUserM2M", back_populates="skill_user_m2m.user")
    links = relationship("Link", back_populates="link.user")
