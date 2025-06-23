from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

project_tag = Table(
    'project_tag', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)