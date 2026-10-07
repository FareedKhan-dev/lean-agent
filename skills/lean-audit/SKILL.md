---
name: lean-audit
description: Use when asked to audit a whole project for over-engineering: unused code, needless layers, dependencies the standard library covers.
mode: one-shot
argument-hint: [folder]
---
Audit the whole project for code it does not need. Look for: packages the standard library or the platform already covers; an abstract class with one subclass; a factory that makes one thing; a settings class for values that never change; functions that only call another function; hand-written versions of standard-library functions; duplicate helpers; modules nothing imports; flags nothing turns on; retries around calls that cannot fail transiently; parameters nobody passes; thread or process pools for work that does no I/O.

Before you list anything for deletion, search the whole tree for it, tests included, and remember that code can be reached by a name built at run time (getattr, importlib, a lookup table). If you find any reference, it is not dead.

List findings as numbered lines, biggest cut first:
N. tag: file: symbol: what to do (net: -K lines)
Use the tags delete, stdlib, native, reuse, yagni, shrink. End with: net: -N lines, -M dependencies.
