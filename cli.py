import argparse

from meltdown import parse


def main():
    parser = argparse.ArgumentParser(
        prog="meltdown-dev-cli",
        description="A cli for developers trying meltdown",
    )
    parser.add_argument("filename", help="Name of the file being parsed and converted.")
    parser.add_argument(
        "--dump", action="store_true", help="Print the dump instead of the html."
    )
    args = parser.parse_args()
    with open(args.filename) as f:
        doc = parse(f.read())

    if args.dump:
        print(doc.dump())
    else:
        print(doc.render())


if __name__ == "__main__":
    main()
