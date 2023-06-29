# Import modules & libraries
import requests
import json
import sys
import os

from termcolor import colored


class Saver:
    def __init__(self, output_path):
        # Check if output path exists
        if os.path.exists(output_path):
            print(colored(
                f'[-] Error: {output_path} already exists. Please delete it and try again.', 'red'))
            exit(1)

        # Create output file
        open(output_path, 'w').close()

        self.output_path = output_path

    def save(self, data):
        with open(self.output_path, 'w') as f:
            json.dump(data, f)

    def load(self):
        with open(self.output_path, 'r') as f:
            return json.load(f)


# Load config file
try:
    config = json.load(open('config.json'))
except FileNotFoundError:
    print(colored('[-] Error: Config file not found', 'red'))
    exit(1)

KEYWORDS = config['keywords']
OUTPUT_PATH = config['output_path']
MAPS_API_KEY = None


MIN_REVIEWS = config['min_reviews']
MAX_reviews = config['max_reviews']
MIN_RATING = config['min_rating']
MAX_RATING = config['max_rating']


def check_reqs():
    # Check if all required modules are installed
    try:
        import requests
        import json
        from termcolor import colored

    except ImportError:
        print(colored(
            '[-] Error: Missing required modules. Please install them using pip3 install -r requirements.txt', 'red'))
        exit(1)

    try:
        MAPS_API_KEY = config['maps_api_key']
    except KeyError:
        try:
            MAPS_API_KEY = sys.argv[1]
        except IndexError:
            print(colored(
                '[-] Error: Missing Google Maps API key. Please provide it as an argument or in config.json', 'red'))
            exit(1)


def get_listings():
    # Get listings (places) from Google Maps using keywords
    listings = []
    # Create a sentence from keywords
    keyword_sentence = ''
    for keyword in KEYWORDS:
        keyword_sentence += keyword + ' '
    url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={keyword_sentence}&key={MAPS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    for place in data['results']:
        print(colored(f'[+] Found {place["name"]}', 'green'))
        listings.append(place)
    return listings


def filter_listings(listings):
    # Filter listings based on min/max reviews and min/max rating
    filtered_listings = []
    for listing in listings:
        if MIN_REVIEWS <= listing['user_ratings_total'] <= MAX_reviews:
            if MIN_RATING <= listing['rating'] <= MAX_RATING:
                filtered_listings.append(listing)
    return filtered_listings


if __name__ == '__main__':
    logoBanner = open('./assets/logo-banner.txt', 'r')
    print(colored(logoBanner.read(), 'blue'))
    check_reqs()
    listings = get_listings()
    filtered_listings = filter_listings(listings)
    saver = Saver(OUTPUT_PATH)
    saver.save(filtered_listings)
    print(colored('[+] Done!', 'green'))
    print(
        colored(f'[+] Saved {len(filtered_listings)} place ids to {OUTPUT_PATH}', 'green'))

'''
This code is licensed under the MIT License. (See LICENSE for details)^
@author: Sami Hindi
@last_updated: 2023-29-06
@description: A Google Maps scraper that scrapes Google Maps for places based on keywords and filters them based on min/max reviews and min/max rating.
'''
