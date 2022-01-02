import requests
import os
import mimetypes
import errno
import json
from .storage import save_code, del_code, resolve_code, get_codes, set_codes
from .errors import MissingCodeError, SpaceNotFoundError, MaxCapacityReached
from .utils import best_effort_file_type, get_files, index_input
from .printer import p_ok, p_question, p_fail, p_head, p_sub, p_info
from .config import API_URL, BASE_HEADERS
from .progress import progress_bar

cols, rows = os.get_terminal_size()


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


def remove_files(code=None, a=False):
    """
    Interactively remove files from a space.
    :param code: Code of the space to remove files from. If no code is provided, an attempt will be made to use the code saved in memory.
    :param a: Removes all files from the space.
    """
    p_head()

    remove_all = a

    try:
        code = resolve_code(code)
    except SpaceNotFoundError:
        p_fail("Space not found.")
        return
    except MissingCodeError:
        p_fail("Missing required param: code.")
        return

    files = get_files(code)

    if remove_all:
        p_info("Removing all files")
        keys = list(map(lambda file: file["key"], files))
    else:
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


def download_files(path=None, code=None, a=False):
    """
    Download files from a space.
    :param path: Path of directory to download files into. If no path is provided, the files will be downloaded into the current working directory.
    :param code: Code of the space to download files from. If no code is provided, an attempt will be made to use the code saved in memory.
    :param a: Downloads all files from the space.
    """
    p_head()
    download_all = a
    try:
        code = resolve_code(code)
    except SpaceNotFoundError:
        p_fail("Space not found.")
        return
    except MissingCodeError:
        p_fail("Missing required param: code.")
        return

    files = get_files(code)
    if download_all:
        p_info("Downloading all files")
        selected_files = files
    else:
        p_question("Which file would you like to download?")
        for index, file in enumerate(files):
            print("({index}) {file_name} ".format(index=index, file_name=file["name"]))

        try:
            indexes = index_input(min=0, max=len(files))
        except ValueError:
            p_fail("Invalid input value detected.")
            return
        selected_files = list(map(lambda index: files[index], indexes))

    for selected_file in progress_bar(
        selected_files, prefix="Progress", length=cols - 20
    ):
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


def upload_files(path, code=None, a=False):
    """
    Upload files to a space.
    :param path: Path to file or directory. If the path provided is a directory, then an interactive prompt will be displayed to select which files in the directory are to be uploaded. If the path is a file, then the file will be uploaded.
    :param code: Code of the space to upload files to. If no code is provided, an attempt will be made to use the code saved in memory.
    :param a: Uploads all files in the directory. Has no effect if the path provided is to a file.
    """
    p_head()
    upload_all = a
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
        # Filter out directories
        paths = list(
            filter(lambda x: os.path.isfile(os.path.join(path, x)), os.listdir(path))
        )
        if upload_all:
            p_info("Uploading all files")
            file_paths = list(map(lambda x: os.path.join(path, x), paths))
        else:
            p_question("Which files do you want to upload?")

            for index, file_path in enumerate(paths):
                print("({index}) {file_path}".format(index=index, file_path=file_path))

            try:
                indexes = index_input(min=0, max=len(paths))
            except ValueError:
                p_fail("Invalid input value detected.")
                return
            file_paths = list(map(lambda x: os.path.join(path, paths[x]), indexes))

    try:
        for file_path in progress_bar(file_paths, prefix="Progress:", length=cols - 20):
            upload_file(code, file_path)

        p_ok("Done!")

    except MaxCapacityReached:
        p_fail("Max capacity reached.")
        return


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

    with open(path, "rb") as f:

        url = API_URL + "/signed-urls"
        data = {"code": code, "file": {"size": file_size}}
        response = requests.post(
            url,
            json=data,
            headers=BASE_HEADERS,
        )
        if response.status_code == 403:
            raise MaxCapacityReached

        response = response.json()
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
            "name": complete_file_name,
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


def spaces(default=None):
    """
    List recently accessed spaces.
    """
    p_head()

    def print_spaces():
        for index, code in enumerate(codes):
            url = "https://app.floatingfile.space/s/" + code
            if index == 0:
                p_ok("(default) {code} ({url})".format(index=index, code=code, url=url))
            else:
                print(
                    "({index}) {code} ({url})".format(index=index, code=code, url=url)
                )

    codes = get_codes()
    if len(codes) == 0:
        print("There are no spaces.")
        return
    if default == True:
        p_question("Which space do you want to set as the default?")
        print_spaces()
        selection = input()

        for index, code in enumerate(codes):
            if index == int(selection):
                default_code = code
                break

        codes.remove(default_code)
        codes.insert(0, default_code)
        set_codes(codes)

        p_ok("Done!")
        p_sub("The default space is now {code}".format(code=default_code))

    elif isinstance(default, str):
        print(default)
    else:
        print_spaces()
