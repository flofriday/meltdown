from src.meltdown import HtmlProducer, MarkdownParser
import pytest


def produce(input: str) -> str:
    producer = HtmlProducer()
    return producer.produce(MarkdownParser().parse(input))


def test_formatted_header():
    src = "## How **I *made* ~~you~~ everyone**"
    assert (
        "<h2>How <strong>I <em>made</em> <del>you</del> everyone</strong></h2>"
        in produce(src)
    )
