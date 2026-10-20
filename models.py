from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship

from db import Base

class ISOContainerType(Base):
    __tablename__ ="ISOContainerType"

    gkey = Column(Integer,primary_key=True)
    code = Column(String)
    description = Column(String)
    length = Column(Integer) 
    height = Column(DECIMAL)
    group = Column(String)