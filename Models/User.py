from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    userName: str
    fullName: str
    email: EmailStr
    password: str
    DoB: datetime
    gender: str
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

