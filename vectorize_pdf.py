import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Hugging Face API key from the environment
inference_api_key = os.getenv("HUGGINGFACE_API_KEY")

# Define paths for data and processed files
DATA_DIR = "data/"
PROCESSED_FILES_PATH = "processed_files.json"
VECTOR_STORE_DIR = "vectorstores/db/"

def load_processed_files():
    """Load the list of processed files from JSON file."""
    if os.path.exists(PROCESSED_FILES_PATH):
        with open(PROCESSED_FILES_PATH, "r") as f:
            return set(json.load(f))  # Use a set to avoid duplicates
    return set()

def save_processed_files(processed_files):
    """Save the list of processed files to JSON file."""
    with open(PROCESSED_FILES_PATH, "w") as f:
        json.dump(list(processed_files), f)  # Convert set back to list for JSON serialization

def create_vector_db():
    """Create a vector database from new PDF documents only."""
    # Load the list of already processed files
    processed_files = load_processed_files()

    # Load documents from the specified directory
    loader = PyPDFDirectoryLoader(DATA_DIR)
    all_documents = loader.load()
    
    # Filter out already processed documents
    new_documents = [doc for doc in all_documents if doc.metadata["source"] not in processed_files]
    
    if not new_documents:
        print("No new documents to process.")
        return

    print(f"Processing {len(new_documents)} new pdf files.")

    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
    texts = text_splitter.split_documents(new_documents)

    # Create or update the vector store with new document chunks
    vectorStore = Chroma.from_documents(
        documents=texts,
        embedding=HuggingFaceInferenceAPIEmbeddings(api_key=inference_api_key, model_name="sentence-transformers/all-MiniLM-L6-v2"),
        persist_directory=VECTOR_STORE_DIR
    )

    # Persist the vector store to disk
    # vectorStore.persist() # deprecated
    
    print("Vector store updated.")

    # Update the processed files list with only unique entries
    processed_files.update(doc.metadata["source"] for doc in new_documents)
    save_processed_files(processed_files)

def main():
    """Main function to create or update the vector database."""
    create_vector_db()

if __name__ == "__main__":
    main()
