from unittest.mock import patch, MagicMock
from io import StringIO
import argparse
import sys
import pytest

from mountains import handle_args


class StdIOBuffer(StringIO):
    pass


class ArgumentParserError(Exception):
    def __init__(self, message, stdout=None, stderr=None, error_code=None):
        Exception.__init__(self, message, stdout, stderr)
        self.message = message
        self.stdout = stdout
        self.stderr = stderr
        self.error_code = error_code


def stderr_to_parser_error(parse_args, *args, **kwargs):
    # if this is being called recursively and stderr or stdout is already being
    # redirected, simply call the function and let the enclosing function
    # catch the exception
    if isinstance(sys.stderr, StdIOBuffer) or isinstance(sys.stdout, StdIOBuffer):
        return parse_args(*args, **kwargs)

    # if this is not being called recursively, redirect stderr and
    # use it as the ArgumentParserError message
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = StdIOBuffer()
    sys.stderr = StdIOBuffer()
    try:
        try:
            result = parse_args(*args, **kwargs)
            for key in list(vars(result)):
                if getattr(result, key) is sys.stdout:
                    setattr(result, key, old_stdout)
                if getattr(result, key) is sys.stderr:
                    setattr(result, key, old_stderr)
            return result
        except SystemExit:
            code = sys.exc_info()[1].code
            stdout = sys.stdout.getvalue()
            stderr = sys.stderr.getvalue()
            raise ArgumentParserError("SystemExit", stdout, stderr, code)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


class ErrorRaisingArgumentParser(argparse.ArgumentParser):

    def parse_args(self, *args, **kwargs):
        parse_args = super(ErrorRaisingArgumentParser, self).parse_args
        return stderr_to_parser_error(parse_args, *args, **kwargs)

    def exit(self, *args, **kwargs):
        exit = super(ErrorRaisingArgumentParser, self).exit
        return stderr_to_parser_error(exit, *args, **kwargs)

    def error(self, *args, **kwargs):
        error = super(ErrorRaisingArgumentParser, self).error
        return stderr_to_parser_error(error, *args, **kwargs)


@patch('mountains.core.ArgumentParser')
def test_handle_args_no_args(m_parser):
    m_parser.return_value = ErrorRaisingArgumentParser()

    with pytest.raises(ArgumentParserError):
        handle_args([])


@patch('mountains.core.ArgumentParser')
def test_handle_args_two_args(m_parser):
    m_parser.return_value = ErrorRaisingArgumentParser()

    with pytest.raises(ArgumentParserError):
        handle_args(['--url', 'http://example.com', '--file', 'example.file'])


@patch('mountains.core.ArgumentParser')
def test_handle_args_valid_url(m_parser):
    m_parser.return_value = ErrorRaisingArgumentParser()
    url = 'http://example.com'

    rv = handle_args(['--url', url])

    assert rv.url == url
    assert rv.file is None


@patch('mountains.core.ArgumentParser')
def test_handle_args_valid_file(m_parser):
    m_parser.return_value = ErrorRaisingArgumentParser()
    file = 'example.file'

    rv = handle_args(['--file', file])

    assert rv.file == file
    assert rv.url is None
