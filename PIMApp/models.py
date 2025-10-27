from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class PIM(Base):
    __tablename__ = 'pim'

    id = Column(Integer, primary_key=True, index=True)
    project_number = Column(String, unique=True)
    team = Column(String)
    engineer = Column(String)
    customer = Column(String)
    project_name = Column(String)
    progress = Column(Integer)
