from sqlalchemy import Table, Column, Integer, ForeignKey
from src.database import Base

project_tags = Table(
    'project_tags',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)
