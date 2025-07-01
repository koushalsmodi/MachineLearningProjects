# builds Markov models from text and can generate new, similar-sounding text
import markovify
import sys

# Read the text from the file
if len(sys.argv) != 2:
  sys.exit("Usage: python3 generator.py sample.txt")

with open(sys.argv[1]) as f:
  text = f.read()

# Train model
# Create a markov chain model from text input
# model learns which words are likely to follow others based on the structure of the sample.txt
text_model = markovify.Text(text)

# Generate sentences
print()

# tries to build a grammatically plausible sentence using the probabilities from the model
for i in range(5):
  print(text_model.make_sentence())
  print()
  
"""
Output:
  
I myself could move thee, I will speak to lady afterward In way of the which we will go.

Then he was dead and rotten; sweet chucks, beat not the creaking of shoes nor the hand that stabbed thy father bore it.

And may it please you to your offices.

Re-enter MISTRESS FORD come forward AJAX.

Sir, I say to you.
  """