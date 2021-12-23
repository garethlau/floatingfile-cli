import fire
from src.main import (
    create_space,
    destroy_space,
    list_files,
    remove_files,
    download_files,
    upload_files,
)

if __name__ == "__main__":
    fire.Fire(
        {
            "create": create_space,
            "destroy": destroy_space,
            "list": list_files,
            "remove": remove_files,
            "download": download_files,
            "upload": upload_files,
        }
    )
