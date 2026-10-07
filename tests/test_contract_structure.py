import ast
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "contracts" / "proposal_execution_guard.py").read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)


class ProposalExecutionGuardStructureTests(unittest.TestCase):
    def test_public_api_and_append_only_registry_exist(self):
        names = {node.name for node in ast.walk(TREE) if isinstance(node, ast.FunctionDef)}
        expected = {
            "assess_execution", "get_assessment", "list_assessment_ids",
            "get_execution_claim",
        }
        self.assertTrue(expected.issubset(names))
        self.assertIn("self.assessment_ids.append(assessment_id)", SOURCE)

    def test_every_consequential_result_is_validator_compared(self):
        for field in (
            "decision", "proposal_status", "execution_status", "proposal_match",
            "action_match", "execution_tx_match", "target_chain", "executed_at_utc",
            "supporting_source_count", "readable_source_count", "source_snapshot_hashes",
            "snapshot_bundle_hash", "assessment_context_hash",
        ):
            self.assertIn(f'proposed["{field}"] == independent["{field}"]', SOURCE)

    def test_commitments_are_collision_resistant_and_unambiguous(self):
        self.assertIn("hashlib.sha256", SOURCE)
        self.assertIn('str(len(str(part))) + ":" + str(part)', SOURCE)
        self.assertNotIn("% 1000000007", SOURCE)

    def test_executed_match_requires_complete_proof(self):
        self.assertIn("executed_match_requires_complete_proof", SOURCE)
        self.assertIn("supporting_count < 2", SOURCE)
        self.assertIn("proposal_and_execution_urls_must_be_sources", SOURCE)

    def test_execution_receipts_cannot_be_replayed(self):
        self.assertIn("execution_already_claimed", SOURCE)
        self.assertIn("self.claimed_executions[execution_reference_hash] = assessment_id", SOURCE)


if __name__ == "__main__":
    unittest.main()
