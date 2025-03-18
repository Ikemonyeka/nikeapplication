from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Double, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from .database import Base

Base = declarative_base()

# Enum for order status
class OrderStatusEnum(enum.Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    RETURNED = "Returned"
    REFUNDED = "Refunded"
    ESCALATED = "Escalated"

# Item Model: For storing shoe information
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    category = Column(String)  # e.g., running, walking, gym, etc.
    image_url = Column(String)  # URL to the image
    price = Column(Double)  # Price of the item (in cents or whole number)
    gender = Column(String) # Items are gender specific
    embedding = Column(Text)  # Store the embedding as JSON string (or use BLOB if using actual binary)

# Order Model: For tracking customer orders
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True)  # Unique order number
    order_images = Column(String) #url for images
