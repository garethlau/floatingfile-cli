import requests
import os
import mimetypes
import errno
import json
import sys
import re
import math
from .storage import save_code, del_code, resolve_code, get_codes
from .errors import MissingCodeError, SpaceNotFoundError
from .utils import get_files, does_exists, index_input
from .printer import p_ok, p_question, p_fail, p_head, p_sub
from .config import API_URL, BASE_HEADERS


def destroy_space(code=None):
    """
    Destroys a space.
    :param code: Code of the space to be destroyed. If no code is provided, an attempt will be made to use the code saved in memory.
    """
    p_head()
    try:
        code = resolve_code(code)
    except SpaceNotFoundError:
        p_fail("Space not found.")
        return
    except MissingCodeError:
        p_fail("Missing required param: code.")
        return

    requests.delete(API_URL + "/spaces/" + code, headers=BASE_HEADERS)
    del_code(code)
    # TODO: If the deleted code was the default code, notify the user of the new default
    p_ok("Done!")


def create_space():
    """
    Create a space. This will overwrite the code saved in memory.
    """
    p_head()
    url = API_URL + "/spaces"
    r = requests.post(url, headers=BASE_HEADERS)
    data = r.json()
    code = data["space"]["code"]
    save_code(code)
    print("Your newly created space can be accessed here:")
    print("https://app.floatingfile.space/s/{code}".format(code=code))
    print("")
    p_sub(
        "The code has been saved and will be used for following commands. If you wish to override this code, you can do so via the --code flag."
    )


def list_files(code=None):
    """
    List all the files in the space.
    :param code: Code of the space to view the files of. If no code is provided, an attempt will be made to use the code saved in memory.
    """
    p_head()
    try:
        code = resolve_code(code)
    except SpaceNotFoundError:
        p_fail("Space not found.")
        return
    except MissingCodeError:
        p_fail("Missing required param: code.")
        return

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
    """
    Interactively remove files from a space.
    :param code: Code of the space to remove files from. If no code is provided, an attempt will be made to use the code saved in memory.
    """
    p_head()

    try:
        code = resolve_code(code)
    except SpaceNotFoundError:
        p_fail("Space not found.")
        return
    except MissingCodeError:
        p_fail("Missing required param: code.")
        return

    files = get_files(code)
    p_question("Which files(s) would you like to remove?")
    for index, file in enumerate(files):
        complete_file_name = file["name"] + file["ext"]
        print(
            "({index}) {complete_file_name}".format(
                index=index, complete_file_name=complete_file_name
            )
        )

    try:
        indexes = index_input(min=0, max=len(files))
    except ValueError:
        p_fail("Invalid input value detected.")
        return
    keys = list(map(lambda index: files[index]["key"], indexes))
    params = {"toRemove": json.dumps(keys)}
    requests.delete(
        API_URL + "/spaces/" + code + "/files", headers=BASE_HEADERS, params=params
    )
    p_ok("Done!")


def download_files(path=None, code=None):
    """
    Download files from a space.
    :param path: Path of directory to download files into. If no path is provided, the files will be downloaded into the current working directory.
    :param code: Code of the space to download files from. If no code is provided, an attempt will be made to use the code saved in memory.
    """
    p_head()
    try:
        code = resolve_code(code)
    except SpaceNotFoundError:
        p_fail("Space not found.")
        return
    except MissingCodeError:
        p_fail("Missing required param: code.")
        return

    files = get_files(code)
    p_question("Which file would you like to download?")
    for index, file in enumerate(files):
        print("({index}) {file_name} ".format(index=index, file_name=file["name"]))

    try:
        indexes = index_input(min=0, max=len(files))
    except ValueError:
        p_fail("Invalid input value detected.")
        return

    selected_files = map(lambda index: files[index], indexes)

    total = len(indexes)
    for index, selected_file in enumerate(selected_files):
        sys.stdout.write("\r")
        sys.stdout.write(
            "[%-30s] %d%%"
            % ("=" * math.floor(index / total * 30), (index / total) * 100)
        )
        sys.stdout.flush()
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

    sys.stdout.write("\r")
    sys.stdout.write("[%-30s] %d%%" % ("=" * 30, 100))
    sys.stdout.write("\n")
    p_ok("Done!")


def upload_files(path, code=None):
    """
    Upload files to a space.
    :param path: Path to file or directory. If the path provided is a directory, then an interactive prompt will be displayed to select which files in the directory are to be uploaded. If the path is a file, then the file will be uploaded.
    :param code: Code of the space to upload files to. If no code is provided, an attempt will be made to use the code saved in memory.
    """
    p_head()
    try:
        code = resolve_code(code)
    except SpaceNotFoundError:
        p_fail("Space not found.")
        return
    except MissingCodeError:
        p_fail("Missing required param: code.")
        return

    file_paths = []

    if os.path.isfile(path):
        file_paths.append(path)
    else:
        p_question("Which files do you want to upload?")

        for index, file_path in enumerate(os.listdir(path)):
            print("({index}) {file_path}".format(index=index, file_path=file_path))

        try:
            indexes = index_input(min=0, max=len(os.listdir(path)))
        except ValueError:
            p_fail("Invalid input value detected.")
            return

        selected_file_paths = map(lambda index: os.listdir(path)[index], indexes)
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
        data = {"code": code, "file": {"size": file_size}}
        response = requests.post(
            url,
            json=data,
            headers=BASE_HEADERS,
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
            headers=BASE_HEADERS,
            data=data,
        )

        f.close()


def spaces():
    """
    List recently accessed spaces.
    """
    p_head()
    codes = get_codes()
    for index, code in enumerate(codes):
        if index == 0:
            p_ok("(default) {code}".format(index=index, code=code))
        else:
            print("({index}) {code}".format(index=index, code=code))
