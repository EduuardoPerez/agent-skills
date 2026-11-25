---
name: project-kanban-workflow
description: Use when managing GitHub Project items, turning a plan or conversation into related cards, choosing what to work on, or handing findings to the next contributor.
license: MIT
---

# Project Kanban workflow

Use this skill for a concrete new project task as well as existing Project
work. Keep the process light for a solo project. Read the optional profile at
`.agents/skills-config/agent-skills/project-kanban-workflow.toml` in the current
repository. `project.url` identifies its Project. If the user assigns a Project
URL to this repository for future work, save the canonical URL immediately;
preserve other settings and comments. Treat a one-off URL as one-off. If a
different Project is configured and replacement is unclear, ask which to keep.
A shared profile may be committed when suitable for everyone; include a short
comment linking to this skill's source and installation instructions. The
profile's keys are in `config-options.json`; validate it with
`scripts/audit_profile.py` when needed. Fetch live Project options and items.

## Find and shape work

- Read the relevant Project items and repository issues. Fetch only a known
  item's relevant fields; broaden plan or backlog discovery to open, closed,
  archived, and draft work to avoid duplicate deliverables.
- Suggest a card for each distinct, actionable outcome with a completion
  check. Link existing coverage, edit existing criteria where appropriate, and
  investigate why canceled work was abandoned before proposing it again.
- For creation, choose the repository that owns the outcome; suggest an
  assignee and priority separately. **Assign only after explicit acceptance of
  that assignee.** Create the issue, then add it to the Project backlog. For a
  planned repository, use an agreed temporary repository or Project draft. A
  draft has no issue assignee; ask again when it becomes an issue. Verify issue
  assignees and Project status separately. If Project addition fails, resume
  with the existing issue; report partial results without creating another.
- Edit issue titles, descriptions, and acceptance criteria on the issue;
  Project fields on the Project item. Read before editing, preserve unrelated
  content, and verify the result. When a deliverable, dependency, or finding
  changes, review directly affected cards and revise dependent actions,
  decisions, or acceptance checks in the same update.

When turning a plan or conversation into multiple deliverables, read
[dependencies and related cards](references/dependencies.md) to identify
which outcomes depend on others. Before creating or substantially editing a
card, read
[handoffs](references/handoffs.md) to make it actionable. Read
[dependencies and related cards](references/dependencies.md) before linking or
changing dependencies. At completion or for a cross-card finding, reread
[handoffs](references/handoffs.md) before editing affected cards. Apply the
repository's language and privacy conventions to public text.

## Choose and progress work

Review work in progress and in review before recommending another task. Choose
a ready item based on the current goal, urgency, prerequisites, and work it
unlocks; one active item is a useful default, but respect a switch. Move an
item to Ready when its outcome, acceptance checks, and starting prerequisites
are clear; to In progress when work begins; and to In review when its
deliverable is ready to assess. **Use the actual Project's status options.**
Use `repo-change-workflow` for implementation in one repository and
`multi-repo-coordination` for several. Mark Done only when acceptance checks
are verified and any required pull request is merged. Check final status
because Project automation may change it.

When work begins, identify the authenticated starter unless the user names
someone else, and read current issue assignees. Keep the assignment if the
starter is already assigned. Otherwise propose adding them for shared work or
replacing assignees for a handoff; if unassigned, propose assigning the starter.
Apply only the accepted option. Earlier consent at creation does not authorize
a later assignment change. Verify assignees and Project fields separately and
report partial results for safe retries.

Read live priority options and any documented convention. Suggest a few useful
changes based on urgency, the next deliverable, and dependencies. Set and
verify the field only when asked. Leave other items unclassified if sufficient.
If no priority field exists, recommend an order in conversation; create a field
only on explicit request.

## Public and private evidence

**Publish only conclusions, scope, and the type of evidence needed for open
questions.** Check text and every reference for sensitive names, identifiers,
sample data, internal URLs, and local paths. Link only items visible to the
intended audience. For private artifacts or a configured
`context.handoff_index_path`, read [private evidence](references/private-evidence.md)
before writing an index or citing evidence. If private evidence is unavailable,
start with a safe public summary; ask privately for specific evidence only if
an open decision requires it.

## Cancel or remove work

For obsolete work, record the reason and replacement, close its issue as not
planned, and archive its Project item. For a draft, record the reason and
archive it. Removing a Project item preserves its issue. Confirm exactly what
would be deleted before irreversible deletion. Verify each transition and
report partial results so retries do not duplicate work.
