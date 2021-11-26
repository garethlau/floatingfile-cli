import fire
import requests
import os
import mimetypes
import errno

API_URL = "http://localhost:5000/api/v5"
API_KEY = "secretcat"


def create():
    url = API_URL + "/spaces"
    headers = {"api-key": API_KEY}
    r = requests.post(url, headers=headers)
    data = r.json()
    code = data["space"]["code"]
    print("Created a new space: " + code)


def list(code):
    headers = {"api-key": API_KEY}
    response = requests.get(API_URL + "/spaces/" + code, headers=headers)
    response = response.json()
    space = response["space"]
    files = space["files"]
    for file in files:
        name = file["name"]
        key = file["key"]
        print(name, key)


def download(code, path):
    headers = {"api-key": API_KEY}
    response = requests.get(API_URL + "/spaces/" + code, headers=headers)
    response = response.json()
    space = response["space"]
    files = space["files"]
    print("Which file would you like to download?")
    for index, file in enumerate(files):
        print("({index}) {file_name} ".format(index=index, file_name=file["name"]))

    selected_ids = input()

    selected_ids = selected_ids.split(" ")
    selected_files = map(lambda id: files[int(id)], selected_ids)
    for selected_file in selected_files:
        r = requests.get(selected_file["signedUrl"])

        if path is not None:
            file_path = os.path.join(path, selected_file["name"])
            if not os.path.exists(os.path.dirname(file_path)):
                try:
                    os.makedirs(os.path.dirname(file_path))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
        else:
            file_path = selected_file["name"]

        open(file_path, "wb").write(r.content)


def upload(code, path):
    if code is None:
        raise Exception("Missing code.")
    print("Uploading")

    file_size = os.stat(path).st_size
    complete_file_name = path.split("/")[-1]
    file_ext = "." + complete_file_name.split(".")[-1]
    file_name = complete_file_name.split(".")[0]
    file_type = mimetypes.guess_type(path)[0]
    print(file_name, file_ext, file_size, file_type)

    with open(path, "rb") as f:

        url = API_URL + "/signed-urls"
        headers = {"api-key": API_KEY}
        data = {"code": code, "file": {"size": file_size}}
        print(data)
        response = requests.post(
            url,
            json=data,
            headers=headers,
        ).json()
        print(response)

        signed_url = response["signedUrl"]
        key = response["key"]

        print(signed_url, key)

        response = requests.put(
            signed_url,
            headers={"Content-type": "application/x-www-form-urlencoded"},
            data=f,
        )
        if not (response.status_code == 200):
            print("Error uploading file to AWS")
            print(response)

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
        print(response)

        f.close()


if __name__ == "__main__":
    fire.Fire()
