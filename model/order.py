from pydantic import BaseModel
from typing import List, Optional
from model.address import Address
from model.product import CartProduct

class Order(BaseModel):
    id: Optional[str] = None
    orderId: int
    userId: str
    orderStatus: str
    address: Address
    products: List[CartProduct]
    totalPrice: float
    dateOrder: str