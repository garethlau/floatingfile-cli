import requests
from .errors import SpaceNotFoundError
from .constants import API_KEY, API_URL


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
