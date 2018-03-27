import requests
import pytz
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


def get_midnighters(all_devman_submissions):
    midnighters = set()
    night_begin = 0
    night_end = 6

    for submission in all_devman_submissions:
        timezone = pytz.timezone(submission['timezone'])
        submission_time = datetime.fromtimestamp(submission['timestamp'])
        local_time = pytz.utc.localize(
                submission_time
                ).astimezone(timezone).time().hour
        if night_end > local_time > night_begin:
            midnighters.add(submission['username'])
    return midnighters


if __name__ == '__main__':
    delimiter = '-'*60
    all_submission = get_all_attempts()
    print(delimiter)
    print('There is the list of midnighters:\n')
    for midnighter in get_midnighters(all_submission):
        print(midnighter)
    print(delimiter)
