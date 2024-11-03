import chainlit as cl
from config import setup_environment
from handlers.memory_handler import initialize_memory, resume_memory
from llm_setup import setup_runnable, process_user_message
from utils.message_templates import get_startup_message
from auth import auth_callback

# Set up environment
setup_environment()

@cl.on_chat_start
async def start():
    user = cl.user_session.get("user")
    # await cl.Message(content=f"Hello {user.identifier}!" if user else "Hello! Please log in.", author="admin").send()
    initialize_memory()
    setup_runnable()
    await cl.Message(content=get_startup_message(), author="admin").send()

@cl.on_chat_resume
async def resume(thread: dict):
    resume_memory(thread)
    setup_runnable()
    await cl.Message(content="Welcome back! Let's continue from where we left off.", author="admin").send()

@cl.on_message
async def main(message: cl.Message):

    await process_user_message(message)
