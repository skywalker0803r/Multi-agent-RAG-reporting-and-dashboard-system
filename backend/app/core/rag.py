import os
import openai
from pinecone import Pinecone
import google.generativeai as genai
from app.core.config import settings

# Initialize OpenAI for embeddings
openai.api_key = settings.OPENAI_API_KEY

# Initialize Pinecone
pinecone_client = Pinecone(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENVIRONMENT)

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 512 # Updated dimension to match user's Pinecone index

def get_embedding(text: str) -> list[float]:
    """Generates an embedding for the given text using OpenAI's model."""
    response = openai.embeddings.create(input=text, model=EMBEDDING_MODEL, dimensions=EMBEDDING_DIMENSION)
    return response.data[0].embedding

def get_pinecone_index(index_name: str) -> Pinecone.Index:
    """Returns a Pinecone index instance."""
    print(pinecone_client.list_indexes())
    if not any(idx['name'] == index_name for idx in pinecone_client.list_indexes()):
        # In a real application, you might create the index here or handle it externally.
        raise ValueError(f"Pinecone index '{index_name}' does not exist.")
    return pinecone_client.Index(index_name)

def get_llm_response(prompt: str, context: str) -> str:
    """Generates a response from the LLM given a prompt and context."""
    model = genai.GenerativeModel('gemini-2.5-flash') # Using gemini-pro for text generation
    full_prompt = f"""You are an AI assistant for a retail chain. 
    Based on the following context, answer the question or generate insights. 
    Provide citations from the context if possible.

    Context: {context}

    Question/Task: {prompt}

    Answer:"""
    response = model.generate_content(full_prompt)
    return response.text