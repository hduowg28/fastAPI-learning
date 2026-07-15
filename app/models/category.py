from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base

class Category(Base):
    __tablename_ = "categories"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    books = relationship("Book", back_populates="category")