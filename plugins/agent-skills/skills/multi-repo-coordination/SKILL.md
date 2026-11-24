---
name: multi-repo-coordination
description: Coordinate related work across two or more Git repositories while preserving each repository's instructions, local changes, and independently verifiable state.
license: MIT
---

# Multi-repository coordination

Use this skill when a request spans multiple repositories or requires changes
to be coordinated across repository boundaries.

## Coordinate the work

1. Identify the repositories in scope from the request and workspace. Confirm
   each root, branch, and working-tree status before changing files.
2. Read each repository's instructions and discover its language, tooling,
   tests, and publication rules independently.
3. Map shared contracts, dependencies, and the order in which each repository
   can safely change. Treat interfaces as the boundary between projects; do
   not duplicate one repository's business logic in another.
   Distinguish existing repositories from planned ones. Record where work is
   tracked, where it belongs, and which dependencies can advance now.
4. Work independently only where changes do not share an unfinished
   dependency. Use the configured parallelism preference as a limit, not a
   reason to parallelize dependent work.
5. Preserve existing local changes in every repository. Keep status, tests,
   branches, commits, and publication decisions separate per repository.
6. Verify each repository with its own checks, then run any available
   cross-repository compatibility check. For a changed interface, identify
   its producer, consumer, and contract version. Say whether verification used
   a mock or actual output from the producer. When resuming partial work,
   inspect existing issues, pull requests, and current interface behavior
   before repeating a stage. Report the result and remaining blockers per
   repository.

Do not commit, push, open pull requests, publish packages, or write to external
systems unless the user requested or explicitly approved that action for the
relevant repository. A request to publish one repository does not authorize
publication of the others.

## Optional preferences

If present, read this skill's optional TOML profile at
`.agents/skills-config/agent-skills/multi-repo-coordination.toml`. Its
available keys are listed in `config-options.json`. The package's
`scripts/audit_profile.py` can report new, unknown, or invalid options. With no
profile, infer conventions and available capacity from the repositories and
current environment. Ask only when a relevant preference cannot be inferred.
Keep this profile separate from every other skill profile.

`context.map_path` may point to a concise repository map, relative to the
directory containing the profile. Keep a skill-specific map in a
`multi-repo-coordination/` subdirectory beside the profile when creating one.
Read the relevant section first, then verify its claims against the current
repositories. A map should identify responsibilities, planned repositories,
producer-consumer interfaces, contract locations, and integration checks.
Link to existing documentation instead of
copying contracts or volatile branch and pull request state into the map.
When a task changes a documented interface or responsibility, update the
affected entry. A shared profile and map should use portable relative paths
and contain no private data.
