---
name: project-kanban-workflow
description: Use when managing GitHub Project items, turning a plan or conversation into related cards, choosing what to work on, or handing findings to the next contributor.
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
  conventions for public text. When an edit changes a deliverable, dependency,
  or finding, review directly affected cards in the same update and revise any
  action, decision, or acceptance criterion that depends on the change.

### Connect cards from a plan or conversation

For each distinct deliverable, identify which other cards need its result and
what they can do before it arrives. List order alone establishes no dependency.
Match deliverables to existing items first. After authorized creation, use the
actual issue or draft links. Only link items visible to the intended audience.

- When an outstanding prerequisite prevents starting or finishing, record a
  native GitHub issue dependency where supported. Name the required result and
  the milestone it gates on the consuming card. If an endpoint is a draft or the
  dependency cannot be set, describe the prerequisite on the card and report the
  limitation.
- When a finding informs a decision or two teams can work in parallel, add a
  contextual reference only if it explains an action or coordination need.
  Independent work needs no link.

### Hand work to the next session

Write the card so a new contributor can identify the outcome, take the first
step, and check completion. Include the decisions, constraints, and open
questions that affect those actions. A short card may need only a few sentences.

At completion, record the outcome, the checks actually performed, and the limits
of the evidence. Identify direct consumers by link when safe. Read each affected
card and integrate the smallest useful finding beside the action, decision or
acceptance check it changes. Link back to its source and summarize enough to
start from that card alone. On retries, reread the cards and their relationships,
apply only missing edits, then verify both ends. Report any unfinished update.

For example, in a synthetic build project, #40 defines an archive format and
#41 builds its reader. The reader can start against a draft, but accepting it
requires the approved format from #40. Record that dependency on #41. When #40
closes, its handoff to #41 can say that an empty archive is valid and was tested.
On #41, link #40 and add a reader check for an empty archive. This finding can
be used immediately. An independent typography review needs no update.

### Use private evidence

Publish only conclusions, their scope, and the type of evidence needed to
resolve an open question. Check the text and every reference for sensitive
details such as names, identifiers, sample data, internal URLs, or local paths
before posting.

Use a private handoff index supplied for the session or configured through
`context.handoff_index_path` (relative to the profile directory). Look up the
card by its qualified issue reference or stable item URL. Each entry points to
the local artifact or section and says which question it answers and where its
evidence ends. Reuse entries when updating the index. Before writing it in a
repository, verify the file is both Git-ignored and untracked. A shared
profile may name a generic relative index path. Supply sensitive locations
privately and keep them out of public cards. If the index or artifact is
unavailable, start with the public summary and ask privately for the specific
evidence only when an open decision requires it.

## Choose and progress work

Review work in progress and in review before recommending another task.
Recommend a ready item based on the current goal, urgency, dependencies, and
work it unlocks. Keep one active item as a useful default, while respecting
the user's choice to switch. Move an item to Ready when its outcome and
acceptance criteria are clear and the prerequisites for starting are available.
Move it to In progress when work begins, and In review when a deliverable is
ready to assess. Confirm the actual Project's status options rather than
assuming these names. Use `repo-change-workflow` for implementation in one
repository and `multi-repo-coordination` when several are involved. Mark Done
only after the acceptance criteria are verified and, when delivery requires a
pull request, its merge is confirmed. Check the final state because Project
automations may also change it.

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
