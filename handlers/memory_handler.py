import chainlit as cl
from langchain.memory import ConversationBufferMemory

def initialize_memory():
    cl.user_session.set("memory", ConversationBufferMemory(return_messages=True))

def resume_memory(thread):
    memory = ConversationBufferMemory(return_messages=True)
    for message in thread.get("steps", []):
        content = message["output"]
        if message["type"] == "user_message":
            memory.chat_memory.add_user_message(content)
        else:
            memory.chat_memory.add_ai_message(content)
    cl.user_session.set("memory", memory)

def get_memory():
    return cl.user_session.get("memory")
