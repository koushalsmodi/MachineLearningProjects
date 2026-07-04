import requests
from PIL import Image 
from io import BytesIO
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title('Travel-GPT✈️')
st.markdown('Corporate Travel Assistant - plans, verifies, and optimizes trips against Company Policy')
user_input = st.text_input('Where would you like to travel?')
submitted = st.button('Plan my trip.')

if submitted:
    col1, col2 = st.columns([4,6])
    with col1: 
        st.subheader('Agent Status')
        status_parse_intent = st.empty()
        status_flight_search = st.empty()
        status_check_policy = st.empty()
        status_build_response = st.empty()
    
        status_parse_intent.info('⏳ Waiting to parse trip request...')
        status_flight_search.info('⏳ Waiting to search flights...')
        status_check_policy.info('⏳ Waiting to check policies...')
        status_build_response.info('⏳ Waiting to build respond...')
    
    with col2: 
        st.subheader('Your Trip')
        image_placeholder = st.empty()
        image_placeholder.info('🌍 Destination image will appear here...')
        results_placeholder = st.empty()
        results_placeholder.info('✈️ Flight options will appear here...')

# getting a photo url
ACCESS_KEY = load_dotenv('ACCESS_KEY')

airport_to_city = {
    "JFK": "Manhattan New York skyline",
    "PHX": "Phoenix Arizona cityscape",
    "SFO": "San Francisco Golden Gate Bridge",
    "LAX": "Los Angeles California skyline",
    "ORD": "Chicago Illinois skyline",
    "MIA": "Miami Florida beach",
    "DFW": "Dallas Texas skyline",
    "BOS": "Boston Massachusetts cityscape",
    "SEA": "Seattle Washington Space Needle",
    "DEN": "Denver Colorado mountains"
}

def get_destination_image(destination_code):
    query = airport_to_city.get(destination_code, destination_code)
    url = f'https://api.unsplash.com/photos/random?query={query}&client_id={ACCESS_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        photo = response.json()
        image_url = photo['urls']['regular']
        image_response = requests.get(image_url)
        return Image.open(BytesIO(image_response.content))
    return None
