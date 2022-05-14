from typing import Optional

from bson import ObjectId
from pydantic import BaseModel

from Helpers.Features.Classes import objectid
from Models.Address import Address
from Models.User import *
from datetime import datetime


class List(BaseModel):
    type: str
    availableNow: bool
    ownerId: Optional[objectid]
    address: Address
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
