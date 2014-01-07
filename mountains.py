import sys
import os
from datetime import datetime
import requests


def get_file_data(filename):
    lines = [l.rstrip() for l in open(filename, "r")]
    return iter(lines)


def get_http_data(url):
    req = requests.get(url)
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

    location = d_split[key["Name"]]
    altitude = d_split[key["Altitude (m)"]]
    altitude = "unknown" if altitude == "null" else altitude

    return "%s has an altitude of %s meters." % (location, altitude)


def main():
    url = "http://www.catalystsecure.com/public/tasks/mountains/mountains-1.csv"

    lines = get_http_data(url)

    header = lines.next()
    key = create_key(header)

    now = datetime.now()
    print create_header(now)

    for line in lines:
        print format_data(key, line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
