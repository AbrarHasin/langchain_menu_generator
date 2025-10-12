from ..langchain_menu_generator.secret_key import anthropic_api_key
import os

# Prefer an existing environment variable (for CI/production). Only set it from the local secret when missing.
if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key

# Do NOT print the raw key in notebooks or logs. Instead print a confirmation that it's set.
print("ANTHROPIC_API_KEY set?", bool(os.getenv("ANTHROPIC_API_KEY")))

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
