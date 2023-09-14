from sqlalchemy import Boolean, Column, DateTime, Integer, String, select, ForeignKey
from db import Base
from sqlalchemy.orm import Session,Mapped,relationship,aliased,mapped_column,selectin_polymorphic,with_polymorphic
from fastapi.responses import JSONResponse
from fastapi import status
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
    user :Mapped[str] = relationship(User)


def get_post_by_id(db: Session, post_id: int):
    try:
        p = aliased(Post)
        u = aliased(User)

        if settings.NOT_PRO_LESS:
            results = db.scalars(
                select(p).join(p.user_id.and_(u.is_active == True)).where(p.id == post_id)
            ).first()
        else:
            results = db.scalar(
                select(p,u)
                .where(p.id == post_id)
                .order_by(p.id)
                .options(
                    selectin_polymorphic(p, [u]),
                )
            )

        if results is not None:
            return results
        else:
            return JSONResponse({"detail": "record not found",
                                "is_succes" : False}, status_code=status.HTTP_400_BAD_REQUEST)
    except:
        return JSONResponse({"detail": "something went wrong",
                "is_succes" : False
            },status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )