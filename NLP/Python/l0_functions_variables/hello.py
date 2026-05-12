# Ask user for their name
name = input("What's your name? ").strip().title()

first, last = name.split()

# Say hello to user
print(f"hello, {first} {last}")
