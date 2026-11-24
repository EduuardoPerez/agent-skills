---
name: project-kanban-workflow
description: Manage a small project's Kanban work, including suggesting, creating, editing, prioritizing, progressing, and canceling GitHub Project items.
license: MIT
---

# Project Kanban workflow

Use this skill when the user asks what to work on, discusses a concrete new
project task, or asks to manage a GitHub Project item. Keep the process light
for a solo project. Read the optional profile at
`.agents/skills-config/agent-skills/project-kanban-workflow.toml` in the
current repository. `project.url` identifies the Project. If the user assigns
a Project URL to this repository for future work, save its canonical URL to
the profile immediately. Preserve other settings and comments on updates.
Treat a one-off URL as one-off. If a different Project is already configured
and the requested replacement is unclear, ask which association to keep.
Shared profiles can be committed when their URLs and content are suitable for
everyone using the repository. Include a short comment linking to the skill's
source and installation instructions.

## Find and shape work

- Read the relevant Project items and repository issues. For a known item,
  fetch only that item and its relevant fields. For a plan or backlog review,
  broaden discovery to open, closed, archived, and draft work so that the same
  deliverable is not proposed twice.
- From a conversation or plan, suggest an item only for a distinct, actionable
  outcome with a way to check completion. Link existing coverage. Suggest an
  edit when an existing issue needs another criterion. Check why canceled work
  was abandoned before proposing it again.
- On a request to create, choose the repository that owns the outcome and
  suggest an assignee and a priority separately. Assign the issue only after
  the user explicitly accepts the suggested assignee. Create the issue there,
  then add it to the Project backlog. If that repository is planned, use the
  agreed temporary repository or a Project draft. A draft has no issue
  assignee; ask again before assigning anyone when it becomes an issue. Verify
  the created issue's assignees, when applicable, and the Project item's status
  separately. Report partial results. If adding an issue to the Project fails,
  resume using the existing issue rather than creating another.
- Edit titles, descriptions, and acceptance criteria on the issue, and Project
  fields on the Project item. Read before editing and preserve unrelated
  content. Verify the result. Follow the repository's language and privacy
  conventions for public text.

## Choose and progress work

Review work in progress and in review before recommending another task.
Recommend a ready item based on the current goal, urgency, dependencies, and
work it unlocks. Keep one active item as a useful default, while respecting
the user's choice to switch. Move an item to Ready when its outcome and
acceptance criteria are clear and required dependencies are available. Move it
to In progress when work begins, and In review when a deliverable is ready to
assess. Confirm the actual Project's status options rather than assuming these
names. Use `repo-change-workflow` for implementation in one repository and
`multi-repo-coordination` when several are involved. Mark Done only after the
acceptance criteria are verified and, when delivery requires a pull request,
its merge is confirmed. Check the final state because Project automations may
also change it.

When work begins, check the authenticated GitHub account to identify who is
starting it, unless the user explicitly names someone else. Read the issue's
current assignees. Keep the assignment if that person is already assigned. If
not, propose assigning them alongside current assignees for shared work, or
replacing the current assignees for a handoff. Apply only the option the user
accepts. If nobody is assigned, propose assigning the person starting the
work. Acceptance of an assignee when the card was created does not authorize a
later assignment change. After changes, verify the issue's assignees and the
Project item's fields and status separately; report any partial result so the
remaining step can be resumed without duplicating work.

Read the Project's priority options and any documented convention. When asked
to suggest priorities, explain a small number of useful changes based on
urgency, the next deliverable, and dependencies. When asked to apply them,
set and verify the Project field. Leave other items unclassified when that is
sufficient. If the Project has no priority field, recommend an order in the
conversation and create a field only on an explicit request.

## Cancel or remove work

When a task is obsolete, record the reason and any replacement, close its
issue as not planned, and archive its Project item. For a draft item, record
the reason and archive it. Removing an item from the Project preserves its
issue. If deletion is requested, identify exactly what would be deleted and
confirm before the irreversible action. Verify each transition and report any
partial result so it can be resumed without duplication.

The optional profile's keys are listed in `config-options.json`. The package's
`scripts/audit_profile.py` can validate it. Prefer the saved Project URL for
stable discovery and fetch live statuses, priorities, and items when needed.
