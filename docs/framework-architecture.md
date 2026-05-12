# AI Game Studios — Framework Architecture

This document describes how the framework operates: agent coordination, the
collaboration protocol, model routing, token policy, tool adapters, and the
optional automation that ships with Claude Code.

Most of this content used to live in the top-level `README.md`. It was moved
here so the README can stay focused on "what is this and how do I install it"
without forcing readers through the full architecture before they decide
whether to clone the repo.

---

## Agent Coordination

Agents follow a structured delegation model:

1. **Vertical delegation** — directors delegate to leads, leads delegate to
   specialists.
2. **Horizontal consultation** — same-tier agents can consult each other but
   cannot make binding cross-domain decisions.
3. **Conflict resolution** — disagreements escalate up to the shared parent
   (`creative-director` for design, `technical-director` for technical).
4. **Change propagation** — cross-department changes are coordinated by
   `producer`.
5. **Domain boundaries** — agents do not modify files outside their domain
   without explicit delegation.

Full rules: [`.claude/docs/coordination-rules.md`](../.claude/docs/coordination-rules.md).

---

## Collaborative, Not Autonomous

The framework is **not** an auto-pilot. Every agent follows a strict
collaboration protocol:

1. **Ask** — agents ask questions before proposing solutions.
2. **Present options** — agents show 2-4 options with pros/cons.
3. **You decide** — the user always makes the call.
4. **Draft** — agents show work before finalizing.
5. **Approve** — nothing gets written without your sign-off.

You stay in control. The agents provide structure and expertise, not autonomy.

Full protocol with examples: [`docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`](COLLABORATIVE-DESIGN-PRINCIPLE.md).

---

## Model Routing

Skills and agents use portable capability tiers instead of vendor-specific
model names. This lets the same studio architecture run on Claude, OpenAI,
Gemini, local models, or future AI coding tools.

| Tier | Role | When to use |
|------|------|-------------|
| **Lightweight** | Fast, efficient model | Read-only status checks, formatting, simple lookups |
| **Standard** | Balanced model | Implementation, design authoring, analysis — default for most work |
| **Leader** | Most capable model | Multi-document synthesis, high-stakes decisions, cross-system review |

Tool-specific config may contain concrete model names as adapter defaults. For
Claude Code, these map to Haiku, Sonnet, and Opus respectively. For other
tools, assign your available models to the nearest tier based on capability,
context window, latency, cost, and reliability.

---

## Token Optimization

The framework treats tokens as a limited engineering resource. Agents start
with indexes, manifests, search results, and summaries before opening full
files; they preserve durable decisions in project files; and they prefer file
references over pasting large blocks into the conversation.

Use `/token-optimize [task]` before heavy reviews, multi-system refactors, or
unfamiliar-code exploration. It produces a read plan, context budget,
compaction strategy, and subagent prompt guidance without modifying files.

Full policy: [`.claude/docs/context-management.md`](../.claude/docs/context-management.md).

---

## OpenCode Adapter

OpenCode support is implemented as a thin adapter rather than a fork of the
framework. `opencode.json` loads `AGENTS.md` and shared policy docs as project
instructions, while `.opencode/commands/` exposes OpenCode-native commands
that route into the existing `.claude/skills/*/SKILL.md` workflows.

Start from the project root:

```bash
opencode
```

Useful OpenCode commands:

| Command | Purpose |
|---------|---------|
| `/start` | Run guided onboarding through the existing `/start` skill |
| `/help` | Show context-aware next steps |
| `/token-optimize` | Build a token-efficient read plan before a large task |
| `/run-skill [name]` | Route to any existing AI Game Studios skill |
| `/model-routing` | Pick the right Lightweight, Standard, or Leader model tier |
| `/engine-mcp` | Choose and configure an optional Unity, Godot, or Unreal MCP adapter |

For long OpenCode sessions, consider a context pruning plugin such as Dynamic
Context Pruning. Keep `AGENTS.md` as the policy source of truth and treat
plugins as implementation helpers.

---

## Engine MCP

Optional MCP adapters let AI tools inspect or control a running game editor.
They are intentionally not enabled by default.

| Engine | Recommended MCP | Notes |
|--------|-----------------|-------|
| Unity | `CoplayDev/unity-mcp` | MIT, active Unity package, HTTP or stdio transport |
| Godot | `Coding-Solo/godot-mcp` | MIT, free default, npm-based launch/run/debug loop |
| Godot advanced | `youichi-uda/godot-mcp-pro` | Paid server package, deeper editor automation; use minimal/CLI mode for OpenCode |
| Unreal Engine | `chongdashu/unreal-mcp` | Experimental UE 5.5+ plugin plus Python MCP server |

Setup snippets: [`docs/mcp/engine-mcp.md`](mcp/engine-mcp.md) and
[`.opencode/mcp-examples/`](../.opencode/mcp-examples).

---

## Automated Safety (Claude Code)

Hooks run automatically on every Claude Code session. Other AI tools get the
same agent coordination and coding standards through their config files, but
without automated hook execution.

| Hook | Trigger | What it does |
|------|---------|--------------|
| `validate-commit.sh` | PreToolUse (Bash) | Checks for hardcoded values, TODO format, JSON validity, design doc sections |
| `validate-push.sh` | PreToolUse (Bash) | Warns on pushes to protected branches |
| `validate-assets.sh` | PostToolUse (Write/Edit) | Validates naming conventions and JSON structure |
| `session-start.sh` | Session open | Shows current branch and recent commits for orientation |
| `detect-gaps.sh` | Session open | Detects fresh projects and missing design docs (skipped in framework-development mode) |
| `pre-compact.sh` | Before compaction | Preserves session progress notes |
| `post-compact.sh` | After compaction | Reminds to restore session state from `active.md` |
| `notify.sh` | Notification event | Shows Windows toast notification via PowerShell |
| `session-stop.sh` | Session close | Archives `active.md` to session log |
| `log-agent.sh` | Agent spawned | Audit trail start |
| `log-agent-stop.sh` | Agent stops | Audit trail stop |
| `validate-skill-change.sh` | PostToolUse (Write/Edit) | Advises running `/skill-test` after skill changes |

---

## Path-Scoped Rules

Coding standards are automatically enforced based on file location (Claude
Code):

| Path | Enforces |
|------|----------|
| `src/gameplay/**` | Data-driven values, delta time usage, no UI references |
| `src/core/**` | Zero allocations in hot paths, thread safety, API stability |
| `src/ai/**` | Performance budgets, debuggability, data-driven parameters |
| `src/networking/**` | Server-authoritative, versioned messages, security |
| `src/ui/**` | No game state ownership, localization-ready, accessibility |
| `design/gdd/**` | Required 8 sections, formula format, edge cases |
| `tests/**` | Test naming, coverage requirements, fixture patterns |
| `prototypes/**` | Relaxed standards, README required, hypothesis documented |
