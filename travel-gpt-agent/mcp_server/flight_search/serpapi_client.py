from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERPAPI_KEY")


cabin_class_mapping = {'Economy': 1, 'Premium Economy': 2, 'Business': 3, 'First Class': 4}

def search_flights(origin, destination, departure_date, cabin_class):
    
    cabin_class_type = cabin_class_mapping.get(cabin_class)
    
    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date":  departure_date,
        "currency": "USD",
        "type": 2,
        "travel_class": cabin_class_type,
         "api_key": api_key,
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    print(results)
    print()
    
    best_flights = results.get("best_flights", [])
    flights_to_use = best_flights if best_flights else results.get("other_flights", [])
    flight_results = []
    for flight in flights_to_use:
        flight_dict = {'price': None, 'total_duration': None, 'legs' : []}
        
        price = flight.get('price')
        total_duration = flight.get('total_duration')
        
        flight_dict['price'] = price
        flight_dict['total_duration'] = total_duration
        

        legs = flight.get("flights", [])
        print(f"Total Price: ${price:.2f} and Total Duration: {total_duration} mins")
    
        for leg in legs:
            leg_dict = {'airline': None,
                        'travel_class': None, 'flight_number': None,
                        'departure_airport': None,
                        'departure_time': None,
                        'arrival_airport': None,
                        'arrival_time': None}
            
            airline = leg.get('airline')
            leg_dict['airline'] = airline
            
            travel_class = leg.get('travel_class')
            leg_dict['travel_class'] = travel_class
            
            flight_number = leg.get('flight_number')
            leg_dict['flight_number'] = flight_number
            
            departure_airport = leg.get('departure_airport', {}).get('name')
            departure_time = leg.get('departure_airport', {}).get('time')
            arrival_airport = leg.get('arrival_airport', {}).get('name')
            arrival_time = leg.get('arrival_airport', {}).get('time')
            leg_dict['departure_airport'] =  departure_airport
            leg_dict['departure_time'] =  departure_time
            leg_dict['arrival_airport'] =  arrival_airport
            leg_dict['arrival_time'] =  arrival_time
            
            print(f"- {airline} ({flight_number}) in {travel_class}: {departure_airport} [{departure_time}] -> {arrival_airport} [{arrival_time}]")
            print("-" * 40)
            flight_dict['legs'].append(leg_dict)
        flight_results.append(flight_dict)
        

    return flight_results

# search_flights("PHX", "JFK", "2026-07-16", "Economy")