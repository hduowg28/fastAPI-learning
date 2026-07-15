from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings


engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass

def verify_db_connection():
    try: 
        with engine.connect() as connection:
            connection.execute(text("select 1"))
            print("Successfully connected to database")
    except Exception as e:
        print("fail to connect with database")      
        print(e)
        raise e

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
