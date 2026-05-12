#!/usr/bin/env python3
"""
AI Game Studios — Static linter for skills and agents.

Deterministic, no-LLM checks for the structural contract every skill and agent
must satisfy. Designed to run on every PR via CI so regressions like
"slash command silently broken because allowed-tools is missing" (cf. fix
9ccc544) are caught before merge.

Exit codes:
    0  no errors  (warnings allowed)
    1  one or more ERROR-level findings

Usage:
    python3 tools/lint-skills.py [--strict]

    --strict  treat warnings as errors.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "ERROR: PyYAML is required. Install with: pip install pyyaml\n"
    )
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"
CATALOG = REPO_ROOT / "skill-testing-framework" / "catalog.yaml"
AGENTS_MD = REPO_ROOT / "AGENTS.md"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# Captures tool names from a markdown table row whose first column is a
# backtick-wrapped identifier. Used to parse the "Universal Tool Mapping"
# tables in AGENTS.md.
TOOL_ROW_RE = re.compile(r"^\|\s*`([A-Za-z0-9_-]+)`\s*\|")

VALID_MODEL_NAMES = {
    # Claude Code accepted model aliases
    "haiku", "sonnet", "opus", "inherit",
    # Capability tiers (universal — see AGENTS.md "Model Routing")
    "lightweight", "standard", "leader",
}

# Authoritative lists, sourced from skill-testing-framework/templates/skill-test-spec.md
# Keep in sync if new categories or priorities are introduced.
VALID_CATALOG_CATEGORIES = {
    "gate", "review", "authoring", "readiness", "pipeline",
    "analysis", "team", "sprint", "utility",
}
VALID_CATALOG_PRIORITIES = {"critical", "high", "medium", "low"}

# Descriptions short enough to be useless or long enough to bloat tool listings
# both hurt UX. Bounds are loose — they catch obvious mistakes, not borderline cases.
DESCRIPTION_MIN_CHARS = 30
DESCRIPTION_MAX_CHARS = 600

# Skills should have at least two top-level body sections (## headings) so the
# workflow has discernible phases. Skills below this threshold are usually
# stubs that nobody finished writing.
MIN_BODY_HEADINGS = 2


@dataclass
class Findings:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def merge(self, other: "Findings") -> None:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)


def parse_tool_mapping(findings: Findings) -> set[str]:
    """Extract every tool name documented in AGENTS.md tool-mapping tables.

    Returns the union of "universal" and "Claude-specific" rows. Any tool used
    in a skill's `allowed-tools` must appear in this set, otherwise the
    universal-tool-portability promise is broken.
    """
    if not AGENTS_MD.is_file():
        findings.error(f"{AGENTS_MD.relative_to(REPO_ROOT)}: missing — cannot validate tool mapping")
        return set()

    try:
        text = AGENTS_MD.read_text(encoding="utf-8")
    except OSError as exc:
        findings.error(f"{AGENTS_MD.relative_to(REPO_ROOT)}: cannot read: {exc}")
        return set()

    if "## Universal Tool Mapping" not in text:
        findings.error(
            f"{AGENTS_MD.relative_to(REPO_ROOT)}: missing '## Universal Tool Mapping' section — "
            f"required for cross-tool portability"
        )
        return set()

    mapping_section = text.split("## Universal Tool Mapping", 1)[1]
    # Stop at the next top-level section so we don't accidentally pick up
    # backtick-wrapped names from unrelated tables.
    mapping_section = mapping_section.split("\n## ", 1)[0]

    tools: set[str] = set()
    for line in mapping_section.splitlines():
        match = TOOL_ROW_RE.match(line)
        if match:
            tools.add(match.group(1))

    if not tools:
        findings.error(
            f"{AGENTS_MD.relative_to(REPO_ROOT)}: 'Universal Tool Mapping' section contains no tool rows"
        )
    return tools


def split_tool_list(value) -> list[str]:
    """Normalize an `allowed-tools` value (string or list) to a list of names."""
    if isinstance(value, str):
        return [t.strip() for t in value.split(",") if t.strip()]
    if isinstance(value, list):
        return [str(t).strip() for t in value if str(t).strip()]
    return []


def parse_frontmatter(path: Path) -> tuple[dict | None, str | None, str]:
    """Return (frontmatter_dict, error_message, body). dict/error are exclusive."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"cannot read file: {exc}", ""

    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, "missing or malformed YAML frontmatter (must start with --- on line 1)", ""

    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, f"invalid YAML in frontmatter: {exc}", ""

    if not isinstance(data, dict):
        return None, "frontmatter did not parse to a mapping", ""

    body = text[match.end():]
    return data, None, body


def count_headings(body: str, level: int = 2) -> int:
    """Count markdown ATX headings at the given level (## for level=2)."""
    prefix = "#" * level + " "
    count = 0
    for raw in body.splitlines():
        line = raw.lstrip()
        # Skip fenced code blocks heuristically — `#` inside ```...``` should not count.
        # Cheap approach: ignore lines starting with backtick or four-space indent.
        if line.startswith(prefix) and not line.startswith("#" * (level + 1) + " "):
            count += 1
    return count


def lint_skill(skill_dir: Path, findings: Findings, seen_names: dict[str, Path],
               documented_tools: set[str]) -> None:
    expected_name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"
    rel = skill_file.relative_to(REPO_ROOT)

    if not skill_file.is_file():
        findings.error(f"{rel}: missing SKILL.md")
        return

    fm, err, body = parse_frontmatter(skill_file)
    if fm is None:
        findings.error(f"{rel}: {err}")
        return

    name = fm.get("name")
    if not name:
        findings.error(f"{rel}: frontmatter missing required field 'name'")
    elif name != expected_name:
        findings.error(
            f"{rel}: name '{name}' does not match directory '{expected_name}'"
        )
    else:
        prev = seen_names.get(name)
        if prev is not None:
            findings.error(
                f"{rel}: duplicate skill name '{name}' (also defined in {prev.relative_to(REPO_ROOT)})"
            )
        else:
            seen_names[name] = skill_file

    description = fm.get("description")
    if not description or not isinstance(description, str) or not description.strip():
        findings.error(f"{rel}: frontmatter missing required non-empty 'description'")
    else:
        d = description.strip()
        if len(d) < DESCRIPTION_MIN_CHARS:
            findings.warn(
                f"{rel}: description is only {len(d)} chars — recommended "
                f"minimum is {DESCRIPTION_MIN_CHARS}"
            )
        elif len(d) > DESCRIPTION_MAX_CHARS:
            findings.warn(
                f"{rel}: description is {len(d)} chars — recommended "
                f"maximum is {DESCRIPTION_MAX_CHARS} (long descriptions bloat tool listings)"
            )

    heading_count = count_headings(body, level=2)
    if heading_count < MIN_BODY_HEADINGS:
        findings.warn(
            f"{rel}: only {heading_count} '##' heading(s) found in skill body — "
            f"workflow should have at least {MIN_BODY_HEADINGS} phases"
        )

    # user-invocable skills are reachable as slash commands; without
    # allowed-tools, Claude Code silently strips tool access. This is the bug
    # fix from commit 9ccc544 — guard against regressions.
    user_invocable = fm.get("user-invocable")
    if user_invocable is True:
        if "allowed-tools" not in fm:
            findings.error(
                f"{rel}: user-invocable skill missing 'allowed-tools' "
                f"(slash command will fail — see commit 9ccc544)"
            )
        else:
            tools = fm["allowed-tools"]
            if not isinstance(tools, (str, list)):
                findings.error(
                    f"{rel}: 'allowed-tools' must be a comma-separated string or list, "
                    f"got {type(tools).__name__}"
                )
            else:
                tool_names = split_tool_list(tools)
                if not tool_names:
                    findings.error(f"{rel}: 'allowed-tools' is empty")
                elif documented_tools:
                    unknown = [t for t in tool_names if t not in documented_tools]
                    for t in unknown:
                        findings.error(
                            f"{rel}: 'allowed-tools' references '{t}', which is not "
                            f"documented in AGENTS.md → 'Universal Tool Mapping'. "
                            f"Add a row there before using this tool in a skill."
                        )
    elif user_invocable is None:
        findings.warn(f"{rel}: missing 'user-invocable' field (assumed false)")
    elif user_invocable is not False:
        findings.error(
            f"{rel}: 'user-invocable' must be a boolean, got {user_invocable!r}"
        )

    model = fm.get("model")
    if model is not None and model not in VALID_MODEL_NAMES:
        findings.warn(
            f"{rel}: unknown 'model' value '{model}' "
            f"(expected one of: {', '.join(sorted(VALID_MODEL_NAMES))})"
        )


def lint_agent(agent_file: Path, findings: Findings, seen_names: dict[str, Path],
               documented_tools: set[str]) -> None:
    expected_name = agent_file.stem
    rel = agent_file.relative_to(REPO_ROOT)

    fm, err, _body = parse_frontmatter(agent_file)
    if fm is None:
        findings.error(f"{rel}: {err}")
        return

    name = fm.get("name")
    if not name:
        findings.error(f"{rel}: frontmatter missing required field 'name'")
    elif name != expected_name:
        findings.error(
            f"{rel}: name '{name}' does not match filename '{expected_name}'"
        )
    else:
        prev = seen_names.get(name)
        if prev is not None:
            findings.error(
                f"{rel}: duplicate agent name '{name}' (also defined in {prev.relative_to(REPO_ROOT)})"
            )
        else:
            seen_names[name] = agent_file

    description = fm.get("description")
    if not description or not isinstance(description, str) or not description.strip():
        findings.error(f"{rel}: frontmatter missing required non-empty 'description'")
    else:
        d = description.strip()
        if len(d) < DESCRIPTION_MIN_CHARS:
            findings.warn(
                f"{rel}: description is only {len(d)} chars — recommended "
                f"minimum is {DESCRIPTION_MIN_CHARS}"
            )
        elif len(d) > DESCRIPTION_MAX_CHARS:
            findings.warn(
                f"{rel}: description is {len(d)} chars — recommended "
                f"maximum is {DESCRIPTION_MAX_CHARS}"
            )

    model = fm.get("model")
    if model is not None and model not in VALID_MODEL_NAMES:
        findings.warn(
            f"{rel}: unknown 'model' value '{model}' "
            f"(expected one of: {', '.join(sorted(VALID_MODEL_NAMES))})"
        )

    tools = fm.get("tools")
    if tools is not None:
        if not isinstance(tools, (str, list)):
            findings.error(
                f"{rel}: 'tools' must be a comma-separated string or list, "
                f"got {type(tools).__name__}"
            )
        elif documented_tools:
            tool_names = split_tool_list(tools)
            unknown = [t for t in tool_names if t not in documented_tools]
            for t in unknown:
                findings.error(
                    f"{rel}: 'tools' references '{t}', which is not documented in "
                    f"AGENTS.md → 'Universal Tool Mapping'. Add a row there before "
                    f"using this tool in an agent."
                )


def lint_catalog(skill_names: set[str], agent_names: set[str], findings: Findings) -> None:
    if not CATALOG.is_file():
        findings.warn(f"{CATALOG.relative_to(REPO_ROOT)}: catalog file missing — skipping cross-check")
        return

    try:
        catalog = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        findings.error(f"{CATALOG.relative_to(REPO_ROOT)}: invalid YAML: {exc}")
        return

    rel = CATALOG.relative_to(REPO_ROOT)
    skill_entries = [e for e in (catalog.get("skills") or []) if isinstance(e, dict)]
    agent_entries = [e for e in (catalog.get("agents") or []) if isinstance(e, dict)]
    cat_skills = {entry.get("name") for entry in skill_entries}
    cat_agents = {entry.get("name") for entry in agent_entries}

    missing_skill_files = cat_skills - skill_names - {None}
    extra_skill_files = skill_names - cat_skills
    missing_agent_files = cat_agents - agent_names - {None}
    extra_agent_files = agent_names - cat_agents

    for name in sorted(missing_skill_files):
        findings.error(f"{rel}: skill '{name}' listed in catalog but no SKILL.md found")
    for name in sorted(extra_skill_files):
        findings.warn(f"{rel}: skill '{name}' has SKILL.md but no catalog entry")
    for name in sorted(missing_agent_files):
        findings.error(f"{rel}: agent '{name}' listed in catalog but no .md file found")
    for name in sorted(extra_agent_files):
        findings.warn(f"{rel}: agent '{name}' has agent .md but no catalog entry")

    # Validate category and priority on each skill entry.
    for entry in skill_entries:
        name = entry.get("name", "<unnamed>")
        cat = entry.get("category")
        prio = entry.get("priority")
        if cat is None:
            findings.warn(f"{rel}: skill '{name}' missing 'category' field")
        elif cat not in VALID_CATALOG_CATEGORIES:
            findings.error(
                f"{rel}: skill '{name}' has invalid category '{cat}' "
                f"(must be one of: {', '.join(sorted(VALID_CATALOG_CATEGORIES))})"
            )
        if prio is None:
            findings.warn(f"{rel}: skill '{name}' missing 'priority' field")
        elif prio not in VALID_CATALOG_PRIORITIES:
            findings.error(
                f"{rel}: skill '{name}' has invalid priority '{prio}' "
                f"(must be one of: {', '.join(sorted(VALID_CATALOG_PRIORITIES))})"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as errors (CI strict mode)",
    )
    args = parser.parse_args()

    findings = Findings()

    if not SKILLS_DIR.is_dir():
        findings.error(f"{SKILLS_DIR.relative_to(REPO_ROOT)}: directory does not exist")
    if not AGENTS_DIR.is_dir():
        findings.error(f"{AGENTS_DIR.relative_to(REPO_ROOT)}: directory does not exist")

    documented_tools = parse_tool_mapping(findings)

    skill_names: dict[str, Path] = {}
    if SKILLS_DIR.is_dir():
        for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
            lint_skill(skill_dir, findings, skill_names, documented_tools)

    agent_names: dict[str, Path] = {}
    if AGENTS_DIR.is_dir():
        for agent_file in sorted(AGENTS_DIR.glob("*.md")):
            lint_agent(agent_file, findings, agent_names, documented_tools)

    lint_catalog(set(skill_names), set(agent_names), findings)

    for w in findings.warnings:
        print(f"WARN  {w}")
    for e in findings.errors:
        print(f"ERROR {e}")

    summary = (
        f"\nLinted {len(skill_names)} skills and {len(agent_names)} agents — "
        f"{len(findings.errors)} error(s), {len(findings.warnings)} warning(s)."
    )
    print(summary)

    failed = bool(findings.errors) or (args.strict and bool(findings.warnings))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
