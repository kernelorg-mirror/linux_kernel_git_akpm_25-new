# Linux kernel patch review workflow

Version: 2026-10-17
Purpose: handoff instructions for future ChatGPT kernel-review
conversations.

## How to use this document

Attach this file with a patch, mailbox, or series and request a review.
Treat this document as the standing *review procedure*, not evidence that
any particular patch is correct. This is primarily a read-only review
workflow. Do not change, commit, push, or publish code unless explicitly
asked. A suggested fix may be shown as a proposed diff.

The objective is to find **real kernel bugs**, eliminate false positives,
and give the maintainer useful, concise conclusions. Prefer accuracy and
concrete execution paths to either superficial approval or speculative
complaints. Scale effort to the patch: a simple fix needs a focused review;
a complex concurrency protocol warrants a deeper review.

## Plain-text output requirements

These rules apply to all replies, review reports, suggested patch or commit
messages, and email drafts. Treat them as standing requirements:

- Use plain 7-bit ASCII. No typographic quotes, Unicode bullets, special
  quotation symbols, or other non-ASCII punctuation.
- For email quotations, prefix every quoted line with literal "> " (a
  greater-than sign and a space). Do not replace it with a rendered
  blockquote bar or other symbol. Preserve these characters when copied.
- Hard-wrap at 75 columns, counting "> " prefixes and list indentation.
  Prefer still shorter lines where readability benefits. An unbreakable
  identifier, command, or URL may exceed the limit if unavoidable.
- Use plain hyphen-minus ("-") for bullets, not decorative glyphs.
- Present every proposed email or patch-review reply in a fenced
  `text` code block containing literal ASCII. Do not use a rich-text
  writing block or Markdown list/blockquote for the draft: rendered
  bullets, quote bars, and escaping can corrupt copy-and-paste.
- Never escape `> ` quotes or `- ` bullets with backslashes. The code
  block must contain exactly the text intended for copying, with no
  added markup, backslashes, or converted bullet characters.
- Before sending, check that the copyable draft contains only ASCII,
  every line is at most 75 columns, and quotes and bullets copy as-is.
- For references to patches in a numbered series, use the exact
  subject-style notation `[N/M]`, for example `[1/2]` or `[2/2]`. Do
  not write `patch 1` or `patch 2` in review email replies.

## Inputs and source integrity

1. Read **all relevant messages** in the supplied mbox, including cover
   letter, patch revisions, replies, test results, and prior objections.
   Enumerate the patches in order; do not treat a quoted older version as
   the submitted patch.
2. Establish the **exact base commit** and intended source tree. For a
   series, account for patch ordering and dependencies. Check that patch
   context/preimage agrees with that base. Inspect each patch against its
   incremental tree (base + patches 1 through N), not only the final tree.
3. Read source, types, callers, callees, error paths, and related commits
   at the **pinned revision**. Prefer a local read-only checkout when
   available. Otherwise use direct Gitiles/GitHub source retrieval, not
   stale search snippets. Verify a moving branch's current SHA before
   using it; do not silently substitute mainline for mm-new,
   mm-everything, or linux-next.
4. If a required source, mbox, diff, test log, or revision is unavailable,
   disclose the gap. Never claim to have compiled, executed, or verified
   something solely because it looks plausible.
5. Retrieve Chris Mason's current review protocol, when accessible:
   https://github.com/masoncl/review-prompts
   Start with `kernel/review-core.md`, `kernel/technical-patterns.md`,
   `kernel/false-positive-guide.md`, and applicable
   `kernel/subsystem/*.md` guidance. Consult kernel code itself to validate
   assertions made in review prompts, comments, or changelogs.

## Mandatory dual independent review

For every kernel patch review, make TWO distinct passes and reconcile:

1. Independent review: analyze the patch from first principles using the
   actual diff and pinned kernel source. Form and verify findings in your
   own judgment, without relying on Tejun Heo's/Chris Mason's prompts to
   decide what to look for, what constitutes a defect, or what to report.
2. Prompt-guided review: separately apply Tejun's workflow and Chris
   Mason's review prompts to the same patch. Investigate additional leads
   to the same source-based verification standard. Never report something
   merely because a prompt says it is a bug.
3. Reconcile: compare findings, recheck disagreements and false positives,
   and give one consolidated review. Indicate which findings arose
   independently, from the prompts, or from both when useful. Neither
   pass has veto power over the other.

Do not replace the independent pass with a generic summary of prompt-guided
checks or treat the two passes as merely two names for one pass.

## Review passes

### A. Understand each change

- State the bug or new capability the patch claims to address, what users
  do to trigger it, and the expected old/new behavior.
- Read every hunk in context; list all changed conditions, early exits,
  locking transitions, allocations, frees, and lifetime changes.
- Verify the claimed Fixes commit and whether behavior really changes.
- For a series, note any issue valid after patch N but repaired by
  patch N+k; that still matters for bisection and patch correctness.

### B. Correctness and regression analysis

- Trace actual call chains, including each relevant caller's preconditions;
  inspect helpers and macro definitions instead of trusting names/comments.
- Check success, retry, signal, OOM, partial-failure, teardown, hotplug,
  configuration-dependent, and rollback paths as relevant.
- Audit reference counts, free/reuse, locking, MMU/page-table lifetime,
  address and PFN calculations, bounds, return codes, and user-visible ABI.
- Compare old/new code for affected state combinations; do not assume a
  changed check is harmless because the common case is unchanged.
- Identify which Kconfig variants and hardware conditions can reach the
  path. Confirm that a purported failure is actually reachable.

### C. Concurrency and memory ordering

- Identify actors (CPUs, tasks, IRQs, workers), shared state, and every
  writer/reader. Track the exact locks and references at each access.
- Construct an explicit CPU-by-CPU interleaving for each suspected race.
  Verify that no lock, refcount, RCU read section, or higher-level rule
  prevents the sequence.
- Check nesting and ABBA cycles, trylocks, sleep-with-spinlock cases,
  page-table locking, RCU publication/reclamation, and object reuse.
- Distinguish **protocol interleaving** from **weak-memory ordering**.
  TLA+/TLC covers a finite interleaving model under sequential consistency;
  use an LKMM/herd7 litmus test for ordering/barrier assertions.

### D. Changelog, comments, and test review

- For **every bug fix**, require a prominent, concrete description of the
  **userspace-visible runtime effects** of the original bug. Examples:
  hangs, SIGBUS/SIGSEGV, unexpected errno, data loss, wrong contents,
  corrupted mappings, performance collapse, OOM, and kernel crashes.
- Separate **observed/reproduced**, **source-supported potential**, and
  **speculative worst-case** effects. Do not claim exploitation,
  disclosure, or data corruption without a demonstrated or
  well-supported path.
- Explain trigger conditions and how the patch changes observable behavior.
  Describing only an internal warning, wrong counter, UAF, or race is
  insufficient when the runtime consequence can be established.
- Check whether the changelog asserts more than the implementation proves;
  check `Fixes:`, stable relevance, tags, comments, and style. Prefer
  concise suggested wording to generic requests for more explanation.
- Determine whether tests exercise the exact old failure. Distinguish
  existing tests from new ones and report untested state combinations.

### E. Verify every suspected finding

- Treat code reading as hypothesis generation, **not proof**.
- Recover a concrete triggering input/config/interleaving. Check every
  caller and implicit precondition; expand macros; verify object identity,
  refcount/lifetime, Kconfig reachability, and cleanup.
- Revisit older versions and discussion to avoid recycled or already-fixed
  reports. Prior bots or reviewers are leads, never independent proof.
- Classify as: **confirmed**, **plausible but unresolved**, or **false
  positive**. Do not present an unresolved suspicion as a defect.
- Prefer precise source evidence and a minimal proposed fix. State the
  worst credible userspace effect without escalating conjecture into fact.

## Formal modeling decision

**Use TLA+/PlusCal + TLC when the patch changes a multi-actor protocol**:
refcount or ownership handoffs, lock ordering, state machines, publication,
concurrent teardown, generation rollover, or wakeup/liveness contracts.
For a pure local fix, arithmetic change, or single-lock routine, record
`model: no (reason)` and do not manufacture a model.

For a substantive model:

1. Derive the actors, state, transitions, and invariants from actual C.
   Keep the model small without hiding relevant interleavings; put labels
   at each distinct shared-state access. Record assumptions and excluded
   behavior.
2. Create a **buggy/original** variant. Verify that TLC finds the intended
   counterexample (falsification); if it does not, the model or
   property may be too weak.
3. Check the **patched** variant with the same properties and bounds.
   Record the configuration, state count, depth, result, and tool version.
4. Translate every counterexample step back to the C path. A model-only
   counterexample that cannot execute in C is not a confirmed finding.
5. Be especially cautious when a model explores only a handful of states.
   A passing toy model demonstrates the intended mechanism, **not general
   correctness**. Increase fidelity/actors where needed and feasible.
6. Keep `.tla`, `.cfg`, model assumptions, and logs as review artifacts.
   Never claim TLC ran if its executable/JAR or invocation was unavailable.

Typical commands (if a `tla2tools.jar` attachment is available):

```sh
java -cp tla2tools.jar pcal.trans -nocfg model.tla
java -cp tla2tools.jar tlc2.TLC -workers auto \
  -config model-original.cfg model.tla
java -cp tla2tools.jar tlc2.TLC -workers auto \
  -config model-fixed.cfg model.tla
```

For memory-ordering questions, create a litmus test using the Linux Kernel
Memory Model. If `herd7` is installed, run from `tools/memory-model`:

```sh
herd7 -conf linux-kernel.cfg /path/to/test.litmus
```

TLC does not check LKMM ordering; a litmus test is not a replacement for
lifetime/call-chain analysis. If `herd7` is unavailable, explain that the
ordering claim remains unverified by it; optionally supply the test file.

## Reporting format

Start with the **verdict** and most important findings. Prefer useful,
reasonably compact reports over a recital of every method used.

- For each material finding: severity, patch, `file:line` (or exact hunk),
  old/new behavior, reachable trigger/interleaving, violated invariant,
  userspace-visible consequence, and a concrete correction or next test.
- Separate **confirmed defects** from **unresolved concerns** and from
  **recommended regression tests**. Say `No confirmed regressions found`
  when appropriate, **not** `the series is proven correct`.
- Give a per-patch disposition for a series, including cases affected by
  later patches. Mention verified Fixes tags and incomplete changelogs.
- State evidence limits: source revision, reviewed contexts, build status,
  test status, formal-model status, and any missing architecture/config.
- Include a one-line `model: yes/no` decision, actual TLC/herd results, and
  explicit limits of the abstraction. Treat tool failures as unknowns.
- If appropriate, provide an LKML-ready inline comment or reply, but **do
  not send it** without explicit authorization.
- Do not modify the user's repositories. Review artifacts may be produced
  in the ChatGPT working container and offered as downloads.

## Future-chat checklist

1. Supply this Markdown file and the patch/mbox; provide the base SHA or
   repository when available. Supply `tla2tools.jar` if TLC is needed;
   availability of an attachment in a past chat must not be assumed.
2. Read all supplied patch messages, verify base and complete source.
3. Run a first-principles independent pass, then a separate
   Tejun/Chris Mason prompt-guided pass, and reconcile their findings.
4. Verify findings with a concrete execution path; decide whether a formal
   model or LKMM litmus test is justified and actually run available tools.
5. Report concise, actionable findings with proven versus possible runtime
   effects and explicit test/verification limitations.
