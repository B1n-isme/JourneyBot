import os
from dotenv import load_dotenv
from langchain_community.cache import InMemoryCache
from langchain_core.globals import set_llm_cache
from utils.logger import setup_logger

def setup_environment():
    load_dotenv()
    set_llm_cache(InMemoryCache())
    setup_logger()
