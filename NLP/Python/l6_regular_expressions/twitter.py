import re 
# https://x.com/davidjmalan

url = input("URL: ").strip()

# ?: grouping that doesn't need to be taken as output
if matches := re.search(r"^https?://(?:www\.)?x\.com/([a-z0-9_]+)$", url, flags=re.IGNORECASE):
    print("Username:", matches.group(1))
