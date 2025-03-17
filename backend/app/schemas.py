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
