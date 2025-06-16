import worldnewsapi
from worldnewsapi.rest import ApiException
import requests

# utilizing API from https://worldnewsapi.com
# current implementation to retrieve news in vietnamese. The free version works okay, but only obtains news within 30 

API_KEY = "..." # insert free worldnews API code here or just ask me for mine
KEY_CONFIG = worldnewsapi.Configuration(api_key={'apiKey': API_KEY}) 

def get_news(category):
    try:
        newsapi_instance = worldnewsapi.NewsApi(worldnewsapi.ApiClient(KEY_CONFIG))
        max_results = 50
        offset = 0
        all_results = []
        
        while len(all_results) < max_results:
            request_count = min(100, max_results - len(all_results)) 
            
            response = newsapi_instance.search_news( 
                source_country='vn',
                language='vn',
                earliest_publish_date='2025-05-17', # if getting error change these dates to represent the current day to 30 days ago (sometimes an error still occurs at exactly 30 days)
                latest_publish_date='2025-06-15',   
                categories=category,
                sort="publish-time",
                sort_direction="desc",
                min_sentiment=-0.8,
                max_sentiment=0.8,
                offset=offset,
                number=request_count
            )
                    
            print("Retrieved " + str(len(response.news)) + " articles. Offset: " + str(offset) + "/" + str(max_results) +
                ". Total available: " + str(response.available) + ".")
            
            if len(response.news) == 0:
                break
                
            all_results.extend(response.news)
            offset += 100

    except worldnewsapi.ApiException as e:
        print("Exception when calling NewsApi->search_news: %s\n" % e)

    for article in all_results:
        print("\nTitle: " + str(article.title))
        print("Author: " + str(article.authors))
        print("URL: " + str(article.url))
        print("Sentiment: " + str(article.sentiment))

    return all_results


def print_article(url):
    api_url = f"https://api.worldnewsapi.com/extract-news?url={url}"
    headers = {
        'x-api-key': API_KEY
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        article_data = response.json()
        print("Title:", article_data.get('title', 'N/A'))
        print("Text:", article_data.get('text', 'N/A'))
        print("Author:", article_data.get('author', 'N/A'))
        print("Publish Date:", article_data.get('publish_date', 'N/A'))
        return article_data
    else:
        print(f"Error: {response.status_code}")
        print("Response:", response.text)
        return f"Error: {response.status_code}"

# **** NOTES ****
# Current api does not need to be translated to Vietnamese; however, it does not bring up many articles for some categories.
# Perhaps web scraping or utilizing more than one API may help improve results for some more niche interests/categories.
# I am considering using the paid version of this API to demo this program better, but for now the free API will do for functionality tests.