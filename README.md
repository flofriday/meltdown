# meltdown
A naive markdown parser in pure python.

**WARNING:** The library will never attempt to do any sanitization on the input. 
If used for user generated content it is highly recommended to use an external
sanitization library.

## Installation

meltdown currently only supports Python 3.12.

```bash
pip install meltdown
```

## Usage

```python
from meltdown import MarkdownParser, HtmlProducer

doc = MarkdownParser().parse("# Hello **friends**!")
html = HtmlProducer().produce(doc)

print(doc.dump())
print(html)
```

The default `HtmlProducer` is heavily inspired by [pandoc](https://pandoc.org),
however, if you are unhappy you can easily write your own producer or if only 
some formattings are unwanted override the default methods.

In the following example we change the bold formatting form `<strong>` to `<b>`:

```python
from meltdown import MarkdownParser, HtmlProducer
from meltdown.Nodes import *
from typing import Self

class CustomHtmlProducer(HtmlProducer):
    def visit_bold(self: Self, node: BoldNode):
        self._output += "<b>"
        for child in node.children:
            child.accept(self)
        self._output += "<b>"

doc = MarkdownParser().parse("# Hello **friends**!")
html = CustomHtmlProducer().produce(doc)

print(html)
```

## Run all tests

```bash
python -m pytest
```