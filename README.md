<p align="center">
  <h1 align="center">AI Game Studios</h1>
  <p align="center">
    Turn any AI coding tool into a coordinated game development studio.
    <br />
    49 agents · 73 skills · one shared process.
  </p>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href=".claude/agents"><img src="https://img.shields.io/badge/agents-49-blueviolet" alt="49 Agents"></a>
  <a href=".claude/skills"><img src="https://img.shields.io/badge/skills-73-green" alt="73 Skills"></a>
  <a href=".claude/hooks"><img src="https://img.shields.io/badge/hooks-12-orange" alt="12 Hooks"></a>
  <a href=".claude/rules"><img src="https://img.shields.io/badge/rules-11-red" alt="11 Rules"></a>
</p>

<p align="center">
  <img src="docs/assets/ai-game-studios-hero.png" alt="AI Game Studios coordinated game development workspace" width="100%">
</p>

---

## What this is

AI coding tools are good at writing code, less good at running a whole game
project. A real game needs design decisions, technical constraints, QA,
production planning, engine-specific knowledge, asset pipelines, and a way
to keep all of that consistent across many sessions.

**AI Game Studios** is a template that gives your AI tool the structure of a
real studio: directors, department leads, specialists, engine experts, QA,
production, and operations. **You** stay in charge — the framework just
makes sure the right specialist asks the right question at the right
checkpoint.

The same project can move between AI tools without losing its process.
`AGENTS.md` is the universal source of truth; every tool reads it through
its own adapter.

---

## Quick Start

```bash
git clone https://github.com/sandsaber/Open-Code-Game-Studios.git my-game
cd my-game
```

Open the project in your AI tool — each tool finds its own entry point:

| Tool | Opens | Run |
|------|-------|-----|
| Claude Code | `CLAUDE.md` | `claude` |
| Codex CLI | `AGENTS.md` | `codex` |
| Gemini CLI | `AGENTS.md` | `gemini` |
| OpenCode CLI | `opencode.json` + `AGENTS.md` | `opencode` |
| Cursor | `.cursorrules` | Open the folder |
| Windsurf | `.windsurfrules` | Open the folder |
| GitHub Copilot | `.github/copilot-instructions.md` | Open in VS Code |
| Aider | `.aider.conf.yml` | `aider` |
| Any other tool | `AGENTS.md` | Point it at the file |

Then start designing. If you're using Claude Code, type `/start` for guided
onboarding. For any other tool, ask: *"I want to start a new game project —
walk me through the onboarding from `.claude/skills/start/SKILL.md`."*

> **Prerequisites:** Git, plus an AI coding tool. Optional but recommended:
> [`jq`](https://jqlang.github.io/jq/) and Python 3 (used by hook
> validation; hooks degrade gracefully without them).

---

## Supported AI Tools

| Tool | Adapter | Notes |
|------|---------|-------|
| Claude Code | `CLAUDE.md` + `.claude/` | Full support: hooks, slash skills, subagents |
| Codex CLI | `AGENTS.md` | Universal config; manual skill/agent routing |
| Gemini CLI | `AGENTS.md` | Universal config; manual skill/agent routing |
| OpenCode CLI | `opencode.json` + `.opencode/` | Native commands route into shared skills |
| Cursor | `.cursorrules` | Agents + coordination rules |
| GitHub Copilot | `.github/copilot-instructions.md` | Coding standards + collaboration protocol |
| Windsurf / Codeium | `.windsurfrules` | Agents + coordination rules |
| Aider | `.aider.conf.yml` | Auto-loads `AGENTS.md` via `read:` |
| Anything else | `AGENTS.md` | Universal entry point |

Slash commands work even on tools without native command support — they map
1:1 to `.claude/skills/<name>/SKILL.md`. For example, `/token-optimize
combat` means: *read `.claude/skills/token-optimize/SKILL.md` and run that
workflow with `combat` as the argument.*

---

## What's Included

| Category | Count | Purpose |
|----------|-------|---------|
| Agents | 49 | Specialists across design, programming, art, audio, narrative, QA, production |
| Skills | 73 | Slash commands for every workflow phase (`/start`, `/design-system`, `/dev-story`, `/story-done`, …) |
| Hooks | 12 | Auto-validation on commit, push, asset write, session lifecycle (Claude Code only) |
| Rules | 11 | Path-scoped coding standards for `src/`, `design/`, `tests/`, etc |
| Templates | 39 | GDDs, ADRs, sprint plans, HUD specs, accessibility checklists, and more |

### The studio

Agents are organized into three tiers — the higher the tier, the heavier the
model and the broader the scope:

- **Tier 1 — Directors** (`creative-director`, `technical-director`,
  `producer`) — vision, architecture, scheduling.
- **Tier 2 — Department Leads** (`game-designer`, `lead-programmer`,
  `art-director`, `audio-director`, `narrative-director`, `qa-lead`,
  `release-manager`, `localization-lead`).
- **Tier 3 — Specialists** (gameplay/engine/AI/network/tools/UI programmers,
  systems/level/economy/UX designers, technical artist, sound designer,
  writer, world-builder, performance/security/devops/analytics engineers,
  QA tester, accessibility specialist, live-ops, community, prototyper).

Plus engine-specific sub-specialists you can swap in based on your stack:

| Engine | Lead | Sub-specialists |
|--------|------|-----------------|
| Godot 4 | `godot-specialist` | GDScript, Shaders, GDExtension |
| Unity | `unity-specialist` | DOTS/ECS, Shaders/VFX, Addressables, UI Toolkit |
| Unreal Engine 5 | `unreal-specialist` | GAS, Blueprints, Replication, UMG/CommonUI |

Full roster: [`.claude/docs/agent-roster.md`](.claude/docs/agent-roster.md).

---

## How It Works

Five ideas hold the framework together:

1. **Vertical delegation.** Directors delegate to leads, leads to
   specialists. Conflicts escalate to the shared parent.
2. **Collaborative, not autonomous.** Every agent follows
   ask → propose options → wait for approval → draft → approve. Nothing is
   written without your sign-off.
3. **Portable model routing.** Skills request Lightweight / Standard /
   Leader capability tiers — never a specific vendor model name. Map the
   tiers to whatever your tool offers.
4. **Token budgets are explicit.** Indexes and summaries before full files;
   durable decisions written to disk; `/token-optimize` for heavy tasks.
5. **Path-scoped rules.** Coding standards activate based on file location
   (`src/gameplay/**`, `src/core/**`, `design/gdd/**`, `tests/**`, …).

Detailed walkthrough of each idea, the full Claude-Code hook table, OpenCode
adapter, and engine-MCP setup live in
[`docs/framework-architecture.md`](docs/framework-architecture.md).

---

## Project Layout

```
AGENTS.md                          # Universal entry point (all AI tools)
CLAUDE.md / .cursorrules / ...     # Thin per-tool adapters that read AGENTS.md
.claude/
  agents/                          # 49 agent definitions
  skills/                          # 73 slash commands (one folder per skill)
  hooks/                           # 12 hook scripts (Claude Code automation)
  rules/                           # 11 path-scoped coding standards
  docs/                            # Coordination rules, agent roster, templates
  statusline.sh                    # Status line: context %, model, stage, focus
skill-testing-framework/           # Optional QA layer for the framework itself
src/  assets/  design/             # Your game lives here
docs/  tests/  tools/              # Tech docs, ADRs, test suites, pipeline tools
prototypes/  production/           # Throwaway prototypes / sprints / milestones
```

---

## Framework Testing & CI

`skill-testing-framework/` holds behavioral specs and catalog coverage for
the framework's own skills and agents — you can ignore it if you're only
consuming the template. To work on or extend the framework:

| Command | What it does |
|---------|--------------|
| `/skill-test static all` | Structural compliance check across all skills |
| `/skill-test spec <name>` | Evaluate a skill against its behavioral spec |
| `/skill-test category <name>` | Evaluate against the category rubric |
| `/skill-test audit` | Coverage report: which specs were last run, when, with what result |
| `/skill-improve <name>` | Test → diagnose → propose fix → rewrite → retest loop |

Static linting also runs in CI on every PR:

- [`tools/lint-skills.py`](tools/lint-skills.py) — frontmatter, tool
  mapping, catalog cross-check (`.github/workflows/skill-lint.yml`).
- `shellcheck` on every hook script (`.github/workflows/shell-lint.yml`).

---

## Customization

This is a template, not a locked framework. The agent set is per-project —
delete what you don't need, add what you do. Common moves:

- Pick one engine set (Godot / Unity / Unreal) and remove the others.
- Edit agent prompts to encode project-specific knowledge.
- Add path-scoped rules in `.claude/rules/` for new directories.
- Choose review intensity per skill: `full` (all director gates),
  `lean` (phase gates only), or `solo` (no gates).

---

## Platform Support

Developed and tested on Windows 10 with Git Bash; hooks use POSIX-compatible
patterns (`grep -E`, not `grep -P`) and degrade gracefully when optional
tools are missing. Works on macOS and Linux without modification.

---

## Further Reading

- [`docs/framework-architecture.md`](docs/framework-architecture.md) — how
  coordination, model routing, hooks, and tool adapters actually work.
- [`docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`](docs/COLLABORATIVE-DESIGN-PRINCIPLE.md)
  — the protocol every agent follows, with examples.
- [`docs/WORKFLOW-GUIDE.md`](docs/WORKFLOW-GUIDE.md) — full 7-phase
  development pipeline from concept to release.
- [`UPGRADING.md`](UPGRADING.md) — migration notes between framework
  versions.

---

## Credits & Original Author

This repository is a **fork** of
[AI Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) by
[**Donchitos**](https://github.com/Donchitos), who built the original
49-agent / 73-skill / 12-hook framework. The work in this fork (universal
tool adapters, additional CI, framework hardening) sits on top of that
foundation.

If the original framework saved you time, the most direct way to support
its continued development is to thank Donchitos:

<p>
  <a href="https://www.buymeacoffee.com/donchitos3"><img src="https://img.shields.io/badge/Buy%20Donchitos%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"></a>
  &nbsp;
  <a href="https://github.com/sponsors/Donchitos"><img src="https://img.shields.io/badge/Sponsor%20Donchitos-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white" alt="GitHub Sponsors"></a>
</p>

Upstream community discussions live at the
[original repo](https://github.com/Donchitos/Claude-Code-Game-Studios/discussions).

---

## License

MIT. Original work © 2026 Donchitos; fork modifications © 2026 sandsaber.
See [LICENSE](LICENSE) for the full text.
