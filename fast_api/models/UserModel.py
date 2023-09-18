from sqlalchemy import Boolean, Column, DateTime, Integer, String, select,label,func,update,literal_column,bindparam
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
    is_superuser = Column(Boolean, nullable=True)
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
    fields.append(u.email)
    fields.append(literal_column("''").label("q"))
    fields.append(func.concat(u.first_name, ' ', u.last_name).label("full_name"))
    fields.append(u.is_staff)
    fields.append(u.is_superuser)

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
        return JSONResponse({"detail": "user not found",
                             "is_success" : False})

def update_user_by_userid(db: Session, user):
    u = aliased(User)
    q = select(u.id,u.last_name).select_from(u).where(u.username == user.username)
    results = db.execute(q).mappings().first()

    if results is not None:
        values= {"id" : results.id, "user_id": results.id}
        if user.email is not None:
            values['email'] = user.email
        if user.first_name is not None:
            values['first_name'] = user.first_name

        if user.last_name is not None:
            values['last_name'] = user.last_name
        else:
            values['last_name'] = results.last_name
        # return {"update" : values }
        if len(values) > 0:
            # this condition is set to false to test custom needs
            if False:
                update_user_q = update(u).where(u.id== results.id).values(**values)
            update_user_q = update(u).where(u.id == bindparam("user_id")).values(
                            email=bindparam("email"),
                            first_name=bindparam("first_name"), last_name=bindparam("last_name")).execution_options(
                            synchronize_session=None)
            db.execute(update_user_q, [
                values]
                )
            db.commit()
            return JSONResponse({"is_success" : True, "query" : str(update_user_q), "results" : results.id})
        else:
            return JSONResponse({"detail": "no parameter is provided to update the record",
                             "is_success" : False})
    else:
        return JSONResponse({"detail": "record not found",
                             "is_success" : False})

