import logging
from langchain_anthropic import ChatAnthropic
from agent_tools import tools, SYSTEM_PROMPT, query, memory
from datetime import datetime
# 1. Logging setup (Audit Trail)

logging.basicConfig(
    filename = "logs/mini_shop.log",
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(messages)s"
)

# start of the audit session
logging.info("==== NEW AGENT SESSION START ====")
logging.info(f"Session Timestamp: {datetime.now().isoformat()}")
logging.info(f"User Budget: {memory['budget']}")
logging.info(f"User Query: {query}")
logging.info("---------------------------------------")


# 2. Configure model with tools
model = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    temperature=0.1,
    timeout=60,
    max_tokens=1000
)

model_with_tools = model.bind_tools(tools)

# 3. Define messages (system prompt + user goal)
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": query}
]

print("\n=== Starting Smart Shopper Agent ===\n")

# 4. Reasoning Loop (up to 10 steps)

for i in range(10):
    print(f"Iteration {i+1}")
    logging.info(f"--- Iteration {i+1} ---")
    
    response = model_with_tools.invoke(messages)
    logging.info(f"Model response: {response.content}")
    
    messages.append({
        "role": "assistant", 
        "content": response.content, 
        "tool_calls": response.tool_calls if hasattr(response, 'tool_calls') else []
    })
    
    # Check if there are tool calls
    if not response.tool_calls:
        print("\n=== Final Response ===")
        print(response.content)
        logging.info("No more tool calls - reasoning complete.")
        logging.info(f"Final Response: {response.content}")
        break
    
    # Execute tool calls
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]  # "recommend"
        tool_args = tool_call["args"] # {"user_query": "laptop under $500"}
        
        print(f"Calling tool: {tool_name} with args: {tool_args}")
        logging.info(f"Tool Call -> {tool_name} | Args: {tool_args}")
        
        # Find and execute the tool
        tool_func = next((t for t in tools if t.name == tool_name), None)
        # Searches [get_products, get_price, add_to_cart, recommend, checkout]
        # Finds the "recommend" function object
        if tool_func:
            try:
                result = tool_func.invoke(tool_args) # EXECUTES recommend(user_query="...")
                print(f"Tool result: {result}\n")
                logging.info(f"Tool Result -> {tool_name}: {result}")
                messages.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool_call["id"]
                })
            
            except Exception as e:
                logging.error(f"Error executing {tool_name}: {e}")
        else:
            print(f"Tool {tool_name} not found")
            logging.error(f"Tool {tool_name} not found")
            
# 5. End of session
logging.info("--------------------")
logging.info("==== AGENT SESSION END ====\n")

print("\n === Session Complete ===\n")