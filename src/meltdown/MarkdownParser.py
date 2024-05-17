from dataclasses import dataclass
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
        self._inside_code: bool = False
        self._inside_strikethrough: bool = False
        self._inside_link: bool = False

        metadata = self._parse_frontmatter()
        blocks = self._parse_blocks()

        return MarkdownTree(metadata, blocks)

    def _parse_frontmatter(self: Self) -> dict[str, str]:
        """A incomplete yaml like frontmatter parser but it only supports top
        level fields."""

        metadata = {}
        start_index = self._index
        self._consume_while(["\n"])
        if not self._match("---"):
            return metadata

        self._consume_while(["\n", " "])

        while not self._match("---") and not self._is_eof():
            line = self._consume_till(["\n", "\0"])
            self._consume_while(["\n", " "])
            if line.strip() == "":
                continue

            parts = line.split(":")
            if len(parts) != 2:
                # Malformed frontmatter, rewind and parse as paragraph
                self._index = start_index
                return {}

            metadata[parts[0].strip()] = parts[1].strip()

        if self._is_eof():
            # Malformed frontmatter, rewind and parse as paragraph
            self._index = start_index
            return {}

        return metadata

    def _parse_blocks(self: Self) -> list[Node]:
        children: list[Node] = []
        while not self._is_eof():
            self._stop_newline = False
            self._inside_emph = False
            self._inside_bold = False
            self._inside_code = False
            self._inside_strikethrough = False
            self._inside_link: bool = False

            # Skip newlines
            self._consume_while(["\n"])

            if self._isHeaderStart():
                counter = 0
                while self._match("#"):
                    counter += 1
                if self._match(" "):
                    children.append(self._parse_header(counter))
                    continue
                else:
                    children.append(self._parse_paragraph(counter))
                    continue

            if self._match("```"):
                counter = 3
                while self._match("`"):
                    counter += 1

                children += self._parse_code_block(counter)
                continue

            if self._match(">"):
                children.append(self._parse_quote_block())
                continue

            paragraph = self._parse_paragraph()
            if paragraph.children != []:
                children.append(paragraph)

        return children

    def _parse_header(self: Self, header_size: int) -> HeaderNode:
        self._stop_newline = True
        children = self._parse_rich_text()
        self._stop_newline = False
        return HeaderNode(header_size, children)

    def _parse_code_block(self, fence_size: int) -> list[Node]:
        fence = "`" * fence_size
        start_index = self._index

        language = self._consume_till(["\n", "\0"]).strip()
        if language == "":
            language = None

        if not self._match("\n"):
            return [TextNode(fence + language)]

        code = ""
        while not self._is_eof() and not self._match(fence):
            code += self._consume()

        if self._is_eof():
            # Rewind and parse as paragraph
            self._index = start_index
            rest = self._parse_paragraph()
            rest.children = [TextNode(fence)] + rest.children
            return [rest]

        return [CodeBlockNode(language, code.strip())]

    def _parse_quote_block(self: Self) -> QuoteBlockNode:
        # FIXME: This should be able to handle headers, recursion and code
        # blocks

        self._stop_newline = True
        children = self._parse_rich_text()
        self._stop_newline = False
        self._match("\n")
        return QuoteBlockNode(children)

    def _parse_paragraph(self: Self) -> ParagraphNode:
        children = self._parse_rich_text()
        return ParagraphNode(children)

    def _parse_rich_text(self: Self) -> list[Node]:
        children: list[Node] = []

        def end_current_text():
            text = self._source[start_index:end_index]
            if text == "":
                return
            children.append(TextNode(text))

        start_index = self._index
        end_index = self._index
        while not self._is_eof():
            end_index = self._index

            if self._peek() == "*":
                # Bold, two stars
                if self._peekn(1) == "*":
                    if self._inside_bold:
                        break
                    self._consume()
                    self._consume()
                    end_current_text()
                    children += self._parse_bold("**")
                    start_index = self._index
                    end_index = self._index
                    continue

                else:
                    # Emphasis, only one star
                    if self._inside_emph:
                        break
                    self._consume()
                    end_current_text()
                    children += self._parse_emph("*")
                    start_index = self._index
                    end_index = self._index
                    continue

            if self._peek() == "_":
                if self._peekn(1) == "_":
                    if self._inside_bold and self._peekn(2) in ["\0", " ", "\t", "\n"]:
                        break

                    if self._previous() in ["\0", " ", "\t", "\n"]:
                        self._consume()
                        self._consume()
                        end_current_text()
                        children += self._parse_bold("__")
                        start_index = self._index
                        end_index = self._index
                        continue
                else:
                    if self._inside_emph and self._peekn(1) in ["\0", " ", "\t", "\n"]:
                        break

                    if self._previous() in ["\0", " ", "\t", "\n"]:
                        self._consume()
                        end_current_text()
                        children += self._parse_emph("_")
                        start_index = self._index
                        end_index = self._index
                        continue

            if self._peek() == "~" and self._peekn(1) == "~":
                if self._inside_strikethrough:
                    break
                self._consume()
                self._consume()
                end_current_text()
                children += self._parse_strikethrough()
                start_index = self._index
                end_index = self._index
                continue

            if self._peek() == "`":
                if self._inside_code:
                    break
                self._consume()
                end_current_text()
                children += self._parse_code()
                start_index = self._index
                end_index = self._index
                continue

            if (not self._inside_link) and self._match("["):
                end_current_text()
                children += self._parse_link()
                start_index = self._index
                end_index = self._index
                continue

            if self._match("!["):
                end_current_text()
                children += self._parse_image()
                start_index = self._index
                end_index = self._index
                continue

            if self._inside_link and self._peek() == "]":
                break

            if self._match("<!--"):
                end_current_text()
                children.append(self._parse_comment())
                start_index = self._index
                end_index = self._index
                continue

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

    def _parse_bold(self: Self, start_token: str) -> list[Node]:
        self._inside_bold = True
        children = self._parse_rich_text()

        if self._match(start_token):
            self._inside_bold = False
            return [BoldNode(children)]

        return [TextNode(start_token)] + children

    def _parse_emph(self: Self, start_token: str) -> list[Node]:
        self._inside_emph = True
        children = self._parse_rich_text()

        if self._match(start_token):
            self._inside_emph = False
            return [EmphNode(children)]

        return [TextNode(start_token)] + children

    def _parse_strikethrough(self: Self) -> list[Node]:
        self._inside_strikethrough = True
        children = self._parse_rich_text()

        if self._match("~~"):
            self._inside_strikethrough = False
            return [StrikeThroughNode(children)]

        return [TextNode("~~")] + children

    def _parse_code(self: Self) -> list[Node]:
        self._inside_code = True

        stop_symbols = ["`", "\n", "\0"]
        code = self._consume_till(stop_symbols)

        if not self._match("`"):
            return [TextNode("`" + code)]

        self._inside_bold = False
        return [CodeNode(code)]

    def _parse_link(self: Self) -> list[Node]:
        # Parsing the text to of the link
        self._inside_link = True
        children = self._parse_rich_text()

        if not self._match("]"):
            return [TextNode("[")] + children

        if not self._match("("):
            return [TextNode("[")] + children + [TextNode("]")]

        # Parsing the url
        stop_symbols = [")", " ", "\n", "\t", "\0"]
        url = self._consume_till(stop_symbols)

        if not self._match(")"):
            # Reset parsing position
            self._index -= len(url)
            return [TextNode("[")] + children + [TextNode("](")]

        self._inside_link = False
        return [LinkNode(url, children)]

    def _parse_image(self: Self) -> list[Node]:
        alt_stop_symbols = ["]", "\n", "\0"]
        alt = self._consume_till(alt_stop_symbols)

        if not self._match("]("):
            # resetting the parsing position
            self._index -= len(alt)
            return [TextNode("![")]

        # Parsing the url
        url_stop_symbols = [")", " ", "\n", "\t", "\0"]
        url = self._consume_till(url_stop_symbols)

        if not self._match(")"):
            # resetting the parsing position
            self._index -= len(url)
            return [TextNode("![")] + alt + [TextNode("](")]

        return [ImageNode(url, alt)]

    def _parse_comment(self: Self) -> Node:
        print("comment")
        start_index = self._index
        comment = ""
        while not self._match("-->"):
            if self._is_eof():
                # Rewind
                self._index = start_index
                return TextNode("<!--")

            comment += self._consume()

        return CommentNode(comment)

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

    def _consume_while(self: Self, symbols: list[str]) -> str:
        out = ""
        while self._peek() in symbols:
            out += self._consume()
        return out

    def _consume_till(self: Self, stop_symbols: list[str]) -> str:
        out = ""
        while self._peek() not in stop_symbols:
            out += self._consume()
        return out

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

    def _previous(self: Self) -> str:
        if self._index == 0:
            return "\0"

        return self._source[self._index - 1]
