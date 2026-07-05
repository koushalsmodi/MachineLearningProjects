import requests
from PIL import Image 
from io import BytesIO
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
import asyncio

from agent.graph import run_agent
from datetime import date 

# getting a photo url
ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')

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
    if not destination_code or not ACCESS_KEY:
        return None
    
    query = airport_to_city.get(destination_code, destination_code)
    url = f'https://api.unsplash.com/photos/random?query={query}&client_id={ACCESS_KEY}'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            photo = response.json()
            image_url = photo['urls']['regular']
            image_response = requests.get(image_url)
            return Image.open(BytesIO(image_response.content))
    except Exception as e:
        st.warning(f'Couldn"t load destination image: {e}')
    return None


st.title('Travel-GPT✈️')
st.markdown('Corporate Travel Assistant - plans, verifies, and optimizes trips against Company Policy')
employee_input = st.text_input('Employee ID')
destination_input = st.text_input('Where would you like to travel?')
departure_date_input = st.date_input('Departure date', min_value=date.today())
submitted = st.button('Plan my trip.')

if submitted and (not employee_input or not destination_input):
    st.error("Please enter both an Employee ID and a destination.")
    
elif submitted:
    col1, col2 = st.columns([4,6])
    with col1: 
        st.subheader('Agent Status')
        status_parse_intent = st.empty()
        status_flight_search = st.empty()
        status_check_policy = st.empty()
        status_build_response = st.empty()
    
        status_parse_intent.info('🔍 Parsing your trip request...')
        status_flight_search.info(f'⏳ Waiting to search flights for {destination_input}...')
        status_check_policy.info('⏳ Waiting to check policies...')
        status_build_response.info('⏳ Waiting to build respond...')
        
        try:
            result = asyncio.run(run_agent(
                employee_id = employee_input,
                destination_text = destination_input,
                departure_date = departure_date_input.strftime('%Y-%m-%d')
            ))
            status_parse_intent.success('✅ Trip request parsed')
            status_flight_search.success(
                f'✅ Found: {len(result.get("flight_results", []))} flight option(s).'
            )
            status_check_policy.success(
                f'✅ Policy check complete: {len(result.get("compliant_flights", []))}'
            )
            status_build_response.success(
                '✅ Response ready'
            )
            
        except Exception as e:
            result = {}
            status_parse_intent.error('❌ Failed to run agent')
            status_flight_search.error('❌ Flight search did not complete')
            status_check_policy.error('❌ Policy check did not complete')
            status_build_response.error('❌ Response generation failed')
            st.error(f'Agent error: {e}')
        
    with col2: 
        st.subheader('Your Trip')
       
        destination = result.get('destination')
        image = get_destination_image(destination)
        
        if image:
            st.image(image, width='stretch')
        
        else:
            st.info('🌍 No destination image')
        
        response_text = result.get('response', 'No response generated.')
        st.markdown(response_text.replace('$', '\\$'))