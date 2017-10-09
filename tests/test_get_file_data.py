from unittest.mock import patch, MagicMock, PropertyMock, mock_open
import pytest

from mountains import get_file_data, RetrieveError, MissingDataError


@patch('builtins.open', new_callable=mock_open)
def test_get_file_data_invalid_filename(m_open):
    m_open.side_effect = Exception

    with pytest.raises(RetrieveError):
        rv = list(get_file_data('non-existent'))

    m_open.assert_called_once_with('non-existent', 'r', encoding='utf-8')


@patch('builtins.open', new_callable=mock_open, read_data='')
def test_get_file_data_empty_file(m_open):

    with pytest.raises(MissingDataError):
        rv = list(get_file_data('non-existent'))

    m_open.assert_called_once_with('non-existent', 'r', encoding='utf-8')


@patch('builtins.open', new_callable=mock_open, read_data='one\ntwo')
def test_get_file_data_valid(m_open):

    rv = list(get_file_data('non-existent'))

    m_open.assert_called_once_with('non-existent', 'r', encoding='utf-8')

    assert rv == ['one', 'two']
