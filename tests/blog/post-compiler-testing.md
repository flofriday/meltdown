---
title: Compiler testing can be even more fun actually
date: 2026-03-24
image: some_image_for_social_preview.png
description: This is just a new post.
draft: true
---


This post is mostly a response to Giacomo's amazing article [_Testing can be fun, actually_](https://giacomocavalieri.me/writing/testing-can-be-fun-actually) on snapshot testing. 

Over the last couple of months I also added snapshot testing to a couple of my projects and I'm beyond happy with the change. Not only that, but I've also noticed my behavior changing and that I intuitively added more test cases, since the burden to do so is a lot lower now. Actually my journey to snapshot testing only started _because_ I saw a talk from Giacomo, so thanks again.

All of this to say the post is amazing, go read it if you haven't yet but maybe we can improve upon this because...

## Code isn't just like any other text

One of the examples Giacomo uses is a test for Gleam's LSP and inside the Gleam compiler there are also many testcases for errors that use snapshot testing.

**img**

This is how such a test looks like for the gleam compiler. To be fair it's pretty readable but the thing that keeps bothering me is that there is no syntax highlighting and that the very LSP in my IDE doesn't recognize this file as Gleam.
And even if I force my editor to interpret the file as Gleam it won't work perfectly because the additional frontmatter at the top and the diagnostic output at the bottom doesn't make it valid gleam syntax. 

The good thing though is that nothing here is set in stone. So if we modify the snapshot framework a bit the snapshot could look like:
