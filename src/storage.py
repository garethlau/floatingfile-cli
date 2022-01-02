import os
import pickle
from .errors import SpaceNotFoundError, MissingCodeError
from .utils import does_exists
from .printer import p_ok, p_question, p_sub

filename = os.path.join(os.getenv("HOME"), ".floatingfile", "data.pkl")


def mem_exists():
    return os.path.isfile(filename)


def save_username(username):
    config_filename = os.path.join(os.getenv("HOME"), ".floatingfile", "config.pkl")
    if not os.path.isfile(config_filename):
        data = {}
    else:
        f = open(config_filename, "rb")
        data = pickle.load(f)
        f.close()

    data["username"] = username

    os.makedirs(os.path.dirname(config_filename), exist_ok=True)
    with open(config_filename, "wb+") as f:
        pickle.dump(data, f)
        f.close()


def get_username():
    config_filename = os.path.join(os.getenv("HOME"), ".floatingfile", "config.pkl")
    if not os.path.isfile(config_filename):
        return None
    f = open(config_filename, "rb")
    data = pickle.load(f)
    f.close()

    return data["username"]


def save_code(code):
    code = code.upper()
    if not mem_exists():
        data = []
    else:
        f = open(filename, "rb")
        data = pickle.load(f)
        f.close()

    data.insert(0, {"code": code})

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb+") as f:
        pickle.dump(data, f)
        f.close()


def get_codes():
    codes = []
    if not mem_exists():
        return codes

    with open(filename, "rb") as f:
        data = pickle.load(f)
        f.close()

    for d in data:
        code = d["code"]
        if does_exists(code):
            codes.append(code)
        else:
            del_code(code)

    return codes


def set_codes(codes):
    data = []
    for code in codes:
        data.append({"code": code})
    with open(filename, "wb") as f:
        pickle.dump(data, f)
        f.close()


def del_code(code):
    with open(filename, "rb") as f:
        data = pickle.load(f)
        f.close()

    data = [x for x in data if x["code"] != code]

    with open(filename, "wb") as f:
        pickle.dump(data, f)
        f.close()


def resolve_code(code=None):
    if code:
        # Code was supplied
        code = code.upper()
        if not does_exists(code):
            raise SpaceNotFoundError

        save_code(code)
        return code
    else:
        # Code was not supplied, check storage
        if not mem_exists():
            f = open(filename, "x")
            f.close()
            raise MissingCodeError

        # Open the data file

        with open(filename, "rb") as f:
            data = pickle.load(f)
            f.close()

        if not data or len(data) == 0:
            raise MissingCodeError

        code = data[0]["code"]

        if not does_exists(code):
            # The code no longer maps to an existing space, remove it from memory
            del_code(code)
            raise SpaceNotFoundError

        return code
