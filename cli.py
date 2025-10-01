import argparse

from meltdown import MarkdownParser
from meltdown.HtmlProducer import HtmlProducer


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
        doc = MarkdownParser().parse(f.read())

    if args.dump:
        print(doc.dump())
    else:
        print(HtmlProducer().produce(doc))


if __name__ == "__main__":
    main()
