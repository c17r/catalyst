from unittest.mock import patch, MagicMock
import pytest

from datetime import datetime
from mountains import create_header


def test_create_header_first_of_month_early():
    dt = datetime(2017, 10, 1, 9, 1, 2)

    rv = create_header(dt)

    assert rv == '2017-10-01 09:01:02 (Sunday)\n'


def test_create_header_last_of_month_late():
    dt = datetime(2017, 10, 31, 23, 50, 50)

    rv = create_header(dt)

    assert rv == '2017-10-31 23:50:50 (Tuesday)\n'
