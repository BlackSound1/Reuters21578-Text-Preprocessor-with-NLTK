from typing import List


def lowercase(text: List[str], article_num: int) -> List[str]:
    LOWER_CASED: List[str] = [token.lower() for token in text]

    if article_num < 5:
        print("Saving to file (LOWERCASE)")

    return LOWER_CASED
