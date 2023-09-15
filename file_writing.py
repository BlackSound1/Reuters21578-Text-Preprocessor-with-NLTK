from typing import Union
from pathlib import Path


def write_to_file(article_num: int, file_name: str, what_to_write: Union[list, str], custom: bool = False) -> None:
    """
    Handle writing to output files

    :param article_num: Which article this is
    :param file_name: The name of the file to save to
    :param what_to_write: The contents of the file
    :param custom: Whether a custom, command-line text or text from the Reuters corpus
    """

    # Choose what directory to save the file in, depending on whether it's normal Reuters text,
    # or custom command-line text
    DIR_NAME = "output/custom_article" if custom else f"output/article{article_num}"

    FILENAME = f"{DIR_NAME}/{file_name}.txt"

    # Ensure the path to the desired file (and all its parents) exists before writing to it
    Path(DIR_NAME).mkdir(parents=True, exist_ok=True)

    with open(FILENAME, "w+t", encoding="utf-8") as file:
        # If a string is given to write, simply write it
        if type(what_to_write) is str:
            file.writelines(what_to_write)

        # If a list of strings is given, write it line by line
        elif type(what_to_write) is list:
            file.writelines([i + '\n' for i in what_to_write])
