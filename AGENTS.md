# AI Game Studios -- Game Studio Agent Architecture

Indie game development managed through coordinated AI subagents.
Each agent owns a specific domain, enforcing separation of concerns and quality.

## Technology Stack

- **Engine**: [CHOOSE: Godot 4 / Unity / Unreal Engine 5]
- **Language**: [CHOOSE: GDScript / C# / C++ / Blueprint]
- **Version Control**: Git with trunk-based development
- **Build System**: [SPECIFY after choosing engine]
- **Asset Pipeline**: [SPECIFY after choosing engine]

> **Note**: Engine-specialist agents exist for Godot, Unity, and Unreal with
> dedicated sub-specialists. Use the set matching your engine.

## Project Structure

@.claude/docs/directory-structure.md

## Engine Version Reference

@docs/engine-reference/godot/VERSION.md

## Technical Preferences

@.claude/docs/technical-preferences.md

## Coordination Rules

@.claude/docs/coordination-rules.md

## Universal Reference Loading

Lines beginning with `@` are file references. AI tools that do not expand these
references automatically MUST read the referenced file before relying on that
section.

Required startup references:

- `.claude/docs/directory-structure.md`
- `.claude/docs/technical-preferences.md`
- `.claude/docs/coordination-rules.md`
- `.claude/docs/coding-standards.md`
- `.claude/docs/context-management.md`

Read additional referenced files only when relevant to the current task.

## Universal Skill Routing

Slash commands are portable workflow names, not only Claude Code commands.
If the current AI tool does not provide native slash-command support, route them
manually:

1. Convert `/skill-name [arguments]` to `.claude/skills/skill-name/SKILL.md`.
2. Read that `SKILL.md`.
3. Follow its workflow using the current tool's available file, shell, and edit
   capabilities.
4. Preserve the collaboration protocol: show drafts or summaries and ask before
   writing files.

Examples:

- `/start` -> `.claude/skills/start/SKILL.md`
- `/help` -> `.claude/skills/help/SKILL.md`
- `/token-optimize [task]` -> `.claude/skills/token-optimize/SKILL.md`
- `/run-skill [name]` -> read `.claude/skills/[name]/SKILL.md`

If a skill references Claude-only tools such as `AskUserQuestion`, replace them
with a concise plain-text question and wait for the user's decision. The full
mapping table is below — every Claude-specific tool name that appears in any
`allowed-tools` field MUST have an entry here.

## Universal Tool Mapping

The following tool names appear in skill `allowed-tools` declarations. The
left column is the canonical (Claude Code) name. Other AI tools should
substitute the equivalent in the right column. The linter
(`tools/lint-skills.py`) enforces that every tool referenced in any skill is
either in the universal set OR present in this mapping.

### Universal tools (every major AI tool has an equivalent)

| Canonical name | Meaning |
|----------------|---------|
| `Read` | Read a file from the filesystem. |
| `Write` | Create or overwrite a file. |
| `Edit` | Make a targeted edit inside an existing file. |
| `Glob` | List files matching a path pattern. |
| `Grep` | Search file contents by regex/pattern. |
| `Bash` | Run a shell command. |
| `WebFetch` | Fetch the contents of a URL. |
| `WebSearch` | Perform a web search and return summarized results. |

### Claude-specific tools (require explicit emulation in other tools)

| Canonical name | Meaning | Emulation in other tools |
|----------------|---------|--------------------------|
| `AskUserQuestion` | Present 2–4 labeled options to the user and wait for a selection. | Ask the question as plain text, list the options inline, wait for the user's reply. |
| `Task` | Spawn a subagent of a given type to handle a delegated task. | Read the referenced agent's `.claude/agents/<name>.md`, emulate its role yourself, summarize findings before moving on. Do not claim a subagent was spawned. |
| `TodoWrite` | Maintain an internal task tracker visible to the user. | Maintain the task list in your own working notes; surface it in conversation when the user asks for status. |

When adding a new tool to any skill's `allowed-tools`, either confirm it is
universal (and add it to the universal table) or add a row to the
Claude-specific table with explicit emulation guidance. The linter will fail
the build if a skill references a name that is in neither table.

## Universal Agent Routing

Agent names are portable roles. If the current AI tool does not provide native
subagent support, emulate the role manually:

1. Read `.claude/docs/agent-roster.md` to choose the right agent.
2. Read `.claude/agents/[agent-name].md`.
3. Apply that agent's domain rules, escalation path, and output format.
4. For multi-agent workflows, run each role sequentially unless the current tool
   supports parallel subagents.
5. Summarize each role's findings before moving to the next role.

Do not claim that a subagent was spawned unless the tool actually supports
subagent execution.

## Model Routing

This project does not require specific vendor model names. It uses capability
tiers so the same studio architecture can run on Claude, OpenAI, Gemini, local
models, or any future AI coding tool.

- **Lightweight**: fastest reliable model for read-only or formatting work.
- **Standard**: balanced model for implementation, design authoring, and focused analysis.
- **Leader**: strongest available model for synthesis, high-risk decisions, and cross-system review.

Tool-specific files may contain concrete model names as adapter defaults. Treat
those names as examples for that tool, not as project requirements.

## Token Optimization

Treat tokens as a limited engineering resource. Load only the context needed for
the current decision, keep durable state in files, and prefer references or
summaries over pasting large content into the conversation.

- Start with manifests, indexes, search results, and summaries before full files.
- Read full files only when the task requires exact details.
- Use targeted search before broad exploration.
- Keep long-running decisions in project files, not only in chat history.
- Pass compact prompts to subagents and require concise result summaries.
- Prefer file paths and line references over copying large blocks of text.
- Compact or clear context after natural milestones before starting unrelated work.

For large or ambiguous tasks, run `/token-optimize [task]` first to produce a
read plan, context budget, and compaction strategy.

## Collaboration Protocol

**User-driven collaboration, not autonomous execution.**
Every task follows: **Question -> Options -> Decision -> Draft -> Approval**

- Agents MUST ask "May I write this to [filepath]?" before using Write/Edit tools
- Agents MUST show drafts or summaries before requesting approval
- Multi-file changes require explicit approval for the full changeset
- No commits without user instruction

See `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md` for full protocol and examples.

> **First session?** If the project has no engine configured and no game concept,
> run `/start` to begin the guided onboarding flow.

## Coding Standards

@.claude/docs/coding-standards.md

## Context Management

@.claude/docs/context-management.md
