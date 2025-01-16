---
title: [WIP] JCC: Optimization And Analysis
description: ''
author: Brandon Kirincich
date: 2024-12-28
tags:
  - jcc
  - compiler
---
Continuing on with the commit log I started in [Part 1](jcc_p1.html).

I also wrote an entire detailed report on topics learned while making these commits [here](/res/final_report.pdf), but this will be much more approachable.

## Commits 26-27

WIP
Big Backend Refactor, especially for x86\_64.
Also add liveness analysis.

## Commits 28-31

Add Mem2Reg Pass.
Also, some small additions/changes.

## Commits 32-34

Passes for Control Flow Graph Creation and Visualization.

## Commits 35-37

Pass for PhiElim(aka Static Single Assignment(SSA) Deconstruction).

## Commit 38

Dead Code Elimination(DCE) Pass.

## Commit 39

Sparse Simple Constant Propagation(SSCP) Pass.

## Commit 40

JBIR Generation.

## Commit 41

Global Value Numbering(GVN) Pass.

## Commit 42

Peephole Pass.

## Commits 43-44

Loop-Invariant Code Motion(LICM) Pass.

## Commits 45-47

Inlining Pass.
CFG Cleanup Pass.

## Commits 48-49

Pass Management.

## Commits 50-51

Instruction Encoding for x86\_64.

## Commits 52-54

Array Support.
Escape Sequences.

Taking inspiration from the example program on Day 15 of [Rui's C Compiler Blog Post](https://www.sigbus.info/how-i-wrote-a-self-hosting-c-compiler-in-40-days#day15) I created the code below for solving the [Eight Queens Puzzle](https://en.wikipedia.org/wiki/Eight_queens_puzzle).
I took special care to make sure it avoids unimplemented features, there's a few obvious workarounds that you may be able to see. However, even then, there's still some minor issue preventing it from working. After a few iterations it ends up crashing. That means there's still more work to do then!

```
#include <stdbool.h>
extern int printf(char*);

void print_board(int *board) {
  for (int i = 0; i < 8; i++) {
    for (int j = 0; j < 8; j++) {
      if (board[i * 8 + j] == 1)
        printf("Q ");
      else
        printf(". ");
    }
    printf("\n");
  }
  printf("\n\n");
  return;
}

bool conflict(int *board, int row, int col) {
  for (int i = 0; i < row; i++) {
    if (board[i * 8 + col] == 1)
      return true;

    int j = row - i;
    if ((col - j) >= 0)
        if(board[i * 8 + (col - j)] == 1)
            return true;

    if ((col + j) < 8)
        if(board[i * 8 + (col + j)] == 1)
            return true;
  }
  return false;
}

int solve(int *board, int row) {
  if (row == 8) {
    print_board(board);
    return 1;
  }
  int solutions = 0;
  for (int i = 0; i < 8; i++) {
    if (conflict(board, row, i) == false) {
      board[row * 8 + i] = 1;
      solutions += solve(board, row + 1);
      board[row * 8 + i] = 0;
    }
  }
  return solutions;
}

int main() {
  int board[64];
  int *board_ptr = board;
  for (int i = 0; i < 64; i++) {
    board[i] = 0;
  }
  solve(board_ptr, 0);
}
```