import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.validate_package import _check_skill_prompt_size, validate_package


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class PackageValidationTests(unittest.TestCase):
    def test_shared_skill_plugin_and_marketplace_are_well_formed(self) -> None:
        self.assertEqual(validate_package(REPOSITORY_ROOT), [])

    def test_skill_prompt_limit_counts_utf8_bytes_for_any_skill(self) -> None:
        with TemporaryDirectory() as directory:
            skill_path = Path(directory) / "another-skill" / "SKILL.md"
            skill_path.parent.mkdir()
            skill_path.write_text("a" * 7_998 + "é", encoding="utf-8")
            errors: list[str] = []
            _check_skill_prompt_size(skill_path, errors)
            self.assertEqual(errors, [])

            skill_path.write_text("a" * 7_999 + "é", encoding="utf-8")
            _check_skill_prompt_size(skill_path, errors)
            self.assertEqual(len(errors), 1)
            self.assertIn("8001 bytes", errors[0])
            self.assertIn("another-skill", errors[0])


if __name__ == "__main__":
    unittest.main()
