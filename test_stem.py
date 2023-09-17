import pytest
import typer

from stem import stem


def test_simple_stem():
    assert (stem(['greetings', 'this', 'is', 'interesting', 'sample', 'text']) ==
            ['greet', 'thi', 'is', 'interest', 'sampl', 'text'])


def test_only_punctuation():
    assert stem(['?', '!', '.', ',', ';', '\'']) == ['?', '!', '.', ',', ';', '\'']


def test_list_of_blanks():
    with pytest.raises(typer.Exit):
        stem([""])

    with pytest.raises(typer.Exit):
        stem([" "])

    with pytest.raises(typer.Exit):
        stem(["", " "])


def test_no_tokens():
    with pytest.raises(TypeError):
        stem()
