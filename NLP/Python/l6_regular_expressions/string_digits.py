import re 

user = input("What's the input? ").strip()

if re.search("[0-9]+", user, flags=re.IGNORECASE):
    print("Found")
    
else:
    print("Not Found")