from typing import List

from file_writing import write_to_file


def lowercase(text: List[str], article_num: int) -> List[str]:
    LOWER_CASED: List[str] = [token.lower() for token in text]

    if article_num < 5:
        print(f"Article {article_num}: writing to file output/article{article_num}/Lowercased-output.txt")

        write_to_file(article_num, "Lowercased-output", LOWER_CASED)

    return LOWER_CASED
