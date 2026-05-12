# Context Management

Context is the most critical resource in an AI tool session. Manage it actively.

## File-Backed State (Primary Strategy)

**The file is the memory, not the conversation.** Conversations are ephemeral and
will be compacted or lost. Files on disk persist across compactions and session crashes.

### Session State File

Maintain `production/session-state/active.md` as a living checkpoint. Update it
after each significant milestone:

- Design section approved and written to file
- Architecture decision made
- Implementation milestone reached
- Test results obtained

The state file should contain: current task, progress checklist, key decisions
made, files being worked on, and open questions.

### Status Line Block (Production+ only)

When the project is in Production, Polish, or Release stage, include a structured
status block in `active.md` that the status line script can parse:

```markdown
<!-- STATUS -->
Epic: Combat System
Feature: Melee Combat
Task: Implement hitbox detection
<!-- /STATUS -->
```

- All three fields (Epic, Feature, Task) are optional — include only what applies
- Update this block when switching focus areas
- The status line displays it as a breadcrumb: `Combat System > Melee Combat > Hitboxes`
- Remove or empty the block when no active work focus exists

After any disruption (compaction, crash, `/clear`), read the state file first.

### Incremental File Writing

When creating multi-section documents (design docs, architecture docs, lore entries):

1. Create the file immediately with a skeleton (all section headers, empty bodies)
2. Discuss and draft one section at a time in conversation
3. Write each section to the file as soon as it's approved
4. Update the session state file after each section
5. After writing a section, previous discussion about that section can be safely
   compacted — the decisions are in the file

This keeps the context window holding only the *current* section's discussion
(~3-5k tokens) instead of the entire document's conversation history (~30-50k tokens).

## Proactive Compaction

- **Compact proactively** at ~60-70% context usage, not reactively at the limit
- **Use `/clear`** between unrelated tasks, or after 2+ failed correction attempts
- **Natural compaction points:** after writing a section to file, after committing,
  after completing a task, before starting a new topic
- **Focused compaction:** `/compact Focus on [current task] — sections 1-3 are
  written to file, working on section 4`

## Context Budgets by Task Type

- Light (read/review): ~3k tokens startup
- Medium (implement feature): ~8k tokens
- Heavy (multi-system refactor): ~15k tokens

## Token Optimization Policy

Token optimization is a workflow constraint, not a provider-specific feature.
Different AI tools expose different token counters, so use a practical approach:
minimize loaded context, use file and line counts as a proxy, and preserve
decisions in files instead of chat history.

### Staged Context Loading

1. **Index first**: read `AGENTS.md`, relevant manifests, registries, catalogs,
   status files, and search results before opening large source or design files.
2. **Target second**: use `rg`, `rg --files`, file globs, and headings to identify
   the smallest set of files that can answer the current question.
3. **Full read last**: read complete files only when exact wording, structure, or
   implementation details are required.
4. **Reference, don't paste**: cite file paths and line numbers instead of copying
   long blocks into the conversation.
5. **Persist decisions**: once a decision is made, write it to the appropriate
   project file after approval so future sessions can read the file instead of
   replaying the conversation.

### Token Risk Signals

Treat a task as token-sensitive when any of these are true:

- The task touches 10+ files or 3+ subsystems.
- A required file is longer than ~400 lines.
- The task requires comparing many GDDs, ADRs, stories, or agent definitions.
- The conversation already contains multiple drafts, corrections, or rejected paths.
- The next step would require spawning multiple subagents or reading generated logs.

### Optimization Techniques

- Use `/token-optimize [task]` before heavy reviews, multi-system refactors, or
  unfamiliar-code exploration.
- Ask subagents for concise findings with file paths, verdicts, and only the
  minimal supporting evidence.
- Summarize completed phases into `production/session-state/active.md` before
  moving to the next phase.
- Prefer structured summaries, checklists, and tables over pasted source content.
- Compact at natural boundaries and explicitly state which files now contain the
  durable record.

### Optimized Output Shape

Long-running skills and agents should return:

- Current task and verdict
- Files read and why
- Decisions made
- Files modified or proposed
- Open questions
- Next minimal context to load

This keeps downstream work actionable without forcing later agents to reconstruct
the full conversation.

## Subagent Delegation

Use subagents for research and exploration to keep the main session clean.
Subagents run in their own context window and return only summaries:

- **Use subagents** when investigating across multiple files, exploring unfamiliar code,
  or doing research that would consume >5k tokens of file reads
- **Use direct reads** when you know exactly which 1-2 files to check
- Subagents do not inherit conversation history — provide full context in the prompt

## Compaction Instructions

When context is compacted, preserve the following in the summary:

- Reference to `production/session-state/active.md` (read it to recover state)
- List of files modified in this session and their purpose
- Any architectural decisions made and their rationale
- Active sprint tasks and their current status
- Agent invocations and their outcomes (success/failure/blocked)
- Test results (pass/fail counts, specific failures)
- Unresolved blockers or questions awaiting user input
- The current task and what step we are on
- Which sections of the current document are written to file vs. still in progress

**After compaction:** Read `production/session-state/active.md` and any files being
actively worked on to recover full context. The files contain the decisions; the
conversation history is secondary.

## Recovery After Session Crash

If a session dies ("prompt too long") or you start a new session to continue work:

1. The `session-start.sh` hook will detect and preview `active.md` automatically
2. Read the full state file for context
3. Read the partially-completed file(s) listed in the state
4. Continue from the next incomplete section or task
