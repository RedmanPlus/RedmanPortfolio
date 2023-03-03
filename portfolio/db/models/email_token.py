from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from portfolio.db.models.base import Base


class EmailToken(Base):

    __tablename__ = "email_token"

    __table_args__ = (
        UniqueConstraint("key", name="uix_1"),
    )

    token_id = Column(Integer, primary_key=True)
    bearer = Column(Integer, ForeignKey("user.user_id"))
    key = Column(String)

    user = relationship("User", back_populates="email_token")
