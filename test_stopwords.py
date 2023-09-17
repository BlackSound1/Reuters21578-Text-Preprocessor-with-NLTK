import pytest
import typer

from handle_stopwords import remove_stopwords


def test_simple_stem():
    # ASSUMES THE USE OF THE GIVEN Stopwords-used-for-output.txt FILE IN ASSIGNMENT SUBMISSION
    assert (remove_stopwords(['where', 'are', 'you', 'at', 'for', 'once', 'at', 'at']) == ['are', 'you', 'once'])


def test_only_punctuation():
    assert remove_stopwords(['?', '!', '.', ',', ';', '\'']) == ['?', '!', '.', ',', ';', '\'']


def test_list_of_blanks():
    with pytest.raises(typer.Exit):
        remove_stopwords([""])

    with pytest.raises(typer.Exit):
        remove_stopwords([" "])

    with pytest.raises(typer.Exit):
        remove_stopwords(["", " "])


def test_no_tokens():
    with pytest.raises(TypeError):
        remove_stopwords()
