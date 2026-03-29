from textwrap import dedent

from inline_snapshot import snapshot

from src.meltdown import MarkdownParser, parse


def produce(input: str) -> str:
    return parse(input).render()


# Simple tests


def test_empty():
    src = ""
    assert produce(src) == snapshot("")


def test_text():
    src = "Hi there"
    assert produce(src) == snapshot("<p>Hi there</p>\n")


def test_header1():
    src = "# Big header"
    assert produce(src) == snapshot("<h1>Big header</h1>\n")


def test_header2():
    src = "## Smaller header"
    assert produce(src) == snapshot("<h2>Smaller header</h2>\n")


def test_header3():
    src = "### Even smaller header"
    assert produce(src) == snapshot("<h3>Even smaller header</h3>\n")


def test_header6():
    src = "###### Tiny header"
    assert produce(src) == snapshot("<h6>Tiny header</h6>\n")


def test_code_block():
    src = """
```golang
a := "flotschi"
x = y
```
"""
    assert produce(src) == snapshot("""\
<pre class="golang"><code>a := &quot;flotschi&quot;
x = y</code></pre>
<p></p>
""")


def test_quote_block():
    src = "> **Note:** This isn't quite correct!"
    assert produce(src) == snapshot(
        "<blockquote> <strong>Note:</strong> This isn&#x27;t quite correct!</blockquote>"
    )


def test_unordered_list():
    src = dedent("""
    * Apple
    * Orange
    * Peach
    """).strip()
    assert produce(src) == snapshot("""\
<ul>
<li>Apple</li>
<li>Orange</li>
<li>Peach</li>
</ul>
""")


def test_bold_double_star():
    src = "Hi **there** dude"
    assert produce(src) == snapshot("<p>Hi <strong>there</strong> dude</p>\n")


def test_bold_double_underline():
    src = "Hi __there__ dude"
    assert produce(src) == snapshot("<p>Hi <strong>there</strong> dude</p>\n")


def test_emph_star():
    src = "I *really* like you"
    assert produce(src) == snapshot("<p>I <em>really</em> like you</p>\n")


def test_emph_underline():
    src = "I _really_ like you"
    assert produce(src) == snapshot("<p>I <em>really</em> like you</p>\n")


def test_emph_underline_special_touching():
    src = "There is _Waldo_!"
    assert produce(src) == snapshot("<p>There is <em>Waldo</em>!</p>\n")


def test_strike_through():
    src = "Hi ~~guys~~ people"
    assert produce(src) == snapshot("<p>Hi <del>guys</del> people</p>\n")


def test_inline_code():
    src = "Have you seen `T ** a;` in C before?"
    assert produce(src) == snapshot(
        "<p>Have you seen <code>T ** a;</code> in C before?</p>\n"
    )


def test_inline_single_char_code():
    src = "There is `u` and `uL` in Kotlin prefixes."
    assert produce(src) == snapshot(
        "<p>There is <code>u</code> and <code>uL</code> in Kotlin prefixes.</p>\n"
    )


def test_comment():
    src = "Have you seen the <!-- boo & woo --> ghost?"
    assert produce(src) == snapshot(
        "<p>Have you seen the <!-- boo & woo --> ghost?</p>\n"
    )


def test_link():
    src = "[Homepage](https://flofriday.dev)"
    assert produce(src) == snapshot(
        '<p><a href="https://flofriday.dev">Homepage</a></p>\n'
    )


def test_image():
    src = "![profile picture](https://flofriday.dev/flofriday.jpg)"
    assert produce(src) == snapshot(
        '<p><img src="https://flofriday.dev/flofriday.jpg" alt="profile picture"/></p>\n'
    )


def test_multiple_paragraphs():
    src = """Hello

World"""
    assert produce(src) == snapshot("""\
<p>Hello</p>
<p>World</p>
""")


def test_frontmatter():
    src = """
---
author: flofriday
title : An exciting test

 date: 2024-05-16
---
# Hello there"""
    ast = MarkdownParser().parse(src)
    assert ast.metadata == snapshot(
        {"author": "flofriday", "title": "An exciting test", "date": "2024-05-16"}
    )


def test_star_not_emph():
    src = "hello *there"
    assert produce(src) == snapshot("<p>hello *there</p>\n")


def test_underline_not_emph():
    src = "hello _there"
    assert produce(src) == snapshot("<p>hello _there</p>\n")


def test_underline_in_word_not_emph():
    src = "hello world_there_"
    assert produce(src) == snapshot("<p>hello world_there_</p>\n")


def test_doublestar_not_bold():
    src = "hello **there"
    assert produce(src) == snapshot("<p>hello **there</p>\n")


def test_doubleunderline_not_bold():
    src = "hello __there"
    assert produce(src) == snapshot("<p>hello __there</p>\n")


def test_doubleunderline_in_word_not_bold():
    src = "hello word__there__"
    assert produce(src) == snapshot("<p>hello word__there__</p>\n")


def test_doublewave_not_strikethrough():
    src = "hello ~~there"
    assert produce(src) == snapshot("<p>hello ~~there</p>\n")


def test_parenthesis_not_link():
    src = "Welcome today (13.may) at this unit test."
    assert produce(src) == snapshot(
        "<p>Welcome today (13.may) at this unit test.</p>\n"
    )


def test_brackets_not_link():
    src = "I like [angles]."
    assert produce(src) == snapshot("<p>I like [angles].</p>\n")


def test_missing_closing_link():
    src = "I like [examples](https://example.com."
    assert produce(src) == snapshot("<p>I like [examples](https://example.com.</p>\n")


def test_missing_closing_link_formatted():
    src = "I like [examples](https://**example.com**."
    assert produce(src) == snapshot(
        "<p>I like [examples](https://<strong>example.com</strong>.</p>\n"
    )


def test_unclosed_bracket_in_strikethrough():
    src = "Hi ~~[there~~"
    assert produce(src) == snapshot("<p>Hi <del>[there</del></p>\n")


def test_unclosed_comment_in_strikethrough():
    src = "Hi ~~<!--there~~"
    assert produce(src) == snapshot("<p>Hi <del>&lt;!--there</del></p>\n")


def test_start_bold():
    # There was a bug in the past where the
    src = "Hi ~~<!--there~~"
    assert produce(src) == snapshot("<p>Hi <del>&lt;!--there</del></p>\n")
