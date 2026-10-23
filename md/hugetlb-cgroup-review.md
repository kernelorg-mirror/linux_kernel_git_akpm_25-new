# Review: mm/hugetlb_cgroup: prevent use-after-free during offlining

Review key: R-018. Author: Daehyeon Ko. Date: 2026-10-20.
Status: LIFETIME REPAIR SOUND IN SOURCE; ONE NEW REDUNDANT GUARD.
No Reviewed-by offered; native Sashiko and kernel runtime unverified.

## Submitted patch, reference tree and source integrity

The complete patch as supplied in this chat is the reviewed artifact.
No previous revisions, replies, or author's raw test logs were supplied.
The diff modifies only mm/hugetlb_cgroup.c (32 additions, 11 removals).

IMPORTANT: The exact preimage is not mainline 7.3-rc7's copy.
The canonical AKPM mirror is
`kernelorg-mirror/linux_kernel_git_akpm_mm`, branch `mm-stable`.
The verified old file has Git blob:
`3fb41311e4c7dcbbd26f7b230ebb1f8c7ce310fe`.
Its charge, commit and uncharge locations are 286, 336 and 418,
matching the submitted diff context and index. The mainline rc7
file is `ecb6e0b7819a0d80bf71504bedbbe1def3d6556f` and lacks
some of the per-node helper logic in this preimage.

Matching surrounding source in mm-stable:
- mm/hugetlb.c: b017ae1dfd6fdd1f0ed7e27a82da840023205425
- mm/page_counter.c: 9167ffd1380c82876315d95f72de953c7fe89d01
- kernel/cgroup/cgroup.c: 227d09704ca591f96949af83c4152cc52559cd66

The historical Fixes commit is
`da1def55919f4852c4759249a78d63a0c5d2d8f9`, committed
2012-08-01, "hugetlb/cgroup: add support for cgroup removal".
Its new offline scan/reparent mechanism matches the bug's ancestry.
The 2012 history does NOT imply that a current upstream diff will
cherry-pick cleanly to every still-supported stable branch.

## Independent-first: source-derived bug proof

The original implementation calls css_tryget() in
mm/hugetlb_cgroup.c:296-303, then hierarchically increments the
page_counter chain (:305-312) and drops the normal CSS reference
(:313-317) BEFORE the folio is committed. The caller commits under
hugetlb_lock in mm/hugetlb.c:2914. A task migration or controller
removal can leave the allocator using a CSS that is being offlined.

A reachable old-code timeline is:

1. Allocator obtains the old task CSS via task_css() under RCU and
   css_tryget(), then pauses before page_counter_try_charge().
2. Cgroup removal sets CSS_DYING in kill_css_sync()
   (kernel/cgroup/cgroup.c:6210-6248).
3. css_offline() scans the hugepage_activelist under hugetlb_lock,
   finds no folio or charged local usage, and completes
   (mm/hugetlb_cgroup.c:255-271).
4. The allocator now completes its hierarchical counter charge;
   the old normal-charge path drops the CSS ref before commit.
5. It publishes that old CSS pointer on the folio under hugetlb_lock.
6. The CSS is ultimately freed; a later folio uncharge dereferences
   its freed page_counter and per-node nodeinfo fields.

The earlier CSS ref only kept the cgroup alive while doing the charge;
it did not span the later publication. The offline scan's lock does
not cover the preceding page_counter_try_charge(). This is a genuine
internal UAF, not a NULL failure, and may crash or corrupt the kernel.

The author's report of three KASAN reproducing boots and a
capability-free uid 1000 allocator is AUTHOR-REPORTED, not an
independently run reproducer. Source review substantiates the
mechanism, not those exact measured rates or collected stack traces.

## Separate fix proof and end-to-end ownership

1. Successful normal charge retains css_tryget()'s reference until
   either hugetlb_cgroup_commit_charge() or the precommit rollback.
   The reservation path already retained its reference; it is
   intentionally unchanged at publication and released with the
   reservation's eventual uncharge. In particular, the separate
   hugetlb_reserve_pages() path (mm/hugetlb.c:6783-6886)
   retains/releases reservation CSS ownership through resv_map or
   region_add(), and its existing cancellation uncharge still does
   exactly one css_put().
2. Under hugetlb_lock, commit checks css_is_dying() on the selected
   CSS and ancestors. It cancels each dying CSS's *local* page count.
   page_counter_try_charge() has already charged each ancestor once.
   page_counter_cancel(), unlike page_counter_uncharge(), affects only
   its specified counter. No replacement charge at a live parent is
   needed; doing so would double charge that ancestor.
3. Root CSS is immortal (CSS_NO_REF in cgroup_init_subsys(),
   kernel/cgroup/cgroup.c:6439-6444), so parent traversal terminates.
   CSS child creation css_get()s parent and freeing css_put()s parent
   (cgroup.c:5855-5856 and 5694-5713); the retained child ref keeps
   the ancestry accessible during the decision. Controller removal
   kills descendants before ancestors (cgroup_apply_control_disable(),
   cgroup.c:3491-3519).
4. The commit decision and css_offline()'s active-folio scan both
   run under hugetlb_lock. If commit precedes the scan, the latter
   sees the folio and reparents it. If the scan finishes first,
   commit sees the dying CSS and selects a live ancestor. The
   CSS_DYING transition precedes the scan and the scan's spin unlock
   orders state before a later commit spin lock acquisition.
5. The published folio gets the *selected live owner's* pointer and
   its per-node usage increment. It does not need a per-node transfer
   from the dying CSS because the charge was never previously
   attributed to that CSS's nodeinfo. For already committed folios,
   the existing hugetlb_cgroup_move_parent() updates per-node usage
   using hugetlb_cgroup_move_usage() under the same lock.
6. Folio uncharge traverses the new owner's hierarchical counters
   and subtracts its local per-node usage. The root/ancestor counts
   match the initial charge less each dying local canceled count.
7. If a precommit allocation fails, the existing
   hugetlb_cgroup_uncharge_cgroup() path uncharges the entire counter
   chain, and the new unconditional css_put() releases its pending
   reference. A successful commit transfers the charge to the folio
   before the retained temporary CSS reference is released.
8. A postcommit memcg charge failure frees the folio; folio uncharge
   reverses its committed hugetlb charge. Reservation-failure and
   reservation-commit paths retain their distinct reference protocol.

No newly introduced allocation or sleep was identified under
hugetlb_lock. A percpu_ref_put() under the lock is supported by
existing reservation folio-uncharge code using css_put() there.
Exceptional ancestor traversal costs O(dying CSS depth), not an
additional active-folio scan. The retained ref can delay a CSS's
freeing while the allocation is stalled, but is required for safety.

## State-class and inverse-operation matrix

- Enabled; CSS remains live: Same owner/count; balanced
Old: Charge then drop ref; new: Ref held to commit
- CSS dying before commit: Safe live owner
Old: May attach dying CSS; new: Cancel dying locals
- Scan finished before charge: Old UAF prevented
Old: Charge may arrive too late; new: Retained ref and redirect
- Scan after commit: Per-node ownership moved
Old: Existing scan reparents; new: Same scan reparents
- Child and parent both dying: Root retains count
Old: In-flight CSS may become stale; new: Cancel both locals
- Precommit allocation failure: Balanced rollback
Old: Full hierarchical uncharge; new: Uncharge plus css_put
- Postcommit memcg failure: Balanced ownership
Old: Folio uncharge; new: Folio uncharge
- Reservation charge: No new transfer
Old: Ref held across use; new: Unchanged reservation path
- Boot-disabled controller: No CSS ref or charge
Old: h_cg NULL; new: h_cg NULL
- NUMA/multiple hugepage sizes: No cross-node transfer
Old: idx/nid-specific counts; new: Same idx and nid


Contrasting configurations checked: CONFIG_CGROUP_HUGETLB depends
on HUGETLB_PAGE (init/Kconfig:1298-1300); mm/Makefile builds this
file only with CONFIG_CGROUP_HUGETLB. The CONFIG-disabled stubs do
not enter these new branches. Nodeinfo exists for possible NUMA
nodes and is selected by folio_nid(). No architecture-specific new
operations are in the diff. Root, nested, delayed-offline and boot-
disabled cases were considered. Actual machine/kernel testing was
not performed.

## Added-guard necessity and diagnostic audit

Guard scope includes every new clause and every existing conditional
whose branch or target state changes in the hunks. The entry sites
below refer to the submitted diff over the mm-stable preimage.

G01: Remove `if (!rsvd) css_put` in charge
  NECESSARY change: successful normal charges now own a ref until commit or
  rollback; no new error masking
G02: Commit `hugetlb_cgroup_disabled()` clause, old return -> out
  REDUNDANT, INHERITED: when disabled, charge sets h_cg=NULL; new out
  handling needed for ref balance, but this old clause has no unique
  protective state
G03: Commit `!h_cg` clause, old return -> out
  NECESSARY: boot-disabled controller has NULL h_cg; prevents dereference,
  same preexisting behavior
G04: New `if (!rsvd)` around reparent loop
  NECESSARY: reservation charges intentionally keep long-lived CSS
  references and are not reparented
G05: New `while (css_is_dying(...))`
  NECESSARY: reachable after task migration/kill; excludes dying owner and
  preserves hierarchical charges, root terminates
G06: Existing `if (!rsvd)` per-node usage after new selection
  NECESSARY: reservation charges have different accounting; no new
  diagnostic masking
G07: New out `if (!rsvd)` before css_put
  NECESSARY: normal success/publish relinquishes temporary CSS ref;
  reservation ref must persist
G08: New out `&& charged_h_cg` before css_put
  NECESSARY: boot-disabled controller has NULL h_cg; avoids NULL
  dereference and only skips no-ref cases
G09: Changed uncharge `if (!h_cg)`
  NECESSARY: boot-disabled controller has no CSS charge or reference; same
  old early return
G10: New uncharge `if (!hugetlb_cgroup_disabled())`
  REDUNDANT, INTRODUCED: successful charge with non-NULL h_cg requires
  enabled boot static key; skip can silently suppress uncharge only in
  impossible internal state
G11: Removal of old `if (rsvd)` CSS-put guard at uncharge
  NECESSARY: normal rollback now owns an outstanding reference too;
  reserves already did


Guard audit: 11 of 11 checked; 2 redundant; 0 unresolved.
One redundant clause (G02) predates the patch; G10 is newly added.
The actionable change is to delete G10 and unconditionally uncharge
when h_cg is non-NULL. G02 is a separate opportunity to simplify the
existing compound early exit, not a newly introduced defect.

Reconstruction check: G05's reachability follows task migration,
kill_css_sync(), and the delayed offline scan. G10's redundancy
follows __charge()'s early disabled exit, non-NULL pointer on a
successful charge, and cgroup.c's boot-only cgroup_disable() at
:7259-7291. It does NOT rely on the comment in the patch.

Diagnostic impact: No new guard converts a normally impossible
kernel invariant failure from an existing Oops to quiet errno. G10
is nonetheless undesirable: its hypothetical true branch after a
non-NULL charge would skip page-counter cleanup rather than expose
an unexpected controller state. Removing it preserves clear
charge/uncharge symmetry and avoids a dead branch.

Suggested simplification (new uncharge body only):

```c
if (!h_cg)
        return;

page_counter_uncharge(
        __hugetlb_cgroup_counter_from_cgroup(h_cg, idx, rsvd),
        nr_pages);
css_put(&h_cg->css);
```

## Native PlusCal/TLA+ verification

Model: `hugetlb_css_lifetime.tla`; checker cfgs for old protocol,
old UAF-only falsification and patched protocol. Actors: one
allocator, child CSS offliner, parent CSS offliner, plus immortal
root. Bounded counters are zero or one per CSS; modeled owner,
CSS references, dying/offline/free states, hugetlb_lock, commit,
rollback and per-CSS local counter cancellation.

Model was drafted independently from the C paths. The first draft
had a bad abstraction allowing CSS ref acquisition after freeing;
this was corrected before the final checks. The final old-code
counterexample has an actual ref acquisition before offlining and
replays against the C paths above. Model uses sequential consistency,
no extra CPU memory reordering, no real slab reuse and a single
allocation; it does not model all Cgroup/NUMA runtime behavior.

Translation: PlusCal -> generated TLA+, SANY parsing: passed.
Native tools: TLC 2026.10.15.145915; tla-mctj 0.1.2.

- TLC: Original, full invariants, 569* distinct states, depth 16;
  NoDeadCharge fails
- tla-mctj: Original, full invariants, 524* distinct states, depth 14;
  NoDeadCharge fails
- TLC: Original, UAF falsification, 828* distinct states, depth 19;
  NoDangling fails
- tla-mctj: Original, UAF falsification, 823* distinct states, depth 18;
  NoDangling fails
- TLC: Patched, all invariants, 1,512 distinct states, depth 31; PASS
- tla-mctj: Patched, all invariants, 1,512 distinct states, depth 31; PASS


*Early-stop counterexample counts, not a full original state graph.
Patched TLC generated 3,695 states before deduplication;
its state queue was empty at completion. Checker logs and cfg files
are packaged separately. These are native model-checker runs, not
native Sashiko, a real kernel build, KASAN or a full LKMM proof.

Old UAF trace, mapped to the actual C:

- a_ref: __charge() obtains CSS reference.
- oc_die: cgroup.c kill_css_sync() marks the CSS dying.
- oc_lock/scan/check: css_offline() finds no active charged folio
  and observes its local usage as zero.
- a_ch_c/p/r: page_counter_try_charge() updates child and ancestors.
- a_precommit: old __charge() drops the normal CSS ref.
- a_publish: old __commit() stores the dying child's CSS in the folio.
- oc_off/free: CSS offlining finishes and the CSS is freed while the
  folio still refers to it; later folio uncharge would use freed data.

The patch disallows this ordering by retaining the ref and redirecting
under hugetlb_lock. Source release/acquire via that lock orders scan
with commit; the CSS_DYING store precedes the offline scan. No new
standalone lockless ordering protocol or required herd7 test was
identified, but the TLA+ model makes no general LKMM guarantee.

## Independent, Sashiko, Tejun and Chris reconciliation

Independent source review (saved BEFORE methodology reading):
`independent-first-pass.md`; traced charge/commit/cancel, offline
active list, folio uncharge, css refcount, ancestor pointers, local
and hierarchical page counters. Candidate UAF confirmed. Candidate
parent double charge dismissed because the parent was charged by
page_counter_try_charge(). Candidate per-node imbalance dismissed
because per-node usage is first added at *final* publication.

Sashiko current HEAD checked 2026-10-20:
`026195ab58e2099e81017adbc6b97f33c509c8ba`.
The seven current stage definitions, `linux_patch_review.rs` and
same-SHA vendored MM/locking/RCU/false-positive guidance were read.
Differences from the previous `f6e2...` checkpoint were primarily
benchmark/CLI and Sashiko-project prompts; stage names unchanged.
Native Sashiko was NOT run; manual relevant specialist coverage:

- GOAL: solve charge/commit vs offline race in the owner of the charge;
  no unrelated page allocator redesign required.
- IMPLEMENTATION: all touched ref and counter semantics checked;
  G10 redundant new guard exposed.
- EXECUTION-FLOW: success, no page, buddy allocation, abort,
  reservation, controller-disabled, postcommit folio free checked.
- RESOURCES: CSS temporary refs, parent refs, folio ownership,
  page counters, per-node fields and final free checked.
- LOCKING: CSS_DYING, hugetlb_lock serialization, RCU acquisition,
  spin-context css_put, 3-actor interleavings checked.
- SECURITY: capability-free attacker-triggerable kernel-memory UAF,
  provided reproducer claims separated from verified source.
- HARDWARE: no hardware-specific register/ABI change; NUMA nid,
  hugepage sizes, configuration gates assessed.

Sashiko's second-stage verification principles were applied: verify
both candidates and dismissals with kernel sources, do not dismiss
multi-actor races from a happy-path-only argument, distinguish
synchronization from lifetime protection, and challenge every guard.
No native tool verdict has been substituted for manual analysis.

Tejun pinned `cbb4478d0f73e15907335e70a2dc2fe54a9e7167`
(unchanged): patchset review, model checker, code idioms, evidence,
validation, patch descriptions and stable tagging applied. Chris
pinned `d048f8742f6740c38833adf02e87901412d771ca`
(unchanged): review core, technical, false positive, build and
applicable MM, RCU, locking, VFS subsystem guides applied.
All three review tracks confirmed the original UAF, agreed on
fix-path ownership, and checked the proposed simplifier against
source; none found a new corruption path in the submitted repair.

## User impact, stable consideration and outstanding evidence

Expected userspace effect: prevent kernel use-after-free/crash or
memory corruption when a task's hugetlb charge races with cgroup
migration/removal or controller offlining. The author states an
unprivileged allocator plus privileged cgroup administration can
trigger it on an empty, otherwise valid configured 2 MiB pool.
The race is rare but its failure is severe; it is not a cosmetic
counter accounting change. This is a credible stable-fix candidate.

Author-reported kernel tests only:
- Unmodified v7.3 kernel, 128 x 2 MiB pool: 3/3 KASAN boots failed.
- With patch: 5,000 rmdir rounds, 1,075,055 successful faults;
  2,000 controller-disable rounds, 1,707,348 faults; no reported
  KASAN, LOCKDEP, page-counter or refcount failures.
No logs, scripts or exact runtime kernel commit accompany the mail;
the above counts were NOT independently confirmed or repeated.
No local kernel build or runtime KASAN test was run.

Stable: `Cc: stable@vger.kernel.org` is in the trailer area and is
supported by a credible user-visible memory-safety failure and the
author's reported before/after tests. Original Fixes commit is from
2012, but many historical backports require adapted patches because
CSS refs, page counters and hugetlb per-node usage have evolved.
Stable maintainers must confirm each target tree's ancestry and fix.
The current mm-stable patch must first be merged upstream.

Outstanding: native Sashiko not run. Kernel runtime independently
untested. The author's raw KASAN logs and test scripts are not in
this submission. These limits do not invalidate the source findings.

## Reviewer recommendation

Request the unnecessary `hugetlb_cgroup_disabled()` guard be removed
from __hugetlb_cgroup_uncharge_cgroup(). The historical compound
guard in commit could also be simplified if the author wishes; it is
not a new introduced regression. I find no material code-correctness
objection to the actual CSS lifetime and reparenting fix on the
reviewed source. Do not add a Reviewed-by trailer until the requested
cleanup and final source are inspected; no mail has been sent.

## LKML-ready reply (PLAIN ASCII; NOT SENT)

```text
The CSS lifetime repair looks correct to me. The ref acquired by
css_tryget() needs to survive until the charge is committed to a
folio or canceled. Holding it through that point, and redirecting
uncommitted charges away from dying CSSs under hugetlb_lock, closes
the window with css_offline()'s active-folio scan.

The local page_counter_cancel() calls also look right: the original
page_counter_try_charge() already charged the ancestor counters, so
those ancestors must not be charged a second time. The per-node usage
is first recorded for the selected live owner at commit.

One code simplification: the new

        if (!hugetlb_cgroup_disabled())

in __hugetlb_cgroup_uncharge_cgroup() is unnecessary. Once h_cg is
non-NULL, a successful charge necessarily came from an enabled
controller, and cgroup_disable= is a boot-time static-key setting.
Please just unconditionally call page_counter_uncharge() after the
existing !h_cg check, followed by css_put().

The reported KASAN reproduction and before/after stress numbers make
this a credible stable fix. I found no other correctness objection to
the proposed charge-to-commit lifetime protocol.
```

## Standing-rule inventory and completion audit

The 75 requirements were fixed before inspecting source.
Status reports execution of the individual review action,
not a claim that the Linux kernel was tested on a machine.

A01 APPLIED: Workflow and R-017 ledger inspected before independent review.
A02 APPLIED: 75 entries in .hugetlb_review_obligations.json before source
  work.
A03 APPLIED: Entire user-supplied email/diff reviewed; no replies attached.
A04 APPLIED: AKPM mm-stable preimage blob 3fb41311e4c7d verified exactly.
A05 APPLIED: 2012-08-01 da1def55919f read; introduced offline reparent.
A06 APPLIED: Source lines 182-443 and 917-957 of exact preimage.
A07 APPLIED: hugetlb_alloc_folio; online/offline/reparent/reservation
  callers.
A08 APPLIED: page_counter, css refs, folio pointer, spin and RCU callees.
A09 APPLIED: Selected CSS; flags; ancestor counter; per-node usage; folio
  owner.
A10 APPLIED: Commit, uncharge, active-list scan, cgroup page/stat readers.
A11 APPLIED: Ten old/new lifecycle scenarios in state matrix above.
A12 APPLIED: Kconfig, NUMA nodeinfo, reservation, boot-disabled and root
  cases.
A13 APPLIED: Normal, buddy failed, reserve charge, memcg failure, cancel.
A14 APPLIED: CSS ref acquisition, hold, transfer, put and parent CSS
  lifetime.
A15 APPLIED: RCU selection; hugetlb_lock scan/commit; dying flag/order.
A16 APPLIED: Six-step source-replayable original UAF plus 3-actor model.
A17 APPLIED: Source-backed crash/corruption risk; distinguish author rates.
A18 APPLIED: Reservation no-reparent history and preexisting disabled
  guard.
A19 APPLIED: Root, nested, controller disable, CONFIG and NUMA variants.
A20 APPLIED: Normal one CSS put in spinlock; exceptional O(depth)
  traversal.
A21 APPLIED: Original UAF timeline and falsification trace against C.
A22 APPLIED: Distinct surviving-reference and local-cancellation proof.
A23 APPLIED: Publication, offline parent transfer, folio uncharge,
  rollback.
A24 APPLIED: CSS owner-side repair preferable to broad hotplug/allocator
  change.
A25 APPLIED: Looked at folio migration, already committed CSS reparent,
  reuse.
A26 APPLIED: Exact header and alloc_folio call signatures; build not run.
A27 APPLIED: Failure rollback and reservation rights retained.
A28 APPLIED: No-page, nested-depth/root bound, page-counter underflow
  review.
A29 APPLIED: Kconfig disabled, high-order hugepage size, NUMA per-node.
A30 APPLIED: percpu_ref_put under spinlock same as existing reservation
  path.
A31 APPLIED: Unlock for buddy alloc then relock; CSS ref spans gap.
A32 APPLIED: Allocator, child-offliner, parent-offliner TLC/TJ traces.
A33 APPLIED: Local and hierarchical counters distinct; nodeinfo only at
  commit.
A34 APPLIED: Dismissed claim that parent charge needs separate increment.
A35 APPLIED: Searched related migration, CSS offline, reserve and folio
  paths.
A36 APPLIED: Sashiko head 026195ab... checked 2026-10-20.
A37 APPLIED: Current linux_patch_review.rs stages and verification
  reviewed.
A38 APPLIED: SHA-pinned vendored MM, locking, RCU, technical, false
  positive.
A39 APPLIED: GOAL: correct owner/layer and alternative design.
A40 APPLIED: IMPLEMENTATION: 11 guard entries and counter semantics.
A41 APPLIED: EXECUTION: success, abort, reservation, disabled, postcommit.
A42 APPLIED: RESOURCES: reference owner, page counter, folio and nodeinfo.
A43 APPLIED: LOCKING: CSS_DYING vs spin; 3-actor finite checker.
A44 APPLIED: SECURITY: unprivileged trigger/privil. manager/UAF.
A45 APPLIED: HARDWARE: no device path; config/NUMA impact checked.
A46 APPLIED: Candidates and dismissals replayed against source and TLA+
A47 UNRESOLVED: Native Sashiko not installed or run; manual domains only.
A48 APPLIED: Tejun cbb4478d... head verified 2026-10-20.
A49 APPLIED: Read/apply patch review, model, evidence, kernel idioms, tags.
A50 APPLIED: Chris d048f874... head verified 2026-10-20.
A51 APPLIED: Loaded core, technical, false-positive, build, MM/locking/RCU.
A52 APPLIED: Sashiko advanced by 3 commits; Tejun/Chris unchanged.
A53 APPLIED: Independent/7 Sashiko/Tejun-Chris reconciliation recorded.
A54 APPLIED: Author reported KASAN/stress; our source and native TLA tests.
A55 APPLIED: Model YES for in-flight CSS ref handoff vs 2 offline actors.
A56 APPLIED: One allocator + child and parent offliner, nested CSS root.
A57 APPLIED: PlusCal translated, SANY, old falsification, both checkers
  pass.
A58 APPLIED: Spin-lock happens-before examined; no herd7 test invoked.
A59 APPLIED: Potential freed-CSS kernel UAF and crash during hugetlb
  uncharge.
A60 APPLIED: Unprivileged allocator + cgroup admin; nested/flat, 2MiB.
A61 APPLIED: Prevent KASAN UAF and preserve correct accounting/free.
A62 APPLIED: Stable release diagnostic: KASAN stacks; exact mm-stable blob.
A63 APPLIED: Impact is explicitly present in author changelog and
  substantiated.
A64 APPLIED: Source UAF, author before/after tests, <100 line fix, no ABI.
A65 APPLIED: 2012 introducing fix, adapted backports may be required.
A66 APPLIED: Cc stable trailer and documented stable-kernel-rules.rst.
A67 APPLIED: Changelog, signoff, one file, authorship and tests evaluated.
A68 APPLIED: Finding G10 separated from runtime evidence and uncertainties.
A69 APPLIED: ASCII 75-column authored text checked after report assembly.
A70 APPLIED: Unsent LKML plain text in report.
A71 APPLIED: R-018 ledger case/finding IDs appended.
A72 APPLIED: Only local review artifacts; no kernel or GitHub write.
A73 APPLIED: Canonical report and ledger; exact paths verified before
  links.
A74 APPLIED: 75-row matrix and computed totals in this report.
A75 APPLIED: R-018 evidence and new redundant-check finding recorded now.


Standing rules: 74 of 75 applied; 0 inapplicable; 1 unresolved.
Unresolved A47: no native Sashiko execution. Manual coverage
has been recorded separately; it is not a native run.

