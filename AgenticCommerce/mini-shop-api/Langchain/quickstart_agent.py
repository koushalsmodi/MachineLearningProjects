import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import os
from dotenv import load_dotenv
from langchain.agents import create_agent


# Load environment variables
load_dotenv()
print("API key loaded:", os.getenv("ANTHROPIC_API_KEY")[:10])

# 1. System prompt
SYSTEM_PROMPT = """ You are an expert weather forecaster, who speaks in puns
You have access to two tools:
- get_weather_for_location: use this to get the weather for a specific location
- get user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location.
If you can tell from the question that they mean wherever they are,
use the get_user_location tool to find their location """

# 2. Create tools
# Let's a model interact with external systems by calling functions you define.
# Tools can depend on runtime context and also interact with agent memory.
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime

@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}"

@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str 
    
@tool 
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id 
    return "Florida" if user_id == "1" else "SF"

# 3. Configure your model
from langchain.chat_models import init_chat_model 

model = init_chat_model( 
        "claude-sonnet-4-5-20250929",
        temperature = 0.5,
        timeout = 10,
        max_tokens = 1000
    )

# 4. Define response format
# define a structured response format for agent responses to match specific schema

from dataclasses import dataclass

@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str 
    # Any interesting information about the weather if available
    weather_condition: str | None = None 
    

# 5. Add memory
# to main state across interactions. This allows the agent to remember previous conversations and context.

from langgraph.checkpoint.memory import InMemorySaver 

checkpointer = InMemorySaver()

# 6. Create and run the agent

agent = create_agent(
    model = model,
    system_prompt = SYSTEM_PROMPT,
    tools = [get_user_location, get_weather_for_location],
    context_schema = Context, 
    response_format = ResponseFormat,
    checkpointer = checkpointer
)

# thread_id is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
    config = config,
    context = Context(user_id = "1")
)


print(response['structured_response'])

# "Well, well, well! Looks like you're in Florida where it's always sunny! 
# I'd say the forecast is absolutely ray-diant! The sunshine state is really living up to its name - it's so bright, you might want to 
# put on your sun-glasses and have a sun-derful day! No clouds on the horizon, just pure solar power.
# I guess you could say the weather is absolutely sun-sational!", weather_condition="It's always sunny in Florida"

response = agent.invoke(
    {"messages": [{"role": "user", "content": "thank you!"}]},
    config = config,
    context = Context(user_id = "1")
)

print(response['structured_response'])
# ResponseFormat(punny_response="You're very welcome! 
# I'm just here to brighten your day with some weather updates! Hope you have a sun-credible time out there! 
# Stay cool, my friend! ☀️", weather_condition=None)