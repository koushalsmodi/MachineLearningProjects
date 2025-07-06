from scipy.spatial.distance import cosine

import math
import numpy as np

with open("words.txt") as f:
    words = dict()
    for line in f:
        row = line.split()
        word = row[0]
        vector = np.array([float(x) for x in row[1:]])
        words[word] = vector 
        
def distance(w1, w2):
    return cosine(w1,w2)

def closest_words(embedding):
    distances = { 
    w: distance(embedding, words[w])
    for w in words
    }
    # to sort based on the value associated with each key, not the key itself
    return sorted(distances, key = lambda w: distances[w])[:10]

def closest_word(embedding):
    return closest_words(embedding)[0]

""" 
from vectors import *
words["book"]
words["apple"]

distance(words["apple"], words["banana"])
0.48883722750651326

distance(words["apple"], words["book"])
0.7921976687234645

closest_words(words["book"])[:10]
['book', 'books', 'essay', 'memoir', 'essays', 'novella', 'anthology', 'blurb', 'autobiography', 'audiobook']

closest_words(words["apple"])[:10]
['apple', 'blackberry', 'ipad', 'webos', 'iphone', 'android', 'macs', 'kitkat', 'smartphone', 'icloud']

closest_word(words["king"] - words["man"] + words["woman"])
'queen'

closest_word(words["revenue"] - words["cost"] + words["profit"])
'revenue'
"""