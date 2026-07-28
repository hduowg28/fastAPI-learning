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
    quantity = Column(Integer, default=1, nullable=False)
    available_quantity = Column(Integer, default=1, nullable=False)

    # FIX: Khai báo back_populates='books' trỏ đúng tới thuộc tính 'books' vừa sửa trong model Author
    author = relationship("Author", back_populates="books")
    category  = relationship("Category", back_populates="books")
    borrows = relationship("Borrow", back_populates="book")

