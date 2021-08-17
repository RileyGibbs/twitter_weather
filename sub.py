import requests

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory

from secrets import WEATHER_API_KEY


CHANNEL = "pubnub-twitter"
WEATHER_BASE_URL = "https://api.weatherapi.com/v1/current.json"
TEMPS_FILE = "temps_f.txt"
SLIDING_AVG_FILE = "sliding_avg_temps_f.txt"


class TwitterFeedCallback(SubscribeCallback):
    def __init__(self, num_tweets=5):
        self.num_tweets = num_tweets

    last_n_temps = []

    def calc_centroid(self, coords):
        num_coords = len(coords)
        # Point
        if num_coords == 1:
            return coords[0]
        # Polygon
        elif num_coords >= 0:
            centroid = [0, 0]  # [long, lat]
            for coord in coords:
                centroid[0] += coord[0]
                centroid[1] += coord[1]
            centroid[0] /= num_coords
            centroid[1] /= num_coords
            return centroid
        else:
            return None

    def message(self, pubnub, event):
        print("[TWEET received]")
        tweet_obj = event.message

        # Get coords/geo or centroid
        location = None  # [longitude, latitude]
        if "place" in tweet_obj:
            place_obj = tweet_obj["place"]
            bounding_box = place_obj["bounding_box"]
            centroid = self.calc_centroid(bounding_box["coordinates"][0])
            location = centroid

        # Get weather
        if location is not None:
            # NOTE: Location is [long, lat] and this api needs lat,long
            request_url = "{}?key={}&q={},{}&aqi=no".format(
                WEATHER_BASE_URL,
                WEATHER_API_KEY,
                location[1],
                location[0]
            )
            weather_data = requests.get(request_url)
            weather_obj = weather_data.json()
            current_temp = weather_obj["current"]["temp_f"]

            # Incorporate in sliding average
            self.last_n_temps.insert(0, current_temp)
            if len(self.last_n_temps) > self.num_tweets:
                self.last_n_temps.pop()
            sliding_avg = sum(self.last_n_temps) / len(self.last_n_temps)

            # Write to output files
            with open(SLIDING_AVG_FILE, "a+") as avg_file:
                avg_file.write("{}\n".format(sliding_avg))
                avg_file.close()
            with open(TEMPS_FILE, "a+") as temps_file:
                temps_file.write("{}\n".format(current_temp))
                temps_file.close()

    def status(self, pubnub, event):
        if event.category == PNStatusCategory.PNConnectedCategory:
            print("[STATUS: PNConnectedCategory]")
            print("Connected to channels: {}".format(event.affected_channels))
            print("*** CTRL-C to end subscriber ***")
