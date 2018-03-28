import requests
from pytz import timezone
import json
from datetime import datetime


def get_all_attempts():
    url = 'https://devman.org/api/challenges/solution_attempts/'
    page = 1
    while True:
        response = requests.get(url, params={'page': page}).json()
        all_pages = response['number_of_pages']
        if page < all_pages:
            for attempt in response['records']:
                yield attempt
            page = page + 1
        else:
            break


def get_midnighters(all_devman_attempts):
    midnighters = set()
    night_begin = 0
    night_end = 6

    for attempt in all_devman_attempts:
        user_tzone = timezone(attempt['timezone'])
        attempt_time = datetime.fromtimestamp(
                attempt['timestamp'],user_tzone
                ).hour
        if night_end > attempt_time > night_begin:
            midnighters.add(attempt['username'])
    return midnighters


if __name__ == '__main__':
    delimiter = '-'*60
    all_attempts = get_all_attempts()
    print(delimiter)
    print('There is the list of midnighters:\n')
    for midnighter in get_midnighters(all_attempts):
        print(midnighter)
    print(delimiter)
