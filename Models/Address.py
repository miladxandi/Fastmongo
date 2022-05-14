from pydantic import BaseModel


class Address(BaseModel):
    streetName: str
    streetNumber: str
    district: str
    city: str
