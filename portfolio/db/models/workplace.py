from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from portfolio.db.models.base import Base


class Workplace(Base):

    __tablename__ = "workplace"

    workplace_id = Column(Integer, primary_key=True)
    workplace_name = Column(String)
    work_start_date = Column(Date)
    work_end_date = Column(Date, nullable=True)
    is_current_workplace = Column(Boolean)
    company_link = Column(String)
    workplace_decsription = Column(String)
    
    skills = relationship("SkillWorkplaceM2M", back_populates="workplace")
    
    projects = relationship("Project", back_populates="workplace")

    worker_id = Column(Integer, ForeignKey("user_info.info_id"))
    worker = relationship("UserInfo", back_populates="workplaces")
