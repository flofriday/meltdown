import pytest
from inline_snapshot import register_format_alias


@pytest.fixture(autouse=True)
def _inline_snapshot_file_formats() -> None:
    register_format_alias(".html", ".txt")
