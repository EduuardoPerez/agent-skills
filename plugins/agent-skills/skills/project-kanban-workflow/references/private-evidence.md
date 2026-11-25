# Private evidence and the handoff index

Use a private handoff index supplied for the session or configured through
`context.handoff_index_path`, relative to the profile directory. Look up a
card by its qualified issue reference or stable item URL. Each entry points
to a local artifact or section and says which question it answers and where
its evidence ends. Reuse entries when updating the index.

Before writing an index in a repository, verify its file is **both Git-ignored
and untracked**. A shared profile may name a generic relative index path.
Supply sensitive locations privately and keep them out of public cards. If
the index or artifact is unavailable, begin with the public summary and ask
privately for the specific evidence only when an open decision requires it.
