#!/usr/bin/env python3
"""AKPM patch-review evidence gate (v2), executed inside ChatGPT.

No separate runner or local installation is required. The assistant must invoke
'new' before analyzing a patch and 'check' before writing the recommendation.

This checks *evidence receipts*, not whether the reviewer's reasoning is true,
whether searches were exhaustive, or whether the model obeyed the invocation
rule. It never authorizes 'take' or a Reviewed-by tag. An unresolved mandatory
requirement always results in HOLD. Never manufacture retroactive receipts.

Commands: new, inspect, run, report, hunk, section, external, check, status.
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

VERSION = 2
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


def classify(raw):
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


def expected_specs(cl):
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


def plan_data(patch, workflow, review_id, source_ref):
    raw = patch.read_bytes()
    cl = classify(raw)
    specs = expected_specs(cl)
    secs = section_plan(workflow.read_text())
    return {"schema": VERSION, "patch_path": str(patch.resolve()), "patch_sha256": digest(raw),
            "workflow_path": str(workflow.resolve()), "workflow_sha256": digest(workflow.read_bytes()),
            "review_id": review_id, "source_ref": source_ref,
            "classification": cl, "requirements": {x: list(y) for x, y in specs.items()},
            "section_headings": {k: v["heading"] for k, v in secs.items()}}


def init(args):
    p = pathlib.Path(args.patch).resolve()
    w = pathlib.Path(args.workflow).resolve()
    manifest = pathlib.Path(args.manifest)
    if manifest.exists():
        raise SystemExit("HOLD: manifest already exists; refusing to overwrite preflight")
    if not args.review_id.strip():
        raise SystemExit("review ID required")
    plan = plan_data(p, w, args.review_id, args.source_ref)
    o = {"plan": plan, "plan_sha256": digest(canonical(plan)), "created_utc": now(),
         "checks": {gate: [] for gate in plan["requirements"]},
         "sections": section_plan(w.read_text()), "hunks": {h["id"]: None for h in plan["classification"]["hunks"]},
         "unresolved": [], "decision": None}
    save(manifest, o)
    print(f"CREATED {manifest} required_gates={len(o['checks'])} "
          f"hunks={len(o['hunks'])} workflow_sections={len(o['sections'])} HOLD")
    if plan["classification"]["shared"] or plan["classification"]["abi"]:
        print("Triggered: whole-tree reverse dependencies, LP64+ILP32, external consumer build")


def valid_manifest(m, require_existing=True):
    errors = []
    p = m.get("plan", {})
    if p.get("schema") != VERSION:
        return ["unknown or old gate manifest schema (v2 required)"]
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
    expected = plan_data(patch, wf, p.get("review_id"), p.get("source_ref"))
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
        combined = " ".join(cl["files"] + cl["symbols"])
        if args.subject not in combined and args.subject not in {"Makefile", "libcgroup.mk", "include"}:
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


def audit(m):
    errors = valid_manifest(m)
    if errors:
        return errors, {}
    counts = {}
    for gate, purposes in m["plan"]["requirements"].items():
        receipts = m["checks"][gate]
        verified = set()
        if not receipts and gate not in {"all_hunks", "standing_rule_inventory"}:
            errors.append(gate + ": no receipts")
        for rec in receipts:
            issue = check_receipt(rec, gate, purposes)
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
    errors, count = audit(m)
    if errors:
        print(f"HOLD: {len(errors)} missing/invalid/unresolved checks")
        for x in errors[:150]:
            print(" -", x)
        if len(errors) > 150:
            print(f" - ... {len(errors)-150} further issues")
        raise SystemExit(2)
    print("ELIGIBLE_FOR_HUMAN_DECISION: receipts meet minimum structural checks")
    print("NOT A SOURCE-CORRECTNESS OR EXHAUSTIVENESS CERTIFICATION")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command_name", required=True)
    new = sub.add_parser("new", help="freeze patch, workflow and gate inventory BEFORE analysis")
    new.add_argument("--patch", required=True)
    new.add_argument("--manifest", required=True)
    new.add_argument("--workflow", default=str(WORKFLOW))
    new.add_argument("--review-id", required=True)
    new.add_argument("--source-ref", default="unverified")
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
    ch = sub.add_parser("check", help="fail closed on missing or invalid evidence (exit 2)")
    ch.add_argument("--manifest", required=True)
    ch.set_defaults(func=status)
    stat = sub.add_parser("status", help="show current hold/eligibility and missing evidence")
    stat.add_argument("--manifest", required=True)
    stat.set_defaults(func=status)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
