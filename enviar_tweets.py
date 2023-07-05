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

def refresh_bearer_token(consumer_key, consumer_secret, refresh_token):
    key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    auth_url = 'https://api.twitter.com/2/oauth2/token'

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'refresh_token',
        'client_id': consumer_key,
        'refresh_token': 
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

    if auth_resp.status_code != 200:
        raise Exception("Failed to refresh token: {}".format(auth_resp.text))
    else:
        token_type = auth_resp.json()['token_type']
        if token_type != 'bearer':
            raise Exception("Unexpected token type: {}".format(token_type))
        
    return auth_resp.json()['access_token']

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
