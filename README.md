# lean-agent

**A coding agent that refuses to over-engineer, built from scratch and measured honestly, in one course notebook.**

Ask a coding agent for a cache and you often get a cache class, a configuration object, an abstract interface and three new files, when `functools.cache` was one line. This project builds an agent whose job is to write the *least code that does the job completely*, without ever cutting the things that keep code safe: input checks, data-loss handling, security, accessibility, or anything the user asked for. Then it runs a pre-registered experiment to find out whether any of it actually works.

Everything lives in one notebook, [`lean_agent_course.ipynb`](lean_agent_course.ipynb): about 1,600 cells, one function per cell, each explained before it is built and demonstrated after, with 24 figures and 37 diagrams. It is written for students, developers, researchers and teams.

The notebook ships with its outputs, so you can read every result on GitHub without running anything.

---

## Contents

- [What the notebook builds](#what-the-notebook-builds)
- [Does it work? The results](#does-it-work-the-results)
- [Quick start](#quick-start)
- [The three run modes](#the-three-run-modes)
- [Using the agent on your own code](#using-the-agent-on-your-own-code)
- [Repository layout](#repository-layout)
- [How the notebook is built](#how-the-notebook-is-built)
- [Models and cost](#models-and-cost)
- [Known limitations](#known-limitations)
- [Reading paths](#reading-paths)

---

## What the notebook builds

The system has three layers. The **host** knows how to run an agent but has no opinion about code size. The **plugin** rides on the host's hooks and carries every idea about proportional code. The **lab** measures both. Switch the plugin off and you get the baseline it is compared against.

| Part | What it builds |
|---|---|
| **I. Measure before you build** | A bloat meter that cannot be gamed (code, comments, docstrings, checks and tests counted apart, only added lines charged), ten detectors for ten shapes of over-engineering, a golf detector, guard signatures, and a table of standard-library replacements where every row carries a test. |
| **II. Tasks that can say no** | 34 tasks with hidden tests and 8 kinds of trap, a sandbox fence built on Python audit hooks, a scorer, mutation testing of the hidden tests, and a self-test that refuses to spend money until every instrument is proven. |
| **III. The host** | A streaming API client in the standard library, a ledger that caches and replays every model answer, six sandboxed tools, an event bus whose hooks cannot break the agent, a context manager with compaction, skills, commands, subagents and a statusline. |
| **IV. The ruleset** | One source text, filtered into three levels (lite, full, ultra), plus a compact copy for subagents. |
| **V. Delivering the rules** | Hooks that inject the rules at session start, after compaction and into subagents, a per-prompt mode header, and the `/lean` command. |
| **VI. Gates, a critic and skills** | Machinery that enforces what the rules only ask for, plus the review, audit, debt, gain and help skills. |
| **VII. Experiments** | Pre-registration, a five-arm main comparison, an ablation ledger that removes every piece that does not earn its place, levels, six models, a Goodhart test, a rule-change gate, a house-style project, long sessions, specifications with a surprise extension, and behaviour probes. |
| **VIII. Honest evaluation** | Validated LLM judges, completeness, instrument checks, aggregation choices, negative results, threats to validity and a claims table. |
| **IX. Case studies** | Three tickets read side by side, why runs failed, and the debt the system leaves behind. |
| **X. Operating it** | Time, tokens and cost, a console, running it on your own folder, dogfooding, an adoption guide and a manifest. |

### The features that fight over-engineering

**Rules the model reads**, at three strengths:

1. **The ladder.** Before writing code, go down a list and stop at the first step that does the job: nothing at all, code the project already has, the standard library, the platform (a database constraint, an HTTP status, an HTML attribute), an installed package, one expression, and only then new code.
2. **Read first, fix the cause.** Open what you change, and fix a bug where it starts.
3. **How to build.** No abstract class with one subclass, no factory that makes one thing, no setting for a value that never changes.
4. **Never cut.** Input checks, data-loss handling, security, accessibility, and anything the user explicitly asked for.
5. **Prove it.** Leave one runnable check.
6. **Shortcuts, marked.** `# shortcut: <the limit>; upgrade when <the condition>`.
7. **How to answer.** Code first, then at most three lines, including `left out: <what> (build it when <condition>)`.

**Machinery that delivers and enforces them:** hooks that keep the rules in front of the model, the `/lean` mode command, a project map, a read gate, a sibling scan, a dependency gate, a one-time nudge for a check, a critic that reviews the change before the agent may finish, and a trim guard that lets the critic cut structure but never a guard.

**Skills a user calls by name:** `/lean-review`, `/lean-audit`, `/lean-debt`, `/lean-gain`, `/lean-help`.

---

## Does it work? The results

All numbers below come from the committed experiment records in [`artifacts/`](artifacts/). The hypotheses and their decision rules were written down and fingerprinted before the main run ([`artifacts/preregistration.json`](artifacts/preregistration.json)).

**The problem is real.** Without any rules, the coder model passed 32 of 34 tasks but wrote a median **1.48x** the code the tasks needed, and more than twice as much on 12 of them.

**The main comparison** (340 episodes, 5 arms, held-out tasks):

| Hypothesis | Result |
|---|---|
| **H1** The full system writes less code (registered bar: interval upper end below 0.85) | Code ratio **0.88** (95% interval 0.68 to 1.00). About 12% less code, but the bar was not met, so **not supported**. |
| **H2** It is not less safe | **Supported.** Safety unchanged (100% in both arms). |
| **H3** It is not less complete where completeness matters | **Supported.** No loss. |
| **H4** The plugin's machinery beats the same rules pasted as plain text | **Not supported.** |
| **H5** A one-line slogan drops guards | **Not supported.** The slogan stayed safe on these tasks. |
| **H9** The LLM judges are valid instruments | **Supported.** Bloated answers ranked above good ones on 100% of known pairs; agreement kappa 0.92. On ordinary agent code the two judges agree far less (0.31), so the meter, not the judges, carries the headlines. |

**The ablation ledger** removed every piece that did not measurably help. **Kept:** the ladder, the check nudge and the critic (and *never cut*, which is exempt by design). **Removed:** read first, prove it, how to answer, the project map, the read gate, the sibling scan and the dependency gate. What ships is what survived.

**The cost:** the full system took about 12 turns and 30k input tokens per episode against 10 turns and 12k for the baseline. The hooks themselves add under 1% of the time.

**In one line:** the system is safe and trims some code, and the ladder and the critic earn their place, but the large saving the plan hoped for was not proven on these tasks. The notebook says so in its own negative-results section (S83), alongside the bugs that produced reassuring wrong answers (S85) and the threats to validity (S86).

---

## Quick start

You need **Python 3.12+** and [uv](https://docs.astral.sh/uv/) (or plain pip).

```bash
git clone <this repository>
cd lean-agent
uv sync                      # or: pip install numpy matplotlib ipykernel ipywidgets nbclient nbformat
```

**To read it:** open `lean_agent_course.ipynb` in VS Code, JupyterLab or on GitHub. All outputs and diagrams are already in the file.

**To re-run it offline**, for free, from the stored model answers:

```bash
uv run python _build/run.py replay
```

This unpacks the answer ledger once (`artifacts/cache/llm.sqlite.gz`, about 150 MB unpacked), rebuilds the notebook from its sources and executes every cell. A request the ledger has never seen stops the run instead of calling the API. It takes about 6 to 7 minutes and needs no API key.

**To run it inside Jupyter**, unpack the ledger once with the command above (or `--upto part01` for a quick start), then open the notebook and run all cells; with a ledger present it replays automatically.

---

## The three run modes

| Mode | What answers the model calls | Cost | Use it to |
|---|---|---|---|
| `smoke` | A scripted stand-in model | Free, about 3 minutes | Check that every cell still runs after an edit |
| `replay` | The stored ledger; a miss is an error | Free, about 6 to 7 minutes | Reproduce the committed notebook exactly |
| `collect` | The live API; every answer is stored | Paid | Run new experiments, or re-run after changing anything a model sees |

```bash
python _build/run.py smoke  --upto part03    # a quick check of the first three Parts
python _build/run.py replay                  # writes lean_agent_course.ipynb
python _build/run.py collect --upto part07a  # live calls, resumable: answered requests replay free
```

`collect` refuses to spend until the Part II self-test has passed, stops at a daily call cap, and resumes from the ledger after an interruption or a network failure.

**The API key.** Live runs use the ModelScope API. Put your key in a file named `modelscope.txt` in the folder **that contains** this repository (one level up). It is kept outside the project on purpose, so it can never be committed. The notebook reads it once, never prints it, keeps it out of every sandboxed process, and the lint scans every shipped file for it.

---

## Using the agent on your own code

Part X (S94b) defines `run_on_folder(path, ticket)`. It treats your folder as read-only:

1. It copies the folder into a sandboxed workspace, leaving out `.git`, virtual environments, caches, binaries and very large files, and reports every skip.
2. The shipped system works the ticket on the copy, inside the fence.
3. You get back a **patch** that `git apply` understands, and a short **report**: the step of the ladder it stopped at, what it left out and when to build it, shortcuts it marked, what the critic said and what the gates refused.

Four checks run on every call: your folder's fingerprint is unchanged, the patch reproduces the result on a fresh copy, nothing can write into your folder, and an unreadable file is reported instead of crashing the run.

Running it on new code makes live model calls, so start the notebook in collect mode (`LEAN_MODE=collect`) with a key in place, run through Part X, then call `run_on_folder("path/to/project", "your ticket")`.

---

## Repository layout

```
lean_agent_course.ipynb   the notebook, with every output (built by _build/run.py replay)
_build/
  cells/                  the notebook's source: one .cells file per Part (edit these, not the .ipynb)
  diagrams/               the diagrams' mermaid sources
  vendor/mermaid.min.js   the pinned mermaid build used to render them offline
  build.py                assembles the notebook; fills {{exp:...}} numbers and embeds diagrams
  run.py                  runs it headlessly: smoke, collect or replay
  lint.py                 style and safety checks on the finished notebook
  render_diagrams.py      draws every diagram to a PNG with headless Chrome or Edge
  check_tasks.py          authoring check for task fixtures
  inspect_outputs.py      dumps cell outputs for review
  build_bugs.md           bugs met while building, which feed section S85
tasks/                    the 34 tasks: seed code, hidden test, reference answers, task.json
fixtures/                 the house-style project, three specifications, the audit project, a sample project
skills/                   the six SKILL.md files the notebook writes and loads
artifacts/
  exp_*.json              every experiment's record: the source of every number in the prose
  preregistration.json    hypotheses and decision rules, fixed before the main run
  shipped_system.json     the configuration that survived the ablation ledger
  manifest.json           models, dates, fingerprints and library versions
  figures/                the 24 figures as PNG files
  diagrams/               the 37 rendered diagrams
  cache/llm.sqlite.gz     the ledger: every model request and answer (12,546 answers)
  cache/scores.sqlite     cached scoring results
```

---

## How the notebook is built

The `.ipynb` is a build product. Its source is `_build/cells/partNN_*.cells`, plain text split into cells by `#%% md` and `#%% code` lines. Markdown cells carry placeholders that the build fills from the experiment records:

- `{{exp:main.h1.ratio:.2f}}` inserts a number from `artifacts/exp_main.json`.
- `{{pick:house.h13|FEWER=...|NOT FEWER=...}}` picks a sentence by verdict.
- `{{diagram:ladder}}` embeds `artifacts/diagrams/ladder.png` as a cell attachment, so diagrams show in any viewer.

So the prose can never drift from the data. A typical edit loop:

```bash
# edit _build/cells/part04_rules.cells
python _build/run.py smoke --upto part04     # does it still run?
python _build/run.py replay                  # rebuild the real notebook, free
python _build/lint.py lean_agent_course.ipynb
```

**One rule matters above all:** replay looks up every model request by its exact text. Changing anything a model sees (a prompt, a rule, a tool's output, a gate's message) makes those requests new, and replay will stop with a `CacheMiss` until you `collect` them, which costs money. Pure readability edits, comments, prose and figures cost nothing.

To redraw the diagrams after editing `_build/diagrams/*.mmd` (needs Chrome or Edge, and Pillow):

```bash
uv run --group diagrams python _build/render_diagrams.py
```

---

## Models and cost

All models are served by ModelScope (`api-inference.modelscope.ai`), each with one role:

| Role | Model |
|---|---|
| Coder (writes every line the experiments measure) | Qwen3.8-27B |
| Router, subagents, critic | Qwen3.8-Flash-Next |
| Judges (a different generation from the coder) | Qwen3.7-Max, Qwen3.7-Plus |
| Transfer sweep | Qwen3.8-Max, Qwen3.8-Omni-Flash |

The full collect made 12,546 calls. At ModelScope's per-request pricing that was roughly 3,400 credits, most of it the coder at about 9,900 calls. Replaying is free.

---

## Known limitations

These are documented rather than fixed, because a fix would change what the model sees and so needs a paid re-collect:

- The sibling scan miscounts changed functions after an edit that deletes text.
- A second compaction in one session loses the first summary's steps.
- The read gate refuses a second edit to a file the agent itself created.
- Compaction does not restore the skills index or a project instructions file.
- The meter treats everything after a real function named `check()` or `demo()` as the self-check, and can mis-label lines after a form-feed character.

The experiments themselves are small: Python only, tasks written by the same people who built the system, and one model family. Section S86 lists the threats to validity in full.

---

## Reading paths

- **Students:** the *In plain terms* paragraphs and the *Try it yourself* exercises at the end of each Part; the statistics in Parts VII and VIII can wait.
- **Developers:** Parts III to VI are the system; S94b points it at your own folder.
- **Researchers:** Part I (instrument validity), S61 (pre-registration), Parts VII and VIII (design, statistics, threats to validity).
- **Teams:** the *For teams* notes, the cost sections S92 and S93, and the adoption guide S96.
