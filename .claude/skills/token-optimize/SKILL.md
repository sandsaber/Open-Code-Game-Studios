---
name: token-optimize
description: "Build a token-efficient context loading plan for a task. Use before heavy reviews, multi-system refactors, unfamiliar-code exploration, long design sessions, or any task likely to exceed the current context budget."
argument-hint: "[task description, file path, feature name, or workflow command]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash
model: haiku
---

# Token Optimization

This skill is read-only. It produces a compact read plan, context budget, and
compaction strategy. It does not modify files.

Use this before expensive tasks such as:
- Cross-document reviews
- Multi-system implementation
- Large refactors
- Brownfield adoption
- Long design authoring sessions
- Debugging across unfamiliar subsystems

**Argument:** `$ARGUMENTS[0]` — task description, target file, feature name, or
workflow command.

---

## Phase 1: Define the Task Boundary

Identify the smallest useful scope for the requested work:

- Restate the task in one sentence.
- Identify the likely domain: design, architecture, code, QA, release, or mixed.
- Identify whether the task is read-only, authoring, implementation, review, or orchestration.
- If the argument is missing or too broad, produce a generic optimization plan
  instead of asking for clarification.

Do not load broad context yet. Start with indexes and metadata.

---

## Phase 2: Inventory Available Context

Use low-cost discovery before reading full files:

- Read `AGENTS.md` for universal project rules.
- Read `.claude/docs/context-management.md` for context policy.
- Check `production/session-state/active.md` if it exists.
- Use `rg --files` or `Glob` to locate relevant files.
- Use targeted `Grep` for feature names, command names, system names, ADR IDs,
  GDD titles, or file path fragments.
- Use `wc -l` or equivalent line counts for candidate large files.

Prefer summaries and indexes when available:

- `design/gdd/systems-index.md`
- `docs/architecture/control-manifest.md`
- `docs/architecture/architecture.md`
- `.claude/docs/workflow-catalog.yaml`
- sprint, epic, or story indexes under `production/`

---

## Phase 3: Classify Token Risk

Assign a token risk level:

| Risk | Signals |
|------|---------|
| **LOW** | 1-3 files, clear target, no cross-system synthesis |
| **MEDIUM** | 4-10 files, one subsystem, some design/code comparison |
| **HIGH** | 10+ files, 3+ subsystems, many GDDs/ADRs/stories, or multi-agent workflow |
| **CRITICAL** | Full-project audit, broad brownfield adoption, large logs, or repeated failed attempts |

Use file count and line count as a provider-agnostic proxy. Do not depend on a
specific tool's token counter.

---

## Phase 4: Build the Optimized Read Plan

Produce a read plan with four groups:

````markdown
## Optimized Read Plan

### Must Read First
| File | Why | Read Mode |
|------|-----|-----------|
| [path] | [reason] | Full / Headings / Search hits |

### Read Only If Needed
| File | Trigger |
|------|---------|
| [path] | [condition that makes it necessary] |

### Avoid Loading Initially
| File/Pattern | Reason |
|--------------|--------|
| [path or glob] | [large, generated, irrelevant, or superseded] |

### Search Queries
```bash
rg -n "[pattern]" [path]
rg --files [path]
```
````

Use "Headings" for long markdown files where section titles are enough to plan.
Use "Search hits" when exact references can answer the question without reading
the full file.

---

## Phase 5: Plan Delegation and Compaction

If the task is MEDIUM or higher, recommend how to keep the main session clean:

- Which subagent or specialist should receive a compact prompt, if any.
- Which independent searches can run in parallel.
- What each subagent must return: verdict, file paths, line references, risks,
  and next action.
- When to update `production/session-state/active.md`.
- When to compact or clear context.

For OpenCode sessions, include an optional note if relevant:

> If using OpenCode, consider pairing this workflow with a context pruning plugin
> or project-level OpenCode configuration. Keep `AGENTS.md` as the authoritative
> universal policy unless an `.opencode/` adapter exists.

---

## Phase 6: Output the Report

Return a concise report:

```markdown
# Token Optimization Plan: [Task]

**Verdict**: TOKEN OPTIMIZATION COMPLETE
**Risk**: LOW / MEDIUM / HIGH / CRITICAL
**Estimated startup context**: [~N files, rough token class]
**Recommended model tier**: Lightweight / Standard / Leader

## Task Boundary
[One-sentence scope]

## Optimized Read Plan
[Tables from Phase 4]

## Delegation Plan
[Subagents or none]

## Compaction Plan
[When to checkpoint, compact, or clear]

## Next Minimal Step
[The first command/read/action to take]
```

Always include the verdict phrase `TOKEN OPTIMIZATION COMPLETE`.

---

## Handoff

End with one of these:

- "Proceed with the Next Minimal Step above."
- "Run the target workflow after loading only the Must Read First files."
- "Use this plan as the prompt boundary for the next agent or session."
