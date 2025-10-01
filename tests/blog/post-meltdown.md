---
title: Meltdown: The story of a markdown parser
date: 2024-05-21
description: Building a markdown parser for fun.
---

<!-- Start writing your markdown here ;) -->

## Getting nerd-sniped
A couple of weeks back my friend [Luis](https://lprod.dev/) 
asked me how my blog works and once I
told him that I wrote a custom (very simple) static site generator, he got
excited and started to build his own. 

> **🦜 Chirpy the Parrot:** Couldn't you just use an existing solution like [substack](https://substack.com/) or [bearblog](https://bearblog.dev/)?

Of course, and that's also what I told him, however as developers we love to 
build stuff and it's not always about getting the easiest solution but about 
the fun of building stuff.

Anyway, a couple of days later I got a message which as a compiler engineer
scared me:

![Chat with friend](chat1.png)

Well, there was only one obvious next step: Building a proper markdown parser 
and recording my-self doing so that he can learn more about parsers 😝.

## Wait ... why not regex?

If you don't spend all day thinking about grammars, LL(1)-conflicts and the 
advantages of right-recursion over left-recursion you might be wondering why 
I was so terrified by the attempt to parse markdown with regex.

The simple answer is that regular expression can only express regular languages 
but most languages like Markdown are context-free. In less fancy terms this 
means that regex just isn't strong enough to understand Markdown.

I think about it in the terms that while regex can count it cannot remember previous
counters. For example, the following regex can accept one to five opening 
parenthesis and one to five closing ones. 

```regex
\({1-5}\){1-5}
```

However, it doesn't enforce that all opening ones have a matching closing one and there
is no way to express that in a regex.

<!-- FIXME: I want code blocks in quotes -->

> **🦜 Chirpy the Parrot:** actually you can express it with: `\((\((\((\((\(()?\))?\))?\))?\))?\)`

Yes, Chirpy you are correct, as long as all counts are finite, we can express it 
with a hideous regular grammar, however we often don't want to limit us to an upper 
limit. Also, even if Markdown would enforce upper limits, I would argue that it
easier to write a recursive decent parser than such regex.

## Parsing markdown is ~~hard~~ _different_

Before getting lost in the weeds of consuming tokens and unexpected EOFs, we 
first need to address the most important question: what to name our baby. And 
this is especially hard when the competition is so strong with great hits like 
[sundown](https://github.com/vmg/sundown), 
[marked](https://github.com/markedjs/marked),
[parsedown](https://github.com/erusev/parsedown) and 
[redcarpet](https://github.com/vmg/redcarpet). However, I quickly discovered 
that **meltdown** doesn't have a prominent entry, which is just a wrong that 
needs to be corrected. As a bonus the package name was also free on 
[PyPI](https://pypi.org/) and to be honest I just like the confidence it emits. 


With a great name at hand, I fired up VSCode and OBS and started writing a 
simple recursive decent 
parser. While there is no official Markdown spec the most common is 
[CommonMark](https://commonmark.org/), since I am more comfortable with GitHub 
flavored markdown, I implemented something along those lines. The goal is
to learn more about parsers anyway.

Pretty soon I discovered a pretty big difference between parsing Markdown and
other programming languages, with which I had more experience: **there are no 
errors in Markdown**.

This means if you come across a _malformed_ rule you just decide to interpret it 
as something else. For example, if the bold start `**` is never closed than we
just interpret it as text and not as formatting.

Unfortunately, this leads to quite some ugly code where we cannot insert a 
node into our tree until we also found a matching closing tag, and 
otherwise need to insert the opening tag as text.

```python
def _parse_strikethrough(self: Self) -> list[Node]:
    self._inside_strikethrough = True
    children = self._parse_rich_text()
    self._inside_strikethrough = False

    if not self._match("~~"):
        # No closing tag found, insert start as text
        return [TextNode("~~")] + children

    return [StrikeThroughNode(children)]
```

This isn't too bad. However, sometimes we don't want to parse something as rich 
text but as unformatted raw input. For example, take inline code, once a backtick
appears we parse everything until the next backtick as code and not as richtext.
If however, no closing backtick appears we need to insert the initial backtick 
as text and go back (rewind) and parse the following content again, but now as rich text.

```python
    def _parse_code(self: Self) -> Node:
        start_index = self._index
        stop_symbols = ["`", "\n", "\0"]
        code = self._consume_till(stop_symbols)

        if not self._match("`"):
            # Malformed input, rewind
            self._index = start_index
            return TextNode("`")

        return CodeNode(code)
```

Other than this, meltdown was quite easy to implement. During the implementation I 
often tried some edge-cases in other parsers like 
[try.pandoc.org](https://try.pandoc.org) which really helped. Meltdown still 
isn't the cleanest implementation but it has quite a few tests and a somewhat 
simple API to use:

```python
from meltdown import MarkdownParser, HtmlProducer

doc = MarkdownParser().parse("# Hello **friends**!")
html = HtmlProducer().produce(doc)
print(html)
```

## Introducing meltdowns cousin: markberg

I recorded myself during the first two hours of meltdowns development and 
explained as I went along. At that point the 
parser could parse bold, italics and headers and could convert it to html. 

> **🦜 Chirpy the Parrot:** Where is the Youtube link?

Well, I am not that great on camera yet, there are minutes of dead time where I 
debug stuff, sometimes some German slips out and at some points I was 
frustrated and used profanities. Nothing too bad but also nothing I want to be 
on the internet forever.

However, if you are interested to learn more about parsers, interpreters and 
compilers, I cannot recommend [Crafting Interpreters](https://craftinginterpreters.com/)
enough. 

Anyway, those two videos were enough for Luis to get started on his own markdown 
parser, which he lovingly called **markberg**. Since he started out with the same base, both parsers have quite a few things in common. However, Markberg surpassed Meltdown's development quite quickly.

Currently all of [Luis's blog posts](https://lprod.dev/) (well at the time of writing there is only 
one but I am sure more will come) are rendered with markberg. But what's more
important is that I could demystify parsers for a friend.

## Porting my blog to meltdown

As I mentioned in the beginning my blog uses a super small (single file) 
custom static site generator. The script previously shelled out to [pandoc](https://pandoc.org/) which
converted the markdown to html. 

Now with a self-written markdown parser this didn't seem like the right solution
anymore. So I expanded the markdown parser to be able to handle all my blog posts without 
needing to modify them, published meltdown on PyPI and converted my static site 
generator.

Which means that the article you are reading right now was parsed and converted 
to HTML by meltdown. 
I don't know if it will stay this way forever, it very well might be that 
someday I'll want to use a complex Markdown feature without messing around with 
my parser first, and I'll switch it out again. But for now, this seems like a 
fun side project.

You can find meltdown on [GitHub](https://github.com/flofriday/meltdown) and 
[PyPI](https://pypi.org/project/meltdown/). It still doesn't handle all 
cases, but if you want an _"understandable in an afternoon"️_ small parser with a 
lot of low hanging fruit for contribution it might be the right choice for you.