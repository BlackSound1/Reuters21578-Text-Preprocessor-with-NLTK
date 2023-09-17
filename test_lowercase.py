import pytest
import typer

from lowercase import lowercase


def test_simple_lowercase():
    assert lowercase(["THESE", "ARE", "TEST", "TOKENS"]) == ['these', 'are', 'test', 'tokens']


def test_only_punctuation():
    assert lowercase(['?', '!', '.', ',', ';', '\'']) == ['?', '!', '.', ',', ';', '\'']


def test_list_of_blanks():
    with pytest.raises(typer.Exit):
        lowercase([""])

    with pytest.raises(typer.Exit):
        lowercase([" "])

    with pytest.raises(typer.Exit):
        lowercase(["", " "])


def test_no_tokens():
    with pytest.raises(TypeError):
        lowercase()
