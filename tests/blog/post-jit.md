---
title: What is a JIT compiler anyway?
date: 2022-07-06
description: My bachelor thesis is in the field of just-in-time(JIT) compiler research and while this already sounds...
image: Drawing_JIT.excalidraw.png
---

My bachelor thesis is in the field of just-in-time(JIT) compiler research and while
this already sounds very advanced (which I absolutely love) this is my attempt at
explaining it to a non technical audience.

## The _"normal"_ compiler

![Drawing AOT](Drawing_AOT.excalidraw.png)

As you probably know from movies, computers can only understand binary (ones and zeros).
Contrary to programmers and hackers in movies, we don't program in binary and just
like you cannot read binary
(well, [some can read basic binary](https://www.youtube.com/watch?v=wCQSIub_g7M),
but it's still a lot slower and I definitely can't).

So the solution is to write something in an programming language which is more
like english text. Then we use a program to translate it to the binary machine code.
The translation program is what we call a compiler.

The classical compiler is a so called ahead-of-time (AoT) compiler, which means the
developer who writes the app also runs the compiler for your machine and then
sends you the compiled binary, which your computer just takes and runs.

## The Interpreter

![Drawing Interpreter](Drawing_Interpreter.excalidraw.png)

Computers can be grouped into different Architectures where each architecture
has a different set of instructions it understands.
The most common architecture for Laptops and Desktops currently is
[x86 64bit](https://en.wikipedia.org/wiki/X86-64) and for Smartphones it is
[ARM 64bit](https://en.wikipedia.org/wiki/ARM_architecture_family).

So one disadvantage from compilers is that for each architecture and for each
Operating System you need to compile the Application. So if you want to have your
new app run on Linux, macOS and Windows for x86 and ARM you need to compile
your app 6 times.

One Solution here is to write your application in an language that is interpreted so that
you can ship the user directly the source code which they then interpret.

However, this normally results in Applications that are a lot slower
(about 40-100 times). For many use cases this is acceptable but we can still improve
this approach.

> **Note:** The speed I reference here is pure computational. However there might be many other reasons an application _feels_ slow.

## The JIT compiler

![Drawing JIT](Drawing_JIT.excalidraw.png)

To improve the performance you can compile (parts of) a program to machine code as you are about to run it. These compilers are called just-in-time(JIT) compilers. Like an interpreter you can just send the user the source code and don't have to compile it for each target. However, unlike an interpreter the application will be a lot faster.

JIT compilers are often integrated into Interpreters. The interpreter starts running a code and generates metrics about the code it runs. Once the interpreter finds a piece that gets run often it will compile this piece with a JIT compiler to machine code which is a lot faster to execute. These interpreters don't compile everything immediately to machine code because the compilation itself also takes some time and for code that isn't executed often it is faster to just interpret it than to compile it to fast machine code.

## Remarks

I have simplified many concepts here, and I could definitely geek out on very
specific details, but I hope you got an overview about the topic of my bachelor
thesis.
