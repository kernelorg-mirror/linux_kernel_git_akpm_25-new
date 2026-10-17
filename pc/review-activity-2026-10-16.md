# Review activity archived on 2026-10-16

Archive date: 2026-10-16 (America/Los_Angeles).
A record may be moved here because it is dormant; that does NOT mean
an author accepted its findings or that a patch has merged. Read the
current index in `review-activity.md` before reopening a topic.

## A-001

Subject: mm: various (urgent?) fixes
Original Subject: [PATCH 00/10] mm: various (urgent?) fixes
Author: David Hildenbrand (Arm). Review date: 2026-10-15/16.
State at archive: DORMANT / UNRESOLVED as to author outcomes.
Base SHA: `0fcb05b72344f40806cbe810de8872f1698bf053`.
Source: `mbox(20261016-024832)` (cover + ten patches + replies).
Supporting previous review: `kernel-review-20261016/REVIEW.md`.

No confirmed new code-level regression was found in the ten changes
on the reviewed paths. This is not a guarantee that the patches are
correct; author responses and final merge outcomes were not tracked.

Issues worth revisiting if this series resurfaces:
- [01/10] `mm/vma` commit-charge leakage: proposed regression test
  with a failing MAP_FIXED mapping under overcommit accounting.
- [02/10] and [03/10] hugetlb new-folio lifetime: patched PTL
  protection appeared sound; [03/10] changelog should identify the
  UFFDIO_COPY/UFFDIO_CONTINUE versus MADV_DONTNEED consequences.
- [04/10] cross-VMA unmap address: test moved and multiply mapped
  mappings, including mixed huge page sizes.
- [05/10] reservation-map lock clearing: patched serialization
  looked sound; changelog should describe possible hung page faults
  and collateral stalls, rather than claiming no behavior change.
- [06/10]..[09/10] stale UFFD bits, RWP, and PROT_NONE: regression
  coverage should include UFFD mode changes and forced accesses.
  Some changelogs lacked concrete userspace-visible consequences.
- [10/10] reservation-map fixup: patched VMA selection looked sound;
  test mremap failure and related unwind paths.

Formal checks from the earlier review (bounded TLC 2.19, under SC):
- `ptl_lifetime.tla`: broken variant failed at 12 states; patched
  variant covered 7 distinct states, depth 7, without error.
- `resv_lock_lifetime.tla`: broken variant failed at 34 states;
  patched variant covered 18 distinct states, depth 10, without error.
- These were narrow abstractions, not kernel runtime tests.

No kernel build, runtime selftest or syzkaller reproducer was run in
that review. If resumed, obtain the relevant author reply and target
patch version before interpreting old conclusions as current.

Index key: `mm: various (urgent?) fixes`.
Other search terms: hugetlb, userfaultfd, UFFD_WP, PROT_NONE,
`fixup_hugetlb_reservations`, `mm/mremap`, mmap commit charge.
