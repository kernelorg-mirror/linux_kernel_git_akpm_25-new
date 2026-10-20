# R-016: Memoryless-node demotion target reset

Status: REVIEWED, conditional recommendation; original full patch mail
and author test context unavailable. No source-level code regression
identified in the supplied one-line change.

## Identification

Subject: [PATCH] mm/memory-tiers: reset demotion targets of nodes without memory
Author: Gregory Price
Fixes: 6c542ab75714 (mm/demotion: build demotion targets based on
explicit memory tiers)
Kernel source checked: 70dd4ee72eb2d5793c62e71c14e3aba78e5a4e56
Full email/Message-ID: not supplied or independently retrieved.
Reviewer: independent source pass, manual SHA-pinned Sashiko and
Tejun/Chris passes; no native agents or model consensus.

## Concise verdict

BUG PROOF: offline_pages() clears N_MEMORY before notifying
  NODE_REMOVED_LAST_MEMORY (mm/memory_hotplug.c:2133-2147). In the
  notifier, clear_node_memory_tier() removes the tier and
  establish_demotion_targets() calls disable_all_demotion_targets(). Its
  old N_MEMORY loop skipped the now-memoryless node, leaving
  node_demotion[nid].preferred stale.

FIX PROOF: for_each_node() ranges over N_POSSIBLE; node_demotion[] is
  allocated with nr_node_ids entries, set from highest possible node ID.
  __node_get_memory_tier() guards absent NODE_DATA. The new reset clears
  memoryless nodes while establishment still rebuilds only N_MEMORY and
  tier masks from live membership. The enabled-memory-node outputs are
  unchanged.

IMPACT: No in-tree user-visible consequence established. All in-tree
  preferred-target consumers were located in mm/vmscan.c; they operate on
  actual source folios. Successful offline_pages() first requires
  test_pages_isolated() to find every page free, poisoned or explicitly
  offlined; isolated reclaim folios prevent that step. On re-online
  N_MEMORY is set before the notifier rebuild, even in the old
  implementation. The stronger assertion that no possible
  external/out-of-tree observer can ever notice the stored bits is NOT
  proved.

ARCHITECTURE: The direct reset is clearer than spreading special cleanup
  among notifier cases and has cold-path linear N_POSSIBLE cost. It does
  not add a reclaim fast-path scan or change allocation policy.

STABLE: not justified. The change repairs bookkeeping with no shown real
  user-benefiting failure, lacks reported real-kernel test results, and
  has not been shown to meet stable-kernel rules. A Fixes: tag does not
  itself qualify the patch.

IMPACT-CHANGELOG: no known effect (substantiated for reviewed in-tree
  readers). Request precise invariant-hygiene rationale and refrain from
  claiming a proven runtime bug; the original full changelog was
  unavailable, so the exact wording is unverified.

RECOMMENDATION: The one-line code change appears sound, but do not issue
  unconditional take or a Reviewed-by tag for this incomplete
  original-email review. Confirm the actual changelog and available test
  evidence before taking as a bugfix.

## Source evidence / state classes

- SOURCE OFFLINE: mm/memory_hotplug.c:2029-2165;
-   mm/page_isolation.c:556-650;
-   mm/memory-tiers.c:376-518,580-614,881-904.

- SOURCE ONLINE: mm/memory_hotplug.c:1137-1252, N_MEMORY at 1207, node
-   notifier at 1237; set_node_memory_tier() mm/memory-tiers.c:542-572.

- SOURCE READERS: mm/memory-tiers.c:302-374;
-   mm/vmscan.c:325-343,966-1037,1058-1075,1545-1557;
-   mm/page_alloc.c:5814-5853.

- SOURCE SIZE/CONFIG: include/linux/nodemask.h:513;
-   mm/mm_init.c:1710-1715; mm/page_alloc.c:195-205,286;
-   include/linux/memory-tiers.h; architecture NUMA setup in
-   arch/x86/mm/numa.c and arch/powerpc/mm/numa.c.

- ONE-LINE DIFF: change only the outer reset in
-   disable_all_demotion_targets(). dump_demotion_targets() and
-   establish_demotion_targets() deliberately keep N_MEMORY loops.

### Producer-to-consumer matrix

- STATE: possible + memory + tier; OLD: old clears then rebuilds; NEW: new
-   same; EFFECT: demotion target for active node unchanged

- STATE: possible + no memory + old stale preferred; OLD: old leaves stale
-   bits; NEW: new zeros bits; EFFECT: no ordinary folio is resident for
-   in-tree demotion

- STATE: possible + no memory + no pgdat; OLD: old skips; NEW: new zeros
-   preferred; guarded NULL tier; EFFECT: no dereference of absent pgdat

- STATE: CPU-only possible node never holding pages; OLD: old skips; NEW:
-   new zeros originally empty preferred; EFFECT: no user-facing change

- STATE: failed memory removal; OLD: N_MEMORY remains set; rollback; NEW:
-   no new changed branch; EFFECT: rebuild if invoked processes active
-   node identically

- STATE: subsequent first memory online; OLD: N_MEMORY before notifier;
-   reset + assign; NEW: new reset + same assign; EFFECT: both restore
-   current target

- STATE: target node removed, source still memory; OLD: source rebuilt old
-   and new; NEW: no changed source target; EFFECT: allocation uses
-   N_MEMORY live check

## Three-actor and RCU hard case

ACTOR A: reclaim running on a source node reads memtier->lower_tier_mask
  under an RCU read lock, releases RCU, and next_demotion_node()
  separately reads the source preferred mask under another RCU section.
  Thus these are NOT an atomic multi-field snapshot.

ACTOR B: memory offline clears and rebuilds these masks. If B is removing
  the last pages from the source, test_pages_isolated() rejects in-use
  pages before setting N_MEMORY false. Any isolated folios used by A make
  removal retry; when B completes there are no folios from that source for
  A to demote. If B instead removes only a target, source remains in
  N_MEMORY, so old and new rebuild its preferred mask identically.

ACTOR C: a competing node online / offline transition is serialized with B
  through hotplug serialization and memory_tier_lock. On successful
  first-memory online N_MEMORY is already true before rebuilding targets,
  meaning both old and new select a fresh mask for future reclaim.

RECHECK: A captured allowed mask can still outlive an RCU section. That
  limitation exists independently of this loop change, and
  next_demotion_node() documents lack of guaranteed continuing
  online/eligibility. The N_MEMORY filter in find_next_best_node() and
  fallback allocation recheck target availability; no newly reachable
  harmful path was established.

BUDGET: acquires=[A: RCU on tier, then RCU on preferred; B: memory hotplug
  writer and memory_tier_lock], releases=[A: both RCU sections, B:
  synchronize_rcu before tier destroy], refs_live_at_free=[A: none on tier
  after read, only copied nodemask], free_reachable_without_pin=no (tier
  unlink/free after grace); logical_free=storage-free;
  use=copied-mask-based decision.

## Separate guided-track results

Sashiko GOAL: sound bookkeeping invariant; challenged whether there is a
  real bugfix. IMPLEMENTATION: loop bounds, pgdat, live-tier membership
  verified. EXECUTION-FLOW: success, cancel, re-online, early setup and
  disabled config covered.

Sashiko RESOURCES: no new allocation; permanent demotion array and RCU
  tier lifetime checked. LOCKING: memory_tier_lock, hotplug ordering and
  independent RCU read windows. SECURITY: root-controlled hotplug and
  reclaim input cannot exploit a new bounds or lifetime defect. HARDWARE:
  generic possible NUMA nodes, x86/powerpc contrasting setup; no new
  device/IRQ/DMA operations.

Sashiko verification: concerns retained for (1) stale state, (2) NULL
  pgdat, (3) nr_node_ids bounds, (4) tier lifetime and (5) split RCU
  snapshots. Disposition: (1) confirmed old invariant violation repaired,
  (2-4) source-rejected as introduced bugs, (5) source-disproved as a
  newly harmful in-tree case. No native Sashiko run.

Tejun/Chris: pinned patchset-review and all applicable deps, evidence
  discipline, formal decision, review-core, false-positive, kernel build,
  callstack, mm-alloc, mm-reclaim, locking and RCU guides. Reachability
  confirmed, new entry point none, Kconfig additions none, code style
  unchanged. Distinct guided pass found no new regression.

Similar MM bug search: all occurrences of node_demotion,
  next_demotion_node and node_get_allowed_targets were searched. Other
  loops which intentionally enumerate only N_MEMORY are target
  construction, debug reporting and allocation, not metadata teardown; no
  additional sibling proven.

## Version pins and comparison

Sashiko: f6e2e172e1e669b6767a4c74fe91d062b41fd71c, committed 2026-10-19
  21:20 UTC. Compared with f4b72fa04f232fe5f2183d32d7cf9c09e5d735ec:
  prescreen/planner temperature handling changed in linux_patch_review.rs,
  not the seven required domains; the last commit changes PRESS.md only.
  Its vendored technical/false-positive/index differ from Chris despite
  REVISION matching Chris.

Tejun: cbb4478d0f73e15907335e70a2dc2fe54a9e7167, committed 2026-10-18
  06:22 UTC. Compared with c8cc6a8bee854cf2850f44e0a61be581c19f1d4e.
  UPGRADING adds $MODEL_CHECKER default tla-mctj; no bearing on this
  no-model decision.

Chris: d048f8742f6740c38833adf02e87901412d771ca, committed 2026-10-01
  11:53 UTC, unchanged since recorded checkpoint. Checked on 2026-10-19
  PT.

## Verification actually run

Python mask enumeration: python3 /mnt/data/.memory_tiers_state_check.py.
  Enumerated 3,900 legal one-to-five-node membership masks and 2,541
  states in which an old stale possible-but-not-memory entry survives
  reset. The preferred bit in this abstraction means only that an entry is
  nonempty; it does not model target-node identities or real migration.
  All 3,900 patched memoryless entries zero, and live-node entries are
  unchanged. This is a bounded loop truth table, NOT a kernel regression
  test or TLA+ proof.

model: no. The loop expands a writer set, not a new shared-state protocol,
  lock-drop owner transfer or new memory-order pairing. The three-actor
  analysis above was independently source-traced. No
  TLA+/PlusCal/TLC/tla-mctj/herd7 run.

Native Sashiko: not run. Kernel build: not run. Runtime hotplug/reclaim
  stress: not run. KASAN/KCSAN/lockdep: not run. Formal checker: not run.
  Semcode-native reviewer agents: not run. Only read-only GitHub source
  fetching and Python mask test executed.

Full original email, all mail replies, author test data and any full
  preimage beyond the supplied one-line change remain absent. The source
  tree uses the unmodified line and was not modified or rebuilt.

## LKML-ready reply (draft, NOT SENT)

```text
The change looks correct as a cleanup of stale demotion metadata.

On successful removal of the last memory, offline_pages() clears
N_MEMORY before the memory-tier notifier rebuilds demotion targets.
The existing loop therefore misses the removed node.  Iterating
N_POSSIBLE clears that entry safely, including where NODE_DATA is NULL.

I did not find an in-tree user-visible failure from the stale bits:
reclaim uses the targets for actual source folios, and successful
memory offlining first drains those pages.  When a node is onlined
again, both versions rebuild its entry after setting N_MEMORY.

Please describe this as an invariant cleanup in the changelog, rather
than implying a demonstrated runtime regression.  I would not mark
it for -stable without a concrete user benefit and testing evidence.

I have no objection to the one-line code change itself, subject to
checking the complete posted patch and changelog.
```

## Precommitted standing-rule compliance (66 obligations)

Standing rules: 63 of 66 applied; 2 inapplicable; 1 unresolved

SRC-01 APPLIED -- Read authoritative workflow and active ledger; identify
  history and constraints
  evidence: Read both supplied authoritative files and the ledger index;
  evidence:   created the fixed 66-rule inventory before source
  evidence:   inspection.

SRC-02 UNRESOLVED -- Retrieve full patch/cover/replies/tests and
  distinguish exact proposed change
  evidence: Only the one-hunk diff, author, subject, Fixes line and a
  evidence:   summary of the no-effect claim were provided. The original
  evidence:   complete email, Message-ID, replies and any reported testing
  evidence:   were not recovered from public search. These cannot be
  evidence:   audited verbatim.

SRC-03 APPLIED -- Establish matching kernel source and inspect surrounding
  implementation
  evidence: Pinned Linux 70dd4ee72eb2; checked
  evidence:   mm/memory-tiers.c:260-518,542-614,881-936,
  evidence:   mm/memory_hotplug.c:1137-1252,2029-2165; headers and
  evidence:   reclaim.

SRC-04 APPLIED -- Verify Fixes commit, history and previous failure
  behavior
  evidence: Verified 6c542ab75714fe90dae292aeb3e91ac53f5ff599 and its
  evidence:   original N_MEMORY reset, against the present hotplug
  evidence:   transition.

SRC-05 APPLIED -- Check each patch/series state, applicability and
  bisectability
  evidence: The supplied single loop hunk exactly matches the old loop at
  evidence:   memory-tiers.c:381; no series or subsequent fix supplied. No
  evidence:   git-am or compilation claimed.

IND-01 APPLIED -- Perform independent first-principles pass before
  external prompts
  evidence: Independent source pass in .memory_tiers_independent.txt
  evidence:   completed before fetching guidance prompts.

IND-02 APPLIED -- Trace each changed branch and all direct/indirect
  callers
  evidence: Call chain: offline_pages -> NODE_REMOVED_LAST_MEMORY ->
  evidence:   memtier_hotplug_callback -> clear_node_memory_tier ->
  evidence:   establish -> disable; all search hits for
  evidence:   next_demotion_node, node_get_allowed_targets and
  evidence:   node_demotion checked.

IND-03 APPLIED -- Enumerate writers/readers/clearers and dependent state
  evidence: Producers set_node_memory_tier + establish; clearer
  evidence:   clear_node_memory_tier + disable; readers can_demote,
  evidence:   demote_folio_list, next_demotion_node,
  evidence:   node_get_allowed_targets; dump and node_is_toptier are
  evidence:   distinct consumers.

IND-04 APPLIED -- Construct input-state and producer-to-consumer old/new
  outcome matrix
  evidence: Producer/consumer table in this report; executed 3,900 finite
  evidence:   bit-mask states for 1..5 possible nodes; old stale vs new
  evidence:   zero on memoryless.

IND-05 APPLIED -- Trace success, failure, retry, cleanup and inverse
  operations
  evidence: offline_pages success, signals/notifier/migration
  evidence:   failures/rollback; onlining N_MEMORY before notifier;
  evidence:   inverse offline->online->offline and failed onlining; no
  evidence:   changed error branch.

IND-06 APPLIED -- Trace locks, atomic/RCU publication, ownership and
  lifetimes
  evidence: memory_tier_lock and mem_hotplug_lock writers; synchronize_rcu
  evidence:   after clearing; RCU readers, separate snapshots, kobject
  evidence:   lifetime; demotion mask is static allocated, not freed.

IND-07 APPLIED -- Check architecture, NUMA and kernel configuration
  variants
  evidence: Generic N_POSSIBLE vs N_MEMORY macros,
  evidence:   MAX_NUMNODES/nr_node_ids, x86 and powerpc possible-node
  evidence:   setup; CONFIG_NUMA_MIGRATION and hotplug-off paths.

IND-08 APPLIED -- Enumerate hostile and boundary inputs and loop
  termination
  evidence: Empty/all possible masks, sparse node IDs, absent NODE_DATA,
  evidence:   n=0 memory nodes, all-memory nodes; bounded for_each_node
  evidence:   and nr_node_ids allocation.

IND-09 APPLIED -- Verify exact user-visible failure and corrected outcome
  evidence: No in-tree consumer capable of demoting actual folios after a
  evidence:   successful last-memory removal: page_isolation.c:556-650
  evidence:   refuses in-use folios; subsequent online rebuilds. No
  evidence:   observed userspace fault was supplied.

IND-10 APPLIED -- Assess changed normal-case costs and architectural
  alternative
  evidence: More metadata zeroes for N_POSSIBLE during cold rebuild only,
  evidence:   no new reclaim-path work; direct cleanup in existing owner
  evidence:   simpler than special-case callbacks.

IND-11 APPLIED -- Separate reachable old bug proof from new fix proof
  evidence: Bug: old loop skips removed node after N_MEMORY clear. Fix:
  evidence:   new loop clears each possible slot; establishment still only
  evidence:   adds live N_MEMORY preferred targets. Different proof
  evidence:   obligations recorded.

IND-12 APPLIED -- Verify assertions and substantive dismissals with source
  evidence: Dismissal of absent pgdat deref checked at
  evidence:   memory-tiers.c:260-274; out-of-bounds checked
  evidence:   mm/mm_init.c:1710-15; challenged cached allowed mask
  evidence:   separately.

IND-13 APPLIED -- Search sibling MM paths for same bug mechanism
  evidence: Search of all node_demotion and demotion reader hits;
  evidence:   memory-tiers.c dump/establish use N_MEMORY legitimately, and
  evidence:   nearby page_alloc/vmscan skip nonmemory for actual
  evidence:   allocation; no confirmed sibling.

IND-14 APPLIED -- Check tests/reproducer coverage and distinguish
  execution from claims
  evidence: Compared suggested hotplug and NUMA stress to exact
  evidence:   old-failure state; no author test report or kernel execution
  evidence:   supplied; bitset Python test is not a kernel test.

IND-15 APPLIED -- Evaluate changelog accuracy, diagnostic impact and
  correction
  evidence: No visible harm found in in-tree consumer paths; no-effect
  evidence:   claim source-supported but full commit prose absent.
  evidence:   Recommend clear invariant-hygiene rationale rather than
  evidence:   overstated bugfix.

IND-16 APPLIED -- Assess stable branch eligibility, tests, tags and
  prerequisites
  evidence: Read stable-kernel-rules.rst and submitting-patches.rst at
  evidence:   pinned Linux SHA; no identified user benefit or author test,
  evidence:   so stable: not justified.

ADV-01 APPLIED -- Failure-state equivalence, cleanup and retained
  ownership
  evidence: All altered cleanup happens only when rebuild executes; old
  evidence:   source state is intentionally cleared; failed offlining
  evidence:   retains N_MEMORY and does not run removed-last-memory
  evidence:   notifier.

ADV-02 APPLIED -- Hostile bounds, empty/full states and fixed-step
  termination
  evidence: Enumerated no-memory, all-memory, CPU-only, sparse ID, NULL
  evidence:   pgdat and 0/1 preferred bits; masks bounded, no new
  evidence:   unbounded loop.

ADV-03 APPLIED -- Architecture/configuration override and reverse effects
  evidence: Generic for_each_node expands to N_POSSIBLE, not an allocator
  evidence:   loop; x86/powerpc setup and absent pgdat guard; no
  evidence:   page-table or DMA teardown changed.

ADV-04 APPLIED -- Caller context and transitive sleepability
  evidence: Only extra operation is zeroing masks plus existing guarded
  evidence:   read in cold rebuild, with memory_tier_lock held and
  evidence:   existing sleepable synchronize_rcu; no new sleeping callee.

ADV-05 APPLIED -- Lifecycle, lock drops, exclusive ownership and complete
  inverse
  evidence: Tier publication uses rcu_assign_pointer; teardown sets
  evidence:   pointer NULL then waits for RCU before unlinks/destroy. No
  evidence:   ownership transfer or relevant lock drop introduced by
  evidence:   one-line change.

ADV-06 APPLIED -- Concrete independent multi-actor counterexamples (three
  actors)
  evidence: Three actors: A reclaim has isolated source folios; B offline
  evidence:   cannot pass test_pages_isolated until they are gone; C
  evidence:   online serialized with B, sets N_MEMORY before rebuilding.
  evidence:   Other target offlines rebuild active sources identically.

ADV-07 APPLIED -- Related-state snapshot coherence for cached pointers and
  node states
  evidence: A can copy lower_tier_mask, release RCU, and later read
  evidence:   preferred in a separate section; this is an existing
  evidence:   advisory selection race, bounded by live-page/isolation and
  evidence:   target allocation rechecks, not an atomic snapshot
  evidence:   guarantee.

ADV-08 APPLIED -- Final adversarial challenge of safe dismissal and
  derived relationship
  evidence: Second pass challenged NULL NODE_DATA dismissal (checked guard
  evidence:   and bounds), and challenged stale allowed-mask snapshot
  evidence:   (checked vmscan folio isolation, page_isolation test and
  evidence:   onlining ordering).

SAS-01 APPLIED -- Verify current Sashiko HEAD SHA and compare known
  checkpoint
  evidence: HEAD f6e2e172e1e669b6767a4c74fe91d062b41fd71c (2026-10-19
  evidence:   21:20 UTC), compared with
  evidence:   f4b72fa04f232fe5f2183d32d7cf9c09e5d735ec; pipeline diff
  evidence:   includes temperature propagation, no reduction in
  evidence:   specialists; latest HEAD adds only PRESS.md.

SAS-02 APPLIED -- Read pinned pipeline/stage selection/verification source
  evidence: Read src/workflows/linux_patch_review.rs: prompt instructions
  evidence:   212-329; prescreen 1441-89, planning 1610-1700, stage table
  evidence:   1739-1803, verify/post-verification/report.

SAS-03 APPLIED -- Read applicable pinned Sashiko-vendored guides
  evidence: Fetched vendor REVISION, core
  evidence:   callstack/technical/false-positive/severity, subsystem
  evidence:   index, MM reclaim, alloc, locking, RCU and other triggered
  evidence:   indirect guides at exact Sashiko SHA. Vendor differs from
  evidence:   Chris.

SAS-04 APPLIED -- GOAL specialist analysis
  evidence: GOAL: restored demotion-metadata invariant after memory
  evidence:   hot-unplug; no demonstrated new API or observable bug.
  evidence:   Considered preserving old loop vs clearing at notifier.

SAS-05 APPLIED -- IMPLEMENTATION specialist analysis
  evidence: IMPLEMENTATION: reset includes all possible indices; pgdat
  evidence:   NULL guard; node_demotion allocated by nr_node_ids; only
  evidence:   N_MEMORY entries subsequently get new targets.

SAS-06 APPLIED -- EXECUTION-FLOW specialist analysis
  evidence: EXECUTION FLOW: whole old/new loop, memory tier teardown,
  evidence:   rebuilder, success/reject/rollback paths, initial late init
  evidence:   and reonline.

SAS-07 APPLIED -- RESOURCES specialist analysis or source-based exclusion
  evidence: RESOURCES: node_demotion allocation permanent; memtier RCU
  evidence:   lifetime, remove-before-free and callback teardown checked.
  evidence:   No new alloc/free.

SAS-08 APPLIED -- LOCKING specialist analysis or source-based exclusion
  evidence: LOCKING: memory_tier_lock writer, memory hotplug serializes
  evidence:   node events, RCU reader/write boundaries and cached
  evidence:   nodemasks explicitly examined.

SAS-09 APPLIED -- SECURITY specialist analysis or source-based exclusion
  evidence: SECURITY: memory hotplug admin-controlled, reclaim accessible
  evidence:   indirectly to workloads, but no new out-of-range, UAF, data
  evidence:   disclosure or harmful permission-bypass path.

SAS-10 APPLIED -- HARDWARE specialist analysis or source-based exclusion
  evidence: HARDWARE: architecture-dependent NUMA possible/memoryless
  evidence:   semantics contrasted x86/powerpc and non-NUMA; no new
  evidence:   register/DMA/IRQ hardware operation.

SAS-11 APPLIED -- Preserve candidate/dismissed concerns and separately
  verify both
  evidence: Retained stale-state proof, NULL deref/OOB/UAF negative
  evidence:   hypotheses, and cached-allowed race as a hard case; verified
  evidence:   rather than voting between tracks.

SAS-12 APPLIED -- Focus unresolved/contested dismissals with hard-case
  verification
  evidence: HARD CASE: reader allowed mask can outlive its RCU section.
  evidence:   Checked reclaim holds live source folios and hotplug
  evidence:   page-isolation gate; does not establish a new in-tree bad
  evidence:   result. No generic global snapshot claim.

SAS-13 APPLIED -- Check series end-state and bisectability in Sashiko
  reconciliation
  evidence: One-hunk stand-alone patch; no following series changes
  evidence:   supplied; final old/new state read with this single diff and
  evidence:   check of preimage.

SAS-14 APPLIED -- Determine availability of native runner, execute if
  available, disclose
  evidence: Searched runner availability: no sashiko binary or runnable
  evidence:   pinned native pipeline in container; no suitable complete
  evidence:   kernel checkout. Native Sashiko: not run; manual
  evidence:   seven-domain + two-stage audit.

TJ-01 APPLIED -- Verify Tejun default HEAD and relevant revision delta
  evidence: HEAD cbb4478d0f73e15907335e70a2dc2fe54a9e7167 (2026-10-18
  evidence:   06:22 UTC); compared with
  evidence:   c8cc6a8bee854cf2850f44e0a61be581c19f1d4e; UPGRADING
  evidence:   introduces model checker default.

TJ-02 APPLIED -- Load pinned patchset-review and all applicable dependency
  modules
  evidence: Fetched pinned review/patchset-review.md,
  evidence:   formal-model-check.md, core evidence/validation/waits,
  evidence:   code/kernel-idioms, patch-description/comment/cover and
  evidence:   build guidance.

TJ-03 APPLIED -- Apply evidence, kernel idioms, patch/change descriptions
  and review gates
  evidence: Checked trace and diff scope, source proof, stable tags,
  evidence:   kernel idioms, no new signature, no new fast-path work, and
  evidence:   no unjustified defense.

TJ-04 APPLIED -- Apply pinned formal-model decision procedure
  evidence: Used formal-model-check decision triggers: no newly added
  evidence:   shared-state protocol or ownership handoff; existing writer
  evidence:   is mutex serialized; bitset finite logic instead.

CH-01 APPLIED -- Verify Chris HEAD SHA and review relevant changes
  evidence: HEAD d048f8742f6740c38833adf02e87901412d771ca, 2026-10-01
  evidence:   11:53 UTC, unchanged against ledger.

CH-02 APPLIED -- Read core/technical/false-positive/build/subsystem index
  guides
  evidence: Read pinned kernel/review-core.md, technical-patterns.md,
  evidence:   false-positive-guide.md, subsystem/build.md and index;
  evidence:   checked reachability, Kconfig, control category and
  evidence:   full-path dismissal rules.

CH-03 APPLIED -- Read and apply all triggered Chris
  MM/concurrency/RCU/hotplug patterns
  evidence: Applied matching Chris mm-reclaim, mm-alloc, locking, RCU,
  evidence:   callstack and relevant indirect guides; contrasted vendor
  evidence:   false-positive and technical additions.

REC-01 APPLIED -- Reconcile independent, Sashiko and Tejun/Chris coverage
  inventories
  evidence: Merged all three tracks by state classes and call-chain
  evidence:   inventory; all found same harmless extension to memoryless
  evidence:   metadata, not independently corroborating models.

REC-02 APPLIED -- Independently verify contradictions and dissenting
  dismissals
  evidence: Reverified presumed safety of NULL pgdat and array bounds;
  evidence:   reexamined RCU multi-snapshot hazard with hotplug isolation
  evidence:   and alloc target validation.

REC-03 APPLIED -- Separate bug, fix and architecture verdicts
  evidence: Bug proof established; fix proof established for metadata;
  evidence:   architecture suitable; no user-facing benefit demonstrated
  evidence:   and no stable nomination.

MOD-01 APPLIED -- Explicit model yes/no decision and source-grounded
  rationale
  evidence: model: no (no new multi-actor protocol, arithmetic or lifetime
  evidence:   handoff); executable 3,900-state mask enumeration,
  evidence:   explicitly not a formal checker.

MOD-02 APPLIED -- Decide necessity of three-actor ownership model
  evidence: Three-actor interleavings reviewed manually; no new ownership
  evidence:   across lock-drop and memory_hotplug prevents source-folio
  evidence:   survival at final transition.

MOD-03 NOT APPLICABLE -- If warranted, construct representative state
  protocol and falsify old
  evidence: No new ownership/publication protocol or lock-drop handoff:
  evidence:   the change expands the set of node-indexed entries cleared
  evidence:   by an existing writer, retaining the existing RCU reader
  evidence:   protocol. A bounded bit-mask truth table was the appropriate
  evidence:   extra check; a PlusCal protocol is not triggered.

MOD-04 NOT APPLICABLE -- If checker used, record
  checker/bounds/states/commands and replay
  evidence: No formal model checker was selected or run under MOD-03.
  evidence:   tla-mctj, TLC, pcal and herd7 are absent; there is no
  evidence:   checker output, configuration or state count to record.

MOD-05 APPLIED -- Distinguish synchronization/order from SC interleaving;
  LKMM if needed
  evidence: RCU lifetime publication and grace examined in C; separate
  evidence:   allowed/preferred reads are an existing advisory snapshot
  evidence:   issue. No new release/acquire pattern to test with LKMM.

REP-01 APPLIED -- Record findings, IDs, evidence, uncertainty and
  disposition in ledger
  evidence: R-016 compact active case, finding IDs and full detailed
  evidence:   report written into canonical review-activity.md and
  evidence:   memory-tiers-review.md.

REP-02 APPLIED -- Audit every obligation with evidence and one explicit
  status
  evidence: All 66 fixed entries given one status and line-based
  evidence:   source/test evidence in per-rule matrix in this report.

REP-03 APPLIED -- Independently recount N/I/U against precommitted
  inventory
  evidence: Counts recomputed by program from untouched precommitted
  evidence:   66-entry list, with reasons for unresolved and inapplicable.

REP-04 APPLIED -- Report native Sashiko/build/tests/models individually
  and accurately
  evidence: Native Sashiko, kernel build, in-kernel runtime, formal
  evidence:   checker and LKMM: not run; only source analysis and finite
  evidence:   Python mask enumeration performed.

REP-05 APPLIED -- State verdict/impact-changelog/stable and applicable
  LKML action
  evidence: Verdict: code correct for restoring metadata; withhold
  evidence:   unconditional take pending whole mail/changelog; stable not
  evidence:   justified and impact no known effect supported.

REP-06 APPLIED -- Provide concise unsent plain ASCII <=75-column text
  email
  evidence: Concise LKML reply authored as literal 7-bit ASCII lines <=75
  evidence:   columns, no claimed tag or sending.

REP-07 APPLIED -- Preserve file/source read-only integrity and canonical
  filename
  evidence: No kernel source or original attachments modified; canonical
  evidence:   ledger/report names without date/version suffix.

REP-08 APPLIED -- Provide verified links for each created project document
  evidence: Generated canonical files on disk; paths existence and ASCII
  evidence:   audit checked before linking.

## Unresolved / excluded status explanations

- SRC-02: Only the one-hunk diff, author, subject, Fixes line and a
-   summary of the no-effect claim were provided. The original complete
-   email, Message-ID, replies and any reported testing were not recovered
-   from public search. These cannot be audited verbatim.

- MOD-03: No new ownership/publication protocol or lock-drop handoff: the
-   change expands the set of node-indexed entries cleared by an existing
-   writer, retaining the existing RCU reader protocol. A bounded bit-mask
-   truth table was the appropriate extra check; a PlusCal protocol is not
-   triggered.

- MOD-04: No formal model checker was selected or run under MOD-03.
-   tla-mctj, TLC, pcal and herd7 are absent; there is no checker output,
-   configuration or state count to record.

## Source reference URLs

https://github.com/torvalds/linux/tree/70dd4ee72eb2d5793c62e71c14e3aba78e5a4e56
https://github.com/torvalds/linux/commit/6c542ab75714fe90dae292aeb3e91ac53f5ff599
https://github.com/sashiko-dev/sashiko/tree/f6e2e172e1e669b6767a4c74fe91d062b41fd71c
https://github.com/htejun/kernel-agent-workflows/tree/cbb4478d0f73e15907335e70a2dc2fe54a9e7167
https://github.com/masoncl/review-prompts/tree/d048f8742f6740c38833adf02e87901412d771ca
