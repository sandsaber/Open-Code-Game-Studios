# Agent Coordination Rules

1. **Vertical Delegation**: Leadership agents delegate to department leads, who
   delegate to specialists. Never skip a tier for complex decisions.
2. **Horizontal Consultation**: Agents at the same tier may consult each other
   but must not make binding decisions outside their domain.
3. **Conflict Resolution**: When two agents disagree, escalate to the shared
   parent. If no shared parent, escalate to `creative-director` for design
   conflicts or `technical-director` for technical conflicts.
4. **Change Propagation**: When a design change affects multiple domains, the
   `producer` agent coordinates the propagation.
5. **No Unilateral Cross-Domain Changes**: An agent must never modify files
   outside its designated directories without explicit delegation.

## Model Tier Assignment

Skills and agents are assigned to capability tiers based on task complexity, not
on a specific vendor's model lineup. The tier names are portable routing labels:
map them to whatever models are available in the current AI tool.

| Tier | Role | When to use |
|------|------|-------------|
| **Lightweight** | Fast, efficient model | Read-only status checks, formatting, simple lookups — no creative judgment needed |
| **Standard** | Balanced model | Implementation, design authoring, analysis of individual systems — default for most work |
| **Leader** | Most capable model | Multi-document synthesis, high-stakes phase gate verdicts, cross-system holistic review |

Concrete model names in tool-specific files are adapter defaults only. For
example, Claude Code can map Lightweight = Haiku, Standard = Sonnet, and
Leader = Opus. OpenAI, Gemini, local models, or future providers should map
their available models to the same three tiers by capability, context window,
latency, cost, and reliability.

Recommended mapping rules:

- Use **Lightweight** for deterministic, low-risk tasks where speed and cost
  matter more than reasoning depth.
- Use **Standard** for normal production work that requires coherent reasoning
  but does not need broad synthesis.
- Use **Leader** when mistakes are expensive, the task spans many documents or
  systems, or the output becomes a binding project decision.
- If a provider has only one usable model, map it to **Standard** and manually
  escalate critical work to the strongest available configuration.
- If a provider has more than three useful models, map extra models to the
  nearest tier rather than adding new project-wide tier names.

Skills with `model: lightweight`: `/help`, `/sprint-status`, `/story-readiness`, `/scope-check`,
`/project-stage-detect`, `/token-optimize`, `/changelog`, `/patch-notes`, `/onboard`

Skills with `model: leader`: `/review-all-gdds`, `/architecture-review`, `/gate-check`

All other skills default to Standard. When creating new skills, assign Lightweight if the
skill only reads and formats; assign Leader if it must synthesize 5+ documents with
high-stakes output; otherwise leave unset (Standard).

## Subagents vs Agent Teams

This project uses two distinct multi-agent patterns:

### Subagents (current, always active)
Spawned via `Task` within a single AI tool session. Used by all `team-*` skills
and orchestration skills. Subagents share the session's permission context, run
sequentially or in parallel within the session, and return results to the parent.

**When to spawn in parallel**: If two subagents' inputs are independent (neither
needs the other's output to begin), spawn both Task calls simultaneously rather
than waiting. Example: `/review-all-gdds` Phase 1 (consistency) and Phase 2
(design theory) are independent — spawn both at the same time.

### Agent Teams (experimental — opt-in)
Multiple independent AI tool *sessions* running simultaneously, coordinated
via a shared task list. Each session has its own context window and token budget.
Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` environment variable (Claude Code only).

**Use agent teams when**:
- Work spans multiple subsystems that will not touch the same files
- Each workstream would take >30 minutes and benefits from true parallelism
- A senior agent (technical-director, producer) needs to coordinate 3+ specialist
  sessions working on different epics simultaneously

**Do not use agent teams when**:
- One session's output is required as input for another (use sequential subagents)
- The task fits in a single session's context (use subagents instead)
- Cost is a concern — each team member burns tokens independently

**Current status**: Not yet used in this project. Document usage here when first adopted.

## Parallel Task Protocol

When an orchestration skill spawns multiple independent agents:

1. Issue all independent Task calls before waiting for any result
2. Collect all results before proceeding to dependent phases
3. If any agent is BLOCKED, surface it immediately — do not silently skip
4. Always produce a partial report if some agents complete and others block

## Agent Memory

Some agents declare `memory: project` or `memory: user` in their frontmatter.
When such an agent has cross-session knowledge worth preserving (canonical
file paths, conventions it has converged on, recurring patterns), it writes
to `.claude/agent-memory/<agent-name>/MEMORY.md` (project-scoped) or to the
tool's user-scoped memory location.

Rules:

- The directory `.claude/agent-memory/<agent-name>/` is created on demand the
  first time an agent has something durable to record. Agents without a
  matching directory have simply never needed to write memory.
- Project-scoped memory (`.claude/agent-memory/`) is committed and shared by
  the whole team. Treat entries like documentation: precise, dated when
  relevant, and pruned when stale.
- User-scoped memory is private to each contributor's tool installation and
  not committed.
- Other AI tools that do not support an agent-memory subsystem natively
  should read these files when emulating the corresponding role.
- Memory is NOT a substitute for files in `docs/` or `design/`. If a
  decision belongs in an ADR or GDD, write it there — memory is only for
  agent-internal working notes.
