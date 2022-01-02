import re

def index_input(min=0, max=None):
    user_input = input()
    user_input_arr = re.split("(?:\s|,)", user_input)

    indexes = set()
    for x in user_input_arr:
        # Skip empty string
        if x.strip() == "":
            continue

        # Convert to integer
        index = int(x)

        # Check that the input index is within bounds
        if index < min:
            raise ValueError
        elif max is not None and index > max:
            raise ValueError

        indexes.add(index)

    return list(indexes)


def best_effort_file_type(ext):
    match ext:
        case "md":
            return "text/markdown"
        case _:
            return "application/octet-stream"
