import getopt
import os
import sys

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from secrets import TWITTER_SUB_KEY
from sub import *


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hn:r")
    except getopt.GetoptError:
        print('run_twitter_weather.py -n <num_tweets> [-r,--remove_files]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run_twitter_weather.py -n <num_tweets> [-r,--remove_files]')
            sys.exit()
        elif opt in ("-n", "--num_tweets"):
            num_tweets = int(arg)
        elif opt in ("-r", "--remove_files"):
            if os.path.exists(SLIDING_AVG_FILE):
                os.remove(SLIDING_AVG_FILE)
            if os.path.exists(TEMPS_FILE):
                os.remove(TEMPS_FILE)

    if num_tweets is None or num_tweets <= 2 or num_tweets >= 100:
        print("** Number of tweets to average must be between 2 and 100")
        print('run_twitter_weather.py -n <num_tweets> [-r,--remove_files]')
        sys.exit(2)
    else:
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = TWITTER_SUB_KEY  # Twitter subscribe key
        pnconfig.uuid = "pubnub-twitterSUB"

        pubnub = PubNub(pnconfig)

        pubnub.add_listener(TwitterFeedCallback(num_tweets=num_tweets))
        pubnub.subscribe().channels(CHANNEL).execute()

        print("***************************************************")
        print("* Starting up Twitter-weather on channel...")
        print("***************************************************")


if __name__ == "__main__":
    main(sys.argv[1:])
