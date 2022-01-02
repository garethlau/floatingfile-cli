import fire
from src.cli import (
    create_space,
    destroy_space,
    list_files,
    remove_files,
    download_files,
    upload_files,
    spaces,
    config,
)


if __name__ == "__main__":
    fire.Fire(
        {
            "create": create_space,
            "destroy": destroy_space,
            "files": list_files,
            "remove": remove_files,
            "download": download_files,
            "upload": upload_files,
            "spaces": spaces,
            "config": config,
        }
    )
