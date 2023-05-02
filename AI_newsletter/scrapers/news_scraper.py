import requests
from datetime import datetime, timedelta

def get_top_10_ai_news(api_key="b206cc24b665410ca0e60240ad6a725a"):
    url = "https://newsapi.org/v2/everything"

    one_week_ago = (datetime.now() - timedelta(weeks=1)).strftime("%Y-%m-%dT%H:%M:%S")
    
    query_params = {
        "q": "machine learning OR artificial intelligence OR AI OR deep learning",
        "from": one_week_ago,
        "sortBy": "popularity",
        "pageSize": 10,
        "page": 1,
        "apiKey": api_key
    }

    response = requests.get(url, params=query_params)
    formatted_articles = []
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        for idx, article in enumerate(articles, start=1):
            title = article["title"]
            url = article["url"]
            ds_result = {'number': idx, 'title': title, 'url': url}
            formatted_articles.append(ds_result)
        return formatted_articles

    else:
        print(f"Error: {response.status_code}")
        return []
    


    



