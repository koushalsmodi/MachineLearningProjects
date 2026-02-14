from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
import os

load_dotenv()
print("API key loaded:", os.getenv("ANTHROPIC_API_KEY")[:10])

def call_claude(prompt: str, system_prompt: str = None, model="claude-haiku-4-5-20251001"):
    """
    Call Claude API with a prompt and return the response.
    
    Args:
        prompt (str): The user's message to Claude
        system_prompt (str, optional): System context for Claude
        model (str): Claude model to use. Defaults to Haiku.
    
    Returns:
        str: Claude's response text, or error message if API call fails
    """
    
    messages = []
    if system_prompt:
        messages.append(SystemMessage(content = system_prompt))
    messages.append(HumanMessage(content = prompt))
    
    try:
        llm = ChatAnthropic(model=model)
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        return f"Error occurred: {e}"
        

if __name__ == "__main__":
    
    result = call_claude(
        prompt = "Hi,what's the cheapest flights from Dhaka to Mumbai for March 6th and March 16th round trip (economy class)?",
        system_prompt = "You are a flight search specialist capable of finding the best price and shortest route for destination and origin cities based on user's question."
    )
    
    print(f"Extraction Test: {result}")
    
 