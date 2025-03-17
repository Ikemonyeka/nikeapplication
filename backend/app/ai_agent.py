import os
import time
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .models import Item  # Import your Item model

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fetch the API key from the environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI model
llm = ChatOpenAI(model="text-embedding-3-small", openai_api_key=openai_api_key)

# Create a prompt template for product recommendation
template = """
You are an AI assistant helping the user find the best products. The user is looking for shoes based on the following description: "{user_input}"

Here are all the products available in the store:
{products}

Based on the user's input, please rank the products in order of relevance. Return the most relevant products first, and explain why they are a good match for the user's request.
"""

# Create a LangChain prompt with the template
prompt = PromptTemplate(input_variables=["user_input", "products"], template=template)

# Chain the model with the prompt
chain = LLMChain(llm=llm, prompt=prompt)

# Function to get product recommendations based on user input
def get_product_recommendation(user_input: str, db: Session):
    # Query the database to get all available products
    items = db.query(Item).all()

    # If no products found, return a message
    if not items:
        return "Sorry, we couldn't find any products."

    # Prepare the product details for the agent
    product_details = "\n".join([f"{item.name}: {item.description} (Category: {item.category}, Price: ${item.price})" for item in items])

    # Pass the user input and product details to the agent
    result = chain.run(user_input=user_input, products=product_details)

    # Stream the result back to the user incrementally
    result_parts = result.split("\n")
    
    for part in result_parts:
        time.sleep(1)  # Simulate streaming
        yield part  # Stream each part to the user

# FastAPI endpoint to handle user input and get product recommendations
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

app = FastAPI()

@app.post("/recommend")
async def recommend_products(user_input: str, db: Session = Depends(get_db)):
    # Get product recommendations using the AI agent
    recommendations = get_product_recommendation(user_input, db)

    # Stream the results back to the user
    return recommendations
