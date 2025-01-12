import os
import requests

# Replace with your Bearer Token
BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")

# Twitter API v2 endpoint for recent searches
url = "https://api.twitter.com/2/tweets/search/recent"

def get_mentions(ticker: str):
    # Define your username or keywords for mentions
    username = "your_username"  # Replace with your Twitter username (without @)
    keywords = "(BTC OR Bitcoin) (awesome OR amazing OR worst OR hate OR happy)"  # Add additional keywords as needed

    # Build the query
    query = f"{keywords}"  # Search for mentions and keywords

    # Query parameters
    params = {
        "query": query,  # Search query
        "tweet.fields": "created_at,author_id,text",  # Fields to include in the response
        "max_results": 100,  # Adjust based on your needs (max 100)
    }

    # Set up headers with Bearer Token
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    # Make the API request
    response = requests.get(url, headers=headers, params=params)

    # Check for success
    if response.status_code == 200:
        tweets = response.json().get("data", [])
        if tweets:
            for tweet in tweets:
                print(f"Author ID: {tweet['author_id']}")
                print(f"Tweet: {tweet['text']}")
                print(f"Created At: {tweet['created_at']}")
                print("-" * 50)
        else:
            print("No tweets found for the given query.")
    else:
        print(f"Failed to fetch tweets. Status code: {response.status_code}")
        print(response.text)
