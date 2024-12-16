from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    id: str
    email: str
    password: str
    firstName: str
    lastName: str
    imagePath: Optional[str] = None
    list_order: Optional[List[str]] = None
    
class UserNewProfile(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    imagePath: Optional[str] = None