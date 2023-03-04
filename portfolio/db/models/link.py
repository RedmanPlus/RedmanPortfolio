from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from portfolio.db.models.base import Base


class Link(Base):

    __tablename__ = "link"

    link_id = Column(Integer, primary_key=True)
    resource = Column(String)
    url = Column(String)
    user_id = Column(Integer, ForeignKey("user_info.info_id"))

    _user = relationship("UserInfo", backref="UserInfo")
