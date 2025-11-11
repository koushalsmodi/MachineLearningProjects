# bind tools

# goal: buy a cheap laptop and let is decide which tools to call in what order
# budget: 50
# store it in a dictionary or langchain conversation buffer memory

import os
from dotenv import load_dotenv
load_dotenv()
print("API key loaded:", os.getenv("ANTHROPIC_API_KEY")[:10])

from langchain.messages import SystemMessage
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from dataclasses import dataclass

from main import read_products, create_cart_item, create_recommendation_request
# 1. System prompt

SYSTEM_PROMPT = SystemMessage("""
You are a product recommenderand you take input as user's query
and advice the user with just 1 item \n
based on the user's budget and preferences
from the catalog.
Output should be short and human-readable.
You have access to 4 tools:
- get_products: use this to look at all products
- get_price: use this to look at all products pricing
- add_to_cart: use this to add only the 1 best product that fits the user's budget
- recommend: user this 
""")

# 2. Creating tools

# get_products() -> calls products
@tool
def get_products():
    return read_products()

# get_price(product_id) -> looks up price
@tool
def get_price(product_id):
    all_products = get_products()
    for product in all_products:
        if product_id == product["id"]:
            price = product["price"]
    
    return price
        
# add_to_cart() -> calls cart/add
@tool 
def add_to_cart(product_id, quantity):
    create_cart_item(product_id, quantity)


query = "Recommend a product to buy under $100"
# recommend() -> calls / recommend
@tool
def recommend(query):
    return create_recommendation_request(query)

memory = {"budget": 100}

# 3. Configure a model with parameters
model = init_chat_model(
    "claude-sonnet-4-5-20250929",
    temperature = 0.1,
    timeout = 60,
    max_tokens = 1000
)

model_with_tools = model.bind([get_products, get_price, add_to_cart, recommend])

# 4. Define a response format
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    query: str
    best_product: str | None = None 

# 5. Add memory
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()

# 6. Create and run the agent
agent = create_agent(
    model = model_with_tools,
    system_prompt = SYSTEM_PROMPT,
    response_format = ResponseFormat,
    checkpointer = checkpointer
)

respponse = agent.invoke({
    "messages": [{"role": "user", "content": query}]
})