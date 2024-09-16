from dotenv import load_dotenv, find_dotenv
from llama_index.core import Settings
from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

_ = load_dotenv(find_dotenv())
Settings.llm = OpenAI(model="gpt-4o-mini")

class RAGEvent(Event):
    query: str

class ResponseEvent(Event):
    answer: str
    metadata: str

class App(Workflow):
    @step
    async def judge_query(self, ev: StartEvent):
        pass