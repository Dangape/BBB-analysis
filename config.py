# tweepy-bots/bots/config.py
import tweepy
import logging
import string
import os

logger = logging.getLogger()

def create_api():
    import json
    with open('credentials.txt') as f:
        json_data = json.load(f)

    consumer_key = json_data['consumerKey'] #API key
    consumer_secret = json_data['consumerSecret'] #API key secret
    access_token = json_data['accessToken'] #Access token
    access_token_secret = json_data['accessTokenSecret'] #Access token secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

def remove_hashtag_and_mention(text):
    entity_prefixes = ['@','#']
    for separator in string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


