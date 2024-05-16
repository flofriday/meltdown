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


def test_code_block():
    src = """
```golang
a := "flotschi"
x = y
```
"""
    expected = '<pre class="golang"><code>a := &quot;flotschi&quot;\nx = y</code></pre>'
    assert expected in produce(src)


def test_quote_block():
    src = "> **Note:** This isn't quite correct!"
    expected = "<blockquote> <strong>Note:</strong> This isn&#x27;t quite correct!</blockquote>"
    assert expected in produce(src)


def test_bold_double_star():
    src = "Hi **there** dude"
    assert "<p>Hi <strong>there</strong> dude</p>" in produce(src)


def test_bold_double_underline():
    src = "Hi __there__ dude"
    assert "<p>Hi <strong>there</strong> dude</p>" in produce(src)


def test_emph_star():
    src = "I *really* like you"
    assert "<p>I <em>really</em> like you</p>" in produce(src)


def test_emph_underline():
    src = "I _really_ like you"
    assert "<p>I <em>really</em> like you</p>" in produce(src)


def test_strike_through():
    src = "Hi ~~guys~~ people"
    assert "<p>Hi <del>guys</del> people</p>" in produce(src)


def test_inline_code():
    src = "Have you seen `T ** a;` in C before?"
    assert "<p>Have you seen <code>T ** a;</code> in C before?</p>" in produce(src)


def test_comment():
    src = "Have you seen the <!-- boo & woo --> ghost?"
    assert "<p>Have you seen the <!-- boo & woo --> ghost?</p>" in produce(src)


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


def test_frontmatter():
    src = """
---
author: flofriday
title : An exciting test

 date: 2024-05-16
---
# Hello there"""
    expected = "<h1>Hello there</h1>\n"
    assert expected == produce(src)

    ast = MarkdownParser().parse(src)
    assert ast.metadata == {
        "author": "flofriday",
        "title": "An exciting test",
        "date": "2024-05-16",
    }


def test_star_not_emph():
    src = "hello *there"
    assert "<p>hello *there</p>" in produce(src)


def test_underline_not_emph():
    src = "hello _there"
    assert "<p>hello _there</p>" in produce(src)


def test_underline_in_word_not_emph():
    src = "hello world_there_"
    assert "<p>hello world_there_</p>" in produce(src)


def test_doublestar_not_bold():
    src = "hello **there"
    assert "<p>hello **there</p>" in produce(src)


def test_doubleunderline_not_bold():
    src = "hello __there"
    assert "<p>hello __there</p>" in produce(src)


def test_doubleunderline_in_word_not_bold():
    src = "hello word__there__"
    assert "<p>hello word__there__</p>" in produce(src)


def test_doublewave_not_strikethrough():
    src = "hello ~~there"
    assert "<p>hello ~~there</p>" in produce(src)


def test_parenthesis_not_link():
    src = "Welcome today (13.may) at this unit test."
    assert "<p>Welcome today (13.may) at this unit test.</p>" in produce(src)


def test_brackets_not_link():
    src = "I like [angles]."
    assert "<p>I like [angles].</p>" in produce(src)


def test_missing_closing_link():
    src = "I like [examples](https://example.com."
    assert "<p>I like [examples](https://example.com.</p>" in produce(src)


def test_missing_closing_link_formatted():
    src = "I like [examples](https://**example.com**."
    assert "<p>I like [examples](https://<strong>example.com</strong>.</p>" in produce(
        src
    )


def test_unclosed_bracket_in_strikethrough():
    src = "Hi ~~[there~~"
    expected = "<p>Hi <del>[there</del></p>"
    assert expected in produce(src)


def test_unclosed_comment_in_strikethrough():
    src = "Hi ~~<!--there~~"
    expected = "<p>Hi <del>&lt;!--there</del></p>"
    assert expected in produce(src)
