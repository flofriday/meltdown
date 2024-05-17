import html
from typing import Self
from .Nodes import (
    BoldNode,
    CodeBlockNode,
    CommentNode,
    QuoteBlockNode,
    CodeNode,
    EmphNode,
    HeaderNode,
    ImageNode,
    LinkNode,
    MarkdownTree,
    MarkdownVisitor,
    ParagraphNode,
    StrikeThroughNode,
    TextNode,
)


class HtmlProducer(MarkdownVisitor):
    def __init__(self) -> None:
        self._output: str = ""

    def produce(self: Self, ast: MarkdownTree) -> str:
        self._output = ""
        self.visit_tree(ast)
        return self._output

    def visit_tree(self: Self, node: MarkdownTree):
        for child in node.children:
            child.accept(self)

    def visit_paragraph(self: Self, node: ParagraphNode):
        self._output += "<p>"
        for child in node.children:
            child.accept(self)
        self._output += "</p>\n"

    def visit_header(self: Self, node: HeaderNode):
        self._output += f"<h{node.header_size}>"
        for child in node.children:
            child.accept(self)
        self._output += f"</h{node.header_size}>\n"

    def visit_code_block(self: Self, node: CodeBlockNode):
        self._output += "<pre"
        if node.language is not None:
            self._output += f' class="{node.language}"'
        self._output += "><code>"
        self._output += html.escape(node.code)
        self._output += "</code></pre>\n"

    def visit_quote_block(self: Self, node: QuoteBlockNode):
        self._output += "<blockquote>"
        for child in node.children:
            child.accept(self)
        self._output += "</blockquote>"

    def visit_emph(self: Self, node: EmphNode):
        self._output += "<em>"
        for child in node.children:
            child.accept(self)
        self._output += "</em>"

    def visit_strikethrough(self: Self, node: StrikeThroughNode):
        self._output += "<del>"
        for child in node.children:
            child.accept(self)
        self._output += "</del>"

    def visit_bold(self: Self, node: BoldNode):
        self._output += "<strong>"
        for child in node.children:
            child.accept(self)
        self._output += "</strong>"

    def visit_code(self: Self, node: CodeNode):
        self._output += f"<code>{html.escape(node.code)}</code>"

    def visit_link(self: Self, node: LinkNode):
        # FIXME: escape url
        self._output += f'<a href="{node.url}">'
        for child in node.children:
            child.accept(self)
        self._output += "</a>"

    def visit_image(self: Self, node: ImageNode):
        # FIXME: escape url
        self._output += f'<img src="{node.url}" alt="{html.escape(node.description)}"/>'

    def visit_text(self: Self, node: TextNode):
        self._output += html.escape(node.text.replace("\n", " "))

    def visit_comment(self: Self, node: CommentNode):
        self._output += "<!--" + node.comment + "-->"
