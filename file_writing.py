from typing import Union
from pathlib import Path


def write_to_file(file_path: Path, what_to_write: Union[list, str]) -> None:
    """
    Write the given content to the given file.

    You can specify any number of nested directories, as long as a filename is specified at the end.

    File paths will have `output/` prepended, thus saving to the `output/` folder. So a given file name of
    `my_folder/my_subfolder/file.txt` will save as `output/my_folder/my_subfolder/file.txt`

    :param file_path: Where to write to. Always writes in the `output/` directory
    :param what_to_write: The content to write. Can be a string or list of strings
    """

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
