from sqlalchemy import Integer, String, Column,Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Borrow(Base):
    __tablename__ = "borrows"
    id = Column(Integer, primary_key= True, index=True)
    user_id = Column(Integer, ForeignKey="users.id", nullable=False)
    book_id = Column(Integer, ForeignKey="books.id", nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable = False)
    status = Column(String, nullable=True)

    user = relationship("User", back_populates="borrows")
    book = relationship("Book", back_populates="borrows")

