# Hotfix pull-request summary policy

This file documents how to write the short summary for `[GIT PULL] hotfixes
for ...` emails to Linus.

## Counts and terminology

Use exact counts for the batch, for example:

    14 hotfixes.  10 are cc:stable.  11 are for MM.

Use the literal term `cc:stable`.  Do not abbreviate this to `cc`.

## What to summarize

Group related fixes when there is a real theme, such as DAMON or hugetlb.
Do not call a batch "all singletons" when there are meaningful clusters.

Call out the most important correctness failures, especially:

- memory corruption;
- kernel crashes or panics;
- BUG/WARN_ON-class failures;
- hung tasks or deadlocks;
- data corruption;
- serious regressions.

Keep the summary concise.  The purpose is to tell Linus what is in the pull,
not to restate every commit changelog.

## Privilege and exploitability

When reviewing a crash, panic, BUG, WARN_ON, memory corruption, or similar
serious kernel failure, always determine internally whether it can be
triggered by unprivileged userspace or requires privilege, capabilities, or
some other special setup.

This distinction is important for triage:

- privileged-only failures still need fixing, but are less concerning;
- unprivileged-triggerable failures deserve much more urgent attention.

Do not automatically include these exploitability details in the public pull
request summary.  In particular, avoid unnecessarily advertising whether a
bug is unprivileged-triggerable, root-only, or otherwise security-sensitive.

The public summary should normally describe the bug and its impact without
describing who can trigger it.

If exploitability information is already public and there is a clear reason
to include it, consider it case by case rather than by default.

## Style

Prefer direct descriptions such as:

    One fixes an arm64 contpte bug where DAMON can write past the end of a
    page-table page, resulting in memory corruption and possible crashes.

or:

    One fixes an mremap() address calculation bug which can panic x86-64.

Avoid wordy phrases such as:

    isn't directly triggerable by ordinary unprivileged userspace

If privilege information genuinely belongs in a non-public discussion,
prefer concise wording such as `root-only`.

## Working rule

During analysis, always surface privilege/triggerability information to
Andrew because it affects severity.

In the public email, omit that information unless there is a specific reason
to disclose it.
