from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Item, Order
from .embeddinghelper import generate_embedding
from .recommendation_engine import recommend_items
from .schemas import OrderCreate, ItemCreate, QueryInput
from .ai_agent_4o import extract_order_numbers_gpt, check_order_status_with_vision, classify_intent, handle_general_talk
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Allow all origins (not recommended for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint for creating a new order (for testing purposes)
@app.post("/create-order/")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Create new order in the database
    order = Order(order_number=order.order_number, order_images=order.order_image)
    db.add(order)
    db.commit()
    db.refresh(order)
    return {"order_number": order.order_number, "message": "order stored successfully"}

@app.post("/items/")
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    # Generate embedding using the description of the item
    embedding_json = generate_embedding(item.description, item.price, item.category)
    
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
    
    return {"message": "Item created successfully", "item": new_item}

@app.post("/recommendations/")
async def get_recommendations(input_data: str, db: Session = Depends(get_db)):

    #user_query = input_data.query
    recommended_items = recommend_items(input_data, db)
    
    # Prepare the response in a friendly format
    recommendations = [
        {"name": item.name, "category": item.category, "price": item.price, "image_url": item.image_url}
        for item in recommended_items
    ]
    
    return {"query": input_data, "recommendations": recommendations}

# FastAPI route for checking order status
@app.post("/get-order/")
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


@app.post("/ai-agent/")
async def agent(user_message: str, db: Session = Depends(get_db)):
    intent = classify_intent(user_message)

    if "General Talk" in intent:
        return handle_general_talk(user_message)
    elif "Recommendation" in intent:
        return await get_recommendations(user_message, db)
    elif "Order Status" in intent:
        return await get_order(user_message, db)
    else:
        return "Sorry, I couldn't understand your request. Could you please clarify?"

























# @app.post("/get-order/")
# async def get_order(user_message: str, db: Session = Depends(get_db)):
#     # Extract order numbers using GPT-4o-mini
#     order_numbers = extract_order_numbers_gpt(user_message)
#     print(order_numbers)
    
#     if not order_numbers:
#         raise HTTPException(status_code=400, detail="No valid order number found in the message")
    
#     # Retrieve orders from the database
#     orders = db.query(Order).filter(Order.order_number.in_(order_numbers)).all()
    
#     # Create a dictionary of the found orders for easier access
#     orders_dict = {order.order_number: order for order in orders}
    
#     # Prepare the result list
#     result = []
    
#     for order_number in order_numbers:
#         # If order exists in the database, add it to the result
#         if order_number in orders_dict:
#             order = orders_dict[order_number]
#             result.append({
#                 "order_number": order.order_number,
#                 "order_images": order.order_images
#             })
#         else:
#             # If order doesn't exist, add it with null for order_images
#             result.append({
#                 "order_number": order_number,
#                 "order_images": None
#             })
    
#     return result


# @app.get("/recommend-old")
# async def recommend(query: str = Query(..., min_length=1, description="User's query for recommendations")):
#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty")

#     logging.info(f"Received recommendation request: {query}")
    
#     input_messages = [HumanMessage(content=query)]
    
#     def generate_response():
#         try:
#             for chunk in llm.stream(input_messages):  # ✅ Pass messages directly
#                 if isinstance(chunk, AIMessage) and chunk.content:
#                     yield chunk.content  # ✅ Stream valid response chunks
#         except Exception as e:
#             logging.error(f"Error generating response: {e}")
#             yield "An error occurred while processing your request."

#     return StreamingResponse(generate_response(), media_type="text/plain")