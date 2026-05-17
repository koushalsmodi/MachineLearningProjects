import random

cards = ["jack", "king", "queen"]

# inplace shuffling randomly (no value is returned like choice or randint)
random.shuffle(cards)

for card in cards:
    print(card)