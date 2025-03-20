# app/schemas.py
from pydantic import BaseModel
from typing import List

class ItemResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    image_url: str

    class Config:
        orm_mode = True

class ProductRecommendationResponse(BaseModel):
    recommendation: str
    products: List[ItemResponse]

class OrderResponse(BaseModel):
    order_number: str
    order_images: str


# Pydantic model for the user input
class QueryInput(BaseModel):
    query: str

# Pydantic model for input validation
class ItemCreate(BaseModel):
    name: str
    description: str
    category: str
    image_url: str
    price: float
    gender: str

# Pydantic model for input validation
class OrderCreate(BaseModel):
    order_number: str
    order_images: str