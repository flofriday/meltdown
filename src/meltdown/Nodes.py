from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self


class Node(ABC):
    @abstractmethod
    def accept(self: Self, visitor: "MarkdownVisitor"):
        pass

    @abstractmethod
    def dump(self: Self, indent: int = 0) -> str:
        pass


@dataclass
class MarkdownTree:
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor"):
        visitor.visit_tree(self)

    def dump(self: Self) -> str:
        out = "MarkdownTree\n"
        for child in self.children:
            out += child.dump(1)
        return out


@dataclass
class ParagraphNode(Node):
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor"):
        visitor.visit_paragraph(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "Paragraph\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out


@dataclass
class HeaderNode(Node):
    header_size: int
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor"):
        visitor.visit_header(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + f"HeaderNode size:{self.header_size}\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out


@dataclass
class EmphNode(Node):
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor"):
        visitor.visit_emph(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "EmphNode\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out


@dataclass
class StrikeThroughNode(Node):
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor"):
        visitor.visit_strikethrough(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "StrikeThroughNode\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out


@dataclass
class BoldNode(Node):
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor"):
        visitor.visit_bold(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "BoldNode\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out


@dataclass
class TextNode(Node):
    text: str

    def accept(self: Self, visitor: "MarkdownVisitor"):
        visitor.visit_text(self)

    def dump(self: Self, indent: int = 0) -> str:
        return (" " * indent * 4) + f'TextNode "{self.text}"\n'


class MarkdownVisitor(ABC):
    @abstractmethod
    def visit_tree(self: Self, node: MarkdownTree):
        pass

    @abstractmethod
    def visit_paragraph(self: Self, node: ParagraphNode):
        pass

    @abstractmethod
    def visit_header(self: Self, node: HeaderNode):
        pass

    @abstractmethod
    def visit_emph(self: Self, node: EmphNode):
        pass

    @abstractmethod
    def visit_strikethrough(self: Self, node: StrikeThroughNode):
        pass

    @abstractmethod
    def visit_bold(self: Self, node: BoldNode):
        pass

    @abstractmethod
    def visit_text(self: Self, node: TextNode):
        pass
