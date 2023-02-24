from urllib.request import urlopen
from notify_run import Notify
import re
from time import sleep
from argparse import ArgumentParser

DEFAULT_NUMBER_OF_MINUTES = 10


def notify_me(url, phrase_to_search='Closed sale', seconds_to_sleep=600):
    notify = Notify()
    data = (urlopen(url)).readlines()

    notify.send('Starting notification process. This is the first notification.')
    phrase_exists = False
    try:
        # A simple while, with an X minutes check.
        while not phrase_exists:
            phrase_exists = True
            for line in data:
                x = re.search(phrase_to_search, str(line))
                if x:
                    phrase_exists = False
                    break
            sleep(seconds_to_sleep)
            data = (urlopen(url)).readlines()
    finally:
        # If we got here, either the site changed
        # or something went wrong. Either way, should check url.
        notify.send('The site has changed! check it!')


def todia():
    args = parse_args()
    seconds_to_sleep = args.minutes * 60
    notify_me(args.url, phrase_to_search=args.phrase, seconds_to_sleep=seconds_to_sleep)


def parse_args():
    parser = ArgumentParser(
        prog='Todia',
        description='Todia is a tool for monitoring webpages and notifying changes made to them.')
    parser.add_argument('-p', '--phrase', required=True, type=str,
                        help='The phrase or tag to search for in the web page.')
    parser.add_argument('-u', '--url', required=True, type=str,
                        help='The web page to check if the phrase exists in.')
    parser.add_argument('-m', '--minutes', type=int, required=True, default=DEFAULT_NUMBER_OF_MINUTES,
                        help='The gap between web page checks (check every X minutes).')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    todia()
