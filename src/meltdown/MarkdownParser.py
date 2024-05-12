from dataclasses import dataclass
from typing import Self
from src.meltdown.Nodes import (
    BoldNode,
    EmphNode,
    HeaderNode,
    ImageNode,
    LinkNode,
    MarkdownTree,
    ParagraphNode,
    StrikeThroughNode,
    TextNode,
    Node,
)


class MarkdownParser:
    def parse(self: Self, source: str):
        self._source = source
        self._index = 0
        self._stop_newline: bool = False
        self._inside_emph: bool = False
        self._inside_bold: bool = False
        self._inside_strikethrough: bool = False
        self._inside_link: bool = False

        blocks = self._parse_blocks()

        return MarkdownTree(blocks)

    def _parse_blocks(self: Self) -> list[Node]:
        children: list[Node] = []
        while not self._is_eof():
            self._stop_newline = False
            self._inside_emph = False
            self._inside_bold = False
            self._inside_strikethrough = False
            self._inside_link: bool = False

            # Skip newlines
            while self._match("\n"):
                pass

            if self._isHeaderStart():
                counter = 0
                while self._match("#"):
                    counter += 1
                if self._match(" "):
                    children.append(self._parse_header(counter))
                else:
                    children.append(self._parse_paragraph(counter))

            else:
                paragraph = self._parse_paragraph()
                if paragraph.children != []:
                    children.append(paragraph)

        return children

    def _parse_header(self: Self, header_size: int) -> HeaderNode:
        self._stop_newline = True
        children = self._parse_rich_text()
        self._stop_newline = False
        return HeaderNode(header_size, children)

    def _parse_paragraph(self: Self) -> ParagraphNode:
        children = self._parse_rich_text()
        return ParagraphNode(children)

    def _parse_rich_text(self: Self) -> list[Node]:
        children: list[Node] = []

        start_index = self._index
        while not self._is_eof():
            end_index = self._index

            if self._peek() == "*":
                # Bold, two stars
                if self._peekn(1) == "*":
                    if self._inside_bold:
                        break
                    self._consume()
                    self._consume()
                    children.append(TextNode(self._source[start_index:end_index]))
                    children += self._parse_bold()
                    start_index = self._index
                    end_index = self._index

                else:
                    # Emphasis, only one star
                    if self._inside_emph:
                        break
                    self._consume()
                    children.append(TextNode(self._source[start_index:end_index]))
                    children += self._parse_emph()
                    start_index = self._index
                    end_index = self._index

            if self._peek() == "~" and self._peekn(1) == "~":
                if self._inside_strikethrough:
                    break
                self._consume()
                self._consume()
                children.append(TextNode(self._source[start_index:end_index]))
                children += self._parse_strikethrough()
                start_index = self._index
                end_index = self._index

            if (not self._inside_link) and self._match("["):
                children.append(TextNode(self._source[start_index:end_index]))
                children += self._parse_link()
                start_index = self._index
                end_index = self._index

            if self._match("!["):
                children.append(TextNode(self._source[start_index:end_index]))
                children += self._parse_image()
                start_index = self._index
                end_index = self._index

            if self._inside_link and self._peek() == "]":
                break

            if self._peek() == "\n":
                if self._stop_newline:
                    break

                if self._peekn(1) == "\n":
                    break

                if self._peekn(1) == "#":
                    break

            self._consume()

        if end_index is None:
            end_index = len(self._source) - 1
        if self._is_eof():
            end_index += 1
        if end_index > start_index:
            text = self._source[start_index:end_index]
            children.append(TextNode(text))
        return children

    def _parse_bold(self: Self) -> list[Node]:
        self._inside_bold = True
        children = self._parse_rich_text()

        if self._match("**"):
            self._inside_bold = False
            return [BoldNode(children)]

        return [TextNode("**")] + children

    def _parse_emph(self: Self) -> list[Node]:
        self._inside_emph = True
        children = self._parse_rich_text()

        if self._match("*"):
            self._inside_emph = False
            return [EmphNode(children)]

        return [TextNode("*")] + children

    def _parse_strikethrough(self: Self) -> list[Node]:
        self._inside_strikethrough = True
        children = self._parse_rich_text()

        if self._match("~~"):
            self._inside_strikethrough = False
            return [StrikeThroughNode(children)]

        return [TextNode("~~")] + children

    def _parse_link(self: Self) -> list[Node]:
        # Parsing the text to of the link
        self._inside_link = True
        children = self._parse_rich_text()

        if not self._match("]("):
            return [TextNode("[")] + children

        # Parsing the url
        stop_symbols = [")", " ", "\n", "\t", "\0"]
        url = ""
        while self._peek() not in stop_symbols:
            url += self._consume()

        if not self._match(")"):
            return [TextNode("[")] + children + [TextNode("](" + url)]

        self._inside_link = False
        return [LinkNode(url, children)]

    def _parse_image(self: Self) -> list[Node]:
        alt_stop_symbols = ["]", "\n", "\0"]
        alt = ""
        while self._peek() not in alt_stop_symbols:
            alt += self._consume()

        if not self._match("]("):
            return [TextNode("![")] + children

        # Parsing the url
        url_stop_symbols = [")", " ", "\n", "\t", "\0"]
        url = ""
        while self._peek() not in url_stop_symbols:
            url += self._consume()

        if not self._match(")"):
            return [TextNode("![")] + children + [TextNode("](" + url)]

        return [ImageNode(url, alt)]

    def _isHeaderStart(self: Self) -> bool:
        if self._peek() != "#":
            return False

        size = 0
        while self._peekn(size) == "#":
            size += 1

        if size > 6:
            return False

        return self._peekn(size) == " "

    def _is_eof(self: Self) -> bool:
        return self._index >= len(self._source)

    def _consume(self: Self) -> str:
        if self._is_eof():
            return "\0"

        char = self._source[self._index]
        self._index += 1
        return char

    def _match(self: Self, target: str) -> bool:
        for n, c in enumerate(target):
            if c != self._peekn(n):
                return False

        for _ in target:
            self._consume()

        return True

    def _peek(self: Self) -> str:
        if self._is_eof():
            return "\0"

        return self._source[self._index]

    def _peekn(self: Self, n: int) -> str:
        if self._index + n >= len(self._source):
            return "\0"

        return self._source[self._index + n]
