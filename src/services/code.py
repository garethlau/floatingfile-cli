from ..errors import SpaceNotFoundError, MissingCodeError
from ..models.Space import Space
from ..storage import Storage


def resolve_code(code=None):
    store = Storage("data.pkl", [])
    data = store.read()

    if code:
        # Code was supplied
        code = code.upper()
        if not Space.is_alive(code):
            raise SpaceNotFoundError

        data.insert(0, {"code": code})
        store.write(data)

        return code

    # Code was not supplied, check storage
    if not data or len(data) == 0:
        raise MissingCodeError

    code = data[0]["code"]

    if not Space.is_alive(code):
        # The code no longer maps to an existing space, remove it from memory
        data = [x for x in data if x["code"] != code]
        store.write(data)
        raise SpaceNotFoundError

    return code


def get_codes():
    store = Storage("data.pkl")
    data = store.read()
    codes = []
    for d in data:
        code = d["code"]
        if Space.is_alive(code):
            codes.append(code)
        else:
            delete_code(code)
            pass
    return codes


def delete_code(code):
    store = Storage("data.pkl")

    data = store.read()
    data = [x for x in data if x["code"] != code]

    store.write(data)


def add_code(code):
    code = code.upper()
    store = Storage("data.pkl")
    data = store.read()
    data.insert(0, {"code": code})
    store.write(data)
