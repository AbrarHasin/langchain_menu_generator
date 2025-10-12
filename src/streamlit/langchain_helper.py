import os
from pathlib import Path
from dotenv import load_dotenv

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

llm = ChatAnthropic(
    model="claude-3-7-sonnet-20250219",
    temperature=0.6,
    timeout=None,
    max_retries=5,
    anthropic_api_key=anthropic_api_key
)

def generate_resturant_name_n_items(country):

    from langchain_core.prompts import ChatPromptTemplate

    # Create a chat template for restaurant naming
    name_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert at creating unique, sophisticated restaurant names. Your names should be memorable, culturally appropriate, and elegant."),
        ("human", "Name of the country is {country}. Provide ONLY a single name for the restaurant, with no explanation or additional text.")
    ])

    from langchain.chains import LLMChain

    name_chain = LLMChain(llm=llm, prompt=name_template, output_key="resturant_name")
    # name_chain.run({"country": "Italy"})

    # Create a chat template for restaurant naming
    menu_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert at creating unique, sophisticated food item menu list. Your names should be memorable, culturally appropriate, and elegant with the given resturant name."),
        ("human", "Name of the resturant is {resturant_name}. Provide me the ONLY a comma separated fancy food item names for the restaurant menu, with no explanation or additional text."),
    ])

    from langchain.chains import LLMChain

    menu_chain = LLMChain(llm=llm, prompt=menu_template, output_key="menu_items")
    # menu_chain.run({"resturant_name": "Italy"})

    from langchain.chains import SequentialChain

    chain = SequentialChain(chains=[name_chain, menu_chain], input_variables=["country"], output_variables=["resturant_name", "menu_items"], verbose=True)

    return chain.invoke({"country": f"{country}"})
