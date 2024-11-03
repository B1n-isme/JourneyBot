# JourneyBot - Personalized Travel Assistant Chatbot

JourneyBot is a personalized travel assistant chatbot built using Chainlit, LangChain, and Ollama. It leverages real-time API data, embedded PDF content, and model knowledge to provide users with customized travel recommendations, itineraries, and detailed responses based on user preferences. It features light and dark themes, smooth animations, and UI enhancements for an engaging user experience.

## Table of Contents
- [Project Structure](#project-structure)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
- [Running Chatbot](#running-chatbot)
- [Theme Switching](#theme-switching)
- [Usage](#usage)
- [Project Highlights](#project-highlights)
  - [PDF Vectorization and Direct File Interaction](#pdf-vectorization-and-direct-file-interaction)
  - [API Integrations](#api-integrations)
  - [UI Customization](#ui-customization)
- [Troubleshooting](#troubleshooting)


## Project Structure
```bash
JourneyBot/
├── data/
│   └── *.pdf                            # Directory for storing PDF files for embedding
├── vectorstores/
│   └── db/                              # Persistent directory for Chroma vector database
├── handlers/
│   ├── callback_handler.py              # Custom callback handler for LangChain
│   └── memory_handler.py                # Manages conversation memory handling
├── tools/
│   ├── geocode_tool.py                  # Fetches country code using OpenCage API
│   ├── search_tool.py                   # Performs Google search using Serper API
│   └── weather_tool.py                  # Retrieves weather information using OpenWeatherMap API
├── utils/
│   ├── helper_functions.py              # Helper functions for location parsing, etc.
│   ├── logger.py                        # Configures logging
│   ├── file_processing.py               # Processing attached file for embedding and interaction
│   └── message_templates.py             # Retrieves and formats the startup message
├── processed_files.json                 # JSON file tracking processed PDF files
├── public/
│   ├── custom.js                        # JavaScript for animations, theme toggle, and interactions
│   ├── stylesheet.css                   # Custom CSS file for UI styling (light and dark themes)
│   └── avatars/
│       └── admin.png
├── auth.py                              # Handles password-based authentication
├── config.py                            # Sets up environment, logging, and cache
├── llm_setup.py                         # Initializes LLM, manages API calls, and processes messages
├── main.py                              # Main entry point, sets up chatbot lifecycle
├── vectorize_pdf.py                     # Script to vectorize new PDF files in data/ and store in vectorstores/db/
│-- .env                                 # Environment variable 
└── README.md                            # Project documentation
```

## Features
1. **Real-Time API Data**: Integrates OpenWeatherMap for weather updates and Google Serper for general searches.
2. **Direct File Interaction**: Allows users to attach files (e.g., PDFs) directly in the UI for vectorization, retrieval, and question answering using Pinecone as the vector store.
3. **PDF Embedding for Retrieval**: Summarizes or answers questions based on PDF files stored in [data/](./data/).
4. **Personalized Travel Recommendations**: Uses model knowledge to provide tailored travel advice, destinations, and itineraries based on user preferences.
5. **UI Enhancements**: Light and dark themes, smooth animations, and visually appealing styles with [stylesheets.css](./public/stylesheets.css) and [custom.js](./public/custom.js).

## Setup Instructions
### Prerequisites
- Python 3.10
- Chainlit: Installed using `pip install chainlit`
- dotenv for environment variable management
- LangChain and LangChain Community Tools
- Pinecone for vector storage and retrieval
- Ollama for model interaction (with local Ollama model support)
- Sentence Transformers for embeddings

### Environment Setup
1. Clone the Repository:

```bash
git clone <repository_url>
cd JourneyBot
```

2. Install Python Dependencies:
```bash
pip install -r requirements.txt
```

3. Setup Environment Variables:
Rename `example.env` to `.env` and add your respective API keys:

```plaintext
OPENCAGE_API_KEY=<Your_OpenCage_API_Key>
OPENWEATHERMAP_API_KEY=<Your_OpenWeatherMap_API_Key>
SERPER_API_KEY=<Your_Serper_API_Key>
LITERAL_API_KEY=<Your_Literal_API_Key>

CHAINLIT_AUTH_SECRET=<Your_Chainlit_Auth_Secret>
LANGCHAIN_TRACING_V2=false
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=<Your_Langchain_API_Key>
LANGCHAIN_PROJECT="chatbot"
LANGCHAIN_HUB_API_URL = "https://api.hub.langchain.com"
PINECONE_API_KEY=<Your_Pinecone_API_Key>
HUGGINGFACE_API_KEY = <Your_Huggingface_API_key>
```

1. Initialize Vector Database:

If you have PDF files in the [data/](./data/) directory, run the [vectorize_pdf.py](./vectorize_pdf.py) script to embed new PDF files into the Chroma vector database:

```bash
python vectorize_pdf.py
```
Only new PDF files will be processed, as already processed files are tracked in [processed_files.json](./processed_files.json).

5. Configure Authentication:

Modify [auth.py](./auth.py) if you want to add multiple roles or customize authentication beyond the default admin credentials.

## Running chatbot
1. Start Chainlit Server:
```bash
chainlit run main.py
```

2. Access the Chatbot:

- Open your browser and go to http://localhost:8000 to access JourneyBot.
- Use the default admin credentials or customize them in [auth.py](./auth.py).

## Theme Switching
The chatbot supports both light and dark themes:

- Click the Toggle Theme button to switch themes.
- Your theme preference is saved in local storage, so it will persist across sessions.
## Usage
- Travel Recommendations: Ask the chatbot for travel advice, destinations, or itineraries.
- API-Based Information: Request current weather or general information by mentioning "weather" or "search" in your question.
- PDF Summaries: Attach a PDF in the UI and ask for summaries or specific information directly from it.
## Project Highlights
### PDF Vectorization and Direct File Interaction
The chatbot allows users to attach PDF files directly in the UI. These files are processed, vectorized using `sentence-transformers` (all-MiniLM-L6-v2 model), and stored in Pinecone for retrieval. This enables the chatbot to answer questions and provide summaries based on the contents of the attached PDF files.

### API Integrations
**OpenWeatherMap**: For providing weather updates based on location.
**Google Serper**: For searching general information.
### UI Customization
The [stylesheets.css](./public/stylesheet.css) and [custom.js](./public/custom.js) files improve the user interface:

- **Smooth Animations**: Fade-in effects for messages and dynamic transitions.
- **Theme Toggle**: Supports light and dark themes with style adjustments.
- **Enhanced Message Styles**: Distinct styling for user and assistant messages.
## Troubleshooting
- **CSS or JavaScript Changes Not Reflecting**: Clear your browser cache or disable caching in developer tools to ensure you’re loading the latest styles.
- **PDF Not Embedding Properly**: Verify that the PDF file is new (not listed in [processed_files.json](./processed_files.json)). Re-run [vectorize_pdf.py](./vectorize_pdf.py) if needed.
- **API Errors**: Ensure that API keys in .`env` are correct and active.


This [README.md](./README.md) provides a comprehensive guide to the JourneyBot project, including setup, usage, and customization instructions. Let me know if there are additional details you'd like to include!