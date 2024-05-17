from src.meltdown import HtmlProducer, MarkdownParser
from src.meltdown.Nodes import *
from typing import Self
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


def test_extend_default_bold():
    class CustomHtmlProducer(HtmlProducer):
        def visit_bold(self: Self, node: BoldNode):
            self._output += "<b>"
            for child in node.children:
                child.accept(self)
            self._output += "<b>"

    doc = MarkdownParser().parse("# Hello **friends**!")
    html = CustomHtmlProducer().produce(doc)
    assert "<h1>Hello <b>friends<b>!</h1>" in html
