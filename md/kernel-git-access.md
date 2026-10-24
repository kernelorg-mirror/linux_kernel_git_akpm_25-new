# Kernel Git access: tested Work workflow

Test date: 2026-10-24. All conclusions below come from executed Git
operations and local Git history, not search results or cached web pages.

## Result

Direct HTTPS Git access worked in the Work execution environment
used for the 2026-10-24 test. This is not a standing claim about other
chats, Work sessions, or execution environments.
A full, non-shallow, unfiltered bare clone of akpm/mm completed from
Google. Fetching Linus master from kernel.org and a subsequent incremental
fetch from Google also completed successfully. Browser Gitiles access was
also tested, but is not needed for the Git workflow.

Session-scoped local repository used in that test:
`/workspace/scratch/91741514aa81/mm.git`

**For a new Work chat:** First check whether that repository exists and
is a valid complete Git repository. If absent, establish a new read-only
clone. The path and 3.32 GiB objects are NOT guaranteed to persist.
Do not treat the branch SHAs below as current until freshly fetched.

The initial Google pack contains 12,754,069 objects and occupies 3.32 GiB
including its index. The initial clone took roughly 15 minutes, chiefly
local indexing. This is an observation for this run, not a performance
promise. Temporary diagnostic transfers were time-limited or stopped;
none was used to calculate the final results.

## Pinned results

| Reference | SHA | Committer timestamp (original offset) |
| --- | --- | --- |
| mm-stable | 183895979c441e52dbd651b388553b09eaa35cfa | 2026-10-24T01:56:43-07:00 |
| mm-unstable | d10295141a98938a767234e73d45b954a69c9a2f | 2026-10-24T02:05:50-07:00 |
| torvalds/linux master | 5b0764a53235d3c77e1ed674e836e1b3fe1a4b1f | 2026-10-23T18:29:02-10:00 |

Linus's timestamp is 2026-10-23 21:29:02 PDT, or
2026-10-24 04:29:02 UTC. HEAD was verified to name refs/heads/master.
The mm-stable author date is 2026-10-17T05:09:27Z; its committer date
above is the appropriate timestamp for this branch-tip comparison.

Both the initial and final remote checks returned the same tips.
Google and public kernel.org akpm/mm agree on both MM branch SHAs.
These also match the user's October 24 checkpoints.

The exact authoritative SSH URL was tested:
`git@gitolite.kernel.org:pub/scm/linux/kernel/git/akpm/mm`
It failed with: `Could not resolve hostname gitolite.kernel.org:
Temporary failure in name resolution`. Therefore direct verification
against Gitolite itself was NOT achieved. Agreement with the public
kernel.org repository and the user's checkpoints is the available evidence;
it must not be described as a successful authenticated Gitolite check.
No credentials were requested or installed.

## Exact branch relationship

Executed against the fetched, non-shallow object database:

```sh
git --git-dir=mm.git rev-list --left-right --count \
  mm-stable...refs/remotes/linus/master
# 213  12447

git --git-dir=mm.git rev-list --count \
  refs/remotes/linus/master..mm-stable
# 213

git --git-dir=mm.git rev-list --count \
  mm-stable..refs/remotes/linus/master
# 12447
```

These are exact commit-identity/reachability counts, including merges.
They do not count patch-equivalent cherry-picks as identical commits.

## Mainline incorporation and currency

The newest commit on Linus's first-parent chain reachable from mm-stable:

- `ff47652a4b66c067c765a7ad464d930b5a9367cc`
- 2026-10-02T14:04:11-07:00
- Merge tag 'cifs-fixes-7.3-rc6' of https://git.manguebit.org/linux
- `git describe`: v7.3-rc5-337-gff47652a4b66

This was verified by intersecting the complete mm-stable ancestor set with
Linus's first-parent chain, selecting the first match when traversing from
Linus's tip. No later first-parent mainline commit is reachable from
mm-stable. Linus is 242 first-parent commits beyond this mainline base.

The first mm-stable first-parent commit above that base is:
`51216825099e36bf9d39de375749d8365556c5fc`, committed
2026-10-06T17:38:42-07:00, "mm: use a folio in the
softleaf_is_device_private path". There are 760 total commits, 753 on
first-parent traversal, above this base in mm-stable.

The later MM-side merge `fbd3c33ceddb79f48ef8b55245fa4288ea752bc5`,
2026-10-08T15:24:49-07:00, merges mm-hotfixes-stable. That branch has
the same October 2 mainline base; this is not a later mainline refresh.

The ordinary merge-base with current mainline is instead:
`2967f3ccdb5fae956f1b085370ec292bab5c7e25`, an MM patch committed
2026-10-12T21:29:59-07:00, "mm: shmem: assign a lock class to the
unused huge shrinklist". It is NOT on Linus's first-parent chain.

Linus incorporated that MM tip in:
`c5fd5e67c7812bc40cd897422c1e0d6dd9ed1e2e`, committed
2026-10-23T07:42:11-10:00 (10:42:11 PDT),
"Merge tag 'mm-stable-2026-10-19-21-33' of
 git://git.kernel.org/pub/scm/linux/kernel/git/akpm/mm".
Its second parent is exactly 2967f3ccdb5fae956f1b085370ec292bab5c7e25.
This is MM flowing into mainline, not mainline flowing into MM.

Assessment: mm-stable has current October 24 MM changes, but a broad
mainline base about 22 days old. It is not current with Linus's tree;
12,447 commits reachable from Linus are absent. That is a topology
observation, not evidence that this subsystem-branch policy is wrong.

Git commits identify the incorporated base, not the exact wall-clock
moment of a branch reset/rebase. Remote reflogs were not available.
Do not report October 2 as a proven date when the branch was synchronized.

## Reusable read-only workflow

Use mm-unstable for patch reviews unless Andrew specifies another base.
Pin the exact fetched SHA for each review; branch names can move.
Never change or push the remote repositories.

1. Check whether the local bare clone still exists. Work scratch storage
   is not a durable cross-session guarantee. If absent, clone again.
2. Test HTTPS Git directly; prefer Google. Compare MM refs with public
   kernel.org, and Gitolite only when authorized SSH access is available.
3. Fetch all advertised MM branches and tags; fetch Linus master into its
   separate remote-tracking ref. Do not substitute akpm/mm's `master` or
   `linus` branch for Linus's live repository.
4. Record retrieval time, remote URLs, exact SHAs, committer dates, and
   verification outcomes. Recheck refs after the fetch to detect movement.
5. Require complete ancestry for counts. Check shallow and partial-clone
   settings; verify connectivity. Report an inability to establish currency
   rather than assuming a stale checkpoint is current. Flag mirror lag
   exceeding 24 hours when that lag can actually be established.
6. Review source at the pinned SHA with git show/grep/log/blame. Trace
   callers, callees, inverse operations, error paths, ownership, locking,
   and object lifetimes. Use a detached disposable worktree if a build or
   runtime test is needed. Do not claim those tests unless executed.
7. Preserve review evidence and outcomes separately from the replaceable
   local repository. Refresh before the next review.

Initialization, when a clone is absent:

```sh
git clone --progress --bare \
  https://kernel.googlesource.com/pub/scm/linux/kernel/git/akpm/mm mm.git
git --git-dir=mm.git config remote.origin.fetch '+refs/heads/*:refs/heads/*'
git --git-dir=mm.git config remote.origin.pushurl /dev/null
git --git-dir=mm.git config push.default nothing
git --git-dir=mm.git config remote.linus.url \
  https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
git --git-dir=mm.git config remote.linus.fetch \
  '+refs/heads/master:refs/remotes/linus/master'
git --git-dir=mm.git config remote.linus.pushurl /dev/null
```

These local remote settings have been established in this session's clone.
The push settings are accident-prevention measures, not a security boundary.
The workflow itself never invokes push.

Refresh and inspect:

```sh
git --git-dir=mm.git fetch --no-auto-maintenance origin
git --git-dir=mm.git fetch --no-tags --no-auto-maintenance linus
git --git-dir=mm.git rev-parse --is-shallow-repository
git --git-dir=mm.git show -s --format='%H %aI %cI %s' \
  mm-stable mm-unstable refs/remotes/linus/master
git --git-dir=mm.git show mm-unstable:mm/memcontrol.c
git --git-dir=mm.git grep -n high_work_func mm-unstable -- mm include
git --git-dir=mm.git log -p mm-unstable -- mm/memcontrol.c
```

For review evidence, replace mm-unstable with the recorded immutable SHA.
The commands shown here illustrate repeatable local inspection; they do
not assert that a patch review, compilation, or VM test was performed.

## Tested capability and limitations

- Full clone: completed; all advertised heads and tags fetched by bare clone.
- Non-shallow: verified false for --is-shallow-repository.
- Non-partial: no promisor/partial-clone settings in the full clone.
- Mainline fetch: completed from kernel.org.
- Incremental Google fetch: completed.
- Local source retrieval, symbol search, path history, and tree enumeration:
  completed at mm-unstable, including high_work_func() in mm/memcontrol.c;
  96,062 tree entries enumerated.
- Exact commit counts: cross-checked with symmetric and separate ranges.
- Cloud browser: Google Gitiles loaded successfully; not used for counts.
- Gitolite SSH: DNS failure; authentication and Git access untested beyond it.
- Alternative git:// transport: unnecessary and not tested in this run.
- Builds, VM tests, and native patch-review tools: not tested by this task.
- Future-session connectivity and retention: not guaranteed by this test.

Connectivity verification completed successfully (exit 0):
`git fsck --connectivity-only --no-dangling`, with empty diagnostic output.
This checks connectivity; it is not a claim to have run full content-hash
verification via `git fsck --full`.


Final advertised-ref audit: 17 heads and 4241 tags; 0 missing or mismatched locally.
Audit timestamp: 2026-10-24T19:35:22.497117+00:00

## Next Work-chat handoff (read-only)

Treat this Markdown as an executed historical connectivity report and a
reusable Git procedure, not as current repository state. At startup:

1. Check for a valid, non-shallow, connected existing clone. If absent,
   use direct HTTPS Git to create one; Google is preferred for MM.
2. Fetch Google MM refs and Linus's actual live `master` from kernel.org.
   Independently compare Google MM tips with public kernel.org; try
   authenticated Gitolite only when authorized and reachable.
3. Capture command results, retrieval date, full SHAs, committer dates,
   remote URL and exact preimages; do not infer authenticated sync.
4. Default to `mm-unstable` for new patch reviews unless the submitted
   patch or user specifies another base. Use immutable SHA throughout.
5. Invoke `akpm-review-gate.py new` against the prevalidated full SHA
   before source analysis; perform all policy checks, then run `check`
   before any acceptance recommendation. Missing evidence is HOLD.
6. Source and Git operations are read-only. Do not create/switch signed
   tags, push, or alter publication branches without a separate request.

The user should not have to run local tooling. Work is expected to carry
out these checks using its own cloud execution environment. If actual
connectivity or tools fail, report exactly what was and wasn't run.
