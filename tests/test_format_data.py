from unittest.mock import patch, MagicMock
import pytest

from mountains import format_data, InvalidDataError


def test_format_data_invalid_1():
    key = {}
    data = ""

    with pytest.raises(InvalidDataError) as e:
        rv = format_data(key, data)

        assert "Data format error:" in str(e)


def test_format_data_invalid_2():
    key = {'Name': 99}
    data = ""

    with pytest.raises(InvalidDataError) as e:
        rv = format_data(key, data)

        assert "Data format error:" in str(e)


def test_format_data_valid_1():
    key = {"Name": 0, "Altitude (m)": 1}
    data = "mountain_name,12345"

    rv = format_data(key, data)

    assert rv == "{data[0]} has an altitude of {data[1]} meters.".format(data=data.split(','))


def test_format_data_valid_2():
    key = {"Name": 3, "Altitude (m)": 6}
    data = "blank,blank,blank,mountain_name,blank,blank,12345,blank"

    rv = format_data(key, data)

    assert rv == "{data[3]} has an altitude of {data[6]} meters.".format(data=data.split(','))


def test_format_data_valid_null_altitude():
    key = {"Name": 0, "Altitude (m)": 1}
    data = "mountain_name,null"

    rv = format_data(key, data)

    assert rv == "{data[0]} has an altitude of unknown meters.".format(data=data.split(','))
