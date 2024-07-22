---
title: 'Making A C Compiler (JCC)'
description: ''
author: 'Brandon Kirincich'
date: 2024-07-19
tags:
  - JCC
  - Compiler
---
*Updated on 7/19/2024*



I started working on a C compiler a little while ago called [JCC](https://github.com/BrandonKi/jcc), and this is log of my progress over time.

First of all, you may be wondering:

*Why would you decide to make a C compiler?*

Well, that's a good question. Honestly, the real reason is I randomly decided one day I wanted to compile and play [DOOM](https://github.com/id-Software/DOOM) using my own compiler.


## Commits 1-2

The plan is to have two backends, a custom backend([JB](https://github.com/BrandonKi/jcc/tree/main/jb)) and an [LLVM](https://llvm.org/) backend. The first thing I did was pull in the code for JB, which was a small project I worked on previously and set up LLVM.

After the boring stuff I started working on the actual parsing and codegen. I basically spent all my time getting expression parsing and operator precedence working correctly. Luckily I implemented it straight from grammar rules in the [spec](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf) so that made it easier. The compiler is surprisingly capable already, but it's missing very basic features. Lastly, codegen was pretty easy for this part since I'm saving integration with JB for later. Here's an example of something it can currently handle.
```
int main() {
    int x = 10;
    int y = x * 2;
    int z = y - x + 5;
    return -(+y * +z) / -(x);
}
```

## Commits 3-5

Progress has been pretty quick. I implemented function calls, pointers, and all the various compound assignment operators. There's still more work to be done for all of these features but it's a solid start. Here's an example of what currently works.
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

Up until this point only ints have been supported but I started laying the groundwork for the other builtin types and type checking. Also, currently the compiler crashes whenever it encounters an error which isn't the best user experience. It may be time to add better error reporting soon.

Also, parsing types in C is... not fun as you all probably know, but not as bad as C++. What's even more unfortunate is they appear before the identifier for a variable/function so they're no even easy to ignore. As a result I put together a bunch of hacks to make parsing work (kinda) for simpler cases, this is something I'll have to revisit when more features are added.


The major features I added this time were string literals, extern function, and char pointers. I can now run the classic [Hello World!](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program). During this I also realized my test runner can't check for correct STDOUT results yet, but that's a problem for future me. Anyways, here's another example of the new features in action.
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

I also did a big cleanup pass over the existing code which was pretty easy since this project is still in it's early stages. Making an example to showcase all of these changes so here's a small one.
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

Sema.

## Commits 