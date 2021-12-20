import os
from .errors import SpaceNotFoundError, MissingCodeError
from .utils import does_exists

def save_code(code):
    p = os.path.join(os.getenv("HOME"), ".floatingfile", "data.txt")
    with open(p, "w") as f:
        f.write("CODE=" + code)


def del_code():
    p = os.path.join(os.getenv("HOME"), ".floatingfile", "data.txt")
    with open(p, "w") as f:
        f.write("")


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
        p = os.path.join(os.getenv("HOME"), ".floatingfile", "data.txt")

        if not os.path.isfile(p):
            f = open(p, "x")
            f.close()

        # Open the data file
        with open(p, "r") as f:
            line = f.readline()
            if not line:
                # There is no saved code
                raise MissingCodeError
            saved_code = line.split("=")[1].rstrip()

            if not does_exists(saved_code):
                del_code()
                f.close()
                raise SpaceNotFoundError
            f.close()

        return saved_code
