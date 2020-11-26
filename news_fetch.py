import requests

_NEWS_API = "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=b5f42b73b64543b4bfa3af7ffdbc436e"

def fetch_bbc_news():
  bbc_page_fetch = requests.get(_NEWS_API).json()
  article = bbc_page_fetch["articles"]
  results = []
  
  for a_article in article:
    results.append(a_article)
    
  for a_result in range(len(results)):
    print(str(a_result + 1) + ") ", results[a_result]['title'])
    
if __name__ == '__main__':
  fetch_bbc_news()