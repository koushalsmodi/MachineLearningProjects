# Weather API Script

A Python script that fetches and displays current weather: temperature and condition information for multiple cities using the Weatherstack API.

## Features

- Fetches real-time weather data for multiple cities worldwide
- Displays temperature in Celsius and weather condition
- Includes error handling for API requests
- Rate limiting to respect API constraints
- Environment variable support for secure API key management

## Sample Output

```
Mumbai: 27 degrees Celsius, Smoke
New Delhi: 19 degrees Celsius, Mist
Bharuch: 21 degrees Celsius, Sunny
New York: 15 degrees Celsius, Overcast
Jaipur: 20 degrees Celsius, Mist
Kashmir: 26 degrees Celsius, Partly Cloudy
San Francisco: 19 degrees Celsius, Partly cloudy
Los Angeles: 22 degrees Celsius, Clear
Toronto: 16 degrees Celsius, Light Rain
Ontario: 27 degrees Celsius, Clear
Surat: 22 degrees Celsius, Sunny
Ahmedabad: 21 degrees Celsius, Haze
```

## Prerequisites

- Python 3.x
- `requests` library
- `python-dotenv` library
- Weatherstack API key (free tier available)

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install requests python-dotenv
```

3. Sign up for a free API key at [Weatherstack](https://weatherstack.com/)

4. Create a `.env` file in the project root directory:
```
WEATHERSTACK_API_KEY=your_api_key_here
```

## Usage

Run the script from the command line:

```bash
python3 weather_API_script.py
```

## Configuration

To modify the list of cities, edit the `cities` list in the script:

```python
cities = ["Mumbai", "New Delhi", "Bharuch", "New York", "Jaipur", ...]
```

You can add or remove cities as needed. The script will fetch weather data for each city sequentially.

## How It Works

1. Loads the API key from the `.env` file
2. Iterates through the list of cities
3. Makes an API request to Weatherstack for each city
4. Parses and displays the temperature and weather description
5. Includes a 1-second delay between requests to avoid rate limiting
