import sys
from datetime import datetime


def get_data(filename):
    lines = [l.rstrip() for l in open(filename, "r")]
    return lines


def main():
    now = datetime.now()
    print now.strftime("%Y-%m-%d %H:%M:%S (%A)")
    print ""

    lines = get_data("mountains-1.csv")
    del lines[0]
    for line in lines:
        data = line.split(",")
        data[5] = "unknown" if data[5] == "null" else data[5]
        print "%s has an altitude of %s meters." % (data[1], data[5])

    return 0


if __name__ == "__main__":
    sys.exit(main())
