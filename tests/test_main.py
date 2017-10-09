from unittest.mock import patch, MagicMock, PropertyMock, mock_open, call
import pytest

from mountains import main


@patch('mountains.core.handle_args')
@patch('mountains.core.get_http_data')
@patch('mountains.core.get_file_data')
@patch('mountains.core.create_key')
@patch('mountains.core.create_header')
@patch('mountains.core.format_data')
def test_error(m_format, m_header, m_key, m_file, m_http, m_args):
    m_args.side_effect = Exception

    rv = main()

    assert rv == -1
    m_http.assert_not_called()
    m_file.assert_not_called()
    m_key.assert_not_called()
    m_header.assert_not_called()
    m_format.assert_not_called()


@patch('mountains.core.handle_args')
@patch('mountains.core.get_http_data')
@patch('mountains.core.get_file_data')
@patch('mountains.core.create_key')
@patch('mountains.core.create_header')
@patch('mountains.core.format_data')
def test_args_url(m_format, m_header, m_key, m_file, m_http, m_args):
    args = MagicMock()
    type(args).url = PropertyMock(return_value='value')
    m_args.return_value = args

    rv = main()

    assert rv == 0
    m_http.assert_called_with('value')
    m_file.assert_not_called()


@patch('mountains.core.handle_args')
@patch('mountains.core.get_http_data')
@patch('mountains.core.get_file_data')
@patch('mountains.core.create_key')
@patch('mountains.core.create_header')
@patch('mountains.core.format_data')
def test_args_file(m_format, m_header, m_key, m_file, m_http, m_args):
    args = MagicMock()
    type(args).url = PropertyMock(return_value=None)
    type(args).file = PropertyMock(return_value='value')
    m_args.return_value = args

    rv = main()

    assert rv == 0
    m_file.assert_called_with('value')
    m_http.assert_not_called()

@patch('mountains.core.handle_args')
@patch('mountains.core.get_http_data')
@patch('mountains.core.get_file_data')
@patch('mountains.core.create_key')
@patch('mountains.core.create_header')
@patch('mountains.core.format_data')
def test_line_loop(m_format, m_header, m_key, m_file, m_http, m_args):
    lines = iter(['head', 'one', '', 'three'])
    m_http.return_value = lines
    args = MagicMock()
    type(args).url = PropertyMock(return_value='value')
    m_args.return_value = args
    key = MagicMock()
    m_key.return_value = key
    m_format.return_value = ''

    rv = main()

    assert rv == 0
    assert m_format.call_count == 2
    m_format.assert_has_calls([
        call(key, 'one'),
        call(key, 'three'),
    ])
