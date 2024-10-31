from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from pydantic import BaseModel
from typing import Annotated, Literal
import functools
import operator
from typing import Sequence
from typing_extensions import TypedDict

llm = ChatOpenAI(model="gpt-4o-mini")
tavily_tool = TavilySearchResults(max_results=5)
python_repl_tool = PythonREPLTool()

def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["messages"][-1].content, name=name)]
    }
    
def supervisor_agent(state):
    """This is the supervisor node
    
    It just picks the next agent to process and decides when the work is completed"""
    supervisor_chain = prompt | llm.with_structured_output(routeResponse)
    return supervisor_chain.invoke(state)

members = ["Researcher", "Mathematician"]
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers:  {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)
options = ["FINISH"] + members

class routeResponse(BaseModel):
    next: Literal[*options]
    
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Given the conversation above, who should act next?"
            " Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=str(options), members=", ".join(members))

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

research_agent = create_react_agent(llm, tools=[tavily_tool])
research_node = functools.partial(
    agent_node,
    agent=research_agent,
    name="Researcher" #must match the name in the 'members' list above
)
code_agent = create_react_agent(llm, tools=[multiply])
code_node = functools.partial(agent_node, agent=code_agent, name="Coder")

workflow = StateGraph(AgentState)

## Add nodes
workflow.add_node("Researcher", research_node)
workflow.add_node("Coder", code_node)
workflow.add_node("supervisor", supervisor_agent)

## Add edges
### We want our workers to always report back to our supervisor when done
for member in members:
    workflow.add_edge(member, "supervisor")

### The supervisor then fills in the 'next' field in the graph state for routing
conditional_map = {k:k for k in members}
conditional_map['FINISH'] = END
workflow.add_conditional_edges(
    "supervisor", lambda x: x['next'],
    conditional_map
)

### Connect entrypoint to supervisor
workflow.add_edge(START, "supervisor")

## Add memory - this creates chat history of the graph in an in-memory SQLite database
memory = MemorySaver()

## Compile
### We interrupt before the code execution just to ensure that we're not doing anything cray
graph = workflow.compile(
    interrupt_before=["Coder"], 
    checkpointer=memory
)