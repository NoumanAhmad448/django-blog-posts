from sqlalchemy import Boolean, Column, DateTime, Integer, String
from db import Base
from sqlalchemy.orm import Session

class User(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    last_login = Column(Boolean, default=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    is_staff = Column(Boolean)
    is_active = Column(Boolean)
    date_joined = Column(DateTime)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

def get_user_by_userid(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()