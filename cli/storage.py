import os
import pickle
from datetime import datetime, timedelta
from .errors import SpaceNotFoundError, MissingCodeError
from .utils import does_exists, is_expired

p = os.path.join(os.getenv("HOME"), ".floatingfile", "data.pkl")


def save_code(code):

    if not os.path.isfile(p):
        f = open(p, "wb")
        pickle.dump([], f)
        f.close()

    with open(p, "rb") as f:
        data = pickle.load(f)
        f.close()

    data.insert(0, {"code": code, "created_at": datetime.now()})

    with open(p, "w+b") as f:
        pickle.dump(data, f)
        f.close()


def get_codes():
    with open(p, "rb") as f:
        data = pickle.load(f)
        f.close()

    for d in data:
        code = d['code']
        created_at = d['created_at']

        if (is_expired(created_at)):
            del_code(code)
        else:
            print(code)



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
