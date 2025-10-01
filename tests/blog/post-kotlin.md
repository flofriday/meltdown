---
title: 50uL Shades of Kotlin: Why your numbers long for color
date: 2025-09-04
image: some_image_for_social_preview.png
description: This is just a new post.
draft: true
---

Recently I was investigating some bug in my branch of the Kotlin compiler and suddenly I had a hunch that my code probably was confused by some inlining. So to quickly verify that idea, my muscle memory rushed me to the already open tab of [*Compiler Explorer*](https://godbolt.org/).



That's weird, the code is correct, the compiler ran, I see the bytecode that confirms that inlining takes place which will be a cause for many future headaches but I already don't care about that anymore. Why doesn't Godbolt correctly highlight `3uL`?

Well at least there is still the trusty [Kotlin Playground](https://play.kotlinlang.org/), let's paste it in there and voilà – _WHAT?_ Even that doesn't highlight the suffix?

Ok back to [IntelliJ IDEA](https://www.jetbrains.com/idea/), I **need** to see at least one colored number literal, and luckily the most common IDE for Kotlin does do it right.

## What's going on here?

It's safe to assume that Compiler Explorer with such a wide array of supported languages and a huge pile of other difficult problems to solve (like [92 million yearly compilations](https://xania.org/202506/how-compiler-explorer-works)) doesn't maintain it's own language parsing and code editing framework. So let's grab our trenchcoat and magnifier glass and cosplay as the world's most famous detective.

_Right click -> Inspect -> Scroll -> Click -> Scroll_ ... and there we have the culprit, [*Manaco - The Editor of the Web*](https://microsoft.github.io/monaco-editor/).
A quick google search later and on the Monaco Playground we can verify that indeed the bug seems to originate from here.

Glancing over the [ReadMe](https://github.com/microsoft/monaco-editor?tab=readme-ov-file#faq) we find the following interesting section:

> The Monaco Editor is generated straight from VS Code's sources with some [...]

_Wait_ does that mean, that the bug actually originates from VS Code?

Well ... no. While the Monaco Core does call the VSCode repo it's home, it doesn't contain the highlighting code, so the bug is isolated to Monaco. This also means that while Monaco is able to highlight Kotlin, vanilla VSCode without plugins isn't.

Going though a similar investigation sprint for Kotlin Playground we find that
here too, they depend on an open source solution, but in this case it's [*CodeMirror*](https://codemirror.net/).

## A quick deep dive into Kotlin's number literals

> **🦜 Chirpy the Parrot:** So what's so hard about Kotlin literals?

Well, nothing here is inherently *hard*, many other languages, like Java, have a similar level of complexity, but to my knowledge it does have some _oddeties_ I haven't seen in many languages.

But let's start at the beginning, there are 4 ways to write a number literal:

```kotlin
val float = 1.23
val dec = 123
val hex = 0xff80
val bin = 0b101010
```

As you can see like C and Java it has floating point and binary and hex notations, with the later two requiring a prefix (the casing doesn't matter and so `0Xff80` would also be fine here.)

For floats the only allowed suffix is `f`. By default all numbers are doubles and if you need to force a reduced width you can add this, but often you don't have to care about this since type-inference can figure it out for you.

```kotlin
val strudel = 1.23      // this is actually a double
val kuchen  = 1.23f     // this is a float
val melange = 123f      // Also a float
```

Since float literals are doubles by default there is no need for, and no way to, express double literals with a suffix.

For decimal, hexadecimal and binary literals you can also add the suffix `u` or `U` to make them unsigned (a somewhat newer feature introduced in Kotlin 1.5, May 2021) and `L` to make them long. Note here that the lower case `l` isn't allowed.

```kotlin
val a = 123u        // Unsinged Int
val b = 123U        // Unsigned Int
val c = 123L        // Long
val d = 123uL       // Unsigned Long
val e = 123UL       // Unsigned Long

val fixned = 123l   // Error: Use 'L' instead of 'l'.
```

> **🦜 Chirpy the Parrot:** This code doesn't look quite right. Why is it so ... _colorless_?

Well well well, guess who relied on an open-source solution for his blog's code highlighting?

Since Kotlin 1.1 you can also use underscores inside nunbers to seperate them (but they must appear in the middle):

```kotlin
val million = 1_000_000
val red = 0xFF_00_00
val twoBytes = 0b01100101_11010101
val longSpace = 1__3
```

It's also important to mention that leading zero's aren't allowed for decimal
literals.

```kotlin
// These are ok
val zero = 0
val floatingZero = 0.0
val floatSuffix = 0000f
val longZero = 0L
val binary = 0b000
val hex = 0x000

// These aren't
val twoZeros = 00
val may = 05
```

We're almost done, but floating points can also directly start with a dot or can contain the _E Noation_.

```kotlin
val x = .123
val 1.2e+3
```

I know this whole paragraph wasn't quite the formal notation you might be used to, so if you're the kind reasonable workaholic who reads EBNF grammar in their free time you can also dive in to the [Kotlin Specification](https://kotlinlang.org/spec/pdf/kotlin-spec.pdf) (section 1.2.3 Literals) that has that.

Or if for some sick reason you prefer a massive regex:

```text
0[xX][0-9a-fA-F]([_0-9a-fA-F]*[0-9a-fA-F])?[uU]?L?|
0[bB][01]([_01]*[01])?[uU]?L?|
\.[0-9]([_0-9]*[0-9])?([eE][+-]?[0-9]([_0-9]*[0-9])?)?[fF]?|
(([0-9]([_0-9]*[0-9])?)(\.[0-9]([_0-9]*[0-9])?)?)(([eE][+-]?[0-9]([_0-9]*[0-9])?)[fF]?|[fF])|
(0|[1-9]([_0-9]*[0-9])?)([uU]?L?)
```

![Regex Graph](regex.png)

_Yikes!_

You can say a lot good things about Regex but it won't win any prices for readability. Luckily, I wrote that one for _Other Reasons™_ (aka. foreshadowing) so stick with the grammar if you need to be sure.

## Bad highlighting all the way down

Ok so we investigated two out of two open source solutions and they get Kotlin's
number literals wrong. That seems pretty unlikely. _What are the odds of that?_

So far I stumbled across the higlighting problem by accident, but to see if it's a broader problem it would be much easier to to have an test file we can past into each. Obviously, I could also always dig into the codebase and compare that to the mental model I have in my head, but having an exhaustive test-set to copy and paste isn't just less error-prone but also much quicker to validate. So I took the original grammar from the spec and instead of using it to create a parser I wrote a [generator for valid literals](https://gist.github.com/flofriday/1ff27a1324a3fa92c5a614e46b43dd37).

After manifesting some utility functions into existance, the generator code ended up looking remarkibly similar to the EBNF grammar it implemented, making it easy to verify for correctness. As a side note I'm a big fan of copying the spec into sourcecode.

```kotlin
/**
 * Grammar:
 * [DecDigits] '.' DecDigits [DoubleExponent]
 * | DecDigits DoubleExponent
 */
fun doubleLiteral(): List<String> =
    either(
        optional(decDigits())
            .add(".")
            .add(decDigits())
            .optional(doubleExponent()),
        decDigits()
            .add(doubleExponent())
    )
```

With my cute 3k lines of testcases (I might have overdone it just a little) it was quite easy to quickly get a rough overview _if_ and _where_ the issues in a highlighter might be.

As a next reasonable step I went on a fever dream like rampage pasting that snippet into any code editor and highlighter library demo page I could think of.

Actually, this reminds me of another point, if you ever find yourself mainting a highlighter 1) good luck with rejecting a never-ending stream of unsoliceted PRs for languages with a single digit userbase, even when represented in binary format and 2) please let me try your library in the browser. With the current state of WASM and basically free hosting with GitHub pages there is almost no excuses not to. I know that it might be impractically slow and the bundle might be too large for production-use but when I'm _shopping_ for a highlighter my first priority is it's quality and an interactive demo lets me figure that out so much faster.

After the initial high of pasting that code into everything I walked away with two realizations. First, while there are a lot of editors, libraries etc that do highlighting, there aren't

From there it was mostly a task of grepping through the codebase for any mention of Kotlin finding the code responsible and adjusting it as needed.

<!-- So from the rules above I patched together a simple file with a handful of test cases and pasted it into any highlighting library I could get my hands on. Which in the end allowed me to produce this little gallery of bad highlights.
 -->
<!-- _TODO_

- CodeMirror
- Monaco
- highlight.js
- prism.js
- rainbow.js
- pygments
- rouge (is good)
- treesiter
- shiki
- sublime text
- bat -->

## All numbers have the literal right to be highlighted

> **🦜 Chirpy the Parrot:** Buhu, all the free open source software that you use on a daily basis has a minor bug. So what ya gonnna do about it?

I guess it's time to get our hands dirty and contribute back.

<!--
As a good open-source loving person that used most many of the libraries mentioned above (directly or indirectly) there is really only thing to do: **Fixing the problem**.
-->
<!--
Till now I used to play around to with each highlighter until I find a problem, but if we are going to fix them it would be really useful to have a test-set. Obviously, I could also always dig into the codebase and compare that to the mental model I have in my head, but having an exhaustive test-set to copy and paste isn't just less error-prone but also much quicker to validate. So I took the original grammar from the spec and instead of using it to create a parser I wrote a [generator for valid literals](https://gist.github.com/flofriday/1ff27a1324a3fa92c5a614e46b43dd37).

With a few utility functions that map closely to EBNF grammar the Kotlin code looked remarkably similar to the the grammar, making it easy to verify the correctness.

```kotlin
/**
 * Grammar:
 * [DecDigits] '.' DecDigits [DoubleExponent]
 * | DecDigits DoubleExponent
 */
fun doubleLiteral(): List<String> =
    either(
        optional(decDigits())
            .add(".")
            .add(decDigits())
            .optional(doubleExponent()),
        decDigits().add(doubleExponent())
    )
```

With my cute 3k lines of testcases (I might have overdone it just a little) it was quite easy to quickly get a rough overview _if_ and _where_ the issues in a highlighter might be. From there it was mostly a task of grepping through the codebase for any mention of Kotlin finding the code responsible and adjusting it as needed -->

While I already had a complete regex for a correct parsing and most libraries do use regex for lexing (which is a totally valid for lexing) I didn't just paste it in there. Some project had only a quite simplistic approach and there it made sense to replace the little they had with a more sophisticated one, but others did only lack some corner cases so there I tried the least invasive approach and only made changesonly changes where it was necessary.

The regular grammar I showed mentioned last chapter is correct but, there are some valid reasons why you want to accept false-positives on purpose. This especially applies to editors where you might want to allow incomplete literals so that when the user types it is already highlighted as it might _feel_ laggy when the editor only caughs up once you are done typing.

```kotlin
// Correct literals
val full = 1_2
val octal = 0xf

// Incomplete literals,
// but we might already highlight it while they are typing
val partial = 1_
val partialOct = 0x
```

For such behaivor I decided on a case by case basis what the current status qou was in for each project.

So finally we end up with a short list of completed PRs – that I promise to keep updating but eventually will propperly forget – and a longer backlog for eventual _nerd-sniping_:

- [Monaco](https://github.com/microsoft/monaco-editor/pull/4973)
- [CodeMirror](https://github.com/codemirror/legacy-modes/pull/23)
- [highlight.js](https://github.com/highlightjs/highlight.js/pull/4307)
- [Pygments](https://github.com/pygments/pygments/pull/2961)
- _prism.js_
- _treesiter_
- _shiki_
- _sublime text_
- _bat_

> **🦜 Chirpy the Parrot:** So what did they get wrong about Kotlin's number parsing?

Well, since Kotlin (especially in the beginning) was so closely related to Java, many projects either reused that parser directly or were heavily insipired by it. Quite often this lead to them accepting invalid code like the `d` and `D` suffixes.

Some syntax was only later introduced, like the `u` and `U` suffixes for unsinged numbers in Kotlin 1.5 and with some of the highlighters supporting about 200 languages changes like that can simply slip under the radar.

And sometimes your educated guesses can be wrong. All prefixes and suffixes are case independent except for the long suffix `L` where only the uppercase is valid.

Also parsing is hard, having implemented a couple of fixes, the same regex might work for one highlighter but fail in another as they use a different regex-engine that either has less features or is to greedy and doesn't backtrack far enough.

> **🦜 Chirpy the Parrot:** What we really needed is a new standard language grammars to rule them all, so that every language has only one implementation, one source of truth.

Yes in theory that would been awesome, but there are good reason for wanting a custom implementation. For example editors need to deal with broken inputs (while the developer is typing) while some other highlighters of static content might decide against it so that the user doesn't even need to copy the code from Stackoverflow into their IDE as it is visibly broken.

However, there are a _some_ quasi standards, many highlighters reuse TextMate grammars or TreeSitter grammars. One library for Go, [chroma](https://github.com/alecthomas/chroma) parses the Python soucecode of [Pygments](https://pygments.org/) to generate it's own (admitedly similar) grammar files.


A notable mention in all of this, however is [Rouge](https://rouge.jneen.net/) a highlighting that did handle everything I threw at it and has an implementation that is remarkably close to the official Kotlin grammar.

## Remarks

While this post mostly highlights issues (pun intended) in open source libraries it's not my intention to blame anyone here. Many of them do support a huge amount of languages and keeping up with syntax changes is impossible for what if often just a side project of a single person.

Instead, I want to thank you, for making it so much easier communicate about code (especially for those of us with dyslexia).

I want to take this space of unused internet realestate to thank my friends for the alternative titles they suggested. They made me laugh pretty hard so you might enjoy them too:

- 50 Shades of Kotlin: Your Code is missing color
- From 0L to Hero: Fixing Kotlin number highlighters
- All Number literals have a right to be highlighted
- Number literal(ly) broken: What syntax highlighters get wrong
- Fixing Kotlin number highlighters with this one simple trick; Developers are shocked!
