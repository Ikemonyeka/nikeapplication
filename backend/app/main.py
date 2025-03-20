from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .ai_agent_4o import classify_intent, handle_general_talk
from fastapi.middleware.cors import CORSMiddleware
from .services import get_recommendations, get_order
from .seed_data import seed_items, seed_orders

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

# Run tasks on startup
@app.on_event("startup")
async def startup_event():
    # Create a new session for seeding
    db = SessionLocal()

    # Seed items and orders on startup if the tables are empty
    try:
        await seed_items(db)
        await seed_orders(db)
    finally:
        db.close()

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