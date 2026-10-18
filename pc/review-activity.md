# Review activity - AKPM

Last updated: 2026-10-17 (America/Los_Angeles)
Scope: working ledger plus Subject-to-location index, NOT review method.
Method: `akpm-patch-review-workflow.md` (invokes pinned upstream Tejun
modules; the old standalone S2 file is historical only).

This ledger was seeded from recent review discussions. It records our
current understanding, NOT author acceptance. Messages, tests and later
feedback not yet supplied are not presumed to exist. Keep each record
short; detailed mail and diffs are retrieved by reference as needed.

## Tejun upstream workflow checkpoint

Repository: https://github.com/htejun/kernel-agent-workflows
Upstream branch: `main`
Last checked: 2026-10-17 (America/Los_Angeles)
Checked HEAD: `c8cc6a8bee854cf2850f44e0a61be581c19f1d4e`
HEAD commit date: 2026-10-17 17:19:05 UTC
HEAD subject: README: Point to the repository on GitHub
Last comparison: 2026-10-17 (America/Los_Angeles)
Status: initial checkpoint; no earlier upstream SHA to compare.
`UPGRADING.md` contains only its initial-version entry.

Migrated from the read-only standalone `tj-patch-review-workflow.md`
(S2). Reviewed the replacement `review/patchset-review.md`,
`review/formal-model-check.md`, and relevant evidence, kernel idiom,
patch-description and other review modules at the pinned SHA.
The core milestone, incremental-patch, source-verification, prose and
formal-model procedures remain available upstream. AKPM's separate
independent pass, MM coverage gates, similar-bug search, Sashiko
refinements and feedback tracking remain in its local entry point.
AKPM retains an explicit model decision despite the upstream default
`$FORMAL_MODEL=off`. No profile, overlay or agent installation performed.
The original S2 file was not modified or deleted.

At each new Tejun-guided review, check HEAD and record the SHA used in
the review entry. If advanced, check `UPGRADING.md` and relevant module
diffs and record substantive changes here. Reuse verified pinned files
when unchanged. Do not attribute this SHA to reviews R-001 through R-005.

## Chris Mason prompt tracking

Repository: https://github.com/masoncl/review-prompts
Upstream branch: `main`
Last checked: 2026-10-17 (America/Los_Angeles)
Checked HEAD: `d048f8742f6740c38833adf02e87901412d771ca`
HEAD commit date: 2026-10-01 11:53:46 UTC
HEAD subject: README: add pahole to the project lists
Status: initial version-tracking checkpoint; no previous pinned SHA.
Last comparison: 2026-10-16 (America/Los_Angeles)
Comparison: HEAD unchanged from the recorded checkpoint; no new diff.

Recent upstream improvements already in this baseline:
- 2026-09-21 `2e5e252bfe56`: MM race refcount budgeting.
- 2026-09-21 `a39be13ca052`: avoid a `virt_to_page()` false positive.
- 2026-09-23 `f85b3a017072`: guides and false-positive updates.
- 2026-10-01 `1a1befd0c56f`: correct guide rules contradicted by code.
These are examples, not every upstream change or independent proof of
improved review accuracy.

For each new Tejun-guided review, record the FULL Chris prompt SHA and
fetch/check date in that review's active entry. Compare `main` with the
previous checked HEAD and summarize material changes to MM, locking,
false-positive handling, and review instructions here. Keep this section
short, retaining only the latest checkpoint and useful change notes.
The earlier reviews R-001 through R-005 have no recorded prompt pin:
DO NOT infer they used the HEAD recorded above.

## Sashiko technique checkpoint

Repository: https://github.com/sashiko-dev/sashiko
Upstream branch: `main`
Last checked: 2026-10-16 (America/Los_Angeles)
Checked HEAD: `f4b72fa04f232fe5f2183d32d7cf9c09e5d735ec`
HEAD commit date: 2026-10-16 20:13:53 UTC
HEAD subject: ingestor: restrict git protocols when bootstrapping archives
Last comparison: 2026-10-16 (America/Los_Angeles)
Comparison: HEAD matches the supplied initial reference; no upstream
change to compare. Verified the vendored `mm-vma.md` and
`false-positive-guide.md` paths at this SHA; no full workflow audit.

Accepted techniques: preserve substantive dismissed hypotheses with
source evidence; independently verify disputed claims and dismissals;
keep distinct failure mechanisms separate. These are local additions to
the existing two-pass review, not a Sashiko review pipeline.

Check HEAD at most weekly during active reviewing, at the next
interaction after seven days. If advanced, inspect relevant deltas only
and record the new SHA, comparison date and any useful general rules.
Carry forward accepted techniques between checks. No background
Sashiko monitoring has been scheduled.

## Subject index

The literal text inside each backtick pair is the normalized `Subject:`
(with `Re:` and `[PATCH ...]` decorations removed). A Subject is kept on
one physical line as an exact lookup key. When an incoming reply has
such a subject, consult the named active record or archive FIRST.

- `mm/mglru: fix using folio_mark_accessed to replace folio_set_active`
  ACTIVE: [R-001](#r-001); author feedback outstanding.
- `mm: multi-gen LRU: fix NULL lruvec->pgdat deref with memcg disabled on cmdline`
  ACTIVE: [R-002](#r-002); author proposes common helper.
- `mm/vma: avoid spurious write locks when mm->mm_lock_seq overflows`
  ACTIVE: [R-003](#r-003); author feedback outstanding.
- `mm/ksm: keep smart scan from losing duplicate pages`
  ACTIVE: [R-004](#r-004); review of its [1/2], [2/2] series.
- `ipc/sem: account enlarged sops arrays to memcg`
  ACTIVE: [R-005](#r-005); review response drafted.
- `mm/vmalloc: read vm_map_ram block regions from the requested offset`
  ACTIVE: [R-006](#r-006); v1 needs an off-by-one correction.
- `proc/kcore: advance the vmalloc retry by the last copy, not the total`
  ACTIVE: [R-007](#r-007); v1 source-reviewed, no defect found.
- `mm: retry page faults once under the per-VMA lock`
  STUDY: [L-001](#l-001); lessons integrated, no patch verdict.
- `mm: various (urgent?) fixes`
  DORMANT: A-001 in
  [review-activity-2026-10-16.md](review-activity-2026-10-16.md#a-001).
  A dormant review is not author-accepted or author-rejected.

## Active records

### R-001

Subject: mm/mglru: fix using folio_mark_accessed to replace
  folio_set_active
Author: Barry Song (Xiaomi). Version: [PATCH], 2026-10-16 PT.
Status: PENDING author/maintainer feedback; source-verified leads.
References: earlier commit `6cbdd9726fb5`. Sashiko attributed
  proposed commit `fa50b3cc1b1d64cb457afbbf37dc545c6d4e06f1`
  (not independently verified as merged).

Findings:
- R-001/F1: Proposed `lru_gen_folio_seq()` treats
  `PG_active && !PG_workingset` on file folios as prefault readahead.
  Migration can carry precisely this state from an active generation;
  reinsertion changes `max_seq-1` to `max_seq-2`. Identified by AKPM
  review and independently by Sashiko. Source path was traced.
- R-001/F2: `evict_folios()` relies on `PG_active` to keep rejected
  folios out of the oldest generation. With three generations, the new
  calculation can put a non-workingset file folio straight back into
  `min_seq`. Noted by Sashiko and verified against MM source here.
- R-001/F3: `shrink_folio_list()` sets `PG_active` for dirty or other
  unreclaimable file folios. The new generation calculation puts a
  non-workingset folio in an older generation. Noted by Sashiko and
  source-verified here.
- R-001/F4: `WORKINGSET_ACTIVATE_FILE` is counted for a non-workingset
  file refault even though its final generation is inactive. Found
  by both reviews; source-verified.

Next: await actual author feedback; validate each claimed failure and
  any higher-level guards before deciding disposition. Do not confuse
  source-verification with author confirmation.
Method lesson: check EVERY writer and consumer of changed state, plus
  failed-reclaim and alternative activation paths. This is already
  generalized into the AKPM workflow.

### R-002

Subject: mm: multi-gen LRU: fix NULL lruvec->pgdat deref with memcg
  disabled on cmdline
Author: Siddharth Chintamaneni. Latest: [PATCH v2 1/2] and [2/2],
  2026-10-17 UTC. Earlier review: v1 and author reply 2026-10-16 PT.
Status: v2 source reviewed; no introduced defect found; PENDING
  author/maintainer feedback and runtime verification.
V2 input: `mbox(20261017-195805)`; Message-IDs:
  <20261017050928.128582-1-sidchintamaneni@gmail.com>
  <20261017050928.128582-2-sidchintamaneni@gmail.com>
Source comparison: `mm/vmscan.c` preimage blob `f11491ee9ed5` at
  mainline `70dd4ee72eb2d5793c62e71c14e3aba78e5a4e56`;
  no explicit base-commit in the supplied v2 mbox.
Fixes: [1/2] `e4dde56cd208` (per-node MGLRU memcg lists),
  [2/2] `ec1c86b25f4b` (MGLRU groundwork); both verified.

Findings:
- R-002/F1: The one-line change from `&pgdat->__lruvec` to
  `mem_cgroup_lruvec(NULL, pgdat)` initializes `lruvec->pgdat` when
  `CONFIG_MEMCG=y` but `cgroup_disable=memory`; sound for reported
  early-boot crash. Under `CONFIG_MEMCG=n`, the helper is a no-op.
- R-002/F2: Similar-code search found `get_lruvec()` in `mm/vmscan.c`
  returning `&pgdat->__lruvec` directly for disabled memcg. MGLRU
  debugfs uses it before `lruvec_pgdat()`, potentially the same NULL
  dereference if no other initializer ran. Plausible path identified,
  but not reproduced. Proposed to investigate use of
  `mem_cgroup_lruvec(NULL, pgdat)` there too.

Author feedback (2026-10-16 PT): The author replied to the sent
  review message, initially asking to replace the special-cased code
  with `mem_cgroup_lruvec()`. His follow-up proposes simplifying the
  whole local helper `get_lruvec(memcg, nid)` to:

      struct pglist_data *pgdat = NODE_DATA(nid);
      VM_WARN_ON_ONCE(!memcg && !mem_cgroup_disabled());
      return mem_cgroup_lruvec(memcg, pgdat);

Assessment: Recommended. Valid calls retain their selected lruvec,
  and the common helper also initializes/reinitializes its pgdat link.
  The warning preserves the existing invalid-NULL-memcg diagnostic.
  A NULL memcg with memcg *enabled* is already a WARN case: the old
  code returned the node lruvec; the new code returns the root memcg's
  per-node lruvec, a change only in that unsupported case.
  Keep the original `lru_gen_shrink_node()` fix too.

V2 focused review (2026-10-17):
- [1/2] uses `mem_cgroup_lruvec(NULL, pgdat)` for disabled memcg
  reclaim. This initializes the node `lruvec->pgdat` under
  `CONFIG_MEMCG=y` and retains the node lruvec selection. Under
  `CONFIG_MEMCG=n` the helper is a stub and `lruvec_pgdat()` uses
  `container_of()`, so the initialization is unnecessary.
- [2/2] implements the proposed common-helper `get_lruvec()`.
  The source shows the MGLRU debugfs iterator uses this helper and
  reads `lruvec_pgdat()`. The common helper selects and initializes
  the correct lruvec on both disabled and enabled memcg paths.
- The previous invalid `memcg == NULL` with memcg enabled WARN
  remains. Its post-WARN return changes to the root memcg lruvec,
  but no supported path relies on the old value; not a reported bug.
- Similar-bug source search found the only direct node `__lruvec`
  accesses in vmscan.c at the two changed sites. Initialization in
  mm/mm_init.c is not another consumer; no further sibling found.
- No v2 regression established. v2 reproducer and stack traces are
  author-provided evidence, not tests executed in this review.
  No build, runtime test, or parallel subagents here. The two review
  passes were performed sequentially.
- Guidance: Tejun `c8cc6a8bee854cf2850f44e0a61be581c19f1d4e`
  and Chris `d048f8742f6740c38833adf02e87901412d771ca`,
  verified 2026-10-17; relevant core, MM reclaim, false-positive and
  build guidance consulted. Sashiko's weekly refresh was not due;
  previously accepted verification techniques applied.
Next: await maintainer/author feedback and any runtime confirmation;
  no source-based changes requested for v2.
Method lesson: search nearby MM for sibling instances of the *cause*,
  not just calls to the changed function. Added to AKPM workflow.

### R-003

Subject: mm/vma: avoid spurious write locks when mm->mm_lock_seq
  overflows
Author: Lorenzo Stoakes (ARM). Version: [PATCH v2], 2026-10-16.
Status: PENDING author/maintainer feedback; no demonstrated new bug.
Patch base: `5ba29027115bc6717b8d6dc3296aae0240933811`.
Related prior commits: `5e31275cc997`, `e5e7fb278e59`.

Findings:
- R-003/F1: On sequence wrap, stale `vm_lock_seq` may alias a later
  mmap write-lock sequence and bypass reader exclusion. The patch
  resets VMAs to zero at wrap, treats only odd equal sequences as
  write-locked, and adds `smp_load_acquire()` on `vm_lock_seq`.
  No introduced regression established on reviewed paths.
- R-003/F2: Sashiko claimed `raw_read_seqcount(&mm->mm_lock_seq)`
  lacked an acquire load. DISMISSED as a false positive after source
  expansion: `raw_read_seqcount()` -> `seqprop_sequence()` ->
  `__seqprop_sequence()` -> `smp_load_acquire(&s->sequence)` for
  `seqcount_t` in `include/linux/seqlock.h`. This was a claim from a
  third-party AI review, not a finding endorsed by our review.
- R-003/F3: Requested testing of actual wraparound, concurrent
  read/write paths, and performance impact of the extra acquire;
  suggestions, not demonstrated code defects.

Next: await author feedback or test results. If author reports a
  different concurrency counterexample, trace the exact interleaving.
Method lesson: expand through macros and type-specific helper variants
  before claiming absent memory ordering. Keep the general rule, not
  a patch-specific exception.

### R-004

Subject: mm/ksm: keep smart scan from losing duplicate pages
Author: Qiliang Yuan. Version: [PATCH 0/2], 2026-10-16.
Message-ID: <20261016-bug-mm-ksm-smart-scan-align-skips-v1-0-2f91d76416be@gmail.com>
Input: `mbox(20261016-231939)`.
Status: PENDING author feedback; design suggestion, not proven bug.

Findings:
- R-004/F1: Per-page smart-scan skip counters leave scans out of
  phase. Aligning the skip schedule to global scan number is intended
  to address this, but changes the scan schedule and potentially work
  bursts.
- R-004/F2: Proposed separating a correctness-only change retaining
  old skip counts (periods 2, 3, 5, 9) from an optional throughput
  change (periods 2, 4, 8), followed by a selftest [3/3].
- R-004/F3: The `ksm_wait_full_scans()` test helper may spin without
  a bounded wait if progress stops; NUMA configurations deserve
  scrutiny. This was a review concern, not demonstrated failure.

Next: inspect subsequent patch revision or author response, and
  distinguish correctness requirements from pacing policy.

### R-005

Subject: ipc/sem: account enlarged sops arrays to memcg
Author: Wang Yingjie (from prior discussion; no original patch here).
Version: patch examined 2026-10-16. Original Message-ID not retained.
Status: PENDING author feedback; reply drafted, not confirmed sent.
Input for reply: `semopm-review-reply.txt`.

Findings:
- R-005/F1: `nsops` is unsigned while `ns->sc_semopm` is signed.
  A negative SEMOPM can bypass the intended upper bound due to unsigned
  conversion. This is a pre-existing input-validation problem.
- R-005/F2: Enlarged `sops` allocation is not sufficiently protected
  in the root or unlimited memcg by merely adding memcg accounting.
  Proposed limits: init IPC namespace 1..INT_MAX for compatibility;
  non-init namespaces 1..1000 as a policy change requiring changelog.
- R-005/F3: `proc_ipc_sem_dointvec()` writes the live limit before
  validating; recommended staged validation prior to publication.
  Proposals are not accepted changes unless author agrees.

Next: collect author feedback before labeling recommendations as
  fixes. Reevaluate whether the 1000 limit is appropriate.

### R-006

Subject: mm/vmalloc: read vm_map_ram block regions from the requested
  offset
Author: Nickolai Zeldovich. Version: [PATCH v1], 2026-10-17.
Message-ID: <20261017154120.795844-1-nickolai@csail.mit.edu>
Base: `70dd4ee72eb2d5793c62e71c14e3aba78e5a4e56`
Fixes: `06c8994626d1` (verified against original commit).
Status: PENDING author feedback; read-only source review, no build or
  kernel runtime test performed. Two separate sequential passes were
  performed; no parallel review agents were available.

Upstream guidance checked for this review:
- Tejun: `c8cc6a8bee854cf2850f44e0a61be581c19f1d4e`;
  2026-10-17, applicable review, evidence and model modules.
- Chris Mason: `d048f8742f6740c38833adf02e87901412d771ca`;
  2026-10-17, core, technical, false-positive, build and relevant
  MM allocation, XArray, locking and RCU guidance successfully loaded.
- Sashiko: weekly refresh not due. Applied previously accepted
  hypotheses/dispute/independent-path verification techniques.

Findings:
- R-006/F1: The two proposed changes (skipping earlier used-map runs
  and deriving the copy offset from `addr - start`) fix the reported
  wrong-page reads through `/proc/kcore`. Confirmed against the full
  `vmap_ram_vread_iter()` and its `read_kcore_iter()` caller.
- R-006/F2: The patch retains `(re - rs + 1) << PAGE_SHIFT` when it
  computes `size`. `for_each_set_bitrange()` produces half-open
  `[rs, re)` ranges, verified in `include/linux/find.h`. Therefore the
  extent incorrectly includes the first clear bitmap page. During
  `vb_free()`, `bitmap_clear()` precedes `vunmap_range_noflush()`;
  a reader of that first cleared page can copy its still-present
  mapping instead of zero-filling it. The off-by-one is pre-existing
  (already in `06c8994626d1`), but this patch carries it forward.
  Proposed correction: `size = (re - rs) << PAGE_SHIFT`.
- R-006/F3: Finite enumeration: 78,336 stable bitmap/read cases matched
  expected contents for either width. A concrete transient bitmap/PTE
  mismatch returned stale page contents with the retained `+1`, versus
  zero with the corrected size. These are logic tests, not kernel tests.

Dismissed leads: `start + size` address overflow is blocked by the
  bounded block allocation and `vread_iter()` range clipping; no
  new lock ordering, non-block VMAP_RAM path, or vb lifetime change.
Model: no formal model; local interval arithmetic and an explicit
  two-actor ordering path suffice. No herd7 or TLC was run.
Next: recommend v2 with the one-line size correction and consider a
  test for an interior freed page followed by another live allocation.
Method lesson: verify iterator/macro endpoint conventions against the
  implementation before computing interval sizes. The independent
  pass originally assumed an inclusive `re` and missed this bug.


### R-007

Subject: proc/kcore: advance the vmalloc retry by the last copy,
  not the total
Author: Nickolai Zeldovich. Version: [PATCH v1], 2026-10-16 PT.
Base: `70dd4ee72eb2d5793c62e71c14e3aba78e5a4e56`.
Fixes: `4c91c07c93bb` (verified in the introducing commit).
Status: PENDING author/maintainer feedback; no regression established.

Finding R-007/F1: The old `KCORE_VMALLOC` retry loop accumulates bytes
  in `read`, then incorrectly advances `src` and decreases `left` by
  that total. Multiple short copies from a multi-iovec destination
  can overadvance the source and underflow `left`, producing `EFAULT`.
  The patch advances by this call's `n` and preserves `read` for the
  completion test. The source and iterator now advance equally, and
  `read + left == tsz` is maintained. Recommend taking the patch.

Verification: Examined `read_kcore_iter()`, `vread_iter()`,
  `aligned_vread_iter()`, `copy_page_to_iter_nofault()`,
  `iterate_iovec()`, `fault_in_iov_iter_writeable()`, and the original
  Fixes commit. Similar retry loops in GFS2 and Btrfs use the correct
  respective return-value semantics; no confirmed sibling found.
  Reproducer statistics are author-reported, not independently run.

Minor prose observation: access to `/proc/kcore` is checked with
  `CAP_SYS_RAWIO`, not strictly UID 0. Optional wording cleanup only.
  No claim of bad data on successful reads was independently shown.

Guidance: Tejun `c8cc6a8bee854cf2850f44e0a61be581c19f1d4e`;
  Chris `d048f8742f6740c38833adf02e87901412d771ca` checked
  2026-10-17. Sashiko weekly refresh not due; existing techniques
  applied. Passes were sequential; no subagents, build, live test,
  TLC or herd7. Model: no (local retry/accounting arithmetic).

Next: await author feedback. No new generalizable workflow change;
  existing producer/consumer and similar-code checks cover this case.

## Methodology studies

### L-001

Subject: mm: retry page faults once under the per-VMA lock
Input: `mbox(20261017-211929)`; 12 messages, 2026-09-11 to 2026-10-03.
Root Message-ID: <20260911025613.1220845-1-zhanghongru@xiaomi.com>
Supplied v6 base: `3628c3df6cd2797b34714d23113cd44cb30801e7`.
Status: methodology study completed 2026-10-17, NOT a completed review
  of v6 or its experimental alternatives. No merge verdict inferred.

Evidence and distinctions:
- Lorenzo's 2026-09-21 reply <arFYRAa-i7CIwmHL@gremlin> challenges
  the workload framing, overloaded retry semantics, architecture
  duplication and the cost of a small workaround. His 2026-09-22
  follow-up allows an interim fix alongside longer-term redesign.
- Matthew's 2026-09-21 reply
  <arF-E3Nsw9ZliH0t@casper.infradead.org> distinguishes retry from a
  requirement for mmap_lock and corrects some AI-derived claims. Treat
  that list as disputed leads, not a verified catalogue of bugs.
- Matthew's 2026-10-01 alternative
  <ar7MsOb6IJLt4eLo@casper.infradead.org> removes parent VMA write
  locking during fork. Lorenzo's 2026-10-02 response
  <ar-o1TrOMGrrcxLX@gremlin> cites past corruption and explains parent
  CoW/TLB, THP and PTE-table stability assumptions, plus contention
  shifted to other VMA writers. This concerns the alternative, not a
  demonstrated regression introduced by Hongru's original retry patch.
- Independently fetched historical commit
  `fb49c455323ff8319a123dd312be9082c49a23a5`: it adds parent VMA
  write locking and explains source-VMA/anon_vma stability during fork.
  The other detailed source claims in this thread were not all audited.
- Xueyuan reports real-app gains; Hongru supplies a writer-queue causal
  explanation, more app measurements and a Perfetto screenshot. Barry
  identifies Android KMI constraints and prior VMA-lock/fork contention.
  These are supplied observations, not tests run in this study. The
  screenshot is not a complete before/after performance validation.

Method change: architectural framing, safeguard provenance, whole-
  operation invariants, cost shifting and bounded alternatives are now
  in the standalone AKPM workflow. Preserve rejected designs and their
  reasons between revisions. Do not label this as a prior false negative
  by our review: no earlier review of this v6 patch is recorded here.
Upstream review prompts were not refreshed for a methodology-only study.

## Maintenance reminder

When feedback arrives, update findings and dispositions here. Archive
resolved OR dormant reviews into that day's
`review-activity-YYYY-MM-DD.md`, leaving the normalized Subject and
filename above. Keep this file lean; retain durable lessons in the
AKPM workflow only when broadly applicable.
