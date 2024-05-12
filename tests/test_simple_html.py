from src.meltdown import HtmlProducer, MarkdownParser
import pytest


def produce(input: str) -> str:
    producer = HtmlProducer()
    return producer.produce(MarkdownParser().parse(input))


# Simple tests


def test_empty():
    src = ""
    assert produce(src) == ""


def test_text():
    src = "Hi there"
    assert "<p>Hi there</p>" in produce(src)


def test_header1():
    src = "# Big header"
    assert "<h1>Big header</h1>" in produce(src)


def test_header2():
    src = "## Smaller header"
    assert "<h2>Smaller header</h2>" in produce(src)


def test_header3():
    src = "### Even smaller header"
    assert "<h3>Even smaller header</h3>" in produce(src)


def test_header6():
    src = "###### Tiny header"
    assert "<h6>Tiny header</h6>" in produce(src)


def test_bold_double_star():
    src = "Hi **there** dude"
    assert "<p>Hi <strong>there</strong> dude</p>" in produce(src)


def test_emph_star():
    src = "I *really* like you"
    assert "<p>I <em>really</em> like you</p>" in produce(src)


def test_strike_through():
    src = "Hi ~~guys~~ people"
    assert "<p>Hi <del>guys</del> people</p>" in produce(src)


def test_link():
    src = "[Homepage](https://flofriday.dev)"
    assert '<p><a href="https://flofriday.dev">Homepage</a></p>' in produce(src)


def test_image():
    src = "![profile picture](https://flofriday.dev/flofriday.jpg)"
    assert (
        '<p><img src="https://flofriday.dev/flofriday.jpg" alt="profile picture"/></p>'
        in produce(src)
    )


def test_multiple_paragraphs():
    src = """Hello

World"""
    assert "<p>Hello</p><p>World</p>" in produce(src).replace("\n", "")
