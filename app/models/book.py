from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author_id  = Column(Integer, ForeignKey("authors.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    published_year = Column(Integer)
    #relationship
    author = relationship("Author", back_populates="book")
    category  = relationship("Category", back_populates="books")
    borrows = relationship("Borrow", back_populates="book")

