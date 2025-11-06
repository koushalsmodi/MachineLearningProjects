import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# imports
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

companies_with_locations = {
    "Wells Fargo & Co.": "Austin, TX",
    "IVY Enterprises": "Port Washington, New York, US",
    "Smile Design Management L": "Tampa, FL, US",
    "GGG Demolition Inc": "US"
}

model = genai.GenerativeModel("gemini-2.5-pro")

for company, location in companies_with_locations.items():
    user_query = f"What is the SIC 4 Code for {company} located in {location}?"

    prompt = f"""
    You are responsible for providing accurate 4-digit SIC industry codes and their descriptions.

    Input: {user_query}

    Output format:
    SIC Code: [4-digit code]
    Description: [concise description of the company's industry based on SIC code]
    """

    try:
        response = model.generate_content(prompt)
        print(f"\n--- {company} ({location}) ---")
        print(response.text.strip() if response.text else "No response returned.")
    except Exception as e:
        print(f"Error processing {company}: {e}")
        
"""
--- Wells Fargo & Co. (Austin, TX) ---
SIC Code: 6021
Description: National Commercial Banks

--- IVY Enterprises (Port Washington, New York, US) ---
Based on public business records, here is the SIC code for IVY Enterprises in Port Washington, NY, which is known for manufacturing industrial markers and writing instruments.

**SIC Code:** 3951
**Description:** Pens, Mechanical Pencils, and Parts

--- Smile Design Management L (Tampa, FL, US) ---
SIC Code: 8021
Description: Offices and clinics of licensed dentists engaged in the practice of general or specialized dentistry.

--- GGG Demolition Inc (US) ---
SIC Code: 1795
Description: Wrecking and Demolition Work
    """