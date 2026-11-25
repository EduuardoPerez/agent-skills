# Dependencies and related cards

For each distinct deliverable, identify which other cards need its result and
what they can do before it arrives. List order alone establishes no
dependency. Match deliverables to existing items first. After authorized
creation, use actual issue or draft links and only link items visible to the
intended audience.

- When an outstanding prerequisite prevents starting or finishing, record a
  native GitHub issue dependency where supported. Name the required result and
  the milestone it gates on the consuming card. If either endpoint is a draft
  or the dependency cannot be set, describe the prerequisite on the card and
  report that limitation.
- When a finding informs a decision or parallel work needs coordination, add
  a contextual reference only if it explains an action or coordination need.
  Independent work needs no link.

In a synthetic build project, #40 defines an archive format and #41 builds
its reader. The reader can start against a draft, but acceptance requires the
approved format from #40. Record that dependency on #41. An independent
typography review needs no link.
