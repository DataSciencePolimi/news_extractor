import tweepy
import json
import sys
from langdetect import detect
import csv
import sys
import getopt

#login to twitter you must have a file called credentialsTwitter.json with your consumer_key, consumer_secret, access_token, access_token_secret
def login():
    fileKeys = open('credentialsTwitter.json').read()
    
    keys = json.loads(fileKeys)
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    twitter = tweepy.API(auth, wait_on_rate_limit=True)
    return twitter


def get_tweets(twitter, account, N, start_date=None, end_date=None):
    max_number = 3200
    max_per_request = 200
    languages = ("de", "en", "es", "fr", "it", "pt")
    user_tweets = []
    if (N>max_number):
        N = max_number
        iteration = 16
        last = 0
    else:
        iteration, last = divmod(N, max_per_request)
    user_timeline = twitter.user_timeline(screen_name =account, count=1, include_rts=False, tweet_mode="extended")
    if (user_timeline):
        for i in range(iteration+1):
            lastTweetId = int(user_timeline[-1].id_str)
            user_timeline = twitter.user_timeline(screen_name = account, max_id = lastTweetId, count = max_per_request, include_rts=False, tweet_mode="extended")
            for tweets in user_timeline:
                if (tweets.lang == None):
                    tweets.lang = detect(tweets.text.replace("\n", " "))
                if (tweets.lang in languages):
                    d = {'id_user': tweets.user.id_str, 'screen_name': tweets.user.screen_name.lower(), 'text': tweets.full_text, 'lang':tweets.lang, 'favourite_count': tweets.favorite_count, 'retweet_count': tweets.retweet_count, 'create_at': tweets.created_at.strftime("%Y-%m-%d %H:%M:%S"), 'mentions': tweets.entities['user_mentions'], '_id':tweets.id_str, 'coordinates':tweets.coordinates}
                    user_tweets.append(d)
            if i != iteration:
                user_tweets = user_tweets[:len(user_tweets)-1]
            if len(user_timeline)<max_per_request:
                break
    else:
        print('no tweets')
    print(account, len(user_tweets))

    return user_tweets[:N]

def get_tweets_from_users(file_users, twitter):
    users = csv.reader(open(file_users,'r'))
    all_tweets = {}
    for u in users:
        all_tweets[u[0]] = get_tweets(twitter, u[0], 200)
    return all_tweets


def save_tweets(all_tweets, file_out_name):
    j = json.dumps(all_tweets)
    file = open(file_out_name,'w')
    file.write(j)

def main():
    try:
        twitter = login()
    except:
        print('no login twitter')
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'f:o:')
    except getopt.GetoptError as err:
        # print help information and exit:
        print('err')  # will print something like "option -a not recognized"
        #        usage()
        sys.exit(2)
    file_users = None
    file_out_name = None
    for o, a in opts:
        if o == "-f":
            file_users = a
        elif o == "-o":
            file_out_name = a
    all_tweets = get_tweets_from_users(file_users, twitter)
    save_tweets(all_tweets, file_out_name)


if __name__ == "__main__":
    main()

