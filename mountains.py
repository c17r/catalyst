import sys
from datetime import datetime


def get_data(filename):
    lines = [l.rstrip() for l in open(filename, "r")]
    return lines


def create_key(header):
    h_split = header.split(",")
    tmp = zip(h_split, range(len(h_split)))
    return dict(tmp)


def main():
    now = datetime.now()
    print now.strftime("%Y-%m-%d %H:%M:%S (%A)")
    print ""

    lines = get_data("mountains-1.csv")
    key = create_key(lines[0])
    del lines[0]

    for line in lines:
        data = line.split(",")
        location = data[key["Name"]]
        altitude = data[key["Altitude (m)"]]
        altitude = "unknown" if altitude == "null" else altitude
        print "%s has an altitude of %s meters." % (location, altitude)

    return 0


if __name__ == "__main__":
    sys.exit(main())
