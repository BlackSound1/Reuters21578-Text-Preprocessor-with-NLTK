from utilities import get_five_articles, textualize
from tokenization import tokenize
from lowercase import lowercase
from stem import stem
from handle_stopwords import remove_stopwords


def pipeline():
    """Run each step of the pipeline automatically"""

    ALL_ARTICLES = get_five_articles()
    STOPWORDS_FILE = "Stopwords-used-for-output.txt"

    for i, article in enumerate(ALL_ARTICLES, start=1):
        this_article = textualize(article, i)
        tokenized = tokenize(this_article, i)
        lower_cased = lowercase(tokenized, i)
        stemmed = stem(lower_cased, i)
        remove_stopwords(stemmed, i, STOPWORDS_FILE)


if __name__ == '__main__':
    pipeline()
