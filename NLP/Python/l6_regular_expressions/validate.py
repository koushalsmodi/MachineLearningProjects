import re

email = input("What's your email? ").strip()

# re.search(r"^[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.edu$", email)

# + means ..*
# r means raw string
# [] means set of characters allowed
# + means one or more repetitions to the things at left
# [a-zA-Z0-9_] means a through z (caps lock included) + numbers + underscore == \w (word character / alphanumeric symbol)
# flags means re.IGNORECASE, re.MULTILINE, re.DOTALL
# (\w+\.)? means grouping set of characters that are optional

if re.search(r"^\w+@(\w+\.)?\w+\.edu$", email, flags=re.IGNORECASE):
    print("Valid")
    
else:
    print("Invalid")