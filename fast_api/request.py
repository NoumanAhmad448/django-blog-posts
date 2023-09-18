from pydantic import BaseModel,Field,field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
from typing import List

class UserRequest(BaseModel):
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None

class PostInsertRequest(BaseModel):
    source:str
    title :str = Field(max_length=500,min_length=5)
    tags:str = Field(max_length=500,min_length=2)
    descrip :str = Field(max_length=10000)
    user_id :int

    @field_validator("source")
    def validate_source(cls, v: str)->str:
        if v not in ["api",'web']:
            raise ValueError("source must be api or web")
        return v

    class Config:
        error_msg_templates = {
            'string_too_short.title': 'post title must be atleast 5 character',
        }

