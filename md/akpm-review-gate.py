#!/usr/bin/env python3
"""AKPM patch-review evidence gate (v4.1), executed inside ChatGPT.

No separate runner or local installation is required. The assistant must invoke
'new' before analyzing a patch and 'check' before writing the recommendation.

This checks *evidence receipts*, not whether the reviewer's reasoning is true,
whether searches were exhaustive, or whether the model obeyed the invocation
rule. It never authorizes 'take' or a Reviewed-by tag. An unresolved mandatory
requirement always results in HOLD. Never manufacture retroactive receipts.

Commands: new, inspect, run, report, hunk, section, external, resolve-retry,
check, status. Retry resolutions are separate, explicit, hash-bound records;
they never remove receipts or change a preflight manifest.
Run --help for an individual command's arguments.
"""
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import shlex
import subprocess
import sys

VERSION = 4
TOOL_VERSION = "4.1"  # Retains the immutable v4 plan/schema.
WORKFLOW = pathlib.Path(__file__).resolve().with_name("akpm-patch-review-workflow.md")

# Evidence types are deliberately NOT interchangeable. A receipt for a source
# analysis cannot substitute for a compile; a successful 'true' cannot satisfy
# a repository-wide search. These are *minimums*, not comprehensive coverage.
BASE = {
    "base_and_preimage": ("source", "preimage-verify"),
    "independent_source_pass": ("analysis",),
    "sashiko_stages": ("analysis",),
    "tejun_method": ("analysis",),
    "chris_method": ("analysis",),
    "all_hunks": ("hunks",),
    "all_callers": ("whole-tree-search", "analysis"),
    "cross_tree_consumers": ("whole-tree-search", "build-graph", "analysis"),
    "config_and_arch": ("analysis",),
    "lifecycle_and_errors": ("analysis",),
    "negative_verification": ("analysis",),
    "similar_bug_search": ("whole-tree-search", "analysis"),
    "guard_audit": ("analysis",),
    "userspace_effects": ("analysis",),
    "adversarial_second_pass": ("adversarial",),
    "test_and_build_scope": ("build-or-test", "analysis"),
    "emailable_verdict": ("analysis",),
    "stable_and_integration": ("analysis",),
    "standing_rule_inventory": ("sections",),
    "report_and_ledger": ("analysis",),
}
CONDITIONAL = {
    "shared_header_abi": ("whole-tree-search", "abi-lp64", "abi-ilp32", "analysis"),
    "external_consumer_build": ("consumer-build",),
    "parallel_tree": ("integration-search", "analysis"),
    "async_lifetime": ("analysis",),
    "test_matrix": ("build-or-test", "analysis"),
}
# A section cannot claim completion by citing an unrelated passing gate.
SECTION_GATES = (
    "base_and_preimage", "independent_source_pass", "tejun_method",
    "chris_method", "sashiko_stages", "cross_tree_consumers",
    "base_and_preimage", "independent_source_pass", "negative_verification",
    "guard_audit", "all_callers", "adversarial_second_pass",
    "report_and_ledger", "similar_bug_search", "independent_source_pass",
    "userspace_effects", "stable_and_integration", "emailable_verdict",
    "test_and_build_scope", "emailable_verdict", "report_and_ledger",
    "report_and_ledger", "report_and_ledger", "report_and_ledger",
)
VALID_SCOPES = {"local", "subsystem", "whole-tree", "cross-subsystem", "LP64", "ILP32", "integration"}
CMD_PURPOSES = {"whole-tree-search", "build-graph", "preimage-verify", "build-or-test", "abi-lp64", "abi-ilp32", "consumer-build", "integration-search"}
SEARCH_COMMANDS = {"git", "rg", "grep", "find"}
BUILD_COMMANDS = {"make", "gmake", "ninja", "gcc", "clang", "cc", "pytest", "meson", "cmake"}
REVIEW_SECTIONS = (
    "Default AKPM source tree", "Execution order", "Tejun upstream", "Chris Mason",
    "Sashiko coverage", "Cross-tree shared-interface", "Source integrity",
    "Architectural and historical", "Separate bug proof", "Added-guard",
    "Mandatory impact-coverage", "Mandatory adversarial", "Standing-rule compliance",
    "Similar-bug search", "Independent pass", "User-visible impact",
    "Stable-backport eligibility", "Other changelog", "Modeling and verification",
    "Reporting and email", "Immediate discovery", "Routine review delivery",
    "Artifact delivery", "Review activity",
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":")).encode()


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def load(path):
    return json.loads(pathlib.Path(path).read_text())


def save(path, obj):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".pending")
    temp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    temp.replace(path)


def classify_v2(raw):
    s = raw.decode("utf-8", "replace")
    files, hunks, changes = [], [], []
    path = None
    in_hunk = False
    for line in s.splitlines():
        hit = re.match(r"diff --git a/(.*?) b/(.*?)$", line)
        if hit:
            path = hit.group(2)
            files.append(path)
            in_hunk = False
        elif line.startswith("@@ ") and path:
            hunks.append({"id": f"H{len(hunks)+1:03d}", "file": path, "header": line})
            in_hunk = True
        elif in_hunk and line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
            changes.append(line)
    if not files or not hunks:
        raise ValueError("no parseable unified-diff files/hunks")
    changed = "\n".join(changes)
    shared = any(p.endswith((".h", ".mk")) or "/lib/" in p or p.startswith(("include/", "lib/", "scripts/")) for p in files)
    # A changed function signature/typedef is relevant even if only a C file
    # is edited. Conservative false positives hold; false negatives lose bugs.
    abi = bool(re.search(r"\b(typedef|int64_t|uint64_t|s64|u64|long long|atoll|atol|size_t|PRId64)\b", changed))
    async_life = bool(re.search(r"\b(work_struct|queue_work|schedule_work|call_rcu|css_put|css_tryget|cancel_work|kfree_rcu|timer_list|irq_work)\b", changed))
    tests = any("selftests" in p or p.startswith("tools/testing/") for p in files)
    # Detect renamed or changed signature declarations. A coarse heuristic,
    # used for audit prompts; reviewers must add any omitted symbols.
    symbols = set()
    declaration = re.compile(
        r"^[+-]\s*(?:(?:static|inline|extern|const|unsigned|signed)\s+)*"
        r"(?:long\s+long|long|int|s64|u64|size_t|ssize_t|bool|void|char|"
        r"struct\s+\w+)\s+\**([a-zA-Z_]\w*)\s*\(")
    for line in changes:
        m = declaration.match(line)
        if m:
            symbols.add(m.group(1))
    return {"files": files, "hunks": hunks, "shared": shared, "abi": abi, "async": async_life, "tests": tests, "symbols": sorted(symbols)}


IDENTIFIER = re.compile(r"^[A-Za-z_]\w*$")
C_WORDS = {"if", "for", "while", "switch", "return", "sizeof", "typeof",
           "__typeof__", "_Alignof", "__alignof__", "__attribute__",
           "__attribute", "__section", "__aligned", "__printf", "__scanf",
           "asm", "__asm__", "void", "int", "long", "short", "char",
           "struct", "union", "enum", "typedef", "static", "inline",
           "extern", "const", "unsigned", "signed", "volatile",
           "restrict", "case", "default", "do", "else", "break",
           "continue", "goto", "_Generic", "_Static_assert"}
HUNK_HEADER = re.compile(
    r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?: (.*))?$")


def c_code(text):
    """Blank comments, literals and directives without moving line numbers."""
    def blank(match):
        return re.sub(r"[^\n]", " ", match.group(0))
    text = re.sub(r'/\*[\s\S]*?\*/|//[^\n]*|"(?:\\[\s\S]|[^"\\])*"'
                  r"|'(?:\\[\s\S]|[^'\\])*'", blank, text)
    lines, continuation = [], False
    for line in text.splitlines(keepends=True):
        directive = continuation or line.lstrip().startswith("#")
        continuation = directive and line.rstrip("\r\n").endswith("\\")
        lines.append(re.sub(r"[^\n]", " ", line) if directive else line)
    return "".join(lines)


def c_blocks(text):
    """Conservative C definition inventory, not a preprocessor or C parser.

    Keep the complete signature for explicit supplements when the automatic
    name heuristic cannot recognize a declaration. Missing coverage holds.
    """
    code = c_code(text)
    depth, parens, boundary, active = 0, 0, 0, None
    blocks = []
    for pos, char in enumerate(code):
        if depth == 0:
            if char == "(":
                parens += 1
            elif char == ")":
                parens -= 1
            elif char == ";" and parens == 0:
                boundary = pos + 1
            elif char == "{":
                signature = code[boundary:pos]
                candidates, nesting = [], 0
                for match in re.finditer(r"[A-Za-z_]\w*|[()]", signature):
                    token = match.group(0)
                    if token == "(":
                        nesting += 1
                    elif token == ")":
                        nesting -= 1
                    elif (nesting == 0 and token not in C_WORDS and
                          re.match(r"\s*\(", signature[match.end():])):
                        candidates.append(token)
                # '=' denotes a global initializer, not a function body.
                if "(" in signature and "=" not in signature:
                    first = boundary + len(signature) - len(signature.lstrip())
                    active = {"name": candidates[-1] if candidates else None,
                              "signature": signature,
                              "start": code.count("\n", 0, first) + 1,
                              "body": code.count("\n", 0, pos) + 1}
                depth = 1
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                if active:
                    active["end"] = code.count("\n", 0, pos) + 1
                    blocks.append(active)
                active, boundary, parens = None, pos + 1, 0
    return blocks


def diff_hunks(raw):
    """Read actual hunk bodies; mail trailers and header hints are not code."""
    parsed, path, current = [], None, None
    old_left = new_left = 0
    for line in raw.decode("utf-8").splitlines():
        if line.startswith("diff --git "):
            if old_left or new_left:
                raise ValueError("truncated diff hunk")
            match = re.fullmatch(r"diff --git a/(.*?) b/(.*?)", line)
            if not match:
                raise ValueError("unsupported quoted diff path")
            path, current = match.group(2), None
            rel = pathlib.PurePosixPath(path)
            if rel.is_absolute() or ".." in rel.parts:
                raise ValueError("diff path escapes source tree")
        elif line.startswith("@@ "):
            if old_left or new_left:
                raise ValueError("truncated diff hunk")
            match = HUNK_HEADER.fullmatch(line)
            if not match or not path:
                raise ValueError("invalid diff hunk header")
            old_left = int(match[2]) if match[2] is not None else 1
            new_left = int(match[4]) if match[4] is not None else 1
            current = {"id": f"H{len(parsed)+1:03d}", "file": path,
                       "old_start": int(match[1]), "old_count": old_left,
                       "new_count": new_left, "old": [], "new": [],
                       "changed": [], "hint": match[5] or ""}
            parsed.append(current)
        elif current and (old_left or new_left):
            if line.startswith("\\ No newline at end of file"):
                continue
            if not line or line[0] not in " +-":
                raise ValueError("invalid diff hunk body")
            if line[0] in " -":
                current["old"].append(line[1:])
                old_left -= 1
            if line[0] in " +":
                current["new"].append(line[1:])
                new_left -= 1
            if line[0] in "+-":
                current["changed"].append(line[1:])
            if min(old_left, new_left) < 0:
                raise ValueError("hunk body exceeds declared line count")
    if old_left or new_left:
        raise ValueError("truncated diff hunk")
    return parsed


def git_text(repo, *args):
    cp = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                        check=False)
    if cp.returncode:
        raise ValueError("pinned source unavailable: " + cp.stderr.decode(errors="replace").strip())
    # Preserve source bytes on the UTF-8 path; unsupported encodings fail
    # closed rather than silently replacing characters in evidence hashes.
    return cp.stdout.decode("utf-8")


def classify(raw, repo, source_ref, supplements=()):
    if not re.fullmatch(r"[0-9a-f]{40}", source_ref or ""):
        raise ValueError("source revision must be a full 40-character SHA")
    if git_text(repo, "rev-parse", "--verify", source_ref + "^{commit}").strip() != source_ref:
        raise ValueError("source revision is not the pinned commit")
    cl = classify_v2(raw)
    parsed = diff_hunks(raw)
    declared = {}
    for item in supplements:
        hid, sep, name = item.partition(":")
        if (not sep or not IDENTIFIER.fullmatch(name) or name in C_WORDS or
                hid not in {h["id"] for h in parsed}):
            raise ValueError("--symbol must identify a real hunk as H001:function_name")
        declared.setdefault(hid, set()).add(name)
    symbols, consumers, evidence, sources = set(), set(), {}, {}
    for path in cl["files"]:
        hunks = [h for h in parsed if h["file"] == path]
        entry = git_text(repo, "ls-tree", source_ref, "--", path).strip()
        if entry:
            original = git_text(repo, "show", source_ref + ":" + path)
        elif all(h["old_count"] == 0 and h["old_start"] == 0 for h in hunks):
            original = ""
        else:
            raise ValueError("changed file absent from pinned source: " + path)
        sources[path] = {"sha256": digest(original.encode()), "tree_entry": entry}
        old_lines, post, cursor = original.splitlines(), [], 0
        for h in hunks:
            old = h["old"]
            start = max(0, h["old_start"] - (1 if old else 0))
            if old_lines[start:start + len(old)] != old:
                matches = [i for i in range(len(old_lines) - len(old) + 1)
                           if old_lines[i:i + len(old)] == old]
                if len(matches) != 1:
                    raise ValueError("preimage missing or ambiguous for " + h["id"])
                start = matches[0]
            if start < cursor or start > len(old_lines):
                raise ValueError("overlapping/out-of-order hunk " + h["id"])
            post.extend(old_lines[cursor:start])
            h["old_range"] = (start + 1, start + max(len(old), 1))
            h["new_range"] = (len(post) + 1, len(post) + max(len(h["new"]), 1))
            post.extend(h["new"])
            cursor = start + len(old)
        post.extend(old_lines[cursor:])
        old_blocks, new_blocks = c_blocks(original), c_blocks("\n".join(post))
        for h in hunks:
            touched = []
            for side, blocks in (("old", old_blocks), ("new", new_blocks)):
                start, end = h[side + "_range"]
                touched.extend({**b, "side": side} for b in blocks
                               if b["start"] <= end and b["end"] >= start)
            found = {b["name"] for b in touched if b["name"]}
            # Explicit supplements must occur in the verified hunk code or
            # an overlapping definition signature, never elsewhere in a file.
            binding = c_code("\n".join(h["old"] + h["new"]))
            binding += "\n" + "\n".join(b["signature"] for b in touched)
            for name in declared.get(h["id"], set()):
                if not re.search(r"\b" + re.escape(name) + r"\b", binding):
                    raise ValueError("supplemental symbol not bound to " + h["id"] + ": " + name)
                found.add(name)
            changed = c_code("\n".join(h["changed"]))
            consumers.update(n for n in re.findall(r"\b([A-Za-z_]\w*)\s*\(", changed)
                             if n not in C_WORDS)
            evidence[h["id"]] = {"symbols": sorted(found), "header_hint": h["hint"],
                                  "old_range": list(h["old_range"]), "new_range": list(h["new_range"]),
                                  "supplements": sorted(declared.get(h["id"], set())),
                                  "definitions": [{k: b[k] for k in ("name", "start", "body", "end", "side")}
                                                  for b in touched]}
            symbols.update(found)
    cl.update(symbols=sorted(symbols), consumer_symbols=sorted(consumers | symbols),
              symbol_evidence=evidence, source_files=sources,
              unresolved_hunks=[hid for hid, item in evidence.items() if not item["symbols"]])
    return cl


def expected_specs(cl, compilation_policy="required"):
    items = dict(BASE)
    # Parallel tree always applies. We must inspect base selection for each patch.
    items["parallel_tree"] = CONDITIONAL["parallel_tree"]
    if cl["shared"] or cl["abi"]:
        items["shared_header_abi"] = CONDITIONAL["shared_header_abi"]
        items["external_consumer_build"] = CONDITIONAL["external_consumer_build"]
    if cl["async"]:
        items["async_lifetime"] = CONDITIONAL["async_lifetime"]
    if cl["tests"]:
        items["test_matrix"] = CONDITIONAL["test_matrix"]
    if compilation_policy == "delegated" and "shared_header_abi" in items:
        # Compilation-only checks are delegated by explicit user policy.
        # Source/ABI analysis, searches and behavioral tests remain required.
        items["shared_header_abi"] = ("whole-tree-search", "analysis")
        items["external_consumer_build"] = ("analysis",)
    return items


def section_plan(wf_text):
    headers = [line[3:].strip() for line in wf_text.splitlines() if line.startswith("## ")]
    selected = []
    for prefix in REVIEW_SECTIONS:
        matching = [h for h in headers if h.startswith(prefix)]
        if not matching:
            raise ValueError("workflow section missing: " + prefix)
        selected.append(matching[0])
    return {f"S{i:02d}": {"heading": h, "status": "UNRESOLVED", "reason": "", "proof_gate": ""}
            for i, h in enumerate(selected, 1)}


def plan_data(patch, workflow, review_id, source_ref, schema=VERSION,
              repo=None, supplements=(), compilation_policy="required"):
    if compilation_policy not in {"required", "delegated"}:
        raise ValueError("unknown compilation policy")
    if schema < 4 and compilation_policy != "required":
        raise ValueError("historical manifests retain original compilation policy")
    if compilation_policy == "delegated":
        policy = workflow.read_text()
        if not all(part in policy for part in (
                "compilation checks are handled by\nothers.",
                "Do not run kernel, object, consumer, cross-architecture or full\nbuilds",
                "Retain source-level caller, type, ABI, configuration and build-graph\nanalysis.")):
            raise ValueError("delegated compilation requires explicit AKPM workflow override")
    raw = patch.read_bytes()
    cl = (classify_v2(raw) if schema == 2 else
          classify(raw, repo, source_ref, supplements))
    specs = expected_specs(cl, compilation_policy)
    secs = section_plan(workflow.read_text())
    plan = {"schema": schema, "patch_path": str(patch.resolve()), "patch_sha256": digest(raw),
            "workflow_path": str(workflow.resolve()), "workflow_sha256": digest(workflow.read_bytes()),
            "review_id": review_id, "source_ref": source_ref,
            "classification": cl, "requirements": {x: list(y) for x, y in specs.items()},
            "section_headings": {k: v["heading"] for k, v in secs.items()}}
    if schema >= 3:
        plan.update(source_repo=str(pathlib.Path(repo).resolve()),
                    supplemental_symbols=sorted(set(supplements)))
    if schema >= 4:
        plan["compilation_policy"] = compilation_policy
    return plan


def init(args):
    p = pathlib.Path(args.patch).resolve()
    w = pathlib.Path(args.workflow).resolve()
    manifest = pathlib.Path(args.manifest)
    if manifest.exists():
        raise SystemExit("HOLD: manifest already exists; refusing to overwrite preflight")
    if not args.review_id.strip():
        raise SystemExit("review ID required")
    try:
        plan = plan_data(p, w, args.review_id, args.source_ref,
                         repo=args.repo, supplements=args.symbol,
                         compilation_policy=args.compilation_policy)
    except (ValueError, OSError) as exc:
        raise SystemExit("HOLD: " + str(exc))
    o = {"plan": plan, "plan_sha256": digest(canonical(plan)), "created_utc": now(),
         "checks": {gate: [] for gate in plan["requirements"]},
         "sections": section_plan(w.read_text()), "hunks": {h["id"]: None for h in plan["classification"]["hunks"]},
         "unresolved": [], "decision": None}
    save(manifest, o)
    print(f"CREATED {manifest} required_gates={len(o['checks'])} "
          f"hunks={len(o['hunks'])} workflow_sections={len(o['sections'])} HOLD")
    if plan["classification"]["shared"] or plan["classification"]["abi"]:
        if args.compilation_policy == "delegated":
            print("Triggered: whole-tree reverse dependencies and source ABI coverage; "
                  "compilation delegated by explicit user policy")
        else:
            print("Triggered: whole-tree reverse dependencies, LP64+ILP32, external consumer build")
    if plan["classification"]["unresolved_hunks"]:
        print("HOLD: unresolved symbol inventory for",
              ", ".join(plan["classification"]["unresolved_hunks"]),
              "(use source-bound --symbol H001:name in a separate preflight)")


def valid_manifest(m, require_existing=True):
    errors = []
    p = m.get("plan", {})
    if p.get("schema") not in (2, 3, VERSION):
        return ["unknown gate manifest schema (v2, v3 or v4 required)"]
    if digest(canonical(p)) != m.get("plan_sha256"):
        errors.append("preflight plan digest changed")
    patch = pathlib.Path(p.get("patch_path", ""))
    wf = pathlib.Path(p.get("workflow_path", ""))
    if not patch.is_file() or not wf.is_file():
        errors.append("patch/workflow snapshot missing")
        return errors
    if digest(patch.read_bytes()) != p.get("patch_sha256"):
        errors.append("patch changed after preflight")
    if digest(wf.read_bytes()) != p.get("workflow_sha256"):
        errors.append("workflow changed after preflight; create a fresh review")
    try:
        expected = plan_data(patch, wf, p.get("review_id"), p.get("source_ref"),
                             schema=p["schema"], repo=p.get("source_repo"),
                             supplements=p.get("supplemental_symbols", ()),
                             compilation_policy=p.get("compilation_policy", "required"))
    except (ValueError, OSError, TypeError) as exc:
        return errors + ["cannot revalidate pinned preflight: " + str(exc)]
    if p != expected:
        errors.append("preflight requirements, source, hunks or sections altered")
    if not re.fullmatch(r"[0-9a-f]{40}", p.get("source_ref") or ""):
        errors.append("source revision not pinned to a full 40-character SHA during preflight")
    if set(m.get("checks", {})) != set(p.get("requirements", {})):
        errors.append("gate inventory altered")
    if set(m.get("hunks", {})) != {h["id"] for h in expected["classification"]["hunks"]}:
        errors.append("hunk inventory altered")
    if set(m.get("sections", {})) != set(expected["section_headings"]):
        errors.append("standing-rule section inventory altered")
    for sid, item in m.get("sections", {}).items():
        if item.get("heading") != expected["section_headings"].get(sid):
            errors.append(f"{sid}: section identity altered")
    return errors


def get(args):
    m = load(args.manifest)
    issues = valid_manifest(m)
    if issues:
        raise SystemExit("HOLD: " + "; ".join(issues))
    if m["plan"]["schema"] != VERSION:
        raise SystemExit("HOLD: historical v2/v3 manifest is read-only in v4; "
                         "preserve it and create a separate v4 preflight")
    return m


def put(args, m):
    save(args.manifest, m)


def receipt_file(path):
    f = pathlib.Path(path).resolve()
    if not f.is_file():
        raise SystemExit("HOLD: evidence file not found: " + str(f))
    return {"path": str(f), "sha256": digest(f.read_bytes()), "size": f.stat().st_size}


def inspect(args):
    m = get(args)
    gate = args.gate
    if gate not in m["checks"]:
        raise SystemExit("HOLD: unknown/conditional gate: " + gate)
    repo = pathlib.Path(args.repo).resolve()
    rel = pathlib.Path(args.path)
    if rel.is_absolute() or ".." in rel.parts:
        raise SystemExit("HOLD: --path must be repository-relative")
    src = (repo / rel).resolve()
    if not src.is_file() or not src.is_relative_to(repo):
        raise SystemExit("HOLD: cited source missing/outside tree")
    lines = src.read_text(errors="replace").splitlines()
    if args.line < 1 or args.line > len(lines) or len(args.note.strip()) < 45:
        raise SystemExit("HOLD: line outside file or inadequate source reasoning")
    rec = {"kind": "source", "file": receipt_file(src), "relative": str(rel), "line": args.line,
           "line_text": lines[args.line-1], "note": args.note.strip(), "recorded_utc": now()}
    m["checks"][gate].append(rec)
    put(args, m)
    print("RECORDED source anchor", gate, str(rel), args.line,
          "(line existence verified; interpretation unverified)")


def report(args):
    m = get(args)
    if args.gate not in m["checks"]:
        raise SystemExit("HOLD: unknown/conditional gate: " + args.gate)
    f = receipt_file(args.file)
    if f["size"] < 250:
        raise SystemExit("HOLD: evidence report too short")
    if len(args.claim.strip()) < 60:
        raise SystemExit("HOLD: report needs a substantive concrete claim")
    body = pathlib.Path(f["path"]).read_text(errors="replace")
    if "GATE:" + args.gate not in body:
        raise SystemExit("HOLD: report lacks an explicitly identified evidence section GATE:" + args.gate)
    if args.gate == "adversarial_second_pass" and not all(
            marker in body for marker in ("Challenge:", "Attempt:", "Result:")):
        raise SystemExit("HOLD: adversarial report needs Challenge/Attempt/Result sections")
    rec = {"kind": "analysis", "file": f, "claim": args.claim.strip(),
           "provenance": args.provenance, "recorded_utc": now()}
    if args.gate == "adversarial_second_pass" and args.provenance != "same-model-adversarial":
        raise SystemExit("HOLD: use external subcommand for genuinely external reviewer")
    m["checks"][args.gate].append(rec)
    put(args, m)
    print("RECORDED", args.gate, "analysis report; interpretation not verified")


def command_valid(purpose, argv, scope, subject, cl):
    prog = pathlib.Path(argv[0]).name
    if prog not in SEARCH_COMMANDS | BUILD_COMMANDS:
        return "unsupported executable for this evidence kind (no arbitrary success commands)"
    tokens = " ".join(argv[1:])
    if purpose in {"whole-tree-search", "build-graph", "integration-search"}:
        if prog not in SEARCH_COMMANDS:
            return "search purpose requires git/rg/grep/find"
        if purpose == "integration-search" and scope != "integration":
            return "integration-search must name integration scope"
        if purpose != "integration-search" and scope != "whole-tree":
            return "whole-tree search must use whole-tree scope"
        if not subject or subject not in tokens:
            return "search must include its subject in the executed argument vector"
        # Scoped searches may not be represented as complete tree evidence.
        if prog == "git" and not re.search(r"\b(grep|ls-files|log|diff)\b", tokens):
            return "git search must be grep/ls-files/log/diff"
        if prog == "rg" and "--files" not in argv and "-n" not in argv and "--line-number" not in argv:
            return "rg requires -n/--line-number or --files"
    elif purpose == "preimage-verify":
        if prog != "git" or "apply" not in argv or "--check" not in argv:
            return "preimage check must execute git apply --check on the submitted patch"
    else:
        if prog not in BUILD_COMMANDS:
            return "build/test evidence must execute make/compiler/recognized test runner"
        if purpose == "abi-lp64" and scope != "LP64":
            return "LP64 evidence needs LP64 scope"
        if purpose == "abi-ilp32" and scope != "ILP32":
            return "ILP32 evidence needs ILP32 scope"
        if purpose == "abi-lp64" and prog in {"gcc", "clang", "cc"} and not any(x in argv for x in ("-m64", "-target", "--target=")):
            return "LP64 compiler evidence needs explicit target flag"
        if purpose == "abi-ilp32" and prog in {"gcc", "clang", "cc"} and not any(x in argv for x in ("-m32", "-target", "--target=")):
            return "ILP32 compiler evidence needs explicit target flag"
        if purpose in {"build-or-test", "consumer-build"} and prog not in {"make", "gmake", "ninja", "pytest"}:
            return "kernel/selftest build scope requires an actual build/test target, not an isolated compiler probe"
        if purpose == "consumer-build" and scope != "cross-subsystem":
            return "consumer build must identify cross-subsystem scope"
        if purpose == "consumer-build" and not any("selftests" in a or "tools" in a or "-C" == a for a in argv):
            return "consumer build must include a real target/tree path"
    return ""


def run(args):
    m = get(args)
    if args.gate not in m["checks"]:
        raise SystemExit("HOLD: unknown gate")
    if args.purpose not in m["plan"]["requirements"][args.gate]:
        raise SystemExit("HOLD: purpose not required for gate")
    argv = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not argv:
        raise SystemExit("HOLD: missing executable")
    issue = command_valid(args.purpose, argv, args.scope, args.subject, m["plan"]["classification"])
    if issue:
        raise SystemExit("HOLD: " + issue)
    cl = m["plan"]["classification"]
    if args.purpose == "preimage-verify" and m["plan"]["patch_path"] not in argv:
        raise SystemExit("HOLD: git apply --check did not name the reviewed patch")
    source_bound = {"whole-tree-search", "build-graph", "preimage-verify"}
    if args.purpose in source_bound:
        if not args.cwd:
            raise SystemExit("HOLD: checked source tree requires explicit --cwd")
        snap = subprocess.run(["git", "-C", args.cwd, "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=False)
        if snap.returncode or snap.stdout.strip() != m["plan"]["source_ref"]:
            raise SystemExit("HOLD: evidence tree HEAD differs from preflight source revision")
        if pathlib.Path(argv[0]).name == "git" and "-C" in argv:
            pos = argv.index("-C")
            if pos + 1 >= len(argv) or pathlib.Path(argv[pos+1]).resolve() != pathlib.Path(args.cwd).resolve():
                raise SystemExit("HOLD: git -C path bypasses pinned evidence tree")
    if args.purpose in {"whole-tree-search", "build-graph"} and not args.cwd:
        raise SystemExit("HOLD: whole-tree search needs an explicit repository root --cwd")
    if args.purpose == "whole-tree-search" and args.gate == "all_callers" and args.subject not in cl["symbols"]:
        raise SystemExit("HOLD: whole-tree caller query must use a detected changed function; missing symbols may be added to a new preflight")
    if args.purpose == "whole-tree-search" and args.gate == "cross_tree_consumers":
        subjects = set(cl["files"] + cl["symbols"] + cl.get("consumer_symbols", []))
        if args.subject not in subjects and args.subject not in {"Makefile", "libcgroup.mk", "include"}:
            raise SystemExit("HOLD: consumer query must mention a changed interface or build graph")
    cp = subprocess.run(argv, cwd=args.cwd or None, capture_output=True,
                        text=True, errors="replace", check=False, timeout=args.timeout)
    root = pathlib.Path(args.manifest).resolve().parent / "gate-evidence"
    root.mkdir(exist_ok=True)
    payload = {"argv": argv, "cwd": str(pathlib.Path(args.cwd).resolve()) if args.cwd else str(pathlib.Path.cwd()),
               "purpose": args.purpose, "scope": args.scope, "subject": args.subject,
               "returncode": cp.returncode, "stdout": cp.stdout, "stderr": cp.stderr}
    serial = json.dumps(payload, indent=2, sort_keys=True).encode()
    out = root / (args.gate + "-" + digest(serial)[:16] + ".json")
    out.write_bytes(serial)
    rec = {"kind": "command", "purpose": args.purpose, "scope": args.scope,
           "subject": args.subject, "argv": argv, "cwd": payload["cwd"],
           "exit": cp.returncode, "file": receipt_file(out), "recorded_utc": now()}
    m["checks"][args.gate].append(rec)
    put(args, m)
    print(("PASS" if cp.returncode == 0 else "FAIL"), args.gate, args.purpose,
          "exit", cp.returncode, "receipt", out)
    if cp.returncode:
        raise SystemExit(1)


def hunk(args):
    m = get(args)
    h = next((v for v in m["plan"]["classification"]["hunks"] if v["id"] == args.id), None)
    if not h:
        raise SystemExit("HOLD: unknown patch hunk " + args.id)
    if args.file != h["file"]:
        raise SystemExit("HOLD: hunk source path does not match patch")
    f = receipt_file(args.report)
    if "HUNK:" + args.id not in pathlib.Path(f["path"]).read_text(errors="replace"):
        raise SystemExit("HOLD: report does not identify exact hunk " + args.id)
    if f["size"] < 200 or len(args.note.strip()) < 45:
        raise SystemExit("HOLD: insufficient hunk-specific proof")
    m["hunks"][args.id] = {"file": f, "note": args.note.strip(), "diff_header": h["header"],
                           "source_file": h["file"], "recorded_utc": now()}
    put(args, m)
    print("HUNK RECEIPT", args.id, h["file"])


def section(args):
    m = get(args)
    if args.id not in m["sections"]:
        raise SystemExit("HOLD: unknown standing-rule section")
    item = m["sections"][args.id]
    expected_gate = SECTION_GATES[int(args.id[1:])-1]
    if args.status == "APPLIED" and args.gate != expected_gate:
        raise SystemExit("HOLD: section " + args.id + " needs gate " + expected_gate)
    if len(args.reason.strip()) < 45:
        raise SystemExit("HOLD: give a concrete reason/status explanation")
    item.update(status=args.status, reason=args.reason.strip(), proof_gate=args.gate or "")
    put(args, m)
    print("SECTION", args.id, args.status)


def external(args):
    m = get(args)
    f = receipt_file(args.report)
    if f["size"] < 250 or not args.reviewer.strip() or args.reviewer.casefold() == "chatgpt":
        raise SystemExit("HOLD: external reviewer identity/report invalid")
    m["checks"]["adversarial_second_pass"].append({"kind": "external_review", "file": f,
        "reviewer": args.reviewer.strip(), "recorded_utc": now()})
    put(args, m)
    print("EXTERNAL REVIEW RECORDED", args.reviewer)


def check_receipt(rec, gate, valid_purposes):
    errors = []
    kind = rec.get("kind")
    f = rec.get("file")
    if not isinstance(f, dict):
        return ["missing receipt file"]
    fp = pathlib.Path(f.get("path", ""))
    if not fp.is_file() or digest(fp.read_bytes()) != f.get("sha256") or fp.stat().st_size != f.get("size"):
        return ["evidence file missing or modified"]
    if kind == "command":
        if rec.get("purpose") not in valid_purposes:
            errors.append("command used for wrong gate purpose")
        if rec.get("exit") != 0:
            errors.append("executed command failed")
        payload = json.loads(fp.read_text())
        for k, value in (("argv", rec.get("argv")), ("cwd", rec.get("cwd")),
                         ("returncode", rec.get("exit")), ("purpose", rec.get("purpose")),
                         ("scope", rec.get("scope")), ("subject", rec.get("subject"))):
            if payload.get(k) != value:
                errors.append("command metadata conflicts with receipt " + k)
        issue = command_valid(rec.get("purpose", ""), rec.get("argv", []),
                              rec.get("scope"), rec.get("subject", ""), {})
        if issue:
            errors.append("invalid command: " + issue)
    elif kind == "analysis":
        body = fp.read_text(errors="replace")
        if len(rec.get("claim", "")) < 60 or "GATE:" + gate not in body:
            errors.append("analysis is not specific to this gate")
        if gate == "adversarial_second_pass" and (
                rec.get("provenance") != "same-model-adversarial" or
                not all(x in body for x in ("Challenge:", "Attempt:", "Result:"))):
            errors.append("adversarial report lacks separately identified challenge")
    elif kind == "source":
        if not rec.get("line_text") or len(rec.get("note", "")) < 45:
            errors.append("invalid source anchor")
        else:
            lines = fp.read_text(errors="replace").splitlines()
            if not (isinstance(rec.get("line"), int) and 1 <= rec["line"] <= len(lines) and
                    lines[rec["line"]-1] == rec["line_text"]):
                errors.append("source line does not match pinned line")
    elif kind == "external_review":
        if not rec.get("reviewer") or fp.stat().st_size < 250:
            errors.append("external review invalid")
    else:
        errors.append("unknown evidence kind")
    return errors


def receipt_id(rec):
    """Bind the whole receipt, including its timestamp and evidence digest."""
    return digest(canonical(rec))


def resolve_revision(repo, token):
    # Restrict corrections to commit names, never options or path arguments.
    if not token or token.startswith("-"):
        raise ValueError("not a revision argument")
    argv = ["git", "-C", str(repo), "rev-parse", "--verify",
            "--end-of-options", token + "^{commit}"]
    cp = subprocess.run(argv, capture_output=True, text=True, timeout=30)
    value = cp.stdout.strip()
    if cp.returncode or not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ValueError("cannot resolve commit: " + token)
    return {"argv": argv, "exit": cp.returncode, "stdout": cp.stdout,
            "stderr": cp.stderr, "commit": value}


def retry_pair(m, gate, failed_id, replacement_id):
    if m["plan"]["schema"] != VERSION:
        raise ValueError("retry resolution requires a genuine v4 preflight")
    receipts = m.get("checks", {}).get(gate, [])
    old = [(i, r) for i, r in enumerate(receipts)
           if receipt_id(r) == failed_id]
    new = [(i, r) for i, r in enumerate(receipts)
           if receipt_id(r) == replacement_id]
    if len(old) != 1 or len(new) != 1:
        raise ValueError("both receipts must uniquely belong to this gate")
    oi, failed = old[0]
    ni, replacement = new[0]
    purposes = m["plan"]["requirements"][gate]
    if failed.get("kind") != "command" or replacement.get("kind") != "command":
        raise ValueError("only executed command receipts can be resolved")
    # Only the nonzero exit is waivable. Corrupt/missing/invalid evidence is not.
    if check_receipt(failed, gate, purposes) != ["executed command failed"]:
        raise ValueError("failed receipt has other errors or did not fail")
    if check_receipt(replacement, gate, purposes):
        raise ValueError("replacement must be a valid successful receipt")
    for key in ("purpose", "scope", "subject", "cwd"):
        if failed.get(key) != replacement.get(key):
            raise ValueError("retry changed " + key)
    try:
        ft = dt.datetime.fromisoformat(failed["recorded_utc"])
        rt = dt.datetime.fromisoformat(replacement["recorded_utc"])
        if ni <= oi or rt <= ft:
            raise ValueError("replacement must follow the failed command")
    except (KeyError, TypeError) as exc:
        raise ValueError("missing retry chronology") from exc
    return failed, replacement


def retry_differences(failed, replacement):
    a, b = failed["argv"], replacement["argv"]
    if a == b:
        return []
    # Corrections may only spell the SAME git-diff commit operands differently.
    # Changed search patterns, pathsets, flags, tests or executables need a new
    # review, not a convenient unrelated success with the same purpose label.
    if (len(a) != len(b) or a[:2] != ["git", "diff"] or
            b[:2] != ["git", "diff"] or "--" not in a or "--" not in b):
        raise ValueError("retry changes command beyond supported ref correction")
    boundary = a.index("--")
    if boundary != b.index("--") or a[boundary:] != b[boundary:]:
        raise ValueError("retry changes diff path coverage")
    differences = [i for i in range(len(a)) if a[i] != b[i]]
    if any(i < 2 or i >= boundary or a[i].startswith("-") or
           b[i].startswith("-") for i in differences):
        raise ValueError("retry changes command flags or scope")
    return differences


def retry_resolutions(m, document):
    """Validate an optional additive sidecar; never trust a mere pass label."""
    if document is None:
        return set(), []
    try:
        if (document.get("schema") != 1 or
                document.get("manifest_sha256") != digest(canonical(m)) or
                document.get("plan_sha256") != m["plan_sha256"]):
            raise ValueError("resolution sidecar does not bind this manifest")
        resolved = set()
        for entry in document["resolutions"]:
            gate, fid, rid = entry["gate"], entry["failed"], entry["replacement"]
            if fid in resolved or len(entry.get("reason", "").strip()) < 60:
                raise ValueError("duplicate resolution or inadequate explanation")
            failed, replacement = retry_pair(m, gate, fid, rid)
            differences = retry_differences(failed, replacement)
            proof = entry["proof"]
            path = pathlib.Path(proof["path"])
            raw = path.read_bytes()
            if len(raw) != proof["size"] or digest(raw) != proof["sha256"]:
                raise ValueError("retry proof missing or modified")
            data = json.loads(raw)
            if data["failed"] != fid or data["replacement"] != rid:
                raise ValueError("retry proof names different receipts")
            pairs = data["revisions"]
            if [p["index"] for p in pairs] != differences:
                raise ValueError("missing revision equivalence proof")
            for pair in pairs:
                for key, rec in (("old", failed), ("new", replacement)):
                    result = pair[key]
                    token = rec["argv"][pair["index"]]
                    argv = result["argv"]
                    if (len(argv) != 7 or argv[:2] != ["git", "-C"] or
                            argv[3:] != ["rev-parse", "--verify",
                                         "--end-of-options", token + "^{commit}"] or
                            result["exit"] != 0 or
                            not re.fullmatch(r"[0-9a-f]{40}", result["commit"]) or
                            result["stdout"].strip() != result["commit"]):
                        raise ValueError("invalid revision resolution receipt")
                if pair["old"]["commit"] != pair["new"]["commit"]:
                    raise ValueError("retry changed the compared commit")
            resolved.add(fid)
        return resolved, []
    except (ValueError, KeyError, TypeError, OSError) as exc:
        return set(), ["retry resolution: " + str(exc)]


def resolve_retry(args):
    m = get(args)
    try:
        failed, replacement = retry_pair(m, args.gate, args.failed,
                                         args.replacement)
        differences = retry_differences(failed, replacement)
        pairs = []
        for i in differences:
            old_token, new_token = failed["argv"][i], replacement["argv"][i]
            try:
                old = resolve_revision(failed["cwd"], old_token)
            except ValueError:
                if not args.ref_repo:
                    raise
                old = resolve_revision(args.ref_repo, old_token)
            new = resolve_revision(replacement["cwd"], new_token)
            if old["commit"] != new["commit"]:
                raise ValueError("retry changed the compared commit")
            pairs.append({"index": i, "old": old, "new": new})
        target = pathlib.Path(args.resolutions).resolve()
        if target == pathlib.Path(args.manifest).resolve():
            raise ValueError("resolution sidecar cannot overwrite manifest")
        if target.exists():
            document = load(target)
            _, errors = retry_resolutions(m, document)
            if errors:
                raise ValueError("; ".join(errors))
        else:
            document = {"schema": 1, "manifest_sha256": digest(canonical(m)),
                        "plan_sha256": m["plan_sha256"], "resolutions": []}
        proof_path = target.with_name(target.name + "." + args.failed[:16] + ".proof.json")
        if proof_path.exists():
            raise ValueError("retry proof already exists; refusing overwrite")
        save(proof_path, {"failed": args.failed, "replacement": args.replacement,
                          "revisions": pairs, "recorded_utc": now()})
        document["resolutions"].append({"gate": args.gate, "failed": args.failed,
            "replacement": args.replacement, "reason": args.reason.strip(),
            "proof": receipt_file(proof_path), "recorded_utc": now()})
        _, errors = retry_resolutions(m, document)
        if errors:
            raise ValueError("; ".join(errors))
        save(target, document)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        raise SystemExit("HOLD: " + str(exc))
    print("RESOLVED retry; original failed receipt and manifest unchanged")


def audit(m, resolutions=None):
    errors = valid_manifest(m)
    if errors:
        return errors, {}
    resolved, retry_errors = retry_resolutions(m, resolutions)
    errors.extend(retry_errors)
    errors.extend("all_callers: unresolved symbol inventory for " + hid
                  for hid in m["plan"]["classification"].get("unresolved_hunks", []))
    counts = {}
    for gate, purposes in m["plan"]["requirements"].items():
        receipts = m["checks"][gate]
        verified = set()
        if not receipts and gate not in {"all_hunks", "standing_rule_inventory"}:
            errors.append(gate + ": no receipts")
        for rec in receipts:
            issue = check_receipt(rec, gate, purposes)
            if issue == ["executed command failed"] and receipt_id(rec) in resolved:
                # A resolved failure supplies no evidence. Only its separately
                # validated successful replacement can meet a requirement.
                continue
            if issue:
                errors.extend(gate + ": " + x for x in issue)
                continue
            if rec["kind"] == "command":
                verified.add(rec["purpose"])
            elif rec["kind"] == "analysis":
                verified.add("adversarial" if gate == "adversarial_second_pass" else "analysis")
            elif rec["kind"] == "source":
                verified.add("source")
            elif rec["kind"] == "external_review":
                verified.add("adversarial")
        if gate == "all_callers":
            touched = {r.get("subject") for r in receipts if r.get("kind") == "command" and
                       r.get("purpose") == "whole-tree-search" and r.get("exit") == 0}
            for sym in m["plan"]["classification"]["symbols"]:
                if sym not in touched:
                    errors.append("all_callers: missing whole-tree consumer search for " + sym)
        if gate == "all_hunks":
            for h in m["plan"]["classification"]["hunks"]:
                ent = m["hunks"].get(h["id"])
                if not ent:
                    errors.append(f"{gate}: missing {h['id']} {h['file']}")
                else:
                    f = ent.get("file", {})
                    fp = pathlib.Path(f.get("path", ""))
                    if (not fp.is_file() or digest(fp.read_bytes()) != f.get("sha256") or
                        "HUNK:" + h["id"] not in fp.read_text(errors="replace") or
                        ent.get("diff_header") != h["header"] or ent.get("source_file") != h["file"]):
                        errors.append(f"{gate}: tampered {h['id']}")
            if all(m["hunks"].values()):
                verified.add("hunks")
        if gate == "standing_rule_inventory":
            for sid, entry in m["sections"].items():
                status = entry.get("status")
                if status == "UNRESOLVED":
                    errors.append(f"{gate}: {sid} unresolved: {entry.get('heading')}")
                elif status == "APPLIED":
                    g = entry.get("proof_gate")
                    expected_gate = SECTION_GATES[int(sid[1:])-1]
                    if g != expected_gate or not m["checks"].get(g):
                        errors.append(f"{gate}: {sid} lacks corresponding gate evidence ({expected_gate})")
                elif status == "NOT_APPLICABLE":
                    errors.append(f"{gate}: {sid} is an always-applicable workflow section; document inapplicable subchecks separately")
                else:
                    errors.append(f"{gate}: {sid} invalid status")
            if not any(e.startswith("standing_rule_inventory:") for e in errors):
                verified.add("sections")
        # Guard against generic analysis report being counted as a real build
        # or against a toy compile masquerading as a reverse-dependency audit.
        for missing in set(purposes) - verified:
            errors.append(gate + ": missing evidence kind " + missing)
        counts[gate] = {"required": list(purposes), "recorded": len(receipts), "matched": sorted(verified)}
    if m.get("unresolved"):
        errors.extend("unresolved: " + x for x in m["unresolved"])
    return errors, counts


def status(args):
    m = load(args.manifest)
    try:
        resolutions = load(args.resolutions) if args.resolutions else None
    except (OSError, ValueError) as exc:
        raise SystemExit("HOLD: cannot read retry resolutions: " + str(exc))
    errors, count = audit(m, resolutions)
    if errors:
        print(f"HOLD: {len(errors)} missing/invalid/unresolved checks")
        for x in errors[:150]:
            print(" -", x)
        if len(errors) > 150:
            print(f" - ... {len(errors)-150} further issues")
        raise SystemExit(2)
    print("ELIGIBLE_FOR_HUMAN_DECISION: receipts meet minimum structural checks")
    print("NOT A SOURCE-CORRECTNESS OR EXHAUSTIVENESS CERTIFICATION")
    if resolutions:
        print("Resolved failed command receipts retained:", len(resolutions["resolutions"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command_name", required=True)
    new = sub.add_parser("new", help="freeze patch, workflow and gate inventory BEFORE analysis")
    new.add_argument("--patch", required=True)
    new.add_argument("--manifest", required=True)
    new.add_argument("--workflow", default=str(WORKFLOW))
    new.add_argument("--review-id", required=True)
    new.add_argument("--source-ref", default="unverified")
    new.add_argument("--repo", required=True,
                     help="Git repository containing the pinned source commit")
    new.add_argument("--compilation-policy", choices=["required", "delegated"],
                     default="required",
                     help="delegated requires explicit AKPM no-compilation workflow override")
    new.add_argument("--symbol", action="append", default=[],
                     metavar="H001:NAME",
                     help="supplement inventory with a symbol in verified hunk code or its enclosing definition")
    new.set_defaults(func=init)
    inspect_p = sub.add_parser("inspect", help="record real file/line source evidence")
    inspect_p.add_argument("--manifest", required=True)
    inspect_p.add_argument("--gate", required=True)
    inspect_p.add_argument("--repo", required=True)
    inspect_p.add_argument("--path", required=True)
    inspect_p.add_argument("--line", type=int, required=True)
    inspect_p.add_argument("--note", required=True)
    inspect_p.set_defaults(func=inspect)
    report_p = sub.add_parser("report", help="attach an analysis report; never substitutes for real commands")
    report_p.add_argument("--manifest", required=True)
    report_p.add_argument("--gate", required=True)
    report_p.add_argument("--file", required=True)
    report_p.add_argument("--claim", required=True)
    report_p.add_argument("--provenance", choices=["same-model", "same-model-adversarial"], default="same-model")
    report_p.set_defaults(func=report)
    run_p = sub.add_parser("run", help="execute a semantic-category-checked command and record stdout/exit")
    run_p.add_argument("--manifest", required=True)
    run_p.add_argument("--gate", required=True)
    run_p.add_argument("--purpose", required=True, choices=sorted(CMD_PURPOSES))
    run_p.add_argument("--scope", choices=sorted(VALID_SCOPES), default="local")
    run_p.add_argument("--subject", default="")
    run_p.add_argument("--cwd")
    run_p.add_argument("--timeout", type=int, default=120)
    run_p.add_argument("command", nargs=argparse.REMAINDER)
    run_p.set_defaults(func=run)
    h = sub.add_parser("hunk", help="record per-diff-hunk source analysis")
    h.add_argument("--manifest", required=True)
    h.add_argument("--id", required=True)
    h.add_argument("--file", required=True)
    h.add_argument("--report", required=True)
    h.add_argument("--note", required=True)
    h.set_defaults(func=hunk)
    sec = sub.add_parser("section", help="mark a precommitted workflow section")
    sec.add_argument("--manifest", required=True)
    sec.add_argument("--id", required=True)
    sec.add_argument("--status", choices=["APPLIED", "NOT_APPLICABLE", "UNRESOLVED"], required=True)
    sec.add_argument("--reason", required=True)
    sec.add_argument("--gate", default="")
    sec.set_defaults(func=section)
    ex = sub.add_parser("external", help="attach genuinely external adversarial reviewer report")
    ex.add_argument("--manifest", required=True)
    ex.add_argument("--report", required=True)
    ex.add_argument("--reviewer", required=True)
    ex.set_defaults(func=external)
    rr = sub.add_parser("resolve-retry", help="record explicit retry resolution without changing original evidence")
    rr.add_argument("--manifest", required=True)
    rr.add_argument("--gate", required=True)
    rr.add_argument("--failed", required=True, help="SHA256 of canonical failed receipt")
    rr.add_argument("--replacement", required=True, help="SHA256 of canonical successful receipt")
    rr.add_argument("--reason", required=True)
    rr.add_argument("--resolutions", required=True, help="separate additive resolution JSON")
    rr.add_argument("--ref-repo", help="repository resolving a missing symbolic ref to the same commit")
    rr.set_defaults(func=resolve_retry)
    ch = sub.add_parser("check", help="fail closed on missing or invalid evidence (exit 2)")
    ch.add_argument("--manifest", required=True)
    ch.add_argument("--resolutions", help="explicit retry-resolution sidecar")
    ch.set_defaults(func=status)
    stat = sub.add_parser("status", help="show current hold/eligibility and missing evidence")
    stat.add_argument("--manifest", required=True)
    stat.add_argument("--resolutions", help="explicit retry-resolution sidecar")
    stat.set_defaults(func=status)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
