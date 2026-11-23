# Repository instructions

## Language

Write all repository-authored content in English, including skills, metadata,
tests, documentation, commit messages, and workflow files.

## Package boundaries

- Keep skills compatible with the Agent Skills specification.
- Keep agent-specific manifests and adapters out of the skills unless support
  for another agent is explicitly chosen.
- Keep examples synthetic. Never publish private statements, local machine
  paths, real spreadsheet links, credentials, or financial results.
- Keep repository-change and multi-repository coordination as independent
  skills with independent optional TOML profiles.
- Never make a marketplace refresh part of CI or a pre-commit hook.

## Development

- Use Python 3.15+ standard-library features only for package validation tools.
- Run `python tools/validate_package.py` and
  `python -m unittest discover -s tests -v` before publishing changes.
- Validate skill metadata with `gh skill publish --dry-run .`; do not publish
  a GitHub release unless explicitly requested.
