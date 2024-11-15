from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableConfig
from handlers.memory_handler import get_memory
from handlers.callback_handler import CustomCallbackHandler
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from tools.weather_tool import get_weather_info
from tools.search_tool import get_search_results
from utils.helper_functions import parse_location
from utils.file_processing import get_docsearch
from langchain_core.messages import HumanMessage, AIMessage
from langchain_chroma import Chroma
from datetime import datetime
from langsmith import Client
import chainlit as cl
import logging
import os
from operator import itemgetter
import asyncio

# Initialize project-specific configurations
PROJECT_NAME = os.getenv("LANGCHAIN_PROJECT", "chatbot")
client = Client()  # LangSmith Client

inference_api_key = os.getenv("HUGGINGFACE_API_KEY")

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Set up logging
logger = logging.getLogger(__name__)

def setup_runnable():
    memory = get_memory()
    llm = OllamaLLM(model="HienBM/gemma2-9b-it-tripadvisor-v4")

    # Load vectorstore for PDF-based retrieval
    vectorstore = Chroma(
        persist_directory="vectorstores/db/",
        embedding_function=HuggingFaceInferenceAPIEmbeddings(api_key=inference_api_key, model_name="sentence-transformers/all-MiniLM-L6-v2")
    )

    # Set up the prompt template with contextual knowledge and QA
    prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a highly detailed travel assistant chatbot with access to optional resources, including real-time data from APIs and PDF-based documents. Respond to the user’s questions with the following priorities:\n"
               "\n1. **Personalized Travel Recommendations**: By default, provide detailed and personalized travel advice based on the user's preferences, such as destination, budget, accommodation type, and activities of interest. Suggest places to visit, practical advice on bookings, itinerary planning, and sightseeing tailored to their interests. Use this knowledge as the primary basis for responses.\n"
               "\n2. **API Data (Optional)**: If the user asks for weather or general information about a location, supplement your answer with real-time details from OpenWeatherMap or Google Serper API as relevant.\n"
               "\n3. **PDF Content Summaries (Optional)**: If the user requests a summary or extraction from PDF files, provide a comprehensive and detailed extraction. Ensure that no important information is omitted, and extract all relevant details, such as suggested locations, key points. If the document contains lists, schedules, or recommendations, include all items to provide a complete overview without omit anything.\n"
               "\nWhen responding, prioritize delivering travel recommendations based on your knowledge, using additional resources from APIs or PDFs only when specifically requested by the user. For PDF extractions, ensure exhaustive coverage of content to provide full context and all details."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
    ])

    # Create a retriever from the vectorstore
    pdf_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Add retriever to session for use in conversations
    cl.user_session.set("pdf_retriever", pdf_retriever)

    # Create the runnable chain by combining prompt, model, and parsing, retaining history
    runnable = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | prompt_template
        | llm
        | StrOutputParser()
    )

    cl.user_session.set("runnable", runnable)

async def process_user_message(message):
    memory = cl.user_session.get("memory")  # ConversationBufferMemory
    runnable = cl.user_session.get("runnable")  # Runnable
    pdf_retriever = cl.user_session.get("pdf_retriever")  # PDF retriever context

    # Check if the message includes a file
    doc_retriever = None
    if message.elements:
        file = message.elements[0]  # Assuming one file per message
        # Process and create document retriever
        docsearch = await cl.make_async(get_docsearch)(file)
        doc_retriever = docsearch.as_retriever(search_kwargs={"k": 3})
        await cl.Message(content=f"Processed `{file.name}` and updated retriever.", author="admin").send()

    # Construct input based on user query and attached file context
    pdf_context = ""

    if "pdf" in message.content.lower():
        pdf_results = pdf_retriever.invoke(message.content)
        pdf_context = "\n".join([f"Document snippet: {doc.page_content}" for doc in pdf_results])

    if doc_retriever:
        pdf_results = doc_retriever.invoke(message.content, k=5)
        pdf_context = "\n".join([f"Document snippet: {doc.page_content}" for doc in pdf_results])

    # Existing logic for API calls for weather and search
    additional_info = ""
    if "weather" in message.content.lower():
        location = parse_location(message.content)
        if location:
            try:
                weather_info = await get_weather_info(location)
                additional_info += f"\nThe weather in {location} is: {weather_info}"
            except Exception as e:
                additional_info += f"\nCould not retrieve weather info due to error: {e}"
    
    if "search for" in message.content.lower():
        query = message.content.split("search for")[-1].strip()
        if query:
            try:
                search_results = await get_search_results(query)
                additional_info += f"\nTop search results for {query}: {search_results}"
            except Exception as e:
                additional_info += f"\nCould not retrieve search results due to error: {e}"

    # Combine user input with PDF context and additional information
    full_input = f"{message.content}\n\nPDF Context: {pdf_context}\n\nAdditional Info: {additional_info}" if pdf_context or additional_info else message.content

    # Streaming response handling with callback
    res = cl.Message(content="", author="admin")
    async for chunk in runnable.astream(
        {"input": full_input},
        config=RunnableConfig(callbacks=[CustomCallbackHandler()])
    ):
        await res.stream_token(chunk)
    await res.send()

    # Add messages to memory
    memory.chat_memory.add_user_message(HumanMessage(content=message.content))
    memory.chat_memory.add_ai_message(AIMessage(content=res.content))

    # Log the run to Langsmith
    try:
        run = client.create_run(
            name="chat_run",
            inputs={"input": full_input},
            outputs={"output": res.content},
            run_type="llm",
            project_name=PROJECT_NAME,
            end_time=datetime.now(),
        )
        
        if run:
            run_id = run.id
            logger.debug(f"Run created successfully with ID: {run_id}")
    
    except Exception as e:
        logger.error(f"Error creating run: {e}")
