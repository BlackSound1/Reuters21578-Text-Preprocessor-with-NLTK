from pathlib import Path


def write_to_file(article_num: int, file_name: str, what_to_write: list) -> None:
    DIR_NAME = f"output/article{article_num}"

    FILENAME = f"{DIR_NAME}/{file_name}.txt"

    Path(DIR_NAME).mkdir(parents=True, exist_ok=True)

    with open(FILENAME, "w+t", encoding="utf-8") as file:
        # Write each entry in the list line-by-line
        file.writelines([i + '\n' for i in what_to_write])
