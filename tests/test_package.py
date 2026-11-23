import unittest
from pathlib import Path

from tools.validate_package import validate_package


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class PackageValidationTests(unittest.TestCase):
    def test_shared_skill_plugin_and_marketplace_are_well_formed(self) -> None:
        self.assertEqual(validate_package(REPOSITORY_ROOT), [])


if __name__ == "__main__":
    unittest.main()
