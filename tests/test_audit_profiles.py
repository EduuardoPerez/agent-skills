import unittest
import sys
from pathlib import Path


sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "plugins/agent-skills/scripts"),
)
from audit_profile import audit_profile


class AuditProfileTests(unittest.TestCase):
    def test_no_profile_uses_discovered_repository_conventions(self) -> None:
        result = audit_profile(None, {"preferences.summary_detail": {"type": "string"}})

        self.assertEqual(result.status, "no_profile")
        self.assertEqual(result.missing, ())
        self.assertEqual(result.unknown, ())

    def test_new_skill_option_is_reported_without_changing_old_profile(self) -> None:
        profile = {"preferences": {"summary_detail": "concise"}}
        schema = {
            "preferences.summary_detail": {
                "type": "string",
                "choices": ["concise", "detailed"],
            },
            "preferences.publication_summary": {
                "type": "string",
                "choices": ["short", "full"],
            },
        }

        result = audit_profile(profile, schema)

        self.assertEqual(result.missing, ("preferences.publication_summary",))
        self.assertEqual(profile, {"preferences": {"summary_detail": "concise"}})

    def test_audit_keeps_each_skills_profile_independent(self) -> None:
        repo_profile = {"preferences": {"summary_detail": "concise"}}
        repo_options = {"preferences.summary_detail": {"type": "string"}}
        multi_repo_options = {
            "preferences.max_parallel_repositories": {"type": "integer"}
        }

        repo_result = audit_profile(repo_profile, repo_options)
        multi_repo_result = audit_profile(repo_profile, multi_repo_options)

        self.assertEqual(repo_result.missing, ())
        self.assertEqual(
            multi_repo_result.missing, ("preferences.max_parallel_repositories",)
        )
        self.assertEqual(multi_repo_result.unknown, ("preferences.summary_detail",))

    def test_wrong_type_and_unsupported_value_are_reported(self) -> None:
        profile = {"preferences": {"max_parallel_repositories": True}}
        options = {
            "preferences.max_parallel_repositories": {
                "type": "integer",
                "minimum": 1,
                "maximum": 4,
            }
        }

        result = audit_profile(profile, options)

        self.assertEqual(result.invalid, ("preferences.max_parallel_repositories",))


if __name__ == "__main__":
    unittest.main()
