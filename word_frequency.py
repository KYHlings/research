import string
import pickle
from collections import Counter

city_names = ['goteborg', 'kiruna', 'ostersund', 'stockholm']
cities = {}
for city in city_names:
    cities[city] = pickle.load(open(f'fallback-tweets/tweets_{city}_1000.p', 'rb'))

# Characters to be removed from tweets
tweet_punctuation = string.punctuation.replace('@', '') + '”' + '“'

tokenized_tweets = []
for city in cities:

    for idx, tweet in enumerate(cities[city]):
        tweet = tweet.lower().replace('\n', ' ')
        table = tweet.maketrans('', '', tweet_punctuation)
        cleaned_tweet = tweet.translate(table)
        tokens = cleaned_tweet.split(' ')

        for token in tokens:
            if "https" in token or '@' in token:
                # Exclude links and username calls in tweets
                continue

            tokenized_tweets.append(token)

word_frequency = Counter(tokenized_tweets)
print(word_frequency)
