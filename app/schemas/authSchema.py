from pydantic import BaseModel
from typing import Optional


class CreateUserRequest(BaseModel):
    username: str
    password: str
    is_admin: Optional[bool] = False


class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
