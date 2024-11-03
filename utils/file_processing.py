# e5-small embedding
import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chainlit as cl
from pinecone import Pinecone

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

inference_api_key = os.getenv("HUGGINGFACE_API_KEY")

index_name = "journeybot"
dimensions = 384  # Ensure this matches the embedding dimensions of the E5 model

# Initialize the E5 model
embedding_model = HuggingFaceInferenceAPIEmbeddings(api_key=inference_api_key, model_name="sentence-transformers/all-MiniLM-L6-v2")

# Set of namespaces to keep track of unique file processing
namespaces = set()

# Define text splitter (adjust chunk size as needed)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

def process_file(file: cl.File):
    """Process the file and split it into documents."""
    if file.mime == "text/plain":
        Loader = TextLoader
    elif file.mime == "application/pdf":
        Loader = PyPDFLoader
    else:
        raise ValueError(f"Unsupported file type: {file.mime}")

    loader = Loader(file.path)
    documents = loader.load()
    docs = text_splitter.split_documents(documents)
    for i, doc in enumerate(docs):
        doc.metadata["source"] = f"source_{i}"
    return docs

def get_docsearch(file: cl.File):
    """Create or retrieve a document search index using Pinecone."""
    docs = process_file(file)

    # Save processed documents in the user session
    cl.user_session.set("docs", docs)

    # Create a unique namespace for the file
    namespace = file.name

    # Create the document search index using the embedding model
    docsearch = PineconeVectorStore.from_documents(
        docs, embedding=embedding_model, index_name=index_name, namespace=namespace
    )

    return docsearch
