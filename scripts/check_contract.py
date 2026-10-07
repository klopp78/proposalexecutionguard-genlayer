import ast
import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "contracts" / "proposal_execution_guard.py").read_text(encoding="utf-8")
ast.parse(SOURCE)

required_controls = (
    "class ProposalExecutionGuard",
    "assess_execution",
    "get_execution_claim",
    "hashlib.sha256",
    "_canonical_parts",
    "declared_actions_hash",
    "source_snapshot_hashes",
    "snapshot_bundle_hash",
    "execution_reference_hash",
    "at_least_two_independent_hosts_required",
    "proposal_and_execution_urls_must_be_sources",
    "executed_match_requires_complete_proof",
    "execution_already_claimed",
    'proposed["decision"] == independent["decision"]',
    'proposed["action_match"] == independent["action_match"]',
    'proposed["source_snapshot_hashes"] == independent["source_snapshot_hashes"]',
)
for control in required_controls:
    if control not in SOURCE:
        raise SystemExit(f"missing required control: {control}")

for forbidden in ("wallet_getSnaps", "total = (total *", "leader_result.calldata =="):
    if forbidden in SOURCE:
        raise SystemExit(f"forbidden weak pattern: {forbidden}")

print("ProposalExecutionGuard contract structure check passed")
