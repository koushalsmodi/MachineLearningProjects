import os
import time
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("WEATHERSTACK_API_KEY")

def get_weather(cities):
    url = "https://api.weatherstack.com/current"

    for city in cities:
        params = {"access_key": api_key, "query": city}

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if response.status_code != 200:
                print(f"HTTP Error for {city}: {response.status_code}")
                time.sleep(1) 
                continue
            
            if "error" in data:
                print(f"API Error for {city}")
                time.sleep(1)
                continue

            if "current" not in data:
                print(f"Unexpected response for {city}:")
                time.sleep(1)
                continue

            current = data["current"]
            print(f"{city}: {current['temperature']} degrees Celsius, {current['weather_descriptions'][0]}\n")

        except Exception as e:
            print(f"Exception occurred for {city}: {e}")

        time.sleep(1)

cities = ["Mumbai", "New Delhi", "Bharuch", "New York", "Jaipur", "Kashmir", "San Francisco", "Los Angeles", "Toronto", "Ontario", "Surat", "Ahmedabad"]
get_weather(cities)
