import json
import asyncio
import config as cf
from slack_bolt.async_app import AsyncApp
from slack_sdk.webhook.async_client import AsyncWebhookClient
import pyjokes
import requests
import logging
import time
import psycopg2
import flask


def postgres_init(topic = 'Lordofthelost'):

    # postgres db definitions
    conn_string_pg = f"postgresql://postgres:postgreskith@postgres:5432/reddit_rgdb"

    conn = psycopg2.connect(conn_string_pg)
    conn.autocommit = True
    cursor = conn.cursor()
    
    time.sleep(3)  # safety margine to ensure running postgres server


    logging.critical(f'-----------------+--{topic}--+--------------------------')
    cursor.execute(f"SELECT * FROM reddits WHERE topic = '{topic}' ORDER BY compound DESC LIMIT 10;")
    conn.commit()
   
    result = cursor.fetchall()
   # for row in result:
   # logging.critical(f'-----------------+--{row}--+--------------------------')

    return result


def data_format(posts, url):
    
    for post in posts:
        logging.critical(f'-----------------+--{post}--+--------------------------')
        joke = "*" + pyjokes.get_joke() + "*"
        data = {'blocks': [{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": post[1] +'\n' + joke
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": "https://i.pinimg.com/564x/69/f1/d1/69f1d1fa8420d23df0755f77e0dea288.jpg",
                        "alt_text": "Deadline Pic"
                    }
                }]
        }
        requests.post(url=url, json = data)
        time.sleep(3)
    return data

def getmenu():
    data1 = {
        "text": "Simple introduction",
        "attachments": [
            {
                "pretext": "Please, choose a topic.:robot_face:",
                "text": "What would you like to know?",
                "callback_id": "os",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "liverpool",
                        "text": ":musical_score:  Liverpool",
                        "type": "button",
                        "value": "liv"
                    },
                    {
                        "name": "eurovosion",
                        "text": ":guitar: Eurovision",
                        "type": "button",
                        "value": "euro"
                    },
                    {
                        "name": "lordlosts",
                        "text": ":microphone: Lordofthelost",
                        "type": "button",
                        "value": "lordlosts"
                    }
                ]
            }
        ]
    }
    return data1

if __name__ == '__main__':

    webhook_url = "https://hooks.slack.com/services/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"

    time.sleep(200)
    json =  getmenu()
    
    requests.post(url=webhook_url, json =  json)

    logging.critical('-------------------postgres_init()----------------------------')
    posts = postgres_init('Lordofthelost')
    logging.critical('-------------------data_format(posts)----------------------------')
    data = data_format(posts, url=webhook_url)
    

    

