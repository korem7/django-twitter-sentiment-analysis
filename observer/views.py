# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

#from django.shortcuts import render

from django.shortcuts import render, HttpResponse
import requests
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from django.http import Http404

class TwitterClient(object):

    def __init__(self):

        consumer_key = 'LKE7F5vvY7ZcPZVsSrG2zhO80'
        consumer_secret = 'ZQzTASgytwsoNt1dwzprwEQrxqPuxhhv2l4vbncArG7KcFGsGG'
        access_token = '916984106323496960-c1LjNWzJKFftpRohzkMPWf4NRNGoJRQ'
        access_token_secret = 'OnvJmO5tN3hHFkQm4MleMwxigEfXm9EZhrWZVilL7zdYG'

        try:

            self.auth = OAuthHandler(consumer_key, consumer_secret)

            self.auth.set_access_token(access_token, access_token_secret)

            self.api = tweepy.API(self.auth)

        except requests.ConnectionError as err:
            err = 'Error: Authentication Failed'
            raise Http404(err)

    def clean_tweet(self, tweet):

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ /  \ /  \S +)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):

        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count):

        tweets = []

        try:

            fetched_tweets = tweepy.Cursor(self.api.search, q=query, rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(count)

            for tweet in fetched_tweets:

                parsed_tweet = {}

                parsed_tweet['text'] = tweet.text

                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                if tweet.retweet_count > 0:

                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as err:
            raise Http404(err)


def home(request):
    postive_tweets = []
    negative_tweets = []
    tweet_count = 250
    retrieve_count = 0
    compnay_name = ""
    try:
        if request.method == 'POST':
            search_id = request.POST['searchcompany']
            api = TwitterClient()

            tweets = api.get_tweets(query=search_id, count=tweet_count)

            ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
                    
            ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']           

            result_positive = round((100 * len(ptweets)/len(tweets)),1)
                    
            result_negative = round((100 * len(ntweets) / len(tweets)),1)

            result_neutral = round((100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)),1)

            compnay_name  = "Sentiment analysis about \"" + search_id  + "\""

            for i in tweets:
                retrieve_count = retrieve_count +1


            return render(
                    request,
                    'home.html',
                    context = {'tweet_count':tweet_count, 'result_positive':result_positive,'result_negative':result_negative,'result_neutral':result_neutral, 'compnay_name': compnay_name, 'retrieve_count':retrieve_count},
                )
        else:
            return render(request, 'home.html')

    except requests.ConnectionError as err:
        raise Http404(err)


