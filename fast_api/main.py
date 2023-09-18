from fastapi import FastAPI,Depends
from models.UserModel import get_user_by_userid,update_user_by_userid
from models.PostModel import  get_post_by_id,get_has_post_users,get_users_without_posts,insert_post
from constants import Constant
from db import get_db
from sqlalchemy.orm import Session
from exception_handlers import unhandled_exception_handler
from request import UserRequest,PostInsertRequest

app = FastAPI()

app.add_exception_handler(Exception, unhandled_exception_handler)

@app.get(f"{Constant.API_V1}")
async def root():
    return {"message": "Hello World"}

# /api/user/{user_id}
@app.get("{}user/{{user_id}}".format(Constant.API_V1,user_id=Constant.USER_ID))
def root(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_userid(user_id=user_id,db=db)

@app.get("{}get_post/{{post_id}}".format(Constant.API_V1,post_id="post_id"))
def root(post_id: int,db : Session = Depends(get_db)):
    return get_post_by_id(post_id=post_id,db=db)

@app.get("{}get_has_post_users".format(Constant.API_V1))
def root(default_post: int=1,db : Session = Depends(get_db)):
    return get_has_post_users(default_post=default_post,db=db)

@app.get("{}get_users_without_posts".format(Constant.API_V1))
def root(default_post: int=0,db : Session = Depends(get_db)):
    return get_users_without_posts(default_post=default_post,db=db)

@app.post("{}update_user_by_userid".format(Constant.API_V1))
def root(user : UserRequest,db : Session = Depends(get_db)):
    return update_user_by_userid(user=user,db=db)

@app.post("{}insert_post".format(Constant.API_V1))
def root(post : PostInsertRequest,  db : Session = Depends(get_db)):
    return insert_post(post=post,db=db)
