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



#list of users who post the news
def get_users_from_news(news, twitter, N=None):
    users = []
    
    for status in tweepy.Cursor(twitter.search,news).items():
        if N != None and len(users) > N:
            break
        users.append(status.user.screen_name)
    return users

def save_users(users, news, name_file):
    file = csv.writer(open(name_file+'.csv','w'))
    for user in users:
        file.writerow([user])


def main():
    try:
        twitter = login()
    except:
        print('no login twitter')

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'n:x:f:')
    except getopt.GetoptError as err:
        # print help information and exit:
        print('err')  # will print something like "option -a not recognized"
        #        usage()
        sys.exit(2)
    N = None
    news = None
    name_file = None
    for o, a in opts:
        if o == "-n":
            N = int(a)
        elif o == "-x":
            news = a
        elif o == "-f":
            name_file = a
    users = get_users_from_news(news, twitter, N)

    save_users(users, news, name_file)

if __name__ == "__main__":
    main()
