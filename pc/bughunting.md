# Linux kernel bug-hunting runbook

This is the authoritative, reusable procedure for kernel bug reproduction,
debugging and patch preparation in future chats. Prefer direct evidence and
small, tested steps to speculation. Keep answers and commands concise.
All drafted email, patch and review prose must be hard-wrapped at a
maximum of 75 columns. This is a strict limit, not a guideline.

## Machines and workspace

- `hp2`: primary development/patch-management machine. Patches may be applied
  there using `apatch`; do not assume `hp2` and `ts` have the same source state.
- `ts`: powerful local-network build/VM host, Ubuntu 24.04, AMD Ryzen
  Threadripper PRO 3995WX (64 cores). Build and test kernels here.
- On `ts`, kernel source and **in-tree build**: `/usr/src/25`.
- On `ts`, syzkaller: `/home/akpm/kernel-testing/src/syzkaller`.
- On `ts`, VM image/SSH key: `~/kernel-testing/images/trixie.img` and
  `~/kernel-testing/images/trixie.id_rsa`.
- On `ts`, reproducers/logs: `~/kernel-testing/repro`, `~/kernel-testing/logs`.
- Do not modify or push GitHub repositories. Do not modify existing production
  code without explicit permission. A request for a test patch authorizes
  creating the patch file, not applying it to the user's tree.
- Tools are already installed; do not waste time repeating installation steps.

## Prepare a debugging kernel on ts

Preserve an existing `.config` if needed: `cp .config .config.saved`.
Check the working tree, branch, and patch status before resetting anything.
From `/usr/src/25`, start with `make x86_64_defconfig` only when a fresh
configuration is intended, then enable these debugging and guest options:

```sh
cd /usr/src/25
make x86_64_defconfig
scripts/config \
  -e KASAN -e KASAN_GENERIC -e KASAN_INLINE \
  -e DEBUG_KERNEL -e FRAME_POINTER \
  -d DEBUG_INFO_NONE -e DEBUG_INFO -e DEBUG_INFO_DWARF5 \
  -e IKCONFIG -e IKCONFIG_PROC \
  -e TRACING -e FTRACE -e FUNCTION_TRACER -e FUNCTION_GRAPH_TRACER \
  -e KPROBES -e KPROBE_EVENTS -e DEBUG_FS \
  -e SECURITYFS -e CONFIGFS_FS -e BINFMT_MISC \
  -e EXT4_FS -e BLK_DEV_LOOP \
  -e DEVTMPFS -e DEVTMPFS_MOUNT \
  -e VIRTIO_PCI -e VIRTIO_BLK
make olddefconfig
make -j64
```

Not every option is necessarily user-settable on every revision; verify
`.config` after `olddefconfig`. `CONFIG_SECURITYFS` and `CONFIG_CONFIGFS_FS`
are needed for Debian guest mounts; omitting them previously caused emergency
mode. `CONFIG_FUNCTION_TRACER` is needed for
`/sys/kernel/tracing/available_filter_functions`; `CONFIG_KPROBE_EVENTS`
permits function probes even without the function tracer. Use KASAN generic on
x86-64; DWARF5 is important for source locations and type offsets.

Check build artifacts:

```sh
readelf -S vmlinux | grep '\.debug_info'
gdb -q -batch vmlinux -ex 'ptype /o struct iov_iter'
ls -lh arch/x86/boot/bzImage vmlinux
```

Keep `vmlinux` from the **exact** running `bzImage` build. A changed kernel
requires restarting QEMU; rebuilding source alone does not change the guest.

## Boot test kernel under QEMU/KVM on ts

From `~/kernel-testing`:

```sh
qemu-system-x86_64 \
  -machine q35,accel=kvm -cpu host -m 8G -smp 4 \
  -kernel /usr/src/25/arch/x86/boot/bzImage \
  -append 'console=ttyS0 root=/dev/sda rw nokaslr net.ifnames=0' \
  -drive file=images/trixie.img,format=raw,if=ide,snapshot=on \
  -netdev user,id=net0,hostfwd=tcp:127.0.0.1:10021-:22 \
  -device e1000,netdev=net0 -nographic
```

Keep QEMU running in its own terminal. Connect from a second terminal on `ts`:

```sh
ssh -i ~/kernel-testing/images/trixie.id_rsa -p 10021 \
  root@127.0.0.1
```

Validate `uname -a`, `systemctl --failed`, `zgrep CONFIG_KASAN
/proc/config.gz`. For GDB, add QEMU `-s` (and optionally `-S`) with `nokaslr`,
then use `gdb /usr/src/25/vmlinux`, `target remote localhost:1234`.
Restrict the GDB port to trusted local access.

**Critical:** `snapshot=on` discards *all guest filesystem changes* at VM
shutdown, including copied reproducers, installed guest packages, generated
logs and scripts. Keep authoritative copies on `ts`; recopy after every reboot:

```sh
scp -i ~/kernel-testing/images/trixie.id_rsa -P 10021 \
  ~/kernel-testing/repro/ext4-bug root@127.0.0.1:/root/
```

The command above uses the historical ext4 reproducer as an example; substitute
the current reproducer path. Exit QEMU with Ctrl-A, X if needed.

## Syzkaller and reproducer workflow

Syzkaller checkout is already on `ts`. If source changes, check `go.mod` and
Go's selected toolchain. Build, when needed:

```sh
cd ~/kernel-testing/src/syzkaller
make prog2c execprog executor
```

Expected binaries: `bin/syz-prog2c`, `bin/linux_amd64/syz-execprog`,
`bin/linux_amd64/syz-executor`. Copy the latter two and the `.syz` input to
the VM to execute syzkaller's program directly. The generated C reproducer
is particularly useful for tracing syscall return values:

```sh
cd ~/kernel-testing/repro
~/kernel-testing/src/syzkaller/bin/syz-prog2c \
  -prog=ext4-bug.syz -sandbox=none -threaded=false \
  -procs=1 -repeat=1 -trace > ext4-bug.c
gcc -O0 -g -static -pthread -o ext4-bug ext4-bug.c
```

`-repeat` takes an **integer** (`1` means once), not `false`. The converter
requires `clang-format` on the host. Generated tracing may print only
`errno`; instrument `res` if actual return values are needed. In the guest:

```sh
cd /root
rm -rf -- syz-tmp
./ext4-bug 2>&1 | tee ext4-bug.log
```

The generated C creates `syz-tmp` and may silently exit if it already exists;
remove it before every run. Its parent can return exit status zero even if
its sandbox child fails. Use `strace -f -o trace.log ./ext4-bug` to diagnose
startup failures. Do not infer that an unreported KASAN fault cannot exist;
check complete kernel logs and syscall return values.

## Kernel-side investigation

1. Reproduce on the exact reported base kernel first; record `git status`,
   `git log`, `uname`, kernel config, full console and KASAN report. Identify
   any already-applied patch before interpreting negative results.
2. Verify all relevant syscalls ran and compare real `write()`/`writev()`
   returns, not just `errno=0`.
3. Use DWARF (`gdb -batch vmlinux -ex 'info line *function+OFFSET'`) and
   `ptype /o` for exact type-member offsets. Source-line attribution can point
   to an inlined macro or KASAN reporting instruction; examine nearby code.
4. On guest, `findmnt -t tracefs,debugfs`; tracefs normally mounts at
   `/sys/kernel/tracing`. `CONFIG_TRACING=y` alone does not imply function
   tracing; kprobes can work without `CONFIG_FUNCTION_TRACER`.
5. Kprobe example on x86-64 for
   `copy_folio_from_iter_atomic(folio, offset, bytes, iter)`:

```sh
cd /sys/kernel/tracing
echo 0 > tracing_on
echo 'p:copy_iter copy_folio_from_iter_atomic offset=%si:u64 bytes=%dx:u64 iter=%cx:x64 type=+0(%cx):u8 iov_offset=+8(%cx):u64 iov=+16(%cx):x64 count=+24(%cx):u64 nr_segs=+32(%cx):u64' >> kprobe_events
echo 1 > events/kprobes/copy_iter/enable
echo > trace
echo 1 > tracing_on
# Run reproducer in another shell, then:
echo 0 > tracing_on
grep copy_iter trace
echo 0 > events/kprobes/copy_iter/enable
echo '-:copy_iter' >> kprobe_events
```

Those offsets are for the demonstrated x86-64 `struct iov_iter`; always
confirm against the build under test. Kprobe return probes can capture
`ret=$retval:s64`, but argument registers are not reliably retained on
function return. Avoid registering an already-existing event name.
6. Trace upstream from the faulting copy toward iterator mutation and error
   handling. Preserve distinctions between observed execution, code-implied
   consequences and unverified hypotheses. In particular, a patch that avoids
   a triggering path may **hide** a separate cleanup bug.
7. A/B-test unpatched, independently patched and combined variants when
   useful. Compare syscall return values and full KASAN reports.

Historical diagnostic example (not a generic assumption): an ext4 test's
nine iovecs totaled 1025 bytes. The unpatched direct-I/O extraction rejected
one vector but left `nr_segs=7` and `count=1025` with only 1015 bytes
remaining; buffered fallback read nonexistent `iov[9].iov_len`. Independent
alignment and rollback patches each prevented the specific reproduction.

## Regression testing and reporting

For deterministic bugs, run >=100 reproducer iterations, removing `syz-tmp`
between runs and asserting the exact expected return value. Examine `dmesg`
for KASAN, warnings and oopses. Use disposable VM filesystems and appropriate
fio (buffered and O_DIRECT) or xfstests workloads. Test independent fixes
separately when there are competing explanations. Do not claim that a test ran
unless its output was actually observed; distinguish source audits, synthetic
patch checks, and real kernel boots/tests. Revisit concurrent patch series
that touch the same error-handling paths (e.g., block atomic-write changes).

## **Mandatory patch production discipline**

Patch correctness is a recurring failure mode. **Do not hand-compose hunk
headers or fabricate diffs**, especially after rewriting a proposed patch.

- Build the patch from **exact base source bytes** whenever possible, in a
  disposable worktree or local copied source tree. Use `git diff`,
  `git format-patch` or `diff -u`; never manually guess `@@` line counts,
  context lines or file indexes. Do not change the user's working tree or
  repository unless specifically authorized.
- Inspect the exact current target source before generating the patch;
  identify upstream revision and whether a preceding version is applied.
  Do not assert a synthetic reconstruction equals the user's tree.
- Validate every emitted file as *delivered*: `git apply --check` (or
  `patch --dry-run` for the applicable patch format) against a known clean
  base, plus `git diff --check`/`git apply --check --whitespace=error` where
  appropriate. If any subsequent edit touches the patch, **rerun validation**.
- Verify both syntactic parsing and actual applicability; these are distinct.
  For `apatch`, ensure its expected metadata/sidecar convention is satisfied
  instead of assuming plain `git apply` compatibility.
- If the actual target checkout isn't accessible, say validation was against
  a specified public source or reconstruction, **not** the user's checkout.
  Never claim success without executing the check.
- Verify hunk contexts and filenames and show a concise diffstat. Keep
  patches 7-bit ASCII and hard-wrap all changelog prose at 75 columns
  maximum.
- The local `hp2` patch queue may store `patches/<name>.patch` together
  with the editable `txt/<name>.txt` changelog, `pc/<name>.pc` metadata
  and `series`/`applied-patches`. Verify the actual destination format
  and keep those representations consistent. In particular, `apatch` can
  expect the `txt/` companion; do not treat successful `git apply --check`
  as sufficient evidence that `apatch` will accept the result.
- Preserve exactly one standalone `---` separator and all genuine test
  notes beneath it when refreshing; never let tooling silently duplicate
  separators, move metadata below the separator, or drop notes.
- Never silently replace a file with a different implementation. Preserve
  testing provenance and note any untested revision.

**Stable download filenames:** The user requires the **same exact filename**
for every revision of an artifact. Do not add `-v2`, `-upstream`, dates,
parenthesized copy numbers or other suffixes. For this example, use
`bio-iov-iter-rollback.patch` for *every* revision. Overwrite the generated
artifact at the same output path and verify that exact file exists **in the
current session** before linking it. Do not invent sandbox download links.

## Changelog, attribution, recipient checks

- Lead with **userspace-visible effects** of the bug: e.g. a short write
  (1015 instead of 1025), error code, corrupted data, hang or crash. Explain
  the precise mechanism and what the patch changes. Avoid exaggerated claims.
- Find and verify the introducing `Fixes:` commit using git history/blame.
  Include `Reported-by:` for the actual reporter and `Closes:` with the exact
  original public bug-report URL, **both verified**, never guessed.
- For the ext4 KASAN report, reporter was **Haocheng Yu** (email shown in
  his report: `l1za0.sec@gmail.com`). Its `Closes:` URL must be recovered
  from the real report or mailing-list archive before inclusion. Do not invent
  that URL.
- In addition to `scripts/get_maintainer.pl`, inspect `git blame` around
  every modified function and nearby error-handling paths, `git log -p` and
  recent related series. Include relevant authors/reviewers even if not in
  `get_maintainer` output. For this case, **Daehyeon Ko and Tal Zussman**
  should have been considered for Cc because their contemporaneous changes
  intersect the issue. Verify addresses from headers/commits; don't invent.
- Preferred changelog layout: `From:`, `Subject:`, `Date:`, then a
  blank line, rationale and userspace-visible impact, a single blank
  line and properly ordered trailers, followed by one standalone `---`
  with temporary testing notes and the diffstat/diff. Plain 7-bit ASCII;
  hard-wrap all changelog prose at 75 columns maximum.
- Trailer order: `Link:`/`Fixes:` before any existing human signoff chain;
  then `Reported-by:`, `Closes:`, review/test acknowledgements,
  named human assistance, `Assisted-by: LLM`, and finally individual
  `Cc:` recipients. Keep `Cc: stable` last if warranted. Do not invent
  a `Signed-off-by:` or add one on the user's behalf. Preserve authentic
  existing signoffs and review tags; never infer review from prose.
- Do not Cc mailing lists *in the stored patch changelog*; lists used
  when emailing a submission are a separate decision. Check `.mailmap`
  when canonicalizing identities; use local `pc/people` only as
  supplementary information where available. Inspect `git blame`,
  related commits and nearby code for recent relevant contributors,
  not only `get_maintainer.pl` output. Avoid duplicate/misplaced trailers.
- Use a verified, normally 12-character abbreviated hash in `Fixes:`;
  ensure it identifies the intended commit, not merely a similar
  change. Check original bug reports and public mail threads for
  exact `Reported-by:`, `Closes:` and related `Link:` metadata.
- Put brief **actual testing notes below the `---` separator**, rather than
  burying them in the permanent changelog. Check how the local patch scripts
  process cover text and trailers.
- Explicitly check interactions with active patch series, particularly
  changes to rejected-bio cleanup, and say what was and wasn't runtime tested.

## Relevant maintainer workflow distinctions

`hp2` uses a maintained patch queue, not merely standalone Git commits.
Patches can be revised repeatedly as discussions, regression tests and
dependencies change. Use the current queue position and source baseline;
a patch that applies cleanly in isolation may conflict after earlier
series patches. Prefer source edits and a refreshed machine-generated diff
over manually repairing hunk headers. Never force through a reject
without understanding the changed context; preserve the existing patch
name when refreshing.

When preparing mail or handling patches from a series, preserve the
original author, the correct version and explicit acknowledgements from
the relevant revision. Replies to a cover letter can apply to the
whole series; patch-specific review belongs only to that patch. Do not
silently carry trailers from older revisions. For the current bug-hunting
scope, consult the original mailing-list thread and its replies rather
than copying reviewers or provenance by guesswork.

Keep the distinction between a *fix tested in a guest VM*, a *patch
accepted into the local queue*, a *patch committed to an MM Git branch*,
and a *patch sent or merged upstream*. None implies the next.

## Fresh-chat handoff

Attach this `bughunting.md` and the latest reproducer/patch/report or relevant
source snippets. The new chat should immediately recall `hp2` vs `ts`, kernel
location `/usr/src/25`, QEMU/SSH commands, `snapshot=on` effects, debugging
configuration, test standards, reviewer/attribution discipline, and immutable
artifact filenames. Ask only for missing evidence, never repeat already
answered setup questions. Avoid a new tool-installation tour.
