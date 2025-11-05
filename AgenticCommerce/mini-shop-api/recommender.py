import google.genai as genai

from dotenv import load_dotenv
import os 

load_dotenv()
 
catalog = [
    {"name": "MacBook", "price": 999},
    {"name": "Dell", "price": 650},
    {"name": "HP", "price": 720},
]
user_query = "Recommend a laptop under $700"

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

prompt = f"""You are a product recommender and your role is to 
take user's query: {user_query} and advise the user with a small list or with just 1 item 
based on the user's budget and preferences
from the catalog: {catalog} based on the user query.
The user will be the buyer so it is of utmost importance to provide a correct response
so as to have our sale successful.


Output should be short and human-readable.
"""


response = client.models.generate_content(
    model="gemini-2.5-pro", 
    contents=prompt
)

print(response.text)
