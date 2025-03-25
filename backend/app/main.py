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
    