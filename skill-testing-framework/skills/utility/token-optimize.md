# Skill Test Spec: /token-optimize

## Skill Summary

`/token-optimize` builds a token-efficient context loading plan for a requested
task. It runs on the Lightweight model, reads only indexes and targeted metadata
first, classifies token risk, and returns an optimized read plan, delegation
plan, compaction plan, and next minimal step.

The skill is read-only. It writes no files, invokes no director gates, and uses
file count plus line count as provider-agnostic proxies instead of depending on
a specific tool's token counter.

---

## Static Assertions (Structural)

Verified automatically by `/skill-test static` — no fixture needed.

- [ ] Has required frontmatter fields: `name`, `description`, `argument-hint`, `user-invocable`, `allowed-tools`
- [ ] Has >=2 phase headings
- [ ] Contains verdict keyword: TOKEN OPTIMIZATION COMPLETE
- [ ] Does NOT contain "May I write" language (skill is read-only)
- [ ] Has a next-step handoff section

---

## Director Gate Checks

None. `/token-optimize` is a read-only planning skill. No director gates apply.

---

## Test Cases

### Case 1: Happy Path — Feature implementation planning

**Fixture:**
- `AGENTS.md` exists
- `.claude/docs/context-management.md` exists
- `src/gameplay/combat/` contains several files
- `design/gdd/combat-system.md` exists

**Input:** `/token-optimize implement combat hit reactions`

**Expected behavior:**
1. Skill defines the task boundary as combat implementation planning
2. Skill uses search and file inventory before full file reads
3. Skill identifies likely design and code files
4. Skill classifies token risk as MEDIUM or HIGH depending on file count
5. Skill returns must-read, conditional-read, avoid-loading, and search-query sections
6. Verdict is TOKEN OPTIMIZATION COMPLETE

**Assertions:**
- [ ] Task boundary is clear and scoped
- [ ] Read plan prioritizes indexes/search before full reads
- [ ] Token risk is explicitly classified
- [ ] Next minimal step is actionable
- [ ] No files are written

---

### Case 2: Broad Task — Full project review

**Fixture:**
- Multiple GDDs exist under `design/gdd/`
- Multiple ADRs exist under `docs/architecture/`
- Multiple stories exist under `production/epics/`

**Input:** `/token-optimize review the whole project`

**Expected behavior:**
1. Skill detects broad scope and high token risk
2. Skill recommends reading indexes and manifests first
3. Skill avoids loading all GDDs, ADRs, and stories initially
4. Skill recommends subagent delegation or phased review
5. Skill includes a compaction/checkpoint plan

**Assertions:**
- [ ] Risk is HIGH or CRITICAL
- [ ] Full-file loading is deferred
- [ ] Delegation plan is present
- [ ] Compaction plan is present
- [ ] No files are written

---

### Case 3: Missing Argument — Generic optimization plan

**Fixture:**
- Normal project files exist
- No task argument is provided

**Input:** `/token-optimize`

**Expected behavior:**
1. Skill does not block on clarification
2. Skill returns a generic token optimization plan
3. Skill recommends using `AGENTS.md`, context-management docs, and active session state first
4. Skill provides a reusable next minimal step

**Assertions:**
- [ ] No clarification is required before output
- [ ] Generic read plan is useful
- [ ] Verdict is TOKEN OPTIMIZATION COMPLETE
- [ ] No files are written

---

### Case 4: Long File Risk — Large markdown or source file

**Fixture:**
- A candidate file has more than 400 lines
- The task mentions that file or its subsystem

**Input:** `/token-optimize review docs/large-design.md`

**Expected behavior:**
1. Skill flags the file as token-sensitive based on line count
2. Skill recommends heading scan or targeted search before full read
3. Skill reads full content only if exact details are required

**Assertions:**
- [ ] Large-file risk is mentioned
- [ ] Headings/search mode is recommended
- [ ] Full read is conditional
- [ ] No files are written

---

### Case 5: OpenCode Context — Adapter-aware note

**Fixture:**
- User mentions OpenCode or `opencode`
- `AGENTS.md` exists
- No `.opencode/` adapter exists

**Input:** `/token-optimize opencode session for architecture review`

**Expected behavior:**
1. Skill keeps `AGENTS.md` as the authoritative universal policy
2. Skill may recommend OpenCode context pruning or project-level OpenCode config
3. Skill does not invent adapter files or claim OpenCode-specific support exists

**Assertions:**
- [ ] OpenCode note is accurate and optional
- [ ] Universal policy remains authoritative
- [ ] No files are written

---

## Test Coverage Notes

- Behavioral tests should verify that the skill remains read-only.
- Static tests should verify the verdict keyword and handoff section.
- OpenCode-specific guidance must stay optional unless the project contains an
  `.opencode/` adapter.
