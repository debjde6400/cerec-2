import re

def clean_text(string: str, punctuations=r'''!()-[]{};:'"\,<>./?@#$%^&*_~''', stop_words=['the', 'a', 'and', 'is', 'be', 'will']) -> str:
  ''' Method to clean text '''
  
  # cleaning the urls
  string = re.sub(r'https?://\S+|www\.\S+', '', string)

  # cleaning the html elements
  string = re.sub(r'<.*?>', '', string)

  # removing the punctuations
  for x in string.lower():
    if x in punctuations:
      string = string.replace(x, "")

  # converting the text to lower
  string = string.lower()

  # removing stopwords
  string = ' '.join([word for word in string.split() if word not in stop_words])

  # cleaning the whitespaces
  string = re.sub(r'\s+', ' ', string).strip()

  return string

def create_unique_word_dict(text:list) -> dict:
  '''
  A method that creates a dictionary where the keys are unique words and key values are indices
  '''
  # getting all unique words from our text and sorting them alphabetically
  words = list(set(text))
  words.sort()

  # creating the dictionary for the unique words
  unique_word_dict = {}
  for i, word in enumerate(words):
    unique_word_dict.update({ word: i })
    return unique_word_dict

texts = ['Ata gachhe tota pakhi', 'Dalim gachhe mou']

# defining window for context
window = 2

# creating a placeholder for scanning of word list
word_lists = []
all_text = []

for text in texts:

  # cleaning the text
  text = clean_text(text)

  # appending to the all text list
  all_text += text
  text = text.split(' ')

  # creating a context dictionary
  for i, word in enumerate(text):
    print(word)
    for w in range(window):
      
      # getting context that is ahead by *window* words
      if i + 1 + w < len(text):
        word_lists.append([word] + [text[(i + 1 + w)]])

      # getting context that is behind by *window* words
      if i - w - 1 >= 0:
        word_lists.append([word] + [text[(i - w - 1)]])
  print(text)
  print(all_text)
      
print(word_lists)
print(create_unique_word_dict(texts))