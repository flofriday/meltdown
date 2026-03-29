import html
from textwrap import dedent
from typing import Self

from inline_snapshot import external_file, register_format_alias, snapshot

from src.meltdown import HtmlRenderer, parse
from src.meltdown.Nodes import *

register_format_alias(".html", ".txt")


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


def test_extend_for_highlightjs():
    class CustomHtmlRenderer(HtmlRenderer):
        def visit_code_block(self: Self, node: CodeBlockNode) -> str:
            output = "<pre"
            if node.language is not None:
                output += f' class="language-{node.language}"'
            output += "><code>"
            output += html.escape(node.code)
            output += "</code></pre>\n"
            return output

    inner = parse(
        dedent("""
            # Code Examples
            look at this example here:

            ```python
            def fib(n: int) -> int:
                return fib(n-1) + fib(n-2)
            ```
        """)
    ).render(CustomHtmlRenderer())
    standalone = dedent(f"""
        <html>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/styles/default.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/highlight.min.js"></script>
        <body>
        {inner}
        <script>hljs.highlightAll();</script>
        </body>
        </html>
        """)
    assert standalone == external_file("snapshots/highlightjs.html")
