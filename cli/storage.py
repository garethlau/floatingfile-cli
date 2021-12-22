import os
import pickle
from datetime import datetime, timedelta
from .errors import SpaceNotFoundError, MissingCodeError
from .utils import does_exists, is_expired
from .printer import p_ok, p_question, p_sub

p = os.path.join(os.getenv("HOME"), ".floatingfile", "data.pkl")


def mem_exists():
    return os.path.isfile(p)


def save_code(code):
    code = code.upper()
    if not mem_exists():
        data = []
    else:
        f = open(p, "rb")
        data = pickle.load(f)
        f.close()

    # TODO: Fix created at logic. Spaces aren't always created via cli
    data.insert(0, {"code": code, "created_at": datetime.now()})

    with open(p, "w+b") as f:
        pickle.dump(data, f)
        f.close()


# TODO: This method should only be responsible for retreiving the objects from memory.
# It should not be responsible for displaying the results to the user
def get_codes():
    if not mem_exists():
        print("There are no saved spaces.")
        return

    with open(p, "rb") as f:
        data = pickle.load(f)
        f.close()

    print("  Code  | Created At")
    for d in data:
        code = d["code"]
        created_at = d["created_at"]

        if is_expired(created_at):
            print("expired")
            del_code(code)
        else:
            # TODO: Format created at date
            print(" {code} | {created_at}".format(code=code, created_at=created_at))


# TODO: Better name for setting the default code. This method should also be moved out of storage.py.
def set_default():
    with open(p, "rb") as f:
        data = pickle.load(f)
        f.close()

    p_question("Which space do you want to set as the default?")
    data = list(filter(lambda d: not is_expired(d["created_at"]), data))

    for index, d in enumerate(data):
        code = d["code"]
        if index == 0:
            p_ok("(default) {code}".format(index=index, code=code))
        else:
            print("({index}) {code}".format(index=index, code=code))

    selection = input()

    # TODO: There has to be a better way of finding an item and moving it the front
    for index, d in enumerate(data):
        code = d["code"]
        if index == int(selection):
            sd = d

    data.remove(sd)
    data.insert(0, sd)

    with open(p, "wb") as f:
        pickle.dump(data, f)
        f.close()

    p_ok("Done!")
    p_sub("The default space is now {code}".format(code=sd["code"]))


def del_code(code):
    with open(p, "rb") as f:
        data = pickle.load(f)
        f.close()

    data = [x for x in data if x["code"] != code]

    with open(p, "wb") as f:
        pickle.dump(data, f)
        f.close()


def resolve_code(code=None):
    if code:
        code = code.upper()
        # Code was supplied
        if not does_exists(code):
            raise SpaceNotFoundError
        save_code(code)
        return code
    else:
        # Code was not supplied, check storage

        if not os.path.isfile(p):
            f = open(p, "x")
            f.close()
            raise MissingCodeError

        # Open the data file

        with open(p, "rb") as f:
            data = pickle.load(f)
            f.close()

        if not data or len(data) == 0:
            raise MissingCodeError

        code = data[0]["code"]
        created_at = data[0]["created_at"]

        if is_expired(created_at):
            del_code(code)
            raise SpaceNotFoundError

        if not does_exists(code):
            # The code no longer maps to an existing space, remove it from memory
            del_code(code)
            raise SpaceNotFoundError

        return code
