import requests
import os
import mimetypes
import errno
import json
import sys
import math
from .storage import save_code, del_code, resolve_code
from .errors import MissingCodeError, SpaceNotFoundError
from .constants import API_KEY, API_URL
from .utils import get_files, does_exists
from .printer import p_ok, p_question, p_fail, p_head, p_sub


def destroy_space(code=None):
    p_head()
    code = resolve_code(code)
    headers = {"api-key": API_KEY}
    requests.delete(API_URL + "/spaces/" + code, headers=headers)
    del_code()
    p_ok("Done!")


def create_space():
    p_head()
    url = API_URL + "/spaces"
    headers = {"api-key": API_KEY}
    r = requests.post(url, headers=headers)
    data = r.json()
    code = data["space"]["code"]
    save_code(code)
    print("=" * 20)
    print(" " * 7 + code)
    print("=" * 20)
    print("")
    p_ok("Done!")
    p_sub(
        "The code has been saved and will be used for following commands. If you wish to override this code, you can do so via the --code flag."
    )


def list_files(code=None):
    p_head()
    try:
        code = resolve_code(code)
    except SpaceNotFoundError:
        p_fail("Space not found.")
    except MissingCodeError:
        p_fail("Missing code.")

    files = get_files(code)
    if files is None or len(files) == 0:
        print("There are no files.")
        p_ok("Done!")
        return
    for file in files:
        name = file["name"]
        key = file["key"]
        print(name, key)
    p_ok("Done!")


def remove_files(code=None):
    p_head()

    try:
        code = resolve_code(code)
    except SpaceNotFoundError:
        p_fail("Space not found.")
    except MissingCodeError:
        p_fail("Missing code.")

    files = get_files(code)
    p_question("Which files(s) would you like to remove?")
    for index, file in enumerate(files):
        complete_file_name = file["name"] + file["ext"]
        print(
            "({index}) {complete_file_name}".format(
                index=index, complete_file_name=complete_file_name
            )
        )

    selected_ids = input()
    selected_ids = selected_ids.split(" ")
    selected_keys = map(lambda id: files[int(id)]["key"], selected_ids)
    to_remove = []
    for selected_key in selected_keys:
        to_remove.append(selected_key)
    to_remove = json.dumps(to_remove)
    headers = {"api-key": API_KEY}
    params = {"toRemove": to_remove}
    requests.delete(
        API_URL + "/spaces/" + code + "/files", headers=headers, params=params
    )
    p_ok("Done!")


def download_files(path=None, code=None):
    p_head()
    try:
        code = resolve_code(code)
    except SpaceNotFoundError:
        p_fail("Space not found.")
    except MissingCodeError:
        p_fail("Missing code.")

    files = get_files(code)
    p_question("Which file would you like to download?")
    for index, file in enumerate(files):
        print("({index}) {file_name} ".format(index=index, file_name=file["name"]))

    selected_ids = input()

    selected_ids = selected_ids.split(" ")
    selected_files = map(lambda id: files[int(id)], selected_ids)
    for selected_file in selected_files:
        print(selected_file)
        r = requests.get(selected_file["signedUrl"])
        complete_file_name = selected_file["name"] + selected_file["ext"]

        if path is not None:
            file_path = os.path.join(path, complete_file_name)
            if not os.path.exists(os.path.dirname(file_path)):
                try:
                    os.makedirs(os.path.dirname(file_path))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
        else:
            file_path = complete_file_name

        open(file_path, "wb").write(r.content)
    p_ok("Done!")


def upload_files(path, code=None):
    p_head()
    try:
        code = resolve_code(code)
    except SpaceNotFoundError:
        p_fail("Space not found.")
    except MissingCodeError:
        p_fail("Missing code.")

    if not does_exists(code):
        p_fail("The space does not exist.")
        return

    file_paths = []

    if os.path.isfile(path):
        file_paths.append(path)
    else:
        p_question("Which files do you want to upload?")

        for index, file_path in enumerate(os.listdir(path)):
            print("({index}) {file_path}".format(index=index, file_path=file_path))

        selected_ids = input()
        selected_ids = selected_ids.split(" ")
        selected_ids = set(selected_ids)

        selected_file_paths = map(lambda id: os.listdir(path)[int(id)], selected_ids)
        for selected_file_path in selected_file_paths:
            file_paths.append(os.path.join(path, selected_file_path))

    total = len(file_paths)
    for index, file_path in enumerate(file_paths):

        sys.stdout.write("\r")
        sys.stdout.write(
            "[%-30s] %d%%"
            % ("=" * math.floor(index / total * 30), (index / total) * 100)
        )
        sys.stdout.flush()
        upload_file(code, file_path)

    sys.stdout.write("\r")
    sys.stdout.write("[%-30s] %d%%" % ("=" * 30, 100))

    sys.stdout.write("\n")
    p_ok("Done!")


def upload_file(code, path):
    file_size = os.stat(path).st_size
    complete_file_name = path.split("/")[-1]
    file_ext = "." + complete_file_name.split(".")[-1]
    file_name = complete_file_name.split(".")[0]
    file_type = mimetypes.guess_type(path)[0]

    with open(path, "rb") as f:

        url = API_URL + "/signed-urls"
        headers = {"api-key": API_KEY}
        data = {"code": code, "file": {"size": file_size}}
        response = requests.post(
            url,
            json=data,
            headers=headers,
        ).json()
        signed_url = response["signedUrl"]
        key = response["key"]

        response = requests.put(
            signed_url,
            headers={"Content-type": "application/x-www-form-urlencoded"},
            data=f,
        )
        if not (response.status_code == 200):
            print("Error uploading file to AWS")

        data = {
            "size": file_size,
            "name": file_name,
            "type": file_type,
            "ext": file_ext,
            "key": key,
        }
        response = requests.patch(
            API_URL + "/spaces/" + code + "/files",
            headers={"api-key": API_KEY},
            data=data,
        )

        f.close()
