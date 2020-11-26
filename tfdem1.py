import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

#nltk.download('punkt')
example_text = "Hello Mr. Dhalu, how are you doing today? The weather is great and Python is awaawa. The sky is green. You should not eat cardboard"

print(sent_tokenize(example_text))
print(sent_tokenize(example_text))