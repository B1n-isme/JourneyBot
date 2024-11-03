import importlib
import pkg_resources

# List of packages you're interested in
packages = [
    "chainlit", "langchain", "langchain-core", "langchain-community",
    "langchain-ollama", "langsmith", "opencage", "python-dotenv",
    "openai", "google-serper", "chroma", "pinecone", "PyPDF2"
]

for package in packages:
    try:
        version = pkg_resources.get_distribution(package).version
        print(f"{package}=={version}")
    except pkg_resources.DistributionNotFound:
        print(f"{package} is not installed.")
