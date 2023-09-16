from sqlalchemy import Boolean, Column, DateTime, Integer, String, select, ForeignKey,func,and_
from db import Base
from sqlalchemy.orm import Session,Mapped,relationship,aliased,mapped_column,selectin_polymorphic
from fastapi.responses import JSONResponse
from fastapi import status, Response
from models.UserModel import User
import settings

class Post(Base):
    __tablename__ = "create_posts"

    id :Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    source :Mapped[str] = mapped_column(String(100))
    title :Mapped[str] = mapped_column(String(500))
    tags:Mapped[str] = mapped_column(String(500))
    descrip :Mapped[str] = mapped_column(String(10000))
    should_display :Mapped[bool] = mapped_column(Boolean)
    created_at :Mapped[DateTime] = mapped_column(DateTime)
    updated_at :Mapped[DateTime] = mapped_column(DateTime)
    user_id :Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
    user :Mapped[User] = relationship(User)


def get_post_by_id(db: Session, post_id: int):
    try:
        p = aliased(Post)
        u = aliased(User)
        if settings.NOT_PRO_LESS:
            results = db.scalar(
                select(p).join(p.user_id.and_(u.is_active == True)).where(p.id == post_id)
            ).first()
        else:
            results = db.scalar(
                select(p,u)
                .join(u)
                .where(and_(p.id == post_id,p.should_display == 1))
                .order_by(p.id)
            )

        stmt  = select(func.count("*").label("total_count")).select_from(u)
        total_count = db.scalar(stmt)

        if results is not None:
            if settings.DEBUG:
                pass
            results.total_count = total_count
            return results
        else:
            return JSONResponse({"detail": "record not found",
                                "is_succes" : False}, status_code=status.HTTP_400_BAD_REQUEST)
    except:
        return JSONResponse({"detail": "something went wrong",
                "is_succes" : False
            },status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def get_has_post_users(db: Session,default_post: int):
    u = aliased(User)
    p = aliased(Post)

    subq = (
     select(func.count(p.id))
        .where(u.id == p.user_id)
        .group_by(p.user_id)
        .having(func.count(p.user_id) > default_post)
     ).exists()


    q = [u.id]
    if True:
        q.append(u.email)

    if True:
        q.append(u.username)

    results= db.execute(select(*q).select_from(u).where(subq)).mappings().all()
    if len(results) > 0:
        return results
    else:
        return JSONResponse({"detail": "record not found",
        "is_succes" : False}, status_code=status.HTTP_200_OK)

def get_users_without_posts(db: Session,default_post: int):
    u = aliased(User)
    p = aliased(Post)

    subq = (
     select(func.count(p.id))
        .where(u.id == p.user_id)
        .group_by(p.user_id)
        .having(func.count(p.user_id) > default_post)
     ).exists()


    q = [u.id]
    if True:
        q.append(u.email)

    if True:
        q.append(u.username)

    results= db.execute(select(*q).select_from(u).where(~subq)).mappings().all()
    if len(results) > 0:
        return results
    else:
        return JSONResponse({"detail": "record not found",
        "is_succes" : False}, status_code=status.HTTP_200_OK)

