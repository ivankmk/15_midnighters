import requests
import pytz
import json
from datetime import datetime


def get_all_attempts():
    url = 'https://devman.org/api/challenges/solution_attempts/'
    total_pages = requests.get(url,
                               params={'page': 1}).json()['number_of_pages']
    for page in range(1, total_pages+1):
        yield requests.get(url, params={'page': page}).json()['records']


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


def get_unique_midnighters(all_submission):
    unique_midnighters = set()
    for a in get_all_attempts():
        for aa in get_midnighters(a):
            unique_midnighters.add(aa)
    return unique_midnighters

if __name__ == '__main__':
    delimiter = '-'*60
    all_submission = get_all_attempts()
    print(delimiter)
    print('There is the list of midnighters:\n')
    for midnighter in get_unique_midnighters(all_submission):
        print(midnighter)
    print(delimiter)
