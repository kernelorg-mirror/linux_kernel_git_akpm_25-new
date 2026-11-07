# AKPM review index

Canonical discovery filename: akpm-review-index.md
Purpose: cross-chat lookup of review results before test planning.
Updated: 2026-11-06 America/Los_Angeles
Coverage: initially the HVO v4 record below only. This is NOT an inventory
of every historical review. A missing entry means UNKNOWN, not unreviewed.

## Required lookup procedure for testing chats

1. Locate this exact filename in Library. If ranked search misses it,
   enumerate Library filenames with pagination; do not conclude absence
   from a search miss. Read the current version.
2. Match normalized subject, then verify exact version, Message-ID and
   base/patch content. Similar titles or older revisions are not a match.
3. Read the linked current review report, including corrections, rejected
   findings, unresolved hypotheses, gate status and test limitations.
   Fetch evidence only as required. Archive-only text may be superseded.
4. In the test plan record the review key, report Library ID/version and
   the findings covered or deliberately excluded. Do not claim review
   results were checked without reading them.
5. If unavailable, mark review retrieval BLOCKED/UNKNOWN explicitly.
   Independent testing may proceed, but never silently substitute memory
   or an old review for current review-informed planning.

## mm: Decouple folio-based vmemmap optimization from HugeTLB

Exact subject: [PATCH v4 00/13] mm: Decouple folio-based vmemmap optimization from HugeTLB
Aliases: HVO; folio-based vmemmap; HugeTLB vmemmap optimization
Author: Muchun Song
Message-ID: 20261107022756.77731-1-songmuchun@bytedance.com
Base: f735a2c21aa94b7b86a93d36f3b17eecc6d49aba
Report filename: mm-decouple-folio-based-vmemmap-optimization-from-hugetlb-v4-review.md
Evidence Library ID: libfile_3e4ddfe68ec481919d03e7d0d4068ad3
Status: source review performed; formal gate HOLD; no runtime testing here.
Correction: remaining PMD allocation OOM concern is unproven; oversized
boot reservations must be distinguished from an otherwise viable setup.
Report Library ID: libfile_2d7d0b17990881919dfd15299e52878f
Report: https://chatgpt.com/library?file_id=libfile_2d7d0b17990881919dfd15299e52878f&account_id=personal
