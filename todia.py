import argparse
import time
import urllib.request
from notify_run import Notify


def create_parser():
    parser = argparse.ArgumentParser(description="Check a URL for a phrase and notify if not found")
    parser.add_argument("-u", "--url", type=str, help="The URL to check")
    parser.add_argument("-p", "--phrase", type=str, help="The phrase to search for")
    parser.add_argument("-c", "--check-interval", type=int, default=600,
                        help="The interval (in seconds) to check the URL (default: 600)")

    return parser


def todia(url, phrase, check_interval):
    notify = Notify()
    try:
        notify.send("Starting service. First notification.")
        while True:
            # Make a request to the URL and get the page content
            with urllib.request.urlopen(url) as response:
                page_content = response.read().decode("utf-8")

            if phrase not in page_content:
                # If the phrase is not found, notify and exit
                notify.send("The phrase was not found on the page! The page has changed!")
                break

            # If the phrase is found, wait and check again
            time.sleep(check_interval)
    finally:
        notify.send("If no other notification was sent, "
                    "something went wrong. Process Stopped.")


def main():
    parser = create_parser()
    args = parser.parse_args()

    todia(args.url, args.phrase, args.check_interval)


if __name__ == '__main__':
    main()
