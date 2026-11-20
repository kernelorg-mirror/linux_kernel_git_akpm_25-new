# AKPM review index

Updated: 2026-11-20 UTC

## Record location

Per-case reports are retained by their existing Library IDs and are
excluded from the kernel-review project tarball. Old `reports/` paths
below identify the original filenames; they are not local project
files. Supporting evidence removed from the v39 tarball is preserved
in Library `kernel-review-case-evidence.tar.gz` (ID
`libfile_d4d380467eb88191ae209b91a4611a3e`); original project
imports are in `kernel-review-history.tar.gz` (ID
`libfile_e9cd753e319c8191b7054a8e1b961f84`). Retrieve individual
reports by their stable ID or exact filename; do not infer that a
report is missing because its old project path no longer exists.

## Review policy checkpoint (2026-11-11 UTC)

For new reviews, gate v5 records source-only evidence. No kernel build,
runtime test, exact-preimage check or patch-application check is part
of the mandatory gate. Older manifests retain their original results.
KCSAN reports and race fixes now require explicit severity analysis:
feasible interleaving, affected consumer, material consequence and
whether the fix closes that path. A warning alone does not establish
severity. See the canonical workflow for the full rule.

2026-11-15 addition: assess whether an actor can deliberately repeat a
rare trigger and cause material harm. Ordinary workload frequency and
known victims do not answer that question; require an accessible entry
point and traced consequence before claiming exploitability. The
mandatory rule is prominent in the canonical workflow and AGENTS.md.

## Current review

### PMD copying at fork, v6

- `R-FORK-HUGE-PMD-V6-20261119`, exact series title
  "[PATCH v6 0/4] mm/huge_memory: copy PMDs at fork like the PTE path does"
  by Konstantin Khorenko. All four v6 patches and the retained v1-v5
  discussion were reviewed against the exact mm/core for-next base
  `f7d95bf74091373fad7273db4557df9b5a902335` and prior v5 evidence.
  No new kernel-code defect found. The new file-folio refcount limit check
  is before the reference, with the same VM_MIXEDMAP exception as the PTE
  path. On follow-up, checking the 4/4 MADV_DONTFORK return was demoted
  to optional hardening: the aligned, mapped range has no ordinary
  failure path. Integration into current mm-unstable still requires
  `read_pmd_pagesize()` to become `pmd_psize()`. The driver zap race may
  preserve revoked PFNs in a child;
  ppc64 hash can crash on the missing deposited table. Stable needs
  1/4 and 2/4 dependencies or a narrower equivalent before 3/4;
  the author offers backports. Source only; no kernel build, runtime
  test, patch application or timely completed gate. Detailed Library
  [report](https://chatgpt.com/library?file_id=libfile_fde3_f-35ca437941e88191ad6d0e6fde213e1a_4b2ce93b89ac81918fc7647a8ebd5560&account_id=personal).

### Boot-time CMA reserved figure

- `R-MM-INIT-CMA-20261119`, exact incoming title
  "[PATCH] mm/mm_init: don't subtract managed CMA pages twice" by
  Chris Mason, forwarded by David Hildenbrand. Author base's submitted
  mm/mm_init.c blob 27a50ecd5c20e732eb169410885afa1e3ba51a4b
  was verified; current mm-unstable 47854e5f27f59a8004c623f543e00209b8967a4c
  has the same affected printout. Some early hugetlb CMA pageblocks
  count in both totalram_pages() and totalcma_pages. Subtracting the
  zone CMA count removes this overlap; no allocation behavior changes.
  The old reserved figure could be understated or wrap on unsigned
  subtraction. `Fixes:` accurately names the commit moving the
  hugetlb setup before the boot message. No source defect found or
  stable backport needed. Late v5 preflight remains HOLD for missing
  receipts; no kernel build, runtime test or patch application.
  Library-only [mm-init-cma-20261119-review.md](https://chatgpt.com/library?file_id=libfile_fde3_f-e52129a0082c8191a583f5d7b1f7c5f9_4b2ce93b89ac81918fc7647a8ebd5560&account_id=personal).

### Failed fork mm lifetime

- `R-FORK-CLEAR-MM-20261119`, exact incoming title
  "[PATCH] fork: clear p->mm when copy_process() fails" by Chris Mason,
  forwarded by David Hildenbrand. Current mm-unstable
  47854e5f27f59a8004c623f543e00209b8967a4c retains the supplied
  old kernel/fork.c blob; exact author base was not fetched. A later
  fork failure used to drop the new mm but leave `p->mm` non-NULL.
  Inherited perf filters can reach `get_task_mm(p)` concurrently;
  task_free BPF can call `bpf_find_vma(p)` after `mmput()`. A failed
  ordinary fork can thus cause a kernel use-after-free. Clearing under
  task_lock before mmput, and clearing the borrowed parent pointer
  before delayed task free on early failure, addresses these paths;
  no new source defect found. The two Fixes commits are credible and
  stable Cc is justified. The v5 preflight was late and remains HOLD
  for incomplete receipts; no kernel build, runtime test or patch
  application. Library-only
  [fork-clear-mm-20261119-review.md](https://chatgpt.com/library?file_id=libfile_fde3_f-e96d899d2a80819187ed935264184ac2_4b2ce93b89ac81918fc7647a8ebd5560&account_id=personal).

### RapidIO config sysfs read limit

- `R-RAPIDIO-FILE-CAP-V1-20261118`, exact incoming title
  "[PATCH] rapidio: Use file_ns_capable() when checking config space read access"
  by Suyuan Wang. Source-only review at current mm-unstable
  376fb945578b6a1f0001fe27adcd01b11340f4a4. The check correctly
  changes the read limit from reader credentials to opener credentials,
  as in PCI. An unprivileged opener remains limited to 256 bytes; an
  unprivileged reader of a privileged-opened descriptor can newly
  access all 16 MiB, potentially locking up affected chips by reading
  undefined space. Ask for a RapidIO use case, explicit discussion of
  both directions, and justification for stable. `Fixes:` correctly
  names the commit introducing the check. Preflight HOLD for incomplete
  source receipts; no kernel build, runtime test or patch application.
  Library-only [rapidio-file-cap-v1-review.md](https://chatgpt.com/library?file_id=libfile_fde3_f-2b3797e4a1808191822130ba48e7d0cb_4b2ce93b89ac81918fc7647a8ebd5560&account_id=personal).

### XArray new-root offset v2

- `R-XARRAY-ROOT-OFFSET-V2-20261117`, exact incoming title
  "[PATCH v2] xarray: initialise the offset of a new root node" by
  Nickolai Zeldovich <nickolai@csail.mit.edu>. Author base
  26344c0dd32af8790d8474d233619db825441138 verified for both file
  preimages; current mm-unstable tip 1b697248a755254115fde38598193d127c562e7f
  also checked. A stale root offset can make a concurrent RCU iteration
  skip entries or return an entry at the wrong index. Page-cache
  `find_lock_entries()` can hit `VM_BUG_ON_FOLIO` with CONFIG_DEBUG_VM
  on an inconsistent returned index. The allocation change fixes the
  root offset; no new source defect found. Split the submitted diff
  without changing either hunk into a test-only [1/2] and fix [2/2]
  for A/B testing. The test depends on slab reuse; A passing is
  inconclusive. The source-only preflight was late and remains HOLD;
  no kernel build, runtime test or patch application. Library-only
  [review](https://chatgpt.com/library?file_id=libfile_77adfe1c28b08191bd7b91e8a37f75de&account_id=personal),
  [test patch](https://chatgpt.com/library?file_id=libfile_f13eea1e3d98819180ce3bd293088d93&account_id=personal),
  [fix patch](https://chatgpt.com/library?file_id=libfile_8ea8c3e136688191a6e10ab09dbea7c3&account_id=personal).

### Userfaultfd state fixes v3

- `R-UFFD-STATE-V3-20261117`, exact series title
  "[PATCH v3 0/9] userfaultfd: assorted fixes (part 1)" by Tal
  Zussman <tz2294@columbia.edu>, cover Message-ID
  <20261117-uffd-state-fixes-v3-0-b617009d1a4a@columbia.edu>.
  All nine submitted patches reviewed against the author's exact mm-new
  base 25fee5b1762b8799dd8b72c2f6d666eb01680cc7, with all initial
  file blobs matching the supplied diffs; mm-unstable
  866f761fd414012d4be77cc82c06667d23a3a7fc also inspected. Source
  supports unintended tmpfs hole allocation and accounting through a
  private possibly read-only mapping in 1/9, but not overwriting
  existing file data (correction to first review); persistent
  UFFDIO_MOVE retry in 2/9, erroneous PAGEMAP_SCAN state in 3/9 and
  5/9, lost tracking after mremap rollback in 7/9 and invalid-range
  unregister in 9/9. Patch 4/9 changes recovery for malformed writable
  plus uffd huge migration entries: it drops the uffd bit and adds a
  potentially fatal warning under panic_on_warn. No producer of that
  malformed state was found after 3/9; ask why the defensive behavior
  should change. Patch 7/9 adds a full destination-VMA protection walk
  and may cause extra write faults. Request focused regression evidence.
  All nine source-only preflights remain HOLD for incomplete receipts,
  so no unconditional take or
  Reviewed-by. No build, runtime test or patch application. Library-only
  [uffd-v3-review.md](https://chatgpt.com/library?file_id=libfile_e1c001a4bf388191891e34bed6034fa2&account_id=personal).

### BPF memcg forced flush v3

- `R-MEMCG-BPF-FORCE-FLUSH-V3-20261117`, exact incoming subject
  "[PATCH v3] mm/bpf: Always flush memcg stats when explicitly requested"
  by Runli <mingyu.he@shopee.com>, Message-ID
  <20261112041348.66915-1-mingyu.he@shopee.com>. Source review at
  mm-unstable 866f761fd414012d4be77cc82c06667d23a3a7fc: the
  concurrent-flush threshold race can leave an ancestor's rstat-derived
  values stale until the periodic forced flush. v3's forced BPF call
  preserves memcg flush bookkeeping and has no identified source
  correctness defect. `memory.current` and `memory.max` accounting do
  not use these stale values; ordinary `memory.stat` reads remain
  thresholded. Frequent explicit BPF flushes can increase rstat-lock
  contention. Provisional source assessment; v5 preflight was missed,
  no unconditional take/Reviewed-by, build, runtime test or patch
  application. Next: request precise effects wording and an immediate
  BPF read test. Library-only
  [memcg-bpf-force-flush-v3-review.md](https://chatgpt.com/library?file_id=libfile_df124ac4d89481919c11e527a6a3aeac&account_id=personal).

### Early hardware-protection poweroff/reboot v2

- "[PATCH v2] reboot: don't rely on the poweroff/reboot helper before init has started":
  v2 preserves the helper for `orderly_poweroff(false)`, resolving the
  v1 regression. CHANGES NEEDED / HOLD: the forced poweroff or reboot
  request only queues work; the new `system_state` check runs in the
  worker. A request made before `SYSTEM_RUNNING` can be processed
  after the transition and still exec an ineffective initramfs helper.
  With the default zero thermal backup delay and one-shot hardware
  protection request, shutdown can again fail. Preserve the early
  request state through work scheduling. The separate interval from
  `SYSTEM_RUNNING` until init is ready remains acknowledged. Source
  at mm-unstable 866f761fd414012d4be77cc82c06667d23a3a7fc;
  no kernel build, runtime test or patch-application check.
  [reboot-early-hw-protection-v2-review.md](https://chatgpt.com/library?file_id=libfile_75e74fedd2f88191a61cd8cb3b3277c8&account_id=personal).

### HugeTLB memfd memory failure policy v4

- "[PATCH v4 0/3] memfd-based Userspace MFR Policy for HugeTLB":
  reviewed all three patches and Chris Down's replies on 2026-11-16
  (Pacific). "[PATCH v4 1/3] mm: memfd/hugetlb: memfd-based userspace
  HugeTLB MFR policy" leaves UFFDIO_CONTINUE rejecting the poisoned
  folio and memory hotremove unmapping it; a pinned folio can later be
  counted as free despite being skipped by allocation, leading to
  reservation success then fault-time SIGBUS; a filtered second error
  can clear the first error's poison state. "[PATCH v4 2/3]
  selftests/mm: test userspace MFR for HugeTLB hugepage" reserves
  another four hugepages in its private seal-mode mapping although it
  ensures only four free; the automated invocation selects only 1G.
  "[PATCH v4 3/3] Documentation: add documentation for
  MFD_MF_KEEP_UE_MAPPED" overpromises isolation after close while
  another pin survives. Source-only HOLD. Current mm-unstable
  e1f34fb16e0236c4e60b5f392f1cf5aee76f7d0f is not the author's
  exact base plus v7 dependency; no kernel build, runtime test or
  patch-application check. Author explicitly disclosed AI help;
  Chris's writing does not establish his tool use. Library-only
  [mfr-hugetlb-v4-chris-down-review.md](https://chatgpt.com/library?file_id=libfile_a27504897a888191bbf1d26d4d5fa59c&account_id=personal).

### Pending secondary reports (not primary acceptance reviews)

- "[PATCH v2] lib/test_hmm: fix alloc tag leak when splitting
  device-private folios" by Nilay Vaish, Message-ID
  <20261119233119.1721789-1-nilayvaish@google.com>:
  secondary source review says the new unsigned int loop counters
  cover one PMD-sized folio and the split/free paths appear consistent.
  It did not verify the exact mm-unstable base or complete the primary
  source evidence record. No primary acceptance decision, build or
  runtime test. Inbox [secondary report](https://chatgpt.com/library?file_id=libfile_fde3_f-72d8e2c612a48191b375d1fde86d97e2_4b2ce93b89ac81918fc7647a8ebd5560&account_id=personal).
- "[PATCH v2 0/7] KMSAN: Move per-page metadata out of struct page":
  secondary source review compared all seven patches with the existing
  v1 case. It flags the 32-bit page-owner alignment limit in 2/7 and
  contiguous memblock allocation of all SPARSEMEM page-extension
  sections in 5/7, including non-KMSAN configurations. Both need a
  primary assessment; its v5 gate remains incomplete. No build, runtime
  test or patch-application check.
  [kmsan-page-ext-v2-20261117-review.md](https://chatgpt.com/library?file_id=libfile_6315fbf0c6288191b1af36c453c9aef3&account_id=personal).
- "mm/vmscan: fix legacy memcg reclaim deadlock against filesystem freeze":
  secondary source review warns that the global writeback-wait skip can
  let an unrelated legacy memcg reach OOM during a pending freeze.
  It drafted an Andrew-authored per-reclaim-target follow-up and a
  proposed A/B guest test. The draft and plan are untested Library
  evidence, not an acceptance decision or runtime result.
  [review](https://chatgpt.com/library?file_id=libfile_1f8909b8bfd0819182f75359fb4a6f1e&account_id=personal),
  [follow-up patch](https://chatgpt.com/library?file_id=libfile_be670315ba808191930daea2a1478f98&account_id=personal),
  [test plan](https://chatgpt.com/library?file_id=libfile_68bf575cde1c81918889c5cb2f93bc6b&account_id=personal).
- `R-MGLRU-NOIO-SWAPPINESS-20261116`, incoming subject
  "[PATCH] mm/vmscan: respect can_reclaim_anon_pages() in MGLRU get_swappiness()":
  secondary source review at `mm-unstable`
  e1f34fb16e0236c4e60b5f392f1cf5aee76f7d0f. It describes the
  GFP_NOIO reclaim stall and the patch's broader anon-aging change;
  it flags overlap with Barry Song's MGLRU v9 work in `mm-new` and an
  unverified submitted preimage. Source-only HOLD, with incomplete v5
  gate inventory, no primary acceptance decision, build, patch
  application or runtime test. In inbox:
  [mglru-noio-swappiness-20261116-review.md](https://chatgpt.com/library?file_id=libfile_9db8161d0ec481919a4f95ae290a7da7&account_id=personal).
- `R-WORKINGSET-NOKMEM-20261116`, incoming subject
  "[PATCH] mm: workingset: compare shadow nodes node-wide without kmem accounting":
  secondary source review of the `cgroup.memory=nokmem` shadow-node
  budget and possible refault/cache-churn effects, at `mm-unstable`
  e1f34fb16e0236c4e60b5f392f1cf5aee76f7d0f. No build, runtime
  test or patch application. Its v5 gate remained HOLD because the full
  evidence inventory was not populated; this is not a patch defect or
  a primary take decision. In inbox:
  [workingset-shadow-nokmem-20261116-review.md](https://chatgpt.com/library?file_id=libfile_eeca3c5db5a08191a1d28b7b682eb045&account_id=personal).
- `R-HUGETLB-BULK-RESTORE-20261116`, report's incoming title
  "hugetlb: don't restore vmemmap of non-HVOed folios on bulk restore error":
  secondary source locking/lifetime review at `mm-unstable`
  e1f34fb16e0236c4e60b5f392f1cf5aee76f7d0f. It reports no new
  race in the changed branch and notes `CONFIG_DEBUG_VM` with
  `panic_on_warn=1` as a conditional impact of the old warning. Its v5
  gate remained HOLD for incomplete evidence; the primary chat has
  not made an acceptance decision. In inbox:
  [hugetlb-bulk-restore-locking-20261116-review.md](https://chatgpt.com/library?file_id=libfile_529be944895c819188e70c7abbfe1b78&account_id=personal).

### Completed or previously assessed work

- "[PATCH 0/2] xarray: free unused spare node after range creation":
  focused Fixes-lineage correction for
  "[PATCH 1/2] lib: xarray: free unused spare node in xas_create_range()".
  Sashiko correctly rejects `cae106dd67b9`: it changed the
  failed-`xas_nomem()` exit, not the successful retry with an unused
  spare. The production `xas_create_range()` / `xas_nomem()` retry
  loop without success-path cleanup was introduced in `77da9389b9d5`
  ("mm: Convert collapse_shmem to XArray"); use that as the Fixes
  trailer. `2264f5132fe4` introduced the helper without cleanup and
  is a less-specific library-API alternative. Patch 2/2 is a test.
  No fresh full source-acceptance review, kernel build, runtime test
  or patch application. Detailed Library-only
  [xarray-spare-node-fixes-lineage-review.md](https://chatgpt.com/library?file_id=libfile_e49040436920819196bb1130c3c8ffe1&account_id=personal).

- "[PATCH] lib/percpu_counter: allow concurrent sums with an rwlock"
  by Jiebin Sun: 2026-11-16 focused whole-tree sum caller inventory on
  mm-unstable `4b028d0cedf95f66b8c5294fde2d7d698bf830da`.
  Non-statfs conditional paths include ext4 allocation near free-space
  exhaustion, XFS near ENOSPC, low-limit writeback throttling, Btrfs
  reservation pressure and opens near global `file-max`. BFQ's
  dispatch sums require its debug config and are under an outer queue
  lock; a Btrfs clamp sum is under a space-info lock. Low-limit
  writeback is the most plausible recurring parallel-sum case, with
  no measured real-world win. The author's 47.34% dentry result has no demonstrated
  causal link to `ext4_statfs()`: current upstream stress-ng dentry
  worker and its directory helper do not visibly call `statfs()`.
  Potential update-side contention and CPU-hotplug latency need
  measurement. No clear locking correctness bug established. Request
  a profile tied to measured workers and mixed read/write workloads
  before taking; formal gate HOLD because preflight was missed, with
  no Reviewed-by, kernel build, runtime test or patch application.
  Library-only [percpu-counter-rwlock-jiebin-review.md](https://chatgpt.com/library?file_id=libfile_352e312802ac8191abe22ded89a7b834&account_id=personal).

- "[PATCH v5 0/3] ipc/sem: account dynamic sops arrays and validate
  SEMOPM" by Yingjie Wang. Focused 2026-11-15 source review of all
  three patches on `mm-nonmm-unstable`
  199bbdb0b473185737495b13bfa86eeab9d63ddb, with supplied base
  7be4bc52fd9e0e55dc9a2e0232b89427d2c4b614 not independently
  reconstructed. For
  "[PATCH v5 1/3] ipc/sem: account dynamically allocated sops arrays to memcg",
  the uncharged blocked array can exhaust host memory across a memcg
  boundary; ARM OABI has a separate capped unaccounted allocation.
  "[PATCH v5 2/3] ipc/sem: reject negative SEMOPM values" also prevents
  a rejected sysctl write from leaving earlier limits changed. The
  positive limit can still be INT_MAX and accounting only contains
  damage with effective memcg limits. Both stable Ccs have prospective
  bugfix grounds, but each standalone changelog needs a concrete
  user-visible consequence. "[PATCH v5 3/3] ipc/sem: remove obsolete
  SEMOPM fragmentation warning" is documentation-only, with no stable
  case. Focused source review only; gate HOLD, no acceptance tag,
  kernel build, runtime test or patch application. Library-only report
  semopm-v5-review.md, ID libfile_d1c9cd7c8fa08191981deb572352d95e
  (https://chatgpt.com/library?file_id=libfile_d1c9cd7c8fa08191981deb572352d95e&account_id=personal).

- Application-status correction for
  "[PATCH v3] ipc/msg: fix msg_qbytes truncation in IPC_SET" (R-054),
  previously titled
  "[PATCH v2] ipc/msg: prevent msg_qbytes limit bypass in IPC_SET"
  (R-052): a 2026-11-15 20:59 UTC source scan of all 17 advertised
  akpm/mm heads found the v3 width changes and selftest in
  `mm-nonmm-unstable` 199bbdb0b473185737495b13bfa86eeab9d63ddb
  and `mm-everything` 930e275dda34ee72b0ad0b12a3af91b570ffd338,
  and absent from the other 15, including `mm-unstable`. The
  2026-10-30 `mm-commits` notice confirms pickup into
  `mm-nonmm-unstable`. Retract the earlier inference from absence in
  `mm-unstable` that Andrew had not applied the fix. Source presence
  was checked; exact commit ancestry was not. See R-054's Library-only
  report (ID libfile_2ba8be1cfb84819193af227f696cd7e0) and the
  branch inventory in `kernel-git-access.md`.

- "[PATCH] mm/filemap: queue non-exclusive folio waiters ahead of exclusive"
  2026-11-15 focused source review, M. Grove, Message-ID
  <179296822701.680532.8543194155713536453@airmail.cc>, review ID
  R-FILEMAP-WAIT-20261115. On current mm-unstable
  4b028d0cedf95f66b8c5294fde2d7d698bf830da, a non-exclusive
  waiter behind an exclusive waiter misses that unlock's wake-one walk,
  but remains queued for the exclusive locker's later unlock. New
  exclusive waiters append behind it. Josef Bacik's separate signal
  race fix is present and addresses a way to lose that follow-on
  unlock. The proposed head insertion can reduce latency across queued
  locker cycles, but a permanent lost wake and a causal link to the
  cited syzbot hang were not established. PENDING/HOLD pending a
  per-waiter trace on a tree with Josef's fix. No full v5 preflight,
  kernel build, runtime test or patch application. Detailed Library-only
  report folio-waiter-order-grove-review.md, ID
  libfile_1017f26aab6081919885b390adff2608
  (https://chatgpt.com/library?file_id=libfile_1017f26aab6081919885b390adff2608&account_id=personal).
  Follow-up correction: `io_uring`'s async tail waiter has flags=0;
  its callback schedules a retry but does not consume the exclusive
  wake allowance. Josef suffices for the established signal race, so
  Grove's email can be dropped as a correctness fix. Neither patch is
  proven to close the cited syzbot report.

- "[PATCH] mm/util: fix retry detection and handling in snapshot_page()"
  David Hildenbrand's proposal in reply
  <72dc7b45-ad20-450b-8ec7-3e86be8a41f8@kernel.org> to
  "[PATCH] mm/util: fix off-by-one when checking folio index in snapshot_page()"
  by Shao Mingyin. 2026-11-15 focused adversarial source review on
  mm-unstable 4b028d0cedf95f66b8c5294fde2d7d698bf830da. David's
  zero-count normalization avoids a false head-page fallback during
  bad-page diagnostics; resetting flags avoids carrying BUDDY/IDLE
  from a failed snapshot into `/proc/kpageflags`. Other consumers are
  `dump_page()` and `/proc/kpagecount`; no source-supported material
  failure from deliberate repetition of this specific bug was found.
  David's low-severity/no-stable judgment is supported in this focused
  trace. Retrospective v5 gate HOLD (73 missing/unresolved items), no
  acceptance tag, kernel build, runtime test or patch application.
  Library-only detailed report snapshot-page-david-proposal-review.md,
  ID libfile_3ea557b54d60819181d041a3c66cbe74
  (https://chatgpt.com/library?file_id=libfile_3ea557b54d60819181d041a3c66cbe74&account_id=personal).

- "[PATCH] mm/huge_memory: flush dirty file PMDs before removing rmap"
  2026-11-15 focused DAX follow-up, David Hildenbrand (Arm), Message-ID
  <20261113-dirty_file_pmd-v1-1-8c11f2a2e65f@kernel.org>, patch base
  55c8a634fd238bc7e6e2c4010985192ae8163435. Review key
  dirty-file-pmd-dax-v1. Filesystem DAX can use folio-backed PMDs;
  `dax_writeback_one()` write-protects mappings, flushes CPU caches,
  then clears the dirty tag. A concurrently cleared PMD with a stale
  writable TLB entry can miss protection and permit untagged stores
  after the flush. David's under-PMD-lock TLB flush closes this
  source-reachable interval. No reproduction of this exact race was
  established; a 2022 DAX data-loss fix covered a distinct failure
  of write-protection after tag clearing. The posted patch copies Jan
  Kara, a DAX reviewer, but not Dan Williams, Matthew Wilcox or the
  linux-fsdevel/nvdimm lists. Focused source assessment only, not a
  complete v5 gate review; no kernel build, runtime test or patch
  application. Normalized subject: mm/huge_memory: flush dirty file
  PMDs before removing rmap. Detailed Library-only report
  dax-dirty-file-pmd-followup-review.md, ID
  libfile_487b64b7b3f48191b531b75a4e8a9fe3
  (https://chatgpt.com/library?file_id=libfile_487b64b7b3f48191b531b75a4e8a9fe3&account_id=personal).

- "[PATCH] ocfs2: drain domain handlers before destroying the DLM worker"
  2026-11-15 focused follow-up on Cen Zhang's unversioned patch,
  Message-ID
  <pm-ocfs2-objects-candidate-0056-v2-57239c657ac017b50fa1@gmail.com>.
  Joseph Qi requested an empty-list guard, as in the join-handler
  cleanup: <88281285-5b3e-4266-88d9-784dfea5ebe7@linux.alibaba.com>.
  The list is initialized before registration; early registration
  failure can leave it empty, and partial registration failure can
  clean it up twice. Avoid an unnecessary global o2net workqueue drain
  in those cases while retaining Cen's drain for installed handlers.
  Andrew-authored incremental patch prepared on mm-nonmm-unstable
  199bbdb0b473185737495b13bfa86eeab9d63ddb, not sent. Review key
  ocfs2-domain-handler-drain-cen-v1; focused source follow-up only,
  not a complete v5 gate review. No kernel build, runtime test or patch
  application. Normalized subject: ocfs2: drain domain handlers before
  destroying the DLM worker. Detailed report
  ocfs2-domain-handler-flush-followup-review.md, Library ID
  libfile_55861354dbc08191ab4320e0b34c5838
  (https://chatgpt.com/library?file_id=libfile_55861354dbc08191ab4320e0b34c5838&account_id=personal).
  Prepared patch ocfs2-skip-network-flush-when-no-domain-handlers-are-registered.patch,
  Library ID libfile_42c9b4446ab4819181b2ec7f36b73cfb.

- "[PATCH 0/3] KMSAN: Move per-page metadata out of struct page"
  2026-11-15 correction: CHANGES NEEDED / HOLD after Chris Down's
  replies. The original source review missed doubled page_ext lookups
  per direct-mapped instrumented access; Chris reports roughly
  14-17% slower elapsed times in three KMSAN VM workloads, and a
  one-lookup prototype returning to baseline. Moving the pointers
  shrinks `struct page` from 80 to 64 bytes on his configuration and
  enables HVO there; changelog and KMSAN documentation need updating.
  [2/3] also moves FLATMEM callbacks, selects a different memblock
  lower bound and prints per-section free messages. Muchun accepted
  those review suggestions. Chris reports crash reproduction and a
  successful quick HVO check; we did not run tests. The original
  source-favorable verdict and reply are superseded. Gate v5 remains
  HOLD (exit 2), with no take or Reviewed-by. See
  reports/kmsan-page-ext-v1-review.md, Library ID
  libfile_1c830b6073d48191a47cc52182a90e7c
  (https://chatgpt.com/library?file_id=libfile_1c830b6073d48191a47cc52182a90e7c&account_id=personal).
  Its gate manifest is in the Library-only case evidence archive as
  reports/evidence/kmsan-page-ext-v1-gate.json.

- "[PATCH v2] mm/readahead: look two windows ahead for the hole on a marker hit"
  2026-11-15: one hunk reviewed on the specified v7.4-rc2 base and
  current mm-unstable. Searching the second window can restart readahead
  after mmap read-around has filled the first; the issued window remains
  capped at `max_pages`. No blocking source defect established. The
  longer cache search and bounded speculative I/O are possible costs.
  Author's speedups are not independent measurements. Retrospective
  evidence gate HOLD because preflight was missed; no acceptance tag,
  kernel build, runtime test or patch-application check. See
  reports/readahead-two-windows-v2-review.md.

- "[PATCH] mm/numa_emulation: use the real node id for leftover nodes"
  2026-11-14 impact correction: with valid SRAT, absent optional SLIT,
  `numa=fake=` and a leftover PXM node, the old second distance loop
  dereferences NULL `phys_dist` during early boot; it can prevent
  userspace from starting. This was missed in the initial
  performance-only assessment. A concrete source path is two SRAT
  RAM nodes, `CONFIG_NUMA_EMU=y`, `numa=fake=1`, and no SLIT; the
  second physical PXM takes leftover slot 1. This is a narrow debug
  configuration, with no boot reproduction or frequency evidence.
  Fake NUMA remains used for performance and memory-tier experiments,
  including on physical multi-node systems; a single-physical-node
  `numa=fake=N` setup lacks the leftover PXM needed for this bug.
  With a physical table, slot-derived
  IDs can instead yield wrong NUMA distances, affecting zonelist
  fallback, scheduler locality and memory demotion. The new mapping
  and zero-count fallback address both source paths; `Cc: stable` is
  reasonable. The two `< 0` checks are redundant after assignment
  and default fill. Formal gate HOLD for incomplete whole-tree search
  and stage receipts, without a take or Reviewed-by recommendation.
  No kernel build, runtime test or patch-application check. See
  reports/numa-emulation-leftover-v1-review.md and evidence manifest.

- "[PATCH v2] lib/lz4: backport upstream fast decode loop"
  2026-11-14: CHANGES NEEDED / HOLD against mainline base
  97d73c825122. The new 32-byte fast copies change the input/output
  overlap contract, but `LZ4_DECOMPRESS_INPLACE_MARGIN()` remains at
  `(n >> 8) + 32` and EROFS still uses it to select direct in-place
  decoding. A separate LZ4 vendoring series reports actual valid-stream
  failures with the upstream fast loop at this margin; Gao Xiang asked
  that its margin fix be inseparable from the decoder update. V2 also
  checks only the variable-length helper's internal sum, not the
  following token/MINMATCH additions on 32-bit. A literal extension
  near `SIZE_MAX` can overflow, have `loop_error` ignored and turn a
  block the old decoder rejected into accepted output. Typical in-tree
  compressed blocks are too small for that length; no direct in-tree
  exploit path was established. No kernel build, runtime test, or
  patch-application check. Source-only v5 gate remains incomplete.
  See reports/lz4-fast-decode-v2-review.md and its evidence manifest.

- "[PATCH v2 0/2] mm/shrinker: per-memcg shrinker units in an xarray, allocated on demand"
  2026-11-14: Both v2 patches reviewed against author base
  6628e7d4c6b2 and current mm-unstable 24231596edf2. No concrete
  regression found in inspected source paths; v2's reported memory
  and reclaim benefits apply to its mount-heavy workload. HOLD as a
  source-review evidence status: exact-base whole-tree consumer search,
  concurrency model and full stage/receipt coverage were not completed;
  the gate preflight was late and its check failed. Current mm-unstable's
  owner-aware list_lru changes must remain during integration. No
  Reviewed-by or unconditional take, kernel build, runtime test or patch
  application. See reports/shrinker-xarray-v2-review.md and the
  preserved v5 preflight under reports/evidence/.

- "[PATCH] mm: list_lru: don't use a new memcg's lists for an offline memcg"
  2026-11-12 correction after the supplied embargoed Sashiko review:
  **CHANGES NEEDED / HOLD.** The owner check addresses the originally
  described stale-ID lookup, but unchanged
  `memcg_list_lru_allocated()` treats another memcg's reused slot as an
  allocated list. With both C and its parent P initially unallocated,
  this false positive skips P's allocation. A folio later added to the
  root list can be unlinked under P's lock after P allocates a list,
  risking corruption. This is a source-verified pre-existing hole left
  unfixed, not a regression introduced by this patch. The previous
  source-favorable verdict is withdrawn; request an owner-aware,
  RCU-protected presence check. Two changelog corrections remain: ID
  reuse waits for outstanding private-ID references, and the race can
  occur on SMP without preemptible RCU. The introducing Fixes
  target 28e98022b31e ("mm/list_lru: simplify reparenting and initial
  allocation") is defensible; fb56fdf8b9a2 ("mm/list_lru: split the lock
  to per-cgroup scope") makes the wrong-list selection a wrong-lock
  mutation. Formal v5 gate HOLD also retains the earlier evidence gaps.
  The previous model assumed already allocated child/parent lists;
  an extended bounded model finds the omitted root-to-parent trace.
  An incremental owner-aware allocation-check patch,
  "[PATCH] mm/list_lru: verify memcg owner before skipping allocation",
  is at
  reports/evidence/mm-list_lru-verify-memcg-owner-before-skipping-allocation.patch;
  its standalone Library ID is
  libfile_08535f4f88a48191ad5ac61b63953766.
  It is intended to be folded into Shakeel's change. The patch is
  source prepared only, without application, build or runtime check.
  No Reviewed-by or unconditional take; no build, runtime test, patch
  application, or mail. See
  [list-lru-memcg-id-reuse-v1-review.md](https://chatgpt.com/library?file_id=libfile_7171c4246f908191a009221a87314dae&account_id=personal)
  and reports/list-lru-memcg-id-reuse-v1-review.md in the project.

- "[PATCH] mm/khugepaged: reject shmem collapse ranges beyond i_size"
  2026-11-12: targeted diagnostic of Pedro Falcato's reply. Andrew ran
  reports/evidence/shmem-collapse-eof-repro.c on ts's
  6.8.0-124-generic kernel: the initial write raised SIGBUS, collapse
  allowed a beyond-EOF write, and sealing and extension exposed its
  0x51 marker. This is a reproduction on an old kernel, not a current
  mm-unstable runtime result or a complete patch review. A proposed
  permanent khugepaged selftest is at
  reports/evidence/shmem-collapse-eof-selftest.patch, based on current
  mm-unstable 4318887a3efa4c53d6f083ccfd7105b809a3ac65. The v24
  draft wrongly required EINVAL and SIGBUS after collapse; v25 tests
  the zero-fill result of extension while allowing either collapse
  policy. V26 adds Jérémy Jean's exact name and patch Link, clarifies
  the marker and mapping steps, and is the only patch to use. No
  compilation, runtime testing or patch-application check of that patch
  occurred in this chat. See reports/shmem-collapse-eof-diagnostic.md.

- PRIVATE, do not publish: "[PATCH] xfs: don't free unshared blocks under
  in-flight direct I/O through COW remaps". Focused source triage of
  the private report "[security] xfs: unprivileged local root via
  O_DIRECT write into blocks freed by a concurrent COW remap (v4.11
  to mainline, reflink filesystems)". The physical-block lifetime
  hazard is credible at author base fa4ad798f6f6. Proposed patch
  covers important preallocation and software atomic-write cases but
  has unresolved writeback and direct-read residuals. Claimed root and
  container results are unverified by this review; no acceptance.
  See reports/xfs-dio-cow-private-security-review.md. Keep the
  complete project archive private while this record is present.

- "[PATCH] shmem: Serialize fallocate progress with writeout"
  2026-11-12 UTC: focused source triage of Sashiko's separate,
  pre-existing first-page punch-hole issue. Confirmed: the unsigned
  `unmap_end=-1` test calls `unmap_mapping_range()` with a zero or
  negative length, zapping mapped translations from the first or
  second page through EOF. The actual shmem truncate still uses only
  the requested byte range; no direct data loss is established.
  Worst case is a long punch and mass refaults across processes sharing
  a large tmpfs file or memfd, with potential service stalls. This is
  not a complete review of Zhu Jun's KCSAN patch. See
  reports/shmem-first-page-punch-unmap-review.md.

- "[PATCH v4] mm/migrate: don't batch the TLB flush when there is nothing to batch"
  2026-11-11 PT: source review against the author's
  56b90edee105e976d4870b9a048e6965dc0eac56 base, with prior
  v1-v3 discussion. No v4 code defect identified; recommend a Fixes
  trailer for 7e12beb8ca2a ("migrate_pages: batch flushing TLB"),
  independent of the stable nomination decision. Formal v5 evidence
  gate did not pass; no Reviewed-by. See
  reports/migrate-tlb-single-v4-review.md.

- "[PATCH v5 0/6] agents: add skills for Fixes tags, stable tags, similar bugs, and commit messages"
  2026-11-11 PT: all six attached v5 patches read. Changes requested:
  [3/6] treats benign data races/KCSAN warnings too broadly for
  stable at the stated base; [6/6] reverses the arguments to the
  KUNIT_DEFINE_ACTION_WRAPPER macro in a sample. No formal gate pass
  or Reviewed-by. See reports/agent-skills-v5-review.md.

- "[PATCH] lib/bch: use flexible array member for xi_tab"
  2026-11-11 UTC: reviewed all four hunks against mm-unstable
  d3925707865d051ba04d5710d60550776e744368. Allocation bounds,
  table initialization/use, failure cleanup and three MTD callers
  showed no source defect. The pinned-tree whole-tree consumer search
  and v5 gate receipts remain incomplete (HOLD); no gate-certified
  take or Reviewed-by. See reports/bch-xi-tab-v1-review.md and its
  evidence in the complete project archive.

- "[PATCH 00/13] mm: batch of (urgentish?) fixes in oomk, cachestat, dev-migrate, percpu"
  2026-11-11: expanded source review of all 13 v1 patches, with old
  failure and new-path reasoning, error ownership, selected driver
  callers and rejected counterexamples. [03/13] needs stable selection
  alongside [02/13]; consider `Cc: stable` for the correctness fix
  [11/13]. [13/13] mitigates starvation without a completion guarantee.
  No new code defect established in inspected paths. The exact author
  base is no longer treated as a routine-review obstacle. The full
  whole-tree evidence gate is still HOLD; no acceptance or Reviewed-by.
  See
  [mason-migrate-et-al-fixes-v1-review.md](https://chatgpt.com/library?file_id=libfile_9dfcaa1db6b88191ad135d3aea41c496&account_id=personal)
  and reports/mason-migrate-et-al-fixes-v1-review.md in the project.

- "[PATCH v7] lib/group_cpus: Snapshot cluster masks to keep grouping hotplug invariant"
  2026-11-10 UTC: full v7 source and caller review. No v7 source defect
  identified; no revision requested. The v4 HOLD and v5 reassessment are
  historical, distinct revisions. The then-current v4.2 gate required
  a prohibited application check, so no gate-certified take or
  Reviewed-by was offered. Gate v5 now supports source-only reviews;
  the historical review is not retroactively certified. No build,
  runtime test or application check by this review project.
  The report now includes an unexecuted ts/QEMU NVMe A/B test design
  with topology, queue-count, and path-coverage conditions for the
  kernel-testing project; do not treat it as test evidence.
  See [group-cpus-snapshot-v7-review.md](https://chatgpt.com/library?file_id=libfile_b908cd45e1188191af1e57726bd6f503&account_id=personal)
  and reports/group-cpus-snapshot-v7-review.md in the project.

- "[PATCH 0/2] mm: kmemleak: avoid long RCU read-side sections in reports"
  2026-11-09 PT: full two-patch source review against the author's
  6628e7d4c6b2 base. [1/2] addresses the cleanup overlap; [2/2]
  leaves its periodic reschedule ineffective inside a long
  kmemleak_seq_next() skip chain because *pos does not advance there.
  CHANGES NEEDED / HOLD. See
  [kmemleak-report-rcu-v1-review.md](https://chatgpt.com/library?file_id=libfile_150e0f8bdc548191a294bb4124e37b51&account_id=personal)
  and reports/kmemleak-report-rcu-v1-review.md in the project.

- "[PATCH v12 00/10] mm/vmalloc: Speed up ioremap, vmalloc and vmap with contiguous memory"
  v12: full ten-commit source pass; [07/10] signed page-array index
  overflows on an extremely large high-order mapping. HOLD: evidence
  gate and per-clause audit incomplete. Earlier [09/10] NULL-page
  claim withdrawn for lack of a legitimate input producer.
  See reports/vmalloc-contiguous-v12-review.md (Library ID libfile_7a87db4f507c8191bb46861d4c25d032).

## Project migration checkpoint

kernel-review version 1 reconciles the complete kernel.org md import
with the current Library records. The small kernel.org index was a
single-case discovery stub, not a replacement for this fuller index.
The reconciled review-activity.md restores the missing R-038 through
R-042 history. Current report versions and corrections still prevail.
Historical line numbers for older ledger snapshots are lookup hints;
match exact headings and subjects in the current ledger.

The project is delivered in full as kernel-review.tar.gz on every file
change. Keep this same index identity synchronized for testing chats.
Original imports and hashes are preserved under history/ in the project.

## Coverage and use

This is a discovery index, not a new review or acceptance decision.
Previous discovery inventory: all 3,659 Library items returned by complete pagination were
examined for review/history/evidence filenames. All identified standalone
kernel review reports were read, including paginated continuations. The
latest cumulative ledger, older canonical ledgers and dated archive were
read. Evidence archive members were inspected for report and submission
identities. Links retain original Library identities and filenames.

This indexes every review recoverable from those records, including
incomplete reviews and separate investigations. It cannot certify every
review ever conducted: conversation-history retrieval is unavailable,
and some chat-only discussions have no saved report. UNKNOWN is not
unreviewed. Raw submitted mail alone is not evidence of completed review.

Before test planning, retrieve the linked report's CURRENT version and
any correction or follow-up. Match subject, version, Message-ID and base
against the actual patch. Record the report ID/version and covered
findings in the test plan. If retrieval fails, mark it BLOCKED/UNKNOWN;
independent testing may proceed with that limitation stated. Search the
exact report filename or use its Library ID if subject search misses.

Review numbers are NOT unique: R-043 identifies both swapoff and
idle_inject; R-044 both Boyer-Moore and migrate_device; R-045 both slab
isolation and pagemap exclusivity. Always disambiguate by subject/source.
Do not combine the dispositions of those unrelated records.

## Corrections which must be read first

- The first vmalloc v12 report called [09/10]'s early NULL-page read
  a blocker without proving that an in-tree caller can supply NULL.
  The 2026-11-09 ten-commit re-review withdraws that objection and
  reports a separate >INT_MAX-page [07/10] signed-index defect.
  Read the current standalone report before citing either claim.

- IPC msg_qbytes v1/R-046's unprivileged UINT_MAX bypass claim was wrong.
  Read R-052's correction and R-054's v3 review; do not reuse that claim.
- R-034's early favorable cgroup-s64 verdict was withdrawn after Tejun
  feedback. Read the corrected report and feedback reconciliation.
- Maple v2's initial take verdict was superseded for the reverse empty-root
  state by maple-root-disappearance-review.md.
- HVO v4's separate PMD allocation OOM concern is an unproven hypothesis,
  not an established additional boot bug. Oversized boot reservations
  must be distinguished from an otherwise viable configuration. Read the
  current standalone HVO report before its historical archive.
- R-036 v5 and v7 are distinct new reviews; neither rewrites v4 HOLD.
- Older gate failures remain historical evidence. A later tooling repair
  does not imply every older review now passed. Retrieve exact records.
- DAX vmemmap v3's gate HOLD reflects incomplete review receipts and an
  intentionally unrun build/test, not a confirmed patch defect. Read the
  current report's 2026-11-07 correction before quoting its first draft.
- DAX vmemmap v3's 06:24 tool-unavailability claim was superseded at
  06:30: AKPM's validated TLA+ checker kit was recovered from Library
  and passed its self-test in Work. A further 06:37 correction found
  herd7 7.58 in a case-local OPAM switch on connected host ts and ran
  an LKMM smoke test. The 06:41 venue correction clarifies that ts
  execution is not Work-local herd7 availability. No kernel model of
  this DAX series ran. Read the current report before repeating any
  old unavailability claim without its execution venue.

## Retired work

AKPM discarded R-069's pagecache-refcount work and the separate Trinity
OOM diagnosis (e97d7c516522) on 2026-11-08. Neither is pending work.
Do not resume them or carry them into future handoffs without a request.
The R-069 record below is retained for historical lookup only.

## Standalone review reports and investigations

Each entry identifies a saved record, not a unique patch count. Multiple
versions, feedback reports and aliases are intentionally retained.

### reboot: fail run_cmd() before init so hw protection can force the action

Historical v1 record; v2 above resolves the lost non-forced request,
but has a separate queued-worker state-transition gap.
Record: `reports/reboot-early-hw-protection-v1-review.md` in the full
project archive. Evidence: `reports/evidence/reboot-early-hw-protection-v1.patch`
and `reports/evidence/reboot-early-hw-protection-v1-manifest.json`.
- Exact subject: [PATCH] reboot: fail run_cmd() before init so hw
  protection can force the action
- Author: Zak Brighton Knight <zakbrightonknight@gmail.com>
- Submitted base: d48723711bae9b8cdc56719c448ba42fef28cbee
- Disposition: CHANGES NEEDED / HOLD. The global early -EBUSY guard
  silently discards orderly_poweroff(false) requests; SYSTEM_RUNNING
  precedes launching init, leaving a residual hardware safety gap.
  The structural evidence gate remains HOLD; no independent runtime
  test or compilation.

### mm/mprotect: UFFD-WP marker installation versus PTE-table reclaim

Record: [uffd-shmem-marker-v1-review.md](https://chatgpt.com/library?file_id=libfile_250548113bf08191909c448947692ce4&account_id=personal),
also in the complete project archive under reports/.
Library ID: `libfile_250548113bf08191909c448947692ce4`.
Evidence: `reports/evidence/uffd-shmem-marker-v1.patch` and
`reports/evidence/uffd-shmem-marker-v1-manifest.json`.
- Exact subject: [PATCH] mm/mprotect: don't skip uffd marker install when
  racing with PTE table reclaim
- Author: David Hildenbrand (Arm) <david@kernel.org>
- Message-ID: 20261107-uffd_shmem_marker-v1-1-91fa2d653cfe@kernel.org
- Submitted base: a3d27154a205f6b32000e7e2734b2a6a4d22c65b
- Disposition: HOLD. Code race fix looks sound on inspected paths, but
  the khugepaged trigger and fe2567eb5521 Fixes attribution appear wrong.
  The evidence gate remains HOLD; no compile or runtime test.
- Version-range correction, 2026-11-08 PST: v5.19 contains the UFFD-WP
  feature and its khugepaged guard, but MADV_DONTNEED PTE-table reclaim
  first appears in v6.14. The demonstrated regression starts there,
  subject to CONFIG_PT_RECLAIM and any downstream backports.

### R-069: mm: limit pagecache folio refcount (v2) - retired

Record: [pagecache-refcount-v2-review.md](https://chatgpt.com/library?file_id=libfile_70fb05b88a0c8191a05cfef7e804d073&account_id=personal)
Library ID: `libfile_70fb05b88a0c8191a05cfef7e804d073`
Evidence: [pagecache-refcount-v2-review-evidence.zip](https://chatgpt.com/library?file_id=libfile_34612edabcfc8191aa43743c703fce28&account_id=personal)
Evidence Library ID: `libfile_34612edabcfc8191aa43743c703fce28`
Last updated: 2026-11-08 PST; retired at AKPM's request.
- Exact subject: [PATCH v2 0/5] mm: limit pagecache folio refcount
- Normalized subject: mm: limit pagecache folio refcount
- Author: David Hildenbrand (Arm) <david@kernel.org>
- Message-ID: 20261107-refcount_overflow_stable-v2-0-c38f6809b106@kernel.org
- Submitted base: df3c65887715e66e2cba69116924020c37996cd8
- Review key: pagecache-refcount-v2-20261108
- Project status: RETIRED at AKPM's request. No further review or
  network-patch work is pending. Original technical and gate results
  remain in the linked historical report.
- Archived draft:
  [net-splice-pagecache-refcount.patch](https://chatgpt.com/library?file_id=libfile_05df823660508191afe312cd3bcac01a&account_id=personal),
  Library ID `libfile_05df823660508191afe312cd3bcac01a`.


### mm: Simplify device DAX vmemmap optimization plumbing (v3)

Record: [mm-simplify-device-dax-vmemmap-optimization-plumbing-v3-review.md](https://chatgpt.com/library?file_id=libfile_cf45957f0cd08191be255ce1faca5073&account_id=personal)
Library ID: `libfile_cf45957f0cd08191be255ce1faca5073`
Evidence: [mm-simplify-device-dax-vmemmap-optimization-plumbing-v3-evidence.zip](https://chatgpt.com/library?file_id=libfile_68a3e5cee1788191a9c60cbe0ace5e30&account_id=personal)
Evidence Library ID: `libfile_68a3e5cee1788191a9c60cbe0ace5e30`
Last saved: 2026-11-07T06:41 UTC; source record version: read current version.
- Exact subject: [PATCH v3 0/5] mm: Simplify device DAX vmemmap optimization plumbing
- Normalized subject: mm: Simplify device DAX vmemmap optimization plumbing
Author: Muchun Song <songmuchun@bytedance.com>
Message-ID: 20261107043122.25650-1-songmuchun@bytedance.com
Base: akpm/mm mm-new 684242af7090928ada5e48fd40a0f3a539b3fd5b
Review key: DAX-vmemmap-v3 / 20261107043122.25650-1-songmuchun@bytedance.com
Disposition: No confirmed v3 defect in source review; gate HOLD reflects
our incomplete evidence receipts, not a patch finding. No compilation,
runtime testing, native Sashiko or kernel formal model. TLC and tla-mctj
were recovered and validated on fixture models in Work. Herd7 7.58 was
found and smoke-tested on connected host ts, but remains unavailable
in this Work container and was not used on this series.
No Fixes/stable tag established; read the current report's correction
and exact evidence gaps.


### mm: Decouple folio-based vmemmap optimization from HugeTLB

Record: [mm-decouple-folio-based-vmemmap-optimization-from-hugetlb-v4-review.md](https://chatgpt.com/library?file_id=libfile_2d7d0b17990881919dfd15299e52878f&account_id=personal)
Library ID: `libfile_2d7d0b17990881919dfd15299e52878f`
Last saved: 2026-11-07T05:37:37.665000Z; source record version: read current version.
- Subject/lookup alias: [PATCH v4 00/13] mm: Decouple folio-based vmemmap optimization from HugeTLB
- Subject/lookup alias: mm: Decouple folio-based vmemmap optimization from HugeTLB
- Additional aliases: HVO; folio-based vmemmap; HugeTLB vmemmap optimization
Author: Muchun Song
Message-ID: 20261107022756.77731-1-songmuchun@bytedance.com
Base: f735a2c21aa94b7b86a93d36f3b17eecc6d49aba
Review key: HVO-v4 / 20261107022756.77731-1-songmuchun@bytedance.com
Read the linked report for current findings, limitations and status.

### [PATCH v4 0/3] mm, swap: keep hibernation swap slots out of the swap cache

Record: [swap-hibernation-review.md](https://chatgpt.com/library?file_id=libfile_97d6501e6988819194a840a23415e733&account_id=personal)
Library ID: `libfile_97d6501e6988819194a840a23415e733`
Last saved: 2026-11-03T21:21:53.004116Z; source record version: read current version.
- Subject/lookup alias: [PATCH v4 0/3] mm, swap: keep hibernation swap slots out of the swap cache
Read the linked report for current findings, limitations and status.

### [PATCH v2 1/3] maple_tree: Fix rcu reader NULL dereference after the tree is emptied

Record: [maple-root-disappearance-review.md](https://chatgpt.com/library?file_id=libfile_f6cbcf6e771c8191a5022298dcdb366c&account_id=personal)
Library ID: `libfile_f6cbcf6e771c8191a5022298dcdb366c`
Last saved: 2026-11-03T03:27:18.023598Z; source record version: read current version.
- Subject/lookup alias: [PATCH v2 1/3] maple_tree: Fix rcu reader NULL dereference after the tree is emptied
Read the linked report for current findings, limitations and status.

### Compaction deferral v2 review

Record: [compaction-defer-review.md](https://chatgpt.com/library?file_id=libfile_1228ded38c44819188266f5854ab5ff7&account_id=personal)
Library ID: `libfile_1228ded38c44819188266f5854ab5ff7`
Last saved: 2026-11-02T06:58:00.219416Z; source record version: read current version.
- Subject/lookup alias: [PATCH v2 0/2] mm/compaction: stop repeating failed async compaction on every THP fault
Source: author Linus v7.4-rc1 base6628e7d4c6b25c8d18f1345e3a20d21829aae7e4.
Read the linked report for current findings, limitations and status.

### [PATCH 0/3] tools/mm/thpmaps: fix THP statistics and mapping names

Record: [thpmaps-review.md](https://chatgpt.com/library?file_id=libfile_0804a63ff6288191bc9cab2d4c8b00ca&account_id=personal)
Library ID: `libfile_0804a63ff6288191bc9cab2d4c8b00ca`
Last saved: 2026-11-02T05:00:08.735325Z; source record version: read current version.
- Subject/lookup alias: [PATCH 0/3] tools/mm/thpmaps: fix THP statistics and mapping names
Read the linked report for current findings, limitations and status.

### [PATCH] selftests/proc: proc-empty-vm: wait for child's SIGSEGV instead of sleep(1)

Record: [proc-empty-vm-review.md](https://chatgpt.com/library?file_id=libfile_e1bed5f455608191b64ff3bfb8b5705e&account_id=personal)
Library ID: `libfile_e1bed5f455608191b64ff3bfb8b5705e`
Last saved: 2026-11-02T04:29:59.734999Z; source record version: read current version.
- Subject/lookup alias: [PATCH] selftests/proc: proc-empty-vm: wait for child's SIGSEGV instead of sleep(1)
Read the linked report for current findings, limitations and status.

### Complete MAINTAINERS series recheck - 2026-11-01

Record: [mm-maintainers-assignment-review.md](https://chatgpt.com/library?file_id=libfile_a9b1d97398808191a0b54eee5c67dc13&account_id=personal)
Library ID: `libfile_a9b1d97398808191a0b54eee5c67dc13`
Last saved: 2026-11-02T03:34:26.959491Z; source record version: 4.
Base: Andrew's MAINTAINERS(4), SHA-256
Source: next-20261030,
Read the linked report for current findings, limitations and status.

### [PATCH 0/4] taskstats: four more tidy-ups in the genl path

Record: [taskstats-review.md](https://chatgpt.com/library?file_id=libfile_bfe12824403c81919848d1fdc47c5d9f&account_id=personal)
Library ID: `libfile_bfe12824403c81919848d1fdc47c5d9f`
Last saved: 2026-11-01T19:41:36.137532Z; source record version: read current version.
- Subject/lookup alias: [PATCH 0/4] taskstats: four more tidy-ups in the genl path
Base b61fa14ce6bcbba2cb9a96feea31b760226d6b43 matched fresh Google and
Read the linked report for current findings, limitations and status.

### R-045: fs/proc/task_mmu: check THP exclusivity for each subpage

Record: [pagemap-thp-exclusivity-review.md](https://chatgpt.com/library?file_id=libfile_ba2058524e1c8191825dfa260cd4d971&account_id=personal)
Library ID: `libfile_ba2058524e1c8191825dfa260cd4d971`
Last saved: 2026-11-01T18:21:21.804750Z; source record version: read current version.
- Subject/lookup alias: [PATCH] fs/proc/task_mmu: check THP exclusivity for each subpage
Author: Kelvin Zhang <zhangxp1998@gmail.com>
Patch base: 64703f0fee7421f0ddfcbd8ee1bfa53b25ffc4ca
Read the linked report for current findings, limitations and status.

### R-068: changes needed

Record: [R-068-review.md](https://chatgpt.com/library?file_id=libfile_ca4cd9d9ae648191acbe1ca5c0c5e6cb&account_id=personal)
Library ID: `libfile_ca4cd9d9ae648191acbe1ca5c0c5e6cb`
Last saved: 2026-11-01T18:08:44.041886Z; source record version: read current version.
- Subject/lookup alias: [PATCH v2 1/1] selftests/proc: use RSS in /proc/pid/smaps_rollup tearing tests
Reviewed author base b61fa14ce6bcbba2cb9a96feea31b760226d6b43.
Read the linked report for current findings, limitations and status.

### R-067

Record: [R-067-review.md](https://chatgpt.com/library?file_id=libfile_8a99d7b3f8b88191aba4dbc80331715e&account_id=personal)
Library ID: `libfile_8a99d7b3f8b88191aba4dbc80331715e`
Last saved: 2026-11-01T05:00:33.100694Z; source record version: read current version.
- Subject/lookup alias: [PATCH 0/2] mm/ksm: keep smart scan from losing duplicate pages
- Subject/lookup alias: [PATCH 1/2] mm/ksm: align smart scan skips with the scan number
- Subject/lookup alias: [PATCH 2/2] selftests/mm: cover merging KSM pages aged by smart scan
Read the linked report for current findings, limitations and status.

### [PATCH 33/44] ipc: use min() instead of min_t()

Record: [R-066-review.md](https://chatgpt.com/library?file_id=libfile_9b03d664c4bc8191a81b960a3d9498ec&account_id=personal)
Library ID: `libfile_9b03d664c4bc8191a81b960a3d9498ec`
Last saved: 2026-11-01T04:36:08.574481Z; source record version: read current version.
- Subject/lookup alias: [PATCH 33/44] ipc: use min() instead of min_t()
Read the linked report for current findings, limitations and status.

### [PATCH 1/1] ipc: sem: fix used_sems overflow in newary()

Record: [R-065-review.md](https://chatgpt.com/library?file_id=libfile_f07a09c6c2f88191a2ac4bf6a484af11&account_id=personal)
Library ID: `libfile_f07a09c6c2f88191a2ac4bf6a484af11`
Last saved: 2026-11-01T03:31:00.122806Z; source record version: read current version.
- Subject/lookup alias: [PATCH 1/1] ipc: sem: fix used_sems overflow in newary()
Base b61fa14ce6bcbba2cb9a96feea31b760226d6b43, fresh matching MM mirrors,
Read the linked report for current findings, limitations and status.

### [PATCH] lib/ts_fsm: preserve token types when exporting patterns

Record: [R-064-review.md](https://chatgpt.com/library?file_id=libfile_d74216c1e8b0819192626c98428a54df&account_id=personal)
Library ID: `libfile_d74216c1e8b0819192626c98428a54df`
Last saved: 2026-11-01T03:07:18.084747Z; source record version: read current version.
- Subject/lookup alias: [PATCH] lib/ts_fsm: preserve token types when exporting patterns
- Subject/lookup alias: [PATCH] lib/ts_bm: fix missed matches with TS_IGNORECASE
Read the linked report for current findings, limitations and status.

### [PATCH] ipc: fix hung task in copy_ipcs()

Record: [R-063-review.md](https://chatgpt.com/library?file_id=libfile_2a4bab3d3a9481918ac8633dc5f7f7d2&account_id=personal)
Library ID: `libfile_2a4bab3d3a9481918ac8633dc5f7f7d2`
Last saved: 2026-10-31T03:22:12.258306Z; source record version: read current version.
- Subject/lookup alias: [PATCH] ipc: fix hung task in copy_ipcs()
Read the linked report for current findings, limitations and status.

### R-062

Record: [R-062-review.md](https://chatgpt.com/library?file_id=libfile_57e31f931bc88191a020af51e9a50d02&account_id=personal)
Library ID: `libfile_57e31f931bc88191a020af51e9a50d02`
Last saved: 2026-10-31T03:00:53.210612Z; source record version: read current version.
- Subject/lookup alias: [PATCH] selftests/uevent: Gracefully handle receive buffer overrun
Read the linked report for current findings, limitations and status.

### R-061 gate resolution (2026-10-30 PDT)

Record: [R-061-review.md](https://chatgpt.com/library?file_id=libfile_c0eaac29d03081918ce7e984187ecbcb&account_id=personal)
Library ID: `libfile_c0eaac29d03081918ce7e984187ecbcb`
Last saved: 2026-10-31T02:49:25.558419Z; source record version: 1.
- Subject/lookup alias: [PATCH v2] params: serialize lookup_or_create_module_kobject()
Source: current mm-unstable b61fa14ce6bcbba2cb9a96feea31b760226d6b43,
Read the linked report for current findings, limitations and status.

### R-044: mm/migrate_device compound folio v4 - targeted follow-up

Record: [migrate-device-compound-v4-review.md](https://chatgpt.com/library?file_id=libfile_86d4266024388191bf81cc9c0fcffbda&account_id=personal)
Library ID: `libfile_86d4266024388191bf81cc9c0fcffbda`
Last saved: 2026-10-31T00:58:48.507940Z; source record version: read current version.
- Subject/lookup alias: [PATCH v4] mm/migrate_device: consolidate compound folio handling
Author: Hui Su, 2026-09-24
Source: torvalds/linux at author-supplied base
Read the linked report for current findings, limitations and status.

### R-060

Record: [R-060-review.md](https://chatgpt.com/library?file_id=libfile_373e64f268f4819194c7d6cc542a2829&account_id=personal)
Library ID: `libfile_373e64f268f4819194c7d6cc542a2829`
Last saved: 2026-10-31T00:41:28.517958Z; source record version: read current version.
- Subject/lookup alias: [PATCH] mm/huge_memory: prevent losing PG_waiters in __split_folio_to_order()
Read the linked report for current findings, limitations and status.

### R-059

Record: [R-059-review.md](https://chatgpt.com/library?file_id=libfile_31e0cf1b68ec819192f599d1ff8239ac&account_id=personal)
Library ID: `libfile_31e0cf1b68ec819192f599d1ff8239ac`
Last saved: 2026-10-31T00:14:06.908724Z; source record version: read current version.
- Subject/lookup alias: [PATCH 1/2] errseq: don't let errseq_check_and_advance() hide later errors
- Subject/lookup alias: [PATCH 2/2] lib/tests: errseq: add a concurrent check_and_advance test
Source: original preflights used cached MM95b7365 with exact matching
Read the linked report for current findings, limitations and status.

### R-058

Record: [R-058-review.md](https://chatgpt.com/library?file_id=libfile_9d90301223408191be04551868c89f52&account_id=personal)
Library ID: `libfile_9d90301223408191be04551868c89f52`
Last saved: 2026-10-30T23:09:20.927603Z; source record version: read current version.
- Subject/lookup alias: [PATCH v2] mm/memory-failure: fix folio refcount leak and min_order_for_split() locking
Read the linked report for current findings, limitations and status.

### [PATCH] userfaultfd: docs: Fix an error code, two names and the POLLERR cause

Record: [R-057-review.md](https://chatgpt.com/library?file_id=libfile_389d7a8ce3208191868cd824c93c011d&account_id=personal)
Library ID: `libfile_389d7a8ce3208191868cd824c93c011d`
Last saved: 2026-10-30T21:59:58.426710Z; source record version: read current version.
- Subject/lookup alias: [PATCH] userfaultfd: docs: Fix an error code, two names and the POLLERR cause
Read the linked report for current findings, limitations and status.

### R-043 - powercap: idle_inject: Create per-CPU threads on registration

Record: [idle-inject-percpu-registration-review.md](https://chatgpt.com/library?file_id=libfile_0d98ff3f8e188191b2a2fa8fcc95afc7&account_id=personal)
Library ID: `libfile_0d98ff3f8e188191b2a2fa8fcc95afc7`
Last saved: 2026-10-30T21:58:01.461945Z; source record version: read current version.
- Subject/lookup alias: [[RFC PATCH]] powercap: idle_inject: Create per-CPU threads on registration
Author: Daniel Lezcano
Read the linked report for current findings, limitations and status.

### [PATCH] mm/shmem: fix swapin livelock on a mismatched large swap cache folio

Record: [R-056-review.md](https://chatgpt.com/library?file_id=libfile_db7273e4426c8191a6bb08f1d14d8480&account_id=personal)
Library ID: `libfile_db7273e4426c8191a6bb08f1d14d8480`
Last saved: 2026-10-30T17:28:54.507803Z; source record version: read current version.
- Subject/lookup alias: [PATCH] mm/shmem: fix swapin livelock on a mismatched large swap cache folio
Reviewed author base bae9a042b03b27924c6fd5bdc00a20d6a44d6041;
Read the linked report for current findings, limitations and status.

### R-018: hugetlb cgroup offlining UAF, v2 review

Record: [hugetlb-cgroup-review.md](https://chatgpt.com/library?file_id=libfile_eb507cfdf1448191a15284fe8382fcac&account_id=personal)
Library ID: `libfile_eb507cfdf1448191a15284fe8382fcac`
Last saved: 2026-10-30T05:03:57.166525Z; source record version: 1.
- Subject/lookup alias: [PATCH v2] mm/hugetlb_cgroup: prevent use-after-free during cgroup offlining
Read the linked report for current findings, limitations and status.

### TSACCT-20261029: tsacct suspend review

Record: [tsacct-suspend-review.md](https://chatgpt.com/library?file_id=libfile_4289a3b33be08191a6348b8af0236646&account_id=personal)
Library ID: `libfile_4289a3b33be08191a6348b8af0236646`
Last saved: 2026-10-30T02:07:12.655209Z; source record version: 1.
- Subject/lookup alias: [PATCH] tsacct: keep task begin times stable across suspend
- Subject/lookup alias: [PATCH] tsacct: keep task begin times stable across suspend Performed after source, guided/history tracks and behavioral results. This is same-model adversarial review, not an external endorsement.
Source: 24d45a1475dd4c671feb1df705f67ef2fc293969.
Read the linked report for current findings, limitations and status.

### memfd_pin_folios initialization review

Record: [memfd-pin-folios-uninitialized-review.md](https://chatgpt.com/library?file_id=libfile_caa47b1b97a881918441dd7a146b398e&account_id=personal)
Library ID: `libfile_caa47b1b97a881918441dd7a146b398e`
Last saved: 2026-10-30T00:48:09.855492Z; source record version: read current version.
- Subject/lookup alias: [PATCH] mm/gup: don't pin uninitialized shmem folios in memfd_pin_folios()
Review ID: R-GUP-20261029
Author: Samiullah Khawaja <skhawaja@google.com>
Source: 72d3fcf802c45d00b300f25b848a93c3a2bd7c7e (v7.3-rc5).
Baseline and strongest counterarguments:
Read the linked report for current findings, limitations and status.

### [PATCH v2 00/47] mm: various (urgent?) fixes

Record: [R-055-review.md](https://chatgpt.com/library?file_id=libfile_c2fbe76a8b8881919feae1f43340b7ae&account_id=personal)
Library ID: `libfile_c2fbe76a8b8881919feae1f43340b7ae`
Last saved: 2026-10-30T00:33:53.555158Z; source record version: 1.
- Subject/lookup alias: [PATCH v2 00/47] mm: various (urgent?) fixes
- Subject/lookup alias: [PATCH v2 01/47] mm/mglru: don't use stack pointers when walking PUD and
- Subject/lookup alias: [PATCH v2 02/47] fork: take mmap_lock before copying mm_struct
- Subject/lookup alias: [PATCH v2 03/47] mm/memfd: check for real shmem inodes before accessing
- Subject/lookup alias: [PATCH v2 04/47] mm/memfd: make f_pos accesses atomic
- Subject/lookup alias: [PATCH v2 05/47] mm/truncate: look again if a folio left the mapping
- Subject/lookup alias: [PATCH v2 06/47] mm/filemap: read mapping->a_ops->free_folio under i_lock
- Subject/lookup alias: [PATCH v2 07/47] mm/filemap: don't lose a folio lock wakeup to a signal
- Subject/lookup alias: [PATCH v2 08/47] mm/filemap: finish fault cleanup before dropping the fault
- Subject/lookup alias: [PATCH v2 09/47] mm/rmap: handle device-exclusive entries in
- Subject/lookup alias: [PATCH v2 10/47] mm/huge_memory: fix list corruption when
- Subject/lookup alias: [PATCH v2 11/47] mm/huge_memory: properly handle refcounted PUD mappings on
Message-ID: 20261029-fixes_core-v2-0-a64ce7f83abb@kernel.org.
Author base: 65ba8f34ec886ec72b2c07ddc8cf3d815c32869d.
Read the linked report for current findings, limitations and status.

### [PATCH v3] ipc/msg: fix msg_qbytes truncation in IPC_SET

Record: [R-054-review.md](https://chatgpt.com/library?file_id=libfile_2ba8be1cfb84819193af227f696cd7e0&account_id=personal)
Library ID: `libfile_2ba8be1cfb84819193af227f696cd7e0`
Last saved: 2026-10-29T22:26:05.616971Z; source record version: read current version.
- Subject/lookup alias: [PATCH v3] ipc/msg: fix msg_qbytes truncation in IPC_SET
- Earlier Subject: [PATCH v2] ipc/msg: prevent msg_qbytes limit bypass in IPC_SET
Author base c339f4010dea8b0d754f84ace70cd1b089878ef8 verified.
Applied to `mm-nonmm-unstable` per mm-commits; the v3 source and
selftest are present there and in `mm-everything` at the 2026-11-15
branch-wide checkpoint. Read the linked report for findings and limits.

### [PATCH] ipc/msg: align compat version-0 msqid_ds with native IPC_OLD

Record: [R-053-review.md](https://chatgpt.com/library?file_id=libfile_5b7a960f751c819185ceae1dfd4eb33a&account_id=personal)
Library ID: `libfile_5b7a960f751c819185ceae1dfd4eb33a`
Last saved: 2026-10-29T18:23:20.990422Z; source record version: read current version.
- Subject/lookup alias: [PATCH] ipc/msg: align compat version-0 msqid_ds with native IPC_OLD
Source:24d45a1475dd4c671feb1df705f67ef2fc293969; Google/public tips agree,
Read the linked report for current findings, limitations and status.

### [PATCH v2] ipc/msg: prevent msg_qbytes limit bypass in IPC_SET

Record: [R-052-review.md](https://chatgpt.com/library?file_id=libfile_168fbeea10b081919bb75dfccc94c3a1&account_id=personal)
Library ID: `libfile_168fbeea10b081919bb75dfccc94c3a1`
Last saved: 2026-10-29T06:59:14.390683Z; source record version: read current version.
- Subject/lookup alias: [PATCH v2] ipc/msg: prevent msg_qbytes limit bypass in IPC_SET
Read the linked report for current findings, limitations and status.

### R-051: ALLOC_NOFRAGMENT watermark series

Record: [R-051-review.md](https://chatgpt.com/library?file_id=libfile_8f1323f943ec8191a42f206433ae570b&account_id=personal)
Library ID: `libfile_8f1323f943ec8191a42f206433ae570b`
Last saved: 2026-10-29T06:24:37.702833Z; source record version: read current version.
Source: author base d865f2677c44cb2171b833d6775cf692756fa8be, sequential
Read the linked report for current findings, limitations and status.

### R-050: ipc/msg: clamp negative MSG_INFO usage counts

Record: [R-050-review.md](https://chatgpt.com/library?file_id=libfile_03013de724108191a624122ee2c248c3&account_id=personal)
Library ID: `libfile_03013de724108191a624122ee2c248c3`
Last saved: 2026-10-29T04:04:45.836972Z; source record version: 1.
Source: mm-unstable 4685a28187f466adb03455ac903363f000ef6a89,
Read the linked report for current findings, limitations and status.

### R-049: ipc/msg percpu statistics saturation

Record: [R-049-review.md](https://chatgpt.com/library?file_id=libfile_7397cf57fe8c81919ac2026ed47cde21&account_id=personal)
Library ID: `libfile_7397cf57fe8c81919ac2026ed47cde21`
Last saved: 2026-10-28T23:48:42.960754Z; source record version: read current version.
Read the linked report for current findings, limitations and status.

### R-048: Lib fixes for 7.3

Record: [R-048-review.md](https://chatgpt.com/library?file_id=libfile_63c96122ec4c81918826326025fbb029&account_id=personal)
Library ID: `libfile_63c96122ec4c81918826326025fbb029`
Last saved: 2026-10-28T18:33:11.215758Z; source record version: 1.
Read the linked report for current findings, limitations and status.

### R-047: smaps_rollup RSS tearing-test review

Record: [R-047-review.md](https://chatgpt.com/library?file_id=libfile_842b69113e90819180a5bef696e14643&account_id=personal)
Library ID: `libfile_842b69113e90819180a5bef696e14643`
Last saved: 2026-10-28T05:57:17.333344Z; source record version: read current version.
Read the linked report for current findings, limitations and status.

### R-046: IPC_SET queue-capacity bypass

Record: [R-046-review.md](https://chatgpt.com/library?file_id=libfile_7c377b2390b08191819bf7d29492e5ee&account_id=personal)
Library ID: `libfile_7c377b2390b08191819bf7d29492e5ee`
Last saved: 2026-10-28T04:12:30.130759Z; source record version: 1.
Base: 8a36f53fd5ec3eff01f1b637d42cbdc3821d0493; exact preimages match.
Read the linked report for current findings, limitations and status.

### R-045: slab pages are not free pages

Record: [R-045-review.md](https://chatgpt.com/library?file_id=libfile_4082362f53088191a2c8e202a3e723a4&account_id=personal)
Library ID: `libfile_4082362f53088191a2c8e202a3e723a4`
Last saved: 2026-10-27T20:22:15.640239Z; source record version: read current version.
Source: 39274b454e9993cea319f4ac342a8082a9ee1730, fresh under 24h and
Read the linked report for current findings, limitations and status.

### R-043: swapoff WRITEOK cluster scans

Record: [swapoff-writeok-review.md](https://chatgpt.com/library?file_id=libfile_c68aac78c3d48191a5b922bda11235de&account_id=personal)
Library ID: `libfile_c68aac78c3d48191a5b922bda11235de`
Last saved: 2026-10-26T23:28:22.066253Z; source record version: read current version.
- Subject/lookup alias: [PATCH] mm, swap: stop cluster list scans once swapoff clears SWP_WRITEOK
Author: Mani Tofigh <mt4022@columbia.edu>
Read the linked report for current findings, limitations and status.

### R-042: F_SEAL_PUNCH_HOLE

Record: [R-042-review.md](https://chatgpt.com/library?file_id=libfile_dd2b09d354348191856eaa1e10f7f941&account_id=personal)
Library ID: `libfile_dd2b09d354348191856eaa1e10f7f941`
Last saved: 2026-10-26T22:41:42.820103Z; source record version: read current version.
Message-ID 20261026220546.3114241-1-skhawaja@google.com, 2026-10-26.
Read the linked report for current findings, limitations and status.

### Boyer-Moore ignore-case report investigation

Record: [ts-bm-ignorecase-review.md](https://chatgpt.com/library?file_id=libfile_b0e408d239f88191849c735e6f8d20e6&account_id=personal)
Library ID: `libfile_b0e408d239f88191849c735e6f8d20e6`
Last saved: 2026-10-26T22:04:42.122977Z; source record version: read current version.
- Subject/lookup alias: Bug in the Boyer-Moore search in lib/ts_bm.c
Read the linked report for current findings, limitations and status.

### R-040 - move_pages query address untagging

Record: [move-pages-untag-review.md](https://chatgpt.com/library?file_id=libfile_63d51f3af9908191988c13962c520576&account_id=personal)
Library ID: `libfile_63d51f3af9908191988c13962c520576`
Last saved: 2026-10-26T00:18:39.448096Z; source record version: 2.
- Subject/lookup alias: [PATCH] mm/migrate: untag addresses when querying page nodes
Author: Hungyu Lin <dennylin0707@gmail.com>
Source: a2abad0d7f453cc9902fc8bf7b871db5563a652c (mm-unstable).
Read the linked report for current findings, limitations and status.

### R-039 - automatic interleave weights after memory hotplug

Record: [mempolicy-auto-hotplug-review.md](https://chatgpt.com/library?file_id=libfile_b796abb92fe08191942647da6468de25&account_id=personal)
Library ID: `libfile_b796abb92fe08191942647da6468de25`
Last saved: 2026-10-25T20:00:16.259200Z; source record version: 1.
- Subject/lookup alias: [PATCH] mm/mempolicy: recompute automatic interleave weights on memory hotplug
Author: Gregory Price (Meta) <gourry@gourry.net>
Read the linked report for current findings, limitations and status.

### filemap_invalidate_inode(): discarded invalidation errors

Record: [filemap-invalidate-errors-review.md](https://chatgpt.com/library?file_id=libfile_93a59c284d708191aa4ff0b4ec28864b&account_id=personal)
Library ID: `libfile_93a59c284d708191aa4ff0b4ec28864b`
Last saved: 2026-10-25T00:53:28.862540Z; source record version: read current version.
- Subject/lookup alias: filemap_invalidate_inode() - losing -EBUSY from invalidate_inode_pages2_range?
Read the linked report for current findings, limitations and status.

### R-037: fat: hold truncate_lock in fat_write_failed()

Record: [fat-write-failed-review.md](https://chatgpt.com/library?file_id=libfile_402d993948f081918fe9aa660132ee3e&account_id=personal)
Library ID: `libfile_402d993948f081918fe9aa660132ee3e`
Last saved: 2026-10-24T23:21:27.229143Z; source record version: read current version.
Read the linked report for current findings, limitations and status.

### R-036 — lib/group_cpus: snapshot cluster masks to keep grouping hotplug invariant

Record: [group-cpus-snapshot-review.md](https://chatgpt.com/library?file_id=libfile_0e1d5e9f971c8191a778ad2152acd51c&account_id=personal)
Library ID: `libfile_0e1d5e9f971c8191a778ad2152acd51c`
Last saved: 2026-10-24T08:15:32.437813Z; source record version: read current version.
Read the linked report for current findings, limitations and status.

### R-036: lib/group_cpus snapshot review history

Current v7 record: [group-cpus-snapshot-v7-review.md](https://chatgpt.com/library?file_id=libfile_b908cd45e1188191af1e57726bd6f503&account_id=personal)
Library ID: `libfile_b908cd45e1188191af1e57726bd6f503`.
Exact subject: [PATCH v7] lib/group_cpus: Snapshot cluster masks to keep grouping hotplug invariant.
Message-ID: `20261110174513.461743-1-Vishal.Badole@amd.com`.
No identified source defect; gate cannot certify under the no-apply policy.
Submitted mail: `reports/evidence/group-cpus-snapshot-v7.patch`.

Historical v5 record:

Record: [group-cpus-snapshot-r036-review.md](https://chatgpt.com/library?file_id=libfile_de335af8840c8191ace554eaf62c07bb&account_id=personal)
Library ID: `libfile_de335af8840c8191ace554eaf62c07bb`
Last saved: 2026-10-30T01:17:41.689210Z; source record version: 1.
- Subject/lookup alias: [PATCH v5] lib/group_cpus: Snapshot cluster masks to keep grouping hotplug invariant
Read the linked report for current findings, limitations and status.

### R-035 — KSM soft-dirty v3, reassessment of R-015

Record: [ksm-softdirty-v3-review.md](https://chatgpt.com/library?file_id=libfile_93e82df48d248191b50cd8e25d4c8bd3&account_id=personal)
Library ID: `libfile_93e82df48d248191b50cd8e25d4c8bd3`
Last saved: 2026-10-24T05:12:50.277693Z; source record version: read current version.
Source: `mbox(20261024-050607)` (20 messages); v3 is message 2,
Message-ID <20261021182157.1873726-1-samarth.colleges@gmail.com>.
Read the linked report for current findings, limitations and status.

Identical-content alias for ksm-softdirty-v3-review.md: [ksm-softdirty-v3-r035-review.md](https://chatgpt.com/library?file_id=libfile_e1d2e20008ec8191b3ee4b70f1088d5d&account_id=personal).

### R-034 — verification of Tejun Heo's review (2026-10-23)

Record: [tejun-feedback-review.md](https://chatgpt.com/library?file_id=libfile_aabe6a9962f48191a2006c2e329c84c1&account_id=personal)
Library ID: `libfile_aabe6a9962f48191a2006c2e329c84c1`
Last saved: 2026-10-23T23:36:53.748631Z; source record version: read current version.
- Subject/lookup alias: Re: [PATCH] selftests/cgroup: convert cg_read_key_*() helpers to s64
Read the linked report for current findings, limitations and status.

Identical-content alias for tejun-feedback-review.md: [r034-tejun-feedback-review.md](https://chatgpt.com/library?file_id=libfile_de5703764a488191ade268b0c2f535de&account_id=personal).

### R-034 — selftests/cgroup: convert cg_read_key_*() helpers to s64

Record: [cgroup-s64-review.md](https://chatgpt.com/library?file_id=libfile_fc19acb9d860819181b6fc47d9894179&account_id=personal)
Library ID: `libfile_fc19acb9d860819181b6fc47d9894179`
Last saved: 2026-10-23T23:21:29.857140Z; source record version: read current version.
Source: `Pasted text(20261023-231457).txt`, one standalone patch.
Read the linked report for current findings, limitations and status.

### R-034 — selftests/cgroup: convert cg_read_key_*() helpers to s64

Record: [cgroup-s64-review.md](https://chatgpt.com/library?file_id=libfile_1d4e86da6bfc8191b95efd253c2b5374&account_id=personal)
Library ID: `libfile_1d4e86da6bfc8191b95efd253c2b5374`
Last saved: 2026-10-23T23:36:10.363791Z; source record version: 1.
- Subject/lookup alias: Re: [PATCH] selftests/cgroup: convert cg_read_key_*() helpers to s64
Source: `Pasted text(20261023-231457).txt`, one standalone patch.
Read the linked report for current findings, limitations and status.

### R-033: memcontrol high_work on dying memcg

Record: [memcontrol-high-work-dying-memcg-review.md](https://chatgpt.com/library?file_id=libfile_3775aa6ce6248191b1b62f73e23d843e&account_id=personal)
Library ID: `libfile_3775aa6ce6248191b1b62f73e23d843e`
Last saved: 2026-10-23T23:06:37.292616Z; source record version: read current version.
- Subject/lookup alias: [PATCH] mm: memcontrol: fix NULL pointer deref in high_work_func() on dying memcg
Base: 2bba28e98578de622ef307d00875aa8f8bca3d10.
Read the linked report for current findings, limitations and status.

### R-032: memcg per-node cacheline contention, v3 (2 patches)

Record: [memcg-lruvec-cacheline-review.md](https://chatgpt.com/library?file_id=libfile_6169471adf788191818d49f0137bc2c3&account_id=personal)
Library ID: `libfile_6169471adf788191818d49f0137bc2c3`
Last saved: 2026-10-23T22:09:58.234478Z; source record version: read current version.
Author base-commit: fcec4f4bcc1101dbd7e3aff267856b3bbfe128c6
Message-IDs:
Read the linked report for current findings, limitations and status.

### R-031: mm: avoid losing atomic VMA flags (4-patch series)

Record: [r031-vma-atomic-flags-series-review.md](https://chatgpt.com/library?file_id=libfile_d22d60e20ac481919266989490a4aafe&account_id=personal)
Library ID: `libfile_d22d60e20ac481919266989490a4aafe`
Last saved: 2026-10-23T18:35:07.200114Z; source record version: read current version.
Read the linked report for current findings, limitations and status.

### R-030: mm/vma mixedmap expansion review

Record: [vma-mixedmap-expansion-review.md](https://chatgpt.com/library?file_id=libfile_1987fa54e2b481919c1b0b049ba9f8ec&account_id=personal)
Library ID: `libfile_1987fa54e2b481919c1b0b049ba9f8ec`
Last saved: 2026-10-23T17:46:40.926930Z; source record version: read current version.
- Subject/lookup alias: [PATCH] mm/vma: fix expansion of VMA_MIXEDMAP_BIT VMAs
Author: Lorenzo Stoakes (ARM) <ljs@kernel.org>
Base: 2bba28e98578de622ef307d00875aa8f8bca3d10
Read the linked report for current findings, limitations and status.

Identical-content alias for vma-mixedmap-expansion-review.md: [vma-mixedmap-expansion-review.md](https://chatgpt.com/library?file_id=libfile_a24e1bf7b4188191b0d1dbfa653c500a&account_id=personal).

### R-029: misplaced-migration source nid, rechecked

Record: [migrate-misplaced-src-nid-review.md](https://chatgpt.com/library?file_id=libfile_38ccae6dc1e08191ab3c39c1cd89fe4a&account_id=personal)
Library ID: `libfile_38ccae6dc1e08191ab3c39c1cd89fe4a`
Last saved: 2026-10-23T05:38:22.292068Z; source record version: 4.
Author: Yafang Shao <laoar.shao@gmail.com>. Subject: "mm/migrate: snapshot
Read the linked report for current findings, limitations and status.

### R-027: mm/zswap: validate dlen and normalize comp_ret on compression success

Record: [zswap-acomp-dlen-review.md](https://chatgpt.com/library?file_id=libfile_9ed246b62634819183ea70442cb2af14&account_id=personal)
Library ID: `libfile_9ed246b62634819183ea70442cb2af14`
Last saved: 2026-10-23T04:33:55.315361Z; source record version: read current version.
Read the linked report for current findings, limitations and status.

### R-028: HugeTLB UFFD poison marker and PMD sharing after unregister

Record: [hugetlb-uffd-pmd-share-review.md](https://chatgpt.com/library?file_id=libfile_de2e47704648819185076c92b736df0d&account_id=personal)
Library ID: `libfile_de2e47704648819185076c92b736df0d`
Last saved: 2026-10-23T04:33:55.264661Z; source record version: read current version.
Read the linked report for current findings, limitations and status.

### R-026: mm/vmalloc: reject overflowing vm_map_ram page counts

Record: [vm-map-ram-overflow-review.md](https://chatgpt.com/library?file_id=libfile_2c96f2fb045481919d7ea8174e003dde&account_id=personal)
Library ID: `libfile_2c96f2fb045481919d7ea8174e003dde`
Last saved: 2026-10-23T01:15:26.909402Z; source record version: read current version.
Author: Shubhang Kaushik (Ampere) <sh@gentwo.org>
Base: 7be4bc52fd9e0e55dc9a2e0232b89427d2c4b614
Read the linked report for current findings, limitations and status.

Identical-content alias for vm-map-ram-overflow-review.md: [vm-map-ram-overflow-review.md](https://chatgpt.com/library?file_id=libfile_498a7d2ee5f481918cba085a7d8baf92&account_id=personal).

### R-025: Hugetlb reserved-folio cgroup charging review

Record: [hugetlb-reserve-charge-review.md](https://chatgpt.com/library?file_id=libfile_e6399cff60ec819192f3ac4a6dd0e747&account_id=personal)
Library ID: `libfile_e6399cff60ec819192f3ac4a6dd0e747`
Last saved: 2026-10-21T23:35:25.021047Z; source record version: read current version.
- Subject/lookup alias: [PATCH] mm/hugetlb: charge hugetlb cgroup and memcg in alloc_hugetlb_folio_reserve()
Author: Hongfu Li <lihongfu@kylinos.cn>
Base: 2887e63d2e8e0cf55402612d8996ce955a2c3e55
Author-reported counter values are consistent with this bypass but
Read the linked report for current findings, limitations and status.

### R-024: delayacct TGID delay extrema aggregation

Record: [delayacct-extrema-review.md](https://chatgpt.com/library?file_id=libfile_5ebe5f1064048191b369613b688ad1d6&account_id=personal)
Library ID: `libfile_5ebe5f1064048191b369613b688ad1d6`
Last saved: 2026-10-21T22:52:56.610911Z; source record version: read current version.
- Subject/lookup alias: [PATCH] delayacct: Preserve delay extrema when aggregating taskstats
Author: Hungyu Lin <dennylin0707@gmail.com>
Author supplied no testing evidence in this patch message.
Read the linked report for current findings, limitations and status.

### R-023: firmware-table subtable bounds - v2 review

Record: [fw-table-review.md](https://chatgpt.com/library?file_id=libfile_86e71d1054a0819183134dad739d9fc0&account_id=personal)
Library ID: `libfile_86e71d1054a0819183134dad739d9fc0`
Last saved: 2026-10-21T22:29:44.894944Z; source record version: 1.
- Subject/lookup alias: [PATCH v2] lib/firmware_table: validate subtable bounds
Author: Jiale Yao <yaojiale02@163.com>
Read the linked report for current findings, limitations and status.

Identical-content alias for fw-table-review.md: [fw-table-review.md](https://chatgpt.com/library?file_id=libfile_1df900aa4240819191f14a3fa1fe1df8&account_id=personal).

### R-015: KSM soft-dirty - mailing-list feedback reconciliation

Record: [ksm-soft-dirty-review.md](https://chatgpt.com/library?file_id=libfile_b8697823b13c819192ce273c9dc76ce7&account_id=personal)
Library ID: `libfile_b8697823b13c819192ce273c9dc76ce7`
Last saved: 2026-10-21T21:54:04.549494Z; source record version: 2.
- Subject/lookup alias: Re: [PATCH v2] mm/ksm: keep soft-dirty and uffd-wp when merging a page
- Subject/lookup alias: [PATCH v3] mm/ksm: keep soft-dirty when merging a page
Source: user-supplied mailbox grabbed(3), decoded with Python's mailbox
Message-ID: <sashiko-outbox-177114@kernel.org>
Message-ID: <efa6a28c-f0f9-4d1e-9cce-fec2c08e7d9f@kernel.org>
Message-ID: <167a14f0-6a6f-4db1-a34b-905a33d5290d@linux.dev>
Read the linked report for current findings, limitations and status.

### profile: simplify /proc/profile read layout - review feedback

Record: [profile-read-review.md](https://chatgpt.com/library?file_id=libfile_a366f099e6d48191ac00e85ddb9a6031&account_id=personal)
Library ID: `libfile_a366f099e6d48191ac00e85ddb9a6031`
Last saved: 2026-10-21T01:31:07.990128Z; source record version: 1.
Source: torvalds/linux f47d223627f80cb7a1eb14c585fe6cb35de5e984,
Read the linked report for current findings, limitations and status.

### R-038: page allocation tag initialization, v2

Record: [page-alloc-hotplug-tag-review.md](https://chatgpt.com/library?file_id=libfile_f7ca9942a6ec819180237ae4adf66052&account_id=personal)
Library ID: `libfile_f7ca9942a6ec819180237ae4adf66052`
Last saved: 2026-10-25T03:42:15.444606Z; source record version: 3.
Read the linked report for current findings, limitations and status.

### R-020: compat: Avoid double rounding in times()

Record: [compat-times-review.md](https://chatgpt.com/library?file_id=libfile_fe6878b1ab8c8191aec8afd71f7523d7&account_id=personal)
Library ID: `libfile_fe6878b1ab8c8191aec8afd71f7523d7`
Last saved: 2026-10-20T21:23:49.722635Z; source record version: read current version.
Author: Hungyu Lin <dennylin0707@gmail.com>
Base: f47d223627f80cb7a1eb14c585fe6cb35de5e984
Read the linked report for current findings, limitations and status.

### R-019: mm/memcontrol stock CSS lifetime review

Record: [memcontrol-stock-review.md](https://chatgpt.com/library?file_id=libfile_d8f7b0270f4081919443dbbff3002697&account_id=personal)
Library ID: `libfile_d8f7b0270f4081919443dbbff3002697`
Last saved: 2026-10-21T02:40:03.716504Z; source record version: 2.
Author: Joshua Hahn. Patch: memcontrol-stock-submission.patch.
Read the linked report for current findings, limitations and status.

### R-019: mm/memcontrol stock CSS lifetime review

Record: [memcontrol-stock-review.md](https://chatgpt.com/library?file_id=libfile_a8abdcde40408191a4a23f872448290b&account_id=personal)
Library ID: `libfile_a8abdcde40408191a4a23f872448290b`
Last saved: 2026-10-20T19:55:16.883353Z; source record version: 5.
Author: Joshua Hahn. Patch: memcontrol-stock-submission.patch.
Read the linked report for current findings, limitations and status.

### Review: mm/hugetlb_cgroup: prevent use-after-free during offlining

Record: [hugetlb-cgroup-review(1).md](https://chatgpt.com/library?file_id=libfile_9b28a26588208191984b0bfcb0b22984&account_id=personal)
Library ID: `libfile_9b28a26588208191984b0bfcb0b22984`
Last saved: 2026-10-20T18:53:24.567937Z; source record version: read current version.
Review key: R-018. Author: Daehyeon Ko. Date: 2026-10-20.
Read the linked report for current findings, limitations and status.

### Review: fs/proc/task_mmu: pin mm_users in do_pagemap_scan()

Record: [task-mmu-review(1).md](https://chatgpt.com/library?file_id=libfile_7a7555dfc00c819192c4d449801a02ae&account_id=personal)
Library ID: `libfile_7a7555dfc00c819192c4d449801a02ae`
Last saved: 2026-10-20T18:53:24.219401Z; source record version: read current version.
Review key: R-017. Author: Ngoc Quy. Date: 2026-10-14.
Base: 24a19b953e2a3d0ea5a8c4951a0ab8f32720c907.
Read the linked report for current findings, limitations and status.

### R-016: Memoryless-node demotion target reset

Record: [memory-tiers-review(1).md](https://chatgpt.com/library?file_id=libfile_c1ca7d19b1548191ac3061fc69df3114&account_id=personal)
Library ID: `libfile_c1ca7d19b1548191ac3061fc69df3114`
Last saved: 2026-10-20T18:53:24.150862Z; source record version: read current version.
- Subject/lookup alias: [PATCH] mm/memory-tiers: reset demotion targets of nodes without memory
Author: Gregory Price
Read the linked report for current findings, limitations and status.

Identical-content alias for hugetlb-cgroup-review(1).md: [hugetlb-cgroup-review.md](https://chatgpt.com/library?file_id=libfile_0371cecf88b4819199fdfabff5bd3951&account_id=personal).

Identical-content alias for task-mmu-review(1).md: [task-mmu-review.md](https://chatgpt.com/library?file_id=libfile_c063d398b8b08191ae4e8df87fb64172&account_id=personal).

Identical-content alias for memory-tiers-review(1).md: [memory-tiers-review.md](https://chatgpt.com/library?file_id=libfile_d393aeb20c7c81919cdd00f54c8cec94&account_id=personal).

### Review: mm: various (urgent?) fixes, [PATCH 00/10]

Record: [REVIEW.md](https://chatgpt.com/library?file_id=libfile_99010e28b0e88191940fab2810e52e9e&account_id=personal)
Library ID: `libfile_99010e28b0e88191940fab2810e52e9e`
Last saved: 2026-10-16T02:59:15.628138Z; source record version: read current version.
Base commit: 0fcb05b72344f40806cbe810de8872f1698bf053
Read the linked report for current findings, limitations and status.

### Deferred: mmap read-around recovery after sparse faults

Record: [mmap-readaround-regression-followup.md](https://chatgpt.com/library?file_id=libfile_361f3ccaed6881919ed217f52b21cf6f&account_id=personal)
Library ID: `libfile_361f3ccaed6881919ed217f52b21cf6f`
Last saved: 2026-11-06T00:18:40.754819Z; source record version: read current version.
- Subject/lookup alias: [REGRESSION] mm/filemap: mmap read-around stays off for an open file after sparse faults, since 7.2
- Subject/lookup alias: [PATCH 1/2] mm/filemap: read ahead downwards on descending VM_HUGEPAGE faults
- Subject/lookup alias: Re: [REGRESSION] mm/filemap: mmap read-around stays off for an open file after sparse faults, since 7.2
Author: fujunjie <fujunjie1@qq.com>. Jan Kara and Vishal Moola reviewed.
Read the linked report for current findings, limitations and status.

### R-044: lib/ts_bm TS_IGNORECASE

Record: [R-044-ts-bm-ignorecase.md](https://chatgpt.com/library?file_id=libfile_59dd0e86f7d48191910773e7c4f04e0c&account_id=personal)
Library ID: `libfile_59dd0e86f7d48191910773e7c4f04e0c`
Last saved: 2026-10-27T18:23:06.471139Z; source record version: read current version.
Base: 21a7f44fd0765fcc5194130b28767786eba1d1e7.
Read the linked report for current findings, limitations and status.

## Ledger-only records and historical follow-ups

These are saved review entries, not a reconstruction from submitted mail.
Read the entire entry and later corrections; headings are lookup labels.

### R-001

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 453.
- Subject/lookup alias: mm/mglru: fix using folio_mark_accessed to replace folio_set_active

### R-002

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 488.
- Subject/lookup alias: mm: multi-gen LRU: fix NULL lruvec->pgdat deref with memcg disabled on cmdline

### R-003

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 564.
- Subject/lookup alias: mm/vma: avoid spurious write locks when mm->mm_lock_seq overflows

### R-004

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 595.
- Subject/lookup alias: mm/ksm: keep smart scan from losing duplicate pages

### R-005

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 618.
- Subject/lookup alias: ipc/sem: account enlarged sops arrays to memcg

### R-006

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 641.
- Subject/lookup alias: mm/vmalloc: read vm_map_ram block regions from the requested offset

### R-007

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 705.
- Subject/lookup alias: proc/kcore: advance the vmalloc retry by the last copy, not the total

### R-008

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 742.
- Subject/lookup alias: mm/mremap: do not charge a shrinking move twice

### L-001

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 799.
- Subject/lookup alias: mm: retry page faults once under the per-VMA lock

### R-009

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 841.
- Subject/lookup alias: ucount: take the rlimit reference before checking the limit
- Subject/lookup alias: [PATCH v2] uses base c03c1a14507dfaf8b856c2608f9ac216021fc222;

### R-010

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 930.
- Subject/lookup alias: lib/buildid: reject file offsets that do not fit in pgoff_t

### R-011

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 983.
- Subject/lookup alias: mm/mempolicy: apply bind policies against the scoped allocation zone

### R-012

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1033.
- Subject/lookup alias: khugepaged: fix readahead lock inversion in collapse_file()

### R-013

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1129.
- Subject/lookup alias: zram: redesign zcomp and rework backends

### R-014

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1196.
- Subject/lookup alias: kasan: fix runtime shadow page table synchronization
- Subject/lookup alias: [PATCH v2] kasan: fix runtime shadow page table synchronization

### R-015

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1277.
- Subject/lookup alias: mm/ksm: keep soft-dirty and uffd-wp when merging a page
- Subject/lookup alias: [PATCH v3] mm/ksm: keep soft-dirty when merging a page. Base fcec4f4bcc1101dbd7e3aff267856b3bbfe128c6; mm/ksm.c preimage dbfb8f98b18925c729d0931760a18f491d0fb156.

### R-016

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1454.
- Subject/lookup alias: mm/memory-tiers: reset demotion targets of nodes without memory

### R-017

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1503.
- Subject/lookup alias: fs/proc/task_mmu: pin mm_users in do_pagemap_scan()

### R-018

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1601.
- Subject/lookup alias: mm/hugetlb_cgroup: prevent use-after-free during cgroup offlining

### R-019

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1665.
- Subject/lookup alias: mm/memcontrol: publish null pointer before dropping css reference

### R-020

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1732.
- Subject/lookup alias: compat: Avoid double rounding in times()

### R-021

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1751.
- Subject/lookup alias: mm/page_alloc: clear page tag refs when onlining hotplugged memory

### R-019 v2 reassessment (2026-10-20)

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1791.

### R-023

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1809.
- Subject/lookup alias: lib/firmware_table: validate subtable bounds

### R-024

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1851.
- Subject/lookup alias: delayacct: Preserve delay extrema when aggregating taskstats

### R-022: profile: simplify /proc/profile read layout - Sashiko feedback

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1895.

### R-019 follow-up: slot generation counterexample (2026-10-20)

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1918.

### R-025

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1935.
- Subject/lookup alias: [PATCH] mm/hugetlb: charge hugetlb cgroup and memcg in alloc_hugetlb_folio_reserve()

### R-026

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 1984.
- Subject/lookup alias: mm/vmalloc: reject overflowing vm_map_ram page counts

### R-027

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2014.
- Subject/lookup alias: mm/zswap: validate dlen and normalize comp_ret on compression success

### R-028

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2051.
- Subject/lookup alias: mm/hugetlb: disable PMD sharing for UFFD missing mode

### R-029

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2087.
- Subject/lookup alias: mm/migrate: snapshot the source nid before the misplaced migration

### R-029 audit scope and limitations

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2228.

### R-029 maintainer feedback (2026-10-22 PT)

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2251.

### R-030

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2300.
- Subject/lookup alias: mm/vma: fix expansion of VMA_MIXEDMAP_BIT VMAs

### R-031: mm: avoid losing atomic VMA flags (four-patch series)

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2356.

### R-032: memcg per-node cacheline contention, v3 [1/2]+[2/2]

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2462.

### R-033: memcontrol high_work on dying memcg

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2545.
- Subject/lookup alias: [PATCH] mm: memcontrol: fix NULL pointer deref in high_work_func() on dying memcg.

### R-034: cgroup keyed selftest counters to s64

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2619.
- Subject/lookup alias: [PATCH] selftests/cgroup: convert cg_read_key_*() helpers to s64. One standalone patch; explicitly rebased on mm-stable.

### R-034: Tejun Heo review reconciliation and correction

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2698.

### R-035: mm/ksm: keep soft-dirty when merging a page (v3)

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2768.

### R-036: lib/group_cpus: snapshot cluster masks to keep grouping hotplug invariant

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2833.

### R-037: FAT failed-write truncation locking (2026-10-24)

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 2954.
- Subject/lookup alias: [PATCH] fat: hold truncate_lock in fat_write_failed()

### Unnumbered: filemap_invalidate_inode error report (2026-10-25 UTC)

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal); line 3044.
- Subject/lookup alias: filemap_invalidate_inode() - losing -EBUSY from invalidate_inode_pages2_range?

### R-001

Source: [review-activity .md](https://chatgpt.com/library?file_id=libfile_8bc15eac2b6481918a342889cb4d85a1&account_id=personal); line 120.
- Subject/lookup alias: mm/mglru: fix using folio_mark_accessed to replace folio_set_active

### R-002

Source: [review-activity .md](https://chatgpt.com/library?file_id=libfile_8bc15eac2b6481918a342889cb4d85a1&account_id=personal); line 155.
- Subject/lookup alias: mm: multi-gen LRU: fix NULL lruvec->pgdat deref with memcg disabled on cmdline

### R-003

Source: [review-activity .md](https://chatgpt.com/library?file_id=libfile_8bc15eac2b6481918a342889cb4d85a1&account_id=personal); line 231.
- Subject/lookup alias: mm/vma: avoid spurious write locks when mm->mm_lock_seq overflows

### R-004

Source: [review-activity .md](https://chatgpt.com/library?file_id=libfile_8bc15eac2b6481918a342889cb4d85a1&account_id=personal); line 262.
- Subject/lookup alias: mm/ksm: keep smart scan from losing duplicate pages

### R-005

Source: [review-activity .md](https://chatgpt.com/library?file_id=libfile_8bc15eac2b6481918a342889cb4d85a1&account_id=personal); line 285.
- Subject/lookup alias: ipc/sem: account enlarged sops arrays to memcg

### R-006

Source: [review-activity .md](https://chatgpt.com/library?file_id=libfile_8bc15eac2b6481918a342889cb4d85a1&account_id=personal); line 308.
- Subject/lookup alias: mm/vmalloc: read vm_map_ram block regions from the requested offset

### A-001

Source: [review-activity-2026-10-16.md](https://chatgpt.com/library?file_id=libfile_21fe7ea97cac8191b05bb885420731a6&account_id=personal); line 8.
- Subject/lookup alias: mm: various (urgent?) fixes
- Subject/lookup alias: [PATCH 00/10] mm: various (urgent?) fixes

### R-001

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_54f63cce6ad8819192eb095bd120722d&account_id=personal); line 109.
- Subject/lookup alias: mm/mglru: fix using folio_mark_accessed to replace folio_set_active

### R-002

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_54f63cce6ad8819192eb095bd120722d&account_id=personal); line 144.
- Subject/lookup alias: mm: multi-gen LRU: fix NULL lruvec->pgdat deref with memcg disabled on cmdline

### R-003

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_54f63cce6ad8819192eb095bd120722d&account_id=personal); line 185.
- Subject/lookup alias: mm/vma: avoid spurious write locks when mm->mm_lock_seq overflows

### R-004

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_54f63cce6ad8819192eb095bd120722d&account_id=personal); line 216.
- Subject/lookup alias: mm/ksm: keep smart scan from losing duplicate pages

### R-005

Source: [review-activity.md](https://chatgpt.com/library?file_id=libfile_54f63cce6ad8819192eb095bd120722d&account_id=personal); line 239.
- Subject/lookup alias: ipc/sem: account enlarged sops arrays to memcg

### R-001

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 394.
- Subject/lookup alias: mm/mglru: fix using folio_mark_accessed to replace folio_set_active

### R-002

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 429.
- Subject/lookup alias: mm: multi-gen LRU: fix NULL lruvec->pgdat deref with memcg disabled on cmdline

### R-003

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 505.
- Subject/lookup alias: mm/vma: avoid spurious write locks when mm->mm_lock_seq overflows

### R-004

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 536.
- Subject/lookup alias: mm/ksm: keep smart scan from losing duplicate pages

### R-005

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 559.
- Subject/lookup alias: ipc/sem: account enlarged sops arrays to memcg

### R-006

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 582.
- Subject/lookup alias: mm/vmalloc: read vm_map_ram block regions from the requested offset

### R-007

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 646.
- Subject/lookup alias: proc/kcore: advance the vmalloc retry by the last copy, not the total

### R-008

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 683.
- Subject/lookup alias: mm/mremap: do not charge a shrinking move twice

### L-001

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 740.
- Subject/lookup alias: mm: retry page faults once under the per-VMA lock

### R-009

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 782.
- Subject/lookup alias: ucount: take the rlimit reference before checking the limit
- Subject/lookup alias: [PATCH v2] uses base c03c1a14507dfaf8b856c2608f9ac216021fc222;

### R-010

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 871.
- Subject/lookup alias: lib/buildid: reject file offsets that do not fit in pgoff_t

### R-011

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 924.
- Subject/lookup alias: mm/mempolicy: apply bind policies against the scoped allocation zone

### R-012

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 974.
- Subject/lookup alias: khugepaged: fix readahead lock inversion in collapse_file()

### R-013

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1070.
- Subject/lookup alias: zram: redesign zcomp and rework backends

### R-014

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1137.
- Subject/lookup alias: kasan: fix runtime shadow page table synchronization
- Subject/lookup alias: [PATCH v2] kasan: fix runtime shadow page table synchronization

### R-015

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1218.
- Subject/lookup alias: mm/ksm: keep soft-dirty and uffd-wp when merging a page
- Subject/lookup alias: [PATCH v3] mm/ksm: keep soft-dirty when merging a page. Base fcec4f4bcc1101dbd7e3aff267856b3bbfe128c6; mm/ksm.c preimage dbfb8f98b18925c729d0931760a18f491d0fb156.

### R-016

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1395.
- Subject/lookup alias: mm/memory-tiers: reset demotion targets of nodes without memory

### R-017

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1444.
- Subject/lookup alias: fs/proc/task_mmu: pin mm_users in do_pagemap_scan()

### R-018

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1542.
- Subject/lookup alias: mm/hugetlb_cgroup: prevent use-after-free during cgroup offlining

### R-019

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1622.
- Subject/lookup alias: mm/memcontrol: publish null pointer before dropping css reference

### R-020

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1689.
- Subject/lookup alias: compat: Avoid double rounding in times()

### R-021

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1708.
- Subject/lookup alias: mm/page_alloc: clear page tag refs when onlining hotplugged memory

### R-019 v2 reassessment (2026-10-20)

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1748.

### R-023

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1766.
- Subject/lookup alias: lib/firmware_table: validate subtable bounds

### R-024

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1808.
- Subject/lookup alias: delayacct: Preserve delay extrema when aggregating taskstats

### R-022: profile: simplify /proc/profile read layout - Sashiko feedback

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1852.

### R-019 follow-up: slot generation counterexample (2026-10-20)

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1875.

### R-025

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1892.
- Subject/lookup alias: [PATCH] mm/hugetlb: charge hugetlb cgroup and memcg in alloc_hugetlb_folio_reserve()

### R-026

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1941.
- Subject/lookup alias: mm/vmalloc: reject overflowing vm_map_ram page counts

### R-027

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 1971.
- Subject/lookup alias: mm/zswap: validate dlen and normalize comp_ret on compression success

### R-028

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 2008.
- Subject/lookup alias: mm/hugetlb: disable PMD sharing for UFFD missing mode

### R-029

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 2044.
- Subject/lookup alias: mm/migrate: snapshot the source nid before the misplaced migration

### R-029 audit scope and limitations

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 2185.

### R-029 maintainer feedback (2026-10-22 PT)

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 2208.

### R-030

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 2257.
- Subject/lookup alias: mm/vma: fix expansion of VMA_MIXEDMAP_BIT VMAs

### R-031: mm: avoid losing atomic VMA flags (four-patch series)

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 2313.

### R-032: memcg per-node cacheline contention, v3 [1/2]+[2/2]

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 2419.

### R-033: memcontrol high_work on dying memcg

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 2502.
- Subject/lookup alias: [PATCH] mm: memcontrol: fix NULL pointer deref in high_work_func() on dying memcg.

### R-034: cgroup keyed selftest counters to s64

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 2576.
- Subject/lookup alias: [PATCH] selftests/cgroup: convert cg_read_key_*() helpers to s64. One standalone patch; explicitly rebased on mm-stable.

### R-034: Tejun Heo review reconciliation and correction

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 2655.

### R-035: mm/ksm: keep soft-dirty when merging a page (v3)

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 2725.

### R-036: lib/group_cpus: snapshot cluster masks to keep grouping hotplug invariant

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 2790.

### R-037: FAT failed-write truncation locking (2026-10-24)

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 2911.
- Subject/lookup alias: [PATCH] fat: hold truncate_lock in fat_write_failed()

### Unnumbered: filemap_invalidate_inode error report (2026-10-25 UTC)

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 3001.
- Subject/lookup alias: filemap_invalidate_inode() - losing -EBUSY from invalidate_inode_pages2_range?

### R-038: page allocation tag initialization, v2

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 3075.

### R-038 follow-up: tools and delivery (2026-10-25 UTC)

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 3156.

### R-039 - automatic interleave hotplug refresh (2026-10-25 PDT)

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 3211.
- Subject/lookup alias: [PATCH] mm/mempolicy: recompute automatic interleave weights on memory hotplug

### R-039-C3 follow-up: standalone reducer fix (2026-10-25 PDT)

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 3325.
- Subject/lookup alias: mm/mempolicy: use one node set for interleave weights This is development on R-039-C3, not a new numbered author submission. R-039 and its C1/C2 findings remain HOLD, along with earlier HOLD cases.

### R-040 - move_pages query untagging (2026-10-25 PDT)

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 3399.
- Subject/lookup alias: [PATCH] mm/migrate: untag addresses when querying page nodes

### R-040 reply correction (2026-10-25 PDT)

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 3552.

### R-041: hugetlbfs F_SEAL_EXEC setattr review

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 3575.

### R-041 evidence and continuity checkpoint

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 3830.

### Unnumbered investigation: Boyer-Moore ignore-case misses

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 3864.

### R-042: F_SEAL_PUNCH_HOLE

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 3940.

### R-042-C1: live update rejects the new seal

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 3971.

### R-042-C2: ordinary fallocate rollback can detach an iommufd pin

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 4006.

### R-043

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 4362.
- Subject/lookup alias: [[RFC PATCH]] powercap: idle_inject: Create per-CPU threads on registration

### R-044

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 4390.
- Subject/lookup alias: [PATCH v4] mm/migrate_device: consolidate compound folio handling

### R-045

Source: [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal); line 4414.
- Subject/lookup alias: [PATCH] fs/proc/task_mmu: check THP exclusivity for each subpage

## Supporting archives and embedded review records

Submission subjects below are search aliases, NOT proof that each message
was reviewed. Use the named review/closure member to establish scope.

### vmemmap-review-evidence.zip

Evidence: [vmemmap-review-evidence.zip](https://chatgpt.com/library?file_id=libfile_3e4ddfe68ec481919d03e7d0d4068ad3&account_id=personal)
Library ID: `libfile_3e4ddfe68ec481919d03e7d0d4068ad3`
- Review member: `vmemmap-review/review.md`
- Submission/report subject: [PATCH v4 00/13] mm: Decouple folio-based vmemmap optimization from HugeTLB
- Submission/report subject: [PATCH] mm/hugetlb: do not invoke the OOM killer when optimizing vmemmap
- Submission/report subject: [PATCH v4 09/13] mm: hugetlb_vmemmap: move alloc_vmemmap_page_list() next to its free helper
- Submission/report subject: [PATCH v4 05/13] mm: hugetlb_vmemmap: generalize vmemmap page allocation
- Submission/report subject: [PATCH v4 13/13] mm: hugetlb_vmemmap: make vmemmap PTE conversion folio-oriented
- Submission/report subject: [PATCH v4 08/13] mm: hugetlb_vmemmap: simplify shared tail page handling
- Submission/report subject: [PATCH v4 11/13] mm: hugetlb_vmemmap: make vmemmap restoration folio-oriented
- Submission/report subject: [PATCH v4 07/13] mm: hugetlb_vmemmap: rename vmemmap_remap_pte() to vmemmap_optimize_pte()
- Submission/report subject: [PATCH v4 03/13] mm: hugetlb_vmemmap: unify VMEMMAP_{SPLIT,REMAP}_NO_TLB_FLUSH
- Submission/report subject: [PATCH v4 04/13] mm: hugetlb_vmemmap: simplify vmemmap head page handling
- Submission/report subject: [PATCH v4 12/13] mm: hugetlb_vmemmap: unify vmemmap range restoration
- Submission/report subject: [PATCH v4 02/13] mm: hugetlb_vmemmap: remove HugeTLB-specific vmemmap optimization macros
- Submission/report subject: [PATCH v4 06/13] mm: hugetlb_vmemmap: unify writable vmemmap page preparation
- Submission/report subject: [PATCH v4 01/13] mm: hugetlb_vmemmap: fix OOM during head page allocation
- Submission/report subject: [PATCH v4 10/13] mm: hugetlb_vmemmap: make vmemmap optimization folio-oriented

### hwpoison-v3-review-evidence.zip

Evidence: [hwpoison-v3-review-evidence.zip](https://chatgpt.com/library?file_id=libfile_7b792cc7c4308191a7637b58874c8e37&account_id=personal)
Library ID: `libfile_7b792cc7c4308191a7637b58874c8e37`
- Review member: `hwpoison-v3-review/review.md`
- Submission/report subject: [PATCH v3] mm/memory-failure: set PG_hwpoison of a non-hugetlb page under hugetlb_lock

### pkeys-review-evidence.zip

Evidence: [pkeys-review-evidence.zip](https://chatgpt.com/library?file_id=libfile_5242fcec4df48191bf83502cef671f28&account_id=personal)
Library ID: `libfile_5242fcec4df48191bf83502cef671f28`
- Review member: `pkeys-review/review.md`
- Submission/report subject: [PATCH] selftests/mm: pkeys: wait for the child in become_child()

### pagecache-refcount-review-evidence.zip

Evidence: [pagecache-refcount-review-evidence.zip](https://chatgpt.com/library?file_id=libfile_c62635d232488191a9476cadfd9f79df&account_id=personal)
Library ID: `libfile_c62635d232488191a9476cadfd9f79df`
- Review member: `review.md`
- Submission/report subject: [PATCH] mm/readahead: Add large folio readahead
- Submission/report subject: [PATCH] shmem: add huge pages support
- Submission/report subject: [PATCH] mm/memory: optimize unmap/zap with PTE-mapped THP
- Submission/report subject: [PATCH] mm,thp: add read-only THP support for (non-shmem) FS
- Submission/report subject: [PATCH] iommufd: pfn_reader for file mappings

### pte-sync-review-20261105.zip

Evidence: [pte-sync-review-20261105.zip](https://chatgpt.com/library?file_id=libfile_e02777eeb82c8191ad0710addd4aa258&account_id=personal)
Library ID: `libfile_e02777eeb82c8191ad0710addd4aa258`
- Review member: `pte-review/closure.txt`
- Review member: `pte-review/review.txt`
- Submission/report subject: [PATCH] mm: synchronize with PTE table reclaim for all folio sizes
- Submission/report subject: [PATCH 15/46] mm/khugepaged: always recheck the pmd in

### copy-huge-pmd-v5-review.zip

Evidence: [copy-huge-pmd-v5-review.zip](https://chatgpt.com/library?file_id=libfile_676bcc4a940481919454ae61893f199d&account_id=personal)
Library ID: `libfile_676bcc4a940481919454ae61893f199d`
- Review member: `fork-v5/arch-review.txt`
- Review member: `fork-v5/kernel-review.txt`
- Review member: `fork-v5/review.txt`
- Review member: `fork-v5/test-review.txt`
- Submission/report subject: [PATCH v5 0/4] mm/huge_memory: copy PMDs at fork like the PTE path does
- Submission/report subject: [PATCH v5 4/4] selftests/mm: test fork of PMD-mapped shmem THPs
- Submission/report subject: [PATCH v5 1/4] mm/rmap: duplicate a PMD mapping as one in folio_dup_file_rmap_pmd()
- Submission/report subject: [PATCH v5 3/4] mm/huge_memory: read a special PMD under the lock in copy_huge_pmd()
- Submission/report subject: [PATCH v5 2/4] mm/huge_memory: copy file THPs at fork like copy_present_ptes() does

### watermark-nofragment-v2-evidence.zip

Evidence: [watermark-nofragment-v2-evidence.zip](https://chatgpt.com/library?file_id=libfile_84ea7a2d2600819181ab89a91d0dd06e&account_id=personal)
Library ID: `libfile_84ea7a2d2600819181ab89a91d0dd06e`
- Review member: `watermark-v2/allocator-review.txt`
- Review member: `watermark-v2/review.txt`
- Review member: `watermark-v2/reclaim-review.txt`
- Submission/report subject: [PATCH v2 0/3] mm: make watermark checks honour ALLOC_NOFRAGMENT Review began 2026-11-04 19:26:36 UTC. Source/preflight work ~first minute; parallel source analysis and test development overlapped through 19:30;
- Submission/report subject: [PATCH v2 0/3] mm: make watermark checks honour ALLOC_NOFRAGMENT
- Submission/report subject: [PATCH v2 1/3] mm: page_alloc: add a watermark check that knows the migratetype
- Submission/report subject: [PATCH v2 3/3] mm: vmscan: tell direct reclaim the allocation is ALLOC_NOFRAGMENT
- Submission/report subject: [PATCH v2 2/3] mm: page_alloc: make the high-order watermark check honour ALLOC_NOFRAGMENT

### uffd-copy-reregister-v3-evidence.zip

Evidence: [uffd-copy-reregister-v3-evidence.zip](https://chatgpt.com/library?file_id=libfile_6ea6cbbd29988191bc39b9b47c4f32e2&account_id=personal)
Library ID: `libfile_6ea6cbbd29988191bc39b9b47c4f32e2`
- Review member: `kernel-review.txt`
- Review member: `test-review.txt`
- Submission/report subject: [PATCH v3 1/2] mm/userfaultfd: recheck WP registration in the hugetlb UFFDIO_COPY retry
- Submission/report subject: [PATCH v3 0/2] mm/userfaultfd: recheck WP registration in the hugetlb UFFDIO_COPY retry
- Submission/report subject: [PATCH v3 2/2] selftests/mm: add a uffd test for re-registering during UFFDIO_COPY

### compaction-random-offset-evidence.zip

Evidence: [compaction-random-offset-evidence.zip](https://chatgpt.com/library?file_id=libfile_41897ad5b3f881919a2243ff439d7955&account_id=personal)
Library ID: `libfile_41897ad5b3f881919a2243ff439d7955`
- Submission/report subject: [PATCH] mm/compaction: sample empty pageblocks again from a random offset
Review scope must be established from the archive; no standalone verdict inferred.

### proc-maps-race-v3-review.zip

Evidence: [proc-maps-race-v3-review.zip](https://chatgpt.com/library?file_id=libfile_5ddc7aa68b908191b4fa6b791974dd81&account_id=personal)
Library ID: `libfile_5ddc7aa68b908191b4fa6b791974dd81`
- Review member: `review.md`
- Submission/report subject: [PATCH v3 1/1] selftests/proc: use RSS in /proc/pid/smaps_rollup tearing tests

### swap-hibernation-evidence.zip

Evidence: [swap-hibernation-evidence.zip](https://chatgpt.com/library?file_id=libfile_891da2239408819191f54bdbedb75488&account_id=personal)
Library ID: `libfile_891da2239408819191f54bdbedb75488`
- Review member: `swap-hibernation-review.md`
- Submission/report subject: [PATCH v4 0/3] mm, swap: keep hibernation swap slots out of the swap cache
- Submission/report subject: [PATCH v4 1/3] mm, swap: only allow swapped-out slots into the swap cache
- Submission/report subject: [PATCH v4 2/3] mm, swap: give hibernation swap slots their own swap table entry type
- Submission/report subject: [PATCH v4 3/3] mm, swap: drop the swap cache guard and reclaim in swap_free_hibernation_slot()

### iommufd-seals-fix-evidence.zip

Evidence: [iommufd-seals-fix-evidence.zip](https://chatgpt.com/library?file_id=libfile_b93eee3935f88191827a29fbec8a9067&account_id=personal)
Library ID: `libfile_b93eee3935f88191827a29fbec8a9067`
- Review member: `reviews/iommu-seals/root-review.md`
- Review member: `reviews/iommu-seals/closure.txt`
- Submission/report subject: [PATCH] iommufd: enforce memfd write seals for file mappings

### memfd-seals-review.zip

Evidence: [memfd-seals-review.zip](https://chatgpt.com/library?file_id=libfile_42eff827ce808191991bea0dff0f64a8&account_id=personal)
Library ID: `libfile_42eff827ce808191991bea0dff0f64a8`
- Submission/report subject: [PATCH 2/2] mm/memfd: handle GUP references reliably when write-sealing
- Submission/report subject: [PATCH 1/2] mm/memfd: handle GUP pins more reliably when write-sealing
Review scope must be established from the archive; no standalone verdict inferred.

### maple-v2-review.zip

Evidence: [maple-v2-review.zip](https://chatgpt.com/library?file_id=libfile_1bf76d8b02308191afc08b267df8ee4d&account_id=personal)
Library ID: `libfile_1bf76d8b02308191afc08b267df8ee4d`
- Review member: `review.md`
- Submission/report subject: [PATCH v2 0/3] maple_tree fixes for 7.3

### mremap-partial-move-review.zip

Evidence: [mremap-partial-move-review.zip](https://chatgpt.com/library?file_id=libfile_b484eaf462a0819193dcef7972bfa5b7&account_id=personal)
Library ID: `libfile_b484eaf462a0819193dcef7972bfa5b7`
- Review member: `review.md`
- Submission/report subject: [PATCH v2 0/5] mm/mremap: fix accounting on a partial move

### uffd-whole-range-review.zip

Evidence: [uffd-whole-range-review.zip](https://chatgpt.com/library?file_id=libfile_ccac1d4ab0848191ab98c46377dad4b8&account_id=personal)
Library ID: `libfile_ccac1d4ab0848191ab98c46377dad4b8`
- Review member: `uffd-whole-range-review.md`
- Submission/report subject: [PATCH 1/2] userfaultfd: validate the whole range before changing write protection
- Submission/report subject: [PATCH 2/2] selftests/mm: test a uffd write-protect range with an unregistered page
- Submission/report subject: [PATCH v3 24/47] mm/userfaultfd: wake all waiters on unregister

### taskstats-evidence.zip

Evidence: [taskstats-evidence.zip](https://chatgpt.com/library?file_id=libfile_3f9dd96db1f881918cde6e1b04b96950&account_id=personal)
Library ID: `libfile_3f9dd96db1f881918cde6e1b04b96950`
- Review member: `taskstats-review.md`
- Submission/report subject: [PATCH 0/4] taskstats: four more tidy-ups in the genl path

### runtime-evidence.zip

Evidence: [runtime-evidence.zip](https://chatgpt.com/library?file_id=libfile_c5f56e330e3081919bc6364e84c9ae1f&account_id=personal)
Library ID: `libfile_c5f56e330e3081919bc6364e84c9ae1f`
- Submission/report subject: [PATCH] selftests/proc: handle personality and memlock constraints
Review scope must be established from the archive; no standalone verdict inferred.

### R-068-evidence.zip

Evidence: [R-068-evidence.zip](https://chatgpt.com/library?file_id=libfile_7c4bd3d9088481918b913b94cfc73209&account_id=personal)
Library ID: `libfile_7c4bd3d9088481918b913b94cfc73209`
- Review member: `R-068/R-068-review.md`
- Submission/report subject: [PATCH v2 1/1] selftests/proc: use RSS in /proc/pid/smaps_rollup tearing tests

### R-067-evidence.zip

Evidence: [R-067-evidence.zip](https://chatgpt.com/library?file_id=libfile_393cfa475db08191b3cad8e751479a2d&account_id=personal)
Library ID: `libfile_393cfa475db08191b3cad8e751479a2d`
- Review member: `R-067/R-067-review.md`
- Submission/report subject: [PATCH 0/2] mm/ksm: keep smart scan from losing duplicate pages
- Submission/report subject: [PATCH 1/2] mm/ksm: align smart scan skips with the scan number
- Submission/report subject: [PATCH 2/2] selftests/mm: cover merging KSM pages aged by smart scan

### R-066-evidence.zip

Evidence: [R-066-evidence.zip](https://chatgpt.com/library?file_id=libfile_ad60d0890c3c81919ac8eabe6719a3da&account_id=personal)
Library ID: `libfile_ad60d0890c3c81919ac8eabe6719a3da`
- Review member: `R-066/R-066-review.md`
- Submission/report subject: [PATCH 33/44] ipc: use min() instead of min_t()

### R-065-evidence.zip

Evidence: [R-065-evidence.zip](https://chatgpt.com/library?file_id=libfile_4827bb8a247c8191801d8d27a243e1a4&account_id=personal)
Library ID: `libfile_4827bb8a247c8191801d8d27a243e1a4`
- Review member: `R-065/R-065-review.md`
- Submission/report subject: [PATCH 1/1] ipc: sem: fix used_sems overflow in newary()

### R-064-evidence.zip

Evidence: [R-064-evidence.zip](https://chatgpt.com/library?file_id=libfile_81ea7a7caf1c8191b2cca208d9b5edf5&account_id=personal)
Library ID: `libfile_81ea7a7caf1c8191b2cca208d9b5edf5`
- Review member: `R-064/R-064-review.md`
- Submission/report subject: [PATCH] lib/ts_fsm: preserve token types when exporting patterns
- Submission/report subject: [PATCH] lib/ts_bm: fix missed matches with TS_IGNORECASE
- Submission/report subject: [PATCH] [LIB]: Naive finite state machine based textsearch

### R-063-evidence.zip

Evidence: [R-063-evidence.zip](https://chatgpt.com/library?file_id=libfile_eed8dde8f3008191b6966b6f6e3c13a6&account_id=personal)
Library ID: `libfile_eed8dde8f3008191b6966b6f6e3c13a6`
- Review member: `R-063/R-063-review.md`
- Submission/report subject: [PATCH] ipc: fix hung task in copy_ipcs()

### R-062-evidence.zip

Evidence: [R-062-evidence.zip](https://chatgpt.com/library?file_id=libfile_8ae85fcf8f788191b2e08f670176c963&account_id=personal)
Library ID: `libfile_8ae85fcf8f788191b2e08f670176c963`
- Review member: `R-062/R-062-review.md`
- Submission/report subject: [PATCH] selftests/uevent: Gracefully handle receive buffer overrun

### R-061-evidence.zip

Evidence: [R-061-evidence.zip](https://chatgpt.com/library?file_id=libfile_ff3407872ffc8191a53e004db05e20b3&account_id=personal)
Library ID: `libfile_ff3407872ffc8191a53e004db05e20b3`
- Review member: `R-061/R-061-review.md`
- Submission/report subject: [PATCH v2] params: serialize lookup_or_create_module_kobject()

### R-060-evidence.zip

Evidence: [R-060-evidence.zip](https://chatgpt.com/library?file_id=libfile_7dfe15695b0c8191812b37abd2010535&account_id=personal)
Library ID: `libfile_7dfe15695b0c8191812b37abd2010535`
- Review member: `R-060/R-060-review.md`
- Submission/report subject: [PATCH] mm/huge_memory: prevent losing PG_waiters in __split_folio_to_order()

### R-059-evidence.zip

Evidence: [R-059-evidence.zip](https://chatgpt.com/library?file_id=libfile_1355757d70948191961a094c870b8cdd&account_id=personal)
Library ID: `libfile_1355757d70948191961a094c870b8cdd`
- Review member: `R-059/R-059-review.md`
- Submission/report subject: [PATCH 1/2] errseq: don't let errseq_check_and_advance() hide later errors
- Submission/report subject: [PATCH 2/2] lib/tests: errseq: add a concurrent check_and_advance test

### R-058-evidence.zip

Evidence: [R-058-evidence.zip](https://chatgpt.com/library?file_id=libfile_271dcb7ad0dc81918e1c92653e0e0f1c&account_id=personal)
Library ID: `libfile_271dcb7ad0dc81918e1c92653e0e0f1c`
- Review member: `R-058/R-058-review.md`
- Review member: `R-058/closure-log.txt`
- Submission/report subject: [PATCH v2] mm/memory-failure: fix folio refcount leak and min_order_for_split() locking

### R-057-evidence.zip

Evidence: [R-057-evidence.zip](https://chatgpt.com/library?file_id=libfile_9bc602aa57b881918fb423b898dfaa7b&account_id=personal)
Library ID: `libfile_9bc602aa57b881918fb423b898dfaa7b`
- Review member: `R-057/R-057-review.md`
- Submission/report subject: [PATCH] userfaultfd: docs: Fix an error code, two names and the POLLERR cause

### R-056-evidence.zip

Evidence: [R-056-evidence.zip](https://chatgpt.com/library?file_id=libfile_90b7ac3060a48191a32485b824a1ae54&account_id=personal)
Library ID: `libfile_90b7ac3060a48191a32485b824a1ae54`
- Review member: `R-056/R-056-review.md`
- Submission/report subject: [PATCH] mm/shmem: fix swapin livelock on a mismatched large swap cache folio

### tsacct-suspend-evidence.zip

Evidence: [tsacct-suspend-evidence.zip](https://chatgpt.com/library?file_id=libfile_34b83c13883c81918fe4849826d871a1&account_id=personal)
Library ID: `libfile_34b83c13883c81918fe4849826d871a1`
- Review member: `review-tsacct/closure.md`
- Review member: `review-tsacct/guided/report.md`
- Review member: `review-tsacct/history/report.md`
- Review member: `review-tsacct/tsacct-suspend-review.md`
- Submission/report subject: [PATCH] tsacct: keep task begin times stable across suspend
- Submission/report subject: tsacct: keep task begin times stable across suspend
- Submission/report subject: [PATCH] tsacct: keep task begin times stable across suspend Performed after source, guided/history tracks and behavioral results. This is same-model adversarial review, not an external endorsement.

### group-cpus-r036-v5-evidence.zip

Evidence: [group-cpus-r036-v5-evidence.zip](https://chatgpt.com/library?file_id=libfile_5506681a5e3881919e494bb7db9558a2&account_id=personal)
Library ID: `libfile_5506681a5e3881919e494bb7db9558a2`
- Review member: `group-cpus-snapshot-r036-review.md`
- Review member: `guided/report.md`
- Review member: `history/report.md`
- Review member: `prior-v4-review.md`
- Submission/report subject: [PATCH v5] lib/group_cpus: Snapshot cluster masks to keep grouping hotplug invariant

### R-055-evidence.zip

Evidence: [R-055-evidence.zip](https://chatgpt.com/library?file_id=libfile_deda46a22b5c819190c08adba4e43b7b&account_id=personal)
Library ID: `libfile_deda46a22b5c819190c08adba4e43b7b`
- Review member: `R-055/P01/bounded-review-evidence.md`
- Review member: `R-055/P02/bounded-review-evidence.md`
- Review member: `R-055/P03/bounded-review-evidence.md`
- Review member: `R-055/P04/bounded-review-evidence.md`
- Review member: `R-055/P05/bounded-review-evidence.md`
- Review member: `R-055/P06/bounded-review-evidence.md`
- Review member: `R-055/P07/bounded-review-evidence.md`
- Review member: `R-055/P08/bounded-review-evidence.md`
- Review member: `R-055/P19/guided-source-review-v2.txt`
- Review member: `R-055/P19/guided-source-review.txt`
- Submission/report subject: [PATCH v2 01/47] mm/mglru: don't use stack pointers when walking PUD and PMD tables
- Submission/report subject: [PATCH v2 02/47] fork: take mmap_lock before copying mm_struct
- Submission/report subject: [PATCH v2 03/47] mm/memfd: check for real shmem inodes before accessing shmem state
- Submission/report subject: [PATCH v2 04/47] mm/memfd: make f_pos accesses atomic
- Submission/report subject: [PATCH v2 05/47] mm/truncate: look again if a folio left the mapping
- Submission/report subject: [PATCH v2 06/47] mm/filemap: read mapping->a_ops->free_folio under i_lock
- Submission/report subject: [PATCH v2 07/47] mm/filemap: don't lose a folio lock wakeup to a signal
- Submission/report subject: [PATCH v2 08/47] mm/filemap: finish fault cleanup before dropping the fault lock
- Submission/report subject: [PATCH v2 19/47] mm/gup: recheck the PUD under PTL in follow_pud_mask()
- Submission/report subject: [PATCH v2 20/47] mm/gup: fix clearing folios in memfd_pin_folios()
- Submission/report subject: [PATCH v2 21/47] mm/gup: fix out-of-bounds write for nr_pages == 0 in
- Submission/report subject: [PATCH v2 22/47] mm/gup: check for overflow when converting nr_pages to
- Submission/report subject: [PATCH v2 23/47] mm/userfaultfd: write-lock the VMA before waking waiters
- Submission/report subject: [PATCH v2 24/47] mm/userfaultfd: wake all waiters on unregister
- Submission/report subject: [PATCH v2 25/47] mm/userfaultfd: wake waiters when registration modes are
- Submission/report subject: [PATCH v2 26/47] mm/userfaultfd: compare exact registration modes before
- Submission/report subject: [PATCH v2 27/47] mm/mmu_gather: fix flushing ranges with 4 GiB or larger
- Submission/report subject: [PATCH v2 28/47] mm/mmu_notifier: finish non-blocking interval invalidation
- Submission/report subject: [PATCH v2 29/47] mm/mmu_notifier: set ->mm only after mmgrab()
- Submission/report subject: [PATCH v2 30/47] mm/mremap: use pudp_huge_get_and_clear() when moving huge PUDs
- Submission/report subject: [PATCH v2 30/47] mm/mremap: use pudp_huge_get_and_clear() when
- Submission/report subject: [PATCH v2 31/47] mm/mremap: recheck PUDs under the page table lock
- Submission/report subject: [PATCH v2 32/47] mm/mremap: fix moving PUD leaves
- Submission/report subject: [PATCH v2 33/47] mm/memory_hotplug: avoid races in pfn_to_online_page() with dying pgmap
- Submission/report subject: [PATCH v2 33/47] mm/memory_hotplug: avoid races in
- Submission/report subject: [PATCH v2 34/47] mm/madvise: fix data loss from MADV_FREE on a KSM page
- Submission/report subject: [PATCH v2 34/47] mm/madvise: fix data loss from MADV_FREE on a KSM
- Submission/report subject: [PATCH v2 35/47] mm/memory: reject remote COW faults on PFN mappings
- Submission/report subject: [PATCH v2 35/47] mm/memory: reject remote COW faults on PFN
- Submission/report subject: [PATCH v2 36/47] mm: fix unmap_mapping_range() beyond 4 GiB on 32-bit
- Submission/report subject: [PATCH v2 36/47] mm: fix unmap_mapping_range() beyond 4 GiB on
- Submission/report subject: [PATCH v2 37/47] mm: fix unkillable fault loop on MAP_DROPPABLE memory
- Submission/report subject: [PATCH v2 37/47] mm: fix unkillable fault loop on MAP_DROPPABLE
- Submission/report subject: [PATCH v2 38/47] mm: fix deadlock of mremap() against UFFDIO_MOVE
- Submission/report subject: [PATCH v2 00/47] mm: various (urgent?) fixes
- Submission/report subject: [PATCH v2 01/47] mm/mglru: don't use stack pointers when walking PUD and
- Submission/report subject: [PATCH v2 03/47] mm/memfd: check for real shmem inodes before accessing
- Submission/report subject: [PATCH v2 08/47] mm/filemap: finish fault cleanup before dropping the fault
- Submission/report subject: [PATCH v2 09/47] mm/rmap: handle device-exclusive entries in
- Submission/report subject: [PATCH v2 10/47] mm/huge_memory: fix list corruption when
- Submission/report subject: [PATCH v2 11/47] mm/huge_memory: properly handle refcounted PUD mappings on
- Submission/report subject: [PATCH v2 12/47] mm/huge_memory: fix livelock on device private folio
- Submission/report subject: [PATCH v2 13/47] mm/huge_memory: fix truncate racing with PMD zapping
- Submission/report subject: [PATCH v2 14/47] mm/huge_memory: fix zapping migration entries for
- Submission/report subject: [PATCH v2 15/47] mm/khugepaged: always recheck the pmd in
- Submission/report subject: [PATCH v2 16/47] mm/khugepaged: fix PMD table lock leak in
- Submission/report subject: [PATCH v2 17/47] mm/khugepaged: preserve dirty bits when collapsing
- Submission/report subject: [PATCH v2 18/47] mm/khugepaged: check if PTE table is empty in
- Submission/report subject: [PATCH v2 30/47] mm/mremap: use pudp_huge_get_and_clear() when moving huge
- Submission/report subject: [PATCH v2 33/47] mm/memory_hotplug: avoid races in pfn_to_online_page()
- Submission/report subject: [PATCH v2 39/47] mm/ksm: reset the unstable trees of all nodes
- Submission/report subject: [PATCH v2 40/47] mm/ksm: fix use of a freed anon_vma at swap-in
- Submission/report subject: [PATCH v2 41/47] mm/ksm: check large swap-cache folios before mapping them
- Submission/report subject: [PATCH v2 42/47] mm/vma: call ->may_split() before a partial merge
- Submission/report subject: [PATCH v2 43/47] mm/huge_memory: split huge PUDs when adjusting VMA
- Submission/report subject: [PATCH v2 44/47] mm/vma: don't leak the charge for stack growth
- Submission/report subject: [PATCH v2 45/47] mm/cma: don't release CMA pages still in use
- Submission/report subject: [PATCH v2 46/47] mm/memory-tiers: unregister empty tiers outside
- Submission/report subject: [PATCH v2 47/47] fs/proc/task_mmu: refuse addresses beyond 32 bits on 32bit
- Submission/report subject: [PATCH v2 09/47] mm/rmap: handle device-exclusive entries in folio_referenced_one()

### R-054-evidence.zip

Evidence: [R-054-evidence.zip](https://chatgpt.com/library?file_id=libfile_eae12041075881918217f9675f504b5e&account_id=personal)
Library ID: `libfile_eae12041075881918217f9675f504b5e`
- Review member: `R-054/R-054-review.md`
- Submission/report subject: [PATCH v3] ipc/msg: fix msg_qbytes truncation in IPC_SET

### R-053-evidence.zip

Evidence: [R-053-evidence.zip](https://chatgpt.com/library?file_id=libfile_744989621ed08191b6ceb6bd4c3c85fa&account_id=personal)
Library ID: `libfile_744989621ed08191b6ceb6bd4c3c85fa`
- Review member: `R-053/R-053-review.md`
- Review member: `R-053/prior-R-052-review.md`
- Submission/report subject: [PATCH] ipc/msg: align compat version-0 msqid_ds with native IPC_OLD
- Submission/report subject: [PATCH v2] ipc/msg: prevent msg_qbytes limit bypass in IPC_SET

### R-052-evidence.zip

Evidence: [R-052-evidence.zip](https://chatgpt.com/library?file_id=libfile_dfa98012573c8191bc64e568c9253ec6&account_id=personal)
Library ID: `libfile_dfa98012573c8191bc64e568c9253ec6`
- Review member: `R-052/R-052-review.md`
- Review member: `R-052/closure-retries.txt`
- Submission/report subject: [PATCH v2] ipc/msg: prevent msg_qbytes limit bypass in IPC_SET
- Submission/report subject: [PATCH 30/43] ipc: add IPC_STAT_R and IPC_SET_R

### R-051-evidence.zip

Evidence: [R-051-evidence.zip](https://chatgpt.com/library?file_id=libfile_64cf113a1a5c819186b334f0d0828f77&account_id=personal)
Library ID: `libfile_64cf113a1a5c819186b334f0d0828f77`
- Review member: `R-051-review.md`
- Review member: `closure-note.md`
- Submission/report subject: [PATCH 1/3] mm: page_alloc: add a watermark check that knows the migratetype
- Submission/report subject: [PATCH 2/3] mm: page_alloc: make the high-order watermark check honour ALLOC_NOFRAGMENT
- Submission/report subject: [PATCH 3/3] mm: vmscan: tell direct reclaim the allocation is ALLOC_NOFRAGMENT

### R-050-evidence.zip

Evidence: [R-050-evidence.zip](https://chatgpt.com/library?file_id=libfile_9d0a329ccf8c8191801ed003b4466749&account_id=personal)
Library ID: `libfile_9d0a329ccf8c8191801ed003b4466749`
- Review member: `R-050/R-050-review.md`
- Submission/report subject: ipc/msg: clamp negative MSG_INFO usage counts

### R-049-negative-statistics-evidence.zip

Evidence: [R-049-negative-statistics-evidence.zip](https://chatgpt.com/library?file_id=libfile_1177dd307cb48191a9e75499473c1753&account_id=personal)
Library ID: `libfile_1177dd307cb48191a9e75499473c1753`
- Review member: `ipc-negative/inputs/R-049-review.md`
- Submission/report subject: [PATCH] ipc/msg: clamp negative MSG_INFO usage counts
- Submission/report subject: [PATCH 05/44] ipc/msg: Fix saturation of percpu counts in msgctl_info()

### R-049-evidence.zip

Evidence: [R-049-evidence.zip](https://chatgpt.com/library?file_id=libfile_294326a56bc08191b8bcdb565e16650f&account_id=personal)
Library ID: `libfile_294326a56bc08191b8bcdb565e16650f`
- Review member: `R-049/R-049-review.md`
- Review member: `R-049/gate-closure.md`
- Submission/report subject: [PATCH 05/44] ipc/msg: Fix saturation of percpu counts in msgctl_info()

### R-048-evidence.zip

Evidence: [R-048-evidence.zip](https://chatgpt.com/library?file_id=libfile_6bc68e9009d481919709ab55d19d5e45&account_id=personal)
Library ID: `libfile_6bc68e9009d481919709ab55d19d5e45`
- Review member: `R-048/R-048-review.md`
- Review member: `R-048/gate-closure.md`
- Submission/report subject: [PATCH 0/4] Lib fixes for 7.3
- Submission/report subject: [PATCH 1/4] maple_tree: Fix rcu reader NULL dereference after the tree is emptied
- Submission/report subject: [PATCH 2/4] maple_tree: Test emptying tree while RCU reading
- Submission/report subject: [PATCH 3/4] maple_tree: Update internal warning and bug_on code
- Submission/report subject: [PATCH 4/4] rhashtable: fix vmalloc() deadlock in atomic rehash

### R-047-evidence.zip

Evidence: [R-047-evidence.zip](https://chatgpt.com/library?file_id=libfile_b79592aeb6a48191975c362d818e5ba5&account_id=personal)
Library ID: `libfile_b79592aeb6a48191975c362d818e5ba5`
- Review member: `R-047/R-047-review.md`
- Submission/report subject: [PATCH 1/1] selftests/proc: use RSS in /proc/pid/smaps_rollup tearing tests

### R-046-evidence.zip

Evidence: [R-046-evidence.zip](https://chatgpt.com/library?file_id=libfile_21600e9b5370819195ed4c00df4d2a73&account_id=personal)
Library ID: `libfile_21600e9b5370819195ed4c00df4d2a73`
- Review member: `R-046/R-046-review.md`
- Submission/report subject: [PATCH] ipc/msg: prevent msg_qbytes limit bypass in IPC_SET

### R-045-evidence.zip

Evidence: [R-045-evidence.zip](https://chatgpt.com/library?file_id=libfile_63b38ae7665c8191b9e893ec7049a0db&account_id=personal)
Library ID: `libfile_63b38ae7665c8191b9e893ec7049a0db`
- Review member: `R-045/R-045-review.md`
- Submission/report subject: [PATCH 7/9] mm: page_isolation: do not take slab pages for free

### R-044-ts-bm-ignorecase-evidence.zip

Evidence: [R-044-ts-bm-ignorecase-evidence.zip](https://chatgpt.com/library?file_id=libfile_ba9e6685d5088191bb503e737046356e&account_id=personal)
Library ID: `libfile_ba9e6685d5088191bb503e737046356e`
- Submission/report subject: [PATCH] lib/ts_bm: fix missed matches with TS_IGNORECASE
Review scope must be established from the archive; no standalone verdict inferred.

### R-043-evidence.zip

Evidence: [R-043-evidence.zip](https://chatgpt.com/library?file_id=libfile_fbe25e1d75308191b17e6c3305e3c369&account_id=personal)
Library ID: `libfile_fbe25e1d75308191b17e6c3305e3c369`
- Review member: `swapoff-writeok-review.md`
- Submission/report subject: [PATCH] mm, swap: stop cluster list scans once swapoff clears SWP_WRITEOK

### R-042-evidence.tar.gz

Evidence: [R-042-evidence.tar.gz](https://chatgpt.com/library?file_id=libfile_5e8db9afee108191891b45d4678ae975&account_id=personal)
Library ID: `libfile_5e8db9afee108191891b45d4678ae975`
- Review member: `R-042/review-reply.txt`
- Review member: `R-042/review-report.md`
- Review member: `R-042/R-042-review.md`
- Submission/report subject: [PATCH 1/2] mm/memfd: add F_SEAL_PUNCH_HOLE
- Submission/report subject: [PATCH 2/2] selftests/memfd: add F_SEAL_PUNCH_HOLE tests

### ts-bm-ignorecase-evidence.tar.gz

Evidence: [ts-bm-ignorecase-evidence.tar.gz](https://chatgpt.com/library?file_id=libfile_8b267cf0ed88819197bb17d0b9e5cf39&account_id=personal)
Library ID: `libfile_8b267cf0ed88819197bb17d0b9e5cf39`
- Review member: `ts-bm-ignorecase/ts-bm-ignorecase-review.md`
- Submission/report subject: Bug in the Boyer-Moore search in lib/ts_bm.c

### hugetlbfs-seal-r041-evidence.tar.gz

Evidence: [hugetlbfs-seal-r041-evidence.tar.gz](https://chatgpt.com/library?file_id=libfile_958ce52c115081919b57ef5a298d5f27&account_id=personal)
Library ID: `libfile_958ce52c115081919b57ef5a298d5f27`
- Review member: `R-041/review.md`
- Review member: `R-041/inputs/akpm-review-gate-README.txt`
- Submission/report subject: [PATCH 05/16] hugetlbfs: enforce F_SEAL_EXEC in setattr

### move-pages-untag-r040-evidence.tar.gz

Evidence: [move-pages-untag-r040-evidence.tar.gz](https://chatgpt.com/library?file_id=libfile_547e1716faf8819193dae7f43148b2e7&account_id=personal)
Library ID: `libfile_547e1716faf8819193dae7f43148b2e7`
- Review member: `report/move-pages-untag-review.md`
- Submission/report subject: [PATCH] mm/migrate: untag addresses when querying page nodes

### mempolicy-interleave-node-set-fix-evidence.tar.gz

Evidence: [mempolicy-interleave-node-set-fix-evidence.tar.gz](https://chatgpt.com/library?file_id=libfile_d1676b0b9ef88191a1b456ac77bde23f&account_id=personal)
Library ID: `libfile_d1676b0b9ef88191a1b456ac77bde23f`
- Review member: `R-039-C3-fix/current-records/mempolicy-auto-hotplug-review.md`
- Review member: `R-039-C3-fix/deliverables/mempolicy-auto-hotplug-review.md`
- Submission/report subject: [PATCH] mm/mempolicy: recompute automatic interleave weights on memory hotplug
- Submission/report subject: [PATCH] mm/mempolicy: use one node set for interleave weights

### mempolicy-auto-hotplug-r039-evidence.tar.gz

Evidence: [mempolicy-auto-hotplug-r039-evidence.tar.gz](https://chatgpt.com/library?file_id=libfile_1dc741b0f978819193f73a7de5ad07f1&account_id=personal)
Library ID: `libfile_1dc741b0f978819193f73a7de5ad07f1`
- Review member: `R-039/reports/mempolicy-auto-hotplug-review.md`
- Submission/report subject: [PATCH] mm/mempolicy: recompute automatic interleave weights on memory hotplug

### page-alloc-tag-v2-r038-evidence.tar.gz

Evidence: [page-alloc-tag-v2-r038-evidence.tar.gz](https://chatgpt.com/library?file_id=libfile_86d469bf7af881919353927c2120b427&account_id=personal)
Library ID: `libfile_86d469bf7af881919353927c2120b427`
- Review member: `R-038/prior-report/Kernel Patch Reviews/reports/page-alloc-hotplug-tag-review.md`
- Review member: `R-038/review-inline.txt`
- Submission/report subject: [PATCH v2] mm/page_alloc: mark pages freed by __free_pages_core() as not tagged

### fat-write-failed-evidence.tar.gz

Evidence: [fat-write-failed-evidence.tar.gz](https://chatgpt.com/library?file_id=libfile_2ff53120c96c8191a6793e7d187b3792&account_id=personal)
Library ID: `libfile_2ff53120c96c8191a6793e7d187b3792`
- Review member: `R-037/fat-write-failed-review.md`
- Review member: `R-037/reporting-evidence.md`
- Submission/report subject: [PATCH] fat: hold truncate_lock in fat_write_failed()

### kernel-review-files-2026-10-24-r036.zip

Evidence: [kernel-review-files-2026-10-24-r036.zip](https://chatgpt.com/library?file_id=libfile_fd5ec41bbff481918984ceac3a721393&account_id=personal)
Library ID: `libfile_fd5ec41bbff481918984ceac3a721393`
- Review member: `r036-review/group-cpus-snapshot-review.md`

### kernel-review-files-2026-10-23-r035.zip

Evidence: [kernel-review-files-2026-10-23-r035.zip](https://chatgpt.com/library?file_id=libfile_3871acee0e948191bc28464280d9460d&account_id=personal)
Library ID: `libfile_3871acee0e948191bc28464280d9460d`
- Review member: `r035-review/ksm-softdirty-v3-review.md`

### kernel-review-master-files-2026-10-23-r034-tejun-corrected.zip

Evidence: [kernel-review-master-files-2026-10-23-r034-tejun-corrected.zip](https://chatgpt.com/library?file_id=libfile_7d5b193dbf5881919ee0b90efedb25db&account_id=personal)
Library ID: `libfile_7d5b193dbf5881919ee0b90efedb25db`
- Review member: `cgroup-s64-review.md`
- Review member: `r034-tejun-feedback-review.md`
- Submission/report subject: Re: [PATCH] selftests/cgroup: convert cg_read_key_*() helpers to s64

### kernel-review-master-files-2026-10-23-r034.zip

Evidence: [kernel-review-master-files-2026-10-23-r034.zip](https://chatgpt.com/library?file_id=libfile_9b8be93d88608191b05b304e798b8b76&account_id=personal)
Library ID: `libfile_9b8be93d88608191b05b304e798b8b76`
- Review member: `cgroup-s64-review.md`

### kernel-review-master-files-2026-10-23-r033.zip

Evidence: [kernel-review-master-files-2026-10-23-r033.zip](https://chatgpt.com/library?file_id=libfile_5831e694a31081919982fb5a34430ba7&account_id=personal)
Library ID: `libfile_5831e694a31081919982fb5a34430ba7`
Review scope must be established from the archive; no standalone verdict inferred.

### kernel-review-master-files-2026-10-23-r032.zip

Evidence: [kernel-review-master-files-2026-10-23-r032.zip](https://chatgpt.com/library?file_id=libfile_f819eb88505c8191954a4eb7eda4effd&account_id=personal)
Library ID: `libfile_f819eb88505c8191954a4eb7eda4effd`
Review scope must be established from the archive; no standalone verdict inferred.

### kernel-review-master-files-2026-10-23.zip

Evidence: [kernel-review-master-files-2026-10-23.zip](https://chatgpt.com/library?file_id=libfile_a554bb04fbac8191942ecc1ef7e67cff&account_id=personal)
Library ID: `libfile_a554bb04fbac8191942ecc1ef7e67cff`
Review scope must be established from the archive; no standalone verdict inferred.

### patch-review-state-2026-10-16-v3.tar.gz

Evidence: [patch-review-state-2026-10-16-v3.tar.gz](https://chatgpt.com/library?file_id=libfile_7f74467fa5288191b6e34991cc443b5f&account_id=personal)
Library ID: `libfile_7f74467fa5288191b6e34991cc443b5f`
Review scope must be established from the archive; no standalone verdict inferred.

### patch-review-state-2026-10-16-v2.tar.gz

Evidence: [patch-review-state-2026-10-16-v2.tar.gz](https://chatgpt.com/library?file_id=libfile_ad56069ae3e881918aa4c4d4d9929cf4&account_id=personal)
Library ID: `libfile_ad56069ae3e881918aa4c4d4d9929cf4`
Review scope must be established from the archive; no standalone verdict inferred.

### patch-review-state-2026-10-16.tar.gz

Evidence: [patch-review-state-2026-10-16.tar.gz](https://chatgpt.com/library?file_id=libfile_abab0d85cfe08191afb97d5d55eb88e8&account_id=personal)
Library ID: `libfile_abab0d85cfe08191afb97d5d55eb88e8`
Review scope must be established from the archive; no standalone verdict inferred.

### kernel-review-20261016.tar.gz

Evidence: [kernel-review-20261016.tar.gz](https://chatgpt.com/library?file_id=libfile_981f2dc805f08191bdb62c47e1778ded&account_id=personal)
Library ID: `libfile_981f2dc805f08191bdb62c47e1778ded`
Review scope must be established from the archive; no standalone verdict inferred.

## Historical ledger snapshots

These preserve older dispositions and may be superseded. Latest cumulative
snapshot recovered: review-activity(20261101-182158).md.

- [review-activity(20261101-182158).md](https://chatgpt.com/library?file_id=libfile_e6703f9d43f88191a9930aec87f49a5f&account_id=personal) (2026-11-01T18:21:58.135383+00:00)
- [review-activity(20261031-005911).md](https://chatgpt.com/library?file_id=libfile_0b5cc36b631c8191894953e9bb650c14&account_id=personal) (2026-10-31T00:59:10.521481+00:00)
- [review-activity(20261030-215843).md](https://chatgpt.com/library?file_id=libfile_bd801cb5e4908191bd748261a277c48d&account_id=personal) (2026-10-30T21:58:43.295611+00:00)
- [review-activity(20261030-050424).md](https://chatgpt.com/library?file_id=libfile_c985c34955d08191825c9f3971b76853&account_id=personal) (2026-10-30T05:04:24.400030+00:00)
- [review-activity(20261026-224143).md](https://chatgpt.com/library?file_id=libfile_05dfe2c8116881918e088d0d15ada7c2&account_id=personal) (2026-10-26T22:41:43.412146+00:00)
- [review-activity(20261024-201901).md](https://chatgpt.com/library?file_id=libfile_04afd8493a2c819198b456d2ab834d91&account_id=personal) (2026-10-24T20:19:01.589731+00:00)
- [review-activity(20261024-201344).md](https://chatgpt.com/library?file_id=libfile_f0adf7f3272481919546e89b5958476a&account_id=personal) (2026-10-24T20:13:43.974728+00:00)
- [review-activity(20261024-081533).md](https://chatgpt.com/library?file_id=libfile_f1760ca51aa48191ae64006367bebd40&account_id=personal) (2026-10-24T08:15:33.466849+00:00)
- [review-activity(20261024-051249).md](https://chatgpt.com/library?file_id=libfile_8b32825540708191a48fe0a8909316f8&account_id=personal) (2026-10-24T05:12:49.331187+00:00)
- [review-activity(20261024-003417).md](https://chatgpt.com/library?file_id=libfile_2d57386a98c081919b8380bf1d6084fd&account_id=personal) (2026-10-24T00:34:17.468727+00:00)
- [review-activity(20261023-233651).md](https://chatgpt.com/library?file_id=libfile_e175827c7eb081918e9caa1f4661f8a7&account_id=personal) (2026-10-23T23:36:51.114145+00:00)
- [review-activity(20261023-232128).md](https://chatgpt.com/library?file_id=libfile_b9e16e4e44208191a0e5e92b315ec3cd&account_id=personal) (2026-10-23T23:21:28.734939+00:00)
- [review-activity(20261023-230729).md](https://chatgpt.com/library?file_id=libfile_e8e901211b848191bf6ed3d3a7a67047&account_id=personal) (2026-10-23T23:07:29.133258+00:00)
- [review-activity(20261023-221101).md](https://chatgpt.com/library?file_id=libfile_a120dc6630c081918682bec8dfdbfe1f&account_id=personal) (2026-10-23T22:11:00.914402+00:00)
- [review-activity(20261023-184030).md](https://chatgpt.com/library?file_id=libfile_bf79287c3e688191b2dc9e8856e53be3&account_id=personal) (2026-10-23T18:40:30.651034+00:00)
- [review-activity(20261023-183621).md](https://chatgpt.com/library?file_id=libfile_9aa1008e5e0c8191af66578a31393849&account_id=personal) (2026-10-23T18:36:21.058749+00:00)
- [review-activity(20261023-175505).md](https://chatgpt.com/library?file_id=libfile_97bb51d3da44819183bab2d335a6089c&account_id=personal) (2026-10-23T17:55:05.046752+00:00)
- [review-activity(20261023-174633).md](https://chatgpt.com/library?file_id=libfile_670b7c30a404819191a20fc2928461f1&account_id=personal) (2026-10-23T17:46:33.177646+00:00)
- [review-activity(20261023-054121).md](https://chatgpt.com/library?file_id=libfile_0cde2b5399d481919090d93e48b0f922&account_id=personal) (2026-10-23T05:41:21.406871+00:00)
- [review-activity(20261023-051640).md](https://chatgpt.com/library?file_id=libfile_6a66fe81506c819185be03dfb9856641&account_id=personal) (2026-10-23T05:16:40.852765+00:00)
- [review-activity(20261023-051029).md](https://chatgpt.com/library?file_id=libfile_7d1b860eb1f081918963d71b3b915fa3&account_id=personal) (2026-10-23T05:10:29.491418+00:00)
- [review-activity(20261023-050851).md](https://chatgpt.com/library?file_id=libfile_959fe34bd4888191a4aa627aa5f4a483&account_id=personal) (2026-10-23T05:08:51.067317+00:00)
- [review-activity(20261023-050657).md](https://chatgpt.com/library?file_id=libfile_476d4f91391081919fc2938ce025f9cc&account_id=personal) (2026-10-23T05:06:57.752418+00:00)
- [review-activity(20261023-050121).md](https://chatgpt.com/library?file_id=libfile_104e646f1aac8191a4450c87452cbc4a&account_id=personal) (2026-10-23T05:01:21.108976+00:00)
- [review-activity(20261023-043459).md](https://chatgpt.com/library?file_id=libfile_cad5351006b48191a4cdb3fcf632c95c&account_id=personal) (2026-10-23T04:34:59.126030+00:00)
- [review-activity(20261023-011530).md](https://chatgpt.com/library?file_id=libfile_68f1dc755bb081918ff7eec8e942b140&account_id=personal) (2026-10-23T01:15:30.520226+00:00)
- [review-activity(20261023-011529).md](https://chatgpt.com/library?file_id=libfile_b3d75cc32c988191bcab257c63ecf9cf&account_id=personal) (2026-10-23T01:15:29.552513+00:00)
- [review-activity(20261022-000329).md](https://chatgpt.com/library?file_id=libfile_2b6aafbdf90c819194bd5ff28e6cc8db&account_id=personal) (2026-10-22T00:03:29.780352+00:00)
- [review-activity(20261021-233632).md](https://chatgpt.com/library?file_id=libfile_0f2a122dbf6481919620aee426b239d4&account_id=personal) (2026-10-21T23:36:32.654939+00:00)
- [review-activity(20261021-233630).md](https://chatgpt.com/library?file_id=libfile_bfdb4992296c8191a675a4c32cdd91c5&account_id=personal) (2026-10-21T23:36:29.994896+00:00)
- [review-activity(20261021-225340).md](https://chatgpt.com/library?file_id=libfile_25b4479cf8ac8191abdf9fc8770c0dee&account_id=personal) (2026-10-21T22:53:39.927236+00:00)
- [review-activity(20261021-225339).md](https://chatgpt.com/library?file_id=libfile_fa472d4156288191af53b52a54c8b0bb&account_id=personal) (2026-10-21T22:53:38.638572+00:00)
- [review-activity(20261021-222951).md](https://chatgpt.com/library?file_id=libfile_4ac6b2b7c7c48191ac9ec602b6ebbac2&account_id=personal) (2026-10-21T22:29:51.107788+00:00)
- [review-activity(20261021-222940).md](https://chatgpt.com/library?file_id=libfile_84fde22a4f008191ae3edc47169fcf1c&account_id=personal) (2026-10-21T22:29:39.282138+00:00)
- [review-activity(20261021-215752).md](https://chatgpt.com/library?file_id=libfile_2272ed4a5f608191a740118dad0076dc&account_id=personal) (2026-10-21T21:57:52.276919+00:00)
- [review-activity(20261021-200907).md](https://chatgpt.com/library?file_id=libfile_2cab593767b881918b84aac5db1b8bcb&account_id=personal) (2026-10-21T20:09:06.960526+00:00)
- [review-activity(20261021-194517).md](https://chatgpt.com/library?file_id=libfile_186f528e9b588191bbf189dd971732d2&account_id=personal) (2026-10-21T19:45:17.266286+00:00)
- [review-activity(20261021-191804).md](https://chatgpt.com/library?file_id=libfile_8f1397073dc881919c574d422878f355&account_id=personal) (2026-10-21T19:18:03.866340+00:00)
- [review-activity(20261021-024029).md](https://chatgpt.com/library?file_id=libfile_7bc01c352f488191a229685f21b141eb&account_id=personal) (2026-10-21T02:40:29.277505+00:00)
- [review-activity(20261021-023117).md](https://chatgpt.com/library?file_id=libfile_60f56c03ed2881919c162150be504c12&account_id=personal) (2026-10-21T02:31:17.586487+00:00)
- [review-activity(20261021-013144).md](https://chatgpt.com/library?file_id=libfile_2d4832b5f3948191b2ce40e51831103c&account_id=personal) (2026-10-21T01:31:44.268720+00:00)
- [review-activity.md](https://chatgpt.com/library?file_id=libfile_9f7a94c51b908191b4bc1670e2d61870&account_id=personal) (2026-10-25T00:53:29.241589+00:00)
- [review-activity(20261021-012251).md](https://chatgpt.com/library?file_id=libfile_c5c886fbf698819192ba1408d887942c&account_id=personal) (2026-10-21T01:22:51.163812+00:00)
- [review-activity(20261021-010450).md](https://chatgpt.com/library?file_id=libfile_c4bd63d466c08191ba886fe58f0d6b05&account_id=personal) (2026-10-21T01:04:50.808177+00:00)
- [review-activity(20261020-220057).md](https://chatgpt.com/library?file_id=libfile_27968daab8d48191be518aa2abca6d13&account_id=personal) (2026-10-20T22:00:57.492442+00:00)
- [review-activity(20261020-200011).md](https://chatgpt.com/library?file_id=libfile_99f860e5dbc08191a3bec745056716ab&account_id=personal) (2026-10-20T20:00:11.304751+00:00)
- [review-activity(20261020-195518).md](https://chatgpt.com/library?file_id=libfile_61e7ee76049881918bbe630bf8e43be1&account_id=personal) (2026-10-20T19:55:18.031995+00:00)
- [review-activity(20261020-190938).md](https://chatgpt.com/library?file_id=libfile_52c04e7652588191bf66b1b76760f4ad&account_id=personal) (2026-10-20T19:09:38.071423+00:00)
- [review-activity(20261020-190935).md](https://chatgpt.com/library?file_id=libfile_6ea88e934720819186a740a03701e33d&account_id=personal) (2026-10-20T19:09:35.191867+00:00)
- [review-activity(20261020-190932).md](https://chatgpt.com/library?file_id=libfile_00568191ce308191a891caa4ac50ee6e&account_id=personal) (2026-10-20T19:09:31.967598+00:00)
- [review-activity(20261020-190923).md](https://chatgpt.com/library?file_id=libfile_264e2e79d74881919012cde83d6eeaa9&account_id=personal) (2026-10-20T19:09:23.617666+00:00)
- [review-activity(20261020-190917).md](https://chatgpt.com/library?file_id=libfile_0aa77bdda5f88191bd56fca88048a1ec&account_id=personal) (2026-10-20T19:09:17.496210+00:00)
- [review-activity(20261020-185324).md](https://chatgpt.com/library?file_id=libfile_b7ad33ca169c8191bdc19ac729005a63&account_id=personal) (2026-10-20T18:53:24.280903+00:00)
- [review-activity(20261020-185141).md](https://chatgpt.com/library?file_id=libfile_9c805e32978081918327af0f1f3177a2&account_id=personal) (2026-10-20T18:51:41.152352+00:00)
- [review-activity(20261020-170931).md](https://chatgpt.com/library?file_id=libfile_1b8ded001cc08191b744700dadceedfe&account_id=personal) (2026-10-20T17:09:31.137012+00:00)
- [review-activity(20261020-010205).md](https://chatgpt.com/library?file_id=libfile_3f5bad1fdc0c81919e38515deaf5160e&account_id=personal) (2026-10-20T01:02:05.658517+00:00)
- [review-activity(20261020-005357).md](https://chatgpt.com/library?file_id=libfile_b8a0693288cc819195d64bd79870e691&account_id=personal) (2026-10-20T00:53:57.398321+00:00)
- [review-activity(20261020-003553).md](https://chatgpt.com/library?file_id=libfile_e0ec3411ecf08191a0128bc00176e502&account_id=personal) (2026-10-20T00:35:53.829187+00:00)
- [review-activity(20261019-225808).md](https://chatgpt.com/library?file_id=libfile_1c5a29ca9b9881918ce08fcc3167bbc1&account_id=personal) (2026-10-19T22:58:08.104636+00:00)
- [review-activity(20261019-213953).md](https://chatgpt.com/library?file_id=libfile_0ef527a7196481918ea432e6ec1c2031&account_id=personal) (2026-10-19T21:39:53.545401+00:00)
- [review-activity(20261019-211331).md](https://chatgpt.com/library?file_id=libfile_fa307e929ed481918969b901bb61637a&account_id=personal) (2026-10-19T21:13:31.197901+00:00)
- [review-activity(20261019-211155).md](https://chatgpt.com/library?file_id=libfile_4d599373b7f0819188984a34e63923cc&account_id=personal) (2026-10-19T21:11:55.498219+00:00)
- [review-activity(20261019-145149).md](https://chatgpt.com/library?file_id=libfile_2bdfc49270f88191b64e3d1772d1ffb9&account_id=personal) (2026-10-19T14:51:48.944657+00:00)
- [review-activity(20261019-144532).md](https://chatgpt.com/library?file_id=libfile_f61887b1e9888191bfecc2cb27c07b3b&account_id=personal) (2026-10-19T14:45:31.904405+00:00)
- [review-activity(20261019-143257).md](https://chatgpt.com/library?file_id=libfile_c01ad42a57e88191b72a9611368ab0c1&account_id=personal) (2026-10-19T14:32:57.390967+00:00)
- [review-activity(20261018-185612).md](https://chatgpt.com/library?file_id=libfile_bd25b4b062d48191af1b499a91bcf32a&account_id=personal) (2026-10-18T18:56:12.335685+00:00)
- [review-activity .md](https://chatgpt.com/library?file_id=libfile_8bc15eac2b6481918a342889cb4d85a1&account_id=personal) (2026-10-18T18:50:13.125169+00:00)
- [review-activity(20261018-184843).md](https://chatgpt.com/library?file_id=libfile_5634ae19e5448191af429bb8348fc045&account_id=personal) (2026-10-18T18:48:43.671575+00:00)
- [review-activity(20261018-184503).md](https://chatgpt.com/library?file_id=libfile_965c4ecef5708191b950b06cb4d08cfd&account_id=personal) (2026-10-18T18:45:03.487128+00:00)
- [review-activity(20261018-183606).md](https://chatgpt.com/library?file_id=libfile_0760361cf23c8191a1c6cfef902ea006&account_id=personal) (2026-10-18T18:36:06.637036+00:00)
- [review-activity(20261018-182512).md](https://chatgpt.com/library?file_id=libfile_375f9ba792908191b346a9967eb3b1f1&account_id=personal) (2026-10-18T18:25:11.726520+00:00)
- [review-activity(20261018-181243).md](https://chatgpt.com/library?file_id=libfile_ccfbedba0c4c8191b1793a111289a7fa&account_id=personal) (2026-10-18T18:12:43.735898+00:00)
- [review-activity(20261018-064010).md](https://chatgpt.com/library?file_id=libfile_1b1b2ca40a188191b0b92eaf7dc8f1ea&account_id=personal) (2026-10-18T06:40:10.022506+00:00)
- [review-activity(20261018-062353).md](https://chatgpt.com/library?file_id=libfile_744dcd09ae288191acd6eb96bc41d719&account_id=personal) (2026-10-18T06:23:53.552194+00:00)
- [review-activity(20261018-061146).md](https://chatgpt.com/library?file_id=libfile_5e2c2127942081919b71c45f5bc7fb4a&account_id=personal) (2026-10-18T06:11:45.886885+00:00)
- [review-activity(20261018-040915).md](https://chatgpt.com/library?file_id=libfile_45a288ed98b08191ac406373ab074882&account_id=personal) (2026-10-18T04:09:15.471859+00:00)
- [review-activity(20261018-035434).md](https://chatgpt.com/library?file_id=libfile_0fbe9a4f28a48191950ae2fe277a7e7a&account_id=personal) (2026-10-18T03:54:34.534520+00:00)
- [review-activity(20261018-033606).md](https://chatgpt.com/library?file_id=libfile_b5c69eea50ec819185f1a452cd5fa623&account_id=personal) (2026-10-18T03:36:06.870734+00:00)
- [review-activity(20261018-032008).md](https://chatgpt.com/library?file_id=libfile_9c60320ab65481918aca75cf2cd15517&account_id=personal) (2026-10-18T03:20:07.955151+00:00)
- [review-activity(20261018-024322).md](https://chatgpt.com/library?file_id=libfile_89dc8202a24c81918b5e1432b3b79bd0&account_id=personal) (2026-10-18T02:43:21.968083+00:00)
- [review-activity(20261018-015504).md](https://chatgpt.com/library?file_id=libfile_c3b77e43291c8191a34446df89ad50dd&account_id=personal) (2026-10-18T01:55:04.224415+00:00)
- [review-activity(20261018-013908).md](https://chatgpt.com/library?file_id=libfile_5952ff5b71608191bbfb61c1898b650a&account_id=personal) (2026-10-18T01:39:08.320581+00:00)
- [review-activity(10).md](https://chatgpt.com/library?file_id=libfile_298082b5b0d881918d4c46a467e8b69f&account_id=personal) (2026-10-18T01:13:37.524136+00:00)
- [review-activity(9).md](https://chatgpt.com/library?file_id=libfile_5fab0b3d4fb481918865a7358295b0cf&account_id=personal) (2026-10-18T00:49:26.038516+00:00)
- [review-activity(8).md](https://chatgpt.com/library?file_id=libfile_a4226082a85c8191b7d97c088a18d103&account_id=personal) (2026-10-18T00:18:30.210149+00:00)
- [review-activity(7).md](https://chatgpt.com/library?file_id=libfile_aa372d02ae1c81919cc2cf6261b5330e&account_id=personal) (2026-10-17T21:33:28.039849+00:00)
- [review-activity(6).md](https://chatgpt.com/library?file_id=libfile_02140ef5889881919acb2add953e8052&account_id=personal) (2026-10-17T20:23:16.396141+00:00)
- [review-activity(5).md](https://chatgpt.com/library?file_id=libfile_34b2b8304ab08191979e9ceccdabe81a&account_id=personal) (2026-10-17T20:03:01.041831+00:00)
- [review-activity(4).md](https://chatgpt.com/library?file_id=libfile_0231e611efa08191b274e4e82e7ebe81&account_id=personal) (2026-10-17T19:47:31.082231+00:00)
- [review-activity(3).md](https://chatgpt.com/library?file_id=libfile_b8c2547dcd2881919123038567acac33&account_id=personal) (2026-10-17T18:07:53.760154+00:00)
- [review-activity(2).md](https://chatgpt.com/library?file_id=libfile_50396815f86081919256b59b23938e16&account_id=personal) (2026-10-17T05:56:36.252068+00:00)
- [review-activity(1).md](https://chatgpt.com/library?file_id=libfile_78ef98ae781081918971fb67dc26a9eb&account_id=personal) (2026-10-17T05:47:13.149925+00:00)
- [review-activity-2026-10-16.md](https://chatgpt.com/library?file_id=libfile_21fe7ea97cac8191b05bb885420731a6&account_id=personal) (2026-10-17T04:58:28.925201+00:00)
- [review-activity.md](https://chatgpt.com/library?file_id=libfile_54f63cce6ad8819192eb095bd120722d&account_id=personal) (2026-10-17T05:43:56.550656+00:00)

## Known retrieval gaps

Conversation-only history could not be searched: the history service returned
"Personal context is unavailable for this conversation." Therefore no claim
of exhaustive all-time coverage is made. Future discoveries must be added
under the exact subject without inventing a prior verdict.

The visible conversation contains additional requests/discussions without a
separately identified saved review, including fault-inject initialization,
shmem_initxattrs remount accounting, MGLRU rotation overhead, khugepaged
non-uptodate MADV_COLLAPSE, and Ada's deferred-split migration report.
Their absence from a standalone report is a persistence gap, not evidence
they were unreviewed. Preserve original chat context when recovering them.

Inventory totals: 74 distinct standalone report texts; 115 ledger sections (including historical repeats); 66 evidence archives. These are record counts, not unique patch counts.
