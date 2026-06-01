#!/usr/bin/env python3
"""
dsa_commit.py — auto-commit daily DSA solutions with smart commit messages.

Usage:
    python dsa_commit.py                     # commit + push all changes
    python dsa_commit.py --dry-run           # preview message, no commit
    python dsa_commit.py "optional note"     # append a custom note to message
"""

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_DIR = Path(__file__).parent

TOPICS = {
    "arrays", "strings", "trees", "graphs", "dp",
    "linked_lists", "heaps", "backtracking", "binary_search",
    "sorting", "greedy", "two_pointers", "sliding_window",
    "stack", "queue", "trie", "bit_manipulation",
}


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def git(*args: str, check=True) -> str:
    result = subprocess.run(
        ["git", *args],
        capture_output=True, text=True, cwd=REPO_DIR,
    )
    if check and result.returncode != 0:
        print(f"[git error] git {' '.join(args)}\n{result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()


def current_branch() -> str:
    return git("rev-parse", "--abbrev-ref", "HEAD")


def changed_python_files() -> list[str]:
    """Modified/untracked Python files inside topic folders only."""
    untracked = git("ls-files", "--others", "--exclude-standard").splitlines()
    modified  = git("diff", "--name-only").splitlines()
    staged    = git("diff", "--cached", "--name-only").splitlines()
    all_files = set(untracked) | set(modified) | set(staged)
    return sorted(
        f for f in all_files
        if f.endswith(".py") and Path(f).parts[0] in TOPICS
    )


# ---------------------------------------------------------------------------
# Content analysis
# ---------------------------------------------------------------------------

def topics_from_files(files: list[str]) -> list[str]:
    found = set()
    for f in files:
        top = Path(f).parts[0] if Path(f).parts else ""
        if top in TOPICS:
            found.add(top)
    return sorted(found)


def new_functions_from_diff() -> list[str]:
    """Extract function names from added lines in git diff (staged + unstaged)."""
    funcs: list[str] = []

    for diff_cmd in (
        ["diff", "--unified=0"],            # unstaged changes
        ["diff", "--cached", "--unified=0"], # staged changes
    ):
        diff_output = git(*diff_cmd, check=False)
        for line in diff_output.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                m = re.match(
                    r"^\+\s*(?:async\s+)?def\s+([a-zA-Z][a-zA-Z0-9_]*)\s*[:(]",
                    line,
                )
                if m:
                    funcs.append(m.group(1))

    return funcs


def new_functions_from_untracked(files: list[str]) -> list[str]:
    """For brand-new files not yet tracked, read defs directly."""
    funcs: list[str] = []
    untracked = set(git("ls-files", "--others", "--exclude-standard").splitlines())
    for f in files:
        if f not in untracked:
            continue
        path = REPO_DIR / f
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(
            r"^(?:async\s+)?def\s+([a-zA-Z][a-zA-Z0-9_]*)\s*[:(]",
            text, re.MULTILINE,
        ):
            name = m.group(1)
            if name not in ("main", "test") and not name.startswith("_"):
                funcs.append(name)
    return funcs


def all_new_functions(files: list[str]) -> list[str]:
    raw = new_functions_from_diff() + new_functions_from_untracked(files)
    seen: set[str] = set()
    unique: list[str] = []
    for fn in raw:
        if fn not in seen:
            seen.add(fn)
            unique.append(fn)
    return unique


# ---------------------------------------------------------------------------
# Commit message builder
# ---------------------------------------------------------------------------

def build_message(funcs: list[str], topics: list[str], files: list[str], note: str) -> str:
    today     = date.today().strftime("%d %b %Y")
    topic_str = ", ".join(topics) if topics else "misc"

    # Subject line (≤72 chars)
    if funcs:
        names = ", ".join(funcs[:4])
        if len(funcs) > 4:
            names += f" (+{len(funcs) - 4} more)"
        subject = f"solve: {names} [{topic_str}]"
    else:
        subject = f"solve: update {len(files)} file(s) [{topic_str}]"

    # Body
    lines = [f"Date: {today}"]

    if funcs:
        lines += ["", f"Problems solved ({len(funcs)}):"]
        lines += [f"  - {fn}" for fn in funcs]

    lines += ["", f"Topics: {topic_str}"]

    lines += ["", "Files:"]
    lines += [f"  - {f}" for f in files]

    if note:
        lines += ["", f"Note: {note}"]

    return subject + "\n\n" + "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args     = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry_run  = "--dry-run" in sys.argv
    note     = args[0] if args else ""

    files = changed_python_files()
    if not files:
        print("Nothing to commit — no new or modified Python files found.")
        sys.exit(0)

    topics = topics_from_files(files)
    funcs  = all_new_functions(files)
    msg    = build_message(funcs, topics, files, note)

    print("\n" + "-" * 60)
    print("  Commit message")
    print("-" * 60)
    print(msg)
    print("-" * 60)
    print(f"\n  Files  : {', '.join(files)}")
    print(f"  Topics : {', '.join(topics) or 'misc'}")
    print(f"  Funcs  : {len(funcs)} detected")

    if dry_run:
        print("\n[dry-run] Nothing committed.\n")
        sys.exit(0)

    print()

    # Stage only topic-folder Python files (not the script itself)
    git("add", "--", *files)

    # Commit
    result = subprocess.run(
        ["git", "commit", "-m", msg],
        capture_output=True, text=True, cwd=REPO_DIR,
    )
    if result.returncode != 0:
        print(f"Commit failed:\n{result.stderr.strip()}")
        sys.exit(1)
    print(result.stdout.strip())

    # Push
    branch = current_branch()
    result = subprocess.run(
        ["git", "push", "origin", branch],
        capture_output=True, text=True, cwd=REPO_DIR,
    )
    if result.returncode != 0:
        print(f"Push failed:\n{result.stderr.strip()}")
        sys.exit(1)
    print(f"Pushed to origin/{branch}.")


if __name__ == "__main__":
    main()
