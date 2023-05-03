import requests
import string
from datetime import datetime, timedelta


def remove_non_utf8_chars(s):
    return s.encode("utf-8", errors="ignore").decode("utf-8")


def clean_list_of_dicts(list_of_dicts):
    """
    Remove non utf-8 characters from a list of dictionaries.

    Args:
        list_of_dicts (list): List of dictionaries.

    Returns:
        list: List of dictionaries with non utf-8 characters removed.
    """
    for dictionary in list_of_dicts:
        for key, value in dictionary.items():
            if isinstance(value, str):
                dictionary[key] = remove_non_utf8_chars(value)
    return list_of_dicts


def get_top_10_ai_news(api_key="b206cc24b665410ca0e60240ad6a725a"):
    """
    Get top 10 AI news articles from the last week.

    Args:
        api_key (str, optional): News API key. Defaults to "b206cc24b665410ca0e60240ad6a725a".

    Returns:
        list: List of dictionaries containing the number, title, description, and url of each article.
    """
    url = "https://newsapi.org/v2/everything"

    one_week_ago = (datetime.now() - timedelta(weeks=1)).strftime("%Y-%m-%dT%H:%M:%S")

    query_params = {
        "q": "machine learning OR artificial intelligence OR AI OR deep learning",
        "from": one_week_ago,
        "sortBy": "popularity",
        "pageSize": 10,
        "page": 1,
        "apiKey": api_key,
    }

    response = requests.get(url, params=query_params)
    formatted_articles = []
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        for idx, article in enumerate(articles, start=1):
            title = article["title"]
            description = article["description"]
            url = article["url"]
            ds_result = {"number": idx, "title": title, "description": description, "url": url}
            formatted_articles.append(ds_result)
        cleaned_articles = clean_list_of_dicts(formatted_articles)
        return cleaned_articles

    else:
        print(f"Error news API: {response.status_code}")
        return []
