# AKPM kernel patch review workflow

Purpose: local review policy for future ChatGPT kernel patch reviews.
This is the entry point. It invokes `tj-patch-review-workflow.md`, which
is Tejun Heo's original S2 workflow and must be left unchanged.

This file contains AKPM-specific instructions and additions. It does
not replace or edit Tejun's instructions. The old
`kernel-patch-review-workflow.md` is superseded: do not use or update it.

## Execution order: two separate review passes

For every review, including single patches and mbox series:

1. First perform an independent, first-principles review of the entire
   submitted change against the relevant kernel source. Do not consult
   Tejun's instructions or Chris Mason's prompts to choose the review
   questions or decide on findings in this pass. Preserve the findings
   and the paths checked before proceeding.
2. Then read and apply `tj-patch-review-workflow.md` as a separate pass.
   Follow its instructions to use Chris Mason's review prompts:
   https://github.com/masoncl/review-prompts
   Load the current core, technical, false-positive, build, and matching
   subsystem guidance. Verify all leads against source code. A prompt's
   declaration that something is wrong is not evidence by itself.
3. Reconcile the two passes. Compare their path coverage, not just their
   reported bugs. Investigate paths checked by only one pass, resolve
   disagreements, eliminate false positives, and deliver ONE combined
   judgment. Indicate the origin of a finding when informative.

Both passes must use their own producer/consumer inventory and inspect
all relevant paths. Do not simply relabel one pass as two. If the tools
do not permit Tejun's suggested parallel reviewers, do two genuinely
separate sequential analyses and disclose that limitation. Do not claim
that subagents, builds, runtime tests, TLC, or herd7 ran unless they did.

The independent pass is required even when the prompt-guided pass is
much deeper. Neither pass has veto power over the other.

## Source integrity and review scope

- Read all relevant material in the supplied mbox: the actual patches,
  cover letter, earlier revisions, replies, test results and objections.
  Distinguish the proposed patch from older patches quoted in email.
- Determine the exact base SHA, tree, and patch ordering. Review each
  patch after applying only its predecessors, so each commit remains
  independently correct and bisectable. Check preimage/hunk context.
- Inspect function bodies, types, callers, callees, macros, lifetime and
  error paths at the pinned source revision. Prefer a local read-only
  checkout or exact GitHub/Gitiles source, not search-result snippets.
- Do not silently substitute mainline for `mm-new`, `mm-everything`,
  `linux-next`, or another named tree. Verify a moving branch's SHA.
- Verify relevant Fixes commits and the actual old behavior. Check
  build/config/hardware reachability before asserting a regression.
- If material evidence is missing, describe the precise limitation.
  Do not fill the gap with guesses or treat a comment as proof.
- Reviews are read-only. Do not edit production code, commit, push, or
  publish anything unless expressly instructed. A suggested change may
  be shown as a proposed diff or an unsent email.
- Scale effort to the change. Favor a fast, decisive review of small
  fixes; use more research and modeling for subtle, consequential bugs.
  Tractability matters, but never replace required coverage with speed.

## Mandatory impact-coverage gate, in BOTH passes

A small condition or bit change can alter behavior in distant code. The
MGLRU `PG_active` review missed `evict_folios()` and
`shrink_folio_list()` because their effects were not systematically
inventoried. Prevent a recurrence as follows:

1. Enumerate all relevant consumers and callers of each changed helper,
   condition, return value, or side effect. Follow wrappers, indirect
   calls, and control decisions at the call site where necessary.
2. Inventory state producers, writers, readers, clearers, and inherited
   state for every affected bit or field. Identify distinct origins of
   the SAME flag combination, e.g. fault, reclaim, migration, explicit
   activation, failed reclaim, retry, hotplug, or teardown. Prove any
   supposedly impossible path is blocked by an actual higher-level guard.
3. Construct a producer-to-consumer matrix: each reachable input class,
   its old and new decision, subsequent action, invariant and possible
   userspace-visible consequence. Do not restrict this to the motivating
   workload. Check the eventual result, not merely the helper's return.
4. Enumerate meaningful combinations of flags, modes, object types,
   architectures, sizes, and boundary values. Pay attention to condition
   precedence and clamping, including min/max generations. For simple
   finite logic, use an executable truth table rather than TLA+.
5. Explicitly check what happens on failed attempts and retries: can a
   rejected object return to the same state, can a protected object be
   immediately reconsidered, and do accounting and traces describe the
   actual final outcome?
6. Before finishing each pass, compare the completed inventory against
   source searches for consumers and writers. Record gaps and guards.
   Do not claim exhaustive coverage if relevant paths remain unexamined.

Reconciliation must compare these inventories and investigate missing
path classes, rather than simply vote on reported issues. A convincing
example of ONE failure path does not end the search for others.

## Similar-bug search: mandatory in BOTH passes

When reviewing an MM fix, search related MM code for other instances of
its underlying bug pattern, not merely other calls to the changed helper.

- Identify the actual failure mechanism and the minimal state or code
  pattern needed to trigger it (such as an uninitialized pointer,
  mismatched flags, unchecked bounds, or a missing lifecycle step).
- Search nearby functions, sibling paths, analogous helpers, other MM
  subsystems and relevant configurations for the same mechanism.
  Check old and new paths, including exceptional, disabled-feature,
  fallback, teardown and initialization cases.
- For each candidate, trace a concrete caller and preconditions to
  establish whether the problematic state is reachable. Compare its
  initialization, locking and lifetime guarantees with the patched site.
- Distinguish confirmed additional bugs, suspected analogues, already
  protected code and unrelated lookalikes. Do not infer a bug from a
  matching name or textual pattern alone.
- Consider whether a narrow patch fixes only one manifestation of a
  broader issue. Report any verified siblings and recommend the smallest
  appropriate scope; avoid unnecessary refactoring.
- Include the similar-code search in the two-pass coverage comparison,
  and explicitly say when it was limited by available source access.

## Independent pass: additional review obligations

- Start from the intended userspace behavior: what the bug does to real
  programs, the conditions that trigger it, and the expected correction.
- Read every hunk and identify changed branches, checks, allocations,
  frees, locking transitions, ownership and object lifetime changes.
- Trace success, retry, signal, OOM, teardown, rollback and partial
  failure where relevant. Inspect call chains and preconditions rather
  than trusting helper names, comments or review summaries.
- Check refcounts, RCU, locking, MMU/page-table lifecycle, address/PFN
  arithmetic, overflow, return values, ABI and all applicable Kconfigs.
- For concurrency, identify actors and shared data; show an explicit
  interleaving and test it against locks, references and barriers.
  Distinguish a state-machine interleaving from LKMM ordering.
- Consider the strongest counterargument to each suspected bug, then
  resolve it with actual source. Do not report defensive programming
  suggestions without a reachable failure.

## Changelog and review standards

- For EVERY bug fix, require a prominent, concrete statement of the
  userspace-visible RUNTIME effects of the original bug. Do not stop at
  internal mechanics, a warning, a counter or a missing lock if more
  specific runtime consequences can be established.
- Distinguish observed/reproduced effects, source-supported possible
  effects, and speculation. Avoid claims of exploitation, disclosure,
  corruption or crashes without a well-supported execution path.
- Check trigger conditions, how the fix changes the observable outcome,
  and whether regression tests actually exercise the original failure.
- Review `Fixes:`, stable suitability, patch ordering, changelogging,
  comments, API semantics, coding style, and both expected and unexpected
  behavior changes. Favor concrete replacement wording over vague advice.
- When evaluating a disputed result, review the exact runtime mechanism.
  External AI reviews, human comments, and docs provide leads, not proof.

## Modeling and verification

Use Tejun's Sections 7-9 for the formal-model decision and protocol.
The following local safeguards are additive:

- Use PlusCal/TLC for a meaningful multi-actor shared-state protocol
  when appropriate, not mechanically for every change. The model must
  represent the actual C paths and their assumptions; record exclusions.
- Falsify the model: the old or deliberately broken variant should
  exhibit the relevant invariant violation. A clean patched run without
  a failing reference model is weak evidence.
- Record real TLC commands, configuration, bounds, state count and tool
  version. A tiny passing model is not a proof of general correctness.
  Translate counterexample steps back into reachable C operations.
- Use herd7/LKMM for claims about release/acquire, barriers or hardware
  reordering. TLC's sequential-consistency model cannot verify them.
- When a tool is unavailable, say so rather than implying it ran.
  `model: no (reason)` is appropriate for local arithmetic, simple
  finite conditions and changes protected by one lock.

## Reporting and email formatting: mandatory

These requirements apply to ALL user-facing replies, review summaries,
suggested changelogs and proposed emails. They are AKPM's preferences,
not edits to Tejun's original document.

- Plain 7-bit ASCII only. No curly quotes, Unicode punctuation,
  decorative bullets, typographic quotation bars, or special symbols.
- Hard-wrap all authored text at 75 columns, including quote prefixes,
  bullets and indentation. Unbreakable identifiers and URLs are the
  only exceptional cases; do not reformat quoted source unnecessarily.
- For email quotations, use literal `> ` at the start of EVERY quoted
  line. For ordinary bullets use `- `, never a rendered bullet glyph.
- For a copyable proposed email/review reply, use a literal `text` code
  block, not a rich-text writing block or rendered Markdown list or
  blockquote. The text must copy AS IS, without inserted backslashes,
  formatting characters or altered bullets/quotes. Verify it first.
- Refer to a numbered patch by its subject notation, e.g. `[1/2]` or
  `[2/3]`, not `patch 1` or `patch 2` in the email reply.
- State the verdict and important defects first. For each material
  finding, give the patch, precise code site, triggering path, failure,
  userspace impact, and a practical corrective action or test.
- Separate confirmed defects, unresolved concerns, and tests you merely
  recommend. No confidence inflation; source review is not a test run.
- For patch series, account for defects present at patch N that a later
  patch repairs. Note material changelog deficiencies and evidence gaps.
- Keep the final response compact and useful. Do not recite the review
  methodology or a checklist unless specifically requested. Provide
  plain-ASCII, 75-column, LKML-ready email text when asked.

## Handoff for subsequent chats

Use `akpm-patch-review-workflow.md` as the entry point and attach
`tj-patch-review-workflow.md` alongside it. Treat Tejun's file as a
read-only, verbatim upstream reference. Never modify it while refining
AKPM's local preferences. Amend only this file when new local rules are
requested. The former `kernel-patch-review-workflow.md` is obsolete.
