# Preparing a pull-request series summary

Purpose: generate the text which follows
`Summary of patch series in this merge:` in the signed `git tag -s`
message for a kernel pull request.  This is a procedure for preparing
and checking that text, not for creating the tag or sending the pull.

## Inputs

1. The branch being pulled, and the chosen upstream/base reference at the
   point the pull will be prepared.
2. A recent, personally written pull request as a style reference.
3. The commit log with per-file added/deleted counts, produced from the
   appropriate local Git checkout with:

       git log --no-merges --numstat --format=full \
           BASE..BRANCH > pull-series.txt

   Replace `BASE` and `BRANCH` with the actual refs; check that the range
   matches the commits intended for the pull.


## Identify the patch series

- Split the log at each `commit <sha>` header.  Retain the subject, author,
  commit body, and each following numstat record.
- Look for the first commit in a series with a changelog line such as
  `Patch series "..."`, often followed by `vN`, and `This patch (of N):`.
  Treat the quoted original series title as the series name.  Read the
  series overview and the individual commit subjects to establish what
  the series actually does.
- Associate the succeeding companion commits with that series, using
  the cover-letter wording, commit ordering, related lore links, and
  stated patch count.  Do not group unrelated commits simply because
  they share an author, directory, or topic.
- Include only series represented by at least two commits in the range.
  Do not manufacture a multi-patch series from a standalone patch.
  If only part of a larger series is present, describe only the commits
  actually in this pull and check the attribution/title carefully.
- Use the series author's name in parentheses after the quoted series
  title, as in the previous pull.  A series can contain other authors'
  patches; use the cover-letter author/maintainer for the attribution.

## Size and ordering

- Sum the numeric added and removed counts in `git log --numstat` for
  every file of every commit belonging to a series:

       series_size = sum(lines_added + lines_removed)

- Use only the commits in the chosen `BASE..BRANCH` range.  Both additions and
  deletions count positively, including tests and documentation.
- Sort the series bullets in descending `series_size` order.  For equal
  sizes, retain a stable ordering (for example, first appearance in the
  log).  The size numbers are for sorting, not for printing in bullets.
- `--numstat` uses `-` for binary-file changes.  Flag these for review;
  they have no numeric line count and should not be silently converted
  into a fabricated size.
- Rename-only changes may have zero line changes; count what Git reports
  and do not substitute file size for changed lines.

## Write the tag text

- Output only the body *after* `Summary of patch series in this merge:`.
  Do not repeat that heading, the pull-request boilerplate, review
  statistics, or the per-author shortlog.
- Follow the previous pull's layout:

       - "original patch series title" (Series Author):

         Imperative verb first.  Explain what changed and why it matters.
         Mention user-visible effects, correctness or performance when
         supported by the commit messages.

- Begin the explanatory text with an imperative verb: `Fix`, `Make`,
  `Remove`, `Give`, `Teach`, `Separate`, `Avoid`, etc.  Avoid introductory
  padding such as "This series aims to" or "The patches introduce".
- Use the user's informal kernel-maintainer voice.  A little folksy
  phrasing is welcome if it sounds natural; avoid breathless praise,
  canned summaries, and LLM-sounding abstractions.
- Normally use one explanatory paragraph per series, with each paragraph
  wrapping to about three or four lines.  Large or complex series may
  have a second short paragraph when that adds something substantive.
- State the salient engineering outcome, why the existing behavior was
  undesirable, and any concrete userspace or performance effect that
  the commits support.  Do not invent results, implied fixes, or claims
  absent from the submitted changelogs.
- Keep the series heading and author, and preserve technical terms,
  interfaces, and important qualifications.  Do not summarize every
  individual patch in a long series.
- Plain old 7-bit ASCII only: no em dashes, curly quotes, smart apostrophes,
  nonbreaking spaces, or other typographical substitutions.  Wrap the
  finished text for email (78 columns is a reasonable default).

## Checks before delivery

1. Every bullet represents two or more actual commits in the range.
2. No eligible multi-patch series has been omitted or double-counted.
3. Each bullet is correctly attributed and describes its actual patches.
4. Bullet ordering agrees with the summed numstat additions + deletions.
5. Explanatory text is imperative-first, mostly one 3-4-line paragraph,
   occasionally two for substantial series.
6. The file is ASCII-only and email-wrapped; the heading itself is absent.
7. Compare the result with the example pull for tone and presentation.
8. Keep the result in a standalone file, e.g.
   `pull-tag-summary.txt`, ready to paste into `git tag -s`.

## Scope and provenance

Generate the prose from the supplied commit log and the supplied example
pull request, not from assumptions about the branch name or project.
This procedure does not create tags, modify repositories, or send mail.
It records the reusable workflow, not an archived implementation script
or an exact transcript of intermediate editorial decisions.
