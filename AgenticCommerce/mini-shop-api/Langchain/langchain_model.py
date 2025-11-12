# import warnings
# warnings.filterwarnings("ignore", category=FutureWarning)


import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
load_dotenv()
print("API key loaded:", os.getenv("ANTHROPIC_API_KEY")[:10])


# conversation = [ 
                
#     {"role": "system", "content": "You are a helpful assistant that translates English to French"},
#     {"role": "user", "content": "Translate: I love programming."},
#     {"role": "assistant", "content": "J'adore la programmation."},
#     {"role": "user", "content": "Translate: I love building applications."}            
#     ]

# conversation = [
#     SystemMessage("You are a helpful assistant that translates English to French"),
#     HumanMessage("Translate: I love programming."),
#     AIMessage("J'adore la programmation."),
#     HumanMessage("Translate: I love building applications.")
# ]


model = init_chat_model(
    "claude-sonnet-4-5-20250929",
    temperature = 0.7,
    timeout=  30,
    max_tokens = 1000,
    )

# response = model.invoke(conversation)
# print(response)

# Stream
# full = None
# for chunk in model.stream("Why do parrots have colorful feathers? "):
#     full = chunk if full is None else full+chunk
#     print(full.text)
    
# print(full.content_blocks)

# Batching
responses = model.batch_as_completed( [
    "Why do parrots have colorful feathers?",
    "How do airplanes fly? ",
    "What is quantum computing?"
])

for response in responses:
    print(response)