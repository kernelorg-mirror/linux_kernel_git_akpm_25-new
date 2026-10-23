# S2: Milestone Batch Review

S2 is one adversarial review of a batch of patches at a milestone. 2-4
sub-agents review the batch in parallel, and one of them also checks prose
and style. A batch that adds or changes a multi-actor protocol over shared
state also gets a PlusCal/TLC model check, and memory-ordering claims get
herd7 litmus tests. The workflow is written for an agent that can spawn
sub-agents (Claude Code or similar), working on a patch stack in a kernel
tree.

Contents:
1. When to run it
2. Tools
3. Prepare the batch
4. Run the reviewers
5. Prose and style checklist
6. Verify the findings
7. Decide on the formal model
8. Write, falsify and run the model
9. Memory ordering: herd7
10. Report and follow-up
11. Reference: PlusCal, TLC config, flags, output, sizing, running
12. Reference: kernel-tla precedents, alternatives, sources

## 1. When to run it

Run S2 once per coherent milestone:
- an implementation or correction batch that is ready for broader testing
- a completed series that is ready for posting

Don't launch reviews patch by patch. Builds and focused development tests
can come before the review. Individual edits and refreshes don't start new
rounds. While the batch is being developed, keep each patch reviewable on
its own.

The review counts against the task's effort budget. Don't add separate
harness, manifest, readiness or acceptance reviews that turn S2 back into a
per-edit gate. A minor correction made after a review gets a focused local
check of what changed and joins the next milestone. It gets a new round
only if it invalidates a material safety or correctness conclusion.

The batch includes everything in the range: tooling, scripts, selftests,
docs and trivial patches. Skip S2 only when the requester explicitly says
to skip the review.

Prose-only batches, such as workflow docs and plans, get a review of scope,
consistency and whether the plan can be executed. They use the writing and
domain guidance below, not the kernel prompts, and nobody traces kernel code
paths for them.

## 2. Tools

### Review prompts

```
git clone https://github.com/masoncl/review-prompts
```

Run `git pull` in the clone before each review. The kernel protocol is:
- `kernel/review-core.md`: the entry point and checklist. It tells the
  agent which other prompts to load for the patch.
- `kernel/technical-patterns.md`: the individual bug patterns.
- `kernel/subsystem/*.md`: subsystem deltas, e.g. `scheduler.md`, `bpf.md`,
  `locking.md`, `rcu.md`, `workqueue.md`, `cleanup.md`, `selftests.md`.
- `kernel/false-positive-guide.md`: the verification pass for findings.
- `kernel/inline-template.md`: the format of an LKML-style inline report.

`./setup.sh <agent> <project>` installs a kernel skill and the `/kreview`,
`/kseries`, `/kdebug` and `/kverify` slash commands (`-h` lists the agents
and projects). S2 doesn't need them, but `/kverify` is handy in step 6.
The prompts can be paired with semcode
(https://github.com/facebookexperimental/semcode), which indexes the tree
for faster and more accurate lookups.

The review-prompts README notes that asking for a "deep dive regression
analysis" gets better compliance with the prompts than asking for a
"review". Use that wording in reviewer prompts.

### Model-check tools

These are only needed when the model check triggers (step 7).

- **TLA+ tools**: one jar, `tla2tools.jar`, containing the SANY parser, TLC,
  the PlusCal translator, TLATeX and the REPL. It needs Java 11 or newer.
  Releases are at https://github.com/tlaplus/tlaplus/releases. 1.7.4
  (2024-08) is the current stable. "1.8.0 Clarke" is a rolling pre-release
  rebuilt from every master commit. No GUI is needed: the Eclipse Toolbox
  is unmaintained and the VS Code extension is optional.
- The jar runs directly. Some distributions package it with `tlc`, `pcal`,
  `tla2sany` and `tla2tex` wrappers that take the same arguments
  (`TLA_JAVA_OPTS` and `TLC_JAVA_OPTS` pass JVM flags to them):
  ```
  java -cp tla2tools.jar pcal.trans -nocfg spec.tla
  java -XX:+UseParallelGC -cp tla2tools.jar tlc2.TLC -workers auto \
      -metadir DIR [-config X.cfg] spec.tla
  ```
- **herd7** from herdtools7 (https://github.com/herd/herdtools7, via opam
  or a distribution package) for memory-ordering questions. The kernel's
  `tools/memory-model/README` requires herd7 7.58 or newer.
- **Precedents**: clone Catalin Marinas's kernel models and read them before
  writing a first model (section 12):
  ```
  git clone https://git.kernel.org/pub/scm/linux/kernel/git/cmarinas/kernel-tla.git
  ```
- **Reading list** (links in section 12): Lamport's PlusCal manual (C
  syntax), "Current Versions of the TLA+ Tools" for TLC options, the TLA+
  summary sheet, Lamport's DCAS paper, and Marinas's LPC 2018 slides.

## 3. Prepare the batch

Collect for the reviewers:
- The patches, one file per patch (`git format-patch base..HEAD`, or the
  quilt series entries).
- The base tree and SHA the stack applies to, so they can read callers.
- One paragraph on what the batch is for and what each patch claims.
- For a correction round, the previous review's findings and what changed
  since, so the reviewers assess the delta instead of starting over.

## 4. Run the reviewers

**How many**: 2-4 sub-agents, launched in one message so that they run
concurrently. Scope each one to the changed behavior.

**Model**: never override it. Sub-agents inherit the parent's model. This
applies to every sub-agent in the workflow, model-writing ones included.

**Split by concern.** For a kernel batch:
- **Correctness**: the review-core.md protocol over every patch:
  regressions, error paths, refcounts, locking, lifetimes and bounds.
- **Concurrency and domain**: races, cpumask safety, budget accounting, BPF
  verifier safety, topology, direction (src vs dst, cpu vs other id
  spaces) and bounds. This reviewer also names every multi-actor protocol
  over shared state in the batch as a candidate for the model check.
- **Prose and style**: always present. Checks every patch against the
  checklist in section 5.
- **Optional fourth**: tooling, scripts and selftests, when the batch has a
  lot of them, or a dedicated reviewer for a non-trivial combination space
  (see "Branch restructuring" below).

Load the prompts once and reuse them for correction rounds. Don't reload the
whole protocol for each delta.

**Every reviewer prompt contains:**
- the patch files, the base tree and SHA, and the intent paragraph
- the protocol files to use (review-core.md and so on), or the style
  checklist for the prose reviewer
- the focus areas for that reviewer
- the incremental rule (below), stated explicitly
- the output format: severity, patch, file:line, and the concrete trigger
  (the input, config or interleaving that causes it)
- "Don't edit any files."

**Review is incremental.** A finding about patch N is judged against the
tree with patches 1..N applied, never the final tree. A concern that is
real at N and resolved by N+k is reported as "valid at N, resolved by N+k",
not dismissed as a false positive. It still matters because it breaks
bisection and the patch can't stand alone. Sub-agents told to check against
"the applied source" default to the final tree. Tell them to check each
patch's incremental state, or do the cross-check against the introducing
patch yourself.

**Rules that set severity:**
- A WARN reachable from any legitimate path is a bug. A change that lets an
  existing WARN fire spuriously is a blocker, fixed in the change or by
  moving the WARN. It is never a "worth guarding?" question and is never
  weighed against how rare the path is.
- Lockless is for a single word that one side writes and the other reads.
  State that another cpu reads as more than one word (a pair, a word plus a
  counter, a record plus an owner) is written and read under a lock. A
  multi-word lockless ordering scheme justified by store and load order is
  a finding. `WRITE_ONCE()` and `READ_ONCE()` pin the compiler, not the
  hardware, so such schemes usually hold only under x86 TSO. If one is
  truly unavoidable, it needs release and acquire barriers written out on
  both sides, a case table, and the model check plus herd7.
- Defensive code without a concrete failure scenario is a finding: a bound,
  NULL or contains check for a case the call path's preconditions already
  rule out. "Just in case", "belt and suspenders" and "airtight" are red
  flags.
- A deviation from a reference implementation (a contributor's prototype,
  a ported diff) must be flagged with its reason. An unflagged half-port is
  a finding.
- **Branch restructuring**: when a patch restructures branches, enumerate
  every combination of the branch conditions and trace old and new
  execution for each, checking the same masks and data, safety properties
  and fallback paths. Give a non-trivial combination space to a dedicated
  reviewer.

**Domain checks for sched_ext batches:**
- A change to `struct sched_ext_ops` (fields, callbacks, semantics) carries
  tools compat in the same patch: a load-time fix-up stanza in
  `SCX_OPS_OPEN()` in `tools/sched_ext/include/scx/compat.h` (probe BTF,
  warn and clear) plus a `COMPAT:` version-list line, so schedulers built
  against newer headers still load on older kernels. Incompatible changes
  get a multi-variant `SCX_OPS_DEFINE()`.
- struct_ops arg-name suffixes (`__arena`, `__nullable`, `__ref`) appear on
  both the cfi stub params and the ops member declaration params, matching.
- Time in scx BPF code comes from `scx_bpf_now()`, not
  `bpf_ktime_get_ns()`, unless a value must line up with CLOCK_MONOTONIC in
  userspace, and then a comment says so.
- Cross-file functions in kernel/sched/ext get the `scx_` prefix.
- Each .c file under kernel/sched/ext is organized as its own compilation
  unit, even though build_policy.c includes them textually. Cross-file
  symbols go through header declarations, config-gated stubs are `static
  inline` in the header's `#else` block, and clangd must pass on each file.
- Build with `CONFIG_SCHED_CORE=y`. With it off, sched code gated on it
  compiles out and a missing include ships unnoticed.

**Example correctness prompt:**
```
Patches 0001-0007 in <dir> apply to <tree> at <sha>. Intent: <paragraph>.

Using review-prompts/kernel/review-core.md and the prompts it tells you to
load, run a deep dive regression analysis of each patch. Judge patch N
against the tree with patches 1..N applied, not the final tree. A problem
fixed later in the series is "valid at N, resolved by N+k". Focus on
error paths, refcounts, lifetimes and bounds. For each finding give
severity, patch, file:line and the concrete trigger. Don't edit any files.
```

**Example concurrency prompt:**
```
<same batch context>

Run a deep dive regression analysis focused on races, cpumask safety,
budget accounting, BPF verifier safety, topology, direction and bounds.
Judge patch N against patches 1..N applied. Name every multi-actor
protocol over shared state the batch adds or changes: the actors, the
shared words, and the claim the code relies on. Report any interleaving
you can't settle by reading as such, with the steps. For each finding give
severity, patch, file:line and the concrete trigger. Don't edit any files.
```

**Example prose prompt:**
```
<same batch context>

Check every patch description, comment and kerneldoc in the batch, and the
code style of every hunk, against the checklist below. Report each finding
as `<patch> (rule) <quote or line> -> <fix>`, or "clean" per patch. Line
widths are checked by a script, don't report them. Don't edit any files.

<paste section 5>
```

## 5. Prose and style checklist

These are the default rules. Where the target tree documents different
conventions, the tree's conventions win. The output is
`<patch> (rule) <quote or line> -> <fix>`, or "clean".

**Line widths are not a reviewer task.** A script checks them before every
refresh, in both directions: no line over the tree's cap, and no line short
enough to take the first word of the next line. Subject lines are unbound.
A print call whose format string pushes the line past the code cap stays on
one line, because a split message can't be grepped. checkpatch's 75-column
warning is not the authority.

### Patch descriptions

The reader is a reviewer looking at this diff. A description says why, not
what. If it reads like a list of everything the patch does, it fails.

Shape:
- One story, one stage per paragraph: who wants this and why, what stands
  in the way, how it is resolved, accepted leftovers. Incidental extras go
  last in a "While at it," paragraph. Imperative voice ("Add X", not "This
  adds X").
- Rationale first, concretely: the consumer and what it wants, then what
  goes wrong without the change. A defect statement is not a rationale, and
  "should be able to" is a prescription, not a want. The problem is the
  missing capability, not one consumer's symptom. Generic infrastructure
  leads with the capability and the class of users.
- The mechanism as properties, not procedure: hot-path cost, who gets
  notified, what gates it, the invariant teardown checks. Never the
  sequence of calls. Field names, call sites, thresholds and pacing math
  belong in comments and kerneldoc.
- For a non-trivial refactor, the equivalence insight that lets a reviewer
  verify it. "Equivalent conversion" alone is not enough.
- Any tightening or loosening of a validation rule set is called out.
- Design tradeoffs and why the obvious simpler version doesn't work. No
  paths not taken unless an elaborate choice needs its rationale.
- A real change names its two or three subtle points as such ("Two things
  need care.") and says why each is right. Every behavior the code shows is
  left to the code. Bullets are for items of one kind a reader has to find,
  never for walking the diff.

Doesn't belong:
- Diff narration: API walkthroughs, algorithm narration, chains of
  functions an event passes through, quoted macro call forms, paraphrase of
  a kerneldoc the diff adds, lists of renamed identifiers, field-by-field
  translations.
- Reassurance: what survives the fix, "all other callers are unchanged",
  leak audits for removed code, correctness or locking proofs that belong
  at the code site. "The pre-existing race in Z is unchanged, separate fix"
  stays when the reader would wonder.
- Speculation and framing: failure modes nobody established, severity
  editorializing, reproducer framing (cover-letter material), positioning
  within the series, reviewer attribution in the body (tags do that),
  educational asides about subsystem internals.
- Sibling patch names, "this series", "this patchset", "iter N". Say "a
  later patch" or "an earlier patch".
- Equivalence mechanics under "No functional change".

By kind:
- One-line fix: 2-3 sentences. The bug, the cause, the fix.
- Prep or mechanical patch (rename, move, factor out): opens with the
  change itself, one clause on its purpose, then "No functional change."
  About four lines. Never a step-by-step of what the next patch does with
  it. "No functional change" only for renames, moves and pure refactors
  with identical machine behavior. A change to ordering, locking or timing
  doesn't qualify. Never "NFC".
- Real logic change: explain fully, but only the non-obvious parts.

Format:
- The subject leads with impact and is capitalized after the prefix
  (`sched_ext: Add foo`). Lowercase nested topic prefixes
  (`sched_ext: scx_qmap - Fix bar`) stay lowercase.
- Commit references are `<sha12> ("full subject")`, exactly 12 chars,
  never bare, never with a "Commit" prefix.
- No `%FOO` kerneldoc prefix in subjects or description bodies.
- "Verified by" in a description is one sentence, no iteration counts or
  machine specs.
- Attribution tags are re-evaluated per patch. `Original-patch-by:` only
  for someone whose diff this specific patch derives from.
- `Link:` URLs are confirmed to resolve. Prefer
  `https://lore.kernel.org/all/<msgid>/`.

Checklist:
1. Do the first one or two sentences say who wants this and what problem
   it solves?
2. Is every sentence the rationale, the problem, the change as properties,
   or a correctness argument the reviewer needs? Are the subtle points
   named as such, with nothing listed that the code shows?
3. Would the reviewer learn anything the diff doesn't already show?
4. Can any sentence be removed while the change stays understandable from
   the diff plus kerneldoc? Then it goes.
5. Is every paragraph under 8 lines and one stage of the story? No
   semicolon chains, every verb and noun conventional, no coined term, no
   unverified identifier, no sibling patch name, no path not taken.
6. Does the length match the kind?

### Comments and kerneldoc

What a comment is for: purpose, constraint, contract, the non-obvious why.
That means hidden invariants callers depend on, the reason for a
non-obvious choice, locking and context preconditions, edge-case semantics,
and return values with several causes. Four or more lines is a smell.

Not:
- play-by-play of the body, or a restatement of the signature
- footnotes teaching another subsystem's semantics
- forward references to sibling patches or future plans
- the derivation behind the why
- trailing imperatives that restate the code ("Migrate instead.")
- a comment on a helper whose name and short body say it all
- status-label prefixes (`LOCKED:`, `RCU:`)
- a clause the reader can see from the code

How to say it:
- Every sentence states a fact or an instruction with a named actor.
- At a test or a write: the fact, the rule and the instruction, in that
  order. "When a cpu goes offline, its ecaps are cleared and must stay zero
  until it comes back online. Don't write non-zero ecaps on an inactive
  cpu." Not a derivation through the mechanism, not the consequence chain
  of the wrong choice.
- Exception: a skip or early return that exists to prevent a failure says
  what goes wrong without it, concretely (the dropped callback, the node
  left linked, the memory freed while still on a list).
- At a check, state the invariant that holds there and what a violation
  means, not how the situation arises.
- At a consumer, cite the layer boundary's contract. Never re-derive it
  from another layer's internals, and never explain how an underlying
  framework works at a use site.
- State a constraint directly, never the adversarial scenario it prevents.
- A barrier-pairing or race comment says who wrote what and what the
  reader on the other side sees, one fact per short sentence. Hazard first,
  then the guarantee with its one load-bearing reason.
- A lockless permission check is justified in two parts: false positives
  are fine because the harm is bounded, and false negatives can't happen
  ("if the caller has seen its ownership, the test sees it too"). If the
  operation completes under the lock that updates the permission state,
  the check must be authoritative under that lock instead.
- Enum and flag entries get one-line meanings. Protocol detail lives in the
  function that enforces it.
- Never two adjacent `/* */` blocks.
- A comment gets its final wording in the patch that introduces it. Later
  patches change it only when they change its meaning.

Form:
- A single-line `/* */` is lowercase with no trailing period. Multi-line
  bodies are full sentences, capitalized, with periods.
- Fully winged (`/*` and `*/` on their own lines) unless the file does
  otherwise. Never a `*/` glued to the last text line.
- Exposed interfaces and any substantial function comment are kerneldoc.
- The kerneldoc summary is `name - Description`, with the description
  capitalized and imperative ("Destroy @cgrp").
- Return values are one imperative sentence in the body ("Return 0 on
  success, -errno otherwise."), no `Return:` tag.
- `@arg: description` with one space, on one line, no tab alignment.

### Voice and words, all prose

- Plain subject-verb-object sentences, one claim each, every clause with
  its real actor. Never make the reader derive a point through "implies",
  an appositive stack or a relative-clause pileup. If it needs a reread, it
  gets rewritten.
- Conventional nouns and verbs, never creative ones. A report is
  suppressed, ignored or lost, not "swallowed". Replace any word that
  wouldn't appear in an existing kernel comment on the same subject.
- No coined terms and no abstract role nouns for variables ("the
  sentinel", "the handle"). Say what the value means at run time.
- No vapid wrappers: "handle", "deal with", "reason about", "steer",
  "drive".
- A code path is called by the code's own name, never a nickname or a word
  the code uses for something else.
- No jargon abbreviations beyond common kernel ones (LLC, SMT, NUMA, RCU,
  IRQ, BPF).
- "block" and "wait" only for paths that sleep. A path returning -EBUSY
  rejects. "inline" means compiler-inlined. Functions get `()`, callbacks
  are `ops.name()`.
- No invented specifics: an API or mechanism named in prose must be
  verified in the source.
- Leave out padding, hedges, reassurance, words the reader supplies, and
  enumerations where one phrase names the class ("every mutable global").
- Periods over semicolons. No `--` or em-dash joins. ASCII only. Single
  space after a period. A paragraph past 8 lines gets split.

### Code style

Structure:
- Bigger chunks: no single-caller helpers without a concrete reason (two or
  more callers, a separable contract, a config stub boundary).
- Gate an out-of-line function with an early return at its top. No
  `__foo()` wrapper split and no `if (cond) foo();` at call sites.
- Fold a one-use guard into the condition it gates.
- `guard()`/`scoped_guard()` over manual lock/unlock pairs when the
  critical section is scope-shaped.
- No naked `{ }` blocks to scope variables.
- Pure moves are their own patch. Restructuring, renames and gating come
  as a follow-up patch.
- Every patch is self-contained (leaves the tree correct) and
  self-justified (never "to set up patch N+12"). Prerequisites land in or
  before the patch that needs them.
- Single-statement if/else never gets braces. Never add or remove braces on
  untouched code.
- A single guarded statement takes the positive test: `if (cond) do_x();`,
  not `if (!cond) continue; do_x();`.
- Every hunk is justified by the stated purpose: no moved blocks, no brace
  changes on untouched code, no dropped debug messages, no collateral. An
  unjustified hunk means the patch should be split.

Declarations and layout:
- Helper names say the object and the field they write, or the op they
  call, verbatim. The inverse of an existing name keeps its word order. No
  `_node` suffix for a list node (it reads as NUMA).
- A helper is defined directly above its first user.
- Headers group by kind (types, prototypes, inlines) and follow the
  definition order of the .c file.
- Loop variables are declared with the other locals, `s32` by default, not
  in the `for` header.
- Related constants go in an `enum`, not several `#define`s.
- No cross-line whitespace alignment. When an already aligned block's
  column shifts, realign the whole block.
- An expression that fits within the width on one line stays on one line.
- Out-params after inputs, implicit args last. `dst`/`src` for mutating
  operations.
- Config-gated no-op stubs are `static inline`.
- `kmalloc_obj()` family for allocations sized by a type. `BIT_U64()` and
  `GENMASK_U64()` for masks in `u64` fields.

Correctness:
- `WARN_ON` only for broken invariants. Valid inputs with a defined answer
  return the answer. Bad input from BPF gets an error report and -EINVAL.
- No casts that C promotion already covers.
- Library code marks concurrent accesses symmetrically: if mutating ops
  use `WRITE_ONCE()`, predicates use `READ_ONCE()`.
- Annotate (`rcu_dereference_check()` with the true condition) instead of
  adding locking that protects nothing.
- No aliased duplicate structs, no open-coded bit loops (use or add an
  iterator), no `volatile` (except BPF `const volatile` rodata).
- Match the primitive to the actual concurrency. Cpu-local state needs no
  atomics. If proving the design needs a paragraph of interleaving
  reasoning, the shape is probably wrong.
- Every state-machine state and transition earns its place.
- Before adding a write, trace later writes. Before removing one, trace
  later readers.
- Use the accessor when one exists. `unlikely()` on errors from kernel APIs
  expected to succeed.
- Lockless reads: bitops helpers first, then `READ_ONCE()`, then
  `data_race()` for an intentional racy read.

## 6. Verify the findings

Code reading proposes bugs. It doesn't confirm them. For every finding:

1. Run it through `kernel/false-positive-guide.md` (or `/kverify`).
2. Check it against the source yourself, in this order:
   - Read the actual function and about 50 lines around it. Don't trust
     the reviewer's quoted snippet.
   - Expand every macro on the path. A macro that discards an argument is
     the most common false positive.
   - List every caller. Check whether each one already establishes the
     missing precondition (holds the lock, checks for NULL, holds an RCU
     read section).
   - Confirm that the lock invariant the finding cites exists
     (`lockdep_assert_*()`) and that it is broken at the call site.
   - Check that the Kconfig combination is buildable.
3. Judge it against the tree with patches 1..N applied (step 4).
4. Label it: real, real but unreachable today (defer), suspect (needs an
   experiment), or false positive with a one-sentence reason.

Common false positives:
- A macro discards the argument the finding calls unguarded.
- Every caller already holds the precondition.
- A validation gate at attach or load time already rejects the flag
  combination.
- The Kconfig combination isn't buildable.
- The path can't run before SMP, the scheduler or RCU is up.
- BPF iterator slot semantics misread (the verifier initializes the slot
  regardless of the return value, and destroy runs).
- A benign monotonic-flag race under a `WARN_ON_ONCE()`. That needs at most
  `data_race()`.
- Hedge-word claims: "latent", "could become a bug if", "depends on link
  order". Defer them and don't chase them ahead of reachable bugs.
- Defensive re-init for a state nothing reads.
- BPF-side misuse or a contractually impossible caller. As long as the
  kernel doesn't break internally, it isn't a kernel bug.

When a finding needs a runtime check:
- Widen the window with delays (`udelay()`, `mdelay()`, `msleep()`, extra
  contention, `module_param` knobs gating the delay). Relaxing thresholds
  so a path runs more often is fine. Never fake state: no writes to
  scheduler-owned fields, no skipped checks, no forced branches. Such a
  repro tests a different code path.
- A repro is the oracle firing (oops, lockdep splat, WARN, KCSAN report,
  hung-task report) plus a trace of the claimed mechanism. A slow run or a
  timeout is not a hang.
- Useful configs: `CONFIG_KCSAN`, `CONFIG_PROVE_LOCKING`, `CONFIG_KASAN`,
  `CONFIG_DEBUG_OBJECTS`, `CONFIG_PREEMPT_RCU`, flipped as the bug needs.
- If the repro keeps failing, suspect the premise, not the harness. Reread
  the source for the gate or precondition before widening further.

Then deduplicate across reviewers. Set aside every interleaving that a
reviewer couldn't settle by reading, or that two reviewers disagree about.
Those go to the model.

## 7. Decide on the formal model

**What it is.** TLA+ describes a system as variables, an initial predicate
`Init` and a next-state relation `Next`. PlusCal is a C-like front end
translated into TLA+ inside the same file. Processes are the actors, and
labels mark atomicity: everything between two labels is one indivisible
step, and other processes interleave only at labels. TLC is an
explicit-state model checker. For fixed small constants it enumerates every
reachable state, checks invariants on each, and returns the shortest trace
to a violation.

TLC checks the model under sequential consistency (SC): each step is atomic
and immediately visible to all processes. It doesn't check the C, the
compiler or the hardware memory model. A clean run says the abstraction, as
written, has no reachable bad state for those constants. A violation is a
candidate bug until it is replayed on the real code. For review work, the
model is the mechanized version of the case table that a multi-step
concurrency argument needs.

**It triggers when** the batch adds or changes a protocol in which two or
more actors coordinate through shared state, and the correctness argument
spans more than one step of more than one actor. Actors are CPUs, tasks,
hardirq or softirq contexts, a BPF program against the kernel, or a
userspace sampler against the kernel. Typical shapes:
- enable or disable counting paired against the state the disable can see
- refcount handoff
- ownership or claim-flag queues
- state machines with transitions from more than one context
- a lockless single-word scheme justified by "A can't observe X because B
  checks Y first"
- rollover or generation schemes

It also triggers when a reviewer reports an interleaving it can't settle by
reading, when two reviewers disagree about one, or when the requester asks
for a model.

**It doesn't trigger for** pure refactors and moves, state touched only
inside one lock's critical sections (the lock makes it single-actor at the
model level), data-structure or arithmetic changes with no concurrent
transitions, or memory-ordering questions (release/acquire pairing, barrier
placement, "is this `READ_ONCE()` enough"), which go to herd7 (step 9).
Don't model anything whose state space is the whole scheduler: modeling
the whole dispatch path is the anti-pattern. The model is the protocol
slice.

**Either way, the report says so** in one line: `model: yes <protocol>` or
`model: no <reason>`. Never skip the decision silently.

Why this class: the kernel precedents all have this shape. Marinas's models
found a qspinlock liveness hole fixed by 59fb586b4a07 ("locking/qspinlock:
Remove unbounded cmpxchg() loop from locking slowpath") and 6512276d97b1
("locking/qspinlock: Bound spinning on pending->locked transition in
slowpath"), a ticket spin_trylock rollover bug, an ASID rollover bug, and a
KVM vGIC SGI loss. Lamport found a published DCAS deque bug in under ten
hours without understanding the algorithm, because low-level C translates
almost line by line.

## 8. Write, falsify and run the model

The main agent or one dedicated sub-agent writes the model after the review
round, from the code paths, not from the patch description.

### Method

1. **Pick the actors and the shared words.** One process per concurrent
   context. The shared state is the set of words the actors read or write
   in the protocol. Everything else is process-local or dropped. Every
   variable multiplies the state space, so a variable earns its place only
   when leaving it out hides an interleaving.
2. **Abstract the data.** Identities are model values
   (`CPUS = {p1, p2}`, `TASKS = {t1, t2, t3}`), never integers, so
   `SYMMETRY` can collapse permutations. Counters are bounded, with a
   `WrapInc` operator or a `CONSTRAINT` that stops exploration past the
   bound. A multi-field word is a record
   (`[locked |-> FALSE, pending |-> FALSE, tail |-> NoCPU]`) read or
   written as one value when the C does so atomically, and as separate
   fields when it doesn't. Per-cpu arrays are functions
   `[c \in CPUS |-> ...]`. A queue is a set when order doesn't matter and a
   sequence when it does. A pointer-linked structure is a `Heap` function
   over a small address set.
3. **Translate the code paths.** Follow the C control flow, not the
   description. Atomics are macros (`cmpxchg`, `xchg`, `atomic_inc`,
   `fetch_or`), one step each, because macros can't contain labels. A
   spinlock is `await ~l; l := TRUE` and `l := FALSE`. Interrupt enable
   state is a per-cpu flag. An interrupt is either a separate process that
   `await`s the flag, or an `either { call irq() } or { skip }` branch at
   every point where one can land. Nondeterministic choices (which task
   runs next, whether a trylock succeeds, whether the timer fires) are
   `either/or` or `with (x \in S)`. Name processes and steps after the
   code's own functions and paths, never nicknames.
4. **Place the labels.** A label at every access to a shared word and
   nowhere else. That is the coarsest grain with one shared access per
   step, and it keeps every SC interleaving the hardware can produce. Don't
   let the translator add labels (`-label`): its minimal labeling hides
   interleavings. Labels are the model's central claim and the first thing
   to check when reviewing a model.
5. **State the properties.** Always `TypeInv` (every variable in its value
   set; it catches translation slips). Then the patch's claim as a state
   predicate: mutual exclusion via `pc`, "count zero implies nobody points
   at it", "an enabled sched has an op", "at most one owner". An `assert`
   inside a step checks what the code assumes at that point. Lamport's
   history-variable trick: keep an abstract copy of the structure, update
   it in the same step as the real linearization point, and assert that the
   concrete result matches. Progress claims ("every waiter eventually
   proceeds") are `PROPERTIES` with `~>` on `fair` processes, checked
   separately and last.
6. **Falsify before trusting.** Remove the mechanism the patch relies on:
   comment out the lock, drop the check, or swap two steps. TLC must report
   a violation with a trace that reads like the bug the mechanism prevents.
   Then restore it. A knob constant (`LOCKED = TRUE`) makes the two runs one
   cfg edit apart. If TLC passes in a fraction of a second with a handful of
   states, the model is too small or the invariant too weak.
7. **Run exhaustively, small first.** Two actors, then three, with symmetry
   on identity sets and constraints on counters. A run should take minutes,
   not hours. Only for a progress claim, add liveness with fairness, drop
   `SYMMETRY` (TLC's liveness checking isn't sound with it), and expect
   orders of magnitude more time. If exhaustive is out of reach at the size
   that matters, `-simulate -depth N` samples random behaviors. It can find
   bugs but can't show their absence, and the report says "sampled".
8. **Map every trace to C.** `-difftrace` prints only what changes per
   step. For each step, name the C line and the context executing it. If a
   step has no C counterpart, or two words change together in the model but
   separately in the C (or the reverse), the model is wrong: fix it and
   rerun. Only a trace that replays on the code is a finding. Report it with
   the interleaving written out and labeled "model-derived, replayed on the
   code", not as an observed failure.
9. **Record and report.** Keep the `.tla` and `.cfg` files with the
   series' working notes, under version control but outside the patches,
   with a paragraph: what was modeled, the abstractions, the constants, the
   falsification run, distinct states, the result. The review report gets
   one line per model. Patch descriptions never mention the model. A cover
   letter's "Verified by" may carry one clause at an outside reader's level
   ("the enable/disable handshake was model checked for small CPU counts").

### Checklist before trusting a model result

- [ ] The trigger decision is in the review report: `model: yes <protocol>`
      or `model: no <reason>`.
- [ ] The model was written from the code paths, not the description. Every
      abstraction is listed next to it: what was dropped, what was merged
      into one step, which constants bound it.
- [ ] It was falsified first: the protective mechanism removed, and TLC
      reported the violation.
- [ ] The exhaustive run's constants, distinct-state count, depth and wall
      time are written down. `-simulate` runs are labeled as sampling.
- [ ] Every counterexample was mapped step by step onto C lines. A trace
      that needs an abstracted step is a model defect.
- [ ] The report states the SC assumption. Ordering claims go to herd7 or
      are marked UNKNOWN, never settled by TLC.
- [ ] Model and cfg are stored with the series' notes, TLC's metadir is
      outside the tree and deleted, and the translator's `.old` backups are
      deleted.

### Failure modes of AI-written models

Published measurements of LLM-written TLA+ are poor. A 2026 benchmark of 30
models found that about a quarter of generated specs parse and under a tenth
check correctly. Guard against these:
- **Weakening the spec to make TLC pass**: adding a constraint that rules
  out the race, declaring the interleaving acceptable, or coarsening labels
  until the race disappears. The only legitimate fix is to model the
  mechanism the code actually has. If the code has none, that's the
  finding.
- **Vacuous properties**: invariants true by construction, the end state as
  an invariant, a property that restates the implementation. The
  falsification run catches these, every time.
- **Wrong abstraction level**: treating model devices (`pc`, the history
  variable) as implementation state, or modeling timing (`sleep`) as a
  value instead of a nondeterministic step.
- **Syntax**: `=` for `==`, `!=` for `#`, TLA+ syntax inside the `.cfg`, two
  assignments to one variable in a step (use `||`), a label inside a macro
  or `with`. Iterate against the translator and SANY messages until clean.
  They are exact.
- **Semantics the translator hides**: read the generated TLA+ for the steps
  that matter: which variables each action changes, where `await` landed,
  what `UNCHANGED` covers.

### Starting template

This models a per-cpu two-word pair that a sampler snapshots. `LOCKED =
TRUE` must pass and `LOCKED = FALSE` must fail. With TLC 2.19: locked, 501
distinct states, depth 21, no error. Lockless, `SnapInv` was violated at
state 6, with the sampler reading the new cell and the old counter between
the writer's two stores. Copy it as the starting point for a new model. The
per-cpu writer and sampler loops, the lock macros, the knob constant, the
type invariant, the counter constraint and the symmetry set are the parts
every review model needs.

`pairsnap.tla`:
```
---------------------------- MODULE pairsnap --------------------------------
\* Review template: per-cpu writers advance a two-word pair (cell, cnt) in
\* lockstep; a sampler snapshots the pair of one cpu. SnapInv says the
\* snapshot is consistent. LOCKED = FALSE is the lockless variant TLC must
\* reject (the falsification run); LOCKED = TRUE protects the pair with a
\* per-cpu lock and must pass. Sequential consistency assumed throughout.
EXTENDS Naturals, FiniteSets, TLC

CONSTANTS CPUS,         \* model values, e.g. {p1, p2}
          RD,           \* model value naming the sampler process
          MAXCNT,       \* bound on the counters, keeps the state space finite
          LOCKED        \* TRUE: writer and sampler take the per-cpu lock

ASSUME /\ MAXCNT \in Nat \ {0}
       /\ LOCKED \in BOOLEAN

(* --algorithm pairsnap {
variables
        cell = [c \in CPUS |-> 0];
        cnt  = [c \in CPUS |-> 0];
        lock = [c \in CPUS |-> FALSE];
        snap = [cpu |-> 0, cell |-> 0, cnt |-> 0];

define {
        TypeInv == /\ cell \in [CPUS -> 0..MAXCNT]
                   /\ cnt \in [CPUS -> 0..MAXCNT]
                   /\ lock \in [CPUS -> BOOLEAN]
        \* the pair advances together, so a consistent snapshot has cell = cnt
        SnapInv == pc[RD] = "rd_check" => snap.cell = snap.cnt
        Constr  == \A c \in CPUS : cnt[c] < MAXCNT
        Perms   == Permutations(CPUS)
}

macro spin_lock(l)   { await ~l; l := TRUE; }
macro spin_unlock(l) { l := FALSE; }

fair process (writer \in CPUS)
{
w_loop: while (TRUE) {
                if (LOCKED) spin_lock(lock[self]);
w_cell:         cell[self] := cell[self] + 1;
w_cnt:          cnt[self] := cnt[self] + 1;
                if (LOCKED) spin_unlock(lock[self]);
        }
}

fair process (sampler = RD)
{
rd_loop: while (TRUE) {
                with (c \in CPUS) snap.cpu := c;
                if (LOCKED) spin_lock(lock[snap.cpu]);
rd_cell:        snap.cell := cell[snap.cpu];
rd_cnt:         snap.cnt := cnt[snap.cpu];
                if (LOCKED) spin_unlock(lock[snap.cpu]);
rd_check:       skip;
        }
}
} *)
\* BEGIN TRANSLATION
\* END TRANSLATION
=============================================================================
```

`pairsnap.cfg`. The falsification cfg, `pairsnap-lockless.cfg`, is the same
with `LOCKED = FALSE`:
```
SPECIFICATION Spec

CONSTANTS       CPUS = {p1, p2}
                RD = RD
                MAXCNT = 3
                LOCKED = TRUE

INVARIANTS      TypeInv
                SnapInv

CONSTRAINTS     Constr

SYMMETRY        Perms
```

Run, with `$SCRATCH` a scratch directory outside the tree:
```
pcal -nocfg pairsnap.tla && rm -f pairsnap.old
tlc -workers auto -metadir $SCRATCH/tlc/pairsnap -config pairsnap.cfg \
    pairsnap.tla
tlc -workers auto -metadir $SCRATCH/tlc/pairsnap-ll \
    -config pairsnap-lockless.cfg pairsnap.tla
rm -rf $SCRATCH/tlc/pairsnap $SCRATCH/tlc/pairsnap-ll
```

The result line states the constants, distinct states, depth, wall time and
the SC assumption, for example: "CPUS={p1,p2} MAXCNT=3: locked, 501 distinct
states, depth 21, no error; lockless, SnapInv violated at state 6. SC
assumed."

## 9. Memory ordering: herd7

A TLC pass says nothing about whether the C's accesses are ordered. Any
claim like "the reader can't see the new cell with the old counter", "this
release pairs with that acquire" or "this `smp_mb()` is needed" is a litmus
test. The kernel ships its memory model (LKMM) in `tools/memory-model`
(`linux-kernel.cat`, run by herd7), with worked tests in `litmus-tests/`
(`MP+pooncerelease+poacquireonce`, `SB+fencembonceonces`, the `LB+...`
tests, the lock variants) and the format in
`Documentation/litmus-tests.txt`. A test is a few lines of C per thread plus
an `exists` clause describing the bad outcome.

```
cd <linux>/tools/memory-model
herd7 -conf linux-kernel.cfg <path>/name.litmus
```

"Never" under `Observation` means the model forbids the bad outcome.
"Sometimes" or "Always" means the ordering argument is wrong. `klitmus7`
turns a test into a kernel module to run on hardware. Marinas's split from
the 2018 qspinlock thread is the rule: liveness and interleavings in a
simplified TLA+ model, ordering safety in herd.

The first gate stays the lockless rule from step 4: a multi-word lockless
scheme should usually become a lock. herd7 confirms an ordering claim that
survives that gate.

## 10. Report and follow-up

The report is proportional to the changes:
- material findings, each with severity, patch, location, trigger and
  resolution, model-derived ones labeled as such
- incremental verdicts ("valid at N, resolved by N+k") where they apply
- the `model:` line, with the result line when a model ran
- style findings in the `<patch> (rule) <quote> -> <fix>` form, or "clean"

Fix the issues within the already authorized scope without a new permission
step. Ask only for a scope or design decision that wasn't already made, or
for an action that needs separate approval.

For correction deltas, reuse the completed review context and assess the
delta with its affected callers and invariants. Reopen unchanged analysis
only when new evidence or substantial restructuring invalidates it.

## 11. Reference: PlusCal, TLC config, flags, output, sizing, running

### PlusCal (C syntax) skeleton

```
---- MODULE name ----
EXTENDS Naturals, Sequences, FiniteSets, TLC
CONSTANTS CPUS, NoCPU, MAXVAL      \* set in the .cfg; NoCPU is a model value
ASSUME MAXVAL \in Nat \ {0}

(* --algorithm name {
variables
        lock = FALSE;
        count = [c \in CPUS |-> 0];
        owner = NoCPU;

define {
        TypeInv == /\ lock \in BOOLEAN
                   /\ count \in [CPUS -> 0..MAXVAL]
                   /\ owner \in CPUS \cup {NoCPU}
        Excl == \A a, b \in CPUS : a # b => ~(pc[a] = "cs" /\ pc[b] = "cs")
        Perms == Permutations(CPUS)
}

macro spin_lock(l) { await ~l; l := TRUE; }
macro spin_unlock(l) { l := FALSE; }
macro cmpxchg(v, old, new, ret) { ret := v; if (v = old) v := new; }

procedure acquire()
        variable tmp;
{
a1:     spin_lock(lock);
        owner := self;
a2:     tmp := count[self] + 1;
        count[self] := tmp;
        return;
}

fair process (cpu \in CPUS)
{
loop:   while (TRUE) {
                call acquire();
cs:             either { skip; } or { count[self] := 0; };
                owner := NoCPU;
                spin_unlock(lock);
        }
}
} *)
\* BEGIN TRANSLATION
\* END TRANSLATION
====
```

**Statements**: `x := e;`, `a := 1 || b := 2` (one multi-assignment per
variable per step), `if (c) {...} else {...}`, `either {...} or {...}`,
`while (c) {...}`, `await c;`, `with (x \in S) {...}` or `with (x = e)`,
`skip;`, `assert e;`, `call p(args);`, `return;`, `goto lbl;`. `self` is the
process identity and `pc[p]` the label process p is at. A local variable `v`
of a process set is `v[p]` in the translation and in invariants. Invariants
over locals go below `\* END TRANSLATION`, where the locals are declared.
Procedures can't return values: pass them through a global indexed by
`self` (`ret[self] := ...`).

**Label rules** (enforced by the translator, PlusCal manual 3.7):
- The first statement of a process or procedure is labeled.
- Every `while` is labeled.
- A statement after `call`, `return` or `goto`, or after an `if` or
  `either` containing one of those or a label, is labeled.
- No labels inside a macro or a `with` body.
- A label must separate two assignments to the same variable. `||` assigns
  several components of one variable in one step.

**Expressions**: `/\ \/ ~ => <=>`, `= #`, `\in \notin \cup \cap \subseteq
\`, `{x \in S : p}`, `{e : x \in S}`, `\A x \in S : p`, `\E x \in S : p`,
`CHOOSE x \in S : p`, `IF p THEN a ELSE b`, `CASE p -> a [] q -> b`,
`LET d == e IN f`. Functions `[x \in S |-> e]`, `f[x]`, `DOMAIN f`,
`[f EXCEPT ![k] = v]` (TLA+ side only; in PlusCal write `f[k] := v`).
Records `[a |-> 1, b |-> 2]`, `r.a`, `[a: S, b: T]` (a set of records).
Tuples `<<a, b>>`, `t[1]`, `S \X T`. Sequences: `Append`, `Head`, `Tail`,
`Len`, `<<>>`, `\o`. `Cardinality(S)`. Strings (`"cs"`) serve as enum
values, and model values from the cfg serve as identities and `NULL`.

**Temporal**: `[]P` (P in every state, an invariant), `<>P` (eventually),
`P ~> Q` (every P state is followed by a Q state), `WF_vars(A)` and
`SF_vars(A)` (weak and strong fairness). `Spec == Init /\ [][Next]_vars`
allows stuttering, which is how a stalled CPU or a lost wakeup shows up.
Liveness needs fairness, or stuttering forever is legal and every liveness
property fails.

### TLC cfg

Same basename as the spec:
```
SPECIFICATION Spec
CONSTANTS       CPUS = {p1, p2}
                MAXVAL = 3
                LOCKED = TRUE
INVARIANTS      TypeInv Excl
PROPERTIES      LockAll          \* liveness; drop SYMMETRY when present
SYMMETRY        Perms
CONSTRAINTS     Constr
```
- `X = X` declares a model value, and `{p1, p2}` declares a set of them.
- `CHECK_DEADLOCK FALSE` only when a process legitimately blocks forever at
  the end. A spin loop is not a deadlock.
- When a procedure variable has no initial value, the translator emits
  `CONSTANT defaultInitValue`. Add `CONSTANT defaultInitValue =
  defaultInitValue` to the cfg.
- Typed model values (`p_1`, prefix `p_`) make TLC complain about
  comparisons between different kinds. Comparisons of untyped model values
  with anything else are silently false.

### TLC invocation and flags

```
pcal -nocfg name.tla && rm -f name.old       # translate, keep our cfg
TLC_JAVA_OPTS="-XX:+UseParallelGC -Xmx8g" \
tlc -workers auto -metadir $SCRATCH/tlc/name name.tla
tlc -workers auto -difftrace ... name.tla     # shorter traces
tlc -simulate -depth 200 ... name.tla         # random sampling, never a pass
```
- `-metadir` keeps TLC's `states/` scratch out of the tree.
- `-deadlock` disables deadlock checking.
- `-continue` keeps going after a safety violation.
- `-dump dot,colorize,actionlabels FILE` writes the state graph for
  GraphViz.
- `-coverage N` prints per-action counts every N minutes. Zero-count actions
  are dead code in the model.
- `-seed` and `-aril` fix the simulation seed.
- `-checkpoint` and `-recover` resume long runs.
- `-fpmem 0.5` gives half of the memory to the fingerprint set.

### Reading the output

- A pass ends with "Model checking completed. No error has been found."
  plus states generated, distinct states, depth and time. A pass with a few
  hundred distinct states on a concurrency model suggests the model is
  trivial.
- "Invariant X is violated." is followed by "The following behavior
  constitutes a counter-example:" and `State 1` ... `State n`. Each state
  is a conjunction of variable values, with `pc` showing where every
  process stands.
- "Deadlock reached." means no process can step.
- "Temporal properties were violated." names no property and gives a
  non-minimal trace.

### Sizing

>From the published precedents:
- qspinlock liveness: 2 threads under a minute, 3 threads hours, 4 days
- ASID allocator safety: 4 tasks under an hour, the full config two days
- DCAS deque safety bug: 3 processes and 4 cells in a few hours
  coarse-grained, 40 hours fine-grained
- a termination-detection spec: N=4 about 50 minutes on a desktop, N=6
  hopeless

Review models stay at 2 or 3 actors and in minutes. Anything larger is a
separate task with its own budget.

### Cleanup after every run

A TLC run leaves a metadir (fingerprint partitions, state-queue spill,
trace pages) that grows to tens or hundreds of GB on a large instance.
Delete each run's metadir as soon as its summary line is recorded: result,
distinct states, depth, time, and the last Progress line for an aborted
run. On a remote machine, also delete the run's log after copying the result
back. Keep only the model, the cfgs, a summary file and the report.

### Where and how to run

- Translate and syntax-check locally. Run every TLC instance, falsifications
  included, on a dedicated multi-core machine when one is available.
  Instance sizes are hard to predict, and a model judged small can grow
  with its revisions and load an interactive machine for many minutes.
- Queue the falsifications first (seconds each, and they gate everything
  else), then the exhaustive instances by expected size, then the bounded
  ones.
- On a remote machine, start each run detached (`setsid nohup ... &`) so it
  survives the ssh session, and copy each result line back into a local
  summary file.
- TLC is lock-bound past a few dozen workers: the state queue is behind one
  lock and the default fingerprint set is contended. On a multi-socket
  machine:
  - Set the cpufreq governor to performance. schedutil can leave the cores
    at low frequency under this lock-bound load.
  - Pin each instance to one NUMA node with
    `numactl --cpunodebind=N --membind=N` and size its memory to that node.
  - Use the off-heap fingerprint set
    (`-Dtlc2.tool.fp.FPSet.impl=tlc2.tool.fp.OffHeapDiskFPSet`), with
    `-XX:MaxDirectMemorySize` at about three quarters of the node's memory
    and the heap at the rest. When two instances share the machine, size
    the set with `-fpmem`.
  - Use about 64 workers per instance.
  - Run one instance per node in parallel, and start the next large one on
    a node as soon as it frees up.
- Measured on a two-node machine with 48 cores per node (distinct states
  per minute, matched depth):
  - Pinned with the off-heap set, throughput doubled from 16 to 64 workers
    and was flat from 64 to 96.
  - Spreading the same 64 workers across both nodes was about 25 percent
    slower than pinning them to one.
  - The default fingerprint set was about 15 percent slower than the
    off-heap set.
  - All 192 threads unpinned on the default set ran at 27 percent busy,
    slower than 32 threads on a single-socket workstation.
  - Two pinned instances, one per node, doubled the total throughput.
- With the default in-heap set, TLC spills the fingerprint set to disk once
  it outgrows the heap (on a 28 GB heap, past about 1.5G distinct states),
  and the run crawls. Move such runs to a machine sized for them.

## 12. Reference: kernel-tla precedents, alternatives, sources

### kernel-tla

`https://git.kernel.org/pub/scm/linux/kernel/git/cmarinas/kernel-tla.git`
(arm64 maintainer Catalin Marinas). Read these as templates:
- `ticketlock.tla` (smallest): the lock as a record `[owner, next]`,
  `WrapInc` for bounded counters, `either { call spin_lock() } or { await
  TRYLOCK; call spin_trylock() }`, `fair process`, `ExclInv` over `pc`, and
  `LockAll == \A p : pc[p] # "cs" ~> pc[p] = "cs"` as liveness.
- `qspinlock.tla`: a `cmpxchg` macro, the lock word as a record, per-cpu MCS
  nodes as `<<cpu, idx>>` tuples, `Permutations(CPUS)` symmetry, and nesting
  contexts (task, softirq, hardirq, NMI) as one process per level gated by a
  `ProcessEnabled(self)` guard that `check.sh` splices into every action.
  Its history found the two liveness fixes above, and a later commit splits
  `set_locked()` into its own step to expose a window.
- `ctxsw.tla`: `mm_users`/`mm_count` as record fields, `mmgrab`/`mmput`
  macros, a per-cpu `interrupts` flag, the scheduler as
  `with (n \in runqueue)`, idle tasks as per-cpu processes, `PreemptSpec` as
  the checked spec, and invariants of the "count zero implies no user"
  shape.
- `asidalloc.tla`: `spin_lock(l)` as `await ~l; l := TRUE`, the TLB as a set
  of records, an asynchronous unmap process, a `CONSTRAINT` on the
  generation counter, and `with (t \in TASKS)` for the next task.
- `check.sh`: `pcal -nocfg`, an awk pass splitting `vars` into global and
  local tuples, `tlc -workers $(nproc)`. The `README` has sizing notes.

### Alternatives considered

- **SPIN/Promela**: C-like and historically faster on small concurrent
  models (McKenney's perfbook uses it for QRCU and dyntick-idle). Same SC
  assumption, no kernel-tla style corpus.
- **CBMC**: checks real C with bounded loop unwinding and has TSO/PSO
  support. It verified Tree RCU from the 4.3 sources, but needs a harness
  per target and bounds.
- **Nidhugg**: a stateless model checker for C/pthreads under TSO, PSO and
  POWER, also used on Tree RCU.
- **TLC trace validation** (2024): TLC checks logged implementation traces
  against a spec. It closes the model-code gap for user-space systems. For
  kernel code, the equivalent is replaying a TLC trace against the source by
  hand (step 8, item 8).
- **Apalache** (symbolic, SMT-backed, bounded depth, needs type
  annotations, no fairness) and **TLAPS** (interactive proofs) exist but
  aren't needed for review work.

None of these changes the choice: PlusCal plus TLC for the interleaving
slice, herd7 for ordering.

### Sources

- Lamport, PlusCal manual (C syntax):
  https://lamport.azurewebsites.net/tla/c-manual.pdf
- Lamport, Current Versions of the TLA+ Tools (TLC options):
  https://lamport.azurewebsites.net/tla/current-tools.pdf
- Lamport, Checking a Multithreaded Algorithm with +CAL (2006):
  https://lamport.azurewebsites.net/pubs/dcas.pdf
- Marinas, Formal Methods for Kernel Hackers, LPC 2018:
  https://lpc.events/event/2/contributions/60/
- Marinas, kernel-tla:
  https://git.kernel.org/pub/scm/linux/kernel/git/cmarinas/kernel-tla.git
- 2018 qspinlock thread, the TLA+ model assumes SC:
  https://lkml.rescloud.iu.edu/1804.1/03635.html
- Konnov, Kuppe, Merz, TLA+ Trifecta (TLC, Apalache, TLAPS):
  https://arxiv.org/abs/2211.07216
- Demirbas, Thinking in TLA+ (2026):
  https://conf.tlapl.us/2026-etaps/demirbas-2026.pdf
- Wayne, learntla.com (concurrency, temporal logic and CLI chapters) and
  "AI is a gamechanger for TLA+ users" (2025):
  https://buttondown.com/hillelwayne/archive/ai-is-a-gamechanger-for-tla-users
- LLM TLA+ generation benchmark (Loyola, ICSOFT 2026):
  https://ai4fm.cs.luc.edu/papers/llm-tla-evaluation/
- Industrial TLA+ practice review (IFM 2024):
  https://arxiv.org/abs/2411.13722
- TLC trace validation: https://docs.tlapl.us/using:tlc:trace_validation
  and https://arxiv.org/abs/2404.16075
- TLA+ tools: https://github.com/tlaplus/tlaplus
- LKMM: `tools/memory-model/README` in the kernel tree. herdtools7:
  https://github.com/herd/herdtools7
- Review prompts: https://github.com/masoncl/review-prompts
