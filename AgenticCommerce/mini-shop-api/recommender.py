import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from dotenv import load_dotenv
import os 



load_dotenv()
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
catalog = [
    {"name": "MacBook", "price": 999},
    {"name": "Dell", "price": 650},
    {"name": "HP", "price": 720},
]
user_query = "Recommend a laptop under $700"


prompt = f"""You are a product recommender and your role is to 
take user's query: {user_query} and advise the user with a small list or with just 1 item 
based on the user's budget and preferences
from the catalog: {catalog} based on the user query.
The user will be the buyer so it is of utmost importance to provide a correct response
so as to have our sale successful.
Output should be short and human-readable.
"""

model = genai.GenerativeModel("gemini-2.5-pro")

response = model.generate_content(prompt)
print(response.text)
