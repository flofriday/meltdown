from src.meltdown import MarkdownParser


blog = """

# How to ask (me) a technical question

I love to help people solve their problems, but sometimes it is just an exhausting experience. So if someone send you this link passiv agressivley you might need to work on how you ask questions.

## 1. *You* need something
When you ask someone a question you want them to take time out of their day to help you. This means they are doing you a favour, so you should be considered of their time. Yes there is also paid support, but making the experience of helping you more pleasent will get you better results either way.

## 2. No hello
Put the question into the first message you send them. Don't just say hello and wait for them to respond, don't ask if it would be ok if you'd ask them a question. Just put the question in the first message.

Sure you can be polite but by putting the question into the first message you will get much faster responses.

[nohello.net](https://nohello.net) is a dedicated website just for this point with a lot more examples and reasons why this sucks.

## 3. Include as much relevant information as possible
Don't just tell me what went wrong, but also what you tried to do, what the output was (if there is interesting output) and where the relevant code-snipped is. 

Your question should have as much relevant information as possible, however sharing too much information is just useless. If you share a screenshot of the relevant function I might be able to debug it. But I definitly won't open a zip of the repository. Most likley because when I read your question I am on mobile and I am just not able to. But more importantly because it shows that you didn't put much effort into your question, and I just don't want to invest the time to hunt down a bug in an unknown codebase which might take a lot of time.

## 4. Consider you might be wrong
When you ask for help, you probably have a wrong understanding in how the system works. You also probably have an assumption on what happened, and you should include them in the description.  Just be careful that you also include an objective description on what actually did happen.

During my time as a tutor I had some cracy question on the levels of:
> My program keeps segfaulting because gammarays maipulate the binary, producing bad code, what to do?

Which technically could happend but most likley is nothing of the sorts but just you messing up memmory management in C. 

While theses assumption sometimes help and often are easy to figure out that they are wrong they might lead the other person on the wrong track hindering them to help you.

## 5. Sharing code right
Code ist not natural text.
If the messanger service you use has a formatting option for code with syntax highlighting, please use it. 

If it doesn't, share a screenshot of the code (I personally always prefer screenshots). And most importat with code screenshots: **include the linenumbers in the screenshot**. 

If I see that you missed a semicolon on line 23, I want to tell you exactly that. And no I won't start counting from the first line of the image or retype the line (mostly because on mobile it is really unintuitive to do so.)
"""
md_tree = MarkdownParser().parse(blog)
print("== DUMP ==")
print(md_tree.dump())

print("== HTML ==")
print(md_tree.html())

with open("out.html", "w") as f:
    f.write("<html>\n")
    f.write(md_tree.html())
    f.write("</html>\n")

# MarkdownTree
#     TextNode "Hi I am "
#     BoldNode
#         TextNode " "
#         EmphNode
#             TextNode "really"
#         TextNode " excited"
#     TextNode "!"
