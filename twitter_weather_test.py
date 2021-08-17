import getopt
import sys

from sub import SLIDING_AVG_FILE, TEMPS_FILE


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hn:r")
    except getopt.GetoptError:
        print('run_twitter_weather_test.py -n <num_tweets>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run_twitter_weather.py -n <num_tweets>')
            sys.exit()
        elif opt in ("-n", "--num_tweets"):
            num_tweets = int(arg)

    if num_tweets <= 2 or num_tweets >= 100:
        print("** Number of tweets to average must be between 2 and 100")
        sys.exit(2)

    last_n_temps = []
    sliding_avg = 0
    with open(SLIDING_AVG_FILE, "r") as sliding_avg_file:
        with open(TEMPS_FILE, "r") as temps_file:
            sliding_averages = sliding_avg_file.readlines()
            for i, temp in enumerate(temps_file.readlines()):
                last_n_temps.insert(0, float(temp))
                if len(last_n_temps) > num_tweets:
                    last_n_temps.pop()
                sliding_avg = sum(last_n_temps) / len(last_n_temps)
                try:
                    assert sliding_avg == float(sliding_averages[i].strip())
                except AssertionError as e:
                    print("**************")
                    print("Sliding avg is {}, expected to be {}"
                          .format(sliding_avg,
                                  float(sliding_averages[i].strip())))
                    print("Last {} temps".format(num_tweets))
                    print("{}".format(last_n_temps))
                    print("**************")
                    raise e

    print("Tests passed.")


if __name__ == "__main__":
    main(sys.argv[1:])
