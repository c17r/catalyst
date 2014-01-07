import sys
import os
from datetime import datetime


def get_data(filename):
    lines = [l.rstrip() for l in open(filename, "r")]
    return lines


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
    now = datetime.now()
    print create_header(now)

    lines = get_data("mountains-1.csv")
    key = create_key(lines[0])
    del lines[0]

    for line in lines:
        print format_data(key, line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
