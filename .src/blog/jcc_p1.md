---
title: JCC: Making A C Compiler
description: ''
author: Brandon Kirincich
date: 2024-07-19
tags:
  - jcc
  - compiler
---
I started working on a C compiler a little while ago called [JCC](https://github.com/BrandonKi/jcc), and this is log of my progress over time.

First of all, you may be wondering:

*Why would you decide to make a C compiler?*

Well, that's a good question. Honestly, the real reason is I randomly decided one day I wanted to compile and play [DOOM](https://github.com/id-Software/DOOM) using my own compiler. Yeah... that's pretty much the only reason.

Anyways, let's get into the interesting stuff.

## Commits 1-2

The plan is to have two backends, a custom backend([JB](https://github.com/BrandonKi/jcc/tree/main/jb)) and an [LLVM](https://llvm.org/) backend. As a result the first things I did was pull in the code for JB, which was a small project I worked on previously, and set up LLVM.

After the boring stuff I started working on the actual parsing and codegen. Basically all my time was spent getting expression parsing and operator precedence working correctly. It was not fun

Luckily I implemented it straight from grammar rules in the [spec](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) so that did make it easier but still not fun.

On the bright side at least codegen was pretty easy for this part since I'm saving integration with JB for later.

Here's an example of something it can currently handle.

```
int main() {
    int x = 10;
    int y = x * 2;
    int z = y - x + 5;
    return -(+y * +z) / -(x);
}
```

## Commits 3-5

Progress has been pretty quick. I implemented function calls, pointers, and all the various compound assignment operators.

There's still more work to be done for all of these features but it's a solid start.

Here's an example of what currently works.

```
int identity(int x) {
    int *y = &x;
    int z = *y;
    return *&z;
}

int main() {
    int t = 99;
    t += 1;
    return identity(t);
}
```

## Commit 6

Up until this point only `int` has been supported, but I started laying the groundwork for the other builtin types and type checking. Parsing types in C is... not fun, as you all probably know, but not as bad as C++.

What's even more unfortunate is they appear before the identifier for a variable/function so they're not even easy to ignore. For this reason, I put together a bunch of hacks to make parsing work (kinda) for simpler cases, this is something I'll have to revisit when more features are added.

Also, currently the compiler crashes whenever it encounters an error which isn't very user-friendly! It may be time to add better error reporting soon.

The major features I added this time were string literals, extern function, and char pointers. I can now run the classic [Hello World!](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) program. During this I also realized my test runner can't check for correct STDOUT results yet, but that's a problem for future me. Anyways, here's another example of the new features in action.

```
extern int printf(char *);
extern void puts(char *);
int main() {
    char *a = "Hello World!";
    int result = printf(a);
    puts("");
    return result; // returns 12
}
```

## Commits 7-11

A lot of progress was made. Here's the major features that were added:

- if/else statements
- for loops
- do/while loops
- ++/-- operators

I also did a big cleanup pass over the existing code which was pretty easy since this project is still in it's early stages. Making an example to showcase all of these changes is too hard so here's a small one.

```
int main() {
    int a = 0;

    for(int i = 0; i < 10; i++) {
        if(i % 2 == 0)
            a += i;
        else
            a -= 1;
    }

    return a; // returns 15
}
```

## Commits 12-13

I finally decided to start working on semantic analysis and type checking. This meant I had to actually make pointers work correctly instead of the hacks I was doing before.

Also, C has a concept of [constant expressions](https://en.cppreference.com/w/c/language/constant_expression) which I am leaving for later but it will be handled during semantic analysis.

The other major features I added were `sizeof` and `\_Alignof`. These were pretty easy to add, but `sizeof` expressions are pretty odd especially because of the optional `()`.

As per usual here's an example with some of the new stuff.

```
int main() {
    short a = 0;
    short b = 1;
    int x = sizeof a + b;
    int y = sizeof(a + b);
    return x + y; // returns 7
}
```

## Commits 14-16

In this project, I took an approach of being very liberal with asserts. Rather than allowing the program to continue in an invalid state, I crash early and often. This approach has saved me a lot of debugging time, since each assert gives a reason for the failing as well.
Although, one issue is, even with asserts, the root cause of the bug is often some arbitrary amount of code prior to where the assert fires. Luckily, this is a compiler, and it's single threaded, so just running the same input again should almost always exibit the incorrect behavior again. However, this can be made even easier if asserts simply printed out a stacktrace, so I created an Internal Compiler Error(ICE) macro.[^1] It is functionally equivalent to an assert, but prints a proper stacktrace.

There also some other easy debug features I can add as well. For example, simply printing out the current position being parsed in the file, and the last and next few tokens. 

I recently started using [X Macros](https://en.wikipedia.org/wiki/X_macro). In compilers, it's common to define long enums that need to be reused across multiple contexts. Without X Macros, this often means copying and pasting the enum members, extra care must be taken to keep all of these pasted locations in sync though. With X Macros, I can avoid the duplication and ensure all these locations stay synchronized.

Additionally, X Macros allow me to associate extra information with each enum item. For example, I can include textual representations of tokens directly within the enum definition, as shown below. Of course, this would be much easier and uneccessary if C++ had proper metaprogramming support though.

Here’s an example from my lexer token definitions. I'm able to use the same token definitions in multiple different contexts without duplicating the over 100 entries.

```
// Defining each entry in token_kinds.inc
X(_inc, -58, "++")
X(_dec, -59, "--")
X(_arrow, -60, "->")
X(_star_equal, -61, "*=")
X(_slash_equal, -62, "/=")
...

// Using an X macro for enum definition
#define X(a, b, _) a = b,
enum TokenKind : char {
    #include "inc/token_kinds.inc"
};
#undef X

// Using an X macro for a switch statement
#define X(a, b, c)     \
    case TokenKind::a: \
        result = c;    \
        break;
switch (token.kind) {
#include "inc/token_kinds.inc"
default:
    ice(false);
}
```

Lastly, I made progress on the C preprocessor implementation, but only basic functionality. Since it's not fully detailed in the spec, for correctness, it's partially based on this [pdf](https://www.spinellis.gr/blog/20060626/cpp.algo.pdf).

## Commits 17-19

The focus of these few commits has just been refactoring the custom backend(JB).

- MCIR is now machine independent
- Register allocation is done on MCIR instead of JBIR now
- Added a baseline interpreter
- Reworked immediates/labels/values
- JBIR instructions were added/removed/renamed
- Added "stack slots", so values can be used normally from the stack now
- Completely reworked x86\_64 codegen to be more like a macro assembler

## Commits 20-22

Frontend Progress.

- Preprocessor expansion bug fix
- Move allocas to beginning of function
- Start conditional include implementation
- Intern strings across the whole AST
- Can now `#include` basic stdlib files, such as `stdbool.h`

Here's a small example.

```
#include <stdbool.h>

#define COND1
int main() {
#ifdef COND1
#ifdef COND2
    return true;
#else
    return 2; // returns 2
#endif
#else
    return 100;
#endif
    return false;
}
```

## Commits 23-25

More Frontend Progress!

- structs
- constant expressions
- `#if`
- `defined`
- `&&` and `||` in constant contexts
- refactored lvalue codegen
- added `->`
- stringize operator `#`

Also, a small bug fix. Object-like macros starting with open paren now parse correctly, previously they would incorrectly be parsed as a function-like macro

```
// object-like
#define test (a)

// function-like
#define test(a) a
```

Code like this now works correctly!

```
int main() {
    struct Pair {
        long long a;
        int b;
    };
    struct Pair s;
    struct Pair *ptr = &s;
    s.a = 5;
    s.b = 10;
    return ptr->a + ptr->b; // returns 15
}
```


## Footnotes

[^1]: A small explanation since I was confused for the reason behind this terminology the first time I saw it. It's commonly referred to as an Internal Compiler Error(ICE) rather than just an error because reporting errors is part of the core functionality of a compiler. In order to remove ambiguity most compilers call this situation an ICE, especially when communicating that an error occurred to the end user, so they know the issue wasn't in their code.
