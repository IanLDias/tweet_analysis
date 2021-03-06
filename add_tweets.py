from Causality_analysis import get_tweets, verify_tweets, preprocess_tweet
import sqlite3
import datetime
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "tweets.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

tweets = get_tweets("bitcoin")

verified, normal = verify_tweets(tweets)

cursor.execute("""
    SELECT id FROM normal_tweets
""")
known_normal_tweets = cursor.fetchall()

cursor.execute("""
    SELECT id FROM verified_tweets
""")
known_verified_tweets = cursor.fetchall()

def input_tweets(tweet_type, known, table):
    for tweet in tweet_type:
        if tweet['id'] not in known:
            date = datetime.datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            message = preprocess_tweet(tweet['text'])
            cursor.execute(f'''INSERT INTO {table} 
            VALUES (?, ?, ?)''', (tweet['id'], date, message))

input_tweets(verified, known_verified_tweets, 'verified_tweets')
input_tweets(normal, known_normal_tweets, 'normal_tweets')
# for tweet in verified:
#     if tweet['id'] not in known_verified_tweets:
#         date = datetime.datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
#         message = preprocess_tweet(tweet['text'])
#         cursor.execute(f'''INSERT INTO verified_tweets 
#         VALUES (?, ?, ?)''', (tweet['id'], date, message))

# for tweet in normal:
#     if tweet['id'] not in known_normal_tweets:
#         date = datetime.datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
#         message = preprocess_tweet(tweet['text'])
#         cursor.execute(f'''INSERT INTO normal_tweets 
#         VALUES (?, ?, ?)''', (tweet['id'], date, message))

print(f'Added {len(normal)} normal tweets and {len(verified)} verified tweets')
conn.commit()
