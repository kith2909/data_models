"""
Example file to simulate an ETL process within a docker pipeline
- Extracts from a mongo db
- Transforms the collections
- Loads the transformed collections to postgres db

To be started by docker (see ../docker-compose.yml)

For inspecting that ETL worked out: docker exec -it pipeline_example_my_postgres_1 psql
"""

import pymongo
import sqlalchemy as sqla # use a version prior to 2.0.0 or adjust creating the engine and df.to_sql()
import psycopg2
import time
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import re

def mongo_init():
    # mongo db definitions
    client = pymongo.MongoClient('mongodb', port=27017)  
    redd = client.reddit #mongo database  
    return redd.posts



def postgres_init():

    # postgres db definitions
    conn_string_pg = f"postgresql://postgres:postgreskith@postgres:5432/reddit_rgdb"

    conn = psycopg2.connect(conn_string_pg)
    conn.autocommit = True
    cursor = conn.cursor()
    
    time.sleep(3)  # safety margine to ensure running postgres server

    create_table_string ="CREATE TABLE IF NOT EXISTS reddits (time TEXT, reddit TEXT, topic TEXT, pos NUMERIC, neu NUMERIC, neg NUMERIC, compound NUMERIC);"
    
    logging.critical(f"Creating table reddits {create_table_string} **************")
    cursor.execute(create_table_string)
    logging.critical("Created table reddits")
    conn.commit()
    
    return conn


def extract(coll, limit=10):
    """
    With connection coll we are extracting rows hrom mongo database
    """
    # We are loading only the last 5 entries for speed/debugging
    extracted_reddits = list(coll.find(limit = limit))
    
    logging.critical(f"\n---- {limit} reddits extracted ----\n")
    
    return extracted_reddits


def regex_clean(text):
    """
    Function to clean the text corpus.
    """
    # Remove apostrophs
    text = text.replace("'", " ")

    # Remove URLs
    text = re.sub(r"\S*https?:\S*", "", text)
    
    # Remove HTML tags
    text = re.sub(re.compile("<.*?>"), "", text)
    
    # Remove line breaks and tabs
    text= re.sub(r'\s+', ' ', text.strip())

    return text

def sentiment_analysis(text):
    #placeholder for real sentiment analysis function
    return 1

def sentiment_score(text):
    '''
    Returns a dataframe of sentiment scores for a given text in a dictionary format/Dataframe format
    '''
    scores = analyser.polarity_scores(text)
    score_df = pd.DataFrame(
        data = {k:[v] for (k,v) in scores.items()},
        index = [text])

    return scores


def transform_reddit(extracted_reddits):
    '''
    Transwormation and preparing data for a longtime storage
    '''

    count = len(extracted_reddits)
    logging.critical(count)
 
    transformed_reddits = []
    
    for item in extracted_reddits:
    
        # optional just to see what is going on:
        logging.critical(f"Extracted from reddit: {item}")
    
        #here we select the 'text' key from the dictoinary
        text = item['text']
   
        #... clean it using the regex cleaning function (which currently does nothing)
        text = regex_clean(text)
        logging.critical(f"========Sentiment: {text} ============")
        #...perform sentiment analysis (currently returns 1 for all text - yours will be different)
        sentiment = sentiment_score(text)
        item['text'] = text
        logging.critical(f"========Sentiment: {sentiment} ============")
        #... add a field to the post dictionary called "sentiment" that contains this value
        item['pos'] = sentiment['pos']
        item['neu'] = sentiment['neu']
        item['neg'] = sentiment['neg']
        item['compound'] = sentiment['compound']

        # ... and finally append the post to our list of transformed reddits
        transformed_reddits.append(item)
        

    return transformed_reddits


def load(conn, transformed_reddits):
    '''
    Loading transformed_reddits for longtime storage with connection conn 
    '''
    
    for post in transformed_reddits:
        insert_query = 'INSERT INTO reddits (time, reddit, topic, pos, neu, neg, compound) VALUES (%s, %s, %s, %s,  %s,  %s,  %s) ON CONFLICT DO NOTHING;'
        cursor = conn.cursor()
        cursor.execute(insert_query, 
                   (post['date'], post['text'], post['topic'], 
                    post['pos'], post['neu'], post['neg'], post['compound']))

        logging.info(f"New reddit post incoming: {post['text']} with sentiment score {post['compound']}")
        logging.info("\n---- new reddit post loaded to postgres db ----\n")
    
    return None



if __name__ == '__main__':
    time.sleep(120)
    analyser = SentimentIntensityAnalyzer()
    logging.critical('-------------------connection = postgres + mongodb----------------------------')
    posts = mongo_init()
    connection = postgres_init()

    extracted_reddits = extract(posts, 100)
    logging.critical('---------------------Reddits extracted------------------------')

    transformed_reddits = transform_reddit(extracted_reddits)
    logging.critical('-------------------Load transformed_reddits----------------------------')
    load(connection, transformed_reddits)
    connection.close()