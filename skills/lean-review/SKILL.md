---
name: lean-review
description: Use when asked to review code or a change for unnecessary complexity, and before finishing a change. Not for correctness, security or style reviews.
mode: one-shot
argument-hint: [the change to review]
---
Review the change for code it did not need. Scope: complexity only. Correctness, security and style are out of scope, and so is the one runnable check: never suggest removing it, and never suggest removing a guard (input checks, error handling that prevents data loss, security checks, accessibility).

List findings as numbered lines, most valuable first, each in this form:
N. tag: file: what to remove or replace, and with what (net: -K lines)
Tags: delete (code nothing needs), stdlib (the standard library already does it), native (the platform does it), reuse (the project already has it), yagni (built for a need nobody has), shrink (the same behaviour in fewer lines).
State each finding flatly, as a fact with its replacement. Do not ask questions and do not hedge.
End with one line: net: -N lines.
If nothing is worth removing, reply with exactly: Lean already. Ship.
