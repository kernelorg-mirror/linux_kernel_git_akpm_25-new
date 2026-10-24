Continue my AKPM Linux kernel review and pull-request work in Work mode.

The attached files are authoritative:

- akpm-patch-review-workflow.md: mandatory review methodology and gates.
- review-activity.md: active and historical review findings through R-036.
- kernel-git-access.md: tested direct Git access and dated checkpoints.
- pull-sumary.md: hotfix pull-email and signed-tag series summary policy.
- akpm-review-gate.py: executable evidence gate v2; actually run it.

Use Work's own execution environment; do not ask me to run local tools.
First check whether the prior Work bare clone exists; its old scratch path
is NOT guaranteed to persist. If absent, establish direct HTTPS Git again.
Prefer Google's akpm/mm mirror; compare MM refs with public kernel.org.
The authenticated Gitolite SSH check previously failed DNS resolution;
never claim it succeeded. Fetch Linus's live master separately. Record
full SHA, commit time, retrieval time and source/preimage verification.
Default to mm-unstable for reviews, unless I specify another base.

October 24 historical checkpoints, not necessarily current tips:
mm-unstable d10295141a98938a767234e73d45b954a69c9a2f
mm-stable   183895979c441e52dbd651b388553b09eaa35cfa
Linus       5b0764a53235d3c77e1ed674e836e1b3fe1a4b1f

For every new review, run akpm-review-gate.py new with a verified full
source SHA BEFORE inspecting source, and preserve its original manifest.
Perform independent first-principles analysis; full applicable Sashiko
stage and specialist coverage; current pinned Tejun and Chris Mason
reviews; whole-tree callers/build consumers; architecture/configuration,
locking, error/rollback and lifetime paths; an adversarial second pass;
and evidence-based reconciliation of confirmed and dismissed findings.
Run akpm-review-gate.py check before any acceptance recommendation.
Missing or failed mandatory evidence means HOLD. Do not claim native
Sashiko, compilers, testing, formal checks or external reviewers unless
actually executed. Do not turn a passing receipt audit into proof of
correctness. Always identify userspace-visible effects and whether
serious bugs require privilege for internal severity assessment.

Latest numbered review is R-036 (HOLD); R-035 and R-034 also HOLD.
The ledger and Library detailed reports contain their unresolved issues.
Do not treat earlier source-favorable findings as gate clearance.

For drafted email and patch prose use my direct voice and hard-wrap at
75 columns. Provide verified download links to the full canonical
review workflow and activity Markdown whenever updated. Preserve their
existing review history. Store detailed patch reports in Library as
specified, with verified readback. Do not edit kernel code, push Git
refs, sign tags or send mail unless I explicitly request it.

Read the attached files, verify actual Git/tool availability, then
continue from my next patch or pull-summary request.
