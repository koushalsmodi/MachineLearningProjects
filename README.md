# Similarity and Distance Measures
We can measure similarity between users and items.
User-item interaction matrix
Assuming a n * m matrix in 2 d space, let's suppose rows to be users (U1, U2, ..Un)
and columns to be items (I1, I2, .., Im).
This means a row shows the set of items (Iu) purchased by a user u
and a column shows the set of users (Ui) purchasing an item i.

## Euclidean Distance
D(User1, User2) = sqrt((difference of values between the rows)^2)
smaller distance = users have more similar purchase behaviors
larger distance = users have less similar purchase behaviors
## Jaccard Similarity
J(A,B) = |A intersection B| / |A union B|
J(A,B) = # of common elements / # of unique elements in  either set
maximum of 1 if two users purchased exactly the same set of items
minimum of 0 if two users purchased completely disjoint set of items
row = user-based recommendations
col = item-based recommendations
## Cosine Similarity
cos(theta) = 1 (when theta = 0) means rated by same users and they all agree
cos(theta) = 0 (when theta = 90) means rated by different sets of users
cos(theta) = -1 (when theta = 180) means rated by same users but they completely disagree
## Pearson Distance 
r = covariance(X,Y) / (std_dev(X) * std_dev(Y))
r = 1: perfect positive correlation
r = -1: perfect negative correlation
r = 0: no correlation
measures how well two variables move together
adjusts for mean and variance differences between users
more robust to rating scale differences than cosine similarity 