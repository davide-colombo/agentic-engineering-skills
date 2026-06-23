#!/usr/bin/env python3
"""Validate the public agentic-engineering-skills repository without writes."""

from __future__ import annotations

import sys
from pathlib import Path


EXPECTED_SKILLS = (
    "agent-output-verification-and-claim-audit",
    "code-review-and-test-audit",
    "configuration-and-environment-integrity",
    "cross-session-handoff-and-continuity",
    "data-transfer-and-integrity",
    "evidence-citation-discipline",
    "failure-recovery-and-rerun-planning",
    "git-integration-and-release-workflow",
    "hardware-aware-parallelism",
    "minimal-diff-implementation-discipline",
    "production-run-launch-and-monitoring",
    "prompt-crafting-for-coding-agents",
    "read-only-audit-protocol",
    "remote-execution-safety",
    "repo-state-audit",
    "resumable-pipeline-design",
    "task-dossier-lifecycle",
    "token-efficient-repository-inspection",
)
NEW_IN_V03 = (
    "agent-output-verification-and-claim-audit",
    "evidence-citation-discipline",
)
NEW_IN_V04 = (
    "minimal-diff-implementation-discipline",
    "token-efficient-repository-inspection",
)
LEAKAGE_PATTERNS = (
    "/Users/",
    "/mnt/das",
    "/mnt/das/users_data",
    "nexteveApp",
    "nexteve_output",
    "nirv",
    "unipv",
    "davide.colombo",
    "Pavia",
)


class Reporter:
    def __init__(self) -> None:
        self.failures = 0

    def check(self, label: str, condition: bool, detail: str = "") -> None:
        if condition:
            print(f"PASS: {label}")
            return
        self.failures += 1
        suffix = f" ({detail})" if detail else ""
        print(f"FAIL: {label}{suffix}")


def _read_frontmatter(skill_md: Path) -> dict[str, str] | None:
    try:
        text = skill_md.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    block = text[4:end]
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def _direct_subdirectories(path: Path) -> set[str]:
    if not path.is_dir():
        return set()
    return {child.name for child in path.iterdir() if child.is_dir()}


def _markdown_children(path: Path) -> list[str]:
    if not path.is_dir():
        return []
    return sorted(child.name for child in path.iterdir() if child.is_file() and child.suffix.lower() == ".md")


def _iter_text_files(repository: Path, self_path: Path) -> list[Path]:
    targets: list[Path] = []
    for sub in ("skills", "scripts", "docs", "templates", "hooks"):
        root = repository / sub
        if not root.is_dir():
            continue
        for child in root.rglob("*"):
            if not child.is_file():
                continue
            if child.resolve() == self_path:
                continue
            if child.suffix.lower() in {".md", ".py"}:
                targets.append(child)
    for top in ("README.md",):
        candidate = repository / top
        if candidate.is_file():
            targets.append(candidate)
    return targets


def main() -> int:
    script_path = Path(__file__).resolve()
    repository = script_path.parents[1]
    reporter = Reporter()

    skills_root = repository / "skills"
    reporter.check("skills/ directory exists", skills_root.is_dir())

    skill_dirs = _direct_subdirectories(skills_root)
    expected = set(EXPECTED_SKILLS)
    reporter.check(
        f"skill inventory is exactly the expected {len(EXPECTED_SKILLS)} skills",
        skill_dirs == expected,
        f"found: {', '.join(sorted(skill_dirs))}",
    )

    for skill in sorted(expected):
        skill_dir = skills_root / skill
        skill_md = skill_dir / "SKILL.md"

        reporter.check(
            f"{skill}: SKILL.md exists",
            skill_md.is_file(),
        )

        md_files = _markdown_children(skill_dir)
        reporter.check(
            f"{skill}: exactly one Markdown file in skill directory",
            md_files == ["SKILL.md"],
            f"found: {', '.join(md_files) if md_files else 'none'}",
        )

        if not skill_md.is_file():
            reporter.check(f"{skill}: frontmatter parses", False, "SKILL.md missing")
            continue

        fields = _read_frontmatter(skill_md)
        reporter.check(
            f"{skill}: frontmatter parses",
            fields is not None,
        )
        if fields is None:
            continue

        reporter.check(
            f"{skill}: frontmatter name matches directory",
            fields.get("name") == skill,
            f"name: {fields.get('name')!r}",
        )
        description = fields.get("description", "")
        reporter.check(
            f"{skill}: frontmatter description is non-empty",
            bool(description),
        )

    readme_path = repository / "README.md"
    reporter.check("README.md exists", readme_path.is_file())
    if readme_path.is_file():
        readme_text = readme_path.read_text(encoding="utf-8")
        for skill in NEW_IN_V03:
            reporter.check(
                f"README references new skill {skill}",
                skill in readme_text,
            )
        reporter.check(
            "README has a v0.3 section heading",
            "## v0.3" in readme_text,
        )
        for skill in NEW_IN_V04:
            reporter.check(
                f"README references new skill {skill}",
                skill in readme_text,
            )
            reporter.check(
                f"README links to SKILL.md for {skill}",
                f"skills/{skill}/SKILL.md" in readme_text,
            )
        reporter.check(
            "README has a v0.4 section heading",
            "## v0.4" in readme_text,
        )

    leaks: list[str] = []
    for target in _iter_text_files(repository, script_path):
        try:
            text = target.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for pattern in LEAKAGE_PATTERNS:
            if pattern in text:
                leaks.append(f"{target.relative_to(repository)}:{pattern}")
    reporter.check(
        "no private-leakage patterns in tracked Markdown or Python sources",
        not leaks,
        "; ".join(leaks) if leaks else "",
    )

    reporter.check(
        "validator runs without external dependencies",
        True,
        "Python stdlib only; gitignored local files such as .DS_Store are outside validator scope",
    )

    if reporter.failures:
        print(f"FAIL: public skills repository has validation errors ({reporter.failures})")
        return 1
    print("PASS: public skills repository is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
