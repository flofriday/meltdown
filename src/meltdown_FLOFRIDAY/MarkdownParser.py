from dataclasses import dataclass
from typing import Self
from src.meltdown_FLOFRIDAY.Nodes import (
    HeaderNode,
    MarkdownTree,
    ParagraphNode,
    TextNode,
    Node,
)


# @dataclass
class MarkdownParser:
    # index: int
    # source: str
    # children: list[Node]

    def parse(self: Self, source: str):
        self.source = source
        self.index = 0
        self._stop_newline: bool = False
        # self.children = []

        # Do magic here
        blocks = self._parse_blocks()

        return MarkdownTree(blocks)

    def _parse_blocks(self: Self) -> list[Node]:
        children: list[Node] = []
        while not self._is_eof():
            if self._peek() == "#" and self._peekn(1) == " ":
                self._consume()
                self._consume()
                children.append(self._parse_header(1))

            else:
                children.append(self._parse_paragraph())

        return children

    def _parse_header(self: Self, header_size: int) -> HeaderNode:
        # start_index = self.index
        # while not self._is_eof():
        #     # print(self.index)
        #     if self._peek() == "\n":
        #         break

        #     self._consume()

        # end_index = self.index
        # self._consume()

        # text = self.source[start_index:end_index].strip()
        self._stop_newline = True
        children = self._parse_rich_text()
        self._stop_newline = False
        return HeaderNode(header_size, children)

    def _parse_paragraph(self: Self) -> ParagraphNode:
        children = self._parse_rich_text()
        return ParagraphNode(children)

    def _parse_rich_text(self: Self) -> list[Node]:
        start_index = self.index
        end_index = None
        while not self._is_eof():
            if self._peek() == "\n":
                if self._stop_newline:
                    end_index = self.index
                    self._consume()
                    break

                if self._peekn(1) == "\n":
                    end_index = self.index
                    self._consume()
                    self._consume()
                    break

                if self._peekn(1) == "#":
                    end_index = self.index
                    self._consume()
                    break

            self._consume()

        if end_index is None:
            end_index = len(self.source) - 1
        text = self.source[start_index:end_index].strip()
        return [TextNode(text)]

    def _is_eof(self: Self) -> bool:
        return self.index >= len(self.source)

    def _consume(self: Self) -> str:
        if self._is_eof():
            return "\0"

        char = self.source[self.index]
        self.index += 1
        return char

    def _peek(self: Self) -> str:
        if self._is_eof():
            return "\0"

        return self.source[self.index]

    def _peekn(self: Self, n: int) -> str:
        if self.index + n >= len(self.source):
            return "\0"

        return self.source[self.index + n]
