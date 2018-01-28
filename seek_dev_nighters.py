import requests
import pytz
import json
from datetime import datetime


def get_all_submissions():
    all_submissions = []
    url = 'https://devman.org/api/challenges/solution_attempts/'
    total_pages = requests.get(url,
                               params={'page': 1}).json()['number_of_pages']
    for page in range(1, total_pages+1):
        each_page = requests.get(url, params={'page': page}).json()['records']
        all_submissions.extend(each_page)
    return all_submissions


def get_midnighters(all_devman_submissions):
    midnighters = set()
    night_begin = datetime.strptime('00:00', '%H:%M').time()
    night_end = datetime.strptime('05:59', '%H:%M').time()
    for submission in all_devman_submissions:
        timezone = pytz.timezone(submission['timezone'])
        submission_time = datetime.fromtimestamp(submission['timestamp'])
        local_time = pytz.utc.localize(
                submission_time
                ).astimezone(timezone).time()
        if night_end > local_time > night_begin:
            midnighters.add(submission['username'])
    return midnighters


if __name__ == '__main__':
    delimiter = '-'*60
    all_devman_submissions = get_all_submissions()
    print(delimiter)
    print('There is the list of midnighters:\n')
    for midnighter in get_midnighters(all_devman_submissions):
        print(midnighter)
    print(delimiter)
