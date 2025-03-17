# app/crud.py
from sqlalchemy.orm import Session
from . import models

def get_items_by_category(db: Session, category: str):
    return db.query(models.Item).filter(models.Item.category == category).all()
