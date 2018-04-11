The news_extractor is a tool that allows to clustering users who are interested in the same news.

## IMPORTANT

Is important to have a file called 'credentialsTwitter.json' with your consumer_key, consumer_secret, access_token, access_token_secret

Before starting, install the following python libraries: json, csv, tweepy, langdetect, getopt, nltk

To run **news_extractor.py** you have to give these options:

-n : number of users

-x : url of the news

-f : file name in which you want to save users_names

*example* python3 news_extractor.py -n 10 -x https://www.nytimes.com/2018/03/19/technology/uber-driverless-fatality.html -f uber.csv


To run **get_tweets.py** you have to give these options:

-f : file name from which you want to get users' names

-o : file name in which you want to save users' tweets

*example* python3 get_tweets.py -f uber.csv -o uber_tweets.json

To run **get_nltk_features.py** you have to give these options:

-f : file name from which you want to get users' tweets

-x : feature you want to extract (NOUN, VERB, NNP or all)

*example* python3 get_nltk_features.py -f uber_tweets -x all

