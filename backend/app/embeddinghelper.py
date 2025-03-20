import openai
import os
import json

# Ensure you have your OpenAI API key in your environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_embedding(description: str, price: float, category: str, gender: str):
    """
    Generate an embedding for the combined fields: description, price, and category.
    """
    try:
        # Combine fields into one string
        combined_text = f"Description: {description}, Price: {price}, Category: {category}, Gender: {gender}"
        print(f"Generating embedding for: {combined_text}")  # Debugging output

        # NEW API CALL FORMAT
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=[combined_text]  # Must be a list
        )
        
        print(f"API Response: {response}")  # Debugging output

        # Extract the embedding correctly
        embedding = response.data[0].embedding  # New API format

        return json.dumps(embedding)  # Convert to JSON string for storage
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return json.dumps([])  # Return empty JSON array if there's an error

# Function to get embeddings
def get_embedding(text):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def get_query_embedding(user_query):
    return get_embedding(user_query)