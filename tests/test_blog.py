import os

import pytest
from inline_snapshot import external_file, register_format_alias

from meltdown import MarkdownParser

register_format_alias(".html", ".txt")


def get_test_cases() -> list[str]:
    """Discover all input files"""
    test_folder = "tests/blog"
    return [test_folder + "/" + f for f in os.listdir(test_folder) if f.endswith(".md")]


@pytest.mark.parametrize("input_file", get_test_cases())
def test_convert_from_files(input_file: str):
    """Test convert function using input files"""

    with open(input_file, encoding="utf-8") as f:
        markdown = f.read()

    parser = MarkdownParser()
    document = parser.parse(markdown)

    dump = document.dump()
    dump_filename = input_file.removesuffix(".md") + ".dump.txt"
    assert dump == external_file(dump_filename)

    html = document.render()
    html_filename = input_file.removesuffix(".md") + ".html"
    assert html == external_file(html_filename)
