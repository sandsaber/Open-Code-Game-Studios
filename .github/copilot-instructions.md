# AI Game Studios — GitHub Copilot Entry Point

GitHub Copilot reads this file as workspace instructions. The authoritative,
tool-agnostic configuration lives in `AGENTS.md` — read it first and follow
every rule it specifies.

## What you must read on startup

1. `AGENTS.md` — full project configuration (read this first)
2. `.claude/docs/coding-standards.md` — code and design doc standards
3. `.claude/docs/technical-preferences.md` — engine-specific settings
4. `.claude/docs/coordination-rules.md` — agent coordination rules
5. `.claude/docs/agent-roster.md` — to choose the right role for a task

Copilot does not expand `@`-prefixed file references — read them manually
when `AGENTS.md` includes them.

## Copilot-specific notes

- Slash commands listed in `AGENTS.md` map to `.claude/skills/[name]/SKILL.md`.
  When the user invokes one, read that file and follow its workflow.
- Agent names listed in `AGENTS.md` map to `.claude/agents/[name].md`.
  Emulate the role manually — do not claim to spawn a subagent.
- Follow the collaboration protocol from `AGENTS.md`: ask before writing files,
  show drafts before approval, no commits without instruction.
- Follow directory-specific rules where they exist (`src/`, `design/`, `docs/`).
