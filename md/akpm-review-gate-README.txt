AKPM review gate v2 -- ChatGPT-local evidence audit (2026-10-23)
==============================================================

PURPOSE
-------
The assistant runs this in its own execution environment for each NEW
kernel review. You do not need to install anything, run software on ts,
or switch to Codex. The review prompt remains simply "review this".

Before source analysis, the assistant must execute:

  python3 akpm-review-gate.py new \
    --patch /mnt/data/submitted-patch.mbox \
    --workflow /mnt/data/akpm-patch-review-workflow.md \
    --manifest /mnt/data/review-R035/gate.json \
    --review-id R-035 --source-ref FULL_40_CHARACTER_BASE_SHA

The full SHA is verified against the intended kernel tree and recorded.
This creates a fail-closed preflight tied to the original patch, tree
revision, workflow checksum, and a fixed set of requirements. Existing
manifests cannot be overwritten via 'new'. For a multi-patch mbox, its
hunks are tracked separately under their source paths.

During review, the assistant records proof, for example:

  # Local pinned checkout, real line anchor:
  python3 akpm-review-gate.py inspect \
    --manifest /mnt/data/review-R035/gate.json \
    --gate base_and_preimage --repo /mnt/data/pinned-kernel \
    --path mm/memcontrol.c --line 2455 \
    --note 'Explain source state, locks and applicable invariant here.'

  # Source search against a real checkout, not an arbitrary snippet:
  python3 akpm-review-gate.py run \
    --manifest /mnt/data/review-R035/gate.json \
    --gate all_callers --purpose whole-tree-search --scope whole-tree \
    --subject named_changed_helper --cwd /mnt/data/pinned-kernel -- \
    rg -n named_changed_helper .

  # Attach substantive analysis. The file must include the exact
  # marker GATE:all_callers and describe the source examination.
  python3 akpm-review-gate.py report \
    --manifest /mnt/data/review-R035/gate.json \
    --gate all_callers --file /mnt/data/review-R035/callers.md \
    --claim 'Concrete explanation of searched producers, consumers, and
             the specific remaining or dismissed failure paths.'

  # For every diff hunk, record a specific HUNK:H001 section, etc.
  # For every standing workflow section S01..S24, record the correct
  # associated evidence gate with the section command.

A separate adversarial report must include:
  GATE:adversarial_second_pass
  Challenge: ...
  Attempt: ...
  Result: ...
It may be a second pass by ChatGPT, correctly labeled SAME MODEL.
An actual external independent reviewer is optional and has a
separate 'external' command. Do not claim a second model was run if not.

At the end, BEFORE any recommendation:

  python3 akpm-review-gate.py check \
    --manifest /mnt/data/review-R035/gate.json

Output:
  HOLD (exit 2): Missing, invalid, failing, or unresolved evidence.
  ELIGIBLE_FOR_HUMAN_DECISION (exit 0): Minimum evidence categories are
    present, with no recorded failing checks or missing section/hunk.

This does NOT prove completeness or authorize Reviewed-by or 'take'.
The assistant must additionally apply the full manual rule inventory and
resolve all material findings. If either remains incomplete, say HOLD.
The gate is not an independent response controller: ordinary ChatGPT
cannot guarantee tool invocation solely by editing policy files.

REPRODUCING THE GATE TESTS
--------------------------
  python3 test_akpm_review_gate.py

Nine tests cover R-034's shared API failure, a real nonzero GCC typedef
probe, fail-closed missing/tampered evidence, an irrelevant 'true'
command, missing adversarial counterexample, wrong evidence links,
and a synthetic passing receipt example that becomes HOLD if evidence
is changed. It does NOT build or run the Linux kernel or KVM selftests.

COMPATIBILITY
-------------
This version uses a new manifest schema. v1 manifests are not quietly
accepted or upgraded, because recreating a preflight after review
would misrepresent the evidence timeline. R-034 remains HOLD.
