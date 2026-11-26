---
name: repo-change-workflow
description: Coordinate the stages of an implementation or fix in one Git repository, from understanding the request through verification and any explicitly requested publication.
license: MIT
---

# Repository change workflow

Use this skill when a repository change spans multiple stages. Skip it for
questions, reviews alone, and isolated routine edits unless the user asks for
the workflow.

## Select the stages

1. Read the repository instructions, Git status and branch, CI workflow,
   pre-commit configuration, and relevant project commands.
2. Preserve uncommitted user changes and keep the change focused.
3. When integration requires review, explicitly include opening or updating a
   pull request in the plan. If publication is pending authorization, mark that
   step as pending. Select the stages required by the requested outcome:
   - **Branch:** create or use a task branch when requested, required by the
     repository, or needed for an agreed commit or pull request. Do not disrupt
     uncommitted work.
   - **Implement:** follow the repository's architecture and instructions.
   - **Verify:** discover checks from CI and pre-commit configuration. Run
     relevant checks when requested or required by the repository. Add tests
     only when requested or needed to implement the change. Report failures
     accurately and do not claim checks passed unless they completed
     successfully.
   - **Commit:** commit only when explicitly requested or included in the
     agreed delivery. Review staged changes and exclude unrelated files.
   - **Publish:** push or open a pull request only when explicitly requested
     or clearly included in the agreed scope. Before opening a pull request,
     check for one on the same repository and head branch and confirm its base.
     Reuse an existing pull request rather than creating a duplicate; update
     its summary only when authorized. If none exists, open one and verify its
     state and direct URL. Never merge unless asked.
4. Review the final diff for unintended changes and report the stages completed
   or skipped with the reason.

## Repository discovery

Discover commands, tests, formatting, type checks, and project conventions
from the current repository. Use the repository's instructions as the source
of truth. Do not copy project-specific commands or settings into a profile.

## Optional preferences

If present, read this skill's optional TOML profile at
`.agents/skills-config/agent-skills/repo-change-workflow.toml`. Its available
keys are listed in `config-options.json`. The package's `scripts/audit_profile.py`
can report new, unknown, or invalid options. A missing profile means discover
repository conventions. For a missing preference, infer it when repository
instructions settle the choice; otherwise ask only when the decision matters
to the requested change. Keep this profile separate from all other skill
profiles.
