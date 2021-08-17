# Twitter Weather App 

The Twitter Weather App averages the weather from the last N number of geotagged tweets.

## Get keys

You will need a subscribe key for pubnub-twitter along with a WeatherAPI key to authenticate your app. Get your keys from the [PubNub Twitter Stream Page](https://www.pubnub.com/developers/realtime-data-streams/twitter-stream) and your [WeatherAPI Account](https://www.weatherapi.com/login.aspx) respectively.

## Set up the project

If you don't want to copy the code from this document, you can clone the repository and use the files in there.
   
1. run `pip install -r requirements.txt`

2. Create a file named `secrets.py` and set the following constants:

    ```text
    TWITTER_SUB_KEY = "<pubnub-twitter-key"
    WEATHER_API_KEY = "<your_weather_api_key>"
    ```

### Note: Don't add `secrets.py` to your git repo!

## Run Twitter Weather

You first need to start the subcribe process to see the updates you want to publish.

1. Open the terminal and run the script with `python3 run_twitter_weather.py -n <number_of_tweets_to_average_over> [-r,--remove_files]`. 

    This will start logging temperatures and the sliding average temperatures in `temps.txt` and `sliding_avg_temps_f.txt`, respectively (in fahrenheit). 

    `-r` or `--remove_files` removes these log files before running. You can also run `python3 run_twitter_weather.py -h` for help.

    Once started, you should see a message that the script has connected to `pubnub-twitter` and begins to receive tweet messages

2. When you're finished, press `Control-C` to exit the script.

3. To test whether the script has run properly, run `python3 twitter_weather_test.py -n <SAME_NUMBER_OF_TWEETS_AS_RUN>` without deleting the log files.

    You should see `Tests passed.` for a successful test run.

    Sample data has been included in this repo for n=10 Tweets to average over.

## Documentation

* [WeatherAPI reference](https://www.pubnub.com/docs/platform/quickstarts/python)
* [PubNub API reference for Python](https://www.weatherapi.com/docs)

## Support

If you **need help** or have a **general question**, contact rjwgibbs@gmail.com.
