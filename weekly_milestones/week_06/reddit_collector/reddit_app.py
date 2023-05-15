
import requests
from requests.auth import HTTPBasicAuth
import pymongo
import time
import sys
from config import tokens  # This is from our config.py containing our credentials.
import datetime as dt
import logging



def token_init():
    '''
    PREPARE AUTHENTIFICATION INFORMATION
    FOR REQUESTING A TEMPORARY ACCESS TOKEN
    '''
    sys.stdout.reconfigure(encoding='utf-8')  \

    basic_auth = HTTPBasicAuth(
        username=tokens['client_id'],  # the client id
        password=tokens['secret']      # the secret
    )

    GRANT_INFORMATION = dict(
        grant_type="password",
        username=tokens['username'],  # REDDIT USERNAME
        password=tokens['password']   # REDDIT PASSWORD
    )

    # POST REQUEST FOR ACCESS TOKEN
    headers = {'User-Agent': 'ApplicationDocker'}
    POST_URL = "https://www.reddit.com/api/v1/access_token"

    access_post_response = requests.post(
        url=POST_URL,
        headers=headers,
        data=GRANT_INFORMATION,
        auth=basic_auth
    ).json()

    # Print the Bearer Token sent by the API
    logging.info(access_post_response)

    # ADDING TO HEADERS THE Authorization KEY

    headers['Authorization'] = access_post_response['token_type'] + ' ' + \
                            access_post_response['access_token']
    
    return headers



def get_post_reddit(db, headers, topics=None, limit = 100):

    for topic in topics:
        URL = f"https://oauth.reddit.com/r/{topic}/new"  # You could also select ".../hot" to fetch the most popular posts.

        logging.info('Request from ', URL, headers)
        response = requests.get(
                    url=URL,
                    headers=headers,
                    params={"limit": limit}
                ).json()
        full_response = response['data']['children']
        
        
            # Go through the full response and define a mongo_input dict
            # see full_response[0]['data'].keys() for a list of possibilities

        for post in full_response:
                data = extract_data(post, topic)
                logging.info("Adding data ====== in", db)
                logging.info(db.count_documents({}))
                try: 
                    res = db.insert_one(data)
                    logging.info("Adding one post to a Collection if not exists.\n", db)
                    logging.info(res.inserted_id)
                    logging.info("====== Data added")     
                except:
                    logging.CRITICAL('ERROR or Data already exists')
        

       
def extract_data(post, topic):
    '''
    Extracting data for database
    '''
    _id = post['data']['id']
    subreddit_id = post['data']['subreddit_id']
    time = post['data']['created_utc']  # time in seconds since 1970
    time = dt.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
    subreddit = post['data']['subreddit']  # the above defined 'topic'
    title = post['data']['title']
    text = post['data']['selftext']  # the actual content
    
    #img = post['data']['thumbnail']
    # shorten or lengthen mongo input as you deem fit:

    mongo_input = {'_id': _id, 'sub_id': subreddit_id, 'date': time, 'title': title, 'text': text, 'topic':topic}
    return mongo_input


def mongo_init():
    logging.info("Create connection to MongoDB.\n")
    client = pymongo.MongoClient(host="mongodb", port=27017)
    db = client.reddit
    print("Create connection to a Collection.\n", db.posts)
    return db.posts


def get_info():
    '''
    Workflow pipeline
    Connection to reddit
    Getting information
    '''
    dbase = mongo_init()
    headers = token_init()
    
    logging.info("Get info start.\n")

    reddits = get_post_reddit(
        dbase,
        headers,
        topics=['Liverpool', 'Lordofthelost', 'Eurovision'],
        limit=50
    )


if __name__ == "__main__":
    get_info()
    time.sleep(10)
