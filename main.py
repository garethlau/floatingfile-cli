from posix import listdir
import fire
import requests
import os
import mimetypes
import errno
import json
import sys
import math

API_URL = "https://developer.floatingfile.space/api/v5"
API_KEY = "secretcat"


class SpaceNotFoundError(Exception):
    pass


def does_exists(code):
    headers = {"api-key": API_KEY}
    response = requests.get(API_URL + "/spaces/" + code, headers=headers)
    if response.status_code == 404:
        return False
    return True


def get_files(code):
    code = code.upper()
    headers = {"api-key": API_KEY}
    response = requests.get(API_URL + "/spaces/" + code, headers=headers)
    if response.status_code == 404:
        raise SpaceNotFoundError

    response = response.json()

    space = response["space"]
    files = space["files"]
    return files


def destroy_space(code):
    code = code.upper()
    headers = {"api-key": API_KEY}
    requests.delete(API_URL + "/spaces/" + code, headers=headers)
    print("Space deleted.")


def create_space():
    url = API_URL + "/spaces"
    headers = {"api-key": API_KEY}
    r = requests.post(url, headers=headers)
    data = r.json()
    code = data["space"]["code"]
    print("Created a new space: " + code)


def list_files(code):
    code = code.upper()
    try:
        files = get_files(code)
        if files is None:
            return
        for file in files:
            name = file["name"]
            key = file["key"]
            print(name, key)
    except SpaceNotFoundError:
        print("Space not found.")


def remove_files(code):
    code = code.upper()
    files = get_files(code)
    print("Which files(s) would you like to remove?")
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

    print("Files successfully removed. The remaining files are: ")
    files = get_files(code)
    for file in files:
        complete_file_name = file["name"] + file["ext"]
        print(complete_file_name)


def download_files(code, path):
    code = code.upper()
    files = get_files(code)
    print("Which file would you like to download?")
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


def upload_files(code, path):
    code = code.upper()
    if not does_exists(code):
        print("The space does not exist.")
        return

    file_paths = []
    if os.path.isfile(path):
        file_paths.append(path)
    else:
        print("Which files do you want to upload?")

        for index, file_path in enumerate(os.listdir(path)):
            print("({index}) {file_path}".format(index=index, file_path=file_path))

        selected_ids = input()
        selected_ids = selected_ids.split(" ")
        selected_ids = set(selected_ids)

        selected_file_paths = map(lambda id: os.listdir(path)[int(id)], selected_ids)
        for selected_file_path in selected_file_paths:
            file_paths.append(os.path.join(path, selected_file_path))
    print(file_paths)

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
    print("Done!")


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


if __name__ == "__main__":
    fire.Fire(
        {
            "create": create_space,
            "destroy": destroy_space,
            "list": list_files,
            "remove": remove_files,
            "download": download_files,
            "upload": upload_files,
        }
    )
