import os
import pickle
from .errors import SpaceNotFoundError, MissingCodeError
from .utils import does_exists
from .printer import p_ok, p_question, p_sub

filename = os.path.join(os.getenv("HOME"), ".floatingfile", "data.pkl")


def mem_exists():
    return os.path.isfile(filename)


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


# TODO: Better name for setting the default code. This method should also be moved out of storage.py.
def set_default():
    with open(filename, "rb") as f:
        data = pickle.load(f)
        f.close()

    p_question("Which space do you want to set as the default?")
    data = list(filter(lambda d: does_exists(d["code"]), data))

    for index, d in enumerate(data):
        code = d["code"]
        if index == 0:
            p_ok("(default) {code}".format(index=index, code=code))
        else:
            print("({index}) {code}".format(index=index, code=code))

    selection = input()

    # TODO: There has to be a better way of finding an item and moving it the front
    for index, d in enumerate(data):
        if index == int(selection):
            default = d
            break

    data.remove(default)
    data.insert(0, default)

    with open(filename, "wb") as f:
        pickle.dump(data, f)
        f.close()

    p_ok("Done!")
    p_sub("The default space is now {code}".format(code=default["code"]))


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
