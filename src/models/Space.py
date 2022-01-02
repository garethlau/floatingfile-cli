import requests
import os
import json
import mimetypes
from ..errors import SpaceNotFoundError, MaxCapacityReached
from ..config import API_URL, BASE_HEADERS
from ..utils import best_effort_file_type
from ..services.username import get_username


class Space:
    def create():
        url = API_URL + "/spaces"
        r = requests.post(url, headers=BASE_HEADERS)
        d = r.json()
        return d["space"]

    def find(code):
        url = f"{API_URL}/spaces/{code}"
        r = requests.get(url, headers=BASE_HEADERS)
        if r.status_code == 404:
            raise SpaceNotFoundError
        d = r.json()
        return d["space"]

    def get_files(code):
        space = Space.find(code)
        return space["files"]

    def remove_files(code, keys):
        params = {"toRemove": json.dumps(keys)}
        headers = BASE_HEADERS
        headers["username"] = get_username()
        url = f"{API_URL}/spaces/{code}/files"
        requests.delete(url, headers=headers, params=params)

    def is_alive(code):
        try:
            Space.find(code)
            return True
        except SpaceNotFoundError:
            return False

    def upload_file(code, path):
        file_size = os.stat(path).st_size
        complete_file_name = path.split("/")[-1]
        file_ext = complete_file_name.split(".")[-1]
        file_type = mimetypes.guess_type(path, strict=False)[0]
        if file_type is None:
            # https://github.com/python/cpython/blob/3.10/Lib/mimetypes.py
            # Unable to guess the mimetype, could be a non-standard ext
            # For file extensions that we know about, let's make our best attempt to fill in the file_type data
            file_type = best_effort_file_type(file_ext)

        url = f"{API_URL}/signed-urls"
        data = {"code": code, "file": {"size": file_size}}
        headers = BASE_HEADERS
        headers["username"] = get_username()

        # Generate signed url for direct upload
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 403:
            raise MaxCapacityReached

        response = response.json()
        signed_url = response["signedUrl"]
        key = response["key"]

        # Upload the file to S3
        with open(path, "rb") as f:
            response = requests.put(
                signed_url,
                headers={"Content-type": "application/x-www-form-urlencoded"},
                data=f,
            )
            if not (response.status_code == 200):
                print("Error uploading file to AWS")

            f.close()

        url = f"{API_URL}/spaces/{code}/files"
        headers = BASE_HEADERS
        headers["username"] = get_username()
        data = {
            "size": file_size,
            "name": complete_file_name,
            "type": file_type,
            "ext": file_ext,
            "key": key,
        }
        response = requests.patch(
            url,
            headers=headers,
            data=data,
        )

    def delete(code):
        url = API_URL + "/spaces/" + code
        requests.delete(url, headers=BASE_HEADERS)
        return
