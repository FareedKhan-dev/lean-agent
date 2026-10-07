# Bugs hit while building (feeds S63, "Bugs that produced reassuring wrong answers")

1. **The build that ran nothing and said OK.** `build.py --upto part01` compared whole file
   stems (`"part01_measure" > "part01"` is True), so the part that was asked for was excluded.
   The runner executed zero code cells and printed `OK in 7s`. Mechanism: a filter that
   silently drops everything still "succeeds". Fix: compare the `partNN` prefix, and make the
   runner count executed cells and fail as INCOMPLETE when fewer ran than were built.

2. **Hidden tests that passed broken code.** Every task passed its authoring check (stub
   fails, lazy fails on its axis, good and bloated pass), and five of them still accepted
   wrong solutions. Mutation testing (S8b) planted one small bug at a time in the good
   references and found them: a rating of 6 accepted and a rating of 1 refused
   (sf-feedback-body); a document id containing a dot refused (sf-share-link); a
   12-character password, a 3- or 20-character username, and a dot right after the first
   or right before the last character of the domain all refused (ex-signup-rules); and a
   table of contents indented by four spaces, which GitHub renders as a code block
   (op-md-toc). Mechanism: tests written from the examples in our heads cover the middle
   of each rule and miss its edges. Fix: the edge cases were added to the hidden tests,
   and S8b now runs on every build, with each surviving mutant reviewed and labelled.
3. **The fence that refused its own interpreter.** The first fence compared the program
   a child process would run against `sys.executable`. On Windows, `subprocess.Popen`
   raises its audit event with the arguments already joined into one command line, so the
   comparison saw `python.exe -c "..."` and refused every child, including the legitimate
   ones the hidden tests start. The attack table still reported the attack rows that
   start a child as "refused, as expected": right answer, wrong reason. Fix: split the
   command line back into arguments, and give every refusal row the reason it must be
   refused for, so a refusal for any other reason counts as a failure.
   A second cause surfaced when the fence moved into the notebook. The check had been made
   stricter, approving `_winapi.CreateProcess` only if its command line matched the one
   `subprocess.Popen` had just reported. On this Python build that event carries a garbled
   command line (`'\x02'`), so nothing ever matched and every child was refused again. This
   time the self-test caught it before anyone read the attack table: the three tasks whose
   hidden tests start a child Python failed for reasons that had nothing to do with their
   answers, and S8 printed REFUSE TO SPEND. Fix: the full check happens at
   `subprocess.Popen`, where the arguments are intact.
4. **The edit tool that wrote the protocol into the code.** The first live baseline failed
   `eg-ipv4`, and the reason was ours, not the model's. In its second edit the model slipped
   and left a line reading `</old>` inside the `<new>` block; the edit tool applied it
   faithfully, the file stopped compiling, and the agent spent its remaining six turns
   failing to repair it. The baseline's pass rate was understated by one task because of a
   host weakness, which would have flattered every arm compared with it. Fix: the edit tool
   refuses any edit containing a line that is only an `<old>`, `<new>` or `<edit>` tag,
   and asks for the edit again. Two other slips from the same run (`<run>ARGS"/>`, a run
   tag closed like a read tag) now get a specific hint instead of "no action found".
   Lesson: read every failure of the baseline before trusting its pass rate.
5. **The exemption that did not exempt.** The ruleset said, at the end of its answer
   section, "If the user asked for an explanation, give it in full. The three-line limit is
   for prose nobody asked for." In the first live run of S32 the agent without the rules
   answered a request for a step-by-step explanation in 344 words; the agent with them
   answered in 13 ("Explained lookup_district step by step ..."). The rule was present,
   delivered and ignored: a limit stated first and an exception stated after it lost to
   the limit. Fix: the exception now opens the section and is phrased as what the answer
   *is* ("the answer is the deliverable: give all of it in your final message"), before
   any limit is mentioned. S32 shows how the revised wording behaves.


6. **The summary that lost the ticket.** Found on review before S73 ran. Compaction kept the
   first message and the last three exchanges. In a session of several tickets the ticket in
   progress was usually more than three exchanges old, so it was summarised away and the
   agent carried on without knowing what it had been asked. S73 would have measured the loss
   of the ticket and called it the loss of the rules. Fix: compaction keeps the latest
   request verbatim and lists earlier ones in the summary; a single-ticket episode is
   unchanged byte for byte, so no stored reply was invalidated.
7. **The critic that reviewed one ticket per session.** Also found before S73 ran. The
   critic and the check nudge kept their "already done" flags per session, so in a session
   of six tickets only the first was reviewed. The full system would have run without its
   critic from the second ticket on, and the decay S73 measures would have mixed rule loss
   with a missing reviewer. Fix: both reset on every new request.
8. **The API error that counted as the agent's failure.** Found on review before the main
   run. An episode cut short by an API error (after four retries) was scored like any
   other, so a provider hiccup became a failed ticket for whichever arm was running. The
   full arm makes more calls per episode (the critic, subagents) and would have absorbed
   more of them. Fix: such an episode is a failed run with no score, counted and reported,
   and left out of the paired comparisons.
9. **The daily cap that would have looked like a bad agent.** When the daily call cap was
   reached, the front door raised an ordinary error, and the grid runner, built to record
   failures rather than drop them, would have recorded every remaining episode as failed
   and gone on to analyse what was left. Fix: refusing to spend is its own exception, and
   it stops the run.
10. **The cache that could not see a changed test.** The score cache was keyed by the
   suite's fingerprint, but the house project and the specifications live outside the
   suite. Editing one of their hidden tests would have left the old scores in the cache,
   and the next run would have served them. Fix: the key covers each task's own seed and
   hidden test. Found before any fixture score was cached.

Not a wrong answer, but it changed the design: **the review that stalled the run.** The critic
called the fast model with thinking left on; a review took 40 seconds, one ran past its
120-second deadline, and the client retried it four times while the collect run sat on one
cell for twenty minutes. A review is a short answer, so the critic now switches thinking off
wherever the probe showed that works, as the router already did.
11. **The file the scorer never copied.** `snapshot()` treated every name with one leading
   underscore as the harness's own (`_tmp/`, `_seed/`), so an agent that put a helper in
   `_util.py` would have had it left out of the scoring folder: its hidden test would have
   failed with an ImportError and its lines would not have been counted. Found while
   building the folder runner, where a user's `_private.py` must survive the round trip.
   Fix: the harness owns exactly three names (`_tmp`, `_seed`, `_hidden_kit.py`). The live
   episodes were checked for such files afterwards (S80).

12. **The audit that never answered.** Every audit (S52 and all six in S76) ran out of its 14
   turns while still reading files, so none of them ever wrote its findings, and both conditions
   of H11 scored 0% recall and 0% precision: a number that measured the turn budget, not the
   auditor. Found by reading the live results before writing about them. Fix: a helper that
   runs out of turns is asked once for its answer so far, and audits get 30 turns; the S52 audit
   then found all twelve pieces of planted bloat with no false findings.
13. **The replay that would have stopped at a timeout.** A request the API failed on was neither
   answered nor recorded, so the final replay would have raised a cache miss at the first one
   (one main-grid timeout, nineteen probe timeouts, two judge errors). Fix: failures are recorded
   beside the answers; a replay meets the same failure the collect run met, and a later collect
   tries again. The coder's deadline was also raised, because its long thinking on single
   questions caused most of the timeouts.
