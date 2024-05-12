from src.meltdown import HtmlProducer
from src.meltdown import MarkdownParser


blog = """
 Hello ~~boy~~ & **girl** dude!

x[orf](https://orf.at)xx
"""
md_tree = MarkdownParser().parse(blog)
print("== DUMP ==")
print(md_tree.dump())

print("== HTML ==")
html = HtmlProducer().produce(md_tree)
print(html)

with open("out.html", "w") as f:
    f.write("<html>\n")
    f.write(html)
    f.write("</html>\n")

# MarkdownTree
#     TextNode "Hi I am "
#     BoldNode
#         TextNode " "
#         EmphNode
#             TextNode "really"
#         TextNode " excited"
#     TextNode "!"
