import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from langchain.tools import tool

# Basic tool definition
@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.
    
    Args:
        query: Search terms to look for 
        limit: Maximum number of results to return
    
    """
    return f"Found {limit} results for '{query}'"

# Customize tool properties
# Custom tool name

@tool("web_search") # Custom name
def search(query: str) -> str:
    """Search the web for information"""
    return f"Results for: {query}"

print(search.name) # web_search

# Custom tool description

@tool("calculator", description = "Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))