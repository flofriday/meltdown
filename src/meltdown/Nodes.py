from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self


class Node(ABC):
    @abstractmethod
    def dump(self: Self, indent: int = 0) -> str:
        pass

    @abstractmethod
    def html(self: Self) -> str:
        pass


@dataclass
class MarkdownTree:
    children: list[Node]

    def dump(self: Self) -> str:
        out = "MarkdownTree\n"
        for child in self.children:
            out += child.dump(1)
        return out

    def html(self: Self) -> str:
        out = ""
        for child in self.children:
            out += child.html()
        return out


@dataclass
class ParagraphNode(Node):
    children: list[Node]

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "Paragraph\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out

    def html(self: Self) -> str:
        out = "<p>"
        for child in self.children:
            out += child.html()
        out += "</p>\n"
        return out


@dataclass
class HeaderNode(Node):
    header_size: int
    children: list[Node]

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + f"HeaderNode size:{self.header_size}\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out

    def html(self: Self) -> str:
        out = f"<h{self.header_size}>"
        for child in self.children:
            out += child.html()
        out += f"</h{self.header_size}>\n"
        return out


@dataclass
class EmphNode(Node):
    children: list[Node]

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "EmphNode\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out

    def html(self: Self) -> str:
        out = "<em>"
        for child in self.children:
            out += child.html()
        out += "</em>"
        return out


@dataclass
class BoldNode(Node):
    children: list[Node]

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "BoldNode\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out

    def html(self: Self) -> str:
        out = "<strong>"
        for child in self.children:
            out += child.html()
        out += "</strong>"
        return out


@dataclass
class TextNode(Node):
    text: str

    def dump(self: Self, indent: int = 0) -> str:
        return (" " * indent * 4) + f'TextNode "{self.text}"\n'

    def html(self: Self) -> str:
        return self.text
