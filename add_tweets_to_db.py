from collect_tweets import get_tweets, verify_tweets, preprocess_tweet
import sqlite3
import datetime
import os.path
import spacy
import collections


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = BASE_DIR+"/tweets.db"
model_path = BASE_DIR+ "/model"


nlp = spacy.load(model_path)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

tweets = get_tweets("bitcoin")

verified, normal = verify_tweets(tweets)

cursor.execute("""
    SELECT id FROM normal_tweets_v2
""")
known_normal_tweets = cursor.fetchall()

cursor.execute("""
    SELECT id FROM verified_tweets
""")
known_verified_tweets = cursor.fetchall()
def is_relevant(tweet):
    'Tweet is already preprocessed'
    doc = nlp(tweet)
    if doc.cats['Relevant'] > 0.3:
        return True

counter = []
def input_tweets(tweet_type, known, table):
    for i, tweet in enumerate(tweet_type):
        if tweet['id'] not in known:
            date = datetime.datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            message = preprocess_tweet(tweet['text'])
            if (is_relevant(message)) or (table == 'verified_tweets'):
                cursor.execute(f'''INSERT INTO {table} 
                VALUES (?, ?, ?)''', (tweet['id'], date, message))
                counter.append(i)
            else:
                print(f'bad message:{message}')
input_tweets(verified, known_verified_tweets, 'verified_tweets')
verified_tweet_n = counter
counter = []
input_tweets(normal, known_normal_tweets, 'normal_tweets_v2')
input_tweet_n = counter
print(f'Added {len(input_tweet_n)} normal tweets and {len(verified_tweet_n)} verified tweets')
conn.commit()
