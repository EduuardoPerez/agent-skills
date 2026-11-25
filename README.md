# Agent Skills

Portable skills for repository changes, coordination across repositories, and
Kanban project work. The plugin is designed for independent use of each skill
and contains no agent-specific adapters.

## Requirements

Python 3.15 or newer is required for package validation tools. The repository's
`.python-version` file selects `3.15` with pyenv, which resolves to the newest
installed 3.15.x patch version.

## Included skills

- **`repo-change-workflow`** coordinates the requested stages of a change in
  one repository, from implementation and verification through publication
  when authorized.
- **`multi-repo-coordination`** maps dependencies and shared interfaces across
  repositories, sequences related work, and verifies the combined result.
- **`project-kanban-workflow`** manages GitHub Project work from task discovery
  through creation, prioritization, delivery, and cancellation. It links related
  cards and carries verified findings into the next task.

The portable skills are in `plugins/agent-skills/skills/`. The plugin manifest
and Codex marketplace catalog package them for installation.

## Install in Codex

Add this repository's marketplace at its `main` branch and install the plugin:

```sh
codex plugin marketplace add EduuardoPerez/agent-skills --ref main
codex plugin add agent-skills@agent-skills
```

Start a new Codex conversation to use the installed skills. Refresh the named
marketplace only when you want to update the plugin:

```sh
codex plugin marketplace upgrade agent-skills
```

The refresh is an explicit local action. CI and pre-commit do not run it.

Other agents can use the standard skill directories according to their own
installation workflow. This repository does not ship host-specific manifests
or adapters for them.

## Configuration

Each skill can read its own optional TOML profile from the consuming
repository:

```text
.agents/skills-config/agent-skills/repo-change-workflow.toml
.agents/skills-config/agent-skills/multi-repo-coordination.toml
.agents/skills-config/agent-skills/project-kanban-workflow.toml
```

Commit profiles that contain shared project context, such as a Project URL or
a path from the profile directory to a repository map. Keep a new map in a
skill-specific subdirectory beside its profile. A profile can include a comment
linking to this repository's installation instructions for new collaborators.
Keep private data and machine-specific paths out of committed profiles. Only
save preferences that cannot be inferred from repository instructions,
configuration, or conventions. If a profile is absent, the skill discovers
repository conventions and asks only when a relevant decision cannot be
inferred. Keep the three profiles separate.

Example profiles are in `examples/config/`. They illustrate the available
preferences and are not user settings. The skill-specific
`config-options.json` files define those options. To audit a profile after an
update, run:

```sh
python plugins/agent-skills/scripts/audit_profile.py repo-change-workflow \
  --profile .agents/skills-config/agent-skills/repo-change-workflow.toml
```

The audit reports new options for review without editing the profile. Ask the
user only when the missing preference affects a choice the repository cannot
settle. Unknown options and invalid values are reported as errors.

## Validation

Run the package checks from the repository root:

```sh
python tools/validate_package.py
python -m unittest discover -s tests -v
gh skill publish --dry-run .
```

The GitHub Actions workflow runs these checks. It validates the package and
skills but does not publish a GitHub release or refresh a Codex marketplace.

## License

This repository is licensed under the MIT License. See `LICENSE`.
