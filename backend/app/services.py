from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Item, Order
from .embeddinghelper import generate_embedding
from .recommendation_engine import recommend_items
from .schemas import OrderCreate, ItemCreate
from .ai_agent_4o import extract_order_numbers_gpt, check_order_status_with_vision

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Create new order in the database
    new_order = Order(order_number=order.order_number, order_images=order.order_images)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"order_number": new_order.order_number, "message": "order stored successfully"}

async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    # Generate embedding using the description of the item
    embedding_json = generate_embedding(item.description, item.price, item.category, item.gender)
    
    # Create a new Item object and save it to the database
    new_item = Item(
        name=item.name,
        description=item.description,
        category=item.category,
        price=item.price,
        gender=item.gender,
        image_url=item.image_url,
        embedding=embedding_json  # Store the embedding as a JSON string
    )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return {"message": "Item created successfully", "item": new_item.id}

async def get_recommendations(input_data: str, db: Session = Depends(get_db)):

    #user_query = input_data.query
    recommended_items = recommend_items(input_data, db)
    
    # Prepare the response in a friendly format
    recommendations = [
        {"name": item.name, "category": item.category, "price": item.price, "image_url": item.image_url}
        for item in recommended_items
    ]
    
    return {"query": input_data, "recommendations": recommendations}

async def get_order(user_message: str, db: Session = Depends(get_db)):
    # Step 1: Extract order number from the user's message (only one order at a time)
    order_numbers = extract_order_numbers_gpt(user_message)
    if not order_numbers:
        raise HTTPException(status_code=400, detail="No valid order number found in the message")

    # Step 2: Retrieve the order from the database based on extracted order number
    order_number = order_numbers[0]  # We're only handling one order at a time
    order = db.query(Order).filter(Order.order_number == order_number).first()

    if not order:
        raise HTTPException(status_code=404, detail="No matching order found")

    # Step 3: Evaluate the order using GPT-4o-mini Vision and get status message directly
    status_message = check_order_status_with_vision(order.order_images, user_message)

    # Step 4: Return the response directly from GPT-4o-mini's result
    return {
        "order_number": order.order_number,
        "order_images": order.order_images,
        "status": status_message
    }
