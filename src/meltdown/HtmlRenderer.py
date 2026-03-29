import html
from typing import Self

from .Nodes import (
    BoldNode,
    CodeBlockNode,
    CodeNode,
    CommentNode,
    EmphNode,
    HeaderNode,
    ImageNode,
    LinkNode,
    ListItemNode,
    MarkdownTree,
    ParagraphNode,
    QuoteBlockNode,
    Renderer,
    StrikeThroughNode,
    TextNode,
    UnorderedListNode,
)


class HtmlRenderer(Renderer):
    def visit_tree(self: Self, node: MarkdownTree) -> str:
        return "".join(c.accept(self) for c in node.children)

    def visit_paragraph(self: Self, node: ParagraphNode) -> str:
        child_content = "".join(c.accept(self) for c in node.children)
        return "<p>" + child_content + "</p>\n"

    def visit_header(self: Self, node: HeaderNode) -> str:
        child_content = "".join(c.accept(self) for c in node.children)
        return f"<h{node.header_size}>" + child_content + f"</h{node.header_size}>\n"

    def visit_code_block(self: Self, node: CodeBlockNode) -> str:
        output = "<pre"
        if node.language is not None:
            output += f' class="{node.language}"'
        output += "><code>"
        output += html.escape(node.code)
        output += "</code></pre>\n"
        return output

    def visit_quote_block(self: Self, node: QuoteBlockNode) -> str:
        inner = "".join(c.accept(self) for c in node.children)
        return "<blockquote>" + inner + "</blockquote>"

    def visit_list_item(self: Self, node: ListItemNode) -> str:
        inner = "".join(c.accept(self) for c in node.children)
        return "<li>" + inner + "</li>\n"

    def visit_unordered_list(self: Self, node: UnorderedListNode) -> str:
        inner = "".join(c.accept(self) for c in node.items)
        return "<ul>\n" + inner + "</ul>\n"

    def visit_emph(self: Self, node: EmphNode) -> str:
        inner = "".join(c.accept(self) for c in node.children)
        return "<em>" + inner + "</em>"

    def visit_strikethrough(self: Self, node: StrikeThroughNode) -> str:
        inner = "".join(c.accept(self) for c in node.children)
        return "<del>" + inner + "</del>"

    def visit_bold(self: Self, node: BoldNode) -> str:
        inner = "".join(c.accept(self) for c in node.children)
        return "<strong>" + inner + "</strong>"

    def visit_code(self: Self, node: CodeNode) -> str:
        return f"<code>{html.escape(node.code)}</code>"

    def visit_link(self: Self, node: LinkNode) -> str:
        # FIXME: escape url
        inner = "".join(c.accept(self) for c in node.children)
        return f'<a href="{node.url}">{inner}</a>'

    def visit_image(self: Self, node: ImageNode) -> str:
        # FIXME: escape url
        return f'<img src="{node.url}" alt="{html.escape(node.description)}"/>'

    def visit_text(self: Self, node: TextNode) -> str:
        return html.escape(node.text.replace("\n", " "))

    def visit_comment(self: Self, node: CommentNode) -> str:
        return "<!--" + node.comment + "-->"
