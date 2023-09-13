from typing import List

from file_writing import write_to_file


def lowercase(tokens: List[str], article_num: int) -> List[str]:
    """
    Turn the tokens of the article all lowercase

    :param tokens: The list of tokens to make lowercase
    :param article_num: Which article this is
    :return: The list of tokens, all lowercase
    """

    # Create the lowercase version of the input tokens list
    LOWER_CASED: List[str] = [token.lower() for token in tokens]

    print(f"Article {article_num}: writing to file output/article{article_num}/Lowercased-output.txt")

    write_to_file(article_num, "3. Lowercased-output", LOWER_CASED)

    return LOWER_CASED
