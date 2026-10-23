# Review: fs/proc/task_mmu: pin mm_users in do_pagemap_scan()

Review key: R-017. Author: Ngoc Quy. Date: 2026-10-14.
Base: 24a19b953e2a3d0ea5a8c4951a0ab8f32720c907.
Status: SOURCE AND NATIVE FORMAL REVIEW COMPLETE; native Sashiko pending.

## Standing-rule inventory (established before source review)

A01. Read local workflow and current active ledger.
A02. Establish this fixed inventory before assessing the diff.
A03. Read full submitted patch, header, changelog and correspondence.
A04. Obtain matching kernel source; establish source/patch integrity.
A05. Verify Fixes commit and historical mechanism.
A06. Read complete modified function and surrounding implementation.
A07. Enumerate direct and consequential callers.
A08. Trace callees and their actual conditions/effects.
A09. Inventory shared-state producers, writers and clearers.
A10. Inventory all significant readers and side-effect consumers.
A11. Build old/new producer-to-consumer and state-class matrix.
A12. Check Kconfig, architecture, NUMA, object/input variants.
A13. Check error, abort, partial progress, retry, undo and exit paths.
A14. Trace allocations, references, ownership and freeing.
A15. Analyze RCU, locking and required ordering against implementations.
A16. Give a concrete concurrency timeline; establish locks/actors.
A17. Trace userspace-visible consequences and actual workload.
A18. Recover rationale for existing guards and historical safeguards.
A19. Compare contrasting architectures/configs/hotplug/lifecycle.
A20. Assess normal and adverse path cost; compare alternatives.
A21. Prove the original reported bug independently.
A22. Prove the proposed fix independently, separate from bug proof.
A23. Trace initial publication, inverse operation and final state.
A24. Assess clean upstream architectural placement and alternatives.
A25. Check akin behavior/related failure patterns in MM.
A26. Check caller/feature reachability and compiler/test compatibility.
A27. Adversarial failure-state equivalence and cleanup ownership.
A28. Adversarial hostile bounds, termination and rollback inputs.
A29. Adversarial architecture/configuration contrasting effects.
A30. Adversarial transitive sleepability and context.
A31. Adversarial lock-drop lifecycle and reverse transitions.
A32. Adversarial 3-actor interleavings and rejected validation.
A33. Adversarial multi-field/snapshot consistency.
A34. Second pass challenges a dismissal and derived-state relationship.
A35. Similar-bug search includes caller reachability and exceptions.
A36. Verify Sashiko default HEAD/date; pin one full revision.
A37. Read Sashiko actual stage-selection and verification pipeline.
A38. Read same-SHA Sashiko core, false-positive, relevant guides.
A39. Independently perform Sashiko GOAL domain.
A40. Independently perform Sashiko IMPLEMENTATION domain.
A41. Independently perform Sashiko EXECUTION-FLOW domain.
A42. Independently perform Sashiko RESOURCES domain.
A43. Independently perform Sashiko LOCKING domain.
A44. Independently perform Sashiko SECURITY domain.
A45. Independently perform Sashiko HARDWARE applicability/coverage.
A46. Sashiko verification and hard-case checks, findings + dismissals.
A47. Native Sashiko check when available/authorized; truthfully report.
A48. Verify Tejun default HEAD/date and pin full revision.
A49. Apply Tejun patchset-review and all applicable dependencies.
A50. Verify Chris prompt default HEAD/date and pin full revision.
A51. Apply Chris
review-core/technical/false-positive/build/index/triggered.
A52. Compare new upstream methodology SHAs to known checkpoints.
A53. Reconcile independent, Sashiko and Tejun/Chris inventories.
A54. Distinguish author-reported tests, our tests and external assertions.
A55. Decide explicitly model yes/no with source-grounded rationale.
A56. Resolve whether formal 3-actor model is needed.
A57. If modeling, translate/falsify/check and report bounds/versions.
A58. Resolve memory-ordering claims using LKMM/herd7 when needed.
A59. Impact: observable symptom, trigger, diagnostic signature.
A60. Impact: scoped affected users, prerequisites and severity.
A61. Impact: expected user-visible improvement.
A62. Impact: operational lookup and backport diagnostics.
A63. Impact: substantiate no-effect if claimed; otherwise request detail.
A64. Stable: apply documented real-bug, tests, size and benefit rules.
A65. Stable: check introducing version, candidates and backport risks.
A66. Stable: check tag location and proper documented routes.
A67. Verify submission style, changelog, comments and patch scope.
A68. Report defects versus uncertainty, impact/stable and verification.
A69. Use strictly ASCII and wrap authored lines at 75 columns.
A70. End with brief plain-text copy-ready LKML reply, unsent.
A71. Update review activity under a stable case/finding ID when available.
A72. Read-only: never edit production code or publish without authority.
A73. Preserve canonical artifact names and verify download paths.
A74. Pre-verdict audit statuses, evidence and exact compliance count.

## Technical verdict

Code assessment: SOUND for the lifetime fix; the added `!mm` is
REDUNDANT and masks an impossible-state programming error by turning
a previously visible Oops into quiet `-ESRCH`. Remove it. The existing
use-after-free is proven from source and the new reference protects
all walking and copyout phases. Request clearer impact and testing.
Native TLC and tla-mctj validate a bounded PlusCal/TLA+
model, with an actual UAF counterexample in the old protocol. This is
not an unconditional take/Reviewed-by because native Sashiko and a
kernel build or targeted runtime tests were not run.

Impact-changelog: needs detail. Describe the consequence up front: a
PAGEMAP_SCAN ioctl racing with exit of a task containing a shared hugetlb
VMA can use a freed rwsem, potentially crashing or corrupting kernel
memory.
This is SOURCE-SUPPORTED POTENTIAL harm, not an observed oops/KASAN report.
The author has not supplied a reproducer or runtime evidence. The rest of
the mechanism in the supplied changelog is substantially accurate.

Stable: prospective candidate after mainline merge and testing. The
introduced ioctl exists in v6.7 and later; v6.6 does not contain the
introducing commit. The 9-line diff is below the 100-line context limit,
is directly relevant to a harmful memory-safety bug and carries the
stable Cc in the commit trailers. Verify each target stable branch's
teardown and hugetlb code before backport; do not extrapolate from Fixes.

## Post-review correction: added-guard necessity (2026-10-19)

The original review explicitly said "no code change to request". That
was WRONG: it verified the lifetime fix but failed to independently
check whether the new `!mm` clause was reachable. This corrective
check was done AFTER the initial verdict and cannot be credited to
its original standing-rule compliance count. It also illustrates why
reading general false-positive guidance alone is insufficient.

Guard audit: 4 of 4 checked; 1 redundant; 0 unresolved
Retrospective diagnostic effects: 4 of 4 checked; 1 masks an Oops.

- G01 REDUNDANT: new `!mm` in `do_pagemap_scan()`.
  `pagemap_open()` calls `proc_mem_open()`; if it returns NULL,
  open returns `-ESRCH` without installing a usable file. Otherwise
  the non-NULL mm pointer goes into `file->private_data` and
  `do_pagemap_cmd()` passes that unchanged to this function. Exit
  leaves the pointer allocated through mm_count; it does not turn
  private_data into NULL. There is no reachable true case for G01
  through this file operation; remove the clause. Its added error
  return suppresses the previous Oops on an impossible NULL input.
- G02 NECESSARY: `!mmget_not_zero(mm)` in the same expression.
  After opening `/proc/pid/pagemap`, the task may exit, dropping
  `mm_users` to zero while the file retains an `mm_count` reference.
  This is a reachable true case; the failure prevents scanning a
  released address space and returns `-ESRCH`. Diagnostic effect:
  a real teardown race is reported rather than walking freed memory.
- G03 NECESSARY: original `if (ret)` following `pagemap_scan_get_args()`
  now goes to `out_mmput`. User-supplied invalid arguments can make
  this branch true; without the new cleanup target, the successfully
  acquired mm_users reference would leak. The old direct return was
  valid only before that reference was acquired. Diagnostic effect:
  the caller still sees the original argument-error code.
- G04 NECESSARY: original `if (ret)` following bounce-buffer setup
  now goes to `out_mmput`. Allocation can fail with `-ENOMEM`; the
  new path releases mm_users. Neither branch repeats G02's purpose.
  Diagnostic effect: the caller still sees `-ENOMEM`.

The user also identified the more important diagnostic consequence:
`!mm` is not only redundant; it masks an impossible internal state.
The successful pagemap-open path guarantees a non-NULL pointer. If
that contract is somehow violated, the old code would Oops, bringing
the programming error to attention. The proposed NULL test silently
turns it into an expected-looking `-ESRCH`, potentially allowing the
underlying kernel bug to go undiagnosed. This is a diagnostic
regression and an independent reason to remove the clause. It does
NOT follow that we should add BUG_ON() or create new Oops sites; the
point is to avoid concealing an existing invariant failure.

The user's author-facing objection explicitly raised this point.
The assistant's earlier description as "one small cleanup" missed
its substance. The correct review disposition is: remove the guard
to preserve diagnostics, not merely simplify the expression.

This is a retrospective correction, not evidence that the ORIGINAL
review met the newly introduced guard audit gate. The old model only
checked the lifetime protocol; formal checking did not establish
whether the additional NULL clause was needed.

Suggested code change:

```diff
-	if (!mm || !mmget_not_zero(mm))
+	if (!mmget_not_zero(mm))
 		return -ESRCH;
```

## Source and identity

- Patch: '[PATCH] fs/proc/task_mmu: pin mm_users in do_pagemap_scan()'.
- Author: Ngoc Quy <ngocquy0700@gmail.com>, 2026-10-14.
- Base: torvalds/linux 24a19b953e2a3d0ea5a8c4951a0ab8f32720c907
  (Linux 7.3-rc7). fs/proc/task_mmu.c blob
  5c54aebe211824681a5c30e03464af51697b11ce matches the diff index.
- Fixes: 52526ca7fdb905a768a93f8faa418e9b988fc34b,
  2023-10-18, contains the original ioctl implementation.
- Public posted copy: https://lkml.iu.edu/2610.1/14732.html
  No additional review response or version was established.
- Patch applicability was supported by the exact preimage hash, not an
  actual git-am or compiler run.

## Original-bug proof

1. fs/proc/task_mmu.c:2398-2415: pagemap_open() saves a pointer
   returned by proc_mem_open() and pagemap_release() calls mmdrop().
   fs/proc/base.c:818-837 explicitly mmgrab()s and mmput()s: it holds
   mm_count, but does not prevent mm_users from reaching zero.
2. fs/proc/task_mmu.c:3227-3271: before the patch, do_pagemap_scan()
   starts walks under mmap_read_lock_killable() without mmget_not_zero().
   This is not a writer lock and does not prevent exit_mmap().
3. kernel/fork.c:1211-1216: a final mmput() calls __mmput(), which calls
   exit_mmap() at 1193. mm/mmap.c:1299-1316: exit_mmap() holds
   mmap_read_lock() across unmap_vmas(), and upgrades to write only
   before free_pgtables() and tear_down_vmas().
4. mm/memory.c:2292-2310: unmap_vmas() passes ZAP_FLAG_UNMAP and invokes
   hugetlb_zap_begin()/hugetlb_zap_end(). mm/hugetlb.c:5370-5407:
   the end helper calls __hugetlb_vma_unlock_write_free(). The latter
   clears vma->vm_private_data, up_write()s, and kref_put()s the lock
   (mm/hugetlb.c:381-406, 373-379).
5. mm/pagewalk.c:336-359: walk_hugetlb_range() calls
   hugetlb_vma_lock_read() while the scanner holds the mmap read lock.
   mm/hugetlb.c:292-303: hugetlb_vma_lock_read() obtains its rwsem
   pointer via vma->vm_private_data then calls down_read().
   It does NOT pin the lock with a kref between load and down_read.
6. Concrete old interleaving: scanner holds mmap_read_lock, loads a
   shareable VMA lock pointer, pauses; exiter takes the same mmap read
   lock, obtains that lock in write mode, clears the VMA pointer,
   releases and kref_put()s the lock, then scanner down_read()s the
   freed rwsem. Another possible interleaving has the scanner take
   the rwsem after writer up_write() but before kref_put(); the
   subsequent kref_put() can free a reader-held rwsem.

The race is between two mmap read lockers; a superficially reassuring
mmap-lock check is insufficient. No actual kernel UAF or sanitizer event
was observed in this review. The author supplied no before-fix test.

## Fix proof and full-path outcome

- A successful mmget_not_zero(mm) executes atomic_inc_not_zero() on
  mm->mm_users (include/linux/sched/mm.h:136-139). A final mmput()
  cannot reach __mmput()/exit_mmap() while the ioctl retains a user.
  If the last user has already dropped to zero, the atomic acquisition
  fails and returns -ESRCH before any address-space access.
- The added mmput() runs after all walk iterations, notifier intervals,
  pagemap_scan_writeback_args(), and kfree(p.vec_buf). The acquired
  reference spans the mmap lock gaps between scan iterations, including
  user copies and retry after -ENOSPC. Its scope is correctly larger
  than the individual mmap_read_lock() intervals.
- Early error cases after pin: invalid arguments (-EFAULT/-EINVAL),
  bounce-buffer ENOMEM, signal EINTR, killable mmap lock failure,
  pagewalk/notify/flush error, partial vector ENOSPC, and copyout
  failure all go through the common mmput() path. The one pre-pin
  failure (-ESRCH) acquires no reference and takes no mmput().
- The before/after user-visible difference if mm_users==0 is an
  -ESRCH response rather than possibly parsing malformed ioctl args
  first. This is consistent with pagemap_read() and other proc readers.
- If the scanner's mmput() becomes the last mm_users reference, it
  may run exit_mmap() in scanner context. This is AFTER all scanner
  mmap_lock uses, so does not recreate the unsafe overlap.
- CONFIG_PROC_PAGE_MONITOR gates the ioctl. With CONFIG_HUGETLB_PAGE=n
  the hugetlb callback is absent and this particular trigger cannot
  occur; the new reference remains valid for normal walks. With
  hugetlb enabled, the lock acquisition is generic before the
  architecture-specific huge_pte_offset() paths (x86, arm64, powerpc).
- A VM_MAYSHARE hugetlb VMA with VM_NORESERVE still obtains a
  per-VMA lock: mm/hugetlb.c:426-458 and 6693-6704. A zero hugepage
  pool need not suppress the walker: walk_hugetlb_range() takes the
  VMA lock even if hugetlb_walk() returns no PTE. The anonymous
  MAP_HUGETLB file setup path uses HUGETLB_ANONHUGE_INODE, not the
  permission check specific to HUGETLB_SHMFS_INODE
  (fs/hugetlbfs/inode.c:1497-1544). Access to a target's pagemap
  still requires proc ptrace read permission; the attacker can
  typically use a same-credential, dumpable process.

### State-class matrix

| Relevant class | Original behavior | Patched behavior |
|---|---|---|
| Live mm, stable VMAs | Scan; no additional mm_users pin | Scan with pin |
| Last mmput before ioctl | May walk teardown state | -ESRCH, no walk |
| Last mmput during ioctl | Can overlap teardown | Exit deferred |
| Scanner between chunks | No pin across released mmap lock | Pin remains |
| Shared hugetlb VMA | Can use freed rwsem | Exit blocked |
| Ordinary VMA, exit | VMA teardown under write phase | Same, extra pin |
| Bad arguments, live mm | Existing error | Same error, mmput |
| Empty/ENOMEM buffer | No pin | Balanced mmput |
| Partial/aborted scan | Existing return semantics | Balanced mmput |
| Other munmap() | Write lock/detachment excludes walker | Unchanged |

## Independent dismissals, hard cases and analogues

D1. "mmap_read_lock already excludes exit": REJECTED. exit_mmap()
    also uses mmap_read_lock() in its unmap phase; two readers can run.
D2. "The hugetlb pointer is cleared before freeing, so NULL is safe":
    REJECTED. Reader can cache the previous pointer and use it after
    kref_put(). This is a UAF, not reliably a NULL-pointer failure.
D3. "The lock's down_read pins its object until up_read": REJECTED.
    Before down_read the reader holds no ref. Between up_write() and
    kref_put(), a concurrent down_read can start and the writer can
    still free its backing object. Hugetlb's release helper also
    re-checks vm_private_data, so a cleared pointer can suppress
    the expected up_read; source and bounded-model hard case checked.
D4. "mmget_not_zero can resurrect a dying mm": REJECTED.
    atomic_inc_not_zero() cannot increment mm_users from zero.
D5. "The new cleanup may call mmput without a pin": REJECTED.
    All jumps to out_mmput occur after a successful acquisition;
    the pre-pin ESRCH path returns directly.
D6. "Other unmap paths can still free that lock under a read lock":
    Not established. mm/vma.c:1478-1560 detach affected VMAs under
    mmap write protection before vms_complete_munmap_vmas() optionally
    downgrades the lock (1410-1459). An existing scanner holding read
    excludes the initial write, and a later scanner cannot look up
    the detached VMA. exit_mmap() lacks that early detachment.
D7. "Holding mm_users across user-copy can indefinitely delay exit":
    It can defer teardown if the scanner blocks, but this is an
    intentional consequence of safely accessing a live address space;
    other proc readers already use this protocol. No new lock cycle
    or measurable performance regression was established.

Similar-code search: fs/proc/task_mmu.c m_start/m_stop,
do_procmap_query, show_smaps_rollup, pagemap_read and clear_refs;
fs/proc/task_nommu.c; fs/proc/base.c mem_rw/environ; mm/vma.c
munmap and mm/mmap.c exit_mmap; all relevant known proc paths
that obtain mm_count separately acquire mm_users for address-space
access, or acquire an mm_users reference through get_task_mm().
No confirmed additional instance of the missing-pin pattern.

## Adversarial and security assessment

Actors: A scanner, B exiting mm owner, C second scanner. The owner and
scanners operate on mm_users, mmap_lock, vma->vm_private_data and the
hugetlb rwsem. mmap_lock read/read is compatible; acquiring an rwsem
through a cached pointer without retaining its owner is unsafe.
The patch closes the producer-to-consumer gap with a user reference,
not by assuming that revalidation or lock reacquisition retains ownership.
There is no new lock/drop protocol inside do_pagemap_scan().

The existing threat is reachable through ioctl on a task whose pagemap
can be opened. For a same-credential target, the submitter's
unprivileged/no-hugepage path is supported by the MAP_HUGETLB and
NORESERVE source sequence. A repeatable triggered freed-rwsem access
could crash the kernel or cause memory corruption; no claim of
successful exploitation, observed fleet crash or proven privilege
escalation is made. Input-range validation is pre-existing and not
changed by this patch. No hardware interrupts, DMA or peripheral
registers participate.

## Three-actor executable scheduler model

Script: task-mmu-mmusers-model.py (Python 3; independently executed).
One VMA, one initial mm_users owner, two racing ioctl scanners, one
exit/last-mmput actor. The already opened proc file holds mm_count.
State splits: atomic_inc_not_zero/dec_and_test, mmap read admission,
VMA-lock pointer load, rwsem down_write/up_write, pointer clear,
kref_put/free, and read-lock acquisition. Includes scheduler choices
between any enabled transitions and adverse two-scanner ordering.

Original: 902 distinct states, 2,134 transitions, max depth 21.
Counterexamples reached (a) lock read omitted when vm_private_data
was cleared, (b) free while scanner has a read lock, (c) down_read
on freed rwsem, and (d) up_read after free. Patched: 187 distinct
states, 380 transitions, max depth 21; none of these violations.
Falsification: original source ordering without the new mm_users pin
reproduces the failure, patched ordering does not.

This was an exhaustive bounded state-graph exploration of that Python
abstraction. It assumes sequentially consistent atomic operations,
valid in-flight file references, no other hugetlb-lock references,
and successful memory allocation. It omits arbitrary kernel tasks,
signals, faults, other VMA mutation, hotplug and relaxed-memory
proofs. This standalone Python search was not itself a TLC/tla-mctj
run, a kernel runtime test or an LKMM/herd7 proof. The separate native
TLA+ check described next now covers the same central protocol.

## Native PlusCal/TLA+ formal verification (2026-10-19)

User supplied archive: akpm-tla-tools.tar(1).gz
SHA256: 263a5d1b9befc04b871d573108d90e899e92d3ee457257b37fa0e69d65ab483f

Archive contains two regular files, no links or extraction escapes:
- tla-mctj: ELF x86-64, version 0.1.2, SHA256
  22d800c21fe331ec707851ca23a77ac253369e40825b6859d9b54bf70881878c
- tla2tools.jar: TLC 2026.10.15.145915 (rev 932d35e), SHA256
  15d103b7e5617780bcc904c0af12f1ad242e2b345c0301136c5be4588f17edac
- Java 21.0.12.1. The supplied binaries were run in this environment.

Model: task_mmu_mmusers.tla, written from Linux 7.3-rc7 C paths.
Two scanner actors and one final-mmput / exit_mmap actor. Configurations:
- task_mmu_mmusers.cfg: PATCHED=TRUE, all three safety invariants.
- task_mmu_mmusers-old.cfg: PATCHED=FALSE, NoUAF invariant.
- task_mmu_mmusers-old-null.cfg: PATCHED=FALSE, NoNull invariant.
The PlusCal translator and SANY successfully parsed the model.

All runs used two model-checker workers and exhaustive exploration of
reachable states, not random simulation. Native checker outcomes:

| Engine | Configuration | Distinct states | Depth | Result |
|---|---|---:|---:|---|
| tla-mctj | old/UAF | 545* | 13 | NoUAF violated |
| TLC | old/UAF | 522* | 14 | NoUAF violated |
| tla-mctj | old/NULL | 270* | 10 | NoNull violated |
| TLC | old/NULL | 244* | 11 | NoNull violated |
| tla-mctj | patched | 504 | 32 | Three invariants pass |
| TLC | patched | 504 | 32 | Three invariants pass |

*Falsification runs stopped upon the first violation; state totals
therefore differ by checker scheduling and are not full old-graph sizes.
TLC and tla-mctj independently agree on the final patched state count.
Each instance completed in under one second of checker wall time here.

TLC's 14-state old/UAF counterexample replays on the original C:
1. Final owner mmput: mm_users 1 -> 0 (kernel/fork.c:1211-1216).
2. exit_mmap takes mmap_read_lock (mm/mmap.c:1299).
3. __hugetlb_zap_begin takes the hugetlb VMA rwsem for writing
   (mm/hugetlb.c:5370-5380).
4. Unpinned scanner enters pagemap_scan and takes mmap_read_lock
   (fs/proc/task_mmu.c:3227,3254); the two reads coexist.
5. Scanner tests and caches vm_private_data in hugetlb_vma_lock_read
   (mm/hugetlb.c:292-297), without yet calling down_read().
6. __hugetlb_vma_unlock_write_put clears vm_private_data, executes
   up_write, then kref_put frees the lock (mm/hugetlb.c:381-394).
7. Scanner calls down_read on the cached, freed rwsem: NoUAF fails.

The separate old/NULL counterexample checks the first
__vma_shareable_lock() test and the second vm_private_data load as
distinct accesses. Clearing the pointer between them can produce a
NULL dereference in the model. This additional hazard is sensitive
to actual compiler reuse and ordering; the UAF trace alone suffices
for the reviewed bug. The patched model excludes both interleavings.

Model assumptions and deliberate exclusions:
- Source-file pin keeps mm_count positive through ioctl invocation.
- One valid shared hugetlb VMA, kref=1, no other PMD-share holders.
- mm_users initial 1, at most two scanner references, one final drop.
- Each scanner makes one ioctl; exiting actor runs one teardown.
- mmap_read_lock admissions coexist; semaphore read and write modes
  exclude one another while held, but not after up_write.
- Atomic nonzero get and decrement/test are indivisible operations.
- The model assumes sequential consistency (SC); it does not analyze
  weak memory, compiler optimization or the Linux memory model.
- No runtime kernel, KASAN, lockdep, signals, other VMA mutation,
  allocator reuse, faults, OOM or RCU concurrent reader is modeled.
- Pointer publication, clearing, rwsem release and final kref_put
  are separate transitions, matching the C lifetime boundary.

Typical native commands (from the directory holding the files):

```sh
java -cp tla2tools.jar pcal.trans -nocfg task_mmu_mmusers.tla
java -cp tla2tools.jar tla2sany.SANY task_mmu_mmusers.tla
tla-mctj -workers 2 -config task_mmu_mmusers-old.cfg \
  task_mmu_mmusers.tla
tla-mctj -workers 2 -config task_mmu_mmusers.cfg \
  task_mmu_mmusers.tla
java -cp tla2tools.jar tlc2.TLC -workers 2 -difftrace \
  -config task_mmu_mmusers-old.cfg task_mmu_mmusers.tla
java -cp tla2tools.jar tlc2.TLC -workers 2 -difftrace \
  -config task_mmu_mmusers.cfg task_mmu_mmusers.tla
```

Verdict: model: yes; both native checkers run and falsify the old
protocol, then pass the patched model. This is bounded formal evidence
for the ownership protocol, not a proof of the entire Linux kernel.

## Guided coverage and upstream revisions

All upstream material was fetched read-only on 2026-10-19, after the
independent source pass. Heads are unchanged from the preceding R-016
checkpoint; no new upstream method diff was applicable:

- Sashiko f6e2e172e1e669b6767a4c74fe91d062b41fd71c
  (2026-10-19 21:20:55 UTC). Actual
  src/workflows/linux_patch_review.rs planning/GOAL/IMPLEMENTATION/
  EXECUTION-FLOW/RESOURCES/LOCKING/SECURITY/HARDWARE/verification/
  hard-case definitions checked, with its separately vendored guides.
  Native runner not installed; manually applied each applicable domain.
- Tejun cbb4478d0f73e15907335e70a2dc2fe54a9e7167
  (2026-10-18 06:22:24 UTC). Reviewed patchset-review,
  formal-model-check, evidence, validation scope, kernel idioms,
  patch descriptions, tags, comments and build expectations.
- Chris Mason d048f8742f6740c38833adf02e87901412d771ca
  (2026-10-01 11:53:46 UTC). Reviewed review-core, technical,
  false-positive, build, subsystem index, callstack and MM-VMA,
  MM-pagewalk, hugetlb, locking, RCU, VFS, syscall and allocation
  guides. Sashiko's copies diverge for some guides despite REVISION
  naming this same Chris commit; source snapshots were kept separate.

Sashiko GOAL: minimal source-mm lifetime pin; no alternative design
with a smaller synchronization impact shown. IMPLEMENTATION: all
new control-flow and cleanup labels traced. EXECUTION-FLOW: all
return/error/empty/partial paths and exit_mmap inverse analyzed.
RESOURCES: mm_count/mm_users and hugetlb kref owners inventoried.
LOCKING: mmap read/read, hugetlb rwsem and writer/free interval
traced, including three actors and lock drops. SECURITY: unprivileged
same-credential entry, ptrace permissions and Kconfig prerequisites
checked; do not claim exploit beyond source-supported UAF. HARDWARE:
generic code precedes arch-specific huge_pte_offset(), and x86,
arm64, powerpc variants were considered; no new hardware operation.

Tejun/Chris guided pass separately checked the complete caller/callee
chain, lock states, old/new branches, similar-code patterns, warning
behavior, error precedence, direct cost, Fixes/stable tags and the
strongest dismissed-hypothesis counterarguments. Reconciliation:
all three tracks support the same UAF and corrected mm_users lifetime;
none supports an introduced regression. More general race concerns
about VMAs, per-VMA locking or a temporary NULL are not treated as
additional patch defects without a distinct reachable trace.

## Runtime verification and changelog request

No kernel build, userfaultfd/hugetlb stress execution, KASAN/lockdep
run, author reproducer, native Sashiko or herd7 ran. Native TLC and
tla-mctj model checks were run as documented above.
Recommended targeted test: with CONFIG_PROC_PAGE_MONITOR and
CONFIG_HUGETLB_PAGE, map shared anonymous hugetlb memory with
MAP_NORESERVE and an empty hugepage pool, race repeated PAGEMAP_SCAN
ioctls on a same-credential target against task exit, exercise scans
with and without PM_SCAN_WP_MATCHING, and compare before/after with
KASAN/SLUB debugging. Verify -ESRCH once the target has torn down,
correct partial/error returns, and no leaked mm_users reference.
The existing selftest home is tools/testing/selftests/mm/pagemap_ioctl.c.
All of these are recommended tests, not tests executed here.

Suggested changelog addition, close to the beginning:

"A PAGEMAP_SCAN of a task exiting with a shared hugetlb VMA can race
with exit_mmap() and use a freed hugetlb_vma_lock. This is a
potentially unprivileged kernel use-after-free and may crash the
system. It does not require any huge pages to be allocated when the
mapping uses MAP_NORESERVE."

If the author has a reproducible crash, show its distinctive
KASAN/oops signature and before/after test evidence. Otherwise
explicitly present the harmful consequence as source-supported,
not observed. The reported mechanism is useful and should remain.

## Executed/not-executed tools

EXECUTED: pinned GitHub source queries, Fixes/release ancestry lookup,
public patch lookup, preimage blob verification, Python 3 finite
explicit-state scheduler checker (902 old states/187 patched states),
source-guided manual Sashiko, Tejun and Chris coverage; PlusCal
translation, SANY parsing, and native TLC and tla-mctj model checks.
NOT RUN: native Sashiko, kernel compiler/build, actual ioctl repro,
KASAN, lockdep or herd7.


## Per-rule compliance evidence

Standing rules: 72 of 74 applied; 1 inapplicable; 1 unresolved

The denominator A01-A74 was fixed before inspecting the Linux source.
APPLIED means the described check was actually performed; it does not
mean that a kernel compiler or native external reviewer was run.

A01 APPLIED: Read uploaded 923-line workflow and latest review-activity.md.
A02 APPLIED: A01-A74 saved before first Linux source retrieval.
A03 APPLIED: Reviewed complete supplied email and public 2026-10-14
             archive; no replies recovered.
A04 APPLIED: Base 24a19b953e2a, Linux 7.3-rc7; task_mmu.c blob 5c54aebe2118
             matches.
A05 APPLIED: Fetched Fixes 52526ca7fdb9 and checked ancestry of v6.6/v6.7.
A06 APPLIED: Read task_mmu.c:3227-3298 in full and scan callbacks.
A07 APPLIED: do_pagemap_cmd:3300, pagemap file operations:3314;
             proc_mem_open.
A08 APPLIED: Read pagemap_scan_get_args, init, walk_page_range, hugetlb
             lock, mmput.
A09 APPLIED: mm_users mmget/mmput; hugetlb VMA pointer
             clearing:hugetlb.c:391.
A10 APPLIED: pagemap_read and scan, pagewalk, mmap exit, hugetlb rwsem
             users.
A11 APPLIED: Nine-row state-class and old/new outcome matrix in this
             report.
A12 APPLIED: PROC_PAGE_MONITOR, HUGETLB_PAGE, VM_MAYSHARE/NORESERVE,
             x86/arm64.
A13 APPLIED: All ioctl failure and -ENOSPC/-EINTR/ENOMEM/copyout paths
             traced.
A14 APPLIED: mm_count/mm_users references and hugetlb_vma_lock kref traced.
A15 APPLIED: mmap read/read overlap, hugetlb rwsem write/read, no new RCU
             site.
A16 APPLIED: Old ten-step pointer-cache/free/down_read counterexample.
A17 APPLIED: Same-credential pagemap ioctl, freed rwsem, potential
             crash/corruption.
A18 APPLIED: Fixes ioctl 2023 commit and proc_mem_open mmgrab/mmput
             contract.
A19 APPLIED: ARM64/powerpc/x86 huge PTE variants; generic rwsem comes
             first.
A20 APPLIED: Two extra atomic ops per ioctl, teardown deferral,
             alternatives evaluated.
A21 APPLIED: exit_mmap read unmap -> ZAP_FLAG_UNMAP -> free before scan
             down_read.
A22 APPLIED: Atomic nonzero pin blocks last-mmput teardown; all exits
             balanced.
A23 APPLIED: Pin before get_args; inverse mmput after copyout and buffer
             free.
A24 APPLIED: Compared full-ioctl mmget against per-chunk pin and mmap write
             lock.
A25 APPLIED: Searched proc mmap readers and detached-munmap analogous
             teardown.
A26 APPLIED: Verified known symbols/Kconfigs/preimage; no compile/test
             claimed.
A27 APPLIED: Each early failure after pin goes to out_mmput; pre-pin
             returns.
A28 APPLIED: Invalid pointer/range, empty vector, end<=start, ENOSPC,
             signals.
A29 APPLIED: No new arch hook; hugetlb rwsem generic before
             huge_pte_offset.
A30 APPLIED: ioctl is sleepable; mmput outside held mmap lock and after
             notifier.
A31 APPLIED: Cached lock pointer loses ownership; no lock-drop authority
             transfer.
A32 APPLIED: Two scanners plus last owner explored in executable scheduler.
A33 APPLIED: mm_count does not imply mm_users; VMA pointer can stale before
             lock.
A34 APPLIED: Rechecked munmap downgrade and indirect VMA-pointer dismissal.
A35 APPLIED: Searched task_mmu, task_nommu, base, memory/pagewalk and vma.
A36 APPLIED: Pinned Sashiko f6e2e172e1e669b6767a4c74fe91d062b41fd71c.
A37 APPLIED: Read linux_patch_review.rs core/stages/verification and hard
             cases.
A38 APPLIED: Same-SHA vendored core, false-positive and eight MM/VFS
             guides.
A39 APPLIED: GOAL: narrow mm_users repair; no unjustified design change.
A40 APPLIED: IMPLEMENTATION: no early return missing reference release.
A41 APPLIED: EXECUTION-FLOW: scan stages, errors, writeback, hugetlb
             teardown.
A42 APPLIED: RESOURCES: mm_count/mm_users/kref and VMA-pointer lifetime.
A43 APPLIED: LOCKING: shared mmap_lock and hugetlb rwsem interleaving.
A44 APPLIED: SECURITY: same-credential entry, capability and no hugepool
             path.
A45 APPLIED: HARDWARE: generic lock path; compared huge PTE architecture
             variants.
A46 APPLIED: Hard cases, findings and substantive dismissals source
             verified.
A47 UNRESOLVED: Native Sashiko runner and full local kernel tree absent;
                manual stages used.
A48 APPLIED: Pinned Tejun cbb4478d0f73e15907335e70a2dc2fe54a9e7167.
A49 APPLIED: Patchset review and evidence/model/build/idioms/description
             deps read.
A50 APPLIED: Pinned Chris d048f8742f6740c38833adf02e87901412d771ca.
A51 APPLIED: Chris core, technical, false-positive, build, index, MM/VFS
             guides.
A52 APPLIED: All SHAs match R-016; no new relevant changes to compare.
A53 APPLIED: Three independent question inventories reconciled in report.
A54 APPLIED: No author test attached; our Python test separate from kernel
             tests.
A55 APPLIED: model: yes (three-actor mm-users/hugetlb lifetime
             interleavings).
A56 APPLIED: Two scanners and one exiting owner; direct source-backed
             steps.
A57 APPLIED: PlusCal translated and SANY parsed; TLC/tla-mctj both
             falsified old (UAF and NULL) and passed patched model.
             Configurations, bounded counts, depths, time, hashes,
             trace replay and exclusions recorded above.
A58 NOT APPLICABLE: No new barrier/relaxed-ordering scheme; standard atomic
                    refcount.
A59 APPLIED: Possible UAF/crash/corruption, no observed incident/sanitizer
             trace.
A60 APPLIED: CONFIG_PROC_PAGE_MONITOR/HUGETLB and same-credential read
             access.
A61 APPLIED: Protected scan instead of using a deallocated VMA rwsem.
A62 APPLIED: Named ioctl, exit timing, hugetlb flags and recommended KASAN
             test.
A63 APPLIED: No no-effect claim; request explicit user-visible risk up
             front.
A64 APPLIED: Stable rules checked: real harm, 9 lines, needs test and
             mainline.
A65 APPLIED: Commit not ancestor of v6.6, ancestor v6.7; targets need
             audit.
A66 APPLIED: Cc: stable in trailers; no submission/push performed.
A67 APPLIED: Subject, Fixes tag, 9-line diff, no changed source comments.
A68 APPLIED: Separate proven old bug, code repair, unobserved impact and
             tests.
A69 APPLIED: ASCII and authored lines at <=75 columns verified below.
A70 APPLIED: Draft LKML reply in literal text block, unsent.
A71 APPLIED: Created new R-017 entry and linked report in
             review-activity.md.
A72 APPLIED: No production source edit, commit, push, patch apply or
             publication.
A73 APPLIED: Canonical task-mmu-review.md and review-activity.md verified.
A74 APPLIED: Fixed A01-A74 inventory audited before verdict; exact counts.

Unresolved obligations:
- A47: native Sashiko unavailable. This does not invalidate the
  completed manual pinned-stage coverage, but is not a native run.

Inapplicable obligation:
- A58: no new release/acquire, barrier, or memory-ordering scheme to
  verify with herd7. Atomic nonzero refcount use follows existing
  mmget_not_zero()/mmput() contracts; source proves the zero exclusion.

## LKML-ready reply (DRAFT ONLY, NOT SENT)

```text
The code fix looks correct to me. The mm_count reference retained by
proc_mem_open() does not keep the address space alive, and two holders
of mmap_read_lock() can overlap during exit_mmap(). In particular,
__hugetlb_zap_end() can free the VMA-specific rwsem before the scan
has taken its read lock. Taking mm_users before the scan and dropping
it after the final copyout closes that window. I did not find a
reference imbalance on the error or partial-result paths.

Could you please lead the changelog with the userspace-visible effect:
a PAGEMAP_SCAN racing with task exit can use freed kernel memory and
potentially crash the kernel? Please distinguish an observed crash
from the source-supported UAF if no reproducer is available.

Please also report before/after testing of this revision. A useful
stress case is a shared MAP_HUGETLB | MAP_NORESERVE mapping, with no
huge pages in the pool, while another task repeatedly scans its
pagemap and the mapped task exits. KASAN coverage would be valuable.

Why the new `!mm` test? pagemap_open() guarantees a non-NULL mm
on this ioctl's call path. If do_pagemap_scan() ever receives NULL,
that is an internal programming error. The current code would Oops
and draw attention to it; the new check silently converts it into
-ESRCH and makes such a bug harder to find. Please remove `!mm` and
use `if (!mmget_not_zero(mm))`.

Otherwise this looks suitable for -stable after the fix is merged
and the testing and userspace impact are documented.
```
