from sqlalchemy import Boolean, Column, DateTime, Integer, String, select,label,func,update,literal_column
from db import Base
from sqlalchemy.orm import Session,aliased
from fastapi.responses import JSONResponse
import settings
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
    fields = [u.first_name,u.last_name.label("family_name")]
    if True:
        fields.append(u.id.label("main_id"))
    if True:
        fields.append(label(element=u.username,name="user_name"))
    fields.append(literal_column("''").label("q"))
    fields.append(func.concat(u.first_name, ' ', u.last_name).label("full_name"))
    q = select(*fields).select_from(u).where(u.id == user_id).order_by(u.id.desc())
    results = db.execute(
        q
    ).mappings().first()
    result = {}
    if settings.DEBUG:
        result["query"] = str(q)

    if results is not None:
        result['results'] = results
        return result
    else:
        return JSONResponse({"detail": "record not found",
                             "is_succes" : False})

def update_user_by_userid(db: Session, user):
    u = aliased(User)
    q = select(u.id).select_from(u).where(u.username == user.username)
    results = db.execute(q).mappings().first()

    if results is not None:
        values= {}
        if user.email is not None:
            values['email'] = user.email
        if len(values) > 0:
            update_user_q = update(u).where(u.username==user.username).values(**values)
            try:
                db.execute(update_user_q)
                return JSONResponse({"is_success" : True})
            except:
                return JSONResponse({"detail": "something went wrong",
                             "is_success" : False})
        else:
            return JSONResponse({"detail": "no parameter is provided to update the record",
                             "is_success" : False})
    else:
        return JSONResponse({"detail": "record not found",
                             "is_success" : False})

