from utilities import fix_encoding_mistakes, get_all_texts
from tokenization import tokenize
from lowercase import lowercase
from stem import stem
from handle_stopwords import remove_stopwords
from file_writing import write_to_file


def pipeline():
    ALL_ARTICLES = get_all_texts()
    STOPWORDS_FILE = "Stopwords-used-for-output.txt"

    for i, article in enumerate(ALL_ARTICLES):
        this_article = str(article)
        if i < 5:
            write_to_file(i, "Initial-text", this_article)
        fixed = fix_encoding_mistakes(this_article)
        tokenized = tokenize(fixed, i)
        lower_cased = lowercase(tokenized, i)
        stemmed = stem(lower_cased, i)
        stopwords_removed = remove_stopwords(stemmed, i, STOPWORDS_FILE)


if __name__ == '__main__':
    pipeline()
