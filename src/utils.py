import requests
import re
from requests.api import head
from .errors import SpaceNotFoundError
from .config import API_URL, API_KEY


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


def index_input(min=0, max=None):
    user_input = input()
    user_input_arr = re.split("(?:\s|,)", user_input)

    indexes = set()
    for x in user_input_arr:
        # Skip empty string
        if x.strip() == "":
            continue

        # Convert to integer
        index = int(x)

        # Check that the input index is within bounds
        if index < min:
            raise ValueError
        elif max is not None and index > max:
            raise ValueError

        indexes.add(index)

    return list(indexes)
