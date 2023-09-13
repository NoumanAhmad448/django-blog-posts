from fastapi import FastAPI,Depends
from models.UserModel import get_user_by_userid
from models.PostModel import  get_post_by_id
from constants import Constant
from db import get_db
from sqlalchemy.orm import Session

app = FastAPI()


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
