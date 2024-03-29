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
    photo_link = Column(String, nullable=True)
    
    user = relationship("User", uselist=False, back_populates="info")
    skills = relationship(
        "SkillUserM2M", back_populates="user", lazy="joined"
    )
    _links = relationship("Link", backref="Link", lazy="joined")
    projects = relationship("Project", back_populates="author")
    project_blocks = relationship(
        "ProjectBlock", back_populates="block_author"
    )
    workplaces = relationship("Workplace", back_populates="worker")
