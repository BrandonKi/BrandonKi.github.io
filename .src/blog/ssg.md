---
title: SSG Abomination
description: ''
author: Brandon Kirincich
date: 2024-09-27
tags:
  - Web
  - SSG
---
Using an existing Static Site Generator([SSG](https://en.wikipedia.org/wiki/Static_site_generator)) like [Jekyll](https://jekyllrb.com/) or [Hugo](https://gohugo.io/) would be no fun, so I decided to make my own from scratch.

Instead of making another run-of-the-mill, typical SSG, I decided to give myself a little challenge. Just for fun.

- Single pass Markdown parsing and HTML generation
- Less than 300 lines of, normal, non-code-golfed, Python
- No external libraries/packages
- Enough features to write high quality(debatable) blog posts

Well the product of that ended up being this ~225 LOC "[abomination](https://github.com/BrandonKi/BrandonKi.github.io/blob/main/.src/gensite.py)", the main part being the `convert2html` function.

That function, while only ~170 LOC, lexes/parses markdown and generates corresponding html all at the same time.

It uses what ended up being a state machine that uses basically no lookahead.

This led to me coming across a pretty useful pattern. (for this project, and probably nothing else!)

In Markdown "keywords" are just normal characters, and their "keywordness" depends on context. This is not unique to Markdown, many programming languages have this as well which is why you can create a variable called "final" in C++ even though it has a special meaning in some [contexts](https://en.cppreference.com/w/cpp/language/final). They use a fully featured lexer/parser though, I've done that enough, why not try something fun?

Using a Markdown example, characters that mean something special such as a "#" or a "-" which are used to create headers or lists, may or may not actually do anything depending on what context they are in, and could just be a normal character. Also to complicate it a bit more, surrounding text with parentheses or brackets *could* mean it's part of a link/image, which needs to be handled properly, or it should just be handled like normal characters. It's not just characters that can be *consumed* at a later point, it's also whole portions of text.

Since I'm generating the HTML while parsing and can't revise previously output HTML, I need to save 

My solution ended up being the following:
- collect all potentially special characters, and mark them as unconsumed
- if I find a new special character that consumes a previously unconsumed character then generate code
- adjust the state of the parser depending on consumed characters, examples would be parsing part of a link, image, bulleted list, etc.

#### Example

I highly recommend never doing any of this, but here's a small example of what the code ends up looking like.

Also, the "no-lookahead" rule I ended up adding was another mini challenge just for fun.

```
unconsumed_sup = False
unconsumed_bang = False
unconsumed_link = False
in_link = False
saved_link = ""
in_href = False
saved_href = ""
in_image = False
for c in line:
    if in_link and c == '^':
        unconsumed_sup = True
    elif c == '[' and unconsumed_bang:
        in_image = True
        in_link = True
        unconsumed_bang = False
    elif unconsumed_bang:
        unconsumed_bang = False
        output += '!' + c
    elif c == '[':
        in_link = True
    elif c == ']':
        in_link = False
        unconsumed_link = True
        continue
    elif unconsumed_link and c == '(':
        in_href = True
    elif unconsumed_link and unconsumed_sup:
        output += f'<sup><a class="link" href="#footnote{saved_link}">{saved_link}</a></sup>'
        unconsumed_link = False
        unconsumed_sup = False
        saved_link = ""
    # many more similar elif statements....
```

Also, I did end up using one package, but just for HTML minification. It's completely optional and doesn't impact functionality at all. The resulting pages are so small anyway that it has basically no impact on load time either.

As an ending note, please don't ever seriously do this, .
