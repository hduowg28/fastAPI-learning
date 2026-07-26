from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # FIX: Đổi tên quan hệ thành 'books' (1 Tác giả có nhiều Sách) và back_populates tham chiếu tới thuộc tính 'author' trong model Book
    books = relationship("Book", back_populates="author")