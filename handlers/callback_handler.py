from langchain.callbacks.base import BaseCallbackHandler

class CustomCallbackHandler(BaseCallbackHandler):
    def on_chain_start(self, serialized, inputs, **kwargs):
        pass
    def on_tool_start(self, serialized, inputs, **kwargs):
        pass
    def on_llm_start(self, serialized, prompts, **kwargs):
        pass
    def on_llm_end(self, response, **kwargs):
        pass
