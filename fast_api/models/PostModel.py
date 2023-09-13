from sqlalchemy import Boolean, Column, DateTime, Integer, String, select, ForeignKey
from db import Base
from sqlalchemy.orm import Session,mapped_column
from .UserModel import User

class Post(Base):
    __tablename__ = "create_posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source = Column(String(100))
    title = Column(String(500))
    tags = Column(String(500))
    descrip = Column(String(10000))
    should_display = Column(Boolean, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    user_id = mapped_column(Integer, ForeignKey(f"{User.__tablename__}.id"))


def get_post_by_id(db: Session, post_id: int):
    try:
        results = db.execute(
        select(Post)
    )
    

        for Post in results:
            return Post
        
    except Exception:
        print(Exception)

