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
  ACTIVE: [R-006](#r-006); v2 resolves v1 issue; no new defect.
- `proc/kcore: advance the vmalloc retry by the last copy, not the total`
  ACTIVE: [R-007](#r-007); v1 source-reviewed, no defect found.
- `mm/mremap: do not charge a shrinking move twice`
  ACTIVE: [R-008](#r-008); v1 code sound, changelog needs correction.
- `ucount: take the rlimit reference before checking the limit`
  ACTIVE: [R-009](#r-009); v1 source-reviewed, code sound.
- `lib/buildid: reject file offsets that do not fit in pgoff_t`
  ACTIVE: [R-010](#r-010); v1 sound, security coordination pending.
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
Status: v2 source-reviewed, no additional change requested. PENDING
  maintainer feedback; author tests not independently reproduced.

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
Next: take v2 as submitted; await feedback. Preserve the general
  lesson of verifying iterator endpoint conventions against source.


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

## Maintenance reminder

When feedback arrives, update findings and dispositions here. Archive
resolved OR dormant reviews into that day's
`review-activity-YYYY-MM-DD.md`, leaving the normalized Subject and
filename above. Keep this file lean; retain durable lessons in the
AKPM workflow only when broadly applicable.
