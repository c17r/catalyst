from unittest.mock import patch, MagicMock
import pytest

from mountains import create_key


def test_create_key_empty():
    data = ""

    rv = create_key(data)

    assert rv == {'': 0}


def test_create_key_valid_1():
    data = "one,two,three"

    rv = create_key(data)

    assert rv == {
        'one': 0,
        'two': 1,
        'three': 2
    }


def test_create_key_valid_2():
    data = "three,two,one"

    rv = create_key(data)

    assert rv == {
        'three': 0,
        'two': 1,
        'one': 2,
    }
