from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.courses import router as courses_router
from app.api.routes.lessons import router as lessons_router




app = FastAPI(title="Learnify AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(courses_router)
app.include_router(lessons_router)



@app.on_event("startup")
def startup():
    # Creates tables (currently none) and verifies DB connection works
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}
