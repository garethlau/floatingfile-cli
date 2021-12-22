import fire
from cli.main import (
    create_space,
    destroy_space,
    list_files,
    remove_files,
    download_files,
    upload_files,
)
from cli.storage import (
    del_code,
    get_codes,
    save_code,
    del_code,
    resolve_code,
    set_default,
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
            "codes": get_codes,
            "save": save_code,
            "delete": del_code,
            "resolve": resolve_code,
            "spaces": get_codes,
            "set": set_default,
        }
    )
