from langgraph.graph import StateGraph,MessagesState,START,END
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

from langchain_groq import ChatGroq

llm=ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    max_tokens=None,
    max_retries=2
)

def multiply(a:int,b:int)->int:
    """
    multiple a and b

    args:
    a:fist int value
    b:second int value
    """
    return a*b

def add(a:int,b:int)->int:
    """
    add a and b

    args:
    a:fist int value
    b:second int value
    """
    return a+b

def divide(a:int,b:int)->float:
    """
    divide a and b

    args:
    a:fist int value
    b:second int value
    """
    return a/b

tools=[multiply,add,divide]

llm_tool=llm.bind_tools(tools)

sys_message=SystemMessage(content="You are a helpfull assistant to solve the arthimetic problems")

def assistant(state:MessagesState):
    return {"messages":[llm_tool.invoke([sys_message] +state["messages"])]}


graph=StateGraph(MessagesState)

graph.add_node("assistant",assistant)
graph.add_node("tools",ToolNode(tools))
graph.add_edge(START,"assistant")
graph.add_conditional_edges("assistant",tools_condition)
graph.add_edge("tools","assistant")

builder=graph.compile()