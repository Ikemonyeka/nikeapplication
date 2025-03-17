# recommendation_engine.py

import json
from .embeddinghelper import get_query_embedding
from .cosine_similarity import cosine_similarity
from .models import Item  # Assuming you have a file models.py for the Item SQLAlchemy model

# Function to recommend items based on user query
def recommend_items(user_query, db_session, top_n=5, similarity_threshold=0.2):
    query_embedding = get_query_embedding(user_query)
    
    items = db_session.query(Item).all()
    recommendations = []
    
    for item in items:
        item_embedding = json.loads(item.embedding)  # Convert JSON string back to list
        similarity = cosine_similarity(query_embedding, item_embedding)
        
        # Only add items with similarity above the threshold
        if similarity >= similarity_threshold:
            recommendations.append((item, similarity))
    
    # Sort items by similarity score (highest first)
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    # Return top N recommendations
    return [item[0] for item in recommendations[:top_n]]
