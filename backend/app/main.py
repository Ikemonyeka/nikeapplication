from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.responses import StreamingResponse
from .database import SessionLocal, engine
from .models import Item, Order, OrderStatusEnum  # Updated to use correct models
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import asyncio
from langchain.schema import HumanMessage, AIMessage, BaseMessage
import logging
from .embeddinghelper import generate_embedding
from pydantic import BaseModel
import json
from .recommendation_engine import recommend_items

# Initialize FastAPI app
app = FastAPI()

# Initialize LangChain agent (OpenAI)
llm = ChatOpenAI(model="gpt-4o-mini")
prompt_template = "Given the following products, which ones match best the query: {query}. Products: {products}"
prompt = PromptTemplate(input_variables=["query", "products"], template=prompt_template)
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

# Stream response generator (for AI recommendation)
async def stream_response(query: str, products: str):
    # Get recommendation from LangChain agent
    result = llm_chain.run({"query": query, "products": products})
    
    # Break the result into words and yield them one by one
    for word in result.split():
        yield word + " "
        await asyncio.sleep(0.1)  # Slight delay to simulate streaming

# Setup logging
logging.basicConfig(level=logging.INFO)

@app.get("/recommend-old")
async def recommend(query: str = Query(..., min_length=1, description="User's query for recommendations")):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    logging.info(f"Received recommendation request: {query}")
    
    input_messages = [HumanMessage(content=query)]
    
    def generate_response():
        try:
            for chunk in llm.stream(input_messages):  # ✅ Pass messages directly
                if isinstance(chunk, AIMessage) and chunk.content:
                    yield chunk.content  # ✅ Stream valid response chunks
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            yield "An error occurred while processing your request."

    return StreamingResponse(generate_response(), media_type="text/plain")
# Endpoint for checking order status
@app.get("/order-status/{order_number}")
async def order_status(order_number: str, db: Session = Depends(get_db)):
    # Query the order by order_number
    order = db.query(Order).filter(Order.order_number == order_number).first()
    
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Get order status and related item details
    item = db.query(Item).filter(Item.id == order.item_id).first()
    order_details = {
        "order_number": order.order_number,
        "status": order.status.value,
        "item_name": item.name,
        "item_category": item.category,
        "item_price": item.price,
        "item_image": item.image_url
    }
    
    return order_details

# Helper function to query items for AI agent from the database
def get_items_for_query(db: Session):
    items = db.query(Item).all()
    return items

# Endpoint for creating a new order (for testing purposes)
@app.post("/create-order/")
async def create_order(order_number: str, item_id: int, db: Session = Depends(get_db)):
    # Create new order in the database
    order = Order(order_number=order_number, item_id=item_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return {"order_number": order.order_number, "status": order.status.value}

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
async def get_recommendations(input_data: QueryInput, db: Session = Depends(get_db)):
    user_query = input_data.query
    recommended_items = recommend_items(user_query, db)
    
    # Prepare the response in a friendly format
    recommendations = [
        {"name": item.name, "category": item.category, "price": item.price, "image_url": item.image_url}
        for item in recommended_items
    ]
    
    return {"query": user_query, "recommendations": recommendations}