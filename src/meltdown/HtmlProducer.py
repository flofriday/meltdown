import html
from typing import Self
from src.meltdown.Nodes import (
    BoldNode,
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
        self.output: str = ""

    def produce(self: Self, ast: MarkdownTree) -> str:
        self.output = ""
        self.visit_tree(ast)
        return self.output

    def visit_tree(self: Self, node: MarkdownTree):
        for child in node.children:
            child.accept(self)

    def visit_paragraph(self: Self, node: ParagraphNode):
        self.output += "<p>"
        for child in node.children:
            child.accept(self)
        self.output += "</p>\n"

    def visit_header(self: Self, node: HeaderNode):
        self.output += f"<h{node.header_size}>"
        for child in node.children:
            child.accept(self)
        self.output += f"</h{node.header_size}>\n"

    def visit_emph(self: Self, node: EmphNode):
        self.output += "<em>"
        for child in node.children:
            child.accept(self)
        self.output += "</em>"

    def visit_strikethrough(self: Self, node: StrikeThroughNode):
        self.output += "<del>"
        for child in node.children:
            child.accept(self)
        self.output += "</del>"

    def visit_bold(self: Self, node: BoldNode):
        self.output += "<strong>"
        for child in node.children:
            child.accept(self)
        self.output += "</strong>"

    def visit_link(self: Self, node: LinkNode):
        # FIXME: escape url
        self.output += f'<a href="{node.url}">'
        for child in node.children:
            child.accept(self)
        self.output += "</a>"

    def visit_image(self: Self, node: ImageNode):
        # FIXME: escape url
        self.output += f'<img src="{node.url}" alt="{html.escape(node.description)}"/>'

    def visit_text(self: Self, node: TextNode):
        self.output += html.escape(node.text.replace("\n", " "))
