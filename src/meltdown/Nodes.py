from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Self, TypeVar

T = TypeVar("T")


class Node(ABC):
    @abstractmethod
    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        pass

    @abstractmethod
    def dump(self: Self, indent: int = 0) -> str:
        pass


@dataclass(slots=True)
class MarkdownTree:
    metadata: dict[str, str]
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_tree(self)

    def dump(self: Self) -> str:
        out = f"MarkdownTree metadata:{self.metadata}\n"
        for child in self.children:
            out += child.dump(1)
        return out

    def render(self: Self, renderer: "Renderer | None" = None) -> str:
        if renderer is None:
            from .HtmlRenderer import HtmlRenderer

            renderer = HtmlRenderer()
        return renderer.render(self)


@dataclass(slots=True)
class ParagraphNode(Node):
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_paragraph(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "Paragraph\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out


@dataclass(slots=True)
class HeaderNode(Node):
    header_size: int
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_header(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + f"HeaderNode size:{self.header_size}\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out


@dataclass(slots=True)
class CodeBlockNode(Node):
    language: str | None
    code: str

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_code_block(self)

    def dump(self: Self, indent: int = 0) -> str:
        # FIXME: The code should be better formatted here.
        return (
            " " * indent * 4
        ) + f'CodeBlock language:{self.language} code:"{self.code}"\n'


@dataclass(slots=True)
class QuoteBlockNode(Node):
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_quote_block(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "QuoteBlockNode\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out


@dataclass(slots=True)
class ListItemNode(Node):
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_list_item(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "ListItemNode\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out


@dataclass(slots=True)
class UnorderedListNode(Node):
    items: list[ListItemNode]

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_unordered_list(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "UnorderedList\n"
        for item in self.items:
            out += item.dump(indent + 1)
        return out


@dataclass(slots=True)
class EmphNode(Node):
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_emph(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "EmphNode\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out


@dataclass(slots=True)
class StrikeThroughNode(Node):
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_strikethrough(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "StrikeThroughNode\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out


@dataclass(slots=True)
class BoldNode(Node):
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_bold(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + "BoldNode\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out


@dataclass(slots=True)
class CodeNode(Node):
    code: str

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_code(self)

    def dump(self: Self, indent: int = 0) -> str:
        return (" " * indent * 4) + f"CodeNode code:'{self.code}'\n"


@dataclass(slots=True)
class LinkNode(Node):
    url: str
    children: list[Node]

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_link(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (" " * indent * 4) + f"LinkNode url: {self.url}\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out


@dataclass(slots=True)
class ImageNode(Node):
    url: str
    description: str

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_image(self)

    def dump(self: Self, indent: int = 0) -> str:
        out = (
            " " * indent * 4
        ) + f"ImageNode url: {self.url}, description: '{self.description}'\n"
        return out


@dataclass(slots=True)
class TextNode(Node):
    text: str

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_text(self)

    def dump(self: Self, indent: int = 0) -> str:
        return (
            " " * indent * 4
        ) + f'TextNode "{self.text.replace("\n", r"\n").replace("\t", r"\t")}"\n'


@dataclass(slots=True)
class CommentNode(Node):
    comment: str

    def accept(self: Self, visitor: "MarkdownVisitor[T]") -> T:
        return visitor.visit_comment(self)

    def dump(self: Self, indent: int = 0) -> str:
        return (" " * indent * 4) + f'CommentNode "{self.comment}"\n'


class MarkdownVisitor[T](ABC):
    @abstractmethod
    def visit_tree(self: Self, node: MarkdownTree) -> T:
        pass

    @abstractmethod
    def visit_paragraph(self: Self, node: ParagraphNode) -> T:
        pass

    @abstractmethod
    def visit_header(self: Self, node: HeaderNode) -> T:
        pass

    @abstractmethod
    def visit_code_block(self: Self, node: CodeBlockNode) -> T:
        pass

    @abstractmethod
    def visit_quote_block(self: Self, node: QuoteBlockNode) -> T:
        pass

    @abstractmethod
    def visit_unordered_list(self: Self, node: UnorderedListNode) -> T:
        pass

    @abstractmethod
    def visit_list_item(self: Self, node: ListItemNode) -> T:
        pass

    @abstractmethod
    def visit_emph(self: Self, node: EmphNode) -> T:
        pass

    @abstractmethod
    def visit_strikethrough(self: Self, node: StrikeThroughNode) -> T:
        pass

    @abstractmethod
    def visit_bold(self: Self, node: BoldNode) -> T:
        pass

    @abstractmethod
    def visit_code(self: Self, node: CodeNode) -> T:
        pass

    @abstractmethod
    def visit_link(self: Self, node: LinkNode) -> T:
        pass

    @abstractmethod
    def visit_image(self: Self, node: ImageNode) -> T:
        pass

    @abstractmethod
    def visit_text(self: Self, node: TextNode) -> T:
        pass

    @abstractmethod
    def visit_comment(self: Self, node: CommentNode) -> T:
        pass


class Renderer(MarkdownVisitor[str], ABC):
    def render(self: Self, doc: MarkdownTree) -> str:
        return doc.accept(self)
