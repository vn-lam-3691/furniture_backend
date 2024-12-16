from pydantic import BaseModel
from typing import Optional, List

class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float
    offerPercentage: float
    description: str
    colors: list[int]
    description: Optional[str] = None
    colors: Optional[List[int]] = None
    sizes: Optional[List[str]] = None
    images: List[str]

class CartProduct(BaseModel):
    product: Product
    quantity: int
    selectedColor: int
    selectedSize: str