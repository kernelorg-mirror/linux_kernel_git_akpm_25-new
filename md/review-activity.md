# Review activity - AKPM

Last updated: 2026-10-26 (PDT)
Latest numbered review: R-042 (memfd F_SEAL_PUNCH_HOLE series).
R-034 through R-042 remain HOLD; see their individual records.
Numbering follows documentation catch-up, not original patch posting order.
Scope: working ledger plus Subject-to-location index, NOT review method.
Method: `akpm-patch-review-workflow.md` (invokes pinned upstream Tejun
modules; the old standalone S2 file is historical only).

This ledger was seeded from recent review discussions. It records our
current understanding, NOT author acceptance. Messages, tests and later
feedback not yet supplied are not presumed to exist. Keep each record
short; detailed mail and diffs are retrieved by reference as needed.

## Work startup verification (2026-10-24 PDT)

This is environment and continuity restoration, not a new patch review.
The supplied October 25 02:44 UTC ledger stopped at R-036 despite the
handoff naming R-037. Its earlier history is preserved. The surviving
master differed only by its R-037 header and appended R-037/filemap
records. Those records were recovered and checked against the current
saved fat-write-failed-review.md and filemap-invalidate-errors-review.md.
R-034, R-035, R-036 and R-037 remain HOLD. The filemap investigation is
unnumbered; no submitted fix, acceptance or Btrfs corruption reproduction.

The workflow's missing body-only-hunk and explicit-search-root lessons
were restored from the surviving master. Its active handoff now spells
pull-summary.md correctly. No other methodology or disposition changed.

Executed in Work, 2026-10-24 19:45-19:51 PDT (October 25 UTC):
- Existing bare clone survives at
  /workspace/scratch/2787927c495b/mm.git.
- HTTPS fetch of all Google MM heads and tags succeeded. The selected
  MM tips matched public kernel.org before and after the fetch.
- Linus's actual master was fetched from torvalds/linux at kernel.org;
  remote HEAD explicitly names refs/heads/master.
- Bare=true, shallow=false; no partial-clone/promisor configuration.
  git fsck --connectivity-only --no-dangling exited 0 without diagnostics.
  This is connectivity verification, not full content-hash verification.
- No authenticated Gitolite access was established or implied.

Fetched pins, checked at 2026-10-25 02:45:49..59 UTC:
- mm-unstable: a2abad0d7f453cc9902fc8bf7b871db5563a652c
  Committer: 2026-10-24 15:48:02 -0700. Age about four hours; no
  24-hour freshness alert. Recheck before the next substantive review.
- mm-stable: 183895979c441e52dbd651b388553b09eaa35cfa
  Committer: 2026-10-24 01:56:43 -0700.
- mm-nonmm-stable: b6232ca8d194c60ee603586e42b5ea584d4b7be9
  Committer: 2026-10-24 00:46:53 -0700.
- mm-hotfixes-stable: 80ce29104123be4d61b5912dae543c70af0fcb75
  Committer: 2026-10-06 16:44:19 -0700.
- torvalds/linux master: 330517c63aa9b48227b6ab45f01003effac77ae4
  Committer: 2026-10-24 15:44:26 -1000 (18:44:26 PDT).

Fresh default-branch checks/fetches at 02:48:20..46 UTC:
- Sashiko: d7c69ae77326a3ef39362897cdf0751a06068cf1
  Committer: 2026-10-23 13:38:00 -0700.
- Tejun: cbb4478d0f73e15907335e70a2dc2fe54a9e7167
  Committer: 2026-10-17 20:22:24 -1000.
- Chris: d048f8742f6740c38833adf02e87901412d771ca
  Committer: 2026-10-01 11:53:46 UTC.
All match the latest prior review pins. This verifies availability and
identity, not completion of the applicable methods for a new patch.

Tool validation:
- git 2.51.1, Python 3, OpenJDK 17.0.20, GCC and make are available.
- The supplied gate executes its CLI. It is byte-identical to R-037's
  archived script. No new patch manifest was invented for this startup.
- Restored TLC 2026.10.15.145915 (rev 932d35e) and tla-mctj 0.1.2.
  PlusCal translation and SANY parsing ran successfully on a disposable
  copy of R-037's existing model. Both checkers reproduced the expected
  old N=3/Keep=1 violation (298 distinct states, exit 12) and patched
  N=5/Keep=1 success (1077 states, depth 50, exit 0). This checks the
  tools and historical model; it does not close R-037's validation gaps.
- Native Sashiko and herd7 are unavailable. No native Sashiko, LKMM,
  kernel build, VM boot, runtime filesystem or hardware test ran here.
  flex, bison, bc, pkg-config, Clang and QEMU are absent from PATH.
- R-037's original manifest, final manifest, failed receipts and old
  gate result were recovered without rewriting their contents or paths.
  Its body-only limitation remains. The old acceptance gate was not
  rerun or presented as passing.

Current tool directory:
/workspace/scratch/08622c88e80d/formal-tools/
Startup logs and separate checker runs:
/workspace/scratch/08622c88e80d/startup-evidence/
These scratch paths are session-specific, not durable guarantees.
The original R-037 evidence archive and saved reports remain the
historical record. No kernel source edit, push, tag or mail send.

## Review-gate v2 implementation checkpoint (process only)

Date: 2026-10-23 PT. This is a review-workflow change, NOT a new patch
review ID. The R-001..R-034 findings and dispositions remain unchanged.
R-034 remains HOLD because of the confirmed LP64 KVM build regression.

Files: `akpm-review-gate.py` (v2), `test_akpm_review_gate.py`,
`akpm-review-gate-README.txt`; these accompany the updated
`akpm-patch-review-workflow.md`. For each NEW review, ChatGPT should run
`new` before source analysis and `check` before any acceptance verdict;
use a review-specific JSON manifest and retain its evidence receipts.
A missing manifest, missing mandatory evidence, changed patch/workflow,
failed required command, or unresolved mandatory requirement means HOLD.
Do not fabricate retroactive preflight on an older review.

The new deterministic preflight parses patch paths/hunks and shared ABI
triggers, freezes the source SHA and workflow checksum, and records
section/hunk obligations. Command receipts are purpose-checked and
source-tree searches must match the preflight SHA; generic commands do
not satisfy source searches or builds. Shared API/ABI changes require
whole-tree caller checks, an out-of-subsystem build, and both LP64 and
ILP32 evidence. A separate same-model adversarial report is allowed but
must not be misdescribed as an externally independent review.

Executed: nine automated gate regression tests passed, including R-034
shared-library trigger discovery and a real failing GCC LP64 typedef
probe (the gate returned HOLD), missing evidence, modified requirement
inventory, forged unrelated command, wrong section evidence, and a
synthetic positive receipt case that reverted to HOLD on altered proof.
No kernel build or full KVM selftest was executed by these gate tests.

Limitation: the script can validate receipts, required categories and
command metadata; it cannot establish the substantive completeness of
an entire kernel source review, guarantee it was invoked in every chat,
or independently control ChatGPT's wording. Its positive output means
structurally ELIGIBLE_FOR_HUMAN_DECISION, never an automatic take. The
full rule-by-rule source-grounded inventory remains required in addition
to the script's 24 coarse workflow-section checks.

## Work Git-access checkpoint (2026-10-24; historical)

Authoritative procedure: `kernel-git-access.md`. A separate Work session
executed a full non-shallow Google `akpm/mm` bare clone (3.32 GiB),
fetched Linus's actual master over HTTPS from kernel.org, and confirmed
Google's `mm-stable` and `mm-unstable` SHA equality with public
kernel.org. The previous Work scratch clone was at
`/workspace/scratch/91741514aa81/mm.git`; this is a SESSION-SPECIFIC
path, NOT a guaranteed checkout for the next chat.

- `mm-unstable`: `d10295141a98938a767234e73d45b954a69c9a2f`,
  committer 2026-10-24 02:05:50 PDT.
- `mm-stable`: `183895979c441e52dbd651b388553b09eaa35cfa`,
  committer 2026-10-24 01:56:43 PDT.
- Linus `master`: `5b0764a53235d3c77e1ed674e836e1b3fe1a4b1f`,
  committer 2026-10-23 21:29:02 PDT.
- Exact complete ancestry `mm-stable...linus/master`: 213 MM-only
  commits and 12,447 mainline-only commits at these checkpoint tips.
  This is reachability, not patch-equivalence or an integration verdict.
- Authenticated Gitolite SSH access was NOT obtained: name lookup for
  `gitolite.kernel.org` failed. Do not promote public kernel.org ref
  agreement into authenticated authoritative verification.
- No builds, native Sashiko runs, kernel runtime tests or VM tests were
  performed during the Git-access task.

Use these as dated verification checkpoints, not live branch tips. On
entering a new Work chat, test network and scratch persistence, refresh
both Git remotes, pin exact SHAs, validate commit/tree connectivity and
patch preimages, and rerun freshness checks before each review. The
October 23 source-inspection checkpoint below is older and superseded
for the HEAD values, but remains relevant to reviews performed then.

## Earlier Google mirror checkpoint (2026-10-23; historical)

Mirror: https://kernel.googlesource.com/pub/scm/linux/kernel/git/akpm/mm/
Policy: default review base is `mm-unstable` unless explicitly overridden;
verify the relevant revision and patch context for each review. Inspect
freshness at every mirror use; alert AKPM if `mm-unstable` HEAD's
committer time is more than 24 hours old. Mirror activity alone does not
prove gitolite synchronization.

Checked: 2026-10-23 10:54 PDT (17:54 UTC), via Google Gitiles.
`mm-unstable` HEAD: 2bba28e98578de622ef307d00875aa8f8bca3d10
Committer: 2026-10-22 22:13:38 PDT. Age at check: about 12h 41m.
`mm-new` HEAD: 3fdcce698abd9193752ee89fb1a440cdceb1b74a
Committer: 2026-10-22 22:13:42 PDT. Age at check: about 12h 41m.
Freshness alert: NO - less than 24 hours old at this check.
Comparison: current mirror `mm-unstable` HEAD matches R-030's explicit
base commit. No current gitolite-versus-mirror hash comparison was made.
Historical user-verified gitolite/Google `mm-new` equality:
fcec4f4bcc1101dbd7e3aff267856b3bbfe128c6 (historical only).

## Upstream prompt HEAD recheck for Work handoff (2026-10-24)

Checked public GitHub `main` ref identities from this chat:

- Sashiko: `d7c69ae77326a3ef39362897cdf0751a06068cf1`.
- Tejun: `cbb4478d0f73e15907335e70a2dc2fe54a9e7167`.
- Chris Mason: `d048f8742f6740c38833adf02e87901412d771ca`.

These are ref identities, not evidence that native analysis ran. The
full Sashiko stage/prompt changes since the earlier recorded 867713...
checkpoint were NOT compared in this handoff; the new Work chat must
check changes before applying the current version. Historical sections
below retain the earlier version-comparison provenance.

## Tejun upstream workflow checkpoint

Repository: https://github.com/htejun/kernel-agent-workflows
Upstream branch: `main`
Last checked: 2026-10-22 (America/Los_Angeles)
Checked HEAD: `cbb4478d0f73e15907335e70a2dc2fe54a9e7167`
Previous HEAD: `c8cc6a8bee854cf2850f44e0a61be581c19f1d4e`
Change: `$MODEL_CHECKER` introduced in `UPGRADING.md`; default
`tla-mctj`. Other relevant module changes: formal-model guidance.
HEAD commit date: 2026-10-18 06:22:24 UTC
HEAD subject: Merge pull request #1 from htejun/overlay-flush
Last comparison: 2026-10-19 (America/Los_Angeles)
Status: fresh HEAD check unchanged during R-029 feedback verification.
The previously recorded comparison with c8cc6a8 remains historical.
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
Last checked: 2026-10-22 (America/Los_Angeles)
Checked HEAD: `d048f8742f6740c38833adf02e87901412d771ca`
HEAD commit date: 2026-10-01 11:53:46 UTC
HEAD subject: README: add pahole to the project lists
Status: unchanged from previous verified prompt baseline.
Last comparison: 2026-10-22 (America/Los_Angeles)
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
Last checked: 2026-10-23 (America/Los_Angeles)
Checked HEAD: `867713d1c5e0005d04ea71c6691f39c8a69384a9`
Previous checkpoint: `8a8cd0aafa00a3c5cf59a36d0d020efdf7d9df8c`
HEAD commit date: 2026-10-23 15:59:07 UTC
HEAD subject: release: bump version to 0.6.3
Last comparison: 2026-10-23 (America/Los_Angeles)
Comparison: 7 intervening commits change provider/runtime budgeting,
  storage/compression and release metadata. None changes the kernel
  review-stage definitions or vendored kernel MM prompts.
The preceding 8a8cd0... checkpoint introduced explicit tracking of
  pre-existing bugs already triggerable at the baseline, even when
  a patch edits their function. The existing AKPM baseline policy
  already requires that distinction, so no duplicate rule was added.
Manual GOAL/IMPLEMENTATION/EXECUTION/RESOURCES/LOCKING/SECURITY/HARDWARE
  coverage attempted for R-030; native Sashiko not run. Full dynamic
  stage selection and every triggered vendored guide not certified.
Earlier checkpoint 026195ab58e2099e81017adbc6b97f33c509c8ba and its
  historical R-018 assessment remain recorded in the case history.

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
  ACTIVE: [R-015](#r-015); zero-page objection withdrawn; v3 split.
- `mm/ksm: keep soft-dirty when merging a page` (v3)
  HOLD: [R-035](#r-035); source-favorable, gate preflight invalid;
  follow-up to R-015.
- `kasan: fix runtime shadow page table synchronization`
  ACTIVE: [R-014](#r-014); v2 must be revised; shared-table bugs.
- `mm/memory-tiers: reset demotion targets of nodes without memory`
  ACTIVE: [R-016](#r-016); one-line code appears sound; original
  mail/changelog unavailable, so unconditional acceptance withheld.
- `fs/proc/task_mmu: pin mm_users in do_pagemap_scan()`
  ACTIVE: [R-017](#r-017); fix sound; `!mm` masks Oops; tests needed.
- `mm/hugetlb_cgroup: prevent use-after-free during cgroup offlining`
  ACTIVE: [R-018](#r-018); lifetime fix sound; one redundant guard.
- `mm/memcontrol: publish null pointer before dropping css reference`
  ACTIVE: [R-019](#r-019); partial review, GCC-built stress tool;
  exact source and kernel/formal testing unresolved.
- `mm: retry page faults once under the per-VMA lock`
  STUDY: [L-001](#l-001); lessons integrated, no patch verdict.
- `mm: various (urgent?) fixes`
  DORMANT: A-001 in
  [review-activity-2026-10-16.md](review-activity-2026-10-16.md#a-001).
  A dormant review is not author-accepted or author-rejected.
- `lib/firmware_table: validate subtable bounds`
  ACTIVE: [R-023](#r-023); v2 admits terminal headers that can trigger
  out-of-bounds reads in PRMT/CEDT handlers; request revision.
- `delayacct: Preserve delay extrema when aggregating taskstats`
  ACTIVE: [R-024](#r-024); source-reviewed, no code blocker; runtime
  testing and full external-review stages outstanding.
- `compat: Avoid double rounding in times()`
  ACTIVE: [R-020](#r-020); source fix sound; kernel test pending.


- `mm/vmalloc: reject overflowing vm_map_ram page counts`
  ACTIVE: [R-026](#r-026); correct overflow fix, Clang W=1
  warning warrants small revision.
- `mm/page_alloc: mark pages freed by __free_pages_core() as not tagged`
  FOLLOW-UP: [R-021](#r-021); v2 fixes v1 head/tail issue;
  only Fixes-tag check completed here.
- `mm/hugetlb: charge hugetlb cgroup and memcg in alloc_hugetlb_folio_reserve()`
  ACTIVE: [R-025](#r-025); charging correct, cross-patch CSS lifetime
  dependency and historical Fixes correction.
- `mm/zswap: validate dlen and normalize comp_ret on compression success`
  ACTIVE: [R-027](#r-027); accounting fix sound, HiSilicon warning
  behavior needs targeted check.
- `mm/hugetlb: disable PMD sharing for UFFD missing mode`
  ACTIVE: [R-028](#r-028); poison marker may be shared after UFFD
  unregister; source-supported follow-up concern.
- `mm/migrate: snapshot the source nid before the misplaced migration`
  ACTIVE: [R-029](#r-029); fix sound; hot-removal source-metadata
  lifetime race supported by inspected paths, not reproduced.

- `mm/vma: fix expansion of VMA_MIXEDMAP_BIT VMAs`
  ACTIVE: [R-030](#r-030); fix source-favorable, impact prose requested.

- `mm: avoid losing atomic VMA flags`
  ACTIVE: [R-031](#r-031); four-patch series, source and race review.
- `mm/memcontrol: improve lruvec cacheline locality`
  ACTIVE: [R-032](#r-032); performance review and dependency gaps.
- `mm/memcontrol: prevent high_work on dying memcg`
  ACTIVE: [R-033](#r-033); source-supported CSS lifetime correction.
- `selftests/cgroup: convert cg_read_key_*() helpers to s64`
  HOLD: [R-034](#r-034); LP64 KVM typedef/build blocker and incomplete
  freezer conversions; prior acceptance recommendation withdrawn.
- `lib/group_cpus: snapshot cluster masks to keep grouping hotplug invariant`
  HOLD: [R-036](#r-036); counterexamples for the stated invariance;
  actual kernel/NVMe reproducer outstanding.

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

R-009 v2 reassessment (2026-10-21): Nickolai Zeldovich's
[PATCH v2] uses base c03c1a14507dfaf8b856c2608f9ac216021fc222;
verified kernel/ucount.c preimage ec8b1445e287. The new == 1
get_ucounts() occurs before the limit check. The reject path passes
iter->ns->ucounts as the exclusive end to
 do_dec_rlimit_put_ucounts(), correctly including the rejecting level.
The get_ucounts() failure path still decrements iter without a put
and unwinds only preceding levels. No new reference imbalance found in
these source paths. Author reports x86-64 QEMU/KASAN/rcuref forced
interleaving: ~80000 original attempts with an imbalanced-put warning;
~82000 patched attempts without warning or KASAN report. This is
AUTHOR-REPORTED, not independently run. Alexey Gladkov Acked-by.
Prospective stable candidate; target branches and runtime tests not
independently checked. Native Sashiko/full methodology not executed.

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
Current status (2026-10-21): No zero-page objection to soft-dirty-only
  v3. The exact-preservation/else request is WITHDRAWN following David's
  explicit assessment of accepted over-indication. UFFD/RWP remains a
  separate follow-up owned by Lance. Full independent audit is incomplete.
Historical pre-v3 status: DO NOT MERGE the combined patch pending RWP
  unmerge corrections. Earlier zero-page blocker was overstated.
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
R-015/F2 (HISTORICAL OBJECTION; WITHDRAWN AS CORRECTNESS BLOCKER): When KSM
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
Historical next action: request v2 for soft-dirty clear and RWP-aware
  KSM unmerge,
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



R-015 v3 recheck (2026-10-21), Samarth Narang:
- Subject: [PATCH v3] mm/ksm: keep soft-dirty when merging a page.
  Base fcec4f4bcc1101dbd7e3aff267856b3bbfe128c6;
  mm/ksm.c preimage dbfb8f98b18925c729d0931760a18f491d0fb156.
- R-015/F2: the zero-page false positive is PRE-EXISTING, unchanged by
  v3. Earlier chat called it a new regression and demanded v4. That
  classification and blanket merge objection were incorrect. V3 repairs
  the distinct ordinary-page false negative; no new zero-page harm is
  established. A separate false-positive fix is a valid option.
- Suggested else pte_clear_soft_dirty(newpte) remains source-supported:
  x86 clears only bit 11, preserving dirty/saved-dirty, special and PFN.
  is_ksm_zero_pte() uses PFN plus pte_dirty(), not soft-dirty. Existing
  remove_migration_pte() uses set/clear after pte_mkdirty() too.
- Reachable case: write an anonymous private page with zeros, clear its
  soft-dirty state via clear_refs=4, then allow KSM zero-page merging
  without another write. A read-faulted shared zero page is not the test.
  KSM mmap read lock excludes clear_refs mmap write lock; pte_same under
  PTL checks the captured PTE. A later real COW write marks soft-dirty.
- Executed GCC and Clang/UBSan userspace bit-model checks: 1,024 cases
  each. Baseline FP=128/FN=128; v3 FP=128/FN=0; suggested FP=0/FN=0.
  Models both x86 saved-dirty encodings and soft-dirty on/off. Not a
  kernel build, i386 execution, KSM runtime, or TLA+/LKMM verification.
- Stable: original false-negative repair remains a prospective
  candidate; target-branch and runtime verification are outstanding.
  No new corruption/crash follows from the zero-page false positive.
- Next: send the corrected, non-regression wording; suggest adding the
  else or addressing the existing false positive separately. Do not
  withhold v3 solely on the mistaken regression claim. Full guided
  audit remains incomplete; no unconditional Reviewed-by.
  Details: /Kernel Patch Reviews/reports/ksm-soft-dirty-review.md.


R-015 thread reconciliation (2026-10-21), grabbed(3):
- Sashiko <sashiko-outbox-177114@kernel.org> raised the exact zero-page
  soft-dirty question. David's October 19 reply
  <efa6a28c-f0f9-4d1e-9cce-fec2c08e7d9f@kernel.org> explicitly says
  over-indicating soft-dirty is generally not a problem. Lance agrees.
- Our earlier advice did NOT incorporate that assessment. The bit-level
  observation stands, but exact equality was an unproved stronger
  requirement. Withdraw the request for else/v4 on correctness grounds.
- Lance requests soft-dirty-only v3 and takes UFFD-WP/RWP separately;
  Samarth complies. No new formal approval or v3 test is inferred.
- Mohammed reports 8/8 before/after tests across two boots for Lance's
  unshare fix, including a read RWP fault afterward. This is third-party
  evidence about the separate UFFD path, not testing of the proposed else.
- Next: do not send the old zero-page objection. No zero-page reason to
  block v3; keep UFFD/RWP follow-up separate. No new tests run here.
- Detailed report updated in /Kernel Patch Reviews/reports/:
  ksm-soft-dirty-review.md. Workflow now distinguishes conservative
  metadata contracts from exact-preservation model properties.

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

### R-018

Subject: mm/hugetlb_cgroup: prevent use-after-free during cgroup offlining
Original: [PATCH] mm/hugetlb_cgroup: prevent use-after-free during
  cgroup offlining
Author: Daehyeon Ko <4ncienth@gmail.com>. Date: 2026-10-20.
Matching source: AKPM mm-stable, mm/hugetlb_cgroup.c blob
  3fb41311e4c7dcbbd26f7b230ebb1f8c7ce310fe.
Fixes: da1def55919f4852c4759249a78d63a0c5d2d8f9 (2012-08-01).
Status: CORE LIFETIME FIX SOUND; ONE NEW REDUNDANT GUARD.
Report: `hugetlb-cgroup-review.md` (75-rule audit).
Native model: `hugetlb-cgroup-formal-model.tar.gz`.

Findings:
- R-018/F1 (CONFIRMED original UAF): css_tryget() protects selected
  hugetlb CSS during charge but the original normal path drops the ref
  before folio commit. css_offline() scans active folios under the
  hugetlb_lock and can finish BEFORE charge becomes visible. Commit
  can then publish a pointer to a freed CSS, causing UAF in later
  folio uncharge. Author reports 3/3 boots reproduced by KASAN.
- R-018/F2 (source fix proof): Retained charge CSS ref spans buddy
  allocator lock drop and commit/rollback; dying ancestor local
  counters are canceled, retaining the already-charged ancestor
  counts. Selected live CSS gets the folio and per-node usage under
  hugetlb_lock; the active scan and commit serialize. Existing
  reservation CSS ownership remains unchanged. Separately checked
  hugetlb_reserve_pages() reservation CSS transfers to resv_map
  and region_add(), plus its partial/full rollback css_put().
- R-018/F3 (GUARD REDUNDANCY): The new
  `if (!hugetlb_cgroup_disabled())` in uncharge after `if (!h_cg)`
  is unneeded. Successful non-NULL h_cg implies enabled controller;
  cgroup_disable() is a boot-time static-key setup. Remove guard and
  call page_counter_uncharge() unconditionally for non-NULL h_cg.
  G02's disabled check in commit is also redundant in the valid call
  chain, but it is preexisting, not introduced by this patch.
  Guard audit: 11 of 11 checked; 2 redundant (1 preexisting),
  0 unresolved. No new Oops-to-quiet-errno masking found.
- R-018/F4 (DISMISSED): No new ancestor charge needed: page_counter
  already charges parents. No per-node transfer of an uncommitted
  charge: usage first increments at commit on chosen live owner.
  Root CSS is immortal; parent CSS protected by child CSS references.
- R-018/F5 (native model): PlusCal -> SANY; TLC and tla-mctj old
  protocol fail NoDeadCharge and NoDangling; patched 1,512 distinct
  states, depth 31, no invariant violation in either checker.
  1 allocator, 2 offliners, child->parent->root; sequentially
  consistent bounded state, not a real-kernel KASAN or LKMM proof.
- R-018/F6 (stable): Credible severe user-visible UAF, Cc stable
  appropriate. Author reports patched 5,000 rmdir rounds and 2,000
  controller-disable rounds with no sanitizer report. These rates
  were not independently reproduced. Fixes is from 2012; modern
  backports need tree-specific adaptation.

Upstream guidance checked 2026-10-20:
  Sashiko 026195ab58e2099e81017adbc6b97f33c509c8ba
  Tejun cbb4478d0f73e15907335e70a2dc2fe54a9e7167
  Chris d048f8742f6740c38833adf02e87901412d771ca.
Manual seven-stage Sashiko, independent and Tejun/Chris covered;
  native Sashiko not run. Native TLC and tla-mctj did run.
No kernel build, live KASAN, or herd7 check performed.
Standing rules: 74 of 75 applied; 0 inapplicable; 1 unresolved.
  Unresolved A47: native Sashiko not run.
Next: ask Daehyeon to remove G10, review updated diff, then consider
  Reviewed-by. LKML-ready reply drafted; NOT SENT.

### R-019

Subject: mm/memcontrol: publish null pointer before dropping css reference
Author: Joshua Hahn. Submitted 2026-10-20.
Status: PARTIAL SOURCE REVIEW; UNRESOLVED. No unconditional take.
Report: `memcontrol-stock-review.md`.
The ledger contains the actionable R-019 summary; the detailed report
retains traces and verification artifacts without duplicating them here.
Submission was retrieved as `memcontrol-stock-submission.patch` from the
file library; preimage `e7d7db5718f9a` remains unlocated.

- R-019/F1 (source-supported risk, not runtime-proven): both writers set
  nr_pages to zero and, in old code, drop the stock CSS ref before
  nulling cached. Reader is_memcg_drain_needed() reads cached then
  nr_pages under RCU and traverses ancestry only with nonzero count.
  Existence and harmful reachability of a stale count/pointer pairing
  need LKMM validation; do not infer UAF solely from pointer lifetime.
- R-019/F2 (proposed fix): pointer-before-put should exclude a new
  post-release RCU read of a non-NULL stock pointer under the intended
  publication assumptions. Full source/architecture proof pending.
- R-019/F3: kernel reproduction NOT RUN. A bounded cgroup
  migrate/offline/recreate, fault and reclaim stress harness has been GCC-built, not KASAN-tested.
- R-019/F4: e1a366be5cb4f849ec4de170d50eebc08bb0af20 (2019)
  verified as the RCU reader's historical introducing change.
- R-019/F6: analogous obj stock already NULLs cached before
  obj_cgroup_put, with an RCU-protected descendant reader; no sibling
  defect established.
- R-019/F5: no guard inserted; changed branch G01 consume zero count,
  G02 drain non-NULL, G03 drain nonzero, G04 reader non-NULL and
  G05 reader nonzero require complete producer/consumer auditing.

Formal: library contained `akpm-tla-tools.tar(2).gz`, now retrieved.
PlusCal translated, SANY succeeded; TLC and tla-mctj run natively.
SC/current count: both old and fixed pass (103/108 states). With
explicit stale count: old fails Safety (TLC 118*, mctj 101*),
patched passes (137 states each); conditional counterexample NOT
verified against LKMM. No native Sashiko, kernel runtime, KASAN,
herd7 or complete pinned-stage review executed.
Upstream SHA heads checked afresh: Sashiko advanced to
b063c144377b569c39eb3c7d2f689478062fc4f1; Tejun remains
cbb4478d0f73e15907335e70a2dc2fe54a9e7167 and Chris remains
d048f8742f6740c38833adf02e87901412d771ca. Pinned guides and
full independent/guided reconciliation remain pending.
Next: exact matching tree, complete lifecycle and LKMM memory-order
audit, full pinned guided methods, KASAN old-vs-new comparison.

R-019 follow-up, 2026-10-20, four-message `grabbed(2)` LKML mbox:
- R-019/F7 (human correction): Shakeel Butt notes consume_stock()
  has a reference held by its caller; its stock CSS put is not final.
  Joshua agreed. Earlier review overgeneralized this site as a
  potential freeing path; the new draft explicitly corrects it.
- R-019/F8 (remaining race candidate): Joshua identifies refill_stock()
  slot eviction calling drain_stock() without the FLUSHING flag; the
  remote is_memcg_drain_needed() RCU reader need not take local_lock.
  Thus the flag does not exclude every concurrent drain/reader pair.
- R-019/F9 (still unresolved): drain_stock zeroes nr_pages before its
  final put, and the reader tests nr_pages before following ancestry.
  A post-GP-entry stale nonzero observation is not yet proven under
  LKMM. Native bounded SC/stale-choice models are not that proof.
- Joshua reports later page_counter_stock series removes this site and
  adjusts ordering; series applicability/merge status unverified.
Next: LKMM memory-order litmus/source check; avoid sending older generic
reply; exact preimage still absent. No kernel tests, Sashiko native run,
or new formal checker run in this follow-up.



### R-020

Subject: compat: Avoid double rounding in times()
Original: [PATCH] compat: Avoid double rounding in times()
Author: Hungyu Lin <dennylin0707@gmail.com>; 2026-10-20.
Base: f47d223627f80cb7a1eb14c585fe6cb35de5e984.
Preimage kernel/sys.c: 35b538ba843c705dba5378f3626ce5610e9db0cf.
Report: reports/compat-times-review.md.
Status: SOURCE-LEVEL FIX SOUND; full guided review/runtime unverified.
Finding R-020/F1: do_sys_times() already emits USER_HZ ticks; the
compat helper converts back to jiffies then to COMPAT_USER_HZ. With
HZ=250 and both rates 100, odd tick counts lose one extra tick (10ms).
The new equal-rate direct-return branch avoids loss and leaves
separate syscall return and unequal rates unchanged. G01 necessary.
Arithmetic Python enumeration run, not kernel build or runtime test.
Historical Fixes f06febc96ba8 verified; backports not checked.
Stable: prospective candidate; changelog: sufficient.
Next: optional compat 32-bit runtime validation and stable ancestry.

### R-021

Subject: mm/page_alloc: clear page tag refs when onlining hotplugged memory
Author: Zenghui Yu. Posted 2026-10-21 +0800.
Status: REVISE; previous favorable verdict withdrawn on Sashiko feedback.
Detailed report: reports/page-alloc-hotplug-tag-review.md.
F1: Original hotplug WARN supported: __free_pages_prepare() subtracts
allocation tag from unallocated head with NULL reference.
F2 (new, SOURCE VERIFIED): clear_page_tag_ref(p) on every base page
marks all pages CODETAG_EMPTY, but pgalloc_tag_sub(page, order count)
consumes only head marker. Tail markers survive into buddy and may
suppress subsequent missing-tag diagnostics after splitting and an
untagged allocation/free. Earlier claim that per-page marking was
necessary for split buddies was wrong. Runtime manifestation untested.
F3 (new): deferred_free_pages() and mm/kmsan/init.c:do_collection()
call __free_pages_core(..., MEMINIT_EARLY) without an immediately
preceding clear_page_tag_ref(). Configuration/boot reachability still
to be completed. Prefer one head-only mark covering both contexts.
F4: Previous comparison to free_reserved_pages() was misleading:
that helper marks all base pages but uses __free_frozen_pages(), not
the same __free_pages_prepare() consumer. CMA uses head-only mark.
Source: base f47d223627f80cb7a1eb14c585fe6cb35de5e984. Submitted
preimage e71e514ea18d still not matched exactly. No kernel tests.
Independent source and external Sashiko claims reconciled, but no native
Sashiko execution here; full guided tracks and testing still incomplete.
Impact: hotplug warning; risk of masking future debug warnings.
Stable: not recommended for current revision. Next: request v2 and test
order-N free/split/untagged allocation/free plus MEMINIT_EARLY paths.

R-021 v2 note (2026-10-22): Zenghui Yu posted
`mm/page_alloc: mark pages freed by __free_pages_core() as not tagged`.
The new diff marks only the head, inside __free_pages_core() for both
MEMINIT_EARLY and MEMINIT_HOTPLUG, and removes the now-duplicated
memblock_free_pages() mark. This addresses the v1 structural concern.
In a focused Fixes-tag check, recommend d224eb0287fb
("codetag: debug: mark codetags for reserved pages as empty"),
consistent with CMA correction 766c163c2068. v2 was NOT subjected
to a complete new guided review or runtime test; previous v1
REVISE verdict must not be misattributed to v2.

### R-019 v2 reassessment (2026-10-20)

Joshua Hahn's [PATCH v2] keeps the same code and adds Shakeel Butt's
PREEMPT_RT timeline (https://lore.kernel.org/all/atfMngq7nyZpt4u-@linux.dev/).
On PREEMPT_RT the per-CPU stock lock remains preemptible and holds an
RCU read-side section. After the last css_put() and before cached[i]
is cleared, freeing may initiate a grace period. A later-started
remote drain reader is not protected by that earlier grace period.
This strengthens the potential UAF mechanism. However, the reader
also requires a nonzero nr_pages observation, whereas drain_stock()
clears nr_pages before css_put(). Source/LKMM confirmation of a stale
count observation is still pending; no KASAN reproduction exists.
Worst credible impact if reached: kernel UAF, oops/panic, system outage
and possibly memory corruption, with indirect data loss. No proven
privilege escalation or filesystem corruption. The reorder itself
appears sound. Detail: reports/memcontrol-stock-review.md.


### R-023

Subject: lib/firmware_table: validate subtable bounds
Original: [PATCH v2] lib/firmware_table: validate subtable bounds
Author: Jiale Yao <yaojiale02@163.com>. Date: 2026-10-21.
Source: torvalds/linux lib/fw_table.c blob
  16291814450ee39a2ad656f93c316bdc8f998939, matching the submitted
  preimage. Fixes: 60574d1e05b094d222162260dd9cac49f4d0996a.
Status: REVISE. Detailed record in reports/fw-table-review.md.
R-023/F1 (new regression): Changing the generic-header admission
  test from < to <= newly dispatches terminal records of exactly the
  generic header's size. PRMT subtable_len=4, entry_len=4, remaining=4
  passes v2 checks. ACPI_SUBTABLE_PRMT reports type 0 and init_prmt()
  installs a handler for 0. acpi_parse_prmt() treats the 4-byte record
  as struct acpi_prmt_module_info (38 bytes), first accessing
  handler_info_count at offset 24. This was not dispatched previously.
  CEDT CHBS also reads beyond its generic four-byte header in its
  handler without a full typed-size guard. Malformed firmware can cause
  kernel out-of-bounds reads and potentially boot/probe oops or panic.
R-023/F2 (valid repair): New entry_len < subtable_len and
  entry_len > remaining checks prevent the generic parser from
  invoking handlers on too-short header envelopes or records beyond
  the declared table end. Trailing bytes shorter than the generic
  header remain ignored. Retain these two guards, but reconsider <=.
R-023/F3 (related pre-existing issue): Some handlers do not check
  typed payload size before accessing fields. PRMT, CHBS and CFMWS
  paths deserve separate hardening beyond the generic header bounds.
Tests: standalone source-mirrored C dispatch model (GCC/ASan+UBSan)
  prints old_dispatch=0, v2_dispatch=1 for a final PRMT header;
  separate ASan model detects a heap-buffer-overflow at offset 24 in
  a four-byte allocation. No actual kernel build, KASAN boot or
  runtime firmware injection. Native Sashiko not run. Guided review
  sources pinned; complete all-stage coverage was not obtained.
Guard audit: 3 of 3 checked; 0 redundant; 0 unresolved. The <=
  decision is independently UNSAFE for the demonstrated state.
Model: no new multi-actor synchronization; finite bounds model was
  used rather than PlusCal/TLA+.
Impact-changelog: needs detail about possible boot/probe failure.
Stable: not this v2; corrected, tested candidate after mainline merge.
Next: ask to retain strict < or validate actual handler requirements
  before allowing exact-end generic-only records; add target tests.

### R-024

Subject: delayacct: Preserve delay extrema when aggregating taskstats
Original: [PATCH] delayacct: Preserve delay extrema when aggregating
  taskstats
Author: Hungyu Lin <dennylin0707@gmail.com>. Date: 2026-10-21.
Source: kernel/delayacct.c blob 479e860aff705ab4b89fd6b7860c37f912e3a17b.
Fixes: 658eb5ab916ddc92f294dbce8e3d449470be9f86 and
  f65c64f311ee2f1ddc1eb395ed8b20e6b9d14e85 (verified).
Status: SOURCE-LEVEL FAVORABLE, not fully validated. Report in Library:
  reports/delayacct-extrema-review.md.
R-024/F1 (old bug confirmed): TGID aggregation overwritten max, min
  and the corresponding max timestamp with the last thread's values.
  Last thread with no delays could erase a positive prior peak while
  retaining a nonzero aggregate delay total.
R-024/F2 (fix correct in reviewed cases): conditional max with paired
  timestamp and min_not_zero() across CPU and seven locked delay types
  preserve valid extrema and ignore zero (unsampled) minima. PID fresh
  zero result and previously aggregated exited-thread stats checked.
  Equal maxima preserve the first maximum's timestamp.
R-024/F3 (preexisting uncertainty): CPU sched_info snapshots may race
  scheduler updates; no new locking or ownership path was introduced.
Testing: GCC and Clang/UBSan standalone reducer model passed 32,768
  three-task/category extrema combinations plus tie and retained-peak
  cases. No real kernel build, getdelays test, KASAN or native Sashiko.
Guard audit: 24 of 24 checked; 0 redundant; 0 unresolved.
Model: no new multi-actor shared protocol; TLA+ not needed.
Impact: misleading taskstats TGID maxima/minima/timestamps may hide
  latency spikes from getdelays. Actual task execution unaffected.
Impact-changelog: sufficient, but a getdelays -t example would improve
  operational usefulness. Stable: candidate after testing and branch
  applicability review; no unconditional approval at present.
Next: request multi-threaded before/after runtime test; confirm stable
  branches and complete pinned external guide coverage.

## Maintenance reminder

When feedback arrives, update findings and dispositions here. Archive
resolved OR dormant reviews into that day's
`review-activity-YYYY-MM-DD.md`, leaving the normalized Subject and
filename above. Keep this file lean; retain durable lessons in the
AKPM workflow only when broadly applicable.


### R-022: profile: simplify /proc/profile read layout - Sashiko feedback

Feedback on a8d18dfd81aa2aff9c918b03a5a93bd7b83ef000:
The [2/2] cleanup narrowed loff_t *ppos into size_t before its EOF
check.  On 32-bit kernels, pread64() at 0x100000000 could therefore
return the first profile bytes rather than EOF.  Source-level finding
verified; prior approval was incorrect.  [1/2] remains unchanged.
Revised [2/2] retains loff_t until negative-offset and EOF checks,
then assigns the known-in-range value to size_t.  The revised series
was applied sequentially in a disposable fixture.  A 32-bit kernel
runtime test has not been run.  A new workflow rule requires checks of
full-width API inputs before any narrowing conversion.

R-022 follow-up (2026-10-20): Reviewed uploaded three-patch series
(Avi sampling-step, partial-copy, cleanup) in order against an
upstream-source-equivalent fixture. All applied; no new code correctness
blocker found. The new cleanup checks full-width loff_t before size_t.
Model of 32/64-bit offsets and fault prefixes passed; no fresh
in-kernel testing, native Sashiko or full guided review was run.
Minor prose: [1/2] names Avi's prerequisite vaguely rather than by
exact subject; recommend precise patch reference. Detailed notes in
reports/profile-read-review.md.

### R-019 follow-up: slot generation counterexample (2026-10-20)

Corrects earlier overly narrow concern about observing a stale
nonzero nr_pages. Following final css_put(old) in drain_stock(), an
RCU reader can load cached[i]=old after G starts, then be preempted.
The owner clears the slot and returns from its RT local lock; G ends,
old is freed, and refill_stock(new) reuses the slot with a new positive
nr_pages[i]. The reader resumes with the old pointer and NEW count,
then dereferences old in mem_cgroup_is_descendant(). No stale count
read or weak-memory behavior is required. This is source-replayable
bounded interleaving reasoning, not a kernel test or herd7 execution.
The patch's NULL-before-final-put order prevents this trace. The
prior R-019 note demanding a stale read is superseded. Update the
LKML reply accordingly. Detailed evidence in
reports/memcontrol-stock-review.md.


### R-025

Subject: [PATCH] mm/hugetlb: charge hugetlb cgroup and memcg in
  alloc_hugetlb_folio_reserve()
Author: Hongfu Li <lihongfu@kylinos.cn>. Reviewed: 2026-10-21.
Base: 2887e63d2e8e0cf55402612d8996ce955a2c3e55.
Status: REVISE/SEQUENCE AFTER R-018 cgroup CSS offlining lifetime fix.
Detailed report: reports/hugetlb-reserve-charge-review.md.

- R-025/F1 (cross-patch UAF): New use of
  hugetlb_cgroup_charge_cgroup()/commit inherits the existing R-018
  CSS ref lifetime race. An existing memfd reservation owned by A
  does not protect B's usage CSS when another cgroup pins the page.
  CPU0 acquires B CSS ref; CPU1 offlines B and scans zero usage BEFORE
  CPU0 charges B; CPU0 then charges the dying B, drops the last ref,
  and commits a stale CSS pointer. Source-replayable UAF risk. R-018
  needed before adding this path. Current AKPM mm-stable still has
  mm/hugetlb_cgroup.c blob 3fb41311e4c7dcbbd26f7b230ebb1f8c7ce310fe.
  Do not incorrectly claim CSS offlining finishes if the counter was
  already charged: hugetlb_cgroup_have_usage() checks that counter.
- R-025/F2 (incorrect introducing Fixes): 26a8ea80929c changed the
  allocation to alloc_hugetlb_folio_reserve(); the predecessor
  alloc_hugetlb_folio_nodemask() was also uncharged. Use
  Fixes: 89c1905d9c14 (original memfd_pin_folios commit).
- R-025/F3 (valid main repair): matched hugetlb_alloc_folio() charge
  and NR_HUGETLB accounting sequence; checked cgroup/memcg failure,
  free_huge_folio rollback, restore_reserve, and memfd inode unreserve.
  No standalone charge/rollback defect found in ordinary paths.
- R-025/F4 (scope): memory.current/max only includes HugeTLB when
  cgroup v2 has CGRP_ROOT_MEMORY_HUGETLB_ACCOUNTING. Author's values
  demonstrate positive accounting change but not denial at limits.
  Suggest one targeted cgroup-limit failure/rollback test; not run.

Validation: mm/hugetlb.c preimage
  b37d7d0db7fc94798a1e98af78853952ee989488;
Fixes history 26a8 and 89c verified in GitHub. Caller scan: mm/memfd.c,
mm/gup.c, drivers/dma-buf/udmabuf.c, IOMMUFD, and shmem-only
live-update. Native Sashiko, kernel tests/build and current-case
formal model: NOT RUN. Existing R-018 TLC/tla-mctj evidence reused
as prior work, not newly run. Guard audit: 5 of 5 checked,
0 redundant, 0 unresolved. Standing rules: 66 of 80 applied;
4 inapplicable; 10 unresolved (see detailed report).
Current upstream pin: Sashiko 780530cc1f894c9a18e3db206a99edf3bc09a70e;
Tejun cbb4478d0f73e15907335e70a2dc2fe54a9e7167;
Chris d048f8742f6740c38833adf02e87901412d771ca.
Stable: prospective candidate after dependency and target-tree validation.
Next: coordinate with Daehyeon's UAF repair; correct Fixes tag and
memory.max qualification, then reconsider acceptance. No email sent.

## R-026

Subject: mm/vmalloc: reject overflowing vm_map_ram page counts
Author: Shubhang Kaushik (Ampere). Date: 2026-10-22.
Status: REVISE; functional fix correct, 64-bit Clang W=1 warning.
- R-026/F1: `count > ULONG_MAX >> PAGE_SHIFT` is always false
  on 64-bit because count is unsigned int. Clang W=1 emits
  `-Wtautological-constant-out-of-range-compare`, and a
  W=1/CONFIG_WERROR build could fail. Prefer check_mul_overflow
  ((unsigned long)count, PAGE_SIZE, &size).
- R-026/F2: On 32-bit, input count 1048577 can create only
  a 4KiB virtual mapping while returning success, exposing later
  users of the mapping to faults/corruption. New guard returns
  NULL. No direct userspace path independently proven.
- Historical Fixes: db64fe02258f originally introduced
  vm_map_ram with unchecked shift.
- Matching preimage blob: bea9f76ed7e74247d4ce919250c2f02dd5c36483.
- Source: vm_map_ram, vb_alloc, alloc_vmap_area,
  vmap_pages_range, vm_unmap_ram, scripts/Makefile.warn.
  Guard audit 1/1. GCC and Clang standalone expression checks,
  no kernel build or actual runtime test.
- Sashiko pin db5a447c7b3bdad217063b993863ba69155a61a8;
  Tejun pin cbb4478d0f73e15907335e70a2dc2fe54a9e7167;
  Chris pin d048f8742f6740c38833adf02e87901412d771ca.
  Native Sashiko not run; full stage/manual 80-rule audit and
  exhaustive caller scan not completed.
- Detailed report: Library `/Kernel Patch Reviews/reports/
  vm-map-ram-overflow-review.md`.


## R-027

Subject: mm/zswap: validate dlen and normalize comp_ret on compression success
Author: Suseendran Bhaskaran <suseendranb@google.com>.
Date: 2026-10-22. Historical Fixes: dca4437a5861.
Status: SOURCE-LEVEL FAVORABLE, hardware status validation outstanding.
- R-027/F1: On a successful crypto_acomp_compress() result of exactly
  PAGE_SIZE bytes, existing writeback-disabled zswap rejects the page as
  before, but comp_ret previously became -EINVAL and incremented
  reject_compress_fail. Patch assigns -ENOSPC and increments
  reject_compress_poor instead. /sys/kernel/debug/zswap counters change;
  acceptance/rejection remains unchanged.
- R-027/F2: Successful zero or oversized dlen now triggers
  WARN_ON_ONCE and rejection. This introduces a possible panic under
  panic_on_warn if any provider can legitimately yield such success.
  HiSilicon ZIP accepts HZIP_NC_ERR as a success-like status and sets
  dlen to hardware-reported produced bytes. The actual attainable
  values of that status under PAGE_SIZE capacity were NOT validated.
- R-027/F3: Real compressor error codes retain priority; dlen after
  errors varies across zstd, 842, LZ4, deflate and hardware backends.
  Longer-term Crypto API error-consistency cleanup should distinguish
  insufficient destination capacity (-ENOSPC) from compressor errors.
  Successful output of PAGE_SIZE is not itself a compressor error.
- Preimage: mm/zswap.c blob 37f34e406c8e3bb00f3ba1479293d486fc9f64ec.
  Looked at include/crypto/acompress.h, crypto/scompress.c,
  crypto/zstd.c, crypto/lz4.c, crypto/deflate.c and hisi ZIP callback.
- Impact: debugfs counter correction on writeback-disabled systems;
  additional one-time kernel warning on invalid reported success,
  possibly fatal under panic_on_warn. No normal-workload performance,
  swap-content, or page-acceptance change shown.
- Stable: unresolved pending provider behavior/target tree/testing.
  Impact-changelog: needs explicit counter and warning description.
- Review performed: focused first-principles source review only.
  Native Sashiko, complete guided-stage coverage, kernel builds and
  runtime tests NOT RUN. No author/maintainer feedback asserted.
- Detail: /Kernel Patch Reviews/reports/zswap-acomp-dlen-review.md.

## R-028

Subject: mm/hugetlb: disable PMD sharing for UFFD missing mode
Commit referenced: 5da87cbb6b8f2271fb75acc59e14e2d5860cb54c.
Author: David Hildenbrand (Arm). Subject and diff supplied in chat.
Status: SOURCE-SUPPORTED INCOMPLETE FIX, pending independent reproducer.
- R-028/F1: New uffd_disable_huge_pmd_share() checks only the current
  VMA's vm_userfaultfd_ctx.ctx, preventing PMD sharing while UFFD is
  registered. UFFDIO_POISON can put a process-local marker into the
  private HugeTLB page table, and unregister/release clears the context
  and flags but preserves the PTE_MARKER_POISONED marker.
- R-028/F2: Another process mapping the same shared hugetlbfs file can
  later choose the unregistered VMA as a PMD table donor: page_table_shareable()
  checks flags/alignment but not poison contents; huge_pmd_share() can
  attach the table, and hugetlb_fault() returns VM_FAULT_HWPOISON_LARGE
  for the second process (userspace SIGBUS).
- R-028/F3: If the original process then unshares its PMD (such as via
  mprotect), __huge_pmd_unshare() removes its PUD reference without
  copying the poison marker into a replacement; the second process
  retains the shared table and the originating process may lose its marker.
- The new VM_WARN_ON_ONCE in hugetlb_mfill_atomic_pte() checks only at
  insertion and cannot prevent a later share after UFFD unregister.
- Source paths read: mm/userfaultfd.c:userfaultfd_clear_vma,
  userfaultfd_unregister, release_all, registration; mm/hugetlb.c:
  hugetlb_mfill_atomic_pte, page_table_shareable, huge_pmd_share,
  __huge_pmd_unshare, hugetlb_fault. Exact submitted commit tree was
  not independently fetched; supplied patch and available sources used.
- Impact: second process may receive SIGBUS for a marker it never set;
  original mapping may lose poison marker. Ordinary configured
  mappings without UFFD poison unaffected.
- Stable: unresolved; author response, correction design and runtime
  registration -> poison -> unregister -> second fault test needed.
- Review performed: focused source-level adjudication of Sashiko claim,
  not native Sashiko and not a complete standalone multi-stage audit.
- Detail: /Kernel Patch Reviews/reports/hugetlb-uffd-pmd-share-review.md.

## R-029

Subject: mm/migrate: snapshot the source nid before the misplaced migration
Original: [PATCH] mm/migrate: snapshot the source nid before the misplaced
  migration
Author: Yafang Shao <laoar.shao@gmail.com>. Date: 2026-10-23 +0800
  (2026-10-22 in America/Los_Angeles).
Fixes: e39bb6be9f2b ("NUMA Balancing: add page promotion counter").
Rechecked: 2026-10-22 PT; checker execution logs use 2026-10-23 UTC.
Status: SOURCE-SUPPORTED hot-remove finding retained with narrower scope;
  no reproduced kernel crash; full standalone review coverage incomplete.

- R-029/F1: migrate_misplaced_folio() can inspect source metadata after
  migrate_pages()/migrate_folio_done() released its final reference.
  Snapshotting the integer nid before migration removes this late load.
  No new allocation, lock, error path or migration decision is introduced.
- R-029/F2: Ordinary reuse of a physical page does not normally change
  its NUMA node. The changelog's reuse-based wrong-nid argument remains
  unsubstantiated. Do not imply a routine allocator-reuse crash or a
  demonstrated promotion-count error.
- R-029/F3: Source-supported conditional x86 hot-remove fault. The old
  read requires nr_succeeded > 0 AND memory-tiering mode. Delay the task
  after migrate_pages() returns, then offline and actually remove an
  otherwise-free removable source block. Keep other source-node memory,
  destination memory and nonmovable kernel state outside that block.
  Removal covering the source vmemmap leaf can clear its mapping and
  flush TLBs before the task resumes the stale folio_nid() load. A kernel
  fault/oops and possibly panic can result. No unprivileged removal
  trigger or exploit has been demonstrated.
- R-029/F3a (important refinement): Offlining != actual removal. DEBUG_VM
  poisoning alone is not a proved crash: folio_nid() extracts node bits
  and node_is_toptier() handles a NULL pgdat. The concrete fault route
  retained here is a load from metadata that has actually been unmapped.
  Do not claim that every partial removal clears the source metadata.
- R-029/F3b (counterarguments checked): do_numa_page() and
  do_huge_pmd_numa_page() drop PTL before migration. Outer VMA/mmap locks
  do not pin the vacated source PFN. lock_vma_under_rcu() drops RCU before
  returning. RCU-watching on exception entry is not an RCU read lock.
  node_is_toptier() takes RCU only after folio_nid() has been evaluated
  as its argument; that inner critical section cannot protect this load.
  kfree_rcu(ms->usage) defers usage storage, not the vmemmap depopulation.
  A pause after migration returns avoids relying on simultaneous source
  page isolation or source allocator locks. No remaining source ref
  blocks the free-page test; an extra-reference model control does block
  it until the accounting step has finished.
- R-029/F4: PGPROMOTE_SUCCESS is statistics, not the promotion rate-limit
  input (PGPROMOTE_CANDIDATE). The patch does not freeze concurrent node
  tier reconfiguration; do not claim perfect counter attribution across
  every topology change. Its demonstrated repair is the metadata lifetime.

Source pin: 864c07de0c7dcbca58b61625dfa2e461ae63b242.
Matching mm/migrate.c blob: 15b45832bcfa7e93f768bea5f3115a2fb95aa5b5.
Re-read: mm/migrate.c (1200, 2755); mm/memory.c (6288, fault dispatcher);
mm/huge_memory.c (2320); mm/mmap_lock.c:lock_vma_under_rcu();
arch/x86/mm/fault.c; mm/memory_hotplug.c (1955, 2291);
mm/page_isolation.c (556, 605); mm/sparse-vmemmap.c (776);
arch/x86/mm/init_64.c (1020-1295); include/linux/mm.h (2368-2420);
mm/debug.c; mm/memory-tiers.c (275-301). Fixes commit fetched again.

Executed validation:
- PlusCal translation and SANY parsing succeeded.
- Both TLC and tla-mctj ran all 8 bounded variants and agreed.
- Old/remove: NoUnmappedRead violated, 30 distinct states (falsification).
- Snapshot/remove: PASS, 32 distinct states, complete depth 13.
- Old/offline-only: PASS, 32 states, no poisoning or removal.
- Old/poison-only: NoPoisonedRead violated, 26 states; this is NOT a
  kernel-crash assertion. Same variant's NoUnmappedRead check passed
  with 38 states.
- Old/tiering-disabled: PASS, 32 states.
- Old/extra-reference-held-until-after-accounting: PASS, 20 states.
- Snapshot/poison-only: PASS, 32 states.
- Two actors, one successful migration/block, refs 0..2; sequential
  consistency only. Model trace replayed against C. This checks the
  specified abstraction, not arbitrary kernel/hardware behavior.
- TLC 2026.10.15.145915 (rev 932d35e); supplied tla-mctj binary identified
  by SHA256 in the model README. Exact commands, configs, wall times,
  generated TLA+, trace and logs retained locally in r029-recheck/.
- No kernel build, runtime hotplug/KASAN/QEMU test, native Sashiko or
  LKMM run. No observed failure or author confirmation invented.

Methodology pins checked afresh:
Sashiko db5a447c7b3bdad217063b993863ba69155a61a8;
Tejun cbb4478d0f73e15907335e70a2dc2fe54a9e7167;
Chris d048f8742f6740c38833adf02e87901412d771ca.
Core Sashiko domains/verification and Tejun formal-model guide applied
in this focused recheck. Complete guided/vendored coverage, broad MM
similar-bug search and stable-branch validation remain uncompleted.

Standing rules: 64 of 86 applied; 6 inapplicable; 16 unresolved
Guard audit: 4 of 4 checked; 0 redundant; 0 unresolved

Impact-changelog: needs accurate post-release/removal conditions rather
than ordinary-reuse changes to nid. Stable: unresolved pending target
applicability and kernel validation; no submission or metadata change.
Next action: use the refined email below, not the earlier implication
that merely poisoning page metadata establishes a crash.

Report path:
/Kernel Patch Reviews/reports/migrate-misplaced-src-nid-review.md
Persistence reconciliation (2026-10-22 PT): the previous Library
write failure describes the earlier review session only. The detailed
report and its formal-model archive are now verified in the Library.
That report records an earlier 83-rule audit and model iteration
(old/remove 42; fixed/remove 45 distinct states). This master ledger
records the later 86-rule audit and eight-variant model recheck
(old/remove 30; snapshot/remove 32 distinct states). They must not
be confused as one execution. An addendum to the detailed report now
records the later ledger's findings, without replacing earlier logs.
The latest model-run artifacts were not independently recovered in
this handoff, and no source or checker work was repeated. Historical
A83 remains UNRESOLVED in the earlier 86-rule audit count; the Library
report update was completed afterward.

Copy-ready reply (unsent):

```text
The source-node snapshot looks correct. I rechecked the hot-remove
case, including the outer fault-path locks and RCU protection.

With memory-tiering mode enabled, a successful migration can release
the source folio before the promotion-accounting folio_nid() read.
If the task is delayed here, the source block can be offlined and
removed, tearing down its vmemmap mapping before that read executes.
On the inspected x86 path this can cause a kernel oops, and possibly
a system panic. Merely offlining or poisoning the metadata does not
by itself establish that outcome.

Ordinary page reuse does not change the physical page's NUMA node.
I'd describe the post-release metadata access and conditional
hot-removal failure in the changelog instead.

This is supported by source inspection and bounded model checking;
I have not reproduced a crash on a running kernel.
```

Correction history: the first review called the hot-remove outcome
unestablished. The next source pass identified metadata teardown. The
prior report overstated poison-to-crash inference and omitted the
memory-tiering branch restriction. This recheck retains actual-unmap
faults, adds those qualifications and executes falsifiable model checks.

### R-029 audit scope and limitations

Fixed inventory: A01-A86 in the detailed recheck evidence; denominator
was recorded before source revalidation. Applied 64; inapplicable 6;
unresolved 16. Inapplicable: A28 no bounds changes, A58 no weak-memory
claim, A77 no userspace reproducer authored, A79 no tracking-contract
change, A80 no multi-element metadata write-set, A81 no record parser.

Unresolved: A10 all counter consumers not re-fetched; A12 architecture
exhaustiveness; A25/A35 broader MM pattern search; A26 kernel build and
runtime compatibility; A37 full Sashiko selection pipeline; A38 full
vendored guides; A47 native Sashiko unavailable; A49 full Tejun workflow
and dependencies; A51 complete Chris prompts; A52 complete historical
methodology diffs; A53 full three-track reconciliation; A64/A65/A66 full
stable validation/routing; A83 Library write unavailable. These are
coverage/storage limits, not observed defects in the snapshot change.

Guard audit: G01 nr_succeeded gates this branch; G02 memory-tiering bit
must be on for the old load; G03 source-tier predicate changes only the
point where source nid is obtained; G04 destination-tier check is later
and cannot protect G03. All four checked, none redundant or unresolved.
No new conditional, rejection, allocation or lock is added by the patch.

### R-029 maintainer feedback (2026-10-22 PT)

Input: mbox(20261023-051302), four messages including the original patch.
R-029/F2: human feedback CONFIRMS rejection of the ordinary-reuse
rationale. Matthew Wilcox disputes changed physical nid after freeing;
Yafang Shao agrees. Normal allocator flag masks and node-field layout were
independently inspected. Original patch reports no real issue observed.

R-029/F3 remains SOURCE-SUPPORTED and UNREPRODUCED, pending human feedback
about actual hot-removal. Neither supplied maintainer/author reply
discusses that mechanism. Andrew's later off-list message forwards an older
AI draft and asks for verification; there is no reply to that question in
this mbox. This is not independent confirmation of the AI claim.

R-029/F3a correction retained: poisoning alone is not a demonstrated crash.
Fresh source checks cover final source put, PTE/PMD callers, outer
fault/VMA RCU scope, offlining versus removal, x86 PMD unmapping/TLB flush,
and the callee's too-late RCU/NULL checks. Keep the successful-migration
and memory-tiering restrictions, an actually removable metadata range, and
other source-node memory.

R-029/F4 remains unchanged: snapshotting nid does not snapshot the node's
current tier. No new kernel build, runtime experiment, compiler test, TLC,
tla-mctj, herd7 or native Sashiko run occurred. Historical model runs and
the 83/86-rule audits remain distinct.

Feedback Message-IDs:
<atrUeGPZgoSACpOR@casper.infradead.org>
<CALOAHbARy4pSrsDLmTfntdsWONETqPrGJM+g6jM27WWnc-bCAw@mail.gmail.com>
<20261022221126.70238debd0c1c601bee952b5@linux-foundation.org>

Standing rules: 38 of 50 applied; 2 inapplicable; 10 unresolved
Guard audit: 4 of 4 checked; 0 redundant; 0 unresolved

Scope: focused feedback verification, not full standalone acceptance.
Outstanding B06/B09/B20: exhaustive caller, architecture and broader MM
checks; B22/B23/B34/B36/B37: complete guided pipeline/dependency coverage
and reconciliation; B32: native Sashiko; B43: full stable validation.

Detailed report updated and Library upload/readback verified at /Kernel
Patch Reviews/reports/migrate-misplaced-src-nid-review.md. The workflow is
unchanged; its current rules already cover this feedback.

Next: await the off-list hot-removal response, request corrected rationale
and targeted old-versus-snapshot testing, and complete the outstanding
full-review coverage before unconditional acceptance. Revised off-list
email is drafted in the report, not sent.


## R-030

Subject: mm/vma: fix expansion of VMA_MIXEDMAP_BIT VMAs
Original: [PATCH] mm/vma: fix expansion of VMA_MIXEDMAP_BIT VMAs
Author: Lorenzo Stoakes (ARM) <ljs@kernel.org>. Date: 2026-10-23.
Base: 2bba28e98578de622ef307d00875aa8f8bca3d10.
Matching mm/vma.c blob: 1be613044b4a50cb8b1bbe6955755fac762dc80e.
Matching VMA userspace dup.h: f449129ea97a9c85eaccf78a10f9a313b8e27b12.
Fixes: ca3d76b0aa808a06997297d123b66d17b81e5285 (verified).
Status: SOURCE-LEVEL FAVORABLE; full review-stage/test coverage incomplete.
Detailed report: /Kernel Patch Reviews/reports/
  vma-mixedmap-expansion-review.md.

R-030/F1 (confirmed old regression): eligible mixedmap mremap() expansion
  fails -ENOMEM even with free adjacent space. The old extension merge
  helper rejects a nonmergeable VMA and its caller treats NULL as OOM,
  without attempting MayMove fallback. Luiz Capitulino reported the
  failure using vm_insert_page() in an external module. Lorenzo says the
  reproducer and mm/VMA selftests pass after the fix; AUTHOR-REPORTED.
R-030/F2 (fix proof): when vma_can_merge() is false, initialize
  VMG start at original vm_start to retain file/anon offsets, rewind VMI,
  keep next=NULL and call vma_expand() on the original target. Earlier
  check_prep_vma() rejects PFNMAP/DONTEXPAND, align_hugetlb() rejects
  HugeTLB expansion; thus the legal nonmergeable case is MIXEDMAP.
  commit_merge() preallocates before mutation; failure returns -ENOMEM
  and mremap uncharges. No new code blocker found.
R-030/F3 (nonblocking redundancy): both new VM_WARN_ON_ONCE() assertions
  are unreachable on legitimate current growth paths. They intentionally
  check future contract violations, but do not protect a valid new path.
  Guard audit: 5 of 5 checked; 2 redundant; 0 unresolved.
R-030/F4 (changelog): explicitly describe false -ENOMEM, absence of
  actual OOM, affected mixedmap applications, and failed MAYMOVE fallback.
  impact-changelog: needs detail. Stable: prospective candidate, not
  already eligible/merged; small tested-by-author fix with stable trailer.
  Check supported target branches and their configurations separately.
R-030/F5 (validation): source-mirrored C predicate/offset test compiled
  with GCC and Clang, both ASan+UBSan, 64 flag/config combinations each;
  all legal nonmergeable grow cases require MIXEDMAP. This is NOT an
  in-kernel test. No kernel build, native Sashiko, VMA userland runner,
  KASAN, TLC, tla-mctj or herd7 executed in this review.

Pinned review methods checked 2026-10-23 PT:
  Sashiko 867713d1c5e0005d04ea71c6691f39c8a69384a9
  Tejun cbb4478d0f73e15907335e70a2dc2fe54a9e7167
  Chris d048f8742f6740c38833adf02e87901412d771ca.
  Applied seven manual Sashiko domains and appropriate guided checks,
  but full vendored guide/dependency coverage was not certified.
  Standing rules: 52 of 67 applied; 3 inapplicable; 12 unresolved.
  Inventory was not precommitted before the independent source pass;
  it remains an explicitly unresolved procedural obligation.
  Model: no, existing mmap/VMA lock protocol unchanged; finite Boolean
  enumeration more appropriate than TLA+ for flag-classification logic.
Next: ask Lorenzo for concrete -ENOMEM changelog wording; review any v2,
  optional warning simplification and further tests. Await feedback;
  no email sent or Reviewed-by given. No new workflow rule established.

### R-031: mm: avoid losing atomic VMA flags (four-patch series)

Date: 2026-10-23 PT. Source mbox(20261023-181024); cover change-id
20261022-fix-vma-atomic-8c910fd66a28. Four patches; authors Lorenzo Stoakes
and David Hildenbrand. Explicit base:
5f980b2d53abf3950caff5d77b5c69dc6ebb19b6.

Status: SOURCE FAVORABLE, NOT FULLY CERTIFIED. Source review identified
three real guard-bit race mechanisms, an unsigned-locked_vm accounting
hazard, and a SOFTDIRTY loss when renaming an anonymous VMA. Source review
did not prove a new regression in patches 1-4. Ask for clearer userspace
runtime impact in changelogs, especially the conditional RLIMIT_MEMLOCK
bypass and wrong /proc soft-dirty reporting. No kernel build/stress tests
or native Sashiko execution; no Reviewed-by issued.

Google mirror currency check: mm-unstable HEAD
2bba28e98578de622ef307d00875aa8f8bca3d10, committer 2026-10-22 22:13:38
-0700. Fresh when checked on 2026-10-23 PT (<24 hours); no stale-mirror
warning. Google mirror freshness does NOT certify gitolite synchronization.
Base was resolved independently, and matching source blobs at both relevant
revisions were inspected; author base was not silently replaced.

R-031/F1 CONFIRMED pre-existing guard-loss race, FIX SOURCE-SUPPORTED:
patch 1 replaces stale flag rewrites from mprotect/madvise/mlock with
vma_overwrite_flags(), which preserves the current VMA_MAYBE_GUARD_BIT
under VMA write locking. vma_flags_same_pair() ignores exactly allowed
atomic flags.

R-031/F2 CONFIRMED pre-existing munlock underflow, FIX SOURCE-SUPPORTED:
when atomic guard only differs, mlock_fixup can decrement mm->locked_vm for
an already-unlocked region. Unsigned underflow followed by do_mlock()
additions can wrap the counter and bypass RLIMIT_MEMLOCK. Trigger: guard
flag set while a concurrent munlock path used stale flags, the eligible VMA
supports mlock, and subsequent mlock calls. Worst credible effects:
over-limit unevictable memory, reclaim pressure, system-wide slowdown or
OOM harm. Not runtime reproduced; no demonstrated kernel memory corruption
or privilege escalation.

R-031/F3 CONFIRMED pre-existing clone race, FIX SOURCE-SUPPORTED: patch 2
moves vma_start_write(vma) before vm_area_dup() in __split_vma(), and
asserts the writer lock in vm_area_dup(). Fork dup_mmap and mremap move_vma
already lock before duplication. NOMMU assertion delegates to mmap write
locking, not an introduced NOMMU WARN. Incomplete exhaustive
all-callers/configuration search remains open.

R-031/F4 CONFIRMED stale SOFTDIRTY overwrite, FIX SOURCE-SUPPORTED: patch 3
skips post-vma_modify_name() stale flag rewrite, preserving sticky
VMA_SOFTDIRTY_BIT acquired from merged neighboring VMAs. The earlier merge
already schedules khugepaged if appropriate. Worst credible userspace
effect: inaccurate soft-dirty bits in /proc/PID/pagemap, causing
dirty-state consumers (including incremental checkpointing) to miss
updates. No runtime reproduction.

R-031/F5 CONFIRMED sticky-publication race, FIX SOURCE-SUPPORTED: patch 4
collects sticky flags only after locking each contributing VMA and
publishes their union inside commit_merge after vma_prepare but before
vma_complete releases rmap locks. This avoids file-backed THP retraction
observing an expanded VMA with a missing guard bit. Both merge-existing and
expansion paths reviewed. Prealloc failure avoids partial mutation.

Guard loss can skip copying guard PTE markers in fork or allow retraction
on eligible file-backed THP mappings. Worst credible userspace behavior is
loss of protected guard regions, possible undetected boundary access and
application-level corruption/crash. No proof of kernel corruption or
observed exploit. In all cases separate source reachability from runtime
reproduction.

Original bug introducing commits verified: guard-bit read-lock work
2ab7f1bbafc927c69374d45578011c814c26ae2f and
49e14dabed7a294427588d4b315f57fbfcab9990 (2025-11-20); anonymous naming
9a10064f5625d5572c3626c1516e0bebc6c9fe9b (2022-01-15); sticky flags
64212ba02e66e705cabce188453ba4e61e9d7325 (2025-11-20). Stable inclusion and
target applicability NOT established; treat as prospective until upstream
merge and branch testing.

Executed a separate source-guided bounded Python interleaving check,
/mnt/data/r031-flag-model.py: old/fixed guard rewrite 1/0 bad legal
schedules (3 each); old/fixed split-copy 1/0 bad (6/1 schedules); old/fixed
sticky publication 1/0 bad (2/1 schedules). Simulated unsigned counter wrap
at 32 and 64 bits. Not a kernel runtime test, formal TLA run, or native
Sashiko. No compilation or Linux selftest run in this review.

Current method pins verified 2026-10-23: Sashiko
1bc9441db7faf9f2e464cd74a9ac0f6c3219082a; Tejun
cbb4478d0f73e15907335e70a2dc2fe54a9e7167; Chris
d048f8742f6740c38833adf02e87901412d771ca. Sashiko seven manual analysis
domains and verification/post-verification questions checked, relevant
Tejun/Chris guide modules read. Guide exhaustive stage/module coverage
incomplete and native run unavailable.

Standing rules: 55 of 70 applied; 4 inapplicable; 11 unresolved. Guard
audit: 8 of 8 checked; 0 redundant; 0 unresolved. Inventory was assembled
after independent source review began, so precommit policy C09 is
explicitly UNRESOLVED. Other outstanding: complete all-callers search,
kernel build/VMA tests/race-injection, full checker, full Tejun/Chris guide
audit, native Sashiko, target -stable validation, full architecture sweeps
and broader analogous-bug scan. No other review IDs, findings, or
historical audit states modified.

Detailed report stored in Library: /Kernel Patch
Reviews/reports/r031-vma-atomic-flags-series-review.md. The tiny
source-guided model archive is intended to reside alongside it. No source
tree modification or email sent. Suggested email in detailed report;
recommendation is source-favorable with changelog improvements and pending
runtime validation, not an unconditional Reviewed-by.

## R-032: memcg per-node cacheline contention, v3 [1/2]+[2/2]

Date: 2026-10-23 PT. From: Joanne Koong.
Source: mbox(20261023-215056); 13 messages, v1-v3 and Shakeel
discussion; submitted base fcec4f4bcc1101dbd7e3aff267856b3bbfe128c6.
Status: SOURCE FAVORABLE, review coverage incomplete; no introduced
correctness bug proven. No unconditional take/Reviewed-by.

Mirror check on 2026-10-23 PT: mm-unstable
2bba28e98578de622ef307d00875aa8f8bca3d10,
committer 2026-10-22 22:13:38 -0700, less than 24 hours old.
mm-new 3fdcce698abd9193752ee89fb1a440cdceb1b74a, committer 2026-10-22
22:13:42 -0700. No stale-mirror alert. These timestamps do not
establish synchronization with gitolite. Touched preimage blobs match:
include/linux/memcontrol.h 69e1bcc67c588d2071a2cb64a5770458bd8ddaff;
mm/memcontrol.c a05d9a8baa1b6bb9f9d95397543105f781a9f205.
Entire fcec base tree history has not been reconstructed.

R-032/F1 SOURCE-SUPPORTED [1/2] performance improvement: moving the
cold group (orig_objcg/objcg_list) after read-mostly fields prevents
direct same-object pairing with hot lruvec heads on 64B caches.
Author-measured Skylake throughput: shmem 20-thread 4.74M->5.59M
pages/s (+18%), shmem 80-thread 7.94M->8.66M (+9%), anon 20-thread
3.04M->3.08M (+1%). No independent benchmark/perf c2c reproduction.

R-032/F2 SOURCE-SUPPORTED [2/2] equivalent accounting: tracked and
untracked folio/kmem routes still update global node once and the
appropriate memcg/per-node state when tracked. Non-dying ancestor
redirection, outer RCU protection and reparent child/parent totals
retained. A 96-case synthetic accounting and 20-case reparent model
ran with equal old/new outcomes; this is NOT a kernel test or proof.
Incremental Skylake shmem gain author reports 5.59M->5.77M (+3%)
at 20 threads, and 8.66M->8.82M (+2%) at 80 threads.

R-032/F3 PERFORMANCE LIMITATION, NOT A PROVEN REGRESSION:
SMP_CACHE_BYTES / SLAB_HWCACHE_ALIGN supply 64B-aligned groups for
the described machine, not necessarily 128B-aligned slab objects.
A read-mostly line at offset 64 mod128 can pair with an adjacent
slab object rather than this object's cold line. Keep author claims
scoped to its own hot lruvec and measured CPU; optional comment edit
or field-offset/placement benchmark; no user-visible harm proven.

R-032/F4 UNRESOLVED dependency: old mem_cgroup_lruvec() can lazily
populate lruvec->pgdat. New stat-only routes no longer do so.
Representative vmscan get_lruvec() initializes it independently;
no failing consumer found, but all direct consumers not enumerated.
Do NOT call this a proven NULL-dereference regression.

R-032/F5 DISMISSED potential guard/root/race regressions:
mem_cgroup_from_virt() returns NULL when disabled, objcg lookup
remains under RCU, reparent uses the same nodeinfo positions,
and the generic mod_lruvec_state node/memcg update is unchanged.
No changed error/cleanup path or kernel/UAPI failure demonstrated.

Prior v1/v2 history: Shakeel Butt suggested the cold rearrangement,
requested an explanation comment, and acked both v2 changes. v3
adds the comment and his Acked-by tags. Joanne reports no reproduced
performance gain on arm64. Human acks not substituted for review.

Current guidance SHAs checked: Sashiko
d7c69ae77326a3ef39362897cdf0751a06068cf1; Tejun
cbb4478d0f73e15907335e70a2dc2fe54a9e7167; Chris
d048f8742f6740c38833adf02e87901412d771ca.
Seven manual Sashiko analysis domains and focused verification,
source-guided Tejun/Chris checks applied. No native Sashiko, build,
kernel tests, formal TLA+ check or actual perf experiment executed.
Guide/comprehensive caller/config coverage remains incomplete.

Standing rules: 57 of 73 applied; 3 inapplicable; 13 unresolved
Guard audit: 4 of 4 checked; 0 redundant; 0 unresolved.
Inventory assembled after independent review began, so precommit
requirement A03 is UNRESOLVED; no historical audit altered.
stable: not justified for performance-only change on this evidence.
Worst concrete userspace effect of OLD code is lower memory fault/free
throughput and elevated latency under reported Skylake contention.
No observed Oops, corruption, denial of service or exploit claimed.

Detailed Library report:
/Kernel Patch Reviews/reports/memcg-lruvec-cacheline-review.md
Next: inspect full lruvec pgdat consumer set, real layout/stride
and Intel c2c data; run kernel builds and workload if available.
No kernel source edited; reply only drafted, not sent.

## R-033: memcontrol high_work on dying memcg

Date: 2026-10-23 PT. From: T.J. Mercier.
Subject: [PATCH] mm: memcontrol: fix NULL pointer deref in
high_work_func() on dying memcg.
Base: 2bba28e98578de622ef307d00875aa8f8bca3d10.
Status: SOURCE FAVORABLE; real author-reported kernel KASAN Oops
and old missing CSS lifetime ref verified from source; no
introduced patch regression proven. NOT unconditional Reviewed-by.

Mirror check: akpm/mm Google mm-unstable HEAD at base SHA,
committer 2026-10-22 22:13:38 -0700, checked 2026-10-23 16:01 PDT
(age 17h47m, NOT stale). Preimage matching base Git tree blob
mm/memcontrol.c a05d9a8baa1b6bb9f9d95397543105f781a9f205.
Google HTML source-view reports a different blob
(aad0498a7bd6587a16df117b2a21fddef9e3798d), with minor
preexisting stock css_put changes and shrinker init; reviewed
high worker and CSS lifetime functions are identical. No mirror
synchronization with gitolite inferred from timestamp alone.

R-033/F1 CONFIRMED OLD DEFECT: high_work_func() performs reclaim_high
without CSS reference. CSS release can unhash MGLRU list before
worker's shrink_lruvec / lru_gen_rotate_memcg; author supplies
KASAN GPF at NULL hlist pprev. cancel_work_sync in css_free is too
late to exclude prior css_released and shrink_many unhashing.

R-033/F2 SOURCE-VERIFIED FIX: css_tryget_online before reclaim
allows either acquired ref delaying CSS release (and shrink_many
unhash), or no work after CSS kill; css_put balances success.
Offline itself may proceed but does not release MGLRU list.

R-033/F3 SOURCE-VERIFIED POLICY FIX: memory.high and swap.high reset
to PAGE_COUNTER_MAX at CSS offline. In try_charge_memcg non-task
context, old dead-child mem_high branch breaks before live parent;
the reset skips the dead child and continues ancestor checks.
Task-context obsolete swap.high delays are also suppressed.

R-033/F4 DISMISSED new ref leak or UAF: failed tryget returns
without css_put; successful tryget has matching put; final work
cancellation precedes memcg memory free; no new sleeping lock.

R-033/F5 UNRESOLVED runtime: complete kernel config/architecture,
teardown notifier, analog async work, full guide audit, kernel
build/KASAN stress and -stable target validation remain undone.
No source tree edit or email sent.

Current review guide pins: Sashiko
 d7c69ae77326a3ef39362897cdf0751a06068cf1; Tejun
 cbb4478d0f73e15907335e70a2dc2fe54a9e7167; Chris
 d048f8742f6740c38833adf02e87901412d771ca.
Seven Sashiko manual domains, verify and post-verify questions,
focused Tejun/Chris methods manually applied; native Sashiko NOT RUN.
Bounded Python scheduler model was RUN, corrected counts:
old 70 valid/15 unsafe; patched 65 valid/0 unsafe. An earlier
incorrect model criterion is superseded (35 old unsafe before fix).
This is NOT native TLA+/TLC, a kernel test, nor a formal C proof.

Standing rules: 27 of 40 applied; 2 inapplicable; 11 unresolved
Guard audit: 1 of 1 checked; 0 redundant; 0 unresolved.
Precommit inventory rule B01 UNRESOLVED. Full per-rule disposition
and separate incomplete coverage in detailed Library report.
Stable: candidate for kernels containing Fixes:
f1cf8d2f36dc369688bbe61ce064fbd829dbc9e1, not yet verified
on individual stable branches. Worst user-visible effect:
kworker Oops or panic/reboot with interruption of applications,
possible availability loss and unclean shutdown. Delegation or
proper cgroup/charge workload required to trigger, not presumed
unprivileged arbitrary memory corruption.

Detailed Library report:
/Kernel Patch Reviews/reports/memcontrol-high-work-dying-memcg-review.md
Next: KASAN MGLRU worker/offline stress and checks of live ancestor
high, PREEMPT_RT, -stable and analogous async memcg work.

## R-034: cgroup keyed selftest counters to s64

Date: 2026-10-23 PT. Author: Wilson Felipe Pereira.
Subject: [PATCH] selftests/cgroup: convert cg_read_key_*() helpers
         to s64. One standalone patch; explicitly rebased on mm-stable.
Status: SUPERSEDED - HOLD / RESPIN REQUIRED (R-034/F7 KVM build).
No proven introduced bug, no unconditional Reviewed-by; no native
Sashiko, full build or actual ILP32 kselftest execution.

AKPM mirror freshness: Google mm-unstable at
2bba28e98578de622ef307d00875aa8f8bca3d10, committer
2026-10-22 22:13:38 -0700, checked 2026-10-23 ~16:15 PDT;
under 24 hours old, so NO STALE-MIRROR ALERT. Author's specified
mm-stable HEAD is 2967f3ccdb5fae956f1b085370ec292bab5c7e25
(committer 2026-10-12 21:29:59 -0700). The older mm-stable
branch is explicitly selected; its age does not prove mirror stale.
All 8 submitted preimage blobs match both mm-stable and
mm-unstable at those SHAs; no branch conflict for the 8 files.

R-034/F1 CONFIRMED OLD WIDTH DEFECT: cg_read_key_long() returned
signed long and used atol(). On ILP32, counters exceeding LONG_MAX
cannot be represented, creating false failures/test judgments.
No running 32-bit kselftest reproduction claimed.

R-034/F2 SOURCE-VERIFIED FIX: keyed read/poll, expected value,
values_close and values_close_report, six test programs' 64-bit
destinations and print format strings converted consistently.
All C files remaining in the cgroup test directory checked for old
helper references; none found. Error sentinel and poll cleanup remain.

R-034/F3 NONBLOCKING TYPE NARROWING: test_cpu.c retains
`long delta;` in overprovision_validate() while both usage operands
are now s64; GCC -m32 and Clang i386 compile probes issued expected
narrowing warnings. If a usage difference exceeded 2^31-1 usec on
ILP32, the comparison could spuriously fail. Caller runs for only
10 seconds and ordinary 32-bit CPU counts cannot produce the
necessary difference. Suggest `s64 delta` for completeness, not a
proven practical blocker or new user-visible regression.

R-034/F4 CHANGELOG ACCURACY: saying atol() overflows and
"wraps into negative numbers" is not a portable assertion. A native
LP64 glibc overflow probe saturated at LONG_MAX with errno ERANGE.
Say values above LONG_MAX cannot be represented and may cause false
results. `cpu.stat` values are microseconds, not bytes.

R-034/F5 DISMISSED: no missing old API calls in other cgroup C
files; %lld matches signed long long; no changed resource lifetimes,
locks, work or ABI. Existing cg_read_long() on single-key fields
retains ILP32 limitations but is beyond the explicitly narrowed
multi-key fix. Extreme s64 arithmetic overflows not reachable in
reviewed fixed-duration test use cases; not a proven new bug.

R-034/F6 USER IMPACT: 32-bit cgroup kselftests can give erroneous
results on large counters; flaky/false CI reports can delay a valid
kernel change or obscure a real defect. No kernel runtime effect,
Oops, corruption or security exploit shown. stable: not applicable;
tests-only change.

Pinned methods (checked 2026-10-23): Sashiko
 d7c69ae77326a3ef39362897cdf0751a06068cf1; Tejun
 cbb4478d0f73e15907335e70a2dc2fe54a9e7167; Chris
 d048f8742f6740c38833adf02e87901412d771ca.
Applied all seven Sashiko manual domains plus verification and
post-verification, relevant current selftests/build/technical and
false-positive guides, Tejun evidence/review and Chris core checks.
Native Sashiko NOT run. GCC/Clang freestanding ILP32 width probes
were executed; native glibc overflow probe was executed; no actual
ILP32 libc or complete selftest build (32-bit libc headers absent).
No complete architecture/consumer external to cgroup suite audit.
Precommit rule inventory was not established before first source
analysis, so that procedural requirement is UNRESOLVED.
No production code edited and no email sent.

Detailed report:
/Kernel Patch Reviews/reports/cgroup-s64-review.md
Recommended email: take patch, optionally widen test_cpu delta and
replace changelog claim of negative wrap with unrepresentable-value
language. Hard-wrap drafted replies to <=75 columns.

## R-034: Tejun Heo review reconciliation and correction

Date: 2026-10-23 PT. Tejun mail dated 10:05:11 -1000,
subject Re: [PATCH] selftests/cgroup: convert cg_read_key_*()
helpers to s64. His mail identifies the review as Claude-generated.
Original R-034 favorable/takeable disposition is WITHDRAWN;
the previous disposition is retained above for historical context.
Current status: HOLD - DEFINITE LP64 KVM BUILD BREAK. Ask for respin.
The earlier R-034/F2 broad-completeness and R-034/F5 no-build-problem
assessments are superseded; old R-034/F1/F3/F4/F6 remain supported.

R-034/F7 CONFIRMED BLOCKER: `kvm/Makefile.kvm` includes the cgroup
library's make fragment; every common KVM test target links its
`cgroup_util.o`. KVM builds with `-I tools/include`; there
`linux/types.h` already declares `s64` as `int64_t` (= long on LP64),
whereas the patch adds `typedef signed long long s64` to the shared
`cgroup_util.h`. `cgroup_util.c` also includes clone3_selftests.h,
which includes linux/types.h; `access_tracking_perf_test.c` includes
both KVM types and cgroup_util.h. GCC and Clang LP64 compile-only
probes BOTH fail with incompatible typedef diagnostics. Real full
KVM selftest build was not executed; build graph and exact header
and compiler evidence establish the defect. Use `int64_t` together
with PRId64 formats (or equivalent compatible API), then build KVM.

R-034/F8 CONFIRMED INCOMPLETE CONVERSION: `cg_check_freezetime()`
returns s64 but test_freezer.c's `time_simple`, `time_populate`,
`time_migrate`, `time_parent`, `time_child`, and `time_nested`
consumers still use long values and %ld. On ILP32, 64-bit values can
be silently narrowed. No large frozen-time live repro executed.
R-034/F3 long `delta` in overprovision_validate() was already
caught in the initial review; independently reconfirmed by Tejun.

R-034/F9 REBASE DEPENDENCY: author mm-stable/mm-unstable preimages match;
this does not imply compatibility with the separate cgroup tree.
The verified commit eb69e955de7b touches test_memcontrol.c
`tcp_client()` and shared test helpers and conflicts semantically
with the submitted hunks. Tejun also observes the mm-stable zswap
predependencies missing from then-mainline. Exact v7.4-rc1
application/rebase was not executed; determine integration tree
at the next respin.

R-034/F10 LOW PRIORITY: the two unrelated blank-line removals and
misaligned test_zswap format continuation are valid cleanup issues.
Tejun independently confirms F4: glibc atol saturation instead of
portable negative wrap; memory counters use bytes, CPU counters
microseconds, events counts. cg_read_long/_fd remain 32-bit on ILP32,
which was identified earlier but excluded from the narrow keyed
helper conversion. No absolute proof that ALL tested workloads can
never exceed LONG_MAX on a 32-bit machine was provided.

ROOT CAUSE OF OUR MISSED BLOCKER: the review searched only cgroup
selftest-local callers and only compiled ILP32 narrowing probes.
It failed to enumerate linked KVM users, namespace conflicts in
transitively included headers, all freezer return consumers and
parallel cgroup-tree changes. Reading Tejun's or Sashiko's prompts
did not mean those steps were executed. The workflow now requires a
whole-tree shared-interface/build-dependency ABI gate.

Executed THIS feedback audit: source-checked KVM Makefile and header
chains, freezer consumers and cgroup conflict commit; GCC/Clang LP64
typedef-conflict probes both failed as predicted; GCC/Clang ILP32
narrowing probes warned. No complete KVM build, 32-bit runtime,
native Sashiko, git apply to v7.4-rc1 or kernel boot was run.

Detailed feedback audit:
/Kernel Patch Reviews/reports/r034-tejun-feedback-review.md
Updated earlier detailed report:
/Kernel Patch Reviews/reports/cgroup-s64-review.md


## R-035: mm/ksm: keep soft-dirty when merging a page (v3)

Date: 2026-10-23 Pacific. Continuing R-015; new gate-v2 review.
Source: `mbox(20261024-050607)` with twenty messages.
Author Samarth Narang; v3 Message-ID:
<20261021182157.1873726-1-samarth.colleges@gmail.com>.
Reviewed-by: Lance Yang (message 1, external endorsement for v3).
Base `fcec4f4bcc1101dbd7e3aff267856b3bbfe128c6`.
`mm/ksm.c` preimage blob
`dbfb8f98b18925c729d0931760a18f491d0fb156`, matching
both author base and prior mm-unstable SHA `2bba28e98578...`.
`Fixes: 0f8975ec4db2` verified at full SHA.

R-035/F1, SOURCE-FAVORABLE: Ordinary KSM replacement PTE loses an
existing positive soft-dirty bit in the old path; the new conditional
copies the old bit into the new PTE before PTL-protected installation.
No new rmap, reference, locking or failure-path effect identified.
`write_protect_page()` captures the bit and `replace_page()` does
`pte_same()` before replacing; pagemap reads it as userspace-visible
soft-dirty status. Worst consequence of old false negative: an
incremental checkpoint can omit a changed page.

R-035/F2, NO NEW REGRESSION: x86 KSM zero-page construction already
calls pte_mkdirty, setting SOFT_DIRTY and potentially causing a
false positive despite the original PTE being clean. The v3 does not
introduce or worsen it. The zero-page blocker previously proposed
in R-015 was withdrawn after David's over-reporting assessment.

R-035/F3, SEPARATE TRACK: The earlier combined v1/v2 UFFD/RWP
unmerge regression remains documented as R-015/F5-F6. V3 drops
those modifications at David's request; Lance undertook follow-up.
Do not attribute the old RWP problem to v3.

R-035/F4, VALIDATION: GCC and Clang UBSan source-mirrored 2,048-case
Boolean PTE model both executed successfully; baseline false
negatives/positives 512/512, v3 0/512. This is not a kernel build,
actual KSM test, or runtime architecture test. No native Sashiko,
no full formal checker run. Sashiko/Tejun/Chris current SHAs
`d7c69ae77326`, `cbb4478d0f73`, `d048f8742f67` respectively.

R-035/GATE v2: **HOLD**. Ran `new` before source analysis, recorded
21 evidence gate categories, one diff hunk, 24 coarse sections; BUT
passed `--source-ref` as descriptive text, not a pinned 40-character
SHA. Gate `check` executed and failed with exit 2. The subsequent
source inspection and compiler model do not retroactively repair
an invalid initial manifest. No acceptance recommendation is issued.
Also incomplete: refreshed live Google `mm-unstable` branch verification
(Gitiles direct calls failed); whole-tree checkout/search and full
caller/config checks; kernel build/reproduction; complete precommitted
standing-rule inventory. The Oct 22 22:13:38 PDT previously verified
mirror HEAD was 23h54m old around Oct 23 22:07 PDT, but current HEAD
could not be refreshed; do not claim new gitolite synchronization.

Coarse gate-section inventory: 0 of 24 recorded applied, 0
inapplicable, 24 unresolved. This is not a full standing-rule audit;
that denominator was not properly committed at preflight. No claim
of review completeness or execution of native Sashiko is made.

Full report: `/Kernel Patch Reviews/reports/ksm-softdirty-v3-r035-review.md`.
Gate manifest `/mnt/data/r035-gate.json` and actual check output
`/mnt/data/r035-review/gate-check.txt` are included in this turn's
ZIP. Workflow unchanged. Proposed reply is informational, not a
Reviewed-by or take recommendation; no email was sent.


## R-036: lib/group_cpus: snapshot cluster masks to keep grouping hotplug invariant

Date 2026-10-24 Pacific. Author Vishal Badole; submitted v4
2026-08-26; 1 file 85 insertions/2 deletions, 5 hunks.
Source: last known AKPM mm-unstable
`2bba28e98578de622ef307d00875aa8f8bca3d10`; original
`lib/group_cpus.c` blob `e6e18d7a49bba6775e5984db681637c826ef1dec`
matched submitted `index` prefix. Current live Google mirror HEAD could
not be refreshed and the last observed SHA is >24 h old: freshness
UNKNOWN, not asserted in sync. Fixes commit full SHA verified as
`89802ca36c96b324829996ef05013f82ecc9b68a`.

F1 SOURCE-PROVEN, UNFIXED: Snapshot starts unavailable if a device is
first probed with some present CPUs offline, selecting sibling/plain
spread. At subsequent all-online recomputation it switches to frozen
cluster spread. Four-CPU/two-queue reduced source model reproduces
0x03/0x0c -> 0x05/0x0a. Invariant fails on this case; not a new
regression relative to the original online-dependent algorithm.

F2 SOURCE-PROVEN, UNFIXED: Even after snapshot, final grouping uses
`topology_sibling_cpumask()` in `grp_spread_init_one()`. x86 CPU
offlining removes the dying CPU from remaining sibling masks. On a
shared-L2 topology with two 4-thread SMT cores and two queue groups,
all-online 0x55/0xaa becomes 0x2b/0xd4 when CPUs 2/4/6 offline.
GCC+Clang reduced model reproduced; Intel Knights Landing supplies
physically relevant shared-L2 multi-SMT-core topology. Not a newly
introduced bug, but a material hole in stated invariance.

F3 SOURCE-PROVEN NEW MODE DEPENDENCY: New `cpus_read_trylock()` and
snapshot allocations may fail even when all present CPUs are online,
using plain grouping; later capture success switches to cluster mode
without any CPU online changes. Source model eight-CPU/two clusters
0x33/0xcc -> 0x55/0xaa, reproduced GCC+Clang. Prior cluster
algorithm had separate allocation-failure fallback, but this adds
new failure sites, including CPU hotplug lock contention. Exact NVMe
IRQ-loss consequence requires runtime reproduction.

F4 SOURCE RISK: `cluster_snapshot_ready` is sampled separately for
each NUMA node/stage, not once across `group_cpus_evenly()`. A
concurrent or later successful capture after a prior failure can
combine plain/cluster grouping within one call; no runtime race
reproduction was performed.

Dismissed: no evidence of published-snapshot UAF/torn initialization.
The mutex serializes publication and the cpus_read_trylock pins
cluster source masks; store-release/load-acquire publishes pointer.
Failed per-CPU allocations unwind using zero-initialized array.
CONFIG_SMP=n excludes new code; HOTPLUG_CPU=n trylock stub succeeds.
Memory footprint increases O(nr_cpu_ids^2 bits). Hotadded CPUs not
covered is disclosed scope limitation. All added guards audited for
reachability, necessity and fallback consequences.

Userspace: the reported original s2idle regression causes NVMe queue
interrupt delivery mismatch, timeout-polled completion and about
2-minute stalls/sluggish I/O. F1-F3 produce demonstrably divergent
CPU/IRQ group masks; whether the specific new modeled scenarios cause
actual NVMe timeout has not been confirmed. Worst plausible stalled
storage I/O/hung processes until timeout; no corruption demonstrated.

Gate v2 initialized BEFORE analysis with full SHA, 23 gates, 5 hunks
and 24 standing sections. GCC and Clang reduced C models executed;
not actual kernel build, IRQ/NVMe runtime, native Sashiko, external
subagents, TLC/PlusCal, or full pinned whole-tree grep. Current mirror
refresh failed. Sashiko/Tejun/Chris SHAs: `d7c69ae77326`,
`cbb4478d0f73`, `d048f8742f67`. Native gate check: HOLD (missing
mandatory source/build/architecture and formal evidence); therefore
NO take or Reviewed-by recommendation. Source findings independently
support requesting v5. Detailed report uploaded and read back from Library path
`/Kernel Patch Reviews/reports/group-cpus-snapshot-r036-review.md`;
workflow itself unchanged.

## Work-mode transition note (2026-10-24; not a new review)

The next chat is intended to run in ChatGPT Work. Attach the three
master context documents `akpm-patch-review-workflow.md`,
`review-activity.md`, and `kernel-git-access.md`, and the executable
`akpm-review-gate.py`. Attach `pull-sumary.md` when doing pull summaries.
Read and enforce these at the beginning of the new Work session.

Read-only direct HTTPS Git, source history and Linus's current branch
were demonstrated in an earlier Work session on October 24. DO NOT
assume that session's clone persists or that its tips are still current.
Prefer Google's MM mirror, independently compare the public kernel.org
MM refs and use authenticated Gitolite only if it becomes reachable and
authorized. `mm-unstable` is the default patch-review source unless an
explicit base overrides it. Verify every relevant diff preimage and
record immutable SHAs before analyzing source.

For each *new* review, run `akpm-review-gate.py new` after validating the
exact source SHA and BEFORE reviewing source; keep the original manifest
and receipts. Complete the independent first-principles, applicable
Sashiko, Tejun and Chris, and later adversarial passes. Run `check` and
include the exact gate result. Missing/failed evidence means HOLD; no
acceptance or Reviewed-by recommendation. Work must actually invoke
these tools: merely loading a Markdown file does not invoke the gate.

Latest numbered review R-036 is HOLD. R-035 is HOLD for invalid initial
gate manifest despite favorable limited source findings. R-034 remains
HOLD due to a confirmed LP64/KVM typedef conflict and six missed
freezer caller conversions; the original favorable verdict was retracted.
The R-036 kernel/IRQ model counterexamples were not demonstrated on
real hardware. Refer to detailed per-patch reports indexed above.

Unnumbered OCFS2 discussion (not a completed gated patch review):
Joseph Qi's `[PATCH 1/6] ocfs2: read the xattr entry hash before
 defragmenting the bucket` was assessed as likely behavior-preserving:
rehashing slot positions after an unstable same-hash sort does not
change the observed hash when the bucket was already hash-sorted.
The distinct pre-existing retry-after-defrag issue may select a
same-hash entry at the displaced `xs->here` slot and could corrupt
xattr values; actual reachability and a kernel reproducer remain to
be established. An earlier suggested `Fixes:` candidate should be
verified using complete Git history and blame before use, not trusted
as a confirmed attribution. Do not assign a new review ID or a take
recommendation to this discussion.

`pull-sumary.md` consolidates hotfix email and signed-tag series
summary rules. Read it only when preparing pull-request text. No
repository tags, sends, pushes or production edits were authorized.


## R-037: FAT failed-write truncation locking (2026-10-24)

Subject: [PATCH] fat: hold truncate_lock in fat_write_failed()
Author: Matheus Alves de Almeida. Submitted message ID:
`20261021162105.62525-1-matheus.aalmeida@inf.ufrgs.br`.
All seven messages in the supplied mbox were read. One hunk, two added
lock operations. Review source: freshly fetched mm-unstable
`d10295141a98938a767234e73d45b954a69c9a2f`, matching public
kernel.org at 2026-10-24T22:54:05Z. Tip committer time 09:05:50Z.
Exact hunk preimage verified; author's complete blob was unavailable.

Disposition: HOLD. No regression found in the added lock, but the
mandatory executable gate cannot pass and kernel validation is missing.
No acceptance or Reviewed-by. R-034, R-035 and R-036 remain HOLD for
all previously recorded reasons; none is reopened or silently changed.

F1: correct Fixes attribution for the demonstrated FIBMAP race to
`16fab2015099a937e1a771f2785c5dd3445fe483`, whose subject is
"fat: permit to return phy block number by fibmap in fallocated region".
The submitted 459f6ed3b8c7 introduced the helper, but the old lookup
remained EOF-bounded. The 2016 change admits allocated space past EOF.
Full history, parent comparisons, blame and v4.4/v4.5 ancestry checked.

F2: changelog lacks user-visible impact. A failed/short extending write
can cut the FAT chain while FIBMAP walks an offset admitted by old
i_blocks. This can emit "request beyond EOF", return a false hole and
set the filesystem read-only by default; errors=panic can panic. A
three-actor source/model trace also follows a reused cluster into another
file's chain. These are source/model findings, not observed kernel
failures or demonstrated on-disk corruption. FIBMAP needs CAP_SYS_RAWIO.

Pedro's page-cache concern was independently rechecked and rejected:
ordinary reads are bounded by i_size, and the containing partial cluster
is retained. Three cleanup callers, other truncation/eviction users,
DIO/AIO, nested expansion, flush/writeback, swap/ecryptfs and JBD2 paths
were traced. All seven manual Sashiko domains, both verification stages,
pinned Tejun/Chris coverage and a separate same-model adversarial pass
were performed. No native Sashiko or external reviewers ran.

Pins, unchanged from the prior checkpoints:
Tejun `cbb4478d0f73e15907335e70a2dc2fe54a9e7167`;
Chris `d048f8742f6740c38833adf02e87901412d771ca`;
Sashiko `d7c69ae77326a3ef39362897cdf0751a06068cf1`.
Fresh remote checks were at 22:59:17..24Z. Vendored prompt differences
were read; identical guide reuse is hash-documented.

Actual verification: 18 bounded three-actor tla-mctj runs (six old fail,
six patched pass, six pre-2016 controls pass), three reference TLC checks
with matching outcomes, and a separate old wrong-mapping TLC failure.
TLC is 2026.10.15.145915, revision 932d35e. A compiled C arithmetic probe
passed 19,584,640 samples; its missing-bound mutation failed 4096 times.
No kernel race, lockdep or filesystem runtime test. Actual x86_64
configuration stopped at missing flex before FAT compilation.

The v2 preflight ran before analysis; original manifest preserved.
Its body-only classifier recorded no function symbol and rejects the
required all_callers search. Correct whole-tree searches are saved,
but cannot substitute for that receipt. Three initial pathless rg
commands failed and were corrected with successful git grep searches;
all failed receipts remain. The failed build receipt also remains.
Final executable check: HOLD, exit 2; nine audit issues across six
of 21 gates. Fifteen gates have no structural audit errors; H001 is
recorded and 22/24 coarse sections are applied, two unresolved. An
initial blank source-line anchor was corrected with the actual i_blocks
line; its original invalid receipt also remains. This does not change
the valid hunk preimage/source verification or permit acceptance.

Standing inventory: 40 precommitted obligations; 37 applied, 1 not
applicable (shared ABI), 2 unresolved (build/runtime validation and
executable gate). These delivery counts require successful artifact
saving, verified in the completed response. Guard audit: 0/0.
Stable: candidate after validation, changelog/Fixes correction and
mainline inclusion. No particular stable backport was tested. The
mm-nonmm-stable FAT allocation/rollback series does not include this
fix; no dependency on that series was established.

Detailed report:
`/Kernel Patch Reviews/reports/fat-write-failed-review.md`.
Supporting source/model/gate records: `fat-write-failed-evidence.tar.gz`.
Next: request the changelog/Fixes corrections; complete a FAT-enabled
build and runtime race/lockdep checks; address the gate's body-only-symbol
limitation through a supported gate update without rewriting this audit.
No kernel source edit, branch push, signed tag or email send.

Context correction from AKPM: the pull policy filename is
`pull-summary.md`, using the supplied attachment. The earlier
`pull-sumary.md` spelling in historical transition notes is a typo;
there is no instruction to retrieve that policy from GitHub.


## Unnumbered: filemap_invalidate_inode error report (2026-10-25 UTC)

Subject: filemap_invalidate_inode() - losing -EBUSY from
invalidate_inode_pages2_range?
Author: Saleh Mammadof. AKPM supplied the complete report, with no diff.
Disposition: reported invalidation-error loss CONFIRMED; no patch
acceptance verdict. R-034, R-035, R-036 and R-037 remain HOLD. No new
numbered patch review is assigned; no preimage/gate evidence was invented.

Current mm-unstable: a2abad0d7f453cc9902fc8bf7b871db5563a652c.
Google and public kernel.org matched, rechecked at 00:48:28Z/31Z.
A replacement complete bare clone was established in Work; 56 source
files matched their Git blobs. Whole-tree caller searches, blame,
parent diffs and release ancestry ran. Linus master was fetched from
public kernel.org at 6fba331225f5040e93d0947d1027e9712238291f;
the helper has the same discarded returns there.

F1: mm/filemap.c:4614 discards invalidate_inode_pages2_range()'s
return. filemap_check_errors() only consumes AS_ENOSPC/AS_EIO; the
invalidation refusal path does not set them. Thus -EBUSY can become
zero while a folio remains. A laundering callback's own negative
errno is also discarded, not necessarily translated to -EBUSY.

CIFS clears CIFS_INO_INVALID_MAPPING before invalidation and restores
it only on error. False success therefore loses its retry indication.
A buffered write can dirty an existing folio after the writeback pass;
CIFS revalidation does not take the write path's inode lock, and the
writer does not take invalidate_lock for that existing folio. This is
a source-reachable refusal witness, not an executed filesystem race.
Surviving old uptodate data can yield stale buffered reads. Direct/
strict-without-read-lease paths and cache=singleclient differ.

Btrfs's final invalidation is after cloning extents, not a pre-clone
abort. A particular refusal trigger under its existing guards remains
unresolved. Do not claim rollback or reproduced reflink corruption.
An early ENOMEM hypothesis was withdrawn: current extent-state clear
retries allocation failure despite the release helper's old comment.
Seven direct calls were checked, including Btrfs relocation, netfs DIO
and AFS. AFS already ignores the helper result; return propagation
alone does not change that caller. Netfs DIO completion also attempts
invalidation, so a surviving pre-write folio need not survive forever.

Correct Fixes for F1: c26096ee0278c5e765009c5eee427bbafe6dc090,
"mm: Fix filemap_invalidate_inode() to use
invalidate_inode_pages2_range()". That commit replaced void truncation
with the error-returning invalidator and discarded its result. It is
in v6.11, not v6.10. The separately ignored writeback return predates it:
74e797d79cf131d9b1a54001cf64a0b492a83e60 introduced that behavior in
v6.10. Current WB_SYNC_ALL retries ENOMEM; do not use a naive allocation
failure as proof of a separate writeback error. Preserve mapping-error
reporting/consumption and lock release in any proposed fix.

Independent pass, seven manual Sashiko domains, both verification
stages, pinned Tejun/Chris questions and a separate same-model
adversarial pass were recorded, including unresolved caller triggers.
Pins unchanged and freshly checked at 00:37:55Z:
Tejun cbb4478d0f73e15907335e70a2dc2fe54a9e7167;
Chris d048f8742f6740c38833adf02e87901412d771ca;
Sashiko d7c69ae77326a3ef39362897cdf0751a06068cf1.
No native Sashiko or external reviewers. No kernel build, runtime,
lockdep, xfstests or formal model. A compiled exact-helper/stub C probe
passed seven return/flag/lock assertions; this is not a kernel test.
Model decision: no, for sequential error propagation with no protocol
change. The mandatory patch new/check gate was not run without a patch.

Detailed report:
`/Kernel Patch Reviews/reports/filemap-invalidate-errors-review.md`.
Supporting records: `filemap-invalidate-errors-evidence.tar.gz`.
Next: obtain a focused patch with the corrected Fixes attribution and
a retained-folio/runtime regression test; run the complete patch gate
before acceptance. A validated fix is a stable candidate; no specific
backport was examined. No source edits, pushes, tags or email send.


## R-038: page allocation tag initialization, v2

Date: 2026-10-25 UTC. Author: Zenghui Yu (Huawei). Subject: mm/page_alloc:
mark pages freed by __free_pages_core() as not tagged Status: HOLD under
the mandatory evidence gate; source analysis found no introduced v2 runtime
regression. Continuation of R-021. Prior findings, errors and dispositions
remain intact; R-034 through R-037 stay HOLD.

Fresh mm-unstable: a2abad0d7f453cc9902fc8bf7b871db5563a652c. Google/public
kernel.org MM tips match at 03:23 UTC; base age under 24h. Queued change:
7429b17714d5984cd4918ce1f44ecfe5f800d223. Parent:
96b0bbc2cffab725866c118288cb883e977753f6. Parent forward and current
reverse apply-check pass, as does stable patch-id matching. Submitted
whole-blob prefixes differ; exact blob identity is not claimed. Linus
actual master 330517c63aa9b48227b6ab45f01003effac77ae4 and mm-stable still
have the old path.

Correct Fixes origin: dcfe378c81f72f146890ce1dcfdcc742d3b66924, "lib:
introduce support for page allocation tagging", in v6.10. d224eb0287fb is a
later incomplete boot-path fix and the tag already queued with v2. Backward
history through the real free hook establishes the earlier hotplug failure.
This supersedes R-021's limited attribution. Prospective Cc:
stable@vger.kernel.org is justified by debug onlining WARN/taint and the
panic_on_warn consequence; no corruption reproduced. Both current 6.12.y
and 6.18.y have the bug and pass forward apply-check. No tested stable
backport or mainline integration is claimed.

Correction to R-021: the head marker must precede lazy acceptance's early
return. __accept_page later calls __free_pages_ok directly. The earlier
advice preferring placement after the return was wrong. V2's one-head
granularity and placement survive all checked callers.

Seven manual Sashiko domains plus verification/post-verification, pinned
Tejun/Chris checks and a later same-model adversarial pass were performed
after the independent source pass. Native Sashiko and external reviewers:
not run. Method pins: Sashiko d7c69ae77326a3ef39362897cdf0751a06068cf1;
Tejun cbb4478d0f73e15907335e70a2dc2fe54a9e7167; Chris
d048f8742f6740c38833adf02e87901412d771ca.

Extracted tag-helper debug/nondebug probes passed 1152 scenarios and 18426
balanced tagged cycles. Old hotplug, late placement and v1 tail controls
failed as expected. Actual W=1 x86_64 affected-object builds passed with
profiling off/on/debug and enabled hotplug, deferred init and unaccepted
memory. Tool/target failures remain in the evidence. No full link, kernel
hotplug runtime, sanitizer or formal check ran. Model: no protocol change;
existing ownership excludes a third actor across lazy acceptance's lock
drop. LKMM: no new ordering claim. Guard audit: 0 of 0 checked; 0
redundant; 0 unresolved
Standing rules: 85 of 90 applied; 4 inapplicable; 1 unresolved

HOLD: 7 missing/invalid/unresolved checks - all_callers: missing evidence
kind whole-tree-search - standing_rule_inventory: S11 unresolved: Mandatory
impact-coverage gate, in ALL tracks - standing_rule_inventory: missing
evidence kind sections - test_and_build_scope: executed command failed -
test_and_build_scope: executed command failed - test_and_build_scope:
executed command failed - test_and_build_scope: executed command failed

Gate evidence: 21 gates; 46 registered receipts; 2 of 2 hunks.
Sections: 23 applied, 1 unresolved. Four failed command receipts
remain; later successful builds are recorded separately. Receipt
counts include repeated commands, not independent correctness proofs.

The original gate symbols=[] inventory and rejected all_callers attempt
remain unchanged. Manual whole-tree coverage cannot manufacture the missing
command receipt; failed build receipts also remain recorded. No acceptance
recommendation is made.

Separate existing C8: free_reserved_pages marks tails then frees one
high-order block, leaving EMPTY refs. Higher-order x86/s390 callers and
d79db3f39684 history are verified. The later missing-tag-allocation witness
needed for a lost diagnostic remains open. No v2 regression or corruption
claim is made from this finding.

Detailed canonical report: `/Kernel Patch
Reviews/reports/page-alloc-hotplug-tag-review.md`. Supporting evidence:
page-alloc-tag-v2-r038-evidence.tar.gz. Next: obtain a supported gate
revision without erasing original evidence, confirm v2 debug hotplug, and
revise Fixes/stable/changelog metadata. No kernel source edit, push, signed
tag or mail send was performed.


## R-038 follow-up: tools and delivery (2026-10-25 UTC)

AKPM's instruction: do not stop when flex is missing; find it and
continue. R-038 did obtain flex 2.6.4, bison, bc, m4 and libelf during
the same review, then successfully built the affected x86_64 objects
with W=1 in profiling-off, enabled and debug configurations. The first
missing-flex attempt is historical evidence, not the final build status.
No new build or hotplug runtime execution is claimed in this follow-up.
The staged tools remain under the R-038 build-tools/root directory in
this Work workspace; check their availability again before reuse.

The R-038 verdict, findings, Fixes/stable assessment, validation and next
actions were already added to this ledger. Sending the separate detailed
report as a routine download was contrary to the delivery preference.
Keep the substantive review result here and use the separate report as
a supporting record. The workflow now states tool recovery and ledger
ownership explicitly. No previous evidence or disposition is rewritten.

## Pull-summary singleton headings (2026-10-25 UTC)

Retrieved the latest mm-stable-summary.txt and
mm-nonmm-stable-summary.txt, both at saved version 2 before this edit.
Added one heading before each existing singleton roundup:

SUmmary of the 65 singletons in this merge:
SUmmary of the 87 singletons in this merge:

The requested capitalization is preserved. All existing series and
singleton prose is byte-identical after removing the inserted heading
and blank line. The totals cover every singleton in the respective
merge; the prose continues to omit trivial changes with no useful
runtime effect.

The historical comparison revision for these existing drafts is
5b0764a53235d3c77e1ed674e836e1b3fe1a4b1f. The exact tips are:

- MM: 183895979c441e52dbd651b388553b09eaa35cfa.
  213 commits, 24 series containing 148 commits, 65 singletons.
- Non-MM: b6232ca8d194c60ee603586e42b5ea584d4b7be9.
  134 commits, 17 series containing 47 commits, 87 singletons.

Counts were rechecked from Git and matched against every series heading
in the retrieved drafts. Shared submission IDs identify series without
cover text. The bootconfig cover says four patches, but only two are in
this non-MM merge range; the count uses those two, not the cover total.
These are the existing drafts' ranges, not a new merge against a moving
Linus branch.

AKPM flagged the attached pull-summary.md filename as wrong. No new
policy filename was inferred and no policy was fetched from GitHub.
The output filenames remain mm-stable-summary.txt and
mm-nonmm-stable-summary.txt. This is a documentation update, not a new
numbered patch review or a change to any HOLD disposition.


## R-039 - automatic interleave hotplug refresh (2026-10-25 PDT)

Subject: [PATCH] mm/mempolicy: recompute automatic interleave weights on
memory hotplug
Author: Gregory Price (Meta) <gourry@gourry.net>
Posted: 2026-10-24 13:04:15 -0400; single unnumbered-version patch.
Record: /Kernel Patch Reviews/reports/mempolicy-auto-hotplug-review.md
Disposition: HOLD/revise. No introduced runtime regression found; the
normal success path repairs the reported ratios, but configuration and
failure-path coverage remain incomplete. No author feedback yet.

Source and history:
- Fresh Google/public kernel.org agreement before/after fetch:
  mm-unstable a2abad0d7f453cc9902fc8bf7b871db5563a652c;
  mm-stable 183895979c441e52dbd651b388553b09eaa35cfa.
  Checked 2026-10-25 17:34-17:46 UTC; unstable committer time was
  2026-10-24 15:48:02 -0700, under 24 hours old. No Gitolite claim.
- Complete bare clone restored at
  /workspace/scratch/08622c88e80d/mm.git; non-shallow/non-promisor,
  final connectivity fsck passed. Old /2787927c495b clone was absent.
  A shallow bootstrap was used only while the full clone transferred.
- Actual Linus master fetched:
  21a7f44fd0765fcc5194130b28767786eba1d1e7.
- Exact mm/mempolicy.c preimage blob:
  0884c629670dd669bedd31ed2e29c9a5c1aaef29. All 3 hunks apply-check.
  In-memory postimage matches ffb293a4cc56. Kernel source stays clean.
- Fixes verified correct:
  e341f9c3c841 ("mm/mempolicy: Weighted Interleave Auto-tuning").
  Full SHA e341f9c3c8412e57fe0042a33a2640245ecdf619; absent v6.15,
  present v6.16. The older sysfs hotplug support is not the origin.
- stable: candidate after revision/mainline; retain existing
  Cc: stable@vger.kernel.org. 6.18.y at
  2926d88bb7fc4608fd942453d929c39e4e5ec006 remains affected and needs
  allocation/RCU helper adaptation. No stable build/backport was made.
- impact-changelog: needs a sentence on skewed application allocation
  proportions and possible bandwidth loss. No measured speedup claimed.

Findings (PENDING external feedback; source analysis is not endorsement):
- R-039-C1: the refresh callback and registration are inside SYSFS and
  successful sysfs setup. NUMA/HMAT/automatic allocation are not. A real
  SYSFS=n configuration compiles with the perf setter and allocator but
  without the notifier. It retains stale weights after re-online.
  A supplemental SYSFS=n build also enables ACPI_HOTPLUG_MEMORY and
  automatic onlining. Firmware eject uses device_offline(), and re-add
  uses __add_memory(); neither requires a sysfs write. Both ACPI driver
  objects build. This closes a gap in the initial config witness,
  which had core hotplug enabled but not the ACPI memory driver.
  Sysfs init failure also prevents registration. This is an incomplete
  repair of the old bug, not a newly introduced regression. Separate
  the core refresh notifier from optional sysfs setup before taking.
- R-039-C2: new notifier drops refresh -ENOMEM; successful hotplug can
  leave stale weights indefinitely. auto=1 is a no-op when already auto;
  a later event/report or 0->1 toggle is needed. Source and fault-injected
  extracted helper confirm it. Residual best-effort limitation, not new
  corruption. Request explicit handling/diagnostic; do not pretend
  returning failure from a success notification rolls hotplug back.
- R-039-C3: separate pre-existing reducer race, also originating in
  e341f9c3c841. Sysfs auto-store holds wi_state_lock but not the hotplug
  lock. Its first N_MEMORY scan can sum zero across unreported resident
  nodes; a previously removed node with saved positive bandwidth can
  rejoin before the second scan. The second scan then divides by zero.
  The hotplug notifier arrives after setting membership and cannot
  prevent this race. x86 can take a kernel divide error; panic_on_oops
  can turn that into a panic. Models and exact extracted C expose the
  failure in old AND submitted versions. No kernel crash reproduced.
  Keep as a separate fix; use a stable mask across passes or another
  justified serialization design, avoiding recursive hotplug locking.
- Dismissals independently checked: lock-drop does not overwrite manual
  state or use a stale bandwidth pointer; detached bandwidth ownership
  and RCU/SRCU retirement remain valid; success notifier ordering and
  sleepability are correct. No new data corruption or exploit claimed.

Executed validation and limits:
- Staged flex/bison/bc/m4 were found and actually used. Eight ORIGINAL
  x86_64 W=1 object builds passed: four objects with SYSFS=y and SYSFS=n.
  Two further ACPI objects passed with SYSFS=n and ACPI memory hotplug
  enabled, for ten original-source object builds in total.
  This is configuration/source-context validation, not patched-kernel
  compilation. Exact old/new helper extraction compiles with strict
  warnings and UBSan; all ten expected scenario outcomes checked.
- Three-actor PlusCal lock-drop model ran under native tla-mctj 0.1.2
  and TLC 2026.10.15.145915: fixed 1199 states, failure-enabled 1765,
  both depth 24, pass. Deliberately broken cached-state control fails.
- Two-actor membership model fails on live-mask code in both checkers;
  stable-mask control passes 25 states/depth 9. SC, bounded models;
  no RCU implementation/weak-memory/hardware proof. No herd7 required.
- No VM/hotplug runtime, full kernel link, arm64 build, native Sashiko
  or external reviewer. Complete applicable manual coverage used the
  same freshly verified Sashiko/Tejun/Chris SHAs as R-038; separate
  independent, guided, later adversarial and hard-case records retained.
- Gate new ran before source review; original manifest SHA256:
  a9ec6b0dae2d56412ff3abff2bb6d95a1115f986475b4a8ca22b91f54716a4ed.
  Original per-rule inventory retained, including an inherited R-021
  continuity reminder marked inapplicable to this unrelated review.
- Final executable gate check exited 0: ELIGIBLE_FOR_HUMAN_DECISION.
  21 requirements, 37 receipts (9 commands, 8 source, 20 analysis),
  3/3 hunks and 24/24 sections covered. This is structural evidence
  validation only; C1/C2 retain HOLD. No acceptance recommended.
  Earlier rejected hunk registrations and initial failed tool attempts
  are retained; no original receipt or frozen phase report was rewritten.
- Guard audit: 7 of 7 checked; 0 redundant; 0 unresolved.
- Standing rules: 86 of 90 applied; 4 inapplicable; 0 unresolved.
  A04: unrelated R-021 continuation; A33/A34: no changed shared ABI/type;
  A74: no new weak-memory claim requiring LKMM. These are coverage
  results, not proof the patch meets its functional goal.

Next action: author revision for independent core notifier registration,
explicit refresh-failure handling and impact wording; pursue C3 as a
separate reducer fix. No source edit, push, tag or mail authorized/run.
The workflow now explicitly checks whether reused notifier registration
and configuration match its added core responsibility. Existing R-034
through R-038 dispositions and all prior case records are preserved.


## R-039-C3 follow-up: standalone reducer fix (2026-10-25 PDT)

AKPM requested a patch for the separate reducer race. Draft:
mempolicy-stabilize-interleave-node-set.patch
Subject: mm/mempolicy: use one node set for interleave weights
This is development on R-039-C3, not a new numbered author submission.
R-039 and its C1/C2 findings remain HOLD, along with earlier HOLD cases.

The reducer now records exactly the nodes visited while summing their
bandwidth, then uses that set for scaling and GCD normalization. Changes
during collection are allowed; an atomic topology snapshot is unnecessary
for the arithmetic invariant. No allocation, new lock or error path.
The patch changes one function, 10 insertions/3 deletions, and has an
x86 divide-error/panic impact paragraph, verified Fixes and stable Cc.
Source edits were explicitly authorized by the patch request; isolated
worktree only, no commit, push, tag or mail. Sign-off fields are drafts.

Base: mm-unstable a2abad0d7f453cc9902fc8bf7b871db5563a652c, freshly
fetched and matched between Google/public kernel.org. Actual Linus
master 21a7f44fd0765fcc5194130b28767786eba1d1e7 also fetched.
Original mempolicy blob 0884c629670dd669bedd31ed2e29c9a5c1aaef29;
postimage 80c693c6d693602171b4f9db010bde18430b51bd.
Fixes: e341f9c3c841 ("mm/mempolicy: Weighted Interleave Auto-tuning").
Commit/parent provenance rechecked; introduced in v6.16.
stable: candidate after approval/mainline. The standalone diff applies
unchanged to v6.16 and checked 6.18.y, unlike Gregory's helper refactor.
Both orders with Gregory's patch produce identical source. No stable
kernel build or actual backport commit was made.

Executed validation:
- Three PATCHED x86_64 W=1 mempolicy builds pass: SYSFS=y, SYSFS=n,
  and 1024-node config. Largest mask is 128 bytes; no frame warning.
- Strict extracted C/UBSan compiles pass. 436,240 fixed scenarios agree
  with old arithmetic over a stable captured set; node 1023 also passes.
  Old divide-by-zero control fails as expected. An additional old-code
  control exposes weight 0 for a node entering only the final pass;
  the fix leaves unvisited slots at 1. This is the same C3 set mismatch,
  not a newly introduced defect or reproduced application corruption.
- New per-node PlusCal model: two actors, three nodes, bw 0..2, one
  resident node and two hotplug toggles. Native TLC and tla-mctj both
  pass 17172 states/depth 18. Old controls violate NoZeroDivisor.
  SC/bounded control-flow only; actual arithmetic checked separately in C.
- Forward apply checks pass on current checked MM/mainline, v6.16 and
  6.18.y. Checkpatch --strict: 0 errors, 0 warnings.
- Fresh Sashiko/Tejun/Chris pins unchanged; 51 previously read guide
  files verified, full applicable manual passes and later same-model
  adversarial check completed. No native Sashiko/external reviewer.
- No running-kernel crash/hotplug test, full link or non-x86 kernel build.

Guard audit: 2 of 2 checked; 0 redundant; 0 unresolved
Standing rules: 87 of 90 applied; 3 inapplicable; 0 unresolved
A33/A34: no changed shared interface/type or ABI; A74: no new weak-memory
claim. These counts describe checks performed, not gate eligibility.

Gate new ran on the draft before independent verification, preserving
the original manifest and all receipts. Its body-only classifier again
records symbols=[] and rejects genuine caller/consumer queries. Both
were separately executed with explicit repository roots and preserved.
Final gate result is recorded below; no acceptance recommendation.

Detailed history remains in:
/Kernel Patch Reviews/reports/mempolicy-auto-hotplug-review.md
Supporting archive: mempolicy-interleave-node-set-fix-evidence.tar.gz.
No new workflow rule is needed; existing rules cover this failure mode.

Final gate check: exit 2, HOLD. Of 21 requirements, two lack accepted
whole-tree-search receipts: all_callers and cross_tree_consumers. Both
queries ran successfully outside the gate, but its immutable empty
symbol list rejects registration. 28 accepted receipts (5 command,
4 source, 19 analysis), 2/2 hunks and 24/24 sections are recorded.
No patch, manifest or gate rewrite was made to manufacture eligibility.
No take/Reviewed-by recommendation. The patch is delivered as a draft.


## R-040 - move_pages query untagging (2026-10-25 PDT)

Subject: [PATCH] mm/migrate: untag addresses when querying page nodes
Author: Hungyu Lin <dennylin0707@gmail.com>
Posted: 2026-10-25 22:32:26 +0000; single unnumbered-version patch.
Record: /Kernel Patch Reviews/reports/move-pages-untag-review.md
Disposition: HOLD for acceptance; no introduced source defect found.
All finding feedback PENDING. No author/external confirmation claimed.

Fresh source and history:
- mm-unstable a2abad0d7f453cc9902fc8bf7b871db5563a652c, Google and
  public kernel.org agree before/after review. Tip over 24 hours old;
  user alerted before source analysis. Full non-shallow bare Git and
  staged flex/bison/bc/m4 verified; no Gitolite claim.
- Actual fetched Linus master:
  21a7f44fd0765fcc5194130b28767786eba1d1e7.
- Submitted blob 7e3a81f06974 exists. Pinned migrate.c differs only in
  unrelated comments; the one hunk applies unchanged. Source stayed
  read-only and clean. No kernel edit, commit, push, tag or mail.
- Fixes verified: 057d3389108e ("mm: untag user pointers passed to
  memory syscalls"). Full 057d3389108eda8a20c7f496f011846932680d88.
  That commit enabled the ABI but omitted query mode; first in v5.4.
- stable: candidate after approval/mainline; retain existing stable Cc.
  Remote helper 428e106ae1ad first appears in v6.4. Earlier affected
  trees need branch-specific untagged_addr/context adaptation.
  Current MM/mainline and fetched 6.18.y source apply checks pass;
  no stable kernel build, runtime test or backport commit was made.
- impact-changelog: sufficient. Explicit aggregate return 0 wording
  would make the per-entry failure easier to diagnose.

Findings and userspace impact:
- R-040-C1: move_pages(nodes=NULL) can return 0 with status[i]=-EFAULT
  for a valid tagged pointer. The raw key misses vma_lookup even though
  the corresponding untagged address has a populated ordinary page.
  Mixed arrays can return real node IDs alongside these failures.
  NUMA placement discovery/verification is broken for affected entries.
  Application fallback, abort or performance effects depend on its
  error handling; none was observed. Query mode itself moves no page
  and writes no page data. No crash or corruption is established.
- R-040-C2: on RISC-V Sv57 with supported PMLEN16, a high VMA created
  before enabling masking can match the raw tagged value. Old query
  can then report that other mapping's node instead of the intended
  low mapping. Source chain and extracted two-VMA case establish the
  conditional wrong-node result; no RISC-V hardware reproduction.
- The submitted line fixes C1/C2 by normalizing with the target mm
  under mmap_read_lock before both VMA and page-table lookup. Caller
  buffer and target addresses have distinct ownership. Permissions,
  mm references, PTL lifetime, normal errors and compat path checked.
- R-040-C3: separate old remap_file_pages tagged-start omission can
  yield EINVAL for an otherwise valid ordinary shared-file mapping.
  Source-supported follow-up, not a defect introduced here. No kernel
  reproduction or dedicated Fixes attribution yet. The later pass
  visibly corrects its earlier no-sibling-found statement. Keep separate.

Executed validation and limits:
- Two ORIGINAL x86_64 W=1 migrate.o builds pass with ADDRESS_MASKING
  off/on and NUMA_MIGRATION enabled. No patched-kernel build.
- Exact-body old/new query and wrapper extraction, with architecture
  definitions and mocked kernel infrastructure: 72,531 sweep cases
  plus explicit remote/disabled/alias/chunk/copyfault/compat tests pass.
  Old control returns 0/status=-14 and fails the expected-node test.
  First compile's unchanged sign-comparison warning is preserved;
  kernel-compatible suppression used; shift UBSan explicitly excluded.
- Corrected checkpatch --strict: 0 errors, 0 warnings. Initial missing
  Git-context warning preserved. Apply checks are source checks only.
- No tagged-address hardware/VM run, full kernel link or arm64 build.
  Full applicable manual Sashiko coverage, Tejun/Chris guidance and
  distinct later same-model adversarial pass completed. Native Sashiko
  and external reviewers were not run. Linked report inaccessible;
  its contents and endorsement are not credited.
- Fresh method pins: Sashiko d7c69ae77326a3ef39362897cdf0751a06068cf1;
  Tejun cbb4478d0f73e15907335e70a2dc2fe54a9e7167;
  Chris d048f8742f6740c38833adf02e87901412d771ca.
- Model: no, pure address normalization inside an existing lock, no
  new ownership/lock-drop protocol. Native TLC/tla-mctj availability
  verified, but no formal model or herd7 run claimed for this review.
- Gate new ran before analysis. Original manifest SHA256:
  96af0b8b0d0ff8a8e9e86b970fb2c56db8e7312077f7bd1b63e1da5e5c4565f0.
  Body-only hunk again produces symbols=[]; real root-wide queries
  succeeded outside the gate. Their rejected registrations remain.
  An initial integration query failed using a checkout without the
  fetched Linus object; corrected bare-repo query passed. Both remain.
- Guard audit: 4 of 4 checked; 0 redundant; 0 unresolved.
- Standing rules: 86 of 90 applied; 4 inapplicable; 0 unresolved.
  A33/A34: no changed shared interface/type or ABI. A73: no formal
  protocol trigger. A74: no new weak-memory claim. These are coverage
  counts, not acceptance eligibility or a proof of correctness.

Next action: address gate evidence limitations before acceptance; ask
for local/remote tagged-versus-untagged query regression coverage.
Pursue C3 separately with history and an arm64 shared-file test.
Workflow unchanged; existing rules already cover these findings.
Earlier HOLD dispositions and all original ledger bytes are preserved.


Final executable gate check: exit 2, HOLD; three checks remain:
- all_callers: missing accepted whole-tree-search receipt.
- cross_tree_consumers: missing accepted whole-tree-search receipt.
- parallel_tree: retained initial failed command, despite corrected
  successful query. The gate does not supersede failed receipts.
There are 33 recorded receipts: 18 analysis, 9 source and 6 command
(one failed command retained); 1/1 hunk and 24/24 sections recorded.
Real caller/consumer searches succeeded but cannot register against
symbols=[]. No original evidence or classifier was rewritten to pass.
No acceptance recommendation or Reviewed-by is given.
Evidence archive: move-pages-untag-r040-evidence.tar.gz.


## Gate maintenance: body-only symbol coverage (2026-10-25 PDT)

AKPM requested a fix for the evidence-gate classifier. Delivered gate
v3 in akpm-review-gate.py; this is tooling work, not a new kernel review.
The v2 detector considered only added/removed function declarations.
It ignored body-only enclosing functions, then refused caller receipts
whose subject was absent from its immutable empty symbol inventory.

The v3 new command requires --repo and reads the exact source-ref Git
objects. It verifies hunk preimages, resolves enclosing definitions in
old source and the in-memory postimage, and records helper-call symbols
for consumer searches. Header hints alone cannot invent a function.
Multiline signatures, renamed/new/deleted functions and unique hunk
line offsets are covered. --symbol H001:NAME provides an explicit,
source-bound supplement; unrelated identifiers are rejected. Unresolved
inventories still HOLD. This is a conservative inventory aid, not a
complete C parser or proof that caller analysis is exhaustive.

Validation:
- 30 executable regression tests pass. They include the old body-only
  failure, actual command receipts, incomplete/complete synthetic reviews,
  altered evidence, bad source/preimage/header/subject/manifest cases,
  failed compilation, mandatory report structure and section mappings.
- The actual R-040 and R-039-C3 patches each register caller and consumer
  searches successfully through v3: four real searches accepted. Four
  v2 controls reject the same subjects. Separate regression manifests
  retain HOLD for their other unpopulated review requirements.
- Historical R-038, R-039, R-039-C3 and R-040 check outputs and exits are
  identical under old and new checkers. v2 manifests are read-only in
  v3. All 76 hashed original manifest/input/receipt files are unchanged.
- R-038's proposed new v3 preflight rejects a mismatched preimage: the
  selected source already contains that change. This is a negative
  source-integrity check, not a new acceptance review.
- No kernel source change, Git ref push, signed tag or mail. Existing
  HOLD dispositions and the original R-040 failed integration receipt
  are preserved. The tool repair does not turn past reviews into passes.

The workflow documents --repo, explicit symbol supplements and the
separation between gate regression testing and a genuine new preflight.
Test source, logs and notes accompany the gate in
akpm-review-gate-v3-tests.tar.gz. The canonical gate filename remains
akpm-review-gate.py. No native Sashiko or formal model execution is
claimed for this Python tooling change.


## R-040 reply correction (2026-10-25 PDT)

The original emailable reply omitted two already-recorded findings.
AKPM requested that both be visible in the reply:
- R-040-C2: conditional silent wrong-node report on RISC-V Sv57 with
  PMLEN16 when the raw tagged value matches another VMA. The submitted
  patch fixes it. Source and extracted two-VMA evidence; no hardware
  reproduction. The revised email requests changelog coverage.
- R-040-C3: separate pre-existing remap_file_pages() missing untagging,
  producing EINVAL for a valid tagged arm64 shared-file address. Source
  inspection only; no kernel reproduction or verified Fixes attribution.
  The revised email asks for separate follow-up, without widening this
  patch or attributing the sibling bug to it.

The revised unsent draft is appended to move-pages-untag-review.md.
It supersedes the earlier email text but preserves that text for audit.
The now-stale gate-registration complaint is removed from the draft.
Original acceptance HOLD, finding feedback and all receipts remain.
No new review, runtime test, kernel edit or mail sending is claimed.
Workflow updated: include materially different failure modes and
source-supported sibling bugs in the email, with evidence limits.


## R-041: hugetlbfs F_SEAL_EXEC setattr review

Disposition: HOLD / needs revision. The reported bug is real, but the
new read of info->seals reaches an uninitialized mount-root field.
This review does not give an acceptance recommendation or Reviewed-by.

R-041-C1, existing bug: a hugetlb memfd carrying F_SEAL_EXEC still permits
execute-bit changes through chmod. A non-executable MFD_NOEXEC_SEAL file
can regain those permission bits. On Work's running x86_64 Linux 6.18.55,
the focused zero-length hugetlb memfd test changed 0666 to 0777. The
equivalent shmem case returned EPERM. Explicit F_ADD_SEALS cases gave
the same contrast. No huge pages were allocated, file data executed,
sysctls changed, or full upstream memfd selftest suite run.

R-041-C2, introduced regression: hugetlbfs_setattr is also installed on
the directory inode operations. hugetlbfs_get_root leaves info->seals
uninitialized, unlike hugetlbfs_get_inode. The common allocator and VFS
initializers do not initialize this member. A reused cache object can
retain F_SEAL_EXEC. Changing a mount root's search permission bits then
returns EPERM. Even an authorized owner/admin cannot perform that chmod
through this path. This can prevent tightening or loosening directory
access as intended. No kernel crash or data corruption is established.

Initialize seals for the root as well, preferably in an allocation path
which runs for every hugetlbfs inode. Do not put the reset only in the
one-time slab constructor. Its timing does not cover object reuse.
The extracted root-initializer/old-new-setattr test confirms the failure
with an injected retained bit; an initialization control succeeds.
The regression has not been reproduced on a patched running kernel.

## Source and history

GATE:base_and_preimage
Default-base preflight ran before analysis against mm-unstable:
1eb36316305767b54fac2cd40b88b3499791bdf2.
Google and public kernel.org mm-unstable/mm-stable tips agreed at entry.
The selected commit was less than 24 hours old. The old historical bare
clone was absent; a new complete, non-shallow bare clone was established.
Current mm-stable was 183895979c441e52dbd651b388553b09eaa35cfa.
Linus's actual master was fetched separately from torvalds/linux:
d135ab453a7400a34930bdda1ef4bdc8acfac80e.
Public kernel.org master agreed. No Gitolite access is claimed.

The cover letter subsequently supplied this explicit author base:
21a7f44fd0765fcc5194130b28767786eba1d1e7.
Its inode.c blob is 6656807ce437724c228daa3afa7a881bbf197067,
an exact match to the submitted index preimage. Separate actual apply
checks pass on that extracted base and on current mm-unstable. Current
mm-unstable has unrelated differences, including idmap constification;
its whole inode.c blob does not match the submitted index. The original
default-base manifest is preserved, not retroactively rebased.

GATE:parallel_tree
GATE:stable_and_integration
The helper is introduced in [04/16], "mm/shmem: honour F_SEAL_EXEC when
an ACL is set", by Chris Mason. It is absent from the selected MM base.
That is a normal series dependency, not an independent defect in [05].
The cover letter changes inode.c only through these eight added lines;
it does not include a root-seals initialization fix. The root path was
also inspected on the author's exact base and fetched Linus master.

Git history verifies the supplied attribution:
Fixes: 6fd7353829ca ("mm/memfd: add F_SEAL_EXEC")
Full commit: 6fd7353829cafc4067aad9eea0dc95da67e7df16.
It accepts F_SEAL_EXEC for memfd backends but adds the mode check only
to shmem. It is in v6.3 and not v6.2. The original omission starts there.
The stable rules were read from the current pinned source. A corrected
fix merits Cc: stable@vger.kernel.org: this restores a real user-visible
seal guarantee. Do not backport the submitted regression. Older trees
need the helper prerequisite or an equivalent self-contained check.
No stable-branch backport or build was executed, and no specific current
stable branch is represented as tested or integration-ready.

## Source analysis and guard audit

GATE:independent_source_pass
The preserved independent-pass.md preceded method reading. It correctly
identified the missing seal check and same-inode locking. Its blanket
ordinary-inode initialization statement is corrected by the later root
finding; the original text remains as an auditable intermediate result.

GATE:all_callers
GATE:cross_tree_consumers
Whole-tree searches enumerate hugetlbfs_setattr in both regular-file and
directory inode operation tables. chmod/fchmod/fchmodat go through
chmod_common, notify_change and this method. Generic VFS mode changes
can also reach it. Permission checks do not enforce the memfd seal.
fs/Kconfig selects MEMFD_CREATE with HUGETLBFS; fs/hugetlbfs/Makefile
builds inode.o into hugetlbfs.o. The prerequisite header supplies an
inline, architecture-neutral helper. No exported ABI layout changes.
The include and mode-check hunks are assessed separately below.

GATE:lifecycle_and_errors
Live inode and dentry lifetimes are held by VFS. chmod_common holds
inode i_rwsem through notify_change; memfd_add_seals takes the same
lock. The change allocates nothing, takes no new lock and drops none.
Successful mode changes use setattr_copy and mark_inode_dirty. Rejected
mode/size combinations return before hugetlb_vmtruncate or copying attrs.
setattr_prepare retains its existing permission/LSM behavior, so this
does not claim that every VFS error path has no possible side effects.
Object destruction returns storage through RCU and hugetlbfs_free_inode
to the same slab cache. That does not clear filesystem seals. Reuse is
the important inverse operation; lack of a reset invalidates C2 safety.

GATE:guard_audit
Four semantic clauses were audited, including the prerequisite helper:
G1 ATTR_MODE: size-only setattr has no valid ia_mode; skipping the mode
test is independently necessary. The finite test covers both branches.
G2 F_SEAL_EXEC: unsealed files must retain ordinary chmod behavior. A
sealed regular memfd is a valid witness, but the new root read is unsafe.
G3 changed 0111 mask: unchanged execute bits and read/write or special-bit
changes remain allowed. Individual execute-bit changes must be rejected.
G4 helper error return: propagates EPERM before mode/size updates. The
old control demonstrates that ignoring rejection permits the violation.
No redundant guard found. Four examined; one unresolved safety premise
(initialized seals for every inode) is disproved by R-041-C2.

HUNK:H001
Adding linux/memfd.h declares the helper introduced by [04/16]. Include
guards protect repetition; fcntl constants come from that prerequisite.
The gate classifies this include-only hunk as an unresolved function
inventory. Preserve that original limitation; do not manufacture a
function association or revise the precommitted manifest to pass.

HUNK:H002
The check is placed after setattr_prepare and before trace/truncate and
attribute copying. This is right for initialized regular-file seals,
but expands the read to mount roots. The needed initialization change
is missing. Merely passing the exhaustive scalar truth table does not
prove that the state supplied to the predicate is valid.

GATE:config_and_arch
With HUGETLBFS disabled the changed implementation is absent. Enabled
HUGETLBFS selects MEMFD_CREATE; that disabled-helper combination is not
realizable in this tree. The prerequisite helper is also outside the
MEMFD_CREATE conditional. umode_t and 0111 are word-size independent.
PMD-sharing layout differences leave seals outside the embedded inode.
Automatic slab initialization excludes this constructor-bearing cache.
No huge-page-size-dependent behavior or hotplug protocol is changed.

GATE:negative_verification
The separate adversarial report verifies the root finding and revisits
the rejected locking, privilege-bit, non-mode, config and NULL-ACL cases.
In particular, posix_acl_equiv_mode(NULL, ...) returns zero: the possible
NULL-ACL concern against [04/16] is dismissed, not reported as a defect.

GATE:similar_bug_search
The whole-tree seal/mode search and direct sibling inspection identify
shmem ACL mode mutation as the related pre-existing omission already
covered by [04/16]. Hugetlbfs provides no POSIX ACL setter in these inode
operation tables. This review supplies no new sibling-syscall bug count.
The earlier broad tagged-address ABI audit remains separate and pending.
R-040's prior candidate is not promoted to a confirmed ABI bug here.

## Method provenance and tests

GATE:sashiko_stages
Sashiko pinned current HEAD:
4e21ccac9066d5a8eadcf15b07464628450444a8.
Its Linux workflow defines goal, implementation, execution-flow,
resources, locking, security and hardware stages, with later verification.
This revision replaces the older vendored prompts with source notes.
Goal: enforce the existing seal across both memfd backends.
Implementation: predicate and placement work for initialized files;
root initialization violates the predicate's input contract.
Execution: caller dispatch, normal/error returns and combined attrs traced.
Resources: no new allocation; inode cache reuse reveals C2.
Locking: same-inode writers serialize; this cannot repair initialization.
Security: execute-bit immutability is the contract; no W^X claim follows.
Hardware: scalar predicate and struct initialization, not an MMU protocol.
Candidate verification uses real-source anchors and executable controls.
Native Sashiko was not run. Complete applicable guide coverage is NOT
certified: some long guide reads were truncated. This remains mandatory
unfinished work; seven-domain notes cannot stand in for that coverage.

GATE:tejun_method
Tejun pinned HEAD: cbb4478d0f73e15907335e70a2dc2fe54a9e7167.
Evidence discipline separates the runtime old-bug test from extracted
fix logic. The later adversarial pass challenges the supposedly safe
directory case and finds C2. Model: no, because the change is a scalar
check under existing inode locking, with no new ownership transfer or
weak-memory claim. Native TLC and tla-mctj help/version ran successfully;
no formal model was run. herd7 was unavailable and not required here.
Some applicable module reads were incomplete; full method completion is
not claimed. No external reviewers or subagents were invoked.

GATE:chris_method
Chris Mason pinned HEAD: d048f8742f6740c38833adf02e87901412d771ca.
Caller/locking/VFS checks were applied, including implicit ATTR_MODE,
setattr preparation and header/config dependencies. The search follows
initializers and inverse paths beyond the changed function. Long guide
reads were partly truncated; full applicable prompt coverage remains
unresolved rather than credited on the strength of this finding.

GATE:test_and_build_scope
Executed: actual old-kernel zero-length memfd test, exact extracted helper
and old/new setattr tests over 67,108,864 mode/seal/ATTR_MODE states,
combined mode/size rejection and size-only control, and ILP32 syntax.
Executed later: extracted root initializer with retained-seal input,
old success versus submitted EPERM, and explicit-initialization control.
These are finite executable tests, not TLA+/PlusCal or patched kernels.
No patched-kernel build, full kernel build, full memfd_test run or new
kernel boot is claimed. The first extracted compile failed because the
generator accidentally renamed a trace helper; its receipt remains.
After correcting the generator the build/test passed. The original
runtime script also encountered missing Python fcntl constants; the
successful script uses source-verified numeric constants instead.
No missing flex failure occurred in this review; an actual future build
should use the available staged tools rather than stop at PATH lookup.

GATE:userspace_effects
The old bug changes observable fchmod success/failure and permission
bits. It defeats the promised immutability of execute bits on hugetlb
memfds, including MFD_NOEXEC_SEAL. Actual executable-file loading was
not tested. F_SEAL_EXEC does not itself forbid executable mmap. Do not
claim arbitrary privilege escalation, kernel corruption or a W^X bypass.
The new regression makes an ordinary mount-root chmod intermittently
fail depending on recycled inode contents. Mention both in the reply.

GATE:emailable_verdict
The unsent email below reports the actionable regression and the old
runtime result. It keeps correct Fixes/stable advice conditional on a
corrected patch and names the existing helper dependency.

```text
This needs one more initialization fix. hugetlbfs_setattr() is also
used for directories, but hugetlbfs_get_root() does not initialize
info->seals. The allocator and inode constructor do not clear it.

A reused inode can therefore retain F_SEAL_EXEC, and the new check
can make chmod of the hugetlbfs mount root fail with EPERM when its
search bits change. Please initialize seals for the root too, or in
the common allocation path on every allocation.

I verified that path in the source and with an extracted-code test
using a retained seal bit, not on a patched running kernel.

The original bug is real: on 6.18.55, fchmod changed a hugetlb memfd
created with MFD_NOEXEC_SEAL from 0666 to 0777. The shmem control
returned EPERM. Please mention that loss of the execute-bit seal
guarantee in the changelog, alongside the selftest failure.

The Fixes tag is correct, and a corrected fix merits the stable Cc.
Backports need the helper from [04/16] or an equivalent local check.
```

GATE:report_and_ledger
Append R-041 to the latest recovered review-activity master, preserving
all prior bytes and HOLD dispositions. The workflow itself is unchanged.
Provide complete current copies of both masters, not a substitute review
document. Keep original preflight, failed receipts, tests and source
anchors in the evidence archive. Record the actual final gate output
separately; this text does not assert a passing gate or complete review.


### R-041 evidence and continuity checkpoint

Final pre-delivery gate check returned exit 2 (HOLD), with nine reported
issues: include-only H001 has no function inventory; the retained first
stable source anchor points at a blank line; S02-S05 method completion
is unresolved; S23 delivery was pending at check time; section evidence
is therefore incomplete; and the first failed harness compile remains.
A corrected nonblank stable-rule anchor was added without deleting the
original. The successful later harness build also remains alongside
its original failure. Neither issue is silently superseded.

There are 37 receipts: 19 analysis, 9 source and 9 executed command
receipts. One command failed. Both hunks have reports. Nineteen of
24 section statuses are APPLIED and five are UNRESOLVED at check time.
The 90-rule audit records 74 APPLIED, seven NOT_APPLICABLE, and nine
UNRESOLVED. Applied means examined, not that the patch is correct.

Four guard clauses were examined. The new seals read lacks a valid
initialization premise for mount roots. No acceptance or Reviewed-by.
The pending guide and target-backport checks remain necessary before
any later acceptance review. Successful saving after the check does
not retroactively alter that check's delivery status.

Final fresh Google/public kernel.org checks still agree on the pinned
MM tips. Original manifest and all receipts are preserved. Evidence:
hugetlbfs-seal-r041-evidence.tar.gz. Workflow bytes are unchanged.
All previous ledger entries and HOLD dispositions are preserved.

The tagged-address interface audit remains pending. Its remit is ABI
promises actually violated, not a raw count of untagging omissions.
No earlier candidate is promoted by this review. No kernel source edit,
Git ref push, signed tag, email, or patched-kernel run was performed.


## Unnumbered investigation: Boyer-Moore ignore-case misses

Date: 2026-10-26 PDT. Report from Lennart Finke, subject
"Bug in the Boyer-Moore search in lib/ts_bm.c".
Detailed report: /Kernel Patch Reviews/reports/ts-bm-ignorecase-review.md.
Supporting archive: ts-bm-ignorecase-evidence.tar.gz.

Confirmed bug; no submitted patch or patch acceptance. Current verified
mm-unstable is 1eb36316305767b54fac2cd40b88b3499791bdf2. Google and
public kernel.org MM tips agree. Linus master is
 d135ab453a7400a34930bdda1ef4bdc8acfac80e;
its ts_bm.c is identical. Existing non-shallow clone survived and both
MM and Linus were fetched. No authenticated Gitolite claim.

BM-ICASE-C1: with TS_IGNORECASE, comparison folds the text but the
bad-character lookup uses raw bytes. Kernel upper(ff)=df and
upper(df)=bf, while the lower-case aliases do not cover these raw keys.
For pattern ff,41 in 42,ff,41, original BM returns UINT_MAX instead of
1. The same holds with df. It can also skip the first occurrence and
return a later one: 4 instead of 1 in 42,ff,41,51,ff,41.

The proposed key normalization fixes all executed cases. Lower-case
aliases then become redundant; a submitted cleanup should also remove
compute_prefix_tbl's unused flags parameter. Do not change the global
ctype mapping merely to repair this local lookup inconsistency.

Userspace: xt_string exposes selectable BM with IGNORECASE. A missed
match skips a positive rule or spuriously satisfies an inverted rule;
final ACCEPT/DROP/logging effects depend on the configured ruleset.
No live packet-path test or universal firewall bypass claim. em_text
and the Amanda helper do not enable IGNORECASE. KMP controls pass;
FSM rejects IGNORECASE. This is separate from BM's documented inability
to match across blocks and from the existing resume-offset patch thread.

History verifies 3b76d08190e6b420ed3f5534aa99ee29d82d731f,
"textsearch: ts_bm: support case insensitive searching in Boyer-Moore
algorithm", first present in v2.6.27. A corrected upstream patch merits
that Fixes attribution and Cc: stable@vger.kernel.org. No stable-branch
backport build or patch acceptance has occurred.

Executed exact-source extraction with the actual kernel ctype table:
34,396,544 differential cases per run, covering all two-byte patterns
and preceding bytes in both modes, exhaustive short exceptional-byte
strings, and deterministic random offsets/block layouts. Original BM
has 132,801 disagreements; lookup-only and combined suggestions have
zero, as does KMP. Normal and unsigned-char runs pass. ASan/UBSan also
pass with leak checking disabled: the original LeakSanitizer run failed
because it could not inspect the Work process/task environment.
A separate later counterexample and all-byte alias-invariant test pass.
Its initial misleading-indentation compile error was corrected. No
kernel build, KUnit, module load, boot or kernel runtime test is claimed.

Model: no, deterministic mapping/skip invariant without a concurrency
protocol. No formal checker or herd7 execution. Later same-model
adversarial verification challenged the ASCII-only/block-boundary
excuses, non-idempotent folding, aliases, KMP, signedness and lifetimes.
One proposed added condition, TS_IGNORECASE, checked in both branches.
No native Sashiko, external reviewer, or complete method coverage claim.
Sashiko HEAD advanced to 104fc7f77fbdcbe565001b50c3ad0606dbab6614;
Tejun and Chris pins remain those recorded for R-041. Some guide output
was truncated, so full mandatory patch-review coverage remains pending.

Gate new ran before source analysis on the actual report, rejecting it
as having no parseable diff. No artificial patch/manifest was created.
A later check of the absent manifest failed (exit 1). Original rejection
and check logs are preserved. This confirms a bug report; any future
patch acceptance still requires its own genuine preflight and evidence.

Next action: ask for a patch with df/ff regressions and case-sensitive
and KMP controls. The unsent draft is in the detailed report. Workflow
now explicitly checks normalization consistency across comparison and
indexes/skip tables, including non-invertible/non-idempotent mappings.
The ledger header was brought current to R-041; all previous findings
and dispositions are unchanged. The tagged-address audit remains pending.


## R-042: F_SEAL_PUNCH_HOLE

Disposition: HOLD / needs revision. Two substantive findings: an omitted
live-update seal capability and an existing rollback race which defeats
the cover's stronger page-membership claim. No Reviewed-by is offered.

## Submission and base

Samiullah Khawaja, [PATCH 0/2] mm/memfd: add F_SEAL_PUNCH_HOLE,
Message-ID 20261026220546.3114241-1-skhawaja@google.com, 2026-10-26.
Both actual patches were reviewed, including all six selftest hunks.
The explicit base is 7bf01f16a4d05028fbeff4d90bab40df25142a24.
The unmodified, complete, non-shallow bare clone survived. Fresh Google
and public kernel.org MM tips agreed; actual torvalds/linux master was
queried and fetched. Exact observations are in refs.json and the final
freshness receipt. Historical checkpoints were not treated as current.

Both patches pass git apply --check against the stated base. Four of
five full preimage blob identities match the mail's index prefixes.
The hugetlbfs index prefix e8a05d3de327 is not in the fetched repository;
the base blob is ab1e4dec3f77b87c95fc324dd91a345cc041154e. The hunk's
actual old lines match and apply cleanly. This is a whole-file preimage
mismatch, not evidence that the changed lines fail to apply. Its exact
unsubmitted antecedent remains unknown. The author's separate hugetlbfs
SEAL-EXEC dependency does not constitute acceptance of R-041.

Original gate v3 manifests were created separately for [1/2] and [2/2]
before source analysis, and immutable copies are retained. The gate
cannot resolve the macro-only new-constant hunks. No evidence was
rewritten to manufacture a pass. Gate checks are preserved separately.

## R-042-C1: live update rejects the new seal

Confirmed integration omission in [1/2], still present after [2/2].
Severity: medium; a requested live-update operation fails cleanly.

include/linux/kho/abi/memfd.h:63 defines MEMFD_LUO_ALL_SEALS without
0x0040. mm/memfd_luo.c:283 rejects any unsupported seal with
-EOPNOTSUPP in memfd_luo_preserve(). The retrieve side makes the same
check at line 530. Adding the new bit to F_ALL_SEALS only changes the
fcntl acceptance mask; it does not change the live-update mask.

Concrete path, with CONFIG_LIVEUPDATE_MEMFD and an active LUO session:
LIVEUPDATE_SESSION_PRESERVE_FD -> luo_session_preserve_fd() ->
luo_preserve_file() -> memfd_luo_preserve(). A shmem memfd with
F_SEAL_PUNCH_HOLE is rejected. luo_preserve_file propagates the error
back to the ioctl; the serializer is freed and shmem_freeze is undone.
No silent seal stripping, resource leak or data corruption was found
on this rejection path. Hugetlbfs is not supported by this memfd LUO
handler: memfd_luo_can_preserve requires shmem_file and zero links.

The ABI header expressly requires adding supported seals and bumping
MEMFD_LUO_FH_COMPATIBLE, currently "memfd-v2". Update the mask and
compatibility handling together, with preservation/retrieval coverage.
Do not merely drop the unknown bit when serializing: that would lose
a userspace protection across the update.

Positive proof: the exact mask rejects every one of the 64 combinations
containing the new bit; the diagnostic amended-mask control accepts
those combinations. This is an extracted arithmetic check, not a live
kexec test. The existing whitelist is intentional forward-compatibility
protection. The omission is failing to extend it for the newly advertised
live-update use, not claiming that rejecting unknown seals was itself
an old bug. History: 8a552d68a86ef0e6fb2ff4af13031a5e82c0f1d0,
"mm: memfd_luo: preserve file seals".

## R-042-C2: ordinary fallocate rollback can detach an iommufd pin

Source-confirmed pre-existing race, not introduced by the new local
hole-punch guards. It invalidates the cover's claim that the two seals
alone guarantee continued file membership. Conditional userspace effect:
the device continues using a pinned folio while reads or new mappings
of the memfd see a hole or replacement folio. Device writes can therefore
be absent from the file, and file writes absent from the device buffer.
A future live-update optimization must not skip membership verification
on the strength of these seals alone. No live DMA, guest corruption or
kexec corruption was reproduced.

Concrete scenario: pre-size a sparse shmem memfd, then install both
F_SEAL_SHRINK and F_SEAL_PUNCH_HOLE. Use an ordinary fallocate range
inside i_size, so neither shrink nor hole punching is requested.

1. shmem_fallocate() holds inode->i_rwsem and allocates an order-0 folio
   through shmem_get_folio(..., SGP_FALLOC). A new folio is deliberately
   left !uptodate (mm/shmem.c:2751-2761), then marked dirty and unlocked.
2. The iommufd file mapping path reaches pin_memfd_pages() and
   memfd_pin_folios() without acquiring that inode lock. It obtains the
   folio through filemap_get_folios_contig() and try_grab_folio(FOLL_PIN).
   Neither checks uptodate, locks the folio, nor establishes continued
   page-cache membership. The lookup's ordinary reference protects its
   lifetime before the FOLL_PIN reference is acquired.
3. A later allocation in fallocate fails, or the fallocating task gets
   a fatal signal. shmem_fallocate() calls shmem_undo_range(..., true)
   for the prefix already instantiated (mm/shmem.c:3943-3951).
4. That undo removes !uptodate folios via truncate_inode_folio(), which
   calls filemap_remove_folio(). An outstanding pin does not prohibit
   removal. The pin holder retains the old folio, now outside the file.

The iommufd chain was traced through iommufd_ioas_map_file(),
iopt_map_file_pages(), iopt_map_common()/domain population,
pfn_reader_user_pin(), pin_memfd_pages() and memfd_pin_folios(). Its
IOAS and pages locks do not serialize with shmem_fallocate. A normal
ZONE_NORMAL folio can pass the long-term pinnability checks without
migration. CONFIG_MIGRATION=n also has a success-returning stub.
The case needs a populated hardware domain or another actual pinning
consumer; merely registering an IOAS with no pinning demand is not a
runtime reproducer.

All three in-tree memfd_pin_folios callers were considered. udmabuf
holds inode_lock_shared across its seal check and pin. memfd LUO holds
the inode lock across freezing and pinning. Those callers exclude this
particular concurrent-fallocate rollback schedule. Do not generalize
this race to them from the shared helper alone. A subsequent fallocate
on a previously fallocated !uptodate folio initializes it before undo,
so the important window is the initial, still-running fallocate.

History was checked: 89c1905d9c140372b7f50ef48f42378cf85d9bc5 introduced
memfd_pin_folios(); 92687c793644c01aa4ca961a5f2cb93ac20a27f0 introduced
the iommufd file pfn reader. These are verified historical origins,
not a finalized Fixes attribution for an unsubmitted correction.

## Formal model and counterexample validation

Model decision for [1/2]: yes for the stronger pin-membership claim.
The two local seal guards themselves are serialized by the existing
inode lock and need only a finite mask check. The uncovered multi-actor
rollback/pinning protocol required a separate bounded model.
Model decision for [2/2]: no separate model; sequential test helper
refactoring and syscall assertions introduce no concurrent protocol.

Native PlusCal translation and SANY parsing succeeded. Both native
TLC and tla-mctj found PinStillInFile violated in the submitted-tree
model. tla-mctj: 36 distinct states, depth 7; TLC: 44 distinct states,
reported search depth 9, an eight-state counterexample. Differences
in explored counts come from parallel exploration, not different
properties. Both diagnostic serialized-pin controls passed: 18 distinct
states, depth 10. Full logs and invocation times are preserved.

The model has two actors, one pre-sized shmem range, one fallocate
failure, and two possible folio identities. A lookup reference is
represented by the retained identity, not by a full refcount. Migration,
reclaim, DMA and the allocator are not modeled; the counterexample uses
an ordinary long-term-pinnable order-0 folio. The seal bits are already
installed, and ordinary fallocate is permitted in both versions.

The failing trace maps to actual C: FStart takes inode_lock; FAlloc
publishes a !uptodate folio; PLookup takes a page-cache reference;
PPin adds FOLL_PIN; FRollback removes the cache entry; PReturn retains
the pin. TLC also finds removal between lookup and pin, protected from
freeing by the lookup reference. There is no use-after-free claim.

The PinLock=true control represents taking the inode lock for pinning.
It is a diagnostic control only: no such kernel fix was written, built,
or checked for lock ordering. Do not interpret its 18-state pass as
verification of a kernel fix. Sequential consistency is assumed.
The failing schedule does not require weak ordering; no herd7 claim
is made. Formal tools were verified by actual execution in this turn.

## Hunk and guard review

[1/2] H001: hugetlbfs_punch_hole checks before partial zeroing, unmapping
or removing pages, while holding inode_lock. Its caller supports only
KEEP_SIZE/PUNCH_HOLE and the VFS validates regular file/write access.
H002: new UAPI bit 0x40 has no collision with existing seal bits;
LP64/ILP32 external-header consumers compile. H003: F_ALL_SEALS accepts
the bit while F_SEAL_SEAL and writable-fd validation retain their roles.
H004: the added comment describes the limited operation accurately.
H005: shmem_fallocate's new guard precedes all punch-side mutations and
exits through the existing inode unlock. MADV_REMOVE funnels into this
same vfs_fallocate path after retaining a file reference.

[2/2] H001: fallback define agrees with UAPI. H002/H003: splitting
mfd_assert_write preserves its original write/mmap/mprotect and punch
order. The variable r remains used by mprotect. H004: both new failure
checks demand EPERM; the mapping is writable/shared, so MADV_REMOVE's
preconditions are met. H005: the two tests distinguish PUNCH alone from
PUNCH|SHRINK; shrinking is intentionally allowed in the former. H006:
main invokes both tests. Hugetlb sizes use two actual hugepages, not
the shmem default. The old helper still exercises unsealed punching.

Added-guard audit: two new kernel bit predicates, both necessary and
reachable; zero redundant new kernel guards found. Also checked the
selftest's feature-definition guard and three error checks. The tests
could be stronger by retaining a writable mapping across seal addition
and verifying nonzero data survives a refused punch. That is suggested
coverage, not evidence that these local guards corrupt data.

## Manual guided coverage and negative verification

Independent source analysis preceded the current guided pass. Its
written note was saved after the first Tejun guide read; do not claim
that the written note predates every guide read. No external reviewer
or independent-model consensus is claimed. A separate later adversarial
pass challenged both findings and the substantive dismissals.

Pinned current methodology sources:
- Tejun: cbb4478d0f73e15907335e70a2dc2fe54a9e7167.
- Chris: d048f8742f6740c38833adf02e87901412d771ca.
- Sashiko: 104fc7f77fbdcbe565001b50c3ad0606dbab6614.

The Sashiko pipeline, current stage/verification definitions, callstack,
locking and false-positive guides were read. Chris core, technical,
callstack, false-positive, build, syscall, selftest, VFS, KHO, folio,
largepage and reclaim guides were considered. Exact differences between
Chris and Sashiko callstack/locking/false-positive guides were read;
they were not assumed identical. The current 7.3 shmem, hugetlb and
iommufd notes were checked against source where relevant. Tejun's
review, evidence, validation, wait, description, comments, cover-letter,
idiom and model rules informed the review. Source inspection used Git
and text tools, not semcode. Native Sashiko was not run.

GOAL: new opt-in seal is coherent as an operation prohibition; the
stronger live-update optimization claim fails C1/C2. No speedup was
measured and neither driver is changed by the submitted series.
IMPLEMENTATION: all hunks, masks, serialization and inverse operations
checked; C1 is the missed inverse consumer.
EXECUTION-FLOW: new EPERM exits release the inode lock without starting
mutation; allocation rollback exposed C2. Tests stop on unsupported new
seal on the old kernel, as observed; that is not a patch runtime pass.
RESOURCES: refs preserve lifetime but not cache identity. File refs keep
inodes alive; no new allocation or refcount changes in the patch.
LOCKING: existing inode locks serialize seal-add and explicit punch;
iommufd does not share the fallocate lock. No lock ordering changed.
SECURITY: writable-fd and seal permanence rules remain; no new writable
access grant, bounds arithmetic, or copy-to-user path is introduced.
HARDWARE: DMA can remain on the old physical folio in C2; no changed
register, IRQ, cache-coherency or barrier protocol. x86 LP64/ILP32 header
checks ran; no arm64/RISC-V kernel build or hardware execution occurred.

Challenge: does a pin prevent truncate, or does the contig lookup wait
for uptodate? Attempt: inspect filemap_get_folios_contig, try_grab_folio,
truncate_inode_folio, and all memfd_pin_folios callers. Result: C2 holds;
only udmabuf and memfd LUO have the relevant inode exclusion.
Challenge: does the existing-file fallocate initialization remove the
window? Attempt: trace SGP_FALLOC's new/existing distinction and rollback
bounds. Result: the first in-flight allocation remains !uptodate.
Challenge: does the new seal already reach the serializer? Attempt:
whole-tree mask search plus 128-combination executable check. Result:
C1 holds; [2/2] changes tests only.
Challenge: does a different operation already block MADV_REMOVE, or
is the new check redundant? Attempt: trace shared writable mapping to
vfs_fallocate and compare F_SEAL_SHRINK-only masks. Result: no; both
new predicates add a meaningful refusal.

Similar-path inventory includes truncate, explicit punch, rollback,
eviction, reclaim, hugetlb preallocation and internal GPU/XFS shmem
users. Internal helper search hits are not themselves confirmed bypasses.
The complete provenance/ownership audit of every GPU/XFS internal file
and a full cross-configuration kernel build remain incomplete; therefore
no exhaustive all-consumer or full mandatory methodology pass is claimed.
The tools/perf copied fcntl header also lacks the new printable seal name;
that is a follow-up header synchronization item, not this runtime bug.

## Executed checks and limitations

- Both original diff preimages apply-check successfully.
- Submitted selftest postimage hash matches 095c5eb255af exactly.
- Selftest compilation succeeds. Extra compiler warnings match baseline.
- On host kernel 6.18.55, existing shmem tests reach the new case, where
  adding 0x40 returns EINVAL and the test aborts as expected.
- All 128 seal combinations pass the extracted decision/control checks.
- Explicit -m64 and -m32 UAPI consumer compilations succeed.
- Native TLC/tla-mctj checks executed as described above.

No patched kernel build, boot, hugetlb runtime test, live DMA test,
kexec test, native Sashiko run or external review was executed. The
submitter's QEMU results are the submitter's report, not our execution.
Original failed/rejected tool calls and gate receipts remain preserved.

## Stable and integration

This is a new userspace API feature, followed by its tests. Do not add
Fixes or Cc: stable to this series merely because an old pinning issue
motivates it. A separate narrow correction for C2 needs its own patch,
verified introducing-path attribution, regression test and stable review.
C1 should be addressed before integrating the intended live-update use.
The separately posted SEAL-EXEC fix remains R-041 HOLD; this review does
not silently accept it as a test dependency.

## Standing-rule completion

APPLIED: current base selection and freshness; original preflights;
independent source pass; per-hunk and guard reasoning; both findings'
userspace effects; inverse/error-path investigation; bounded model and
failing/control runs; later adversarial verification; stable decision;
plain-ASCII unsent reply; preservation of earlier dispositions.
UNRESOLVED: macro-only gate symbol inventory; exhaustive reverse-consumer
coverage and cross-configuration kernel builds; full acceptance evidence.
Gate check must remain HOLD. A completed bug finding is not a completed
patch acceptance. No production kernel source was edited; no refs were
pushed.

## Executed final gate checks

Both checks returned exit 2 (HOLD). These include missing acceptance
evidence and gate limitations; they do not invalidate the two source
findings. Failed searches for newly added functions in the old base
are preserved as failed receipts, not described as runtime bugs.

Patch 1:

```text
HOLD: 17 missing/invalid/unresolved checks
 - all_callers: unresolved symbol inventory for H002
 - cross_tree_consumers: missing evidence kind build-graph
 - external_consumer_build: no receipts
 - external_consumer_build: missing evidence kind consumer-build
 - parallel_tree: missing evidence kind integration-search
 - shared_header_abi: missing evidence kind whole-tree-search
 - similar_bug_search: missing evidence kind whole-tree-search
 - standing_rule_inventory: S03 unresolved: Tejun upstream modules and upgrade tracking
 - standing_rule_inventory: S04 unresolved: Chris Mason prompt version pinning and update tracking
 - standing_rule_inventory: S05 unresolved: Sashiko coverage floor: mandatory, not supplemental
 - standing_rule_inventory: S06 unresolved: Cross-tree shared-interface and ABI build gate
 - standing_rule_inventory: S07 unresolved: Source integrity and review scope
 - standing_rule_inventory: S11 unresolved: Mandatory impact-coverage gate, in ALL tracks
 - standing_rule_inventory: S13 unresolved: Standing-rule compliance report: mandatory before every verdict
 - standing_rule_inventory: S14 unresolved: Similar-bug search: mandatory in ALL tracks
 - standing_rule_inventory: S23 unresolved: Artifact delivery: mandatory
 - standing_rule_inventory: missing evidence kind sections
```

Patch 2:

```text
HOLD: 26 missing/invalid/unresolved checks
 - all_callers: unresolved symbol inventory for H001
 - all_callers: executed command failed
 - all_callers: executed command failed
 - all_callers: executed command failed
 - all_callers: executed command failed
 - all_callers: executed command failed
 - all_callers: missing whole-tree consumer search for __mfd_assert_write
 - all_callers: missing whole-tree consumer search for mfd_assert_punch_hole
 - all_callers: missing whole-tree consumer search for mfd_fail_punch_hole
 - all_callers: missing whole-tree consumer search for test_seal_punch_hole
 - all_callers: missing whole-tree consumer search for test_seal_punch_hole_shrink
 - cross_tree_consumers: missing evidence kind whole-tree-search
 - cross_tree_consumers: missing evidence kind build-graph
 - parallel_tree: missing evidence kind integration-search
 - similar_bug_search: missing evidence kind whole-tree-search
 - standing_rule_inventory: S03 unresolved: Tejun upstream modules and upgrade tracking
 - standing_rule_inventory: S04 unresolved: Chris Mason prompt version pinning and update tracking
 - standing_rule_inventory: S05 unresolved: Sashiko coverage floor: mandatory, not supplemental
 - standing_rule_inventory: S06 unresolved: Cross-tree shared-interface and ABI build gate
 - standing_rule_inventory: S07 unresolved: Source integrity and review scope
 - standing_rule_inventory: S11 unresolved: Mandatory impact-coverage gate, in ALL tracks
 - standing_rule_inventory: S13 unresolved: Standing-rule compliance report: mandatory before every verdict
 - standing_rule_inventory: S14 unresolved: Similar-bug search: mandatory in ALL tracks
 - standing_rule_inventory: S23 unresolved: Artifact delivery: mandatory
 - standing_rule_inventory: missing evidence kind sections
 - test_matrix: missing evidence kind build-or-test
```


## Unsent review reply

```text
There are two things to address here.

[1/2] also needs to update MEMFD_LUO_ALL_SEALS. As it stands,
memfd_luo_preserve() rejects a memfd carrying F_SEAL_PUNCH_HOLE with
-EOPNOTSUPP. The retrieve path rejects it too. The ABI header requires
bumping MEMFD_LUO_FH_COMPATIBLE when adding support for another seal.
Please include that support and a preservation/retrieval test.

There is also an existing hole in the page-membership argument.
Consider a pre-sized sparse shmem memfd with both seals already set:

- Ordinary fallocate() installs a new !uptodate folio.
- iommufd pins it through memfd_pin_folios(), which neither takes the
  inode lock nor checks uptodate on the page-cache lookup path.
- A later allocation fails and shmem_undo_range(..., true) removes
  that folio. The pin keeps it alive, but it is no longer in the file.

The device can then keep accessing the old folio while the memfd sees
zeroes or a replacement folio. Writes through one cease to be visible
through the other. F_SEAL_SHRINK and F_SEAL_PUNCH_HOLE don't prevent
this ordinary-fallocate rollback.

This predates your patch and needs a separate fix. udmabuf holds the
inode lock across pinning, so this particular race does not apply to
that caller. I checked the source path and a small PlusCal model with
TLC and tla-mctj; I haven't reproduced it on a running kernel.

The two new hole-punch checks look properly placed, but the seals
aren't sufficient grounds to drop the iommufd membership walk yet.
The new UAPI itself isn't a stable candidate.
```

## Timing checkpoint

```text
22:14:06-22:16:27 UTC   140.6s
  Read submission and establish review scope

22:16:27-22:20:37 UTC   249.9s
  Independent source and caller analysis

22:20:37-22:22:14 UTC    97.5s
  Guided methods, history and integration checks

22:22:14-22:23:08 UTC    53.8s
  Build and executable validation

22:23:08-22:25:01 UTC   112.7s
  Guided coverage and caller verification

22:25:01-22:29:49 UTC   287.8s
  Adversarial rollback investigation and formal check

22:29:49-22:30:55 UTC    66.7s
  Final adversarial verification

22:30:55-22:41:12 UTC   616.1s
  Evidence gate, master documents and delivery

Packaging and save confirmation continue after this checkpoint.
The final chat table includes their measured elapsed time.
```
