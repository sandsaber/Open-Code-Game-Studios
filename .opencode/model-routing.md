# OpenCode Model Routing

AI Game Studios uses capability tiers instead of fixed vendor model names.
OpenCode can run those tiers on any configured provider.

| Studio Tier | OpenCode Session Use | Typical Command |
|-------------|----------------------|-----------------|
| Lightweight | Status checks, formatting, simple read-only scans | `opencode -m <fast-model>` |
| Standard | Default implementation, design authoring, focused review | `opencode -m <balanced-model>` |
| Leader | Phase gates, architecture, cross-system synthesis, high-risk decisions | `opencode -m <strongest-model>` |

## Mapping Rules

- Set your default OpenCode session model to the tier of work you expect to do.
- Use Standard for normal development if unsure.
- Start a Leader session for project-wide architecture, phase gates, or multi-document synthesis.
- Start a Lightweight session for maintenance, status checks, changelogs, and short read-only tasks.
- If you only have one reliable OpenCode model configured, treat it as Standard
  and manually switch to your strongest available configuration for Leader work.

## Provider Examples

OpenCode model IDs are provider-specific. Examples:

```bash
opencode -m anthropic/claude-sonnet-4-5
opencode -m openai/gpt-4o
opencode -m google/gemini-2.5-pro
opencode -m ollama/qwen2.5-coder
```

Use `opencode models` to inspect the models available in your local setup.
