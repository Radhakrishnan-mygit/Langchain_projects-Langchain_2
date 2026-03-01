from langgraph.graph import START,END,StateGraph
from langgraph.prebuilt import ToolNode,tools_condition
from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict,Annotated

from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"]=os.getenv("TAVILY_API_KEY")


arxiv_api_wrapper=ArxivAPIWrapper(top_k_results=5,load_max_docs=100)
arxiv_query=ArxivQueryRun(api_wrapper=arxiv_api_wrapper)

wiki_api_wrapper=WikipediaAPIWrapper(top_k_results=5,doc_content_chars_max=200)
wiki_query=WikipediaQueryRun(api_wrapper=wiki_api_wrapper)


gemini_model = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

tavily=TavilySearchResults()

Tools=[arxiv_query,wiki_query,tavily]

llm_with_tools=gemini_model.bind_tools(tools=Tools)

class State(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]

def Tool_calling_llm(state:State)->State:
    return {"messages":llm_with_tools.invoke(state["messages"])}


builder=StateGraph(State)
builder.add_node("Tool calling llm",Tool_calling_llm)
builder.add_node("tools",ToolNode(Tools))
builder.add_edge(START,"Tool calling llm")
builder.add_conditional_edges("Tool calling llm",tools_condition)
builder.add_edge("tools","Tool calling llm")
builder.add_edge("Tool calling llm",END)


memory=MemorySaver()
config={"configurable":{"thread_id":"1"}}

builder.compile(checkpointer=memory)