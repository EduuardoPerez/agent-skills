"""Validate the plugin, marketplace, and example profiles in this repository."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "plugins/agent-skills/scripts"),
)
from audit_profile import audit_profile  # noqa: E402


EXPECTED_SKILLS = {
    "repo-change-workflow",
    "multi-repo-coordination",
    "project-kanban-workflow",
}
MAX_SKILL_PROMPT_BYTES = 8_000
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MARKETPLACE_URL = "https://github.com/EduuardoPerez/agent-skills.git"


def _read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing required file: {path.name}")
        return None
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"Invalid JSON in {path}: {error}")
        return None
    if not isinstance(value, dict):
        errors.append(f"Expected a JSON object in {path}")
        return None
    return value


def _check_manifest(root: Path, errors: list[str]) -> None:
    manifest_path = root / "plugins/agent-skills/plugin.json"
    manifest = _read_json(manifest_path, errors)
    if manifest is None:
        return

    expected = {
        "$schema": PLUGIN_SCHEMA,
        "name": "agent-skills",
        "license": "MIT",
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            errors.append(f"Plugin manifest must set {key} to {value!r}")
    if (
        not isinstance(manifest.get("description"), str)
        or not manifest["description"].strip()
    ):
        errors.append("Plugin manifest must have a non-empty description")
    if not isinstance(manifest.get("version"), str) or not re.fullmatch(
        r"\d+\.\d+\.\d+", manifest["version"]
    ):
        errors.append("Plugin manifest version must use semantic versioning")


def _check_marketplace(root: Path, errors: list[str]) -> None:
    catalog_path = root / ".agents/plugins/marketplace.json"
    catalog = _read_json(catalog_path, errors)
    if catalog is None:
        return
    if catalog.get("name") != "agent-skills":
        errors.append("Marketplace name must be 'agent-skills'")
    interface = catalog.get("interface")
    if not isinstance(interface, dict) or not interface.get("displayName"):
        errors.append("Marketplace must define interface.displayName")

    plugins = catalog.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        errors.append("Marketplace must contain exactly one plugin")
        return
    entry = plugins[0]
    if not isinstance(entry, dict) or entry.get("name") != "agent-skills":
        errors.append("Marketplace plugin name must be 'agent-skills'")
        return

    source = entry.get("source")
    if not isinstance(source, dict):
        errors.append("Marketplace plugin source must be an object")
    else:
        if source.get("source") != "git-subdir":
            errors.append("Marketplace plugin source must use 'git-subdir'")
        if source.get("url") != MARKETPLACE_URL:
            errors.append(f"Marketplace plugin URL must be {MARKETPLACE_URL!r}")
        source_path = source.get("path")
        if not isinstance(source_path, str) or not source_path.startswith("./"):
            errors.append("Marketplace plugin path must be a repository-relative path")
        else:
            relative = Path(source_path[2:])
            resolved = (root / relative).resolve()
            if ".." in relative.parts or not resolved.is_relative_to(root.resolve()):
                errors.append("Marketplace plugin path must stay inside the repository")
            elif not (resolved / "plugin.json").is_file():
                errors.append("Marketplace plugin path must point to a plugin manifest")
        if source.get("ref") != "main":
            errors.append("Marketplace plugin must track the 'main' branch")

    policy = entry.get("policy")
    if not isinstance(policy, dict):
        errors.append("Marketplace plugin must define installation policy")
    elif (
        policy.get("installation") != "AVAILABLE"
        or policy.get("authentication") != "ON_INSTALL"
    ):
        errors.append("Marketplace plugin policy must be AVAILABLE and ON_INSTALL")
    if entry.get("category") != "Developer Tools":
        errors.append("Marketplace plugin category must be 'Developer Tools'")


def _frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as error:
        errors.append(f"Cannot read {path}: {error}")
        return {}
    parts = content.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        errors.append(f"{path} must begin with YAML frontmatter")
        return {}

    fields: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def _check_skill_prompt_size(path: Path, errors: list[str]) -> None:
    try:
        size = path.stat().st_size
    except OSError as error:
        errors.append(f"Cannot measure {path}: {error}")
        return
    if size > MAX_SKILL_PROMPT_BYTES:
        errors.append(
            f"{path} is {size} bytes; maximum SKILL.md size is "
            f"{MAX_SKILL_PROMPT_BYTES} UTF-8 bytes"
        )


def _check_skills(root: Path, errors: list[str]) -> None:
    skills_root = root / "plugins/agent-skills/skills"
    found = (
        {
            directory.name
            for directory in skills_root.iterdir()
            if directory.is_dir() and (directory / "SKILL.md").is_file()
        }
        if skills_root.is_dir()
        else set()
    )
    if found != EXPECTED_SKILLS:
        errors.append(
            f"Expected skills {sorted(EXPECTED_SKILLS)}, found {sorted(found)}"
        )

    for name in sorted(found):
        _check_skill_prompt_size(skills_root / name / "SKILL.md", errors)

    for name in sorted(EXPECTED_SKILLS):
        skill_root = skills_root / name
        skill_path = skill_root / "SKILL.md"
        fields = _frontmatter(skill_path, errors)
        if fields.get("name") != name:
            errors.append(f"Skill name in {skill_path} must match its directory")
        if not fields.get("description"):
            errors.append(f"Skill {name} must have a non-empty description")
        if fields.get("license") != "MIT":
            errors.append(f"Skill {name} must declare the MIT license")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append(f"Skill directory name {name!r} is not portable kebab-case")

        schema_path = skill_root / "config-options.json"
        schema = _read_json(schema_path, errors)
        if schema is None:
            continue
        if schema.get("skill") != name:
            errors.append(f"Configuration options in {schema_path} must name {name!r}")
        options = schema.get("options")
        if not isinstance(options, dict) or not options:
            errors.append(
                f"Configuration options in {schema_path} must be a non-empty object"
            )
            continue
        for key, option in options.items():
            if not isinstance(option, dict) or option.get("type") not in {
                "string",
                "integer",
                "number",
                "boolean",
            }:
                errors.append(
                    f"Unsupported configuration option {key!r} in {schema_path}"
                )
            elif not option.get("description"):
                errors.append(f"Configuration option {key!r} needs a description")
            elif option.get("type") in {"integer", "number"}:
                minimum = option.get("minimum")
                maximum = option.get("maximum")
                if minimum is not None and not isinstance(minimum, (int, float)):
                    errors.append(f"Minimum for {key!r} must be numeric")
                if maximum is not None and not isinstance(maximum, (int, float)):
                    errors.append(f"Maximum for {key!r} must be numeric")
                if (
                    isinstance(minimum, (int, float))
                    and isinstance(maximum, (int, float))
                    and minimum > maximum
                ):
                    errors.append(f"Minimum for {key!r} cannot exceed its maximum")

        example_path = root / "examples/config" / f"{name}.toml"
        try:
            example = tomllib.loads(example_path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as error:
            errors.append(f"Invalid TOML example for {name}: {error}")
            continue
        audit = audit_profile(example, options)
        if audit.missing or audit.unknown or audit.invalid:
            errors.append(
                f"TOML example for {name} does not match its declared options: {audit}"
            )


def validate_package(root: Path) -> list[str]:
    errors: list[str] = []
    _check_manifest(root, errors)
    _check_marketplace(root, errors)
    _check_skills(root, errors)
    workflow_path = root / ".github/workflows/validate.yml"
    if not workflow_path.is_file():
        errors.append("Missing .github/workflows/validate.yml")
    elif "marketplace upgrade" in workflow_path.read_text(encoding="utf-8"):
        errors.append("CI must not refresh a Codex marketplace")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_package(root)
    if errors:
        print("Package validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Package validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
