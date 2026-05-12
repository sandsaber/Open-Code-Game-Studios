# OpenCode Adapter

This directory is a thin OpenCode adapter for AI Game Studios.

`AGENTS.md` remains the authoritative, tool-agnostic project configuration. The
OpenCode files here provide project-local commands and guidance so OpenCode can
route into the same agents, skills, coordination rules, and token optimization
policy without maintaining a second copy of the framework.

## Files

| Path | Purpose |
|------|---------|
| `../opencode.json` | Project-level OpenCode config. Loads `AGENTS.md` and shared policy docs as instructions. |
| `commands/` | OpenCode custom commands that route into existing `.claude/skills/*/SKILL.md` workflows. |
| `mcp-examples/` | Copyable engine MCP snippets for Unity, Godot, and Unreal Engine. |
| `model-routing.md` | OpenCode-specific model tier mapping guidance. |

## Usage

Start OpenCode from the project root:

```bash
opencode
```

Then use project commands from the OpenCode command picker:

- `/start` for guided onboarding
- `/help` for next-step guidance
- `/token-optimize` before large tasks
- `/run-skill [skill-name] [arguments]` to route to any existing skill
- `/model-routing` to choose an OpenCode model for the current task tier
- `/engine-mcp [engine]` to choose and configure an optional engine MCP adapter

## Optional Context Pruning

For long OpenCode sessions, consider installing a context pruning plugin globally
or enabling equivalent context management in your OpenCode setup. Keep
`AGENTS.md` and `.claude/docs/context-management.md` as the policy source of
truth, even when a plugin performs the mechanics.

## Engine MCP

Engine MCP servers are not enabled by default. Read `docs/mcp/engine-mcp.md`,
choose the MCP server for the configured engine, then merge the matching snippet
from `mcp-examples/` into `opencode.json`.
