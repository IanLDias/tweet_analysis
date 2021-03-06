import sqlite3 
conn = sqlite3.connect('tweets.db')

c = conn.cursor()

c.execute('''CREATE TABLE verified_tweets
    (id INT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    message VARCHAT(280) NOT NULL)
''')

c.execute('''CREATE TABLE normal_tweets
    (id INT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    message VARCHAR(280) NOT NULL)
''')

c.execute('''CREATE TABLE normal_tweets_v2
    (id INT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    message VARCHAR(280) NOT NULL)
''')

#c.execute('DROP TABLE normal_tweets')
#c.execute('DROP TABLE verified_tweets')
conn.commit()