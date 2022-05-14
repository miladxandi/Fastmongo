from datetime import datetime

from pydantic import BaseModel
from Helpers.Features.Classes import objectid


class AccessToken(BaseModel):
    access_token: str
    user_id: objectid
