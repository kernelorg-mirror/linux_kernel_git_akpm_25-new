# AKPM kernel patch review workflow

Purpose: local review policy for future ChatGPT kernel patch reviews.
This is the entry point. Tejun's current generic review workflow is at
https://github.com/htejun/kernel-agent-workflows; fetch its relevant
modules at a pinned commit. This file provides AKPM-specific additions
and overrides. Chris Mason's prompts and Sashiko's full review
coverage are separate upstream sources.

The original `tj-patch-review-workflow.md` (S2) is a retired, read-only
historical reference. Do not load it for routine reviews, modify it or
delete it without authorization. The older
`kernel-patch-review-workflow.md` is also superseded.

## Standalone handoff

This file alone is sufficient as the review-policy handoff for a NEW
patch or series. The reviewer must also have the submitted patch and
access to its matching kernel source and public upstream review guides.
Fetch Tejun's modules, Chris Mason's prompts, and Sashiko's review
instructions by verified commit SHA as described below.
No local Tejun copy or AKPM activity ledger is needed to perform
the review.

`review-activity.md` contains AKPM's active cases, prior feedback and
upstream version checkpoints, not additional review methodology. It is
OPTIONAL for fresh reviews. If absent, put the review's identifiers,
findings, evidence and upstream SHAs in the review report. Establish an
initial checkpoint where no previous SHA is known; do not invent an
upstream comparison or previous finding. The ledger (and any indicated
dated archive) is needed to CONTINUE an existing AKPM review.

AKPM's weekly Lore feedback monitor is not part of this file and does
not automatically run for another reviewer.

## Execution order: independent review plus two coverage tracks

For EVERY review, including single patches and mbox series, cover the
entire change by three distinct analyses and an evidence-based merge:

1. Perform and record an independent first-principles review against
   relevant kernel source, without consulting Tejun, Chris Mason or
   Sashiko prompts to choose questions or findings. Capture the paths
   checked, hypotheses, dismissed concerns and supporting evidence.
2. Perform the mandatory Sashiko coverage track specified below. Use
   the current SHA-pinned Sashiko stage definitions and matching vendor
   guides. Independently examine its core and applicable specialist
   domains, retaining both candidate defects and rejected hypotheses.
   Do not substitute familiarity with its README or another prompt set
   for actually performing the analyses. Native Sashiko execution, when
   available and authorized, is additional evidence, not a substitute
   for checking its findings against source.
3. Perform the Tejun- and Chris-Mason-guided track. Read Tejun's pinned
   `review/patchset-review.md` and applicable dependencies, and all
   triggered Chris prompts from a single pinned SHA. Independently
   check their distinct questions and source paths.
4. Reconcile ALL three tracks. Compare actual coverage, state classes,
   assertions, candidates and dismissals, not just reported bugs.
   Verify contradictions and unsupported dismissals; keep separate
   judgments about bug proof, fix proof and architectural suitability.
   Deliver one combined verdict with actionable findings.

Retain meaningful intermediate results until reconciliation. Sequential
analysis is acceptable when parallel models are unavailable, but do not
call it a native multi-agent Sashiko run or independent model consensus.
Do not claim an external analyzer, test, build or formal model was run
unless it actually ran. Neither upstream tool's verdict has veto power
and no review track may dismiss another's finding without code proof.

Sashiko-level coverage is a FLOOR, not a claim of matching its output:
LLM analyses are nondeterministic. The final report must say whether
native Sashiko ran, whether full applicable stage coverage was completed
manually, and any missing guides, tests or unverified paths. Do not
label a review "Sashiko-equivalent" if coverage is incomplete.

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

## Sashiko coverage floor: mandatory, not supplemental

Source: https://github.com/sashiko-dev/sashiko.

At the start of EACH substantive review, verify Sashiko's default-branch
HEAD and pin ONE full SHA for the entire coverage track. Read the actual
pipeline instructions from `src/workflows/linux_patch_review.rs`, plus
its current prompt-selection and verification definitions. Read the
applicable Sashiko-vendored core, technical, false-positive, subsystem
and pattern guides at that SAME SHA. These may diverge from Chris's own
prompts: never silently substitute one for the other. Reuse cached,
fully verified files only if the SHA is unchanged. Compare new versions
to the last known checkpoint when material, and record adopted changes.
Do not mix Sashiko source from different revisions, and do not assume
this document captures all future changes to its pipeline.

Sashiko currently has seven specialist analysis domains. Preserve their
separate questions, with independent consideration before consolidation:

- GOAL: challenge architecture, compatibility, intended invariant,
  alternative designs, system-wide costs and suitability of the layer.
- IMPLEMENTATION: verify every claimed effect, changed interface,
  contract, side effect, omitted caller, and valid input or object state.
- EXECUTION-FLOW: trace all changed branches, loops, success, errors,
  retries, cleanup, initialization and eventual observable outcomes.
- RESOURCES: follow allocation, reference, ownership, publication,
  asynchronous handoff, removal, reuse and teardown for every resource.
- LOCKING: map actors, locks, memory ordering, races, CPU/hotplug states,
  synchronization and lock inversions across callers and callbacks.
- SECURITY: trace trust boundaries, attacker-controlled inputs,
  bounds/overflow, disclosures, privilege and harmful failure paths.
- HARDWARE: where relevant, trace architecture variants, page-table or
  device contracts, DMA, barriers, interrupt and hardware state.

GOAL, IMPLEMENTATION and EXECUTION-FLOW are ALWAYS required. Evaluate
all four specialist domains for every patch; perform each whenever a
change may interact with its subject, even indirectly. Record a short
source-grounded exclusion reason for any omitted specialist analysis.
The pre-screen or author's subsystem label may not suppress relevant
coverage. For architecture-dependent generic code, HARDWARE includes
contrasting platform implementations, not only peripheral drivers.

Apply Sashiko's two-stage verification discipline as well:

1. Collect concrete concerns AND substantive dismissed concerns from
   every analysis domain. Do not allow early positive impressions in
   one domain to narrow or terminate another. Preserve distinct paths,
   cleanup stages and failure effects when merging duplicates.
2. Verify each finding and each dismissal. Demand positive code proof
   to dismiss an issue, across all relevant callers, modes and states;
   a typical caller, familiar architecture, happy path or an untested
   assertion is not sufficient proof. Do not treat several reviewers
   sharing an assumption as independent corroboration.
3. Route contested, partly supported or assumption-based dismissals to
   a focused HARD-CASE examination. Form a concrete verification
   question, trace both sides with source, and conclude CONFIRMED,
   REJECTED or UNRESOLVED. Revisit suspicious "harmless" side effects,
   omitted restore/cleanup and relied-on-but-unproven preconditions.
4. Check any candidate against the final state of a patch series before
   deciding it is still present; retain the original affected patch
   and bisectability assessment. Do not skip later hunks because an
   earlier concern has already been found.

A useful minimum counterexample search for each important new
condition, early exit, fast path or cleanup decision is: find a valid
state in which the check means something DIFFERENT from what the author
assumes. Trace that state from its producer to the eventual consumer.
For generic code, use contrasting implementations, configurations,
boot/runtime phases and repeated create/destroy or rollback/retry.
Establish the *final system state*, not just local branch correctness.
Also compare how much work the patch adds to normal successful paths.
These are general proof methods, not KASAN-specific rules.

When a native Sashiko runner and a suitable source tree are available,
run it for each authorized review. Obtain explicit approval before
third-party data transfer, especially for nonpublic security reports.
Read its findings and dismissals, verify each against source, and
reconcile them with the other tracks.
Do not assume a native Sashiko runner is present simply because its
GitHub source can be read. Without a runner, carry out the pinned stage
coverage manually and state "native Sashiko: not run". If any stage or
source cannot be accessed, say exactly what is missing rather than
claiming an unqualified coverage superset.

When a Sashiko report is supplied, audit it finding by finding against
our own candidates AND dismissals. For each valid additional finding,
trace why all our review tracks missed it, then rerun the revised method
on the missed case. Record the specific feedback in the activity ledger
and only the generalizable lesson here. A new rule is not validated
merely because it describes the missed bug: show how its review question
would expose the counterexample without knowing the bug in advance.

Our additional requirements remain mandatory ABOVE this floor:
independent first-principles analysis, Tejun/Chris coverage, historical
invariant reconstruction, source-verified bug/fix proofs, architectural
alternatives, analogous-bug search, all significant producers and
consumers, user-visible impact, stable suitability, and concise email
replies. Sashiko prompts are hypotheses and review methods, not proof;
evidence standards and AKPM delivery rules always still apply.

## Source integrity and review scope

- Read all relevant material in the supplied mbox: the actual patches,
  cover letter, earlier revisions, replies, test results and objections.
  Distinguish the proposed patch from older patches quoted in email.
- Trust the author to have used a suitable base for routine reviews.
  An exact base-commit SHA is not required and its absence is not a
  review finding or a routine caveat. Patch applicability and build
  compatibility are the practical tests; report them as verified only
  if actually checked. Do not spend time reconstructing a base solely
  to establish a bit-for-bit preimage match.
- Preserve patch ordering: assess each series commit with only its
  predecessors applied, so it remains independently correct and
  bisectable. Inspect the relevant surrounding implementation, callers,
  and error paths in a suitable source tree, not isolated diff snippets.
- When a patch does not apply, behavior materially differs by tree,
  history or ordering is consequential, or the author specifies a
  non-mainline tree, resolve the actual source context. Do not silently
  substitute mainline for `mm-new`, `mm-everything`, or `linux-next`.
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

## Architectural and historical framing: ALL tracks

Do not accept the patch's framing without checking it. Distinguish a
real problem, a safe repair, and a suitable design. Use these questions
in every relevant track, not only after a defect is found:

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
- When a fix adds a preparation scan, prefetch, readahead, or retry,
  measure its cost on the COMMON successful path, not just the reported
  failure: extra lookups, folio locks, waiting, drains, allocations,
  passes and I/O. Ask whether work needed only after an exceptional
  event can run on demand after unwinding held locks/references. Compare
  eager and deferred designs before recommending an upstream merge;
  a correct lock-order fix can still be unnecessarily expensive.
- Before introducing local retries or prepasses, examine higher callers
  for existing recovery and bounded retry machinery. Prefer one clear
  owner of each retry, with established status codes and cleanup; prove
  the alternative's locking, object lifetime and forward progress too.
- Treat each new branch, guard or cleanup decision as a claim about
  reachable states. Search for a legal counterexample instead of only
  confirming the motivating case. Check actual initial conditions,
  producers and callers before deciding a counterexample is impossible.
- Judge a repair by end-to-end observable state, not just local safety,
  balanced references or successful return. Follow its effects through
  later consumers and through cleanup, failure and subsequent reuse.
  Retaining an object does not prove that its retained state is valid.
- Apply the mandatory adversarial correctness gate below to state
  persistence, inverse operations and internal handler dispatch.
- For changes to generic code, examine contrasting implementations or
  configurations selected because their behavior or initial state can
  differ. Verify the relevant helper contracts in those environments;
  do not generalize from the motivating platform or usual lifecycle.
- Ask whether the new control flow can amplify work, change progress or
  replace a cheap fast path with an expensive path for some valid
  preexisting state. Check common-case and adverse-case costs at the
  scale actually encountered by callers.
- After establishing behavioral correctness, seek the simplest
  expression of the operation and its invariant. Prefer direct
  relationships between the actual inputs and outputs to derived
  offsets, redundant intermediate values, or reconstructed state.
  Compare clarity as a separate review dimension without requiring
  cosmetic changes that do not materially improve understanding.
- Choose a clean, maintainable UPSTREAM fix on its merits. Older stable
  branches may need separate adapted backports and validation; missing
  infrastructure there is not by itself a reason to complicate the
  upstream design or duplicate existing retry logic.

Keep this proportional: a brief framing check for routine patches;
expand targeted history and design analysis only for material questions.
Reuse verified context. Record consequential rejected alternatives and
why they failed in the review record, with references, so later versions
and chats do not restart a settled design discussion. Reopen a rejection
when its premises change. Do not turn these examples into special rules
for individual patches or treat maintainer recollection as proof.

## Separate bug proof from fix proof: mandatory in ALL tracks

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

## Added-guard reachability and necessity gate: EVERY patch

A general instruction to "question new checks" did not prevent a missed
redundant NULL test in an earlier review. This gate is a required
artifact with per-condition evidence, not a statement of intent.

1. During the first source/hunk walkthrough, inventory EVERY added or
   behavior-changed guard: `if`, `?:`, `switch` decision, error test,
   early return, fallback, bounds check, assertion or rejection. Split
   each `&&` and `||` expression into individually justified clauses.
   Include checks copied from nearby code, macros and helper wrappers.
   Give each clause or changed branch a `G01`, `G02`, ... identifier and
   a source location. Mark `none` only after checking every diff hunk.
2. For each guard, trace BACKWARD from its input to all relevant
   producers: file open, object creation, initial state, assignments,
   callbacks, direct/indirect callers, error exits and concurrent
   teardown. Verify the ACTUAL entry contract on the reviewed path,
   not the apparent purpose of the helper or behavior of a neighbor.
   In particular, determine whether a pointer can truly be NULL,
   ERR_PTR, stale or freed at that site, and whether a counter/flag
   can reach the value being rejected.
3. Write down a concrete, legal path which makes each clause true at
   that location. Name the upstream code and condition that permits
   it. If no such path exists, prove why: locate the earlier guard,
   successful-open guarantee, invariant or ownership rule excluding it.
   Do not manufacture an invalid state just to justify a check.
4. Establish INDEPENDENT NECESSITY: what distinct failure does this
   clause prevent that is not already prevented by caller contracts,
   another clause or an earlier guard? For compound conditions, test
   each clause removed while the others remain. Trace both outcomes
   through cleanup, errno, observable behavior and subsequent reuse.
   A checked condition can be harmless yet unnecessary.
5. Audit the DIAGNOSTIC CONSEQUENCE of each guard. Compare the
   behavior of the original code and the patch if the condition is
   true. Is it an expected userspace/runtime error, or a violation of
   an upstream internal contract? If the contract makes the condition
   impossible, an added error return or fallback may replace an Oops
   or warning with quiet apparent success or an ordinary errno. This
   masks a programming defect and weakens defect detection; report it
   explicitly, not as merely cosmetic redundancy. Preserve the
   visibility of impossible-state failures. Do not introduce new
   BUG_ON/Oops sites merely to enforce this principle, or conflate
   hostile input and legitimate error cases with internal invariants.
6. Record exactly one conclusion for each entry:
   - NECESSARY: a reachable true case or required external API contract,
     with source evidence and its unique protective effect.
   - REDUNDANT: a source-proven unreachable condition or duplicated
     protection. Recommend its removal/simplification as an explicit
     code-review observation, even if the patch is otherwise correct.
   - UNRESOLVED: reachability or unique protection not established;
     name the missing path or assumption rather than blessing the guard.
   Do not demand removal on conjecture: public helper contracts,
   alternate callers and legitimate hardening may justify a check.
7. Before verdict, compare the `G` inventory against EVERY diff hunk.
   Reconstruct one apparently necessary guard and one proposed
   redundancy from the call graph without relying on comments or the
   author's description (or challenge two necessary guards if none is
   redundant). Record a compact table in the review report:

   `ID | site/clause | precondition | reachable true path |`
   `unique protection | old->new diagnostic effect | disposition`

   Include the exact line:
   `Guard audit: X of Y checked; R redundant; U unresolved`
   Count distinct clauses and changed branch decisions, not just `if`
   statements. If there are none, say `0 of 0` and cite the hunk walk.

This is separate from bug proof: a patch can correctly repair a serious
bug AND contain a redundant check. An invariant-masking guard can be
more harmful than merely redundant: e.g., suppressing an existing Oops
for a NULL pointer that the call chain guarantees cannot be NULL.
Do not say "no code change needed" or issue an unqualified approval
while redundant/unknown guards have been silently skipped.
A proven redundancy can be a minor, nonblocking cleanup. A material
UNRESOLVED premise blocks unconditional acceptance.
The overall standing-rule audit cannot mark this gate APPLIED unless the
per-guard evidence table and count actually exist.

## Mandatory impact-coverage gate, in ALL tracks

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
7. Apply the adversarial gate's full inverse-operation and handler
   checks to each newly reachable state.
8. For state initialized on a multi-element object or range, verify
   the granularity of the NEXT consumer before choosing the write set.
   A helper accepting an order, length, or folio may consume metadata
   only from the head, while splitting can later expose constituent
   elements. Trace initialization, first consumption (including clearing
   or resetting metadata), splitting, reuse and the next consumption.
   Confirm that neither uninitialized heads nor stale tail metadata
   can suppress warnings, duplicate accounting or contaminate reuse.
   Compare superficially similar callers by their actual free/consume
   helpers, not merely by the name of the initialization helper.
   Search all entry contexts (including early boot, deferred init,
   sanitizer-held resources and hotplug), not only the reported path.
   An initial correct outcome does not establish safe later reuse.

Reconciliation must compare these inventories and investigate missing
path classes, rather than simply vote on reported issues. A convincing
example of ONE failure path does not end the search for others.

## Mandatory adversarial correctness gate: ALL tracks

After the ordinary source review, make a distinct attempt to falsify the
patch's safety and completion claims. This is additive to Sashiko's full
applicable coverage, Tejun's and Chris's methods, and the independent
review; no earlier stage is waived by a passing adversarial check.

1. **Failure-state equivalence and ownership.** For every changed error,
   cancellation, timeout, partial-success or retry path, inventory state
   present on entry, state created by this invocation, and state removed
   by its cleanup. Establish that failure preserves the pre-call external
   state unless partial effects are documented and permitted. In
   particular, cleanup must not destroy pre-existing state or duplicate
   work still owned by a caller. If cleanup ownership moves between
   layers, check all relevant callers, retries and inverse operations.
2. **Hostile bounds.** Enumerate empty, smallest, largest, unaligned,
   overflowing, partially valid and already-occupied inputs wherever
   applicable. For fixed-step loops, prove termination, including when
   the endpoint is not reachable by repeated increments. Check that
   inputs rejected by the forward path cannot become dangerous inputs
   to its rollback path; validate before destructive operations.
3. **Architecture and configuration effects.** For a generic operation,
   search architecture overrides, hooks and alternate configurations
   affecting the changed path. Trace their real effects: a function
   named `flush_cache_*`, for example, may synchronize a secondary
   page-table or host mapping. Verify that rollback reverses every
   externally visible effect, not only software state in the caller.
4. **Context and transitive sleepability.** For each new call on a
   changed path, trace reachable callees and all distinct callers.
   Check scheduling, sleeping locks, allocation/reclaim and blocking
   synchronization against the *actual* execution context. GFP flags
   alone do not prove that a caller is in atomic context. Consider
   whether formerly deferred cleanup has become synchronous.
5. **Lifecycle, ownership, and lock-drop protocols.** Identify the
   owner of allocate, initialize, publish, use, undo, remove, free,
   and the corresponding callbacks. After every lock drop, establish
   whether the caller still has exclusive ownership; reacquiring the
   lock establishes mutual exclusion, not retained ownership. Distinguish
   an object's validity or usability from the caller's authority to
   modify, relocate, publish or free it. Trace the ownership transfer
   and any generation or isolation state that proves that authority.
   For shared objects, check whether another actor can acquire, publish
   or transfer ownership while the original caller is unlocked. Follow
   at least one complete reverse path for persistent state, including
   internal handler flags, dispatch priority, retry and final state.
6. **Independent counterexample pass.** Attempt concrete traces for
   partial progress, repeated operations, invalid inputs, exhaustion,
   architecture variations and undo; omit only demonstrably irrelevant
   classes. For shared-state protocols, explore at least three actors
   when a third actor can re-isolate, republish, free or otherwise
   acquire an object during another actor's lock drop. Include traces
   where the object is still usable but is no longer owned by the
   resumed caller; check both successful and rejected validation paths.
   Independently verify concerns and dismissals against the matching
   source and guards. Record credible unresolved concerns explicitly.

7. **Related-state snapshot consistency.** For each cached pointer,
   cursor, index, flags word, generation or eligibility predicate that
   depends on another mutable value, identify the relationship that must
   hold between them. Verify that separate atomic/READ_ONCE reads still
   describe one eligible object and its associated attributes after
   concurrent replacement, filtering or a retry. A stable pointer is
   not necessarily an eligible pointer; a validated loop candidate
   does not validate a separately cached preferred/default object.
   Trace all downstream users of both the candidate and cached state,
   including accounting, statistics, locality and watermark checks.

**Review completion is evidence-gated.** At the start of each review,
create a coverage record with the seven adversarial classes above and
all applicable Sashiko, Tejun and Chris stages. For each applicable
class, cite specific inspected source paths and the invariant or
counterexample checked; for inapplicable classes, state a source-based
reason. Mark an unexamined or partially checked class UNRESOLVED.
Before a take/accept recommendation, reread this record, reconcile
all unresolved classes and test every assertion of "checked" against
its cited evidence. Do not use a generic "manual coverage complete"
statement in place of evidence. If material coverage remains unresolved,
report the review as incomplete and do not issue an unconditional take
recommendation. A second final pass must challenge at least one
apparently safe dismissal and one derived-state relationship wherever
applicable. Record executed tools separately from manual checks.

## Standing-rule compliance report: mandatory before every verdict

Use the standing-rule inventory as an execution gate, not a final
self-assessment. Before reviewing a patch, enumerate every applicable
mandatory obligation in this file, including the independent, Sashiko,
Tejun/Chris, adversarial, similar-bug, model-decision and reporting
requirements. Assign each obligation a stable identifier in the review
record. Do not choose the denominator from the rules remembered later,
and do not count a repeated statement as a second rule. A rule may be
split into separately testable obligations only if this is done before
reviewing, not to inflate the result afterward.

Include the added-guard necessity gate as its own mandatory obligation.
Its status is APPLIED only when the separate `G` inventory, per-clause
reachability witnesses, old/new diagnostic effects and final count
have been checked. A missing
inventory or a merely asserted "all guards needed" is UNRESOLVED,
even when the patch's main correctness argument is convincing.

For each rule, record exactly one status:

- APPLIED: performed, with specific inspected source or test evidence.
  Reading a rule, planning a check or asserting that coverage is complete
  is not evidence that the check was performed.
- NOT APPLICABLE: bypassed with a concrete, source-grounded reason.
  No rule may be marked inapplicable just because it is inconvenient or
  a tool is missing.
- UNRESOLVED: relevant but not performed or insufficiently verified.
  Record what evidence is missing; tool unavailability is disclosed,
  not silently treated as completion or inapplicability.

Before composing the recommendation, independently recount the statuses
against the original inventory. The final review must include the exact
line `Standing rules: N of M applied; I inapplicable; U unresolved`,
where M = N + I + U. Include brief reasons for *each* inapplicable
or unresolved rule, referencing its identifier. The count must refer
only to checks actually performed for THIS review; previous reviews,
reviewer endorsements and promised tests do not count. State native
Sashiko, build, tests and model execution separately, without crediting
manual methodology as native execution.

Any unresolved material correctness or mandatory coverage requirement
prevents an unconditional take recommendation. Explain the consequence
of non-executed external tools separately from source-analysis gaps;
never report `M of M` if the record lacks evidence for a required rule.
Keep the user-facing summary compact, but retain the per-rule evidence
matrix in the review record so the numbers are auditable. If no ledger
is available, include it in the review report. This gate may not be
waived merely to keep the response short or improve latency.

## Similar-bug search: mandatory in ALL tracks

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
- Include the similar-code search in the cross-track coverage comparison,
  and explicitly say when it was limited by available source access.

## Independent pass: additional review obligations

- Start from the intended userspace behavior: what the bug does to real
  programs, the conditions that trigger it, and the expected correction.
- Read every hunk and identify changed branches, checks, allocations,
  frees, locking transitions, ownership and object lifetime changes.
- Execute the added-guard gate on this first pass, before adopting an
  existing neighboring idiom as evidence. Separately justify every
  Boolean clause; record non-reachability as a review result, not an
  invitation to invent a failure.
- Trace success, retry, signal, OOM, teardown, rollback and partial
  failure where relevant. Inspect call chains and preconditions rather
  than trusting helper names, comments or review summaries.
- Check refcounts, RCU, locking, MMU/page-table lifecycle, address/PFN
  arithmetic, overflow, return values, ABI and all applicable Kconfigs.
- For concurrency, identify actors and shared data; show an explicit
  interleaving and test it against locks, references and barriers.
  Distinguish a state-machine interleaving from LKMM ordering.
- For each inserted path and goto/cleanup label, establish which
  locks and references are actually held THERE. Do not infer ownership
  from an adjacent old code path, or treat a removed unlock as a bug
  without confirming the new path acquired that lock.
- For asynchronous reads, a completed wait or successful folio lock
  does NOT establish successful I/O or PG_uptodate. Separately decide
  whether a true status check is necessary AT THAT STAGE, especially
  when the eventual consumer already checks it. Validate semantics
  and necessity independently; don't retain redundant work by default.
- Consider the strongest counterargument to each suspected bug, then
  resolve it with actual source. Do not report defensive programming
  suggestions without a reachable failure.

## User-visible impact and changelog gate: mandatory for EACH bugfix

Bugfix changelogs must answer "why should users care?" BEFORE spending
most of their space on internal code mechanics. The changelog is a durable
diagnostic and backporting resource for upstream, -stable, distro/vendor
maintainers, and operators investigating affected deployed kernels.

In every relevant review track, independently determine and check:

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
- When referring to another patch, identify its author and exact quoted
  Subject:, including a version suffix such as v2 when applicable.
  If the change is already merged into mainline or mm-stable, use the
  form `Author's abcdef123456 ("exact commit subject")`, with the
  verified 12-character commit SHA. Check merge status rather than
  guessing. Do not use vague references such as "the earlier fix".
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

- Use PlusCal/TLA+ for a meaningful multi-actor shared-state protocol
  when appropriate, not mechanically for every change. The model must
  represent the actual C paths and assumptions; record exclusions.
- When isolation, publication, reuse or ownership spans a lock drop,
  explicitly decide whether a three-actor model is needed. Check the
  original owner, a competing acquirer, and a third actor that can
  reclaim or transfer ownership before the original resumes. Record
  the reason if a three-actor model is unnecessary. Distinguish
  validity and usability invariants from exclusive-ownership ones.
- Use Tejun's tla-mctj Rust checker by default after it has been
  installed and validated. Use TLC for unsupported configurations,
  uncertain verdicts, comparison checks and simulations. Do not claim
  that either checker ran until its output has been inspected.
- Falsify the model: the old or deliberately broken variant should
  exhibit the relevant invariant violation. A clean patched run without
  a failing reference model is weak evidence.
- Record the actual checker, version or source revision, command,
  configuration, bounds, state count and wall time. A tiny passing
  model is not a proof of general correctness. Replay counterexamples
  against reachable C operations.
- Use herd7/LKMM for claims about release/acquire, barriers or hardware
  reordering. Sequentially consistent models cannot verify them.
- When a tool is unavailable, report the model check as NOT RUN and
  explain why. Never mislabel unavailable tooling as a successful model
  check. `model: no (reason)` is appropriate only when no model is needed,
  not when a required check could not be executed.

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
- Report the guard-audit count. Mention proven redundant guards and
  unresolved guard contracts as code-review observations, even when
  they do not alter the substantive correctness verdict. Do not write
  "no code changes requested" until the per-guard audit has passed.
- Keep the final response compact and useful. Do not recite the review
  methodology or a checklist unless specifically requested. Provide
  plain-ASCII, 75-column, LKML-ready email text when asked.

## Immediate discovery-to-Markdown update: mandatory

Whenever a substantive new fact, missed path, incorrect previous
finding, revised disposition or generalizable workflow lesson is
established, update the relevant canonical project `.md` files in the
SAME response cycle. Do not wait for a later handoff or for AKPM to
ask for an update. This includes discoveries made in follow-up chat,
not just during the original review. An unverified hypothesis is not
a verified discovery; preserve its uncertainty in the record.

- Update the specific review report with technical evidence, old and
  new conclusions, and any corrected advice or LKML reply. Preserve
  the earlier error visibly when important for auditability.
- Update `review-activity.md` when it is available, tying the change
  to the existing review/finding ID and updating the next action.
- Update THIS workflow whenever the discovery yields a generally
  applicable review rule. Keep case-specific details out of policy
  unless they are a compact motivating example. Do not add repeated
  historical narrative or duplicate standing rules.
- Save detailed per-patch review reports to Library and verify the saved
  path. When this workflow or the master ledger changes, provide actual
  downloadable Markdown files, preserving canonical filenames. Always
  resend `akpm-patch-review-workflow.md` after any update, without
  waiting for a request. Never claim unverified storage or delivery.
- Documentation updates do NOT authorize changing kernel code or any
  other production code. Respect the standing source-edit policy.

For new reviews, precommit this update gate as its own audit obligation.
Mark it APPLIED only if discoveries were recorded during the review or
no new discoveries occurred; UNRESOLVED if required documentation was
not updated. Do not retroactively alter a completed review's original
compliance denominator simply because a new rule was added later.

## Routine review delivery and canonical record ownership

- Give the verdict, actionable findings and copy-ready LKML reply in
  chat. Do not expose review machinery as routine user deliverables.
- `akpm-patch-review-workflow.md` is user-held authoritative methodology.
  ALWAYS supply a verified direct download link to its full, updated
  canonical `.md` file whenever it changes, in that same response.
- `review-activity.md` is the user-held master index and compact active
  ledger, listing review IDs, findings, feedback, detailed-report Library
  paths and next actions. On updates, deliver the revised canonical file
  as a direct download; do not require users to hunt through Library.
- Store ONLY detailed per-patch review histories in the persistent
  ChatGPT Library under `/Kernel Patch Reviews/reports/`. Each report
  retains its canonical `<topic>-review.md` basename. Update it as new
  source findings, feedback or methodology corrections are discovered.
- For per-patch reports, verify Library upload success and tell the user
  which report was saved. Do not routinely send per-patch `.md` files.
- In subsequent chats, retrieve a detailed report from the Library using
  the path in `review-activity.md`; never assume `/mnt/data` persists.
- Keep formal models, test logs and reproducers as supporting artifacts,
  providing them only on request or when needed for validation. Do not
  make these routine handoff downloads.
- The Library is NOT the authoritative delivery mechanism for the
  workflow or master ledger. Do not upload new versions of these two
  files there. Provide user-held copies instead.
- Never report a Library save or a download as successful unless it is
  verified. If persistence fails, disclose the failure explicitly.

## Artifact delivery: mandatory

- ALWAYS send the complete updated `akpm-patch-review-workflow.md` with
  a verified direct download link whenever the workflow is modified.
- Send updated `review-activity.md` as a direct download whenever it
  changes; do not put the canonical master ledger in Library.
- Store detailed per-patch report Markdown in Library and confirm its
  exact location, without routine per-patch download links.
- Prefer the download tray when available. Never invent a sandbox path.
- Never delete or replace user files without authorization.
- Preserve canonical filenames exactly, including case and extension.
  Never append dates, versions or suffixes unless explicitly asked.
- Temporary paths or staging directories must not change the basename
  of the final downloadable file.

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
   author, patch link/Message-ID, any supplied base SHA, and related
   series subjects in the detailed record. Disambiguate collisions by
   Message-ID and source context when needed.
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
5. For a missed review issue identified afterward, record it as a
   new finding with the omitted code path and why the prior coverage
   audit failed. Correct any stale verdict or proposed reply; do not
   silently retain the earlier "no code changes" assessment.
6. Promote a lesson to THIS AKPM workflow only if it improves review
   methodology across patches. Do not append a special rule for every
   bug, false positive, or argument. Do not edit upstream modules.
7. Archive records which are resolved or sufficiently dormant to be
   removed from the active working set. Use one file per local close-off
   date, `review-activity-YYYY-MM-DD.md` (America/Los_Angeles). Several
   reviews may share that file. An archived `UNRESOLVED` review is
   *dormant*, not approved or rejected by its author.
8. When archiving, MOVE the compact record out of the active section;
   leave a Subject-to-filename mapping in the index. Retain the finding
   dispositions, counterarguments, durable lesson and source references
   in the archive. Remove superseded detail and transcript repetition.
   Archive files are snapshots: normally append to the day's file, but
   do not rewrite previous snapshots just to tidy the active index.
9. When a topic resurfaces in another chat, consult the active/index
   file by normalized Subject and identify its exact archive filename.
   Read that archive before resuming; request that file if unavailable.
   Copy only the still-relevant state back to the active entry, preserve
   the archive link and finding IDs, and update the index to `ACTIVE`.
   On a later close-off, use that day's archive with a backlink.
10. Periodically remove obsolete or uninteresting Subject mappings from
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
Sashiko, Tejun and Chris sources as directed above. When continuing
AKPM's previous findings or feedback, also attach `review-activity.md`
and only the relevant dated archive. Do not attach the historical
`tj-patch-review-workflow.md` or `kernel-patch-review-workflow.md`.
Neither file should be modified or deleted without authorization.
