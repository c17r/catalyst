import sys


def main():
    with open("mountains-1.csv", "r") as f:
        lines = f.read()

    count = (1024 ** 3) / len(lines)

    with open("mountains-1.big", "w") as f:
        for x in range(count):
            f.write(lines)


if __name__ == "__main__":
    sys.exit(main())
