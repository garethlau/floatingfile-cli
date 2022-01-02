import os
import pickle


class Storage:
    def __init__(self, name, init_value={}) -> None:
        self.name = name
        self.filename = os.path.join(os.getenv("HOME"), ".floatingfile", name)

        if not os.path.isfile(self.filename):
            # file does not exist, create it
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            with open(self.filename, "wb+") as f:
                pickle.dump(init_value, f)
                f.close()

    def read(self):
        with open(self.filename, "rb") as f:
            data = pickle.load(f)
            f.close()
        return data

    def write(self, data):
        with open(self.filename, "wb+") as f:
            pickle.dump(data, f)
            f.close()
