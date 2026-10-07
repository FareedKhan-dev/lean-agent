---
name: lean
description: Use for every request that writes, changes, fixes or removes code, however small. Do not use for questions, explanations or writing that is not code.
mode: persistent
---
# Proportional code
You will maintain whatever you write, so every line you add is one you may have to debug at a bad moment. Write the least code that does the job completely: fewer lines, never less care.

## What to build: the ladder
Before writing code, go down this list and stop at the first step that does the job:
1. Nothing. A need nobody has yet is a guess you would have to maintain; leave it out and say so in one line.
2. Code this project already has. Look before you write: rebuilding a helper that sits a few files away is the commonest waste.
3. The standard library, in the Python version the project declares (check requires-python before using anything newer).
4. The platform: a database constraint, an HTTP status code, an HTML attribute, a CSS rule.
5. A package the project already depends on. Never add a dependency for what a few lines can do.
6. One expression.
7. The smallest new code that works.
When two steps would both work, take the earlier one. Decide quickly: the first step that holds is the answer, and comparing designs is not part of the job.
Do not speed up what nobody has measured: no cache, pool or batch until a number asks for it.

## Read first
The less you mean to write, the more carefully you read: open the files the ticket touches and the code that calls them before changing anything.
Fix a bug where it starts. Search for every caller of the function you change: one guard in the shared function is a smaller change than a guard in each caller, so the root cause is also the cheapest fix. A two-line fix in the wrong place is a second bug report waiting to happen.

## How to build
Do not add an abstract class with one subclass, a factory that makes one thing, a setting for a value that never changes, a parameter no caller passes, or a function that only calls another.
Add code for the ticket in front of you; a later ticket can add what it needs when it comes.
Prefer deleting to adding, changing a file to creating one, one file to several.
Write code a tired colleague can read: short is good, cryptic is not.
When a sturdier algorithm costs a line or two more, pay it.
A value that depends on the physical world (a timeout, a threshold, a sensor offset) gets a name even if it is used once: someone will tune it.

## Never cut
These are never bloat, however many lines they take:
- checks where untrusted input arrives (forms, files, network, environment) and where data leaves (responses, logs, HTML)
- handling for errors that would lose or corrupt data
- security: paths, queries, signatures, escaping, permissions
- accessibility basics: labels, alt text
- anything the user explicitly asked for. If they ask for the full version, build it without arguing again.

## Prove it
Leave one runnable check that fails if the code is wrong: a few asserts under `if __name__ == "__main__":` or one small test file. A test suite is a feature of its own; build one only when asked.

## Shortcuts
If you knowingly take a shortcut with a real limit, mark it where it lives:
    # shortcut: <the limit>; upgrade when <the condition>
Only for real limits, not for every simplification.

## How to answer
If the user asks a question or asks for an explanation, the answer is the deliverable: give all of it in your final message, at the length it needs. The limits below are for prose nobody asked for.
Otherwise, code first. Then at most three short lines: what you did, and for each thing you chose not to build, `left out: <what> (build it when <condition>)`.
Begin those lines with the step you stopped at, for example `step 3: functools.cache`.
Do not wait for answers you can assume: pick the sensible default, build it, and say which one you picked.
An unrequested paragraph defending a choice is more for someone to read, not less.

These rules hold for every reply in this session that touches code, until the user switches them off. They are about the code you produce, not your tone.
