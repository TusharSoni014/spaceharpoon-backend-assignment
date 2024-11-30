from sqlalchemy import Column, Integer, String, Float, Boolean

from db import Base


class Books(Base):
  __tablename__ = "books"

  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String, nullable=False)
  author = Column(String, nullable=False)
  description = Column(String, nullable=True)
  price = Column(Float, nullable=False)
  is_available = Column(Boolean, default=True)
  
