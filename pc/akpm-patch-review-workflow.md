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

## Chris Mason prompt version pinning and update tracking

Tejun's S2 workflow says to `git pull` Chris Mason's prompts before
review. Add the following requirements without editing Tejun's file:

1. Complete and record the independent first pass BEFORE reading Chris's
   prompts. At the start of the Tejun-guided pass, check the current
   HEAD commit SHA and date of the default branch of
   https://github.com/masoncl/review-prompts for EACH review. When
   unchanged, reuse verified prompt files pinned to that exact SHA if
   available; otherwise fetch them. Never reuse an unverified cache.
2. Load ALL required Chris prompt files from exactly that one SHA, using
   a checkout pinned to it or source requests with `ref=<full SHA>`.
   Include core, technical, false-positive, build, the subsystem
   index, and all triggered guides and patterns. Never combine files
   from different revisions or assume unversioned GitHub requests
   provide a consistent snapshot.
3. In the review's `review-activity.md` entry, record the full prompt
   SHA, its commit date, the date checked, and whether all required
   files were successfully loaded. Cite that SHA in the combined review
   when reproducibility matters. Never retroactively invent a SHA for
   earlier reviews where the prompt version was not recorded.
4. On each review check only the HEAD SHA and fetch relevant prompt
   content as needed. Perform substantive upstream diff/lesson analysis
   no more than once in seven days while reviewing, unless a particular
   change directly affects the current patch. Record meaningful MM,
   locking, concurrency and false-positive changes and SHAs in the
   small tracking section of `review-activity.md`. No full-history scan
   or repeated analysis of unchanged commits.
5. When reviewing author feedback or reassessing a previous finding,
   distinguish improvements in the kernel source from changes in the
   prompt version. If an older review has a known prompt SHA, use it to
   reproduce that review before comparing with current upstream prompts.
6. If GitHub access, SHA resolution, or required prompt files fail,
   state exactly what could not be verified. Do not label the prompt
   version current, pinned, or complete without evidence.

Treat newer prompts as updated review instructions, not automatic proof of
better results. Keep AKPM-specific methodology in THIS file, review state
and upstream change tracking in `review-activity.md`, and Tejun's file
unchanged. Refresh on review runs or explicit request; do not claim
continuous monitoring between reviews.

## Sashiko: upstream comparison without clone-and-own

Upstream: https://github.com/sashiko-dev/sashiko

- In an active reviewing period, check Sashiko's HEAD and analyze its
  relevant methodology/prompt changes at most once every seven days,
  or on explicit request. Record last-checked date and SHA in
  `review-activity.md`. Do NOT do a full Sashiko comparison per patch.
- When changed, inspect only relevant review-protocol changes and
  Sashiko-specific MM guidance that differs from the pinned Chris
  version. Compare against Chris's exact SHA, not unpinned branches.
  Neither project's prompts prove kernel behavior without code evidence.
- Do not clone-and-own Sashiko's Rust pipeline or its forked prompt
  tree. Distill only small, general review procedures into THIS file;
  otherwise read relevant upstream material by pinned SHA on demand.
- During two-pass reconciliation, retain substantial hypotheses that
  either pass examined and dismissed, with the actual disproving code.
  A disagreement or weakly proven dismissal is a "disputed finding":
  formulate one concrete verification question and investigate the
  competing explanations in the exact kernel source. Check all relevant
  callers, macros, configurations and lifecycle modes. Preserve
  CONFIRMED, REJECTED and UNRESOLVED outcomes; never force certainty.
- When merging findings, retain distinct setup, runtime, retry and
  teardown paths and their different failure mechanisms. Multiple
  reviewers making the same claim is not a substitute for proof.
- Keep this targeted: no separate Sashiko execution on routine reviews.

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

## Review activity, feedback and archive protocol

Keep review state outside the permanent workflow. This file describes
HOW to review; `review-activity.md` records WHICH reviews remain open.
The latter also indexes closed or dormant records in dated archives.

1. At the start of a substantive patch review, create or update a
   compact entry in `review-activity.md` if writable. Key it by the
   original `Subject:` after removing `Re:` and patch/version/series
   brackets for lookup. Retain the exact original Subject, version,
   author, patch link/Message-ID, base SHA, and related series subjects
   in the detailed record. Disambiguate collisions by Message-ID/base.
2. Assign stable review and finding IDs. Record claimed defect, concrete
   execution path, evidence, uncertainty, practical impact and any
   proposed reply. Distinguish our source analysis from external review
   assertions. Do not reproduce full patch bodies or mailing-list
   threads when a Message-ID or commit identifies them.
3. Treat dispositions as feedback, not as confidence labels. Use:
   `PENDING`, `CONFIRMED`, `REJECTED`, `PARTIAL`, `UNRESOLVED`, or
   `SUPERSEDED`. Until an author or other corroborating evidence weighs
   in, our own source verification alone does not mean `CONFIRMED`.
4. When new feedback arrives, reopen the entry, attribute the feedback,
   verify its concrete counterargument against the actual source and
   update each finding's disposition independently. For rejections,
   record the EXACT false assumption, actual guarding condition or
   misunderstood API, and evidence disproving the finding. For accepted
   findings, record why the original review found the problem. Then
   ask: what general verification rule would prevent the same error?
5. Identify the failure mode of OUR REVIEW (missed producer/consumer,
   unexpanded macro, wrong config, invalid lifetime/locking invariant,
   mistaken impact, etc.), not merely whether the patch was accepted.
   Test each proposed lesson against other plausible paths to avoid
   overfitting. Promote a SHORT high-level rule to THIS file only when
   genuinely useful across patches; leave specifics in the ledger.
   Do not edit Tejun's workflow.
6. Archive records which are resolved or sufficiently dormant to be
   removed from the active working set. Use one file per local close-off
   date, `review-activity-YYYY-MM-DD.md` (America/Los_Angeles). Several
   reviews may share that file. An archived `UNRESOLVED` review is
   *dormant*, not approved or rejected by its author.
7. When archiving, MOVE the compact record out of the active section;
   leave a Subject-to-filename mapping in the index. Retain the finding
   dispositions, counterarguments, durable lesson and source references
   in the archive. Remove superseded detail and transcript repetition.
   Archive files are snapshots: normally append to the day's file, but
   do not rewrite previous snapshots just to tidy the active index.
8. When a topic resurfaces in another chat, consult the active/index
   file by normalized Subject and identify its exact archive filename.
   Read that archive before resuming; request that file if unavailable.
   Copy only the still-relevant state back to the active entry, preserve
   the archive link and finding IDs, and update the index to `ACTIVE`.
   On a later close-off, use that day's archive with a backlink.
9. Periodically remove obsolete or uninteresting Subject mappings from
   the active index. Do not silently erase unresolved findings or
   author feedback; historical dated archives may stay in the git tree.

## Lore feedback check: weekly, with immediate manual follow-up

- A weekly Monday-morning scheduled check (America/Los_Angeles) looks
  for NEW public replies to ACTIVE entries in `review-activity.md`.
  It uses exact Message-IDs where known and otherwise verified subject
  matches. It does not monitor dormant reviews or unsent draft replies.
- Record per thread: original Message-ID, our sent reply ID if known,
  last-seen reply IDs, last-check date, and meaningful dispositions.
  Unrecorded IDs are UNKNOWN, never fabricated. Do not assert that a
  thread was checked if Lore or the source file was inaccessible.
- Scan new author/maintainer objections, corroboration, tests and new
  patch revisions. Distinguish responses to OUR finding from generic
  discussion. Inspect exact code at the relevant patch version before
  assigning CONFIRMED, REJECTED, PARTIAL, UNRESOLVED or SUPERSEDED.
- Deliver only meaningful changes; no weekly no-news notification.
  Any feedback the user brings to chat gets assessed immediately,
  without waiting for the scheduled check.
- Primary output is the GENERAL REVIEW LESSON: our claim, concrete
  author feedback, evidence confirming/refuting it, mistaken premise,
  and a concise cross-patch rule that prevents recurrence. Update the
  activity ledger first; only promote proven general rules into this
  file. Do not copy email transcripts into workflow documentation.
- A scheduled task cannot be assumed to see files modified only in
  the user's local Git tree. Use a current accessible ledger if one is
  available; otherwise report access limits and do not claim durable
  updates. Never modify GitHub repositories without permission.

A new chat normally needs `akpm-patch-review-workflow.md`,
`tj-patch-review-workflow.md`, and `review-activity.md`. Retrieve dated
archives only for the topics being resumed; do not preload them all.

## Handoff for subsequent chats

Use `akpm-patch-review-workflow.md` as the entry point and attach
`tj-patch-review-workflow.md` alongside it. Add `review-activity.md`
when continuing reviews or incorporating author feedback, and supply
only the archived `review-activity-YYYY-MM-DD.md` file indicated by its
index for a resumed dormant subject. Treat Tejun's file as a read-only,
verbatim upstream reference. Never modify it while refining AKPM's
local preferences. The former `kernel-patch-review-workflow.md` is
obsolete; do not attach it.
