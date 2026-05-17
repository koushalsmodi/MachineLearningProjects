import requests
import sys
import json

if len(sys.argv) != 2:
    sys.exit()
    
url = "https://itunes.apple.com/search?entity=song&limit24&term="+ sys.argv[1]

response = requests.get(url)

data = response.json()
for result in data["results"]:
    print(result["trackName"])
    