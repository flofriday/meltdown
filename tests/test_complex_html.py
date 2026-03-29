from typing import Self

from inline_snapshot import snapshot

from src.meltdown import BoldNode, HtmlRenderer, parse


def produce(input: str) -> str:
    return parse(input).render()


def test_formatted_header():
    src = "## How **I *made* ~~you~~ everyone**"
    assert produce(src) == snapshot(
        "<h2>How <strong>I <em>made</em> <del>you</del> everyone</strong></h2>\n"
    )


def test_extend_default_bold():
    class CustomHtmlRenderer(HtmlRenderer):
        def visit_bold(self: Self, node: BoldNode) -> str:
            output = "<b>"
            for child in node.children:
                output += child.accept(self)
            output += "<b>"
            return output

    html = parse("# Hello **friends**!").render(CustomHtmlRenderer())
    assert html == snapshot("<h1>Hello <b>friends<b>!</h1>\n")
