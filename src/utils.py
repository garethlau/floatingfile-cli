import requests
from requests.api import head
from .errors import SpaceNotFoundError
from .constants import API_KEY, API_URL


def get_space(code):
    headers = {"api-key": API_KEY}
    response = requests.get(API_URL + "/spaces/" + code, headers=headers)
    if response.status_code == 404:
        raise SpaceNotFoundError

    response = response.json()
    return response["space"]


def does_exists(code):
    try:
        get_space(code)
        return True
    except SpaceNotFoundError:
        return False


def get_files(code):
    space = get_space(code)
    files = space["files"]
    return files
