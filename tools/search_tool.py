from langchain_community.utilities import GoogleSerperAPIWrapper
import asyncio

search = GoogleSerperAPIWrapper()

async def get_search_results(query):
    return await asyncio.to_thread(search.run, query)
