from datetime import datetime

from pydantic import BaseModel
from pyparsing import Optional


class AccessToken(BaseModel):
    access_token: str
    user_id: str
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
