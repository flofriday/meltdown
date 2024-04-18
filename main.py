from src.meltdown_FLOFRIDAY.MarkdownParser import MarkdownParser


blog = """# My *blog* here
Hi there 
# This thing

And another *great* one
"""
md_tree = MarkdownParser().parse(blog)
print("== DUMP ==")
print(md_tree.dump())

print("== HTML ==")
print(md_tree.html())


# MarkdownTree
#     TextNode "Hi I am "
#     BoldNode
#         TextNode " "
#         EmphNode
#             TextNode "really"
#         TextNode " excited"
#     TextNode "!"
