from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from portfolio.db.models import Base


class Project(Base):

    __tablename__ = "project"

    project_id = Column(Integer, primary_key=True)
    project_name = Column(String)
    short_description = Column(String)
    project_logo = Column(String)
    full_description = Column(String)
    is_public = Column(Boolean, default=False)

    blocks = relationship("ProjectBlock", back_populates="project")

    author_id = Column(Integer, ForeignKey("user_info.info_id"))
    author = relationship("UserInfo", back_populates="projects")

    workplace_id = Column(
        Integer, ForeignKey("workplace.workplace_id"), nullable=True
    )
    workplace = relationship("Workplace", back_populates="projects")


class BlockBlockM2M(Base):
    __tablename__ = "block_block_m2m"

    left_id = Column(
        Integer, ForeignKey("project_block.block_id"), primary_key=True
    )
    right_id = Column(
        Integer, ForeignKey("project_block.block_id"), primary_key=True
    )

    left = relationship(
        "ProjectBlock",
        primaryjoin=lambda: BlockBlockM2M.left_id == ProjectBlock.block_id,
        backref="left_references"
    )
    right = relationship(
        "ProjectBlock",
        primaryjoin=lambda: BlockBlockM2M.right_id == ProjectBlock.block_id,
        backref="right_references"
    )


class ProjectBlock(Base):
    
    __tablename__ = "project_block"

    block_id = Column(Integer, primary_key=True)
    block_name = Column(String)
    block_description = Column(String)

    skills = relationship(
        "SkillBlockM2M", back_populates="block", lazy="joined"
    )

    block_author_id = Column(Integer, ForeignKey("user_info.info_id")) 
    block_author = relationship("UserInfo", back_populates="project_blocks")

    project_id = Column(Integer, ForeignKey("project.project_id"))
    project = relationship("Project", back_populates="blocks")

    blocks = relationship(
        BlockBlockM2M,
        secondary="block_block_m2m",
        primaryjoin=lambda: ProjectBlock.block_id == BlockBlockM2M.left_id,
        secondaryjoin=lambda: ProjectBlock.block_id == BlockBlockM2M.right_id,
        backref="block"
    )
