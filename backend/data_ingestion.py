import os
import pandas as pd
import openai
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

# --- Configuration --- #
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT") # Not directly used for ServerlessSpec

INDEX_NAME = "retail-data-index"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 512 # Updated dimension to match user's Pinecone index

# --- Initialize Clients --- #
openai.api_key = OPENAI_API_KEY
pinecone_client = Pinecone(api_key=PINECONE_API_KEY) # Environment not needed for Serverless client init

# --- Helper Functions --- #
def get_embedding(text: str) -> list[float]:
    """Generates an embedding for the given text using OpenAI's model."""
    if not text or not isinstance(text, str):
        return []
    try:
        response = openai.embeddings.create(input=text, model=EMBEDDING_MODEL, dimensions=EMBEDDING_DIMENSION)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding for text: {text[:50]}... Error: {e}")
        return []

def process_and_upsert_csv(file_path: str, index: Pinecone.Index, batch_size: int = 100, max_rows: int = None):
    """Processes a CSV file, generates embeddings, and upserts to Pinecone.

    Args:
        file_path (str): Path to the CSV file.
        index (Pinecone.Index): Pinecone index instance.
        batch_size (int): Number of vectors to upsert in each batch.
        max_rows (int, optional): Maximum number of rows to process. Defaults to None (process all rows).
    """
    print(f"\nProcessing {file_path}... (Max rows: {max_rows if max_rows else 'All'})")
    df = pd.read_csv(file_path).sample(max_rows) # Read only up to max_rows
    df = df.fillna('') # Fill NaN values with empty string for text processing

    # Dynamically determine id_column
    if df.index.name:
        id_column = df.index.name
    else:
        # Assume the first column is the ID column if index is not named
        id_column = df.columns[0]

    # Dynamically determine text_columns (all object/string columns, excluding id_column)
    text_columns = [col for col in df.columns if df[col].dtype == 'object' and col != id_column]

    data_to_upsert = []
    for i, row in df.iterrows():
        unique_id = str(row[id_column])
        if file_path == "./warranty-claims.csv":
            temp_texts = []
            for col in text_columns:
                if col in row and str(row[col]).strip():
                    if '_Issue' in col: # Check if it's an issue column (e.g., AC_1001_Issue)
                        product_id = col.replace('_Issue', '')
                        temp_texts.append(f"{product_id} issue: {str(row[col])}")
                    else: # For Call_details and Purpose
                        temp_texts.append(str(row[col]))
            combined_text = " ".join(temp_texts)
        else:
            combined_text = " ".join([str(row[col]) for col in text_columns if col in row])
        
        if not combined_text.strip():
            print(f"Skipping row {unique_id} due to empty combined text.")
            continue

        embedding = get_embedding(combined_text)
        if not embedding:
            print(f"Skipping row {unique_id} due to embedding generation error.")
            continue

        # Prepare metadata (excluding the text itself to save space, but include other useful info)
        metadata = row.drop(text_columns).to_dict()
        metadata['original_text'] = combined_text # Keep original text for RAG context

        data_to_upsert.append((unique_id, embedding, metadata))

        if len(data_to_upsert) >= batch_size:
            print(f"Upserting batch of {len(data_to_upsert)} from {file_path}...")
            index.upsert(vectors=data_to_upsert)
            data_to_upsert = []
    
    # Upsert any remaining vectors
    if data_to_upsert:
        print(f"Upserting final batch of {len(data_to_upsert)} from {file_path}...")
        index.upsert(vectors=data_to_upsert)
    
    print(f"Finished processing {file_path}.")

# --- Main Execution --- #
if __name__ == "__main__":
    # Directly initialize the index, assuming it already exists
    pinecone_index = pinecone_client.Index(INDEX_NAME)
    print(f"Pinecone index '{INDEX_NAME}' initialized.")

    # --- Configure your CSV files and columns here --- #
    warranty_claims_file = "./warranty-claims.csv"
    
    

    product_sales_returns_file = "./retail_sales_dataset.csv"
    
    

    # --- Run processing for each dataset --- #
    # Make sure these CSV files are in the same directory as this script, or provide full paths.
    
    # Process Warranty Claims Data
    if os.path.exists(warranty_claims_file):
        process_and_upsert_csv(warranty_claims_file, pinecone_index, max_rows=1000)
    else:
        print(f"Warning: {warranty_claims_file} not found. Skipping warranty data ingestion.")

    # Process Product Sales and Returns Data
    if os.path.exists(product_sales_returns_file):
        process_and_upsert_csv(product_sales_returns_file, pinecone_index, max_rows=1000)
    else:
        print(f"Warning: {product_sales_returns_file} not found. Skipping product sales/returns data ingestion.")

    print("\nData ingestion process completed.")
