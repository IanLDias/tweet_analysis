import sqlite3 
import pandas as pd
conn = sqlite3.connect('tweets.db')

c = conn.cursor()

c.execute('''
SELECT * FROM normal_tweets
''')
rows = c.fetchall()
df = pd.DataFrame(rows, columns=['id', 'datetime', 'tweet'])
sample = df.sample(len(df))
sample['tweet'].to_csv('data_labeling/FULL_label_data.txt') 