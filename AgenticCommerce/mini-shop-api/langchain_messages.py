import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables
load_dotenv()
print("API key loaded:", os.getenv("ANTHROPIC_API_KEY")[:10])

model = init_chat_model( 
        "claude-sonnet-4-5-20250929",
        temperature = 0.5,
        timeout = 60,
        max_tokens = 1000
    )

# messages  = [
#     SystemMessage("You are a poetry expert."),
#     HumanMessage("Write a haiku about spring"),
#     AIMessage("Cherry blossoms bloom...")
# ]

# System message
# system_msg = SystemMessage("""
# You are a senior Python developer with expertise in web frameworks.
# Always provide code examples and explain your reasoning.
# Be concise but thorough in your explanations.                 
#  """)

# messages = [
#     system_msg,
#     HumanMessage("How do I create a REST API?")
# ]
# response = model.invoke(messages)
# print(response.text)

# Human message
# human_msg  = HumanMessage(
#     content = "Hello! What is machine learning?",
#     name = "alice",
#     id = "msg_123"
# )
# response = model.invoke([human_msg])
# print(response.text)

# AI message
# Create an AI message manually(eg: for conversation history)
# ai_msg = AIMessage("I'd be happy to help you with that question!")

# Add to conversation history
# messages = [
#     SystemMessage("You are a helpful assistant."),
#     HumanMessage("Can you help me?"),
#     ai_msg,
#     HumanMessage("Great! What's 2+2? ")
# ]

# response = model.invoke(messages)
# print(response.text)

# def get_weather(location: str) -> str:
#     """Get the weather at a location."""
#     return f"It's sunny in {city}"

# model_with_tools = model.bind_tools([get_weather])
# response = model_with_tools.invoke("What's the weather in Paris?")

# for tool_call in response.tool_calls:
#     print(f"Tool: {tool_call['name']}")
#     print(f"Args: {tool_call['args']}")
#     print(f"ID: {tool_call['id']}")
    
# print(response.usage_metadata)

chunks = []
full_message = None
for chunk in model.stream("Hi, what's machine learning?"):
    chunks.append(chunk)
    print(chunk.text)
    full_message = chunk if full_message is None else full_message + chunk