from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.authors import AuthorCreate, AuthorUpdate
from typing import List, Optional

class AuthorRepository:
    def __init__(self, db:Session):
        self.db=db

    def get_all(self) -> List[Author]:
        return self.db.query(Author).all()
    
    def get_by_id(self, author_id) -> Author:
        return self.db.query(Author).filter(Author.id==author_id).first()

    def check_duplicate(self, author_id:int , name: str) ->Optional[Author]:
        return self.query().filter(Author.id==author_id, Author.name.ilike(name)).first()
    
    def create(self, data_author:AuthorCreate)-> Author:   
        db_author = Author(name = data_author.name)
        self.db.add(db_author)
        self.db.commit()
        self.db.refresh(db_author)
        return db_author
    
    def update(self, db_author:Author, update_author:AuthorUpdate) -> Author:
        update_data = update_author.model_dump(exclude_unset=True)
        for key, value in update_author:
            setattr(db_author, key, value)
        self.db.commit()
        self.db.refresh(db_author)
        return db_author
    def delete(self, db_author: Author)->Author:
        self.db.delete(db_author)
        self.db.commit()
        return db_author
    