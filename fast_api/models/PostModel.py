from sqlalchemy import Boolean, insert, DateTime, Integer, String, select, ForeignKey,func,and_,Column,String
from sqlalchemy.orm import Session,Mapped,relationship,aliased,mapped_column,registry,DeclarativeBase
import enum
from typing_extensions import Annotated
from fastapi.responses import JSONResponse
from fastapi import status
from models.UserModel import User,get_user_by_userid
import settings
from request import PostInsertRequest
from datetime import datetime
from typing import Literal

PostCustomStatus = Literal["web","api"]
str_100 = Annotated[str, 100]
class PostSource(enum.Enum):
    api = "api"
    web = "web"

class DBBase(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str_100: String(100),
        }
    )
class Post(DBBase):
    __tablename__ = "create_posts"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id :Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True,nullable=False)
    # source :Mapped[PostSource]
    source :Mapped[PostCustomStatus]
    title :Mapped[str_100]
    tags:Mapped[str] = mapped_column(String(500))
    descrip :Mapped[str] = mapped_column(String(10000))
    should_display :Mapped[bool] = mapped_column(Boolean)
    created_at :Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    updated_at :Mapped[DateTime] = mapped_column(DateTime)
    user_id :Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
    user :Mapped[User] = relationship(User)


def get_post_by_id(db: Session, post_id: int):
    # try:
    p = aliased(Post)
    u = aliased(User)
    # stmt  = select(func.count("*").label("total_count")).select_from(u).subquery()
    # stmt = aliased(u,stmt)

    q =  select(p,u).select_from(p).outerjoin(u).where(and_(p.id == post_id)).order_by(p.id)

    if settings.NOT_PRO_LESS:
        results = db.scalar(
            select(p).join(p.user_id.and_(u.is_active == True)).where(p.id == post_id)
        ).first()
    else:
        results = db.scalar(
            q
        )

    # total_count = db.scalar(stmt)

    if results is not None:
        # results.total_count = total_count
        if settings.DEBUG:
            results.query = str(q)
        if not results.should_display:
            return JSONResponse({"detail": "record is found but cannot be displayed",
                            "is_success" : False}, status_code=status.HTTP_400_BAD_REQUEST)
        return results
    else:
        return JSONResponse({"detail": "record not found",
                            "is_success" : False}, status_code=status.HTTP_400_BAD_REQUEST)
    # except:
    #     return JSONResponse({"detail": "something went wrong",
    #             "is_succes" : False
    #         },status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )

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

def insert_post(db: Session, post:PostInsertRequest):
    p = aliased(Post)
    q = insert(p)

    user = get_user_by_userid(db=db,user_id=post.user_id,return_dict=True)

    if not isinstance(user,JSONResponse):
        user = user["results"]
        is_staff = user["is_staff"] or user["is_superuser"]
        values= {"should_display": is_staff}
        if post.source is not None:
            values['source'] = post.source
        if post.title is not None:
            values['title'] = post.title

        if post.tags is not None:
            values['tags'] = post.tags

        if post.descrip is not None:
            values['descrip'] = post.descrip

        if post.user_id is not None:
            values['user_id'] = user["main_id"]
        if len(values) > 0:
            # db.execute(q.values(**values)
            #     )
            data= values
            p = Post(**values)
            db.add(p)
            db.commit()
            db.refresh(p)
            data["user"] = user
            return JSONResponse({"is_success" : True, "query" : str(q), "id" : p.id,
                                 "data": data})

        else:
            return JSONResponse({"detail": "no parameter is provided to update the record",
                                "is_success" : False})
    else:
        return user