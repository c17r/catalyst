from unittest.mock import patch, MagicMock, PropertyMock
import pytest

from mountains import get_http_data, RetrieveError, MissingDataError


def make_req_object(text_value=''):
    req = MagicMock()

    text = PropertyMock(return_value=text_value)
    type(req).text = text

    lines = MagicMock()
    req.iter_lines.return_value = lines
    return req, text, lines


@patch('mountains.core.requests.get')
def test_get_http_data_invalid_url(m_get):
    m_get.side_effect = Exception()

    with pytest.raises(RetrieveError):
        get_http_data('http://none')

    m_get.assert_called_once_with('http://none', stream=True)


@patch('mountains.core.requests.get')
def test_get_http_data_invalid_missing_data(m_get):
    req, text, lines = make_req_object('')
    m_get.return_value = req

    with pytest.raises(MissingDataError):
        get_http_data('http://none')

    m_get.assert_called_once_with('http://none', stream=True)
    text.assert_called_once_with()
    lines.assert_not_called()


@patch('mountains.core.requests.get')
def test_get_http_data_valid(m_get):
    req, text, lines = make_req_object('non-empty')
    m_get.return_value = req

    rv = get_http_data('http://none')

    m_get.assert_called_once_with('http://none', stream=True)
    assert rv == lines
    text.assert_called_once_with()
    req.iter_lines.called_once_with()
