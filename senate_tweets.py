import sys, csv, json, functools
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener

consumer_key='PRSM0lQIfJA7tCCIbn5nuHP1I'
consumer_secret='aGy1w0MJHVJPS9x0SDQYLzSLO0CPZsgP5Bdtci0l7DKoyqZOpc'
access_token='71156237-TdLIhLaQQuQDSjIr12gg9Rwf3yGQHC1ReTVqztvWO'
access_secret='IRJUOTKAomEwWZzBfRGBt8TyeT2FzuHiUUOMKlNEpepBh'

class Listener(StreamListener):
    
    def on_data(self, data):
        status = json.loads(data)
        user, tweet, tweet_id = (status.get('user').get('screen_name'), status.get('text').encode('ascii', 'ignore'), str(status.get('id')))
        
        print user, tweet
        
        file = csv.writer(open('senate_results.csv', 'a'))
        file.writerow([tweet_id, user, tweet])
        
        return True
        
    def on_error(status):
        print status
        return False


def dpr_user_id(screen_name, auth):
    try:
        id = str(tweepy.API(auth).get_user(screen_name = screen_name).id)
    except Exception, e:
        print e
        id = None
        
    return id

def dpr_user_ids(screen_names, auth):
    return filter(lambda x: x is not None, map(functools.partial(user_id, auth = auth), screen_names))

def user_ids(screen_names, auth):
    api = tweepy.API(auth)
    return [str(x.id) for x in api.lookup_users(screen_names = screen_names)]

def stream_users(in_file, auth):    
    screen_names = [x.strip() for x in in_file]
    
    tw_list = user_ids(screen_names, auth)
    
    twitterStream = Stream(auth, Listener())
    twitterStream.filter(follow=tw_list)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

stream_users(open('senate_twitters.csv', 'r'), auth)




