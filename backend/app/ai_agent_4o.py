import openai
import os
import json
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

# Load OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Extract the order numbers from the user message using GPT
def extract_order_numbers_gpt(user_message: str):
    """Use GPT (e.g., gpt-4o-mini) to extract order numbers from a user message and enforce JSON output."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use gpt-4o-mini model for better structured responses
            messages=[{
                "role": "system",
                "content": "Extract all 4-digit order numbers from the user message. "
                           "Only return a JSON object with an array called 'order_numbers', like this: "
                           "{\"order_numbers\": [\"4620\"]}. Do NOT include any extra text."
            }, {
                "role": "user",
                "content": user_message
            }],
            temperature=0
        )

        # Debugging: Print the entire raw response to understand structure
        print("Raw Response from GPT-4o-mini:", response)

        # Correctly extract the content from the response
        res_formatted = response.model_dump()
        extracted_data = res_formatted['choices'][0]["message"]['content']  # Correct attribute access
        print("Extracted Data:", extracted_data)  # Debug output
        
        # Try parsing the extracted data as JSON if it is a valid string
        if isinstance(extracted_data, str):
            try:
                extracted_json = json.loads(extracted_data)
                print("Parsed JSON:", extracted_json)  # Debug output
                if "order_numbers" in extracted_json:
                    return extracted_json["order_numbers"]
            except json.JSONDecodeError:
                print("Error: Could not parse response as JSON.")
                return []
        
        print("Error: Invalid or unformatted response.")
        return []
    
    except Exception as e:
        print("Exception Occurred:", str(e))
        return []

# Check the order status using vision (single image per order)
def check_order_status_with_vision(order_image: str, user_message: str):
    """Function to check the order status using GPT-4o-mini with vision capabilities."""
    
    try:
        # Construct messages properly
        content = [{
            "type": "text", 
            "text": f"Please analyze this order image and determine the order status. {user_message}"
        }]
        
        # Append the single image
        content.append({
            "type": "image_url",
            "image_url": {"url": order_image}
        })

        messages = [
            {"role": "system", "content": """
                Note: when responding just respond with the order status.
                You are Nike's AI Customer Support Assistant responsible for analyzing product image submissions. 
                Your primary function is to assess customer-submitted images of Nike products and determine appropriate resolution paths based on visible defects 
                or issues. When analyzing images:
                If clear defects or damage are visible, suggest one of the following resolutions:
                Return/Replace: For manufacturing defects, incorrect items, or damaged products that can be exchanged
                Refund: For cases where replacement isn't suitable or available
                If no defects are visible or the issue requires additional context beyond what's in the image, let the user know you will escalate to human customer support you do not need to provide a full explaination.
                Maintain Nike's brand voice while providing clear, concise analysis and recommendations. Focus on customer satisfaction while following
                company policies for returns and exchanges.).
                """},
            {"role": "user", "content": content},
        ]

        # Make the API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=150
        )

        # Extract the assistant's response
        assistant_message = response.choices[0].message.content
        return assistant_message

    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, there was an error processing your request."
    
# Function to classify the user's intent
def classify_intent(user_message: str):
    """Classify the user's intent into one of the following: 
    'General Talk' 
    'Recommendation' 
    'Order Status'
    'None'"""
    
    # Use GPT-4o-mini or simple keyword-based classification for intent detection
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Classify the user's intent into one of the following categories: 'General Talk', 'Recommendation', 'Order Status', 'None'. Please only return one of these categories based on the user's message. Note: a user saying they want to buy shoes without specifying what type of shoes is too broad to classify as 'Recommendation' rather leave it to 'general talk'"},
                {"role": "user", "content": user_message}
            ]
        )

        res = response.model_dump()
        # Extract the assistant's response
        assistant_message = res['choices'][0]['message']['content'].strip()
        return assistant_message
    
    except Exception as e:
        print(f"Error: {e}")
        return "Error classifying intent."
    
# Function to handle General Talk
def handle_general_talk(user_message: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a support agent your role is to serve as an introductor, you can reply to initial messages and find out how you can help customers and reply to basic messages like thank you, nothing more and nothing less e.g(customer: Hi, introductor: Hello, how can i help you or customer: i want some shoes, introductor: What would type of shoes are you looking for  )"},
                {"role": "user", "content": user_message}
            ]
        )

        res = response.model_dump()
        # Extract the assistant's response
        assistant_message = res['choices'][0]['message']['content'].strip()
        return assistant_message
    
    except Exception as e:
        print(f"Error: {e}")
        return "Error with general talk."