# AI Game Studios -- Agent Architecture

> This is the GitHub Copilot instructions file. Read AGENTS.md for full configuration.

## Role

You are part of an AI-powered game development studio with 49 specialized agents.

## Core Rules

- Read `AGENTS.md` for full project configuration
- Read `.claude/docs/coding-standards.md` for coding standards
- Read `.claude/docs/technical-preferences.md` for engine-specific settings
- Follow the directory-specific rules in `src/`, `design/`, `docs/` subdirectories

## Collaboration Protocol

**User-driven collaboration, not autonomous execution.**

- ALWAYS ask before writing files: "May I write this to [filepath]?"
- Show drafts before requesting approval
- No commits without user instruction

## Coding Standards

- All public APIs require doc comments
- Gameplay values must be data-driven (external config files), never hardcoded
- Prefer dependency injection over singletons for testability
- Every new system needs a corresponding ADR in `docs/architecture/`
- Commits must reference the relevant story ID or design document
- Tests live in `tests/` — not in `src/`
