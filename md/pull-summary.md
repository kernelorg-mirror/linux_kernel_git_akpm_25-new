# Preparing kernel pull-request summaries

This file covers two separate deliverables. For a new Work chat, use
the complete repository described in `kernel-git-access.md` to ground
branch ranges and commit counts. Verify current refs rather than reuse
historical SHAs; don't require Andrew to run local commands.

The two deliverables are:

1. The short summary in a `[GIT PULL] hotfixes for ...` email to Linus.
2. The patch-series summary in a signed `git tag -s` pull-request tag,
   immediately after `Summary of patch series in this merge:`.

Do not confuse their formats. This is a writing and verification procedure;
it does not create tags, modify repositories, or send mail.

## Common rules

- Describe what the submitted commits actually do. Do not infer results,
  fixes, user-visible effects, or performance changes from a branch name.
- Use a recent, personally written pull request as the style reference.
  Prefer Andrew's direct, informal kernel-maintainer voice. A little
  folksiness is fine; avoid canned praise and LLM-sounding prose.
- Describe the important correctness, performance, and userspace effects
  where the commit messages and source evidence support them. Preserve
  meaningful technical terms and qualifications.
- Keep summaries concise. Do not reproduce individual changelogs.
- Use 7-bit ASCII and wrap prose for email at no more than 75 columns.

### Serious failures and triggerability

Pay particular attention to memory or data corruption, crashes, panics,
BUG/WARN_ON-class failures, hung tasks, deadlocks, and serious regressions.

For every such issue, determine during analysis whether the failure can be
triggered by unprivileged userspace, requires privilege or capabilities,
or needs some other special setup. Surface that distinction to Andrew for
severity triage; an unprivileged-triggerable failure generally deserves
more urgent attention than a privileged-only failure.

Do **not** automatically disclose the privilege or exploitability details
in the public pull summary. Normally describe the problem and its impact
without advertising who can trigger it. Consider including such details
only when already public and specifically useful. For a private note,
prefer a concise term such as `root-only` to wordy qualifications.

## A. Hotfix pull-request email summary

This section applies to `[GIT PULL] hotfixes for ...` emails to Linus.

### Counts and terminology

- Obtain exact counts from the actual hotfix batch: total fixes, number
  marked `cc:stable`, and number concerning MM.
- Use the literal term `cc:stable`, never abbreviate it to `cc`.
- A suitable format, with illustrative counts only, is:

      14 hotfixes.  10 are cc:stable.  11 are for MM.

### Content and emphasis

- Group genuinely related fixes, such as DAMON or hugetlb changes.
  Do not describe a batch as "all singletons" if meaningful groups exist.
- Call out the most serious correctness failures and their consequences.
- Summarize the batch rather than giving every commit its own changelog.
- State effects directly, for example:

      One fixes an arm64 contpte bug where DAMON can write past the
      end of a page-table page, resulting in memory corruption and
      possible crashes.

      One fixes an mremap() address calculation bug which can panic
      x86-64.

- Do not add gratuitous comments about privilege, such as "isn't directly
  triggerable by ordinary unprivileged userspace".

### Hotfix delivery check

Verify the three counts, the `cc:stable` spelling, the presence of
meaningful groups, and accurate descriptions of serious failures. Keep
the public email brief and apply the triggerability rule above.

## B. Signed-tag patch-series summary

This section prepares **only the text after** the literal heading
`Summary of patch series in this merge:` in a signed pull-request tag.
Do not repeat the heading, pull boilerplate, review statistics, or the
per-author shortlog in this output.

### Inputs and source range

Obtain:

1. The branch to be pulled and the chosen upstream/base reference.
2. A recent, personally written pull request as a style reference.
3. A commit log including the subject, author, message, and per-file
   additions and deletions, from the appropriate local checkout:

       git log --no-merges --numstat --format=full \
           BASE..BRANCH > pull-series.txt

Substitute the actual refs and verify `BASE..BRANCH` contains precisely
the commits intended for the pull. Do not guess the range.

### Identify eligible series

1. Split the log at each `commit <sha>` header and retain the subject,
   author, body, and associated `--numstat` records.
2. Find series introductions such as `Patch series "..."`, often with
   `vN` or `This patch (of N):`. Use the original quoted series title.
3. Read the series overview and all related subjects. Associate companion
   commits using the cover letter, ordering, lore links, and stated
   patch count. Never group commits solely by author, directory, or topic.
4. Include a series only when **at least two of its commits** occur in
   the selected range. Do not turn standalone patches into series.
5. If the range includes only part of a larger series, describe only
   the included commits; check the title and attribution accordingly.
6. Put the series author in parentheses after the title. Use the
   cover-letter author or maintainer, even if individual commits have
   different authors.

### Calculate size and order

For each eligible series, sum additions plus deletions across every file
in every included commit:

    series_size = sum(lines_added + lines_removed)

- Count both additions and deletions positively, including changes in
  documentation and tests. Use only commits in `BASE..BRANCH`.
- Sort series bullets by descending size; break ties with stable order
  (for example, first appearance in the log).
- Do not print the sizes: they determine ordering only.
- `--numstat` uses `-` for binary changes. Flag them for review; do not
  invent a numeric size.
- A rename-only change can have zero changed lines. Use Git's reported
  count rather than substituting file size.

### Write the tag text

Follow the prior pull's layout:

    - "original patch series title" (Series Author):

      Fix the underlying problem, describing what changed and why it
      matters. Mention userspace or performance effects when supported.

- Start each explanatory paragraph with an imperative verb: `Fix`,
  `Make`, `Remove`, `Give`, `Teach`, `Separate`, `Avoid`, etc.
- Do not begin with padding such as "This series aims to" or
  "The patches introduce".
- Ordinarily use one three- or four-line explanatory paragraph per
  series; allow a second short paragraph for a genuinely complex series.
- Explain the engineering result and why the previous behavior was
  undesirable. Preserve important interfaces and qualifications.
- Avoid item-by-item narration of a long patch series.

### Signed-tag delivery check

1. Every bullet covers two or more commits actually in the range.
2. Every eligible series is present once, with no double counting.
3. Titles and author attributions match the original series.
4. Each description matches the commits included in this pull.
5. Bullet order agrees with the summed additions plus deletions.
6. Paragraphs begin with an imperative and are mostly three to four
   lines, with exceptions only when useful.
7. The output omits the heading and boilerplate, contains only ASCII,
   and is hard-wrapped at no more than 75 columns.
8. Compare the tone and layout with the supplied example pull.
9. Save the standalone tag body, e.g. `pull-tag-summary.txt`, ready
   for insertion into `git tag -s`.

## Provenance and scope

Generate summaries from the supplied commit log and example pull request.
When Work Git access is available, obtain and verify the appropriate
complete commit log there; a saved Work scratch path is not guaranteed
in a new session. Keep the hotfix email and tag series formats separate.
If required data (range, counts, or changelogs) is unavailable, identify
the gap; do not invent values or claim that a series was checked. This
file records reusable policy, not historical intermediate decisions.
