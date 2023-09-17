from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None