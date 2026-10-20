# Review activity - AKPM

Last updated: 2026-10-19 (America/Los_Angeles)
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
Last checked: 2026-10-19 (America/Los_Angeles)
Checked HEAD: `cbb4478d0f73e15907335e70a2dc2fe54a9e7167`
Previous HEAD: `c8cc6a8bee854cf2850f44e0a61be581c19f1d4e`
Change: `$MODEL_CHECKER` introduced in `UPGRADING.md`; default
`tla-mctj`. Other relevant module changes: formal-model guidance.
HEAD commit date: 2026-10-18 06:22:24 UTC
HEAD subject: Merge pull request #1 from htejun/overlay-flush
Last comparison: 2026-10-19 (America/Los_Angeles)
Status: compared current HEAD with previous recorded checkpoint.
`UPGRADING.md` now adds `$MODEL_CHECKER`, default `tla-mctj`.

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
Last checked: 2026-10-19 (America/Los_Angeles)
Checked HEAD: `d048f8742f6740c38833adf02e87901412d771ca`
HEAD commit date: 2026-10-01 11:53:46 UTC
HEAD subject: README: add pahole to the project lists
Status: unchanged from previous verified prompt baseline.
Last comparison: 2026-10-19 (America/Los_Angeles)
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
Last checked: 2026-10-19 (America/Los_Angeles)
Checked HEAD: `f6e2e172e1e669b6767a4c74fe91d062b41fd71c`
Previous HEAD: `f4b72fa04f232fe5f2183d32d7cf9c09e5d735ec`
Difference: pipeline prescreen/planner temperature propagation;
seven analysis domains unchanged. Full manual track covered in R-016.
HEAD commit date: 2026-10-19 21:20:55 UTC
HEAD subject: docs: add LWN 7.3 development statistics article to PRESS.md
Last comparison: 2026-10-19 (America/Los_Angeles)
Comparison: advanced from prior SHA; reviewer verified latest diff is
PRESS.md-only and earlier workflow changes carry temperatures to stages.
Verified the pinned pipeline plus applicable core, specialist and
false-positive sources at this SHA. Native Sashiko: not run.

Accepted techniques: preserve substantive dismissed hypotheses with
source evidence; independently verify disputed claims and dismissals;
keep distinct failure mechanisms separate. These are local additions to
the existing two-pass review, not a Sashiko review pipeline.

Check HEAD at each substantive review. If advanced, inspect deltas
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
  ACTIVE: [R-006](#r-006); v2 correct; maintainer asks simplify.
- `proc/kcore: advance the vmalloc retry by the last copy, not the total`
  ACTIVE: [R-007](#r-007); v1 source-reviewed, no defect found.
- `mm/mremap: do not charge a shrinking move twice`
  ACTIVE: [R-008](#r-008); v1 code sound, changelog needs correction.
- `ucount: take the rlimit reference before checking the limit`
  ACTIVE: [R-009](#r-009); v1 source-reviewed, code sound.
- `lib/buildid: reject file offsets that do not fit in pgoff_t`
  ACTIVE: [R-010](#r-010); v1 sound, security coordination pending.
- `mm/mempolicy: apply bind policies against the scoped allocation zone`
  ACTIVE: [R-011](#r-011); source-reviewed, take as submitted.
- `zram: redesign zcomp and rework backends`
  ACTIVE: [R-013](#r-013); v5 source-reviewed; tests requested.
- `mm/ksm: keep soft-dirty and uffd-wp when merging a page`
  ACTIVE: [R-015](#r-015); zero-page soft-dirty case omitted.
- `kasan: fix runtime shadow page table synchronization`
  ACTIVE: [R-014](#r-014); v2 must be revised; shared-table bugs.
- `mm/memory-tiers: reset demotion targets of nodes without memory`
  ACTIVE: [R-016](#r-016); one-line code appears sound; original
  mail/changelog unavailable, so unconditional acceptance withheld.
- `fs/proc/task_mmu: pin mm_users in do_pagemap_scan()`
  ACTIVE: [R-017](#r-017); fix sound; `!mm` masks Oops; tests needed.
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
Author: Nickolai Zeldovich. Latest: [PATCH v2], 2026-10-17.
V1 Message-ID: <20261017154120.795844-1-nickolai@csail.mit.edu>.
V2 Message-ID: not supplied in this chat; v2 full patch supplied.
Base: `70dd4ee72eb2d5793c62e71c14e3aba78e5a4e56`.
Fixes: `06c8994626d1` (verified introducing commit).
Status: v2 behavior source-reviewed and correct; maintainer requests
  clearer endpoint-based implementation. PENDING revised patch; author
  tests not independently reproduced.

Findings and v1-to-v2 resolution:
- R-006/F1: v1 and v2 skip expired used-map runs and copy at the
  requested offset (`addr - start`). Verified against the entire
  `vmap_ram_vread_iter()` and its `vread_iter()` and kcore callers.
- R-006/F2: v1 retained a pre-existing off-by-one: it counted
  `[rs, re)` as `(re - rs + 1)` pages, including the first clear bit.
  With `vb_free()` clearing used-map bits before unmapping, a reader
  could copy a newly freed page. V2 correctly uses `(re - rs)` pages.
  The author supplied an additional `msleep()` race reproducer showing
  zero-fill with v2; the author ran it, not this reviewer.
- R-006/F3: V2 finite enumeration checked 135,168 combinations of
  eight-bit page-occupancy maps, read offsets and lengths with a
  four-byte simulated page; all matched the expected bitmap-based
  contents. This tests stable-map arithmetic, not kernel concurrency.

Architectural/historical check (v2): Introducing commit `06c8994626d1`
  deliberately made used-map regions readable and holes zero-filled.
  The bitmap defines the intended public `/proc/kcore` contents, not
  temporarily present page-table mappings. Fixing the reader rather
  than changing kcore or the alloc/free ordering is correctly scoped.
  `vb_alloc()` sets bits under `vb->lock`; `vb_free()` clears them
  under that lock before unmapping. `vread_iter()` retains its
  `vn->busy.lock` while the block reader obtains `vb->lock`.
  `free_vmap_block()` unlinks the VA under `vn->busy.lock` before RCU
  freeing the block, so no new block-lifetime problem was found.
  Direct, non-VMAP_BLOCK allocations follow `aligned_vread_iter()`
  unchanged. The separate kcore retry issue is tracked as R-007.

Dismissed leads: `start + size` stays within the block's VA range;
  the copy size is capped by `remains`; zero-fill handles holes and
  partial user copies. No new lock nesting or material fast-path cost.
Model: no formal model; local interval logic and lock order suffice.
  No kernel build, runtime test, TLC or herd7 was executed here.
Review: two sequential passes, no parallel subagents. Tejun
  `c8cc6a8bee854cf2850f44e0a61be581c19f1d4e`; Chris
  `d048f8742f6740c38833adf02e87901412d771ca` checked
  2026-10-17. Sashiko weekly refresh not due; prior methods applied.
Maintainer feedback (2026-10-18, Uladzislau Rezki): simplify the
  arithmetic to the payload [start, end) and current read addr.
  Express skip as addr >= end; zero-fill before start; read from
  addr for min(end - addr, remains), eliminating offset and size.
  This is a clarity improvement, not a newly identified defect.
  Compute end = start + ((re - rs) << PAGE_SHIFT); do not call
  vmap_block_vaddr(va_start, re): at re == VMAP_BBMAP_BITS its
  same-block BUG_ON would trigger at the exclusive end.
Next: request/await a simplified revision, preserve v2 behavior
  and half-open interval tests. No revised kernel code was built
  or run. General lesson: verify correctness and then separately
  ask whether the code expresses the invariant directly.


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

### R-008

Subject: mm/mremap: do not charge a shrinking move twice
Author: Nickolai Zeldovich. Version: [PATCH v1], 2026-10-17.
Base: `70dd4ee72eb2d5793c62e71c14e3aba78e5a4e56`.
Fixes: `b714ccb02a76` (refactoring move_vma; verified).
Status: PENDING author/maintainer feedback; no introduced defect found.

Findings:
- R-008/F1: `check_prep_vma()` records original `vrm->delta` as the
  positive length difference. `mremap_to()` unmaps the shrink tail
  (which uncharges VM_ACCOUNT), then changes `vrm->old_len` to
  `vrm->new_len` without updating delta. `move_vma()` calls
  `vrm_calc_charge()`, which charges the stale positive delta through
  `security_vm_enough_memory_mm()`. The move's source unmap suppresses
  uncharging using VMA_ACCOUNT, and the extra global commitment survives
  future unmap/exit. An original 2 MiB -> 1 MiB move leaks 1 MiB of
  Committed_AS. The proposed second `vrm_set_delta()` sets delta=0
  after the shrink; both successful and failed move paths keep correct
  charging. Recommend taking the one-line patch.
- R-008/F2: Every use of `vrm->delta` in mm/mremap.c was inventoried.
  Early checks and shrink operation use the original value, before the
  reset. Non-fixed in-place shrink, expansion and MREMAP_DONTUNMAP do
  not take the changed path. `remap_move()` recalculates delta when
  processing same-sized subranges; `copy_vma_and_data()` may also
  change old_len on error but no subsequent delta consumer depends on
  it. The unchanged remap_type still describes the initial request.
- R-008/F3: Material changelog correction requested: the statement
  that a move which does NOT unmap its source needs only a growth charge
  is backwards. `vrm_calc_charge()` charges the entire new mapping for
  `MREMAP_DONTUNMAP` and just delta for the ordinary move, which unmaps
  its source. Here shrink_vma() already uncharged the tail, so the
  subsequent ordinary move requires zero extra pages. Also optional:
  "every accounted allocation ... fails until reboot" is too absolute,
  as unrelated mappings may be released. `vrm_set_delta()`'s comment
  "specified by user" should refer to the now-current remap lengths.

Architecture/history: correct layer for charge delta is `mremap_to()`
  after mutation of lengths and before `move_vma()` charges. Similar
  known MREMAP_DONTUNMAP `VM_ACCOUNT`/locked_vm corrections from the
  same historical refactor are distinct and not touched by this patch.
Author tests: QEMU x86_64 defconfig; 1000 shrink/moves leaked 1 GiB
  before, zero afterward (author-reported, not run here).
Verification: source examined in mm/mremap.c, mm/vma.c, mm/mmap.c,
  mm/util.c, and original Fixes commit. No build/runtime test.
Guidance: Tejun `c8cc6a8bee854cf2850f44e0a61be581c19f1d4e`;
  Chris `d048f8742f6740c38833adf02e87901412d771ca`, checked
  2026-10-17. Two sequential passes; no parallel subagents.
Model: no (local derived-state and accounting arithmetic; no new
  concurrency protocol).
Next: request corrected changelog before taking; code itself sound.
  Consider Cc stable due systemic overcommit regression. Await feedback.
No new general workflow rule: current bug/fix/architecture and full
  consumer inventory requirements cover the missed-state pattern.

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

### R-009

Subject: ucount: take the rlimit reference before checking the limit
Author: Nickolai Zeldovich. Version: [PATCH v1], 2026-10-17.
Base: `70dd4ee72eb2d5793c62e71c14e3aba78e5a4e56`.
Fixes: `15bc01effefe` (verified introduction in 2021).
Status: PENDING author/maintainer feedback; no introduced defect found.

Findings:
- R-009/F1: Old `inc_rlimit_get_ucounts()` increments a per-namespace
  rlimit count before checking max, but takes the extra `get_ucounts()`
  reference only after passing that check. A 0->1 increment failing
  its limit while another override-rlimit charge increments to 2 can
  leave an accepted positive count without its expected extra ref.
  A later 1->0 decrement calls an unmatched `put_ucounts()`, risking
  premature removal/free of a live ucounts and its pinned namespace.
  The reverse interleaving can leak the extra reference.
- R-009/F2: The patch takes `get_ucounts()` upon observing new==1 before
  testing the limit, then uses `do_dec_rlimit_put_ucounts(ucounts,
  iter->ns->ucounts, type)` to unwind the rejecting level inclusively.
  The helper's stop argument is exclusive and caches `next` before
  calling `put_ucounts()`. The no-reference-acquired `dec_unwind` case
  remains unchanged. No new lock or blocking operation introduced.
- R-009/F3: `kernel/signal.c` uses this API for SIGPENDING; ordinary
  realtime signal queues enforce the limit while forced synchronous
  signals can bypass it. Task credentials are read under RCU and the
  namespace/ucounts chain supplies lifetime protection during lookup.
  Other rlimit counter APIs use distinct rlimit types (NPROC, MEMLOCK,
  MSGQUEUE), so no confirmed analogue of this reference-handoff bug.

Verification: inspected kernel/ucount.c, kernel/signal.c,
  include/linux/user_namespace.h, kernel/user_namespace.c,
  include/linux/rcuref.h and introducing Fixes commit. A bounded
  two-participant scheduler model reached both unmatched-put and
  leaked-reference outcomes in the old ordering, and neither in the
  patched ordering (48 old states, 58 patched states). This is a
  simplified interleaving model, not a kernel test or formal proof.
Architecture: fix belongs in the common rlimit increment/reference
  handoff. The extra reference represents positive occupancy at each
  hierarchy level, not a reference per queued signal. Caller-held
  lifetime must cover the short interval from atomic increment to
  conditional get; verified for the signal caller and parent chain.
Tests: author reports a reproducer under KASAN/rcuref debug, but its
  code and output were not supplied. No build/runtime test here.
Guidance: Tejun `c8cc6a8bee854cf2850f44e0a61be581c19f1d4e`;
  Chris `d048f8742f6740c38833adf02e87901412d771ca`, checked
  2026-10-17. Two sequential passes, no parallel review subagents;
  Sashiko weekly refresh not due. No TLC/herd7 used.
Reassessment (2026-10-17 PT; stable rules and user-impact gate):
- impact-changelog: sufficient. The text identifies CONFIG_USER_NS,
  privilege and signal-limit conditions, a concrete stale reference
  outcome, and possible premature freeing/UAF or retained namespace.
  These are source-supported possible harms, not known fleet incidents.
- stable: prospective candidate upon mainline merge. A reproducible
  harmful race needs no previously reported victims. Recommend
  `Cc: stable@vger.kernel.org` in commit trailers, not just email Cc.
  Author says KASAN/rcuref reproducer exists; code and diagnostic output
  have not been supplied, and older-branch backports are not tested.
- Concrete reachability refinement: ordinary signal delivery and
  forced synchronous delivery both hold the target `sighand->siglock`.
  Two threads sharing that sighand cannot execute those paths in
  parallel. The cited scenario requires two distinct sighands sharing
  one per-(user namespace,UID) ucounts (e.g. separate processes).
  Request clarification of the author's reproducer, not a code change.
- Fresh bounded two-actor scheduler check (one limit failure, one
  accepted charge, both role orderings) found an unmatched put and a
  leaked ref under old ordering (30 states per case); patched ordering
  balanced both cases (38 states per case). Only a finite logical
  interleaving test; assumes valid caller references and successful
  get_ucounts(), not a kernel run, LKMM proof, or actual exploit.
Next: take code; ask for distinct-sighand explanation and brief
  before/after reproducer output; recommend stable trailer. Await
  author/maintainer feedback.

### R-010

Subject: lib/buildid: reject file offsets that do not fit in pgoff_t
Author: Nickolai Zeldovich. Version: [PATCH v1], 2026-10-17.
Base: `70dd4ee72eb2d5793c62e71c14e3aba78e5a4e56`.
Fixes: `de3ec364c3c3` (verified in 2024-09-11 introducing commit).
Input: `Pasted text(20261018-014757).txt` (private security report).
Status: PENDING author/security maintainers' feedback. Source review
  supports the overflow and repair; no independent kernel test/build.

Findings:
- R-010/F1: On 32-bit, `file_off >> PAGE_SHIFT` (from 64-bit loff_t)
  narrows to 32-bit pgoff_t for `filemap_get_folio`. An out-of-range
  ELF64 header offset can select the wrong cached folio. `freader_fetch`
  assumes it covers the requested offset; when it does not, the
  cross-folio size subtraction underflows and the ensuing `memcpy`
  can exceed the 64-byte on-stack buffer in `__build_id_parse`.
  Author reports an i386 stack-protector panic, not reproduced here.
- R-010/F2: Proposed guard in `freader_get_folio()` rejects negative
  and above-MAX_LFS_FILESIZE file offsets before `filemap_get_folio`.
  On 32-bit, MAX_LFS_FILESIZE bounds the page index representable by
  pgoff_t; on 64-bit it is LLONG_MAX. Guard is also exercised for
  subsequent folio fetches. The faultable __kernel_read path and
  memory-backed reader are not changed. No introduced defect found.
- R-010/F3: Perf hook in `kernel/events/core.c` uses the nofault build
  ID reader when the global `nr_build_id_events` is nonzero. BPF
  build-ID stack maps also reach it. Exposure depends on the presence
  of an active build-ID perf event and perf/BPF access policies. The
  author demonstrates the trigger with perf configured to permit his
  test; do not imply every default configuration admits an unprivileged
  event creation. This is changelog qualification, not code defect.

Architecture: correct layer to validate an offset before converting to
  pgoff_t; existing `freader_fetch()` copy-size precheck only ensures
  the requested `sz` fits, not a computed `part_sz` after invalid folio
  lookup. Avoid changing general page-cache APIs for a bad caller.
Impact-changelog: sufficient for observed stack corruption and general
  affected scope; consider clarifying the active perf-event prerequisite
  and distinguish demonstrated panic from any exploitability claims.
Stable: prospective candidate after upstream/security coordination;
  severe source-supported corruption on 32-bit, tested per author;
  verify stable targets and avoid a public stable trailer before the
  security process permits publication. For unpublished vulnerability,
  stable-kernel-rules documents `Cc: stable@kernel.org` privately.
Guidance: Tejun `c8cc6a8bee854cf2850f44e0a61be581c19f1d4e`;
  Chris `d048f8742f6740c38833adf02e87901412d771ca`, checked
  2026-10-17. Used MM folio, BPF, core, evidence, false-positive and
  build guides. Sashiko weekly refresh not due. Sequential passes;
  no formal model, live reproducer, build, KASAN or public disclosure.
Next: take code; request only a precise note on build-ID perf event
  prerequisites if author replies. Handle privately with recipients and
  security team; do not redistribute supplied reproducer publicly.

### R-011

Subject: mm/mempolicy: apply bind policies against the scoped allocation zone
Author: Gregory Price (Meta). Version: [PATCH], 2026-10-17 PT.
Diff preimage: `mm/mempolicy.c` blob `70298fded1b4a` (user supplied).
Base commit not supplied; inspected equivalent policy, allocator, GUP and
hugetlb code in upstream `master` at
`58161ead29e50d70a317ea26b472e0c7508e69da` (Oct 17).
The exact diff preimage was not independently resolved to a kernel tree.
Fixes: `8e3560d963d2` (verified introducing `PF_MEMALLOC_PIN`
`current_gfp_context()` behavior in 2021-05-05 commit).
Status: PENDING author/maintainer feedback; no introduced defect found.

Findings:
- R-011/F1: `policy_nodemask()` tests the original `gfp_zone(gfp)`
  when deciding whether `MPOL_BIND` to a movable-only node applies.
  Long-term GUP under `memalloc_pin_save()` sets `PF_MEMALLOC_PIN`;
  actual page allocator applies `current_gfp_context()` and strips
  `__GFP_MOVABLE`, so no eligible zone intersects the retained mask.
  Faulting previously untouched pages for long-term pins can fail.
- R-011/F2: Using `gfp_zone(current_gfp_context(gfp))` when applying
  the policy uses the same scoped zone as the buddy allocator. No
  change for non-pin scopes, or where __GFP_MOVABLE is absent; preserves
  the prior policy relaxation for ineligible zones. Covers base
  page allocations, hugetlb `huge_node()`, and bulk mempolicy allocator.
- R-011/F3: The analogous `policy_mbind_nodemask()` in mm/hugetlb.c
  also tests the unscoped GFP zone, but is associated with hugetlb pool
  reservation/resize, not established as a path running under long-term
  GUP pin scope. No additional demonstrated bug; not a blocker.

Impact-changelog: sufficient: QEMU/VFIO guest launch fails -ENOMEM;
  io_uring registration/pinning of unfaulted pages fails; hugetlb
  fault path may fail -EFAULT; movable-only NUMA binding is required.
  Author reports after-fix qemu, VFIO, io_uring and 2 MB hugetlb tests.
Stable: prospective candidate after upstream merge; real user-visible
  failures; `Cc: stable@vger.kernel.org` already in commit trailers.
  Target releases require branch verification, not attempted here.
Architecture: correct decision-layer fix; existing `apply_policy_zone()`
  deliberately relaxes bindings that cannot provide the required
  allocation zone. No redesign or special treatment in GUP is needed.
Model: no (single local GFP-zone policy decision; source control
  flow and scoped context explain it). No kernel build or live test.
Guidance: Tejun `c8cc6a8bee854cf2850f44e0a61be581c19f1d4e`;
  Chris `d048f8742f6740c38833adf02e87901412d771ca`, verified
  unchanged 2026-10-17. Applied code/allocator/folio, evidence,
  description and false-positive guidance in separate sequential
  pass; Sashiko refresh not due.
Next: take patch; no changes requested. Author's testing not
  independently reproduced. Email reply drafted, not sent.

### R-012

Subject: khugepaged: fix readahead lock inversion in collapse_file()
Author: Lance Yang. Version: [PATCH v3 1/1], 2026-10-16 (+0800).
Input: patch email supplied in chat, 2026-10-17 PT.
Status: HUMAN FEEDBACK RECEIVED; v3 architectural concern reopened.
Fixes: `730633f0b7f9` (2021-07-13; verified introducing the
  invalidate_lock for read/readahead against truncation).

Findings:
- R-012/F1: Verified old inversion: collapse_file() held previous
  source folio locks then entered page_cache_sync_readahead(), which
  acquires mapping->invalidate_lock shared. Truncate holds that rwsem
  exclusively while waiting on one of the source folio locks. The
  syzbot trace shows both waits: ext4_write_end/truncate and
  collapse_file/page_cache_ra_order. Public bug URL:
  https://syzkaller.appspot.com/bug?extid=16bf7cd0ebeb1de93aa5
- R-012/F2: v3's non-shmem preparation pass locks at most one folio
  at once, releases before invoking any readahead, and completes
  readahead calls before collecting locked source folios in the second
  pass. Missing entries discovered in second pass cause rollback,
  not readahead. Xarray locking and rollback ownership traced;
  no code correctness blocker found.
- R-012/F3: Notable change: the preparation pass uses blocking
  filemap_lock_folio() even for resident cached folios; formerly the
  second-pass cached-folio path used folio_trylock() and returned
  SCAN_PAGE_LOCK promptly on contention. This can prolong
  MADV_COLLAPSE or background khugepaged waits. Ask whether intended
  or whether the preparation pass can trylock resident folios.
- R-012/F4: v3 email does not report verification with original
  truncate/readahead reproducer. Request before/after stress/syzbot
  retest on this exact revision; do not claim independently run.

Impact-changelog: sufficient: reproducible uninterruptible hung-task
  lock cycle affecting file-backed collapse, truncate and writes,
  observed syzbot and independent v2-era report. Authors' v2 reports
  do not establish v3 testing.
Stable: candidate; Fixes tag verified, author notes complex old-stable
  branch differences and proposes individually reviewed backports;
  don't presume the v3 diff applies unchanged to all stable versions.
Architecture: two-pass scan preserves existing sync readahead semantics
  rather than replacing with page_cache_ra_unbounded; shortens
  invalidate_lock scope and avoids nesting with retained folio locks.
  Changes between passes are tolerated by abort/rollback.
Model: no full model; simple two-actor wait-for cycle removed by
  reordering; no new lock primitive and no complex state protocol.
Guidance: independent pass followed by Tejun
  `c8cc6a8bee854cf2850f44e0a61be581c19f1d4e` and Chris
  `d048f8742f6740c38833adf02e87901412d771ca` guided pass;
  current heads unchanged as checked for this review. Read
  evidence/code, technical/false-positive, patch-review prompts.
Validation: source-only GitHub master, introductory commit and syzbot
  traces; no build, live reproducer, syzbot test or formal model.
Next: ask Lance about blocking prep-pass folio locks and request
  v3 reproduction test. Pending reply; not sent.

Human follow-up, 2026-10-16 to 2026-10-18, from supplied mbox:
- Pedro Falcato identified the more important design flaw: v3 makes
  every non-shmem collapse do a full preliminary walk, lock/unlock
  cached folios, and drain LRU even when no readahead is necessary.
  Much of the read I/O started by this pass may still be in progress
  when collapse resumes. He proposed readahead only AFTER a failed
  scan has rolled back and released the source folio locks.
- Lance accepted the on-demand idea and posted an exploratory
  post-rollback readahead/retry sketch. It is NOT a submitted v4 or a
  fully reviewed/tested change. This supersedes our premature
  recommendation to take v3 as-is; request a revised design.
- Baolin Wang suggested moving recovery to an existing outer retry
  site (called collapse_pmd() in the thread; the examined mainline
  equivalent is collapse_single_pmd()). Lance noted old stable trees
  lack that outer retry. Baolin replied that clean upstream design
  should not be constrained by backport architecture; David's
  preference was still awaited in the supplied thread.
- Baolin initially asked why xas_unlock_irq() was omitted, then
  retracted the question. At the beginning of the preparation pass
  the xarray lock was never acquired; there is nothing to unlock.
- Baolin questioned PG_uptodate after taking the folio lock. Pedro
  correctly explained that a folio is unlocked after failed I/O too;
  locking does not imply Uptodate. The early check is nonetheless
  duplicated by the real collapse scan, so Lance agreed it can go.
- Baolin also asked for the long new code to become a helper. This
  is readability feedback, distinct from the more consequential
  proposal to avoid the entire unconditional preparation pass.
- Original R-012/F3 blocking-lock concern is source-supported, but
  the human follow-up did not specifically endorse it. Avoiding the
  normal-path pass addresses that concern more structurally.
- No v4, runtime retest or resolution from David is supplied. The
  old deadlock and v3 lock-order cure are still source-supported;
  the final upstream design remains under discussion.

Methodological correction: review fast-path costs of exceptional-case
preparation, compare deferred recovery after rollback, search for
higher-level retry owners, separate check validity from necessity,
track lock state at each new path, and favor upstream design over
backport convenience. General lessons added to the AKPM workflow.

### R-013

Subject: zram: redesign zcomp and rework backends
Author: Sergey Senozhatsky. Version: [PATCH v5 00/13], 2026-10-18
  (+0900). Input: user-supplied mbox with all 13 patches and two older
  v1 discussion replies, 2026-10-17 PT.
Status: SOURCE REVIEW COMPLETE; no proven code defect; ask for
  correctness/stress validation before taking the full series.

Independent pass:
- [01-08/13]: printk prefix, debugfs cleanup, dictionary and workspace
  optimizations, and writeback reset inspected. No confirmed defect.
- [09/13]: compression and decompression stream split preserves each
  backend's mutable-context ownership; zstd/deflate retain exclusive
  dctx, while LZO/LZ4/842 decompression is stateless. CPU hotplug
  releases C/D contexts using their separate locks. No proven defect.
- [10-11/13]: stateless decompression can use a read-held lifetime
  semaphore; mutable dctx and the fallback local_copy require the
  exclusivity mutex. Spanning objects use a GFP_NOWAIT bounce buffer
  with serialized fallback. SG lifetime maintained. No proven defect.
- [12/13]: wait_event() repeatedly scans online CPUs and acquires a
  read pin plus exclusive mutex by trylock. Release wakes waiters;
  bounce-buffer fallback also wakes. The online CPU stream is pinned
  through hotplug teardown. No proven missed wake or UAF.
- [13/13]: secondary compressors are used by recompress_store() under
  dev_lock write; singleton compressor preserves independent per-CPU
  decompressors for reads. Allocation and cleanup paths examined.
- Although read_compressed_page() may sleep between
  zs_obj_read_sg_begin/end(), current zsmalloc's counted reader pin
  explicitly permits sleeping (its writer uses trylock); not a bug.

Actionable feedback:
- Large synchronization and allocation series warrants documented
  round-trip/corruption and CPU hotplug/reset/failure-injection tests,
  especially zstd/deflate dictionaries, lz4hc and multi-CPU exclusive
  stream borrowing. Submitted benchmarks are performance evidence,
  not an exhaustive correctness matrix; no tests run here.
- [08/13] changelog should make the userspace symptom explicit:
  reset of a reused zram device retained writeback limits/options,
  potentially causing unexpected -EIO on later writeback when the
  retained enabled limit is zero. Historical commit cited in prose;
  assess Fixes/stable separately if a maintained branch is affected.
- Older [00/10] replies request deferral until next -rc1; no
  contradiction with current v5, and no request for immediate merge.

Impact-changelog: [08/13] needs a concrete operational example for
  downstream diagnosis; rest are principally performance or local
  resource fixes. Stable: [08/13] possible standalone candidate,
  requires affected-tree confirmation. Do not stable-tag 13-patch
  performance redesign automatically.

Guided review: Tejun HEAD
  c8cc6a8bee854cf2850f44e0a61be581c19f1d4e; Chris HEAD
  d048f8742f6740c38833adf02e87901412d771ca, checked 2026-10-17.
  Inspected patch-review, evidence, kernel-idioms, technical,
  false-positive, block, locking, allocator and build guidance;
  no new source-supported defect from guided pass.
Validation: source-only against submitted diffs, Linux mainline
  backend implementation and public linux-next zsmalloc reference;
  the zcomp SG conversion predates mainline snapshot and was supplied
  as part of the patch preimage. No build, test, formal model or
  independent performance benchmark performed.
Next: request concise functional/stress coverage and strengthen the
  [08/13] changelog; review follow-up before applying a tag. Reply
  drafted, NOT SENT.


### R-014

Subject: kasan: fix runtime shadow page table synchronization
Original Subject: [PATCH v2] kasan: fix runtime shadow page table
  synchronization
Author: Muchun Song <songmuchun@bytedance.com>
Date: 2026-10-18 (message); reviewed 2026-10-17 PT.
Source: `Pasted text(20261018-061334).txt`.
Follow-up: user's Sashiko review of commit
  84e267a96cb1eab3b9fd041e188f62b5f7899dd0.
Base: 63562804f25cb5b6f5e4f5e3a9f0d1c3c6868596
Fixes: 0207df4fa1a869281ddbf72db6203dbf036b3e1a
Status: DO NOT MERGE v2; request a revised patch and tests.

Original findings:
- R-014/F1: Runtime KASAN zero-shadow population can add page tables
  visible only to init_mm. Architecture-specific synchronization is
  necessary. Historical Fixes commit introduced devm_memremap_pages()
  zero-shadow add/remove. This root cause remains valid.
- R-014/F2: The pgalloc tracking helpers and one final sync (including
  partial-failure cases) are sound in principle. The aligned-entry
  guards, however, missed the shared-template cases below.
- R-014/F3: The original review treated retention as only a risk of
  empty page-table allocations. That was an INCORRECT conclusion: v2
  can also retain mapped shared static zero-shadow entries; see F6.
- R-014/F4: The original review checked x86 masks but neglected
  other architectures' *_none() definitions and early-shadow setup.
  This coverage failure enabled F5 to escape both passes.

Sashiko feedback, independently checked against the supplied base:
- R-014/F5 CONFIRMED: LoongArch kasan_init() first calls
  kasan_pgd_populate(..., early=true), then
  kasan_populate_early_shadow() for VMALLOC..KFENCE. LoongArch
  p4d_none()/pud_none()/pmd_none() compare against their respective
  invalid_*_table, not the installed kasan_early_shadow_* table.
  New `*_none()` tests fail for preexisting shared entries, so an
  aligned fast path formerly skipped instead descends down to
  zero_pte_populate(), repeatedly rewriting the shared static PTEs.
  Excessive boot-time page-table work is a proven code consequence;
  exact run time, crash, or early write-protect failure not reproduced.
- R-014/F6 CONFIRMED conditional path: When an aligned early-shadow
  entry lies at an ARCH_PAGE_TABLE_SYNC_MASK level, v2 installs a
  static shared child and marks the level synchronized. During
  kasan_remove_zero_shadow(), new `continue` skips the entry and does
  not clear its valid zero-shadow PTE mapping. A later normal RAM
  online in that shadow range has kasan_mem_notifier() check only
  shadow_mapped(), which returns true for the stale zero PTE, thus
  skipping real writable shadow allocation. This can lead to a KASAN
  fault on access. The exact hotplug/arch configuration and runtime
  reproduction were not established; mapping-retention mechanism is
  source-proven, not merely an empty-table memory leak.
- R-014/F7 DESIGN: Retain parent table storage if another mm might
  reference it, but still remove the logically invalid leaf mapping.
  Shared static tables can alias other virtual ranges, so clearing
  their PTEs blindly is not safe either. A runtime-private table at a
  synchronized level may be appropriate, but replacing a parent
  already copied into other page tables requires architecture-safe
  coordination; do not assert that a simple swap is sufficient.

Disposition: Fix the shared-table classification in aligned paths;
  correct the teardown semantics at synchronized levels; prove
  add/remove/add and boot-time behavior on relevant architectures.
  Stable: candidate for a corrected upstream fix, not v2.
  Impact: hotplug-related shadow faults and possible boot slowdown;
  observed versus potential effects must be distinguished.

Reason previous review failed: assumed !*_none implied a private page
  table that could be descended into, and treated retain-table-pages
  as equivalent to retain-parent-mapping. Focused primarily on x86
  runtime fix rather than all architecture boot states. This is a
  fix-proof and architecture-coverage failure, not a flaw in proving
  the original bug.

Guided pass: Tejun HEAD
  c8cc6a8bee854cf2850f44e0a61be581c19f1d4e; Chris HEAD
  d048f8742f6740c38833adf02e87901412d771ca.
Verification: source review of generic KASAN code, LoongArch
  initialization, *_none() definitions, memory notifier and x86/ARM
  sync-mask semantics; no compilation, live reproduction or model.
Next: send revised reply to author; NOT SENT.

### R-015

Subject: mm/ksm: keep soft-dirty and uffd-wp when merging a page
Original: [PATCH] mm/ksm: keep soft-dirty and uffd-wp when merging
  a page
Author: Samarth Narang <samarth.colleges@gmail.com>
Date: 2026-10-18. Base: 48fe11c8d0f1e4e59426a3606f20ac1130b6d8dc
Fixes: 292924b26024 (UFFD WP), 0f8975ec4db2 (soft dirty),
  763f43865fc4 (UFFD RWP); subjects/SHAs checked in GitHub.
Status: DO NOT MERGE; incomplete soft-dirty fix plus RWP unmerge
  failures; request revised patch and cross-subsystem corrections.
Review 2: 2026-10-18. Source-based re-review against base; no native
  Sashiko runner or Rust compiler in current container and no outbound
  DNS. Manual specialist analyses performed; NOT a native run and NOT
  a claim of matching Sashiko's stochastic findings.

R-015/F1 (VALID, NOT FULLY FIXED): The normal KSM page is built with
  mk_pte(kpage, vma->vm_page_prot). write_protect_page() retains the
  existing soft-dirty/uffd state in orig_pte, and replace_page()
  verifies pte_same() under the page-table lock. Copying these flags
  and restoring PAGE_NONE on an RWP VMA matches analogous PTE rewrites
  in mm/memory.c and mm/migrate.c. The UFFD-WP/RWP logic appears
  locally correct. Downstream KSM unmerging is unsafe for RWP;
  see Sashiko-identified F5 and F6 below.
R-015/F2 (INCOMPLETE FIX; PREEXISTING MECHANISM): When KSM
  use_zero_pages is enabled, replace_page() initializes newpte using
  pte_mkdirty(pte_mkspecial(...)). On x86, pte_mkdirty() sets both
  _PAGE_DIRTY and _PAGE_SOFT_DIRTY. The patch sets soft-dirty when
  orig_pte has it, but never clears the bit that the zero-page path
  set when orig_pte lacks it. Reproducible input state: anonymous
  mergeable zero page whose soft-dirty bit was cleared with
  /proc/PID/clear_refs and which was not subsequently written.
  A KSM zero-page replacement falsely sets pagemap's soft-dirty bit.
  The logic covers all four combinations of zero vs ordinary KSM,
  and orig_pte soft-dirty set vs clear; only zero + clear fails.
  Ask for symmetric set/clear restoration of soft-dirty state, e.g.
  else newpte = pte_clear_soft_dirty(newpte). The accounting sentinel
  uses the distinct dirty/saved-dirty bits and is unaffected.
R-015/F3 (REJECTED HYPOTHESIS): RWP's pte_modify(PAGE_NONE) does not
  lose x86's KSM zero-page dirty accounting marker. On x86,
  pte_mkdirty() moves the hardware dirty bit to SAVED_DIRTY if the
  PTE is read-only; pte_modify() preserves the saved bit on its
  read-only input; pte_dirty() sees both. No reported regression.
R-015/F4 (REJECTED HYPOTHESIS): An RWP protnone PTE is not excluded
  merely for being PROT_NONE: pagewalk's PTE path handles present
  entries and vm_normal_page(). No proven special exclusion from KSM.

Manual Sashiko goal: direct PTE reconstruction is the minimal repair,
  but the intended metadata invariant needs preservation in both
  directions and on both old/new zero-page states.
Manual Sashiko implementation: F2 defeats full stated soft-dirty
  preservation. PTE markers, RWP and the three Fixes subjects align.
Manual Sashiko execution-flow: followed write_protect_page() through
  try_to_merge_one_page() and replace_page() for normal/zero pages,
  mismatch abort, pte_clear_flush and mapped-page replacement.
Manual Sashiko resources/locking: no new ownership or serialization;
  page-table lock, mmap read lock and PTE equality cover the rewrite;
  references, counters and error paths unchanged by added flags.
Manual Sashiko security/hardware: preserving UFFD protection prevents
  losing intended write/access traps. Cross-checked x86/arm64 PTE
  helpers. x86 zero-page soft-dirty set is confirmed; arm64
  pte_mkdirty() does not itself set soft-dirty.
Manual Sashiko verification (previous review): F2 code proof;
  F3/F4 rejected, but inverse-operation KSM unmerging was missed.
  Claims of complete execution-flow coverage were unwarranted.
Tejun/Chris: current SHAs at redo, cbb4478d0f73e15907335e70a2dc2fe54a9e7167
  and d048f8742f6740c38833adf02e87901412d771ca.
Sashiko source: 27815bffd745c1e30e91bdd9d4f197ec7620d204.
  Source prompts fetched from pinned SHA; native run unavailable.
User-visible impact: lost soft-dirty history produces false negatives
  for ordinary KSM; unprotected WP/RWP stops expected userfaultfd
  faults; zero-page path still produces false positive in pagemap.
  RWP unmerge can silently leave KSM pages shared after
  MADV_UNMERGEABLE; asynchronous unmerge can consume RWP state.
Stable: candidate after complete fix; stable tag already present.
Testing: no author test in supplied patch; no real kernel build,
  hardware execution or native Sashiko run. Four-way flag check was
  a source-derived Boolean exercise, not a live-kernel test.
Model: no new multi-actor protocol; page-table lock serializes PTE
  replacement. TLA+ is not relevant to this incomplete state-copy.
Next: request v2 for soft-dirty clear and RWP-aware KSM unmerge,
  including synchronous and asynchronous cases and PTE unshare.
  Require regression testing; email drafted, NOT SENT.


R-015 Sashiko feedback, 2026-10-18:
  External native Sashiko report for commit
  a0c91d60795a1c981863694b2d5797c97c36486f was user-provided.
  Its additional unmerge concerns were independently source-verified.
  This was NOT a native Sashiko execution in our environment.
R-015/F5 (CONFIRMED, synchronous RWP): break_ksm() calls
  handle_mm_fault() with FAULT_FLAG_UNSHARE | FAULT_FLAG_REMOTE but
  without FAULT_FLAG_ALLOW_RETRY. An RWP-armed protnone PTE is
  dispatched by handle_pte_fault() into do_uffd_rwp() *before* the
  UNSHARE flag check. In synchronous mode, handle_userfault() warns
  (with CONFIG_DEBUG_VM) about missing ALLOW_RETRY, and returns
  VM_FAULT_SIGBUS. break_ksm() exits and converts SIGBUS into a
  zero (success) result. __ksm_del_vma() can then clear VM_MERGEABLE
  without unmerging, and the global unmerge can release rmap items.
R-015/F6 (CONFIRMED, asynchronous RWP): do_uffd_rwp() rewrites the
  PTE to VMA protection and clears its UFFD marker during internal
  UNSHARE. break_ksm() can retry and unshare, but RWP tracking was
  consumed without any actual user access. Also, wp_page_copy()
  preserves the uffd bit on its UNSHARE path yet fails to restore
  PAGE_NONE; redirecting the fault to COW alone is not sufficient.
  The paths can also be triggered on already RWP-marked KSM mappings
  without this patch; preserving RWP through KSM merge makes their
  incompatibility directly reachable in the proposed new behavior.
Proposed repair (not code-tested): distinguish internal UNSHARE from
  RWP access before userfault dispatch, ensure real unsharing, and
  restore PAGE_NONE after PTE copy. Carefully preserve NUMA protnone
  handling, existing userfault behaviors and accounting invariants.
Review failure analysis: prior passes traced merge -> replacement, but
  never tested replacement -> MADV_UNMERGEABLE -> internal fault ->
  handler and cleanup. The earlier favorable UFFD verdict was wrong.
  Workflow now mandates inverse-operation and internal-caller audits.
No kernel runtime experiment, compilation, formal model or native
  Sashiko execution was performed for this feedback analysis.


### R-016

Subject: mm/memory-tiers: reset demotion targets of nodes without memory
Original: [PATCH] mm/memory-tiers: reset demotion targets of nodes
  without memory
Author: Gregory Price. Reviewed: 2026-10-19 (America/Los_Angeles).
Full mail/Message-ID: not supplied; original complete changelog and
  author tests not recovered. Diff: one-line `for_each_node_state(node,
  N_MEMORY)` -> `for_each_node(node)` in disable_all_demotion_targets().
Source: torvalds/linux 70dd4ee72eb2d5793c62e71c14e3aba78e5a4e56.
Fixes: 6c542ab75714 (verified introducing commit).
Status: REVIEW COMPLETE for supplied one-line code; NO UNCONDITIONAL
  TAKE until the full posted mail and changelog are checked.
Report: `memory-tiers-review.md` (full 66-rule evidence matrix).

Findings:
- R-016/F1 (source verified): the old reset skips a node immediately
  after its N_MEMORY bit is cleared by last-memory hot-unplug. This
  leaves stale per-node demotion preferred bits.
- R-016/F2 (source verified): changing reset to N_POSSIBLE clears
  memoryless entries. NULL pgdat is guarded; array is sized for
  nr_node_ids, which covers N_POSSIBLE; only actual N_MEMORY nodes
  are rebuilt. No new source-level defect proven.
- R-016/F3 (no observed user effect): all in-tree demotion target
  consumers are in mm/vmscan.c. Actual source folios prevent
  test_pages_isolated() success; re-online rebuilds after setting
  N_MEMORY. Treat as invariant cleanup, not a proven runtime regression.
- R-016/F4 (hard case checked): lower-tier allowed mask and preferred
  target are read in separate RCU sections. The existing non-atomic
  snapshot may change during hotplug, but source folio isolation and
  online/target guards revealed no regression from the new reset.

Verification: source and historical Fixes commit inspected; Python
  finite truth-table: 3900 masks, 2541 old stale-vs-new cases, all
  active-node outcomes unchanged. No real kernel compile/runtime test,
  native Sashiko, TLA+, TLC, tla-mctj or herd7 execution.
SHA pins: Sashiko f6e2e172e1e669b6767a4c74fe91d062b41fd71c;
  Tejun cbb4478d0f73e15907335e70a2dc2fe54a9e7167;
  Chris d048f8742f6740c38833adf02e87901412d771ca.
Model: no - no new multi-actor protocol; manual 3-actor analysis and
  bounded executable mask enumeration suffice for introduced behavior.
Impact-changelog: no known effect for in-tree users, substantiated;
  original complete mail not available, so cannot confirm wording.
Stable: not justified - no demonstrated user benefit/test data.
Standing rules: 63 of 66 applied; 2 inapplicable; 1 unresolved.
  Unresolved: original mail/changelog/replies/tests not recovered.
Next: obtain full original mail and audit claimed testing, then decide
  final unconditional take. LKML-ready reply drafted, NOT SENT.

### R-017

Subject: fs/proc/task_mmu: pin mm_users in do_pagemap_scan()
Original: [PATCH] fs/proc/task_mmu: pin mm_users in do_pagemap_scan()
Author: Ngoc Quy <ngocquy0700@gmail.com>. Date: 2026-10-14.
Base: 24a19b953e2a3d0ea5a8c4951a0ab8f32720c907 (Linux 7.3-rc7).
Source preimage: fs/proc/task_mmu.c blob
  5c54aebe211824681a5c30e03464af51697b11ce.
Fixes: 52526ca7fdb905a768a93f8faa418e9b988fc34b (verified).
Status: CORE FIX SOUND; `!mm` masks impossible-state Oops; missed
  in initial review. Remove guard; request impact and testing.
Report: `task-mmu-review.md` (74-rule evidence matrix).
Model: `task-mmu-mmusers-model.py` (executed Python checker).

Findings:
- R-017/F1 (source proof): proc_mem_open() pins mm_count, not
  mm_users; exiting task may enter exit_mmap() under mmap_read_lock()
  while PAGEMAP_SCAN also holds the read lock. unmap_vmas() invokes
  hugetlb_zap_end(ZAP_FLAG_UNMAP); the VMA-specific rwsem can be freed
  after a walker cached its address but before down_read(), yielding
  a reachable UAF. An empty hugepage pool does not prevent the path
  with a shared MAP_HUGETLB | MAP_NORESERVE mapping. User-side read
  permission for target pagemap is still required.
- R-017/F2 (fix proof): mmget_not_zero() at ioctl entry blocks the
  final mmput() until all walks, copies and cleanup finish; every
  new error goto releases the reference, and zero mm_users yields
  -ESRCH. No code regression established on examined paths.
- R-017/F3 (dismissals): Ordinary munmap() detaches VMAs before its
  optional mmap_lock downgrade; exit_mmap() still exposes them
  during the read-locked unmap. Clearing vm_private_data is not
  protection against cached pointers; acquiring a hugetlb rwsem is
  not an independent kref.
- R-017/F4 (changelog): source-supported possible kernel crash or
  corruption should lead the changelog. No live symptom, KASAN log
  or before/after kernel test was supplied or independently run.

- R-017/F6 (post-review correction, 2026-10-19): User challenged
  failure to flag newly added `!mm`. Verified `pagemap_open()` rejects
  NULL from `proc_mem_open()`. On success, `file->private_data`
  cannot be NULL at `do_pagemap_cmd()`. No other caller or setter of the
  ioctl private_data was established. Hence `!mm` is unreachable
  on this path and redundant, although `mmget_not_zero(mm)` IS
  necessary when mm_users hits zero. Proposed removal: use
  `if (!mmget_not_zero(mm))`. The initial "no code change" verdict
  was mistaken: the review followed the UAF but skipped a necessity
  test for this guard. The new mandatory gate requires a per-clause
  witness and explicit reachability/necessity conclusion. The
  follow-up audited four added/behavior-changed decisions:
  4 of 4 checked; 1 redundant; 0 unresolved. This is retrospective,
  NOT proof that the original 74-rule review executed the new gate.
- R-017/F7 (user diagnostic-contract clarification, 2026-10-19):
  The objection to `!mm` is not merely redundant defensive coding.
  A NULL `mm` would violate the guaranteed open/ioctl call chain.
  Before the patch, such a programming error would Oops and demand
  investigation. The new `!mm` turns it into quiet `-ESRCH`, hiding
  a possible kernel defect. AKPM has already challenged the author
  on this exact point. Remove `!mm` to preserve the existing
  diagnostic behavior; do not add BUG_ON solely for this purpose.
  General rule: every changed guard needs an old/new diagnostic
  behavior check, distinguishing impossible internal invariant
  violations from expected runtime or userspace failures.
  Retrospective diagnostic audit: 4/4; G01 masks prior Oops, G02
  converts reachable mm_users-zero race to ESRCH, G03/G04 retain
  their original error codes while releasing the added reference.
- R-017/F5 (native formal): PlusCal source was translated and parsed;
  TLC and tla-mctj independently find a concrete UAF in the unpinned
  model and no failure in the pinned two-scanner/one-exit model.
  Separately tested pointer-check/load NULL race; original fails.
  No kernel runtime/sanitizer experiment was run.

Execution: Python 3 bounded scheduler with two scanners and one
  exiting task: old 902 states, 2134 transitions, unsafe; patched
  187 states, 380 transitions, no unsafe states under abstraction.
  Native PlusCal -> SANY -> TLC and tla-mctj ran on 2026-10-19.
  Old protocol violated NoUAF and NoNull in both model checkers:
  mctj old/UAF 545* distinct states, depth 13; TLC 522*, depth 14;
  mctj old/NULL 270*, depth 10; TLC 244*, depth 11.
  *Counterexample found before complete enumeration of old graph.
  Patched: 504 distinct states, depth 32, no invariant failures in
  BOTH checkers. SC abstraction; not a kernel runtime test/LKMM proof.
  TLC 2026.10.15.145915; tla-mctj 0.1.2. See task-mmu-review.md
  and task_mmu_mmusers.tla plus three canonical .cfg instances.
Guidance checked 2026-10-19: Sashiko
  f6e2e172e1e669b6767a4c74fe91d062b41fd71c; Tejun
  cbb4478d0f73e15907335e70a2dc2fe54a9e7167; Chris
  d048f8742f6740c38833adf02e87901412d771ca. Independent and
  full applicable manual stage analysis performed, no native Sashiko.
Impact-changelog: needs explicit user-facing harm and test evidence.
Stable: prospective candidate after mainline and actual testing;
  introducing commit is included from v6.7, not v6.6.
Standing rules: 72 of 74 applied; 1 inapplicable; 1 unresolved.
  Unresolved: native Sashiko not run (A47). Native model covered A57.
  Not applicable: no new weak-memory protocol/herd7 (A58).
Next: await Ngoc's answer to AKPM's `!mm` diagnostic objection;
  request explicit user impact and before/after KASAN testing.
  Corrected LKML draft in report;
  it has NOT been sent. No Reviewed-by provided.

## Maintenance reminder

When feedback arrives, update findings and dispositions here. Archive
resolved OR dormant reviews into that day's
`review-activity-YYYY-MM-DD.md`, leaving the normalized Subject and
filename above. Keep this file lean; retain durable lessons in the
AKPM workflow only when broadly applicable.
