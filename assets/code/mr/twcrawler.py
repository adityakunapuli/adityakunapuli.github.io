import sys
import sqlite3
import datetime
import re
import json
import tweepy
import time
from urllib3.exceptions import ProtocolError


start_time = time.time()

class StreamListener(tweepy.StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        try:
            all_attributes = ''
            for attributes in all_data:
                all_attributes += attributes + ' | '
            if 'extended_tweet' in all_data:
                all_attributes += ' ||| '
                for attributes in all_data['extended_tweet']:
                    all_attributes += attributes + ' | '

            if 'extended_tweet' in all_data:
                raw_tweet_text = all_data['extended_tweet']['full_text']
            else:
                raw_tweet_text = all_data['text']

            if not (not (not 'RT' in all_data['text'][0:3]) or not (all_data['user']['lang'] == 'en') or not (
                    all_data['lang'] == 'en')):

                tweet_text = re.sub('(@[A-Za-z0-9_]+)|'#......................Usernames
                                    '(#[0-9A-Za-z]+)|'#.......................Hashtags/topics
                                    '[^\x00-\x7F]|'#..........................Emojis
                                    'http[s]?\:\/\/.[a-zA-Z0-9\.\/\-]+'#......URLs
                                    , ' ', raw_tweet_text)
                tweet_text = re.sub('([^0-9A-Za-z \t])', '', tweet_text)#.....Non-alphabet characters
                tweet_text = tweet_text.strip()

                # check if geolocation is available
                coordinates = ''
                if(all_data['geo'] != None):
                    coordinates = all_data['geo']['coordinates']
                    coordinates = ','.join(map(str, coordinates ))
                    print(coordinates)

                created_at           = all_data['created_at']
                favorite_count       = all_data['favorite_count']
                favorited            = all_data['favorited']
                filter_level         = all_data['filter_level']
                lang                 = all_data['retweeted']
                retweet_count        = all_data['retweet_count']
                retweeted            = all_data['retweeted']
                source               = all_data['source']
                text                 = tweet_text
                rawtext              = raw_tweet_text
                user_created_at      = all_data['user']['created_at']
                user_followers_count = all_data['user']['followers_count']
                user_location        = all_data['user']['location']
                user_lang            = all_data['user']['lang']
                user_name            = all_data['user']['name']
                user_screen_name     = all_data['user']['screen_name']
                user_time_zone       = all_data['user']['time_zone']
                user_utc_offset      = all_data['user']['utc_offset']
                user_friends_count   = all_data['user']['friends_count']
                id_str = all_data['id_str']
                URL = 'https://twitter.com/statuses/' + all_data['id_str']
                # Append file-type if necessary
                if '.db' not in sys.argv[2]:
                    dbName = sys.argv[2]+'.db'
                else:
                    dbName = sys.argv[2]

                conn = sqlite3.connect(dbName)
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS tweets (created_at TEXT,
                favorite_count TEXT,
                favorited TEXT,
                filter_level TEXT,
                lang TEXT,
                retweet_count TEXT,
                retweeted TEXT,
                source TEXT,
                text TEXT,
                rawtext TEXT,
                user_created_at TEXT,
                user_followers_count TEXT,
                user_location TEXT,
                user_lang TEXT,
                user_name TEXT,
                user_screen_name TEXT,
                user_time_zone TEXT,
                user_utc_offset TEXT,
                user_friends_count TEXT,
                geolocation TEXT,
                id_str TEXT PRIMARY KEY,
                URL TEXT,
                recordRetrieved TEXT) ''')
                conn.commit()

                c.execute('''
                INSERT INTO tweets
                (created_at,
                favorite_count,
                favorited,
                filter_level,
                lang,
                retweet_count,
                retweeted,
                source,
                text,
                rawtext,
                user_created_at,
                user_followers_count,
                user_location,
                user_lang,
                user_name,
                user_screen_name,
                user_time_zone,
                user_utc_offset,
                user_friends_count,
                geolocation,
                id_str,
                URL,
                recordRetrieved)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (created_at,
                favorite_count,
                favorited,
                filter_level,
                lang,
                retweet_count,
                retweeted,
                source,
                text,
                rawtext,
                user_created_at,
                user_followers_count,
                user_location,
                user_lang,
                user_name,
                user_screen_name,
                user_time_zone,
                user_utc_offset,
                user_friends_count,
                coordinates,
                id_str,
                URL,
                str(datetime.datetime.now()) ) )
                conn.commit()
                conn.close()
                print('Success')
        except Exception as e:
            print('Error: ' + str(e))
            # print(all_data)


def main():
    print(sys.argv[1])
    print("tags: " + str(sys.argv[1].split(':')))
    print("output location: " + sys.argv[2])
    consumer_key        = 'ZZZZZZZZZZZ'
    consumer_secret     = 'ZZZZZZZZZZZ'
    access_token        = 'ZZZZZZZZZZZ'
    access_token_secret = 'ZZZZZZZZZZZ'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth,  wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    myStreamListener = StreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener, tweet_mode='extended')
    # NOTE: Can't use both keyword & location filter at same time
    # myStream.filter(track=['Donald Trump', 'Trump', 'Whitehouse'])
    # myStream.filter(follow=None, locations=[-122.75,36.8,-121.75,37.8]) # SF
    myStream.filter(follow=None, locations=[-129.85,18.04,-60.94,56.5]) # US
    # myStream.filter(follow=None, locations=[-167.6,-47.1,179.4,69.2]) # World
    while True: # bypass urllib3.exceptions IncompleteRead

        try:
            myStream.filter(track=sys.argv[1].split(':'))
        except ProtocolError as e:
            print(e)
            continue
        except Exception as e:
            print(e)



if __name__ == "__main__":
    main()
    print('--- %s seconds ---' % round(time.time() - start_time))
