# Review activity - AKPM

Last updated: 2026-10-16 (America/Los_Angeles)
Scope: working ledger plus Subject-to-location index, NOT review method.
Method: `akpm-patch-review-workflow.md` (invokes the unchanged
`tj-patch-review-workflow.md`).

This ledger was seeded from recent review discussions. It records our
current understanding, NOT author acceptance. Messages, tests and later
feedback not yet supplied are not presumed to exist. Keep each record
short; detailed mail and diffs are retrieved by reference as needed.

## Chris Mason prompt tracking

Repository: https://github.com/masoncl/review-prompts
Upstream branch: `main`
Last checked: 2026-10-16 (America/Los_Angeles)
Checked HEAD: `d048f8742f6740c38833adf02e87901412d771ca`
HEAD commit date: 2026-10-01 11:53:46 UTC
HEAD subject: README: add pahole to the project lists
Status: initial version-tracking checkpoint; no previous pinned SHA.

Recent upstream improvements already in this baseline:
- 2026-09-21 `2e5e252bfe56`: MM race refcount budgeting.
- 2026-09-21 `a39be13ca052`: avoid a `virt_to_page()` false positive.
- 2026-09-23 `f85b3a017072`: guides and false-positive updates.
- 2026-10-01 `1a1befd0c56f`: correct guide rules contradicted by code.
These are examples, not every upstream change or independent proof of
improved review accuracy.

For each new Tejun-guided review, record the FULL Chris prompt SHA and
fetch/check date in that review's active entry. Check HEAD each review,
but analyze substantive upstream prompt diffs at most weekly while
actively reviewing (or earlier if relevant to a particular finding).
Keep only the latest checkpoint and generalizable change notes.
The earlier reviews R-001 through R-005 have no recorded prompt pin:
DO NOT infer they used the HEAD recorded above.

## Upstream Sashiko tracking (weekly, not per patch)

Repository: https://github.com/sashiko-dev/sashiko
Reference branch: `main`
Last examined: 2026-10-16 (America/Los_Angeles)
Examined commit: `f4b72fa04f232fe5f2183d32d7cf9c09e5d735ec`
Chris reference: `d048f8742f6740c38833adf02e87901412d771ca`
Observations: Sashiko's vendored `mm-reclaim`, `mm-folio`,
`mm-pagetable`, `mm-largepage` and `locking` guides match Chris at
that reference. Sashiko-specific `mm-vma` and false-positive rules
contain additional material which requires independent validation.
Its separate `concerns`/`dismissed_concerns`/`hard_cases` processing
suggests a targeted disagreement check, not importing its pipeline.
Next substantive comparison: after 2026-10-23 PT (while active), or
when the user requests it. HEAD may be checked more cheaply.

## Public mailing-list follow-up tracking

Monitoring: weekly Monday mornings (America/Los_Angeles), beginning
2026-10-19; scheduled task active. When author feedback is supplied
in chat, review it immediately instead of waiting for Monday.
Purpose: identify WHY a finding was right, wrong or incomplete, and
produce broadly applicable review rules -- not merely count replies.

Last full Lore batch: NOT YET RUN. This ledger is not a live feed.
Monitoring source: ACTIVE records below only. Exact Message-IDs and
sent-review IDs are preferred. No initial thread-wide last-seen cursor
has been verified. On each successful check, record the check date,
new reply IDs and per-finding disposition; preserve unverified states.
A future scheduled check may not see changes made only in a private
local Git tree: provide an accessible current ledger or an exact
read-only repository path when needed. Never infer missing replies.

Review-specific status:
- R-001: original Message-ID unknown; fallback to exact Subject.
  Last checked: not yet. Our sent-reply ID: unknown.
- R-002: original Message-ID unknown; fallback to exact Subject.
  Known author reply: 2026-10-16 PT, already summarized below.
  Last public-thread check: not yet. Our sent-reply ID: unknown.
- R-003: original Message-ID unknown; fallback to exact Subject.
  Last checked: not yet. Our sent-reply ID: unknown.
- R-004: original Message-ID recorded in R-004; last checked: not yet.
  Our sent-reply ID: unknown.
- R-005: original Message-ID and whether draft was sent are unknown.
  Do not treat it as an active publicly posted review until verified.

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
Author: Siddharth Chintamaneni. Version: [PATCH v1], 2026-10-17 UTC.
Status: AUTHOR REPLIED 2026-10-16 PT; proposal assessed, awaiting v2.
Fixes: `e4dde56cd208` (per-node MGLRU memcg lists).

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
  Keep the original `lru_gen_shrink_node()` fix too. No revised patch
  or runtime verification supplied yet.
Next: inspect the author's v2 and any tests, then resolve F2.
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

## Maintenance reminder

When feedback arrives, update findings and dispositions here. Archive
resolved OR dormant reviews into that day's
`review-activity-YYYY-MM-DD.md`, leaving the normalized Subject and
filename above. Keep this file lean; retain durable lessons in the
AKPM workflow only when broadly applicable.
