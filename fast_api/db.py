from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import settings


DB_URL = settings.DATABASE_URL

if settings.DEBUG:
    engine = create_engine(
        DB_URL, echo= True
    )
else:
    engine = create_engine(
        DB_URL
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()