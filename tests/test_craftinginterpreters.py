# The following files were copied from the amazing blog
# https://github.com/munificent/journal/tree/master

import os

import pytest
from inline_snapshot import external_file

from meltdown import MarkdownParser

name = "craftinginterpreters"


def get_test_cases() -> list[str]:
    """Discover all input files"""
    test_folder = f"tests/{name}"
    return [test_folder + "/" + f for f in os.listdir(test_folder) if f.endswith(".md")]


def dump_filename(input_name: str, extension: str) -> str:
    return (
        f"snapshots/{name}/"
        + os.path.basename(input_name).removesuffix(".md")
        + extension
    )


@pytest.mark.parametrize("input_file", get_test_cases())
def test_convert_from_files(input_file: str):
    """Test convert function using input files"""

    with open(input_file, encoding="utf-8") as f:
        markdown = f.read()

    parser = MarkdownParser()
    document = parser.parse(markdown)

    # dump = document.dump()
    # assert dump == external_file(dump_filename(input_file, ".dump.txt"))

    html = document.render()
    assert html == external_file(dump_filename(input_file, ".html"))
