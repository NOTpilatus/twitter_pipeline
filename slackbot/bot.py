import slack
from sqlalchemy import create_engine 
import time
import psycopg2
import config 


HOST = config.pg_host
USERNAME = config.pg_username
PORT = config.pg_port
DB = config.pg_db
PASSWORD = config.pg_password
oauth_token = config.slack_token

engine = create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}')
client = slack.WebClient(token=oauth_token)


while True:
    query = '''SELECT * FROM tweets
                 ORDER BY RANDOM()
                 LIMIT 1;'''

    latest_tweet = engine.execute(query)
    response = client.chat_postMessage(channel='#botchannel', text=f"latest tweet:{latest_tweet.first()}")
    time.sleep(30)