---
title: Static Site Generator Abomination
description: 'A quick look at how this website was made(the fun parts)'
author: Brandon Kirincich
date: 2024-09-27
tags:
  - web
  - ssg
  - fun
---

I originally built this website using Go and hosted it on Google Cloud, but I decided to switch things up and save some money. Now, it's a simple static site hosted on GitHub Pages.

However, using an existing Static Site Generator([SSG](https://en.wikipedia.org/wiki/Static_site_generator)) like [Jekyll](https://jekyllrb.com/) or [Hugo](https://gohugo.io/) would be no fun, so I decided to make my own from scratch.

Additionally, rather than creating another run-of-the-mill, typical SSG, I decided to challenge myself—just for fun.

- Single-pass Markdown parsing and HTML generation
- Less than 300 lines of normal, non-code-golfed Python
- No external libraries or packages
- Enough features to write high-quality (debatable) blog posts

The result was a ~225 lines of code (LOC) "[abomination](https://github.com/BrandonKi/BrandonKi.github.io/blob/main/.src/gensite.py)", with the core of it being the convert2html function.

That function, while only ~170 LOC, lexes and parses markdown while simultaneously generating the corresponding HTML. It uses what essentially became a state machine with almost no lookahead.

This led me to discover a surprisingly useful pattern (for this project at least, and probably nothing else!).

#### Single-Pass Generation, Without Lookahead

In Markdown, "keywords" are just normal characters, and their special significance ("keywordness") depends on context. This concept isn't unique to Markdown—many programming languages have similar behaviors. For example, in C++, you can name a variable "final" even though it has a special meaning in certain contexts. Most languages use fully-featured lexers and parsers, but I’ve done enough of that. Why not try something more interesting?

In Markdown, characters like "#" and "-" are used to create headers or lists, but they may do nothing if they appear in certain contexts. To complicate things further, surrounding text with parentheses or brackets could mean it's part of a link or image (which requires special handling), or it might just be regular text. It’s not just about characters being "consumed" later; sometimes entire portions of text are involved.

Since I was generating HTML while parsing and couldn’t go back to revise already output HTML, I had to come up with a system.

Anything that may may have it's meaning changed by a later character has to be saved.

TODO

#### Example

I wouldn’t recommend doing this for any serious project, but here’s a small snippet of what the resulting code looks like. The "no-lookahead" rule I imposed on myself was just an extra mini-challenge for fun.

```python
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
    # some uninteresting elifs here were elided for readability
    elif unconsumed_link and unconsumed_sup:
        output += f'<sup><a class="link" href="#footnote{saved_link}">{saved_link}</a></sup>'
        unconsumed_link = False
        unconsumed_sup = False
        saved_link = ""
    elif unconsumed_link and unconsumed_sup:
        output += f'<sup><a class="link" href="#footnote{saved_link}">{saved_link}</a></sup>'
        unconsumed_link = False
        unconsumed_sup = False
        saved_link = ""
    elif in_image and in_href and c == ')':
        in_image = False
        in_href = False
        output += f'<figure><img src="{saved_href}"><figcaption>{saved_link}</figcaption></figure>'
        saved_link = ""
        saved_href = ""
    # many more similar elif statements....
```

I did end up using one external package for HTML minification, but it’s completely optional and doesn’t impact functionality. The resulting pages are so small that the minification has almost no effect on load time.

As an ending note, please don't ever seriously do this. :)
