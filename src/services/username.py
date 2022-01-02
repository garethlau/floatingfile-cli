from ..storage import Storage


def get_username():
    store = Storage("settings.pkl")
    data = store.read()
    if len(data) == 0:
        return ""
    return data["username"]
