import tweepy, time, sys
import hashlib  # hash do tweet
import json     # escrever JSON
import os.path  # paths do sistema
import os       # ler variaveis de ambiente
import time     # sleep
import normalize_tweets
from dotenv import load_dotenv # ler variaveis de ambiente do arquivo .env

load_dotenv()

if not os.path.exists('dados/.dummy'):
    print("Faltando pasta ./dados/ (arquivo .dummy nao existe)")
    raise

if not os.path.exists('dados/tweets.json'):
    print("Faltando arquivo ./dados/tweets.json [execute primeiro o script @elasnacamara.py")
    raise

if not os.getenv("CONSUMER_KEY"):
    print("Faltando configurar ENV CONSUMER_KEY")
    raise
if not os.getenv("CONSUMER_SECRET"):
    print("Faltando configurar ENV CONSUMER_SECRET")
    raise
if not os.getenv("ACCESS_KEY"):
    print("Faltando configurar ENV ACCESS_KEY")
    raise
if not os.getenv("ACCESS_SECRET"):
    print("Faltando configurar ENV ACCESS_SECRET")
    raise


dirName = 'dados/tweets-enviados/'
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Diretorio " , dirName ,  " criado")

with open('dados/tweets.json') as f:
  tweets = json.load(f)

bearer_token = os.getenv("BEARER_TOKEN")

def post_tweet(text, bearer_token):
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    # Avoid exceeding the Tweet length by trimming the message
    if len(text) > 280:
        text = text[:277] + "..."

    payload = json.dumps({"text": text})

    response = requests.post(
        "https://api.twitter.com/2/tweets",
        headers=headers,
        data=payload)

    return response

for tweet in tweets:
    text = tweet['tweet']
    result = hashlib.md5(text.encode())
    file_name = f'{REQUIRED_DIRS[1]}/{result.hexdigest()}'

    if os.path.exists(file_name):
        print(f"Tweet '{text}' has been tweeted before")
        continue

    print(f"Tweeting: '{text}'...")
    response = post_tweet(text, bearer_token)

    if response.status_code != 200:
        print(f"Failed to send tweet: '{text}'")
        print(response.json())
        continue

    with open(file_name, 'w') as outfile:
        json.dump(response.json(), outfile)

    if bool(os.getenv("RANDOM_SLEEP_BETWEEN_TWEETS")):
        time.sleep(300)  # wait for 5 minutes

print("All tweets sent successfully!")
