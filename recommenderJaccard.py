import gzip
from collections import defaultdict
import random
import numpy as np
import scipy.optimize

path = '/Users/koushalsmodi/recommenders/MachineLearningProjects/amazon_reviews_us_Musical_Instruments_v1_00.tsv.gz'

f = gzip.open(path, 'rt', encoding='utf8')

header = f.readline()
header = header.strip().split('\t')

print(header)

# GOAL: make recommendations on products based on users' purchase histories.
# based on: customer_id and product_id

dataset = []

for line in f:
    fields = line.strip().split('\t')
    d = dict(zip(header, fields))
    d['star_rating'] = int(d['star_rating'])
    d['helpful_votes'] = int(d['helpful_votes'])
    d['total_votes'] = int(d['total_votes'])
    
    dataset.append(d)
print()
print(dataset[0])

# set of Users per item (Ui), in other words, cols
usersPerItem = defaultdict(set)
# set of Items per user (Iu), in other words, rows
itemsPerUser = defaultdict(set)

itemNames = {}
for d in dataset:
    user, item = d['customer_id'], d['product_id']
    usersPerItem[item].add(user)
    itemsPerUser[user].add(item)
    itemNames[item] = d['product_title']

# Jaccard Similraity
# J(A,B) = # of common elements / # of unique elements in either set
# J(A, B) = A intersection B / A union B

def Jaccard(s1, s2):
    numer = len(s1.intersection(s2))
    denom = len(s1.union(s2))
    
    return numer / denom

# recommendation function that returns items similar to candidate item i
# Find the set of users who purchased i
# Iterate over all other items other than i
# For all other items, compute their similarity with i (and store it)
# Sort all other items by (Jaccard) similarity
# return the most similar

def mostSimilar(i):
    similarities = []
    users = usersPerItem[i]
    for i2 in usersPerItem:
        if i2==i:
            continue
        sim = Jaccard(users, usersPerItem[i2])
        similarities.append((sim,i2))
    similarities.sort(reverse=True)
    return similarities[:10]
print()
print(dataset[2])
print()
query = dataset[2]['product_id']
print(query)
print()

# query output is product id
print(mostSimilar(query))
print()

print(itemNames[query])
print()
print([itemNames[x[1]] for x in mostSimilar(query)])

# more efficient algorithm
# Find the set of users who purchased i
# Iterate over all users who purchased i
# Build a candidate set from all items those users consumed
# For items in this set, compute their similarity with i (and store it)
# Sort all other items by (Jaccard) similarity
# Return the most similar

def mostSimilarFast(i):
    similarities = []
    users = usersPerItem[i]
    candidateItems = set()
    for u in users:
        candidateItems = candidateItems.union(itemsPerUser[u])
    for i2 in candidateItems:
        if i2 == i:
            continue
        sim = Jaccard(users, usersPerItem[i2])
        similarities.append((sim, i2))
    similarities.sort(reverse=True)
    return similarities[:10]
print()
print(mostSimilarFast(query))