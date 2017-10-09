import sys
import os
from argparse import ArgumentParser
from datetime import datetime

from . import errors

import requests


def handle_args(sys_args):
    parser = ArgumentParser(description="""
        Retrieve the mountain data.
        Output each mountains altitude (if present).
        """)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', help="URL that contains the mountain data")
    group.add_argument('--file', help="local file that contains the mountain data")
    args = parser.parse_args(sys_args)
    return args


def get_file_data(filename):
    lines = False
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # This loop is odd for reasons: we want to not load the entire file into memory rather stream it line by
            # line.  We want to be able to track whether or not the file had any data.  Finally, we want to be able to
            # unit test it.  Python's mock_open() seems to have an issue with "for line in f: yield line.rstrip()"
            # while "for line = f.readline()" yields one character at a time.  So here we are.
            while True:
                try:
                    line = f.readline()
                except StopIteration:  # needed for py34 and r.readline(), possibly only under mock conditions
                    line = ''

                if line:
                    lines = True
                    yield line.rstrip()
                else:
                    break
    except Exception as e:
        raise errors.RetrieveError("File error: %s" % str(e))

    if not lines:
        raise errors.MissingDataError("File contains no data.")


def get_http_data(url):
    try:
        req = requests.get(url, stream=True)
    except Exception as e:
        raise errors.RetrieveError("URL error: %s" % str(e))

    if len(req.text) == 0:
        raise errors.MissingDataError("URL contains no data.")

    return req.iter_lines()


def create_key(header):
    h_split = header.split(",")
    tmp = zip(h_split, range(len(h_split)))
    return dict(tmp)


def create_header(dt):
    header = ""
    header += dt.strftime("%Y-%m-%d %H:%M:%S (%A)")
    header += os.linesep

    return header


def format_data(key, data):
    d_split = data.split(",")

    try:
        location = d_split[key["Name"]]
        altitude = d_split[key["Altitude (m)"]]
    except Exception as e:
        raise errors.InvalidDataError("Data format error: %s" % str(e))

    altitude = "unknown" if altitude == "null" else altitude

    return "%s has an altitude of %s meters." % (location, altitude)


def main():
    try:
        args = handle_args(sys.argv[1:])
        if args.url:
            lines = get_http_data(args.url)
        else:
            lines = get_file_data(args.file)

        header = next(lines)
        key = create_key(header)

        now = datetime.now()
        print(create_header(now))

        for line in lines:
            if line:
                print(format_data(key, line))

        return 0

    except Exception as e:
        print("Error: %s" % str(e), file=sys.stderr)
        return -1


def cli():
    sys.exit(main())


if __name__ == "__main__":
    cli()
