from fastapi import FastAPI
from app.api.book import router as book_router
from app.api.author import router as author_router
from app.api.category import router as category_router
from app.api.user import router as user_router
from app.api.borrow import router as borrow_router
from app.core.database import verify_db_connection
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Checking database connection...")
    verify_db_connection()
    yield

    print("Shutting down application...")
app = FastAPI(
    title="Library API",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(book_router)
app.include_router(author_router)
app.include_router(category_router)
app.include_router(user_router)
app.include_router(borrow_router)

@app.get("/")
def root():
    return {"message":"Library API is running"}