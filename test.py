import twitter, csv, sys, re
from pprint import pprint

api = twitter.Api(consumer_key='PRSM0lQIfJA7tCCIbn5nuHP1I',
    consumer_secret='aGy1w0MJHVJPS9x0SDQYLzSLO0CPZsgP5Bdtci0l7DKoyqZOpc',
    access_token_key='71156237-TdLIhLaQQuQDSjIr12gg9Rwf3yGQHC1ReTVqztvWO',
    access_token_secret='IRJUOTKAomEwWZzBfRGBt8TyeT2FzuHiUUOMKlNEpepBh'
    )

def gun_text(text):
    return re.search('gun', text)

def get_tweets(twitter_handles):
    data = {}
    
    for twitter_handle in twitter_handles:
        twitter_handle_tweets = []
        
        try:
            tweets = api.GetUserTimeline(screen_name = twitter_handle)
            
            for tweet in tweets:
                if not gun_text(tweet.text):
                    continue
                else:
                    print tweet.text
                    dct_tweet = {'id': tweet.id, 'text': tweet.text.encode('ascii', 'ignore'), 'link': 'https://twitter.com/{0}/status/{1}'.format(twitter_handle, tweet.id)}
                    twitter_handle_tweets.append(dct_tweet)
        except Exception, e:
            print e
            dct_tweet = {'id': 'ERROR', 'text': 'TWITTER HANDLE WRONG OR PRIVATE', 'link': 'https://twitter.com/{0}'.format(twitter_handle)}
            twitter_handle_tweets.append(dct_tweet)
        
        data[twitter_handle] = twitter_handle_tweets
    
    return data


## run script

in_file = csv.reader(open(sys.argv[1], 'r'))
in_file.next()
twitter_handles = [x[0] for x in in_file]

query = get_tweets(twitter_handles)

out_data = []
for twitter_handle in query:
    for tweet in query[twitter_handle]:
        row = [twitter_handle, tweet.get('text'), tweet.get('link')]
        out_data.append(row)

css = """
    <!doctype html>
    <head>
        <style>
            body {
                font-family: "Times New Roman";
                margin: 0.5in 0.5in;
            }
            
            ul {
                list-style: none;
            }
            
            li {
                margin: 2px;
            }
        </style>
    </head>
    """

content = '<body><ul>'

for twitter_handle in query:
    for tweet in query[twitter_handle]:
        content += '<li><a target="_blank" href="https://twitter.com/{0}">&#64;{0}</a>: {1} <a target="_blank" href="{2}">i</a></li>'.format(twitter_handle, tweet.get('text'), tweet.get('link'))

content += '</ul></body>'

out_file = open(sys.argv[1].replace('.csv', '_tweets.html'), 'w')
out_file.write(css + content)
out_file.close()