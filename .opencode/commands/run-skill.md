---
description: Route to an existing AI Game Studios skill by name
---

Run an existing AI Game Studios skill.

Read and follow:
- @AGENTS.md
- @.claude/docs/context-management.md
- @.claude/docs/skills-reference.md

Requested skill and arguments: $ARGUMENTS

Locate the matching skill file under `.claude/skills/[skill-name]/SKILL.md`,
read that file, and execute its workflow. If the requested skill is ambiguous,
list the closest matching skill names and ask the user to choose one.

Follow the collaboration protocol. Do not write files unless the selected skill
asks for approval and the user explicitly approves the write.
