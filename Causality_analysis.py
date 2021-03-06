import requests
import os
import json
import sqlite3  
import re
from env import BEARER

conn = sqlite3.connect('tweets.db')

bearer_token = BEARER
print(bearer_token)
headers = {"Authorization": "Bearer {}".format(bearer_token)}

def create_url(query):
    query = query
    tweet_fields = "tweet.fields=author_id,created_at"
    user_fields = "user.fields=entities"
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}".format(
        query, user_fields, tweet_fields
    )
    return url

def create_url_verified(id):
    url = f"https://api.twitter.com/2/users?ids={id}&user.fields=verified"
    return url

def get_tweets(query):
    url = create_url(query)
    r = requests.request("GET", url, headers = headers)
    return r

def verify_tweets(r):
    tweets_verified = []
    tweets_normal = []
    for tweet in r.json()['data']:
        url = create_url_verified(tweet['author_id'])
        r = requests.request("GET", url, headers = headers)
        verified = r.json()['data'][0]['verified']
        if verified:
            print(tweet)
            tweets_verified.append(tweet)
        else:
            tweets_normal.append(tweet)
    return tweets_verified, tweets_normal

def preprocess_tweet(tweet):
    pattern = "[^0-9a-zA-Z]+"
    tweet = re.sub(pattern, ' ', tweet)
    return tweet.strip()

tweets = get_tweets("bitcoin")

verified = verify_tweets(tweets)
verified
