import sys
import os
import argparse
from datetime import datetime
import requests


class RetrieveError(Exception):
    pass


class MissingDataError(Exception):
    pass


class InvalidDataError(Exception):
    pass


def cmd_line_parse():
    parser = argparse.ArgumentParser(description="""
        Retrieve the mountain data.
        Output each mountains altitude (if present).
        """)
    parser.add_argument("URL", help="URL that contains the mountain data")
    args = parser.parse_args()
    return args.URL


def get_file_data(filename):
    try:
        lines = [l.rstrip() for l in open(filename, "r")]
    except Exception as e:
        raise RetrieveError("File error: %s" % e.message)

    if len(lines) == 0:
        raise MissingDataError("File contains no data.")
    return iter(lines)


def get_http_data(url):
    try:
        req = requests.get(url)
    except Exception as e:
        raise RetrieveError("URL error: %s" % e.message)

    if len(req.text) == 0:
        raise MissingDataError("URL contains no data.")

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
        raise InvalidDataError("Data format error: %s" % e.message)

    altitude = "unknown" if altitude == "null" else altitude

    return "%s has an altitude of %s meters." % (location, altitude)


def main():

    url = cmd_line_parse()
    lines = get_http_data(url)

    header = lines.next()
    key = create_key(header)

    now = datetime.now()
    print create_header(now)

    for line in lines:
        print format_data(key, line)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (MissingDataError, RetrieveError, InvalidDataError) as e:
        print "Error: %s" % e.message
        sys.exit(-1)
