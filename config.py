# tweepy-bots/bots/config.py
import tweepy
import logging
import string


logger = logging.getLogger()

def create_api():
    consumer_key = 'AxrLnGCzWymdqtyaGyuPps5oa' #API key
    consumer_secret = 'dDZP1s8kCO5fg2yM3sVv60cFb0Zhmj0DT2cgh5ZneJDUEerhQM' #API key secret
    access_token = '1460657321839890436-ZnRI0HMOYTVNpWh7j0QIM4m62G4qCo' #Access token
    access_token_secret = 'janLV9AZyllBqORJJfltkegaeYISDNTbflUZZtCLWmgEB' #Access token secret

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


