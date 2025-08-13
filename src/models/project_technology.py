from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

project_technology = Table(
    'project_technology',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('technology_id', Integer, ForeignKey('technologies.id'), primary_key=True)
)
