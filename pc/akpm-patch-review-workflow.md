# AKPM kernel patch review workflow

Purpose: local review policy for future ChatGPT kernel patch reviews.
This is the entry point. Tejun's current generic review workflow is at
https://github.com/htejun/kernel-agent-workflows; fetch its relevant
modules at a pinned commit. This file provides AKPM-specific additions
and overrides. Chris Mason's prompts are a separate upstream source.

The original `tj-patch-review-workflow.md` (S2) is a retired, read-only
historical reference. Do not load it for routine reviews, modify it or
delete it without authorization. The older
`kernel-patch-review-workflow.md` is also superseded.

## Standalone handoff

This file alone is sufficient as the review-policy handoff for a NEW
patch or series. The reviewer must also have the submitted patch and
access to its matching kernel source and public upstream review guides.
Fetch Tejun's modules and Chris Mason's prompts by verified commit SHA
as described below. No local Tejun copy or AKPM activity ledger is
needed to perform the review.

`review-activity.md` contains AKPM's active cases, prior feedback and
upstream version checkpoints, not additional review methodology. It is
OPTIONAL for fresh reviews. If absent, put the review's identifiers,
findings, evidence and upstream SHAs in the review report. Establish an
initial checkpoint where no previous SHA is known; do not invent an
upstream comparison or previous finding. The ledger (and any indicated
dated archive) is needed to CONTINUE an existing AKPM review.

AKPM's weekly Lore feedback monitor is not part of this file and does
not automatically run for another reviewer.

## Execution order: two separate review passes

For every review, including single patches and mbox series:

1. First perform an independent, first-principles review of the entire
   submitted change against the relevant kernel source. Do not consult
   Tejun's instructions or Chris Mason's or Sashiko's prompts to choose
   review questions or findings in this pass. Preserve the findings and
   the paths checked before proceeding.
2. Then read and apply Tejun's pinned `review/patchset-review.md`
   module and its applicable dependencies as a separate pass. Use Chris
   Mason's pinned prompts at https://github.com/masoncl/review-prompts.
   Load core, technical, false-positive, build, and matching subsystem
   guidance. Verify all leads against source code. A prompt's
   declaration that something is wrong is not evidence by itself.
3. Reconcile the two passes. Compare their path coverage, not just their
   reported bugs. Investigate paths checked by only one pass, resolve
   disagreements, eliminate false positives, and deliver ONE combined
   judgment. Keep bug proof, fix proof and architectural suitability
   distinct. Indicate the origin of a finding when informative.

Both passes must use their own producer/consumer inventory and inspect
all relevant paths. Do not simply relabel one pass as two. If the tools
do not permit Tejun's suggested parallel reviewers, do two genuinely
separate sequential analyses and disclose that limitation. Do not claim
that subagents, builds, runtime tests, TLC, or herd7 ran unless they did.

The independent pass is required even when the prompt-guided pass is
much deeper. Neither pass has veto power over the other.

## Tejun upstream modules and upgrade tracking

Tejun's current workflow is
https://github.com/htejun/kernel-agent-workflows. After recording the
independent pass, check the default-branch HEAD SHA and commit date at
each substantive review. Fetch all applicable modules from ONE full SHA
(or reuse complete, already verified copies if unchanged), starting
with `review/patchset-review.md` and its relevant `Depends on` modules.
These include `core/evidence-discipline.md`, `code/kernel-idioms.md`,
`review/formal-model-check.md`, and the relevant `patches/` guides.
Use `mail/lore-thread.md` when retrieving posted discussions.

When HEAD advances from a known checkpoint, compare the revisions:
read additions to `UPGRADING.md` and only the relevant module diffs.
Record the SHA, check date and material changes or conflicts in the
activity ledger if present, otherwise in the review report. With no
previous checkpoint, record the initial SHA without claiming a diff.
AKPM-specific policies here prevail on conflicts;
never silently weaken them or infer an upgrade from unverified files.
If upstream access fails, disclose which version or module was not
verified. Do not mix modules from different SHAs in a review.

`INTEGRATION.md` also describes installing a persistent local agent
profile, overlays, and instruction-file hooks. Do not install those for
ChatGPT reviews or alter any Git checkout without express permission.
Use the upstream modules read-only, not a local copy to maintain.
The original standalone S2 file is kept only for historical comparison.

## Chris Mason prompt version pinning and update tracking

Tejun's `review/patchset-review.md` uses Chris Mason's prompts.
For our reviews, apply these additional version-pinning requirements:

1. Complete and record the independent first pass BEFORE reading Chris's
   prompts. At the start of the Tejun-guided pass, determine the current
   HEAD commit SHA and commit date on the default branch of
   https://github.com/masoncl/review-prompts. Check HEAD afresh for EACH
   review. Reuse complete, previously verified, SHA-pinned prompt files
   when the SHA is unchanged; otherwise fetch the new revision.
2. Load ALL required Chris prompt files from exactly that one SHA, using
   a checkout pinned to it or source requests with `ref=<full SHA>`.
   Include core, technical, false-positive, build, the subsystem
   index, and all triggered guides and patterns. Never combine files
   from different revisions or assume unversioned GitHub requests
   provide a consistent snapshot.
3. In the review record (`review-activity.md` when maintained,
   otherwise the review report), record the full prompt SHA, its commit
   date, the date checked, and whether all required files were loaded.
   Cite that SHA in the combined review
   when reproducibility matters. Never retroactively invent a SHA for
   earlier reviews where the prompt version was not recorded.
4. When the SHA advances from a known checkpoint, briefly inspect the
   upstream diff, especially MM, locking, concurrency, false-positive
   guidance and `review-core.md`. Record significant changes and SHAs
   in the activity ledger if present, otherwise the review report.
   With no previous checkpoint, record the initial SHA without a diff.
   Do not copy entire upstream commit logs or prompts into local files.
5. When reviewing author feedback or reassessing a previous finding,
   distinguish improvements in the kernel source from changes in the
   prompt version. If an older review has a known prompt SHA, use it to
   reproduce that review before comparing with current upstream prompts.
6. If GitHub access, SHA resolution, or required prompt files fail,
   state exactly what could not be verified. Do not label the prompt
   version current, pinned, or complete without evidence.

Treat newer prompts as updated review instructions, not automatic proof of
better results. Keep AKPM-specific methodology here. Keep review state
and upstream tracking in an activity ledger when used, or in the review
report for standalone work; all external sources remain read-only.
Refresh on reviews or explicit requests; do not claim
continuous monitoring between reviews.

## Selective Sashiko integration

Chris Mason's `masoncl/review-prompts` remains the primary external
prompt source. `sashiko-dev/sashiko` is supplemental: adopt useful MM
review techniques, not its prompt set or multi-stage review pipeline.
Sashiko vendors Chris's prompts and may alter them, notably
`third_party/prompts/kernel/subsystem/mm-vma.md` and
`third_party/prompts/kernel/false-positive-guide.md`. Treat categorical
Sashiko-specific rules as hypotheses, not authority: some may hide bugs.

During active reviews, check Sashiko's default-branch HEAD at most once
per seven days (the next interaction after seven days, not a background
process). Compare only if its SHA advanced, and inspect only relevant
MM, concurrency, false-positive and methodology changes. Record the
full SHA, check date, comparison date and adopted changes in the
activity ledger if present, otherwise the review report. Without a
prior checkpoint, record the initial SHA without claiming a comparison.
Carry forward vetted techniques; do not redo an
upstream methodology comparison for each patch.

Apply these refinements within the existing two-pass review:

- In BOTH passes retain substantive, plausible hypotheses that were
  dismissed, with the exact source evidence, guard or precondition
  supporting dismissal. Omit trivial or unsupported speculation.
- If reviewers disagree, or dismissal depends on an unverified premise,
  conduct a focused third examination. State arguments for and against,
  frame the specific technical question, and trace source, callers,
  callees, macros, configurations and lifecycle paths. Distrust both
  the finding and its dismissal. Conclude `CONFIRMED`, `REJECTED` or
  `UNRESOLVED` from evidence; never force an unresolved claim to be
  confirmed. This technical assessment does not override the
  author-feedback disposition policy below.
- During reconciliation, deduplicate repeated reports, but preserve
  distinct execution paths, lifecycle stages and consequences even if
  they share a root cause.

Do not read Sashiko prompts in the independent pass, create a mandatory
Sashiko review pass, or copy or maintain its upstream workflow locally.

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

## Architectural and historical framing: BOTH passes

Do not accept the patch's framing without checking it. Distinguish a
real problem, a safe repair, and a suitable design. Use these questions
within the existing passes, not as another full review pipeline:

- Identify the actual workload, observable goal and bottleneck. Connect
  measurements to the proposed mechanism; distinguish synthetic stress,
  representative workloads and effects on competing operations. Keep
  deployment constraints separate from general upstream requirements.
- Identify the contract and its owner before adding another exception.
  For overloaded flags or results, distinguish progress, lock ownership,
  retry eligibility and mandatory fallback using the existing coverage
  inventory. Shared spelling does not establish shared semantics.
- Before removing or weakening a lock, check, retry rule or other
  safeguard, inspect why it was introduced: relevant history, fixes,
  reverts, discussion and reproducers. State which old failure it blocks
  and what changed to make that protection unnecessary. Follow moved
  code where needed; unknown history is not evidence of redundancy.
- Trace the whole operation, including changes to source/parent objects,
  cached state and deferred completion. Identify which protection spans
  that operation and what lower-level code assumes. A local lock or a
  harmless userspace interleaving does not prove the full protocol safe.
- Ask whether the change removes work or moves waiting and risk to other
  callers. Repeated policy in architecture or subsystem wrappers is a
  reason to consider a common owner. Count new states, exceptions and
  future synchronization work, not only changed lines. Do not demand an
  unrelated redesign merely because shared code would be cleaner.
- Compare the bounded workaround with the structural alternative and
  the status quo. Separate correctness findings from architectural and
  performance tradeoffs. An interim improvement may be worth taking,
  but name its scope and remaining debt; a simpler-looking alternative
  needs the same evidence and fix proof as the submitted patch.

Keep this proportional: a brief framing check for routine patches;
expand targeted history and design analysis only for material questions.
Reuse verified context. Record consequential rejected alternatives and
why they failed in the review record, with references, so later versions
and chats do not restart a settled design discussion. Reopen a rejection
when its premises change. Do not turn these examples into special rules
for individual patches or treat maintainer recollection as proof.

## Separate bug proof from fix proof: mandatory in BOTH passes

Demonstrating the old failure does not establish that the proposed fix
is correct. Treat these as two separate proof obligations:

- Bug proof: trace a reachable old-code path to the reported observable
  failure, distinguishing reproduction from inferred consequences.
- Fix proof: enumerate what the patch changes for ALL relevant paths,
  configurations, owners and lifecycle stages, not just the reproducer.
  State the invariant that must hold when new behavior becomes visible,
  including who can still access or release the affected object.
- Check the earliest point at which the new state, flag or decision is
  published. Follow outstanding references, sharing, error cleanup,
  asynchronous work, retries, and concurrency across that point.
- Verify that the fix removes the original failure without creating a
  new failure or suppressing a legitimate recovery path. Compare both
  the old and new results for each reachable state class.
- Where fix safety rests on a premise not established by source, mark it
  UNRESOLVED and name the missing guard, ordering rule or test. Do not
  turn proof of the original failure into presumed proof of the repair.

Apply this explicitly during reconciliation; keep the two proof results
separate even when an author has supplied a convincing reproducer.

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

## User-visible impact and changelog gate: mandatory for EACH bugfix

Bugfix changelogs must answer "why should users care?" BEFORE spending
most of their space on internal code mechanics. The changelog is a durable
diagnostic and backporting resource for upstream, -stable, distro/vendor
maintainers, and operators investigating affected deployed kernels.

In BOTH review passes, independently determine and check:

1. The observable failure: what a user, program, service, administrator,
   or fleet sees (errno, wrong output, stale data, timeout, hang, crash,
   data loss, performance/latency regression, resource exhaustion, etc.).
   Identify the affected operation/workload, trigger and configuration.
   Include a distinctive diagnostic signature (log, warning, trace,
   metric, command or reproduction) where one is established. State when
   a failure is silent and what measurement reveals it.
2. Scope and impact: which users or systems can hit it, required privileges
   and configuration, affected versions when verified, observed severity,
   and credible worst-case consequences. Distinguish *observed* results,
   source-supported possible outcomes and conjecture; never upgrade an
   internal warning or hypothetical race into a claimed fleet crash or
   exploitable security issue without an established path. Lack of any
   reported incident does NOT make a real, attacker-triggerable bug
   unimportant: an adversary can deliberately repeat a rare trigger.
   For that case, identify the attacker's accessible entry point,
   controllable inputs, required privilege/configuration, how repeated
   attempts reach the defect, and the credible harmful consequence.
   Distinguish demonstrated exploitation, source-supported attack paths,
   and merely imagined exploits. Do not require known victims or a
   reliable proof-of-concept when the harmful path is established.
3. Expected improvement: what changes from the affected user's point of
   view after applying the fix. Keep mechanism and fix explanation, but do
   not let them substitute for the preceding user-facing information.
4. Operational lookup: would someone with a report from a production
   6.x.y kernel recognize that this fix applies? Check that the changelog
   has enough conditions, symptoms and evidence to match the report and
   decide whether a downstream backport is worth the regression risk.
5. If NO userspace-visible runtime effect is known, require a concise,
   explicit statement to that effect, justified by the paths reviewed.
   If impact is unknown or has not been traced, say so: do NOT conflate
   "not demonstrated" with "none". Investigate plausible consequences
   yourself first, then request targeted author clarification if needed.
   For a series, the [0/N] may summarize a proven no-effect conclusion,
   but each bugfix still needs sufficient standalone explanation.

Treat missing or weak impact description as a substantive changelog
finding, even when the code fix is correct. Supply concrete replacement
text or the exact question to ask the author, not just "more detail".
The observed/possible/unknown distinction is part of the fix-proof gate.

## Stable-backport eligibility gate: mandatory for EACH patch and series

Source (read and verified 2026-10-17):
Documentation/process/stable-kernel-rules.rst, Linux mainline
https://www.kernel.org/doc/html/latest/process/stable-kernel-rules.html
Also read Documentation/process/submitting-patches.rst, especially
"Describe your changes", "Fixes:" and stable-tag instructions.
Apply the following actual stable rules, not a generic preference for
backporting all fixes:

- A fix (or equivalent) must already be in mainline for actual -stable
  inclusion. A proposed upstream patch can be a *prospective candidate*;
  do not call it already eligible or reject its tag merely because it has
  not yet landed.
- The change must be obviously correct, tested, and at most 100 lines
  WITH context, and follow submitting-patches.rst. Check evidence of
  testing; an author's claim is not a test run performed by us. For
  individual patches in a series, assess each commit independently.
- The published rules cover real bugs with user benefit (or new
  device IDs), including crashes, hangs, corruption, security issues,
  build failures and hardware quirks. They also permit consideration
  of otherwise theoretical races when the changelog explains how the
  bug can be exploited, and reject trivial cleanups without benefit.
  "Real security issue" and "some 'oh, that's not good' issue"
  include demonstrated harmful failure paths not seen in production.
  An attacker may deliberately repeat an improbable race. Explain the
  accessible trigger, attacker control, repetition, and credible harm.
  The rule rejecting an unexplained "theoretical race condition" does
  not require a known victim, reliable reproduction, or weaponized
  exploit where the harmful path is already established by evidence.
  Keep the distinction between evidence and speculation explicit.
  This interprets the published rules; it is NOT a separate exception.
- A notable performance/interactivity issue reported by a distro user
  is a narrow exception: the rules call for submission by a distro
  kernel maintainer and an addendum with the bug report if available
  and further user-visible impact evidence. Do not equate any measured
  improvement with automatic stable suitability.
- Check whether the fix is applicable to supported stable branches:
  verify the introducing commit, relevant version/config scope,
  backport dependencies, risks and conflicts where data is available.
  Do not infer exact affected releases from a Fixes: tag alone. When
  requesting option 2 or 3 for particular series, ensure newer supported
  stable series also receive the fix or equivalent; avoid reintroducing
  the problem when users upgrade.

For every patch, report `stable: candidate / not justified / unresolved`
with a brief reason and a separate `impact-changelog: sufficient /
needs detail / no known effect (substantiated)`. An unexploited but
credible attacker-triggerable failure counts as potential user-visible
harm; absence of known incidents is not `no known effect`. For a series,
report per-patch results and a compact overall assessment; do not let a
cover letter replace each standalone commit message. If the code
is correct but the changelog omits WHY stable recipients need it,
explicitly request an impact description BEFORE recommending its stable
submission. "Fixes:" and "Cc: stable" are routing metadata, not a
substitute for that explanation.

Use the documented submission routes correctly:

- Preferred option 1: for a prospective upstream stable candidate, add
  `Cc: stable@vger.kernel.org` in the commit trailer/sign-off area (NOT
  merely the email header). `Fixes:` assists version selection but does
  not replace the stable tag. Where an actual non-public disclosure is
  being maintained, the rules document `Cc: stable@kernel.org` to avoid
  exposing a fix through ordinary public mailing-list delivery.
- Option 2: for an already mainlined fix, email stable@vger.kernel.org
  with subject, commit ID, why it is needed and requested kernel series.
- Option 3: for an adapted downstream backport, include the exact
  upstream commit identification (`commit <sha> upstream.` or
  `[ Upstream commit <sha> ]`), target series and justification for each
  deviation from the upstream version.
- When relevant, use documented stable-tag inline comments for version
  bounds, prerequisite commits, delayed pickup or known adjustments.
  Use `stable+noautosel@kernel.org` with a stated reason when explicitly
  asking the stable tooling not to select a change automatically.

Do not speculate that a patch meets the stable rules just because it
has a Fixes: tag, or because it is correct. For `stable: unresolved`,
name what is missing (impact, tests, mainline status, target versions,
size or prerequisites). Do not submit anything to -stable on behalf of
the user unless expressly instructed. For security issues, consult
Documentation/process/security-bugs.rst instead of relying solely on
normal stable review.

Security/publication and stable timing: do not assume there is an
embargo, coordinated-release schedule, or other separate security
process merely because `security@kernel.org` is on the email. Respect
actual confidentiality instructions and keep private material private.
Once an upstream fix is public, the change may reveal enough about the
bug for an attacker to target unpatched systems. Therefore recommend
prompt -stable pickup of qualifying fixes, not waiting for undefined
"security handling" to finish. Give the concrete impact, affected
versions, prerequisites and stable routing steps; do not claim that an
upstream merge alone protects deployed stable kernels. If a real
coordination or disclosure constraint exists, state it specifically
instead of inventing a generic prerequisite.

## Other changelog and review standards

- Verify Fixes: history, patch ordering, individual versus series scope,
  comments, API semantics, coding style and any unexpected behavior
  changes. Favor a precise corrected paragraph over vague advice.
- Check regression tests actually exercise the old failure, and compare
  the change against the userspace-visible outcome, not merely the
  repaired helper's local behavior.
- External AI reviews, human comments and docs offer leads, not proof:
  verify disputed behavior against source and reachable call paths.

## Modeling and verification

Use Tejun's pinned `review/formal-model-check.md` for model triggers,
procedure, and verification. Make an explicit `model: yes` or
`model: no (reason)` decision for each review, even though Tejun's
profile defaults `$FORMAL_MODEL` to `off`. That default does not waive
our review: model consequential multi-actor protocols and unresolved
interleavings when warranted, not every routine arithmetic change.
These local safeguards are additive:

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
suggested changelogs and proposed emails. These AKPM preferences
override conflicting upstream style defaults.

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
- Every completed patch or patchset review MUST end with a short,
  copy-ready email reply suitable for sending to the author or thread,
  even when there are no objections. State take/revise/reject clearly;
  mention only actionable findings, essential qualifications and, when
  useful, the precise changelog or stable-tag request. Do not repeat the
  full analysis or invent a positive Reviewed-by tag. Keep a private
  security-thread reply private, without reproducer or exploit detail.
  Do not defer -stable recommendations with vague "security handling"
  language; name an actual restriction only when established. Draft only;
  never imply the message was sent.
- Refer to a numbered patch by its subject notation, e.g. `[1/2]` or
  `[2/3]`, not `patch 1` or `patch 2` in the email reply.
- State the verdict and important defects first. For each material
  finding, give the patch, precise code site, triggering path, failure,
  userspace impact, and a practical corrective action or test. Include
  the concise impact-changelog and stable assessment for each bugfix.
- Separate confirmed defects, unresolved concerns, and tests you merely
  recommend. No confidence inflation; source review is not a test run.
- For patch series, account for defects present at patch N that a later
  patch repairs. Note material changelog deficiencies and evidence gaps.
- Keep the final response compact and useful. Do not recite the review
  methodology or a checklist unless specifically requested. Provide
  plain-ASCII, 75-column, LKML-ready email text when asked.

## Review activity, feedback and archive protocol

Keep review state outside the permanent workflow. This file describes
HOW to review; an optional `review-activity.md` records WHICH reviews
remain open, and indexes archived records. For a standalone review with
no ledger, keep the corresponding record in the review report.

1. At the start of a substantive patch review, create or update a
   compact ledger entry if available and writable; otherwise use the
   review report. Key it by the original `Subject:` after removing `Re:`
   and patch/version/series
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
4. For AKPM's ongoing cases, use the already scheduled weekly public
   Lore feedback check. Other reviewers do not inherit that schedule;
   inspect public feedback when continuing a review. Examine any
   author/maintainer response supplied in chat immediately.
   For meaningful feedback, reopen the entry, attribute the response,
   verify its technical claims against actual source and update each
   finding independently. For rejections, record the EXACT false
   assumption, guard or misunderstood API and the disproving evidence.
   For confirmations or partial rejections, identify any missed paths or
   mistaken dismissals. Distill what a future independent review should
   do differently to prevent false positives and false negatives.
5. Promote a lesson to THIS AKPM workflow only if it improves review
   methodology across patches. Do not append a special rule for every
   bug, false positive, or argument. Do not edit upstream modules.
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

For a NEW review, only `akpm-patch-review-workflow.md` is needed as
a policy document. Supply the patch or mbox and identify its base tree
if known. Fetch pinned upstream material on demand. To RESUME AKPM's
older reviews, also provide `review-activity.md` and the dated archive
identified by its index, if any.

## Handoff for subsequent chats

For fresh reviews, attach only `akpm-patch-review-workflow.md`, plus
the patch/mbox. After the independent pass, fetch the current pinned
Tejun modules and Chris prompts as directed above. When continuing
AKPM's previous findings or feedback, also attach `review-activity.md`
and only the relevant dated archive. Do not attach the historical
`tj-patch-review-workflow.md` or `kernel-patch-review-workflow.md`.
Neither file should be modified or deleted without authorization.
