import requests
from datetime import timedelta, datetime
from .errors import SpaceNotFoundError
from .constants import API_KEY, API_URL


def is_expired(created_at):
    expires_at = created_at + timedelta(hours=12)
    now = datetime.now()
    # print("Now: ", now)
    # print("Created At: ", created_at)
    # print("Expires At: ", expires_at)
    # print("Diff: ", expires_at - now)
    # print(timedelta(seconds=12))
    return expires_at - now < timedelta(seconds=0)


def does_exists(code):
    headers = {"api-key": API_KEY}
    response = requests.get(API_URL + "/spaces/" + code, headers=headers)
    if response.status_code == 404:
        return False
    return True


def get_files(code):
    headers = {"api-key": API_KEY}
    response = requests.get(API_URL + "/spaces/" + code, headers=headers)
    if response.status_code == 404:
        raise SpaceNotFoundError

    response = response.json()

    space = response["space"]
    files = space["files"]
    return files
