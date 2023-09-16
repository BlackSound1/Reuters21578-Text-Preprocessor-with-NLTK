from typing import Union
from pathlib import Path


def write_to_file(file_path: Path, what_to_write: Union[list, str]) -> None:

    FILENAME = "output" / file_path

    # Ensure the path to the desired file (and all its parents) exists before writing to it
    Path(FILENAME.parent).mkdir(parents=True, exist_ok=True)

    # Write to file
    with open(FILENAME, "w+t", encoding="utf-8") as file:
        # If a string is given to write, simply write it
        if type(what_to_write) is str:
            file.writelines(what_to_write)

        # If a list of strings is given, write it line by line
        elif type(what_to_write) is list:
            file.writelines([i + '\n' for i in what_to_write])
