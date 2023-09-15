from sqlalchemy import Boolean, Column, DateTime, Integer, String, select
from db import Base
from sqlalchemy.orm import Session,aliased
from fastapi.responses import JSONResponse
class User(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    email = Column(String(254), unique=True)
    password = Column(String(128))
    last_login = Column(DateTime)
    username = Column(String(150), unique=True, index=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    is_staff = Column(Boolean, nullable=True)
    is_active = Column(Boolean, nullable=True)
    date_joined = Column(DateTime)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

def get_user_by_userid(db: Session, user_id: int):
    u = aliased(User)
    results = db.execute(
        select(u).where(u.id == user_id)
    ).scalars().first()

    if results is not None:
        user = results
        del user.password
        if not user.is_staff:
            del user.is_staff

        return user
    else:
        return JSONResponse({"detail": "record not found",
                             "is_succes" : False})