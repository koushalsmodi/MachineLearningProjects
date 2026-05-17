name = input("What's your name? ")

with open('names.txt', 'a') as f:
    f.write(f"{name}\n")
    # no need to for close line using "with"


        