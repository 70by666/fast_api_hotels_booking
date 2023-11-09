from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SAuthRegisterLogout(BaseModel):
    status: str
    data: None
    details: None


class SToken(BaseModel):
    access_token: str


class SAuthLogin(BaseModel):
    status: str
    data: SToken
    details: None


class SUser(BaseModel):
    id: int
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime


class SMe(BaseModel):
    status: str
    data: SUser
    details: None


class SUsers(BaseModel):
    password: str
    id: int
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime


class SAllUsers(BaseModel):
    status: str
    data: list[SUsers]
    details: None
