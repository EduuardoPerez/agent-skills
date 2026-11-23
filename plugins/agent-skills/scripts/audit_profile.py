"""Audit a skill-specific TOML preference profile."""

from __future__ import annotations

import argparse
import json
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Mapping


@dataclass(frozen=True)
class ProfileAudit:
    status: str
    missing: tuple[str, ...] = ()
    unknown: tuple[str, ...] = ()
    invalid: tuple[str, ...] = ()


def _flatten(values: Mapping[str, object], prefix: str = "") -> dict[str, object]:
    flattened: dict[str, object] = {}
    for key, value in values.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, Mapping):
            flattened.update(_flatten(value, path))
        else:
            flattened[path] = value
    return flattened


def _is_valid(value: object, option: Mapping[str, object]) -> bool:
    expected_type = option.get("type")
    valid_type = {
        "string": lambda item: isinstance(item, str),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float))
        and not isinstance(item, bool),
        "boolean": lambda item: isinstance(item, bool),
    }.get(str(expected_type))
    if valid_type is None or not valid_type(value):
        return False

    choices = option.get("choices")
    if choices is not None and value not in choices:
        return False

    minimum = option.get("minimum")
    maximum = option.get("maximum")
    if minimum is not None or maximum is not None:
        if expected_type not in {"integer", "number"} or isinstance(value, bool):
            return False
        if minimum is not None:
            if not isinstance(minimum, (int, float)) or isinstance(minimum, bool):
                return False
            if value < minimum:  # type: ignore[operator]
                return False
        if maximum is not None:
            if not isinstance(maximum, (int, float)) or isinstance(maximum, bool):
                return False
            if value > maximum:  # type: ignore[operator]
                return False

    return True


def audit_profile(
    profile: Mapping[str, object] | None,
    options: Mapping[str, Mapping[str, object]],
) -> ProfileAudit:
    """Report missing, unknown, and invalid options without modifying a profile."""
    if profile is None:
        return ProfileAudit(status="no_profile")

    flattened = _flatten(profile)
    declared = set(options)
    configured = set(flattened)
    return ProfileAudit(
        status="configured",
        missing=tuple(sorted(declared - configured)),
        unknown=tuple(sorted(configured - declared)),
        invalid=tuple(
            sorted(
                key
                for key, value in flattened.items()
                if key in options and not _is_valid(value, options[key])
            )
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", help="Skill directory name")
    parser.add_argument("--profile", type=Path, help="Optional TOML profile to inspect")
    arguments = parser.parse_args()

    plugin_root = Path(__file__).resolve().parents[1]
    skills_root = plugin_root / "skills"
    skill_root = (skills_root / arguments.skill).resolve()
    if not skill_root.is_relative_to(skills_root.resolve()) or not skill_root.is_dir():
        parser.error(f"Unknown skill: {arguments.skill}")
    schema_path = skill_root / "config-options.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        if arguments.profile is None:
            profile = None
        else:
            profile = tomllib.loads(arguments.profile.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, tomllib.TOMLDecodeError) as error:
        parser.error(str(error))

    audit = audit_profile(profile, schema["options"])
    print(json.dumps(asdict(audit), indent=2))
    if audit.status == "no_profile":
        print(
            "Infer repository conventions and ask only when a relevant choice is unclear."
        )
    elif audit.missing:
        print(
            "Review missing options; ask only when a relevant choice cannot be inferred."
        )
    return 1 if audit.unknown or audit.invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
