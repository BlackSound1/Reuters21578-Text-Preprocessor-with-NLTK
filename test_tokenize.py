from pathlib import Path

import pytest
import typer

from tokenization import tokenize


def test_simple_tokenization():
    assert tokenize("This is a test string") == ["This", "is", "a", "test", "string"]


def test_only_punctuation():
    assert tokenize("?!.,;'") == [ch for ch in "?!.,;'"]


def test_blank_text():
    with pytest.raises(typer.Exit):
        tokenize("")


def test_no_text():
    with pytest.raises(TypeError):
        tokenize()
