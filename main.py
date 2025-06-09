from octopus import Octopus
from pathlib import Path


if __name__ == "__main__":
    path_to_file = Path("files")
    path_to_logs = Path("logs")
    path_to_file.mkdir(exist_ok=True)
    path_to_logs.mkdir(exist_ok=True)

    """
    Example:
    
    some_brand = Octopus("Some_brand")
    some_brand.get_file_from_yandex(
        "yandex_url",
        "file_name_from_yandex",
        format_file_xlsx="xlsx",
    )
    """
