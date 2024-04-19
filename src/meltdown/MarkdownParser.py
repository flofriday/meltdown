from dataclasses import dataclass
from typing import Self
from src.meltdown.Nodes import (
    BoldNode,
    EmphNode,
    HeaderNode,
    MarkdownTree,
    ParagraphNode,
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

        # Do magic here
        blocks = self._parse_blocks()

        return MarkdownTree(blocks)

    def _parse_blocks(self: Self) -> list[Node]:
        children: list[Node] = []
        while not self._is_eof():
            self._stop_newline = False
            self._inside_emph = False
            self._inside_bold = False

            if self._isHeaderStart():
                counter = 0
                while self._match("#"):
                    counter += 1
                children.append(self._parse_header(counter))

            else:
                children.append(self._parse_paragraph())

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

            if self._peek() == "\n":
                if self._stop_newline:
                    self._consume()
                    break

                if self._peekn(1) == "\n":
                    self._consume()
                    self._consume()
                    break

                if self._peekn(1) == "#":
                    self._consume()
                    break

            self._consume()

        if end_index is None:
            end_index = len(self._source) - 1
        if end_index > start_index:
            text = self._source[start_index:end_index]
            children.append(TextNode(text))
        return children

    def _parse_bold(self: Self) -> [Node]:
        self._inside_bold = True
        children = self._parse_rich_text()

        if self._match("**"):
            self._inside_bold = False
            return [BoldNode(children)]

        return [TextNode("**")] + children

    def _parse_emph(self: Self) -> [Node]:
        self._inside_emph = True
        children = self._parse_rich_text()

        if self._match("*"):
            self._inside_emph = False
            return [EmphNode(children)]

        return [TextNode("*")] + children

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
