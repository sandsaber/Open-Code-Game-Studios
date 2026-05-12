# AI Game Studios — Claude Code Entry Point

This file exists because Claude Code auto-loads `CLAUDE.md`. The authoritative,
tool-agnostic project configuration lives in `AGENTS.md` — read it before doing
any work. Everything in this file is Claude-Code-specific.

@AGENTS.md

## Claude-Code-specific notes

- `@`-prefixed paths above are auto-expanded by Claude Code — the referenced
  files are loaded into context automatically. Other AI tools must read them
  manually.
- Slash commands map to `.claude/skills/[name]/SKILL.md`. Use them natively.
- Hooks live in `.claude/hooks/`. The `SessionStart` hooks print a context
  banner and detect documentation gaps; do not duplicate that work in chat.
- Subagents are real (`Task` tool). Spawn them per the routing in
  `.claude/docs/agent-roster.md`.
- Status line script: `.claude/statusline.sh`.

## Onboarding

> **First session in a new game project?** If the engine is not configured and
> no game concept exists, run `/start` for the guided onboarding flow. (This
> does not apply to the framework repo itself — the `SessionStart` hook will
> detect framework-development mode and skip the prompt.)
