from fastapi import FastAPI,Depends
from models.UserModel import get_user_by_userid

from db import SessionLocal, engine, Base
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api")
async def root():
    return {"message": "Hello World"}

@app.get("/api/user/{user_id}")
def root(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_userid(user_id=user_id,db=db)
