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
