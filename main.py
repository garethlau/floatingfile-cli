import fire
from src.cli import (
    create_space,
    destroy_space,
    list_files,
    remove_files,
    download_files,
    upload_files,
    spaces,
)
from src.config import init


if __name__ == "__main__":
    init()
    fire.Fire(
        {
            "create": create_space,
            "destroy": destroy_space,
            "files": list_files,
            "remove": remove_files,
            "download": download_files,
            "upload": upload_files,
            "spaces": spaces,
        }
    )
