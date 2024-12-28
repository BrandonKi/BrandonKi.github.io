---
title: JCC, Part 2: Making A C Compiler
description: ''
author: Brandon Kirincich
date: 2024-12-28
tags:
  - JCC
  - Compiler
---
Continuing on with the commit log I started in [Part 1](jcc_p1.html)

## Commits 26-27

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

## Commits 52-53

Array Support.
