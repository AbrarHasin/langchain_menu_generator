import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

# Get API key from environment
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Do NOT print the raw key in notebooks or logs. Instead print a confirmation that it's set.
print("ANTHROPIC_API_KEY set?", bool(anthropic_api_key))

if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables. Please set it in the .env file.")

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize LLM
llm = ChatAnthropic(
    model="claude-3-7-sonnet-20250219",
    temperature=0.1,
    timeout=None,
    max_retries=5,
    anthropic_api_key=anthropic_api_key
)

# Define the state structure for our graph (LangGraph 2025 approach)
class State(TypedDict):
    """State tracks messages in the conversation"""
    messages: Annotated[list, add_messages]

# Create MemorySaver for in-memory persistence
memory = MemorySaver()

# Define the chatbot node function
def chatbot(state: State):
    """Process messages and generate response using LLM"""
    return {"messages": [llm.invoke(state["messages"])]}

# Build the LangGraph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile with memory checkpointer
graph = graph_builder.compile(checkpointer=memory)


def generate_resturant_name_n_items(country):
    """
    Legacy function for backward compatibility.
    Generates restaurant name based on country.
    """
    from langchain_core.prompts import ChatPromptTemplate
    from langchain.chains import LLMChain
    from langchain.chains import SequentialChain

    name_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert at creating unique, sophisticated restaurant names and associated menu lists. Your names should be memorable, culturally appropriate, and elegant."),
        ("human", "{country}")
    ])

    name_chain = LLMChain(llm=llm, prompt=name_template, output_key="resturant_name")
    chain = SequentialChain(chains=[name_chain], input_variables=["country"], output_variables=["resturant_name"], verbose=True)

    return chain.invoke({"country": f"{country}"})


def chat_with_memory(user_message: str, thread_id: str, system_prompt: str = None):
    """
    Modern LangGraph approach with MemorySaver (2025 best practice).

    This function demonstrates the latest way to handle conversations with memory.

    Args:
        user_message: The user's input message
        thread_id: Unique identifier for this conversation thread (maintains separate conversations)
        system_prompt: Optional system prompt to guide the AI's behavior

    Returns:
        The AI's response as a string
    """
    # Prepare input messages
    input_messages = []

    # Add system prompt if provided (sets the AI's role/context)
    if system_prompt:
        input_messages.append(SystemMessage(content=system_prompt))

    # Add user's message
    input_messages.append(HumanMessage(content=user_message))

    # Configure with thread_id - this is KEY for memory persistence
    config = {"configurable": {"thread_id": thread_id}}

    # Invoke the graph - it automatically manages message history
    result = graph.invoke({"messages": input_messages}, config)

    # Extract and return the AI's response
    return result["messages"][-1].content


def get_conversation_history(thread_id: str):
    """
    Retrieve full conversation history for a given thread.

    Args:
        thread_id: The conversation thread identifier

    Returns:
        List of all messages in this conversation
    """
    config = {"configurable": {"thread_id": thread_id}}
    state = graph.get_state(config)

    if state and state.values.get("messages"):
        return state.values["messages"]
    return []
