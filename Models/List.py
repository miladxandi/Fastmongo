from typing import Optional

from pydantic import BaseModel

from Models.Address import Address
from Models.User import *
from datetime import datetime


class List(BaseModel):
    type: str
    availableNow: bool
    ownerId: str
    address: Address
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
