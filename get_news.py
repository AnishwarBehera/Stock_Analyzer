import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_company_news(company_name):
    subscription_key = os.getenv("NEWS_ID")
    endpoint = "https://api.bing.microsoft.com/v7.0/news/search"

    if not subscription_key:
        return "Error: Bing API key not set."

    query = f"{company_name} news"
    mkt = "en-IN"
    params={'q':query, 'mkt':mkt,"freshness":'Month','count':5}
    headers={'Ocp-Apim-Subscription-Key':subscription_key}

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        news_json = response.json()

        news_articles = []
        for article in news_json.get("value", []):
            news_articles.append({
                "name": article.get("name"),
                "url": article.get("url"),
                "description": article.get("description"),
                "datePublished": article.get("datePublished"),
                "provider": article.get("provider"),
            })
        return news_articles

    except Exception as e:
        return f"Error fetching news: {str(e)}"



