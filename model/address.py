from pydantic import BaseModel

class Address(BaseModel):
    addressTitle: str
    fullName: str
    phone: str
    city: str
    street: str
    state: str