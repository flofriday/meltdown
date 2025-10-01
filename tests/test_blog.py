import os

import pytest

from meltdown import MarkdownParser


def get_test_cases() -> list[tuple[str, str]]:
    """Discover all test case pairs (input/expect files)"""
    test_folder = "tests/blog"
    inputs = [
        test_folder + "/" + f for f in os.listdir(test_folder) if f.endswith(".md")
    ]
    expected = [f.removesuffix(".md") + ".expected.txt" for f in inputs]

    # Create empty expected files for new tests
    for expect in expected:
        if not os.path.exists(expect):
            with open(expect, "w"):
                pass

    return list(zip(inputs, expected, strict=True))


@pytest.mark.parametrize("input_file,expect_file", get_test_cases())
def test_convert_from_files(input_file: str, expect_file: str):
    """Test convert function using input/expect file pairs"""

    with open(input_file, encoding="utf-8") as f:
        markdown = f.read()

    parser = MarkdownParser()
    actual_dump = parser.parse(markdown).dump()

    if os.environ.get("GOLDEN", "").lower() in ("1", "true", "yes"):
        with open(expect_file, "w", encoding="utf-8") as f:
            f.write(actual_dump)
        pytest.skip(f"Updated golden file: {expect_file}")

    with open(expect_file, encoding="utf-8") as f:
        expected_dump = f.read()

    try:
        assert actual_dump == expected_dump, f"Test '{input_file}' failed"
    except AssertionError as e:
        with open(expect_file.replace("expected.txt", "actual.txt"), "w") as f:
            f.write(actual_dump)

        raise e
