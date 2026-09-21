#!/usr/bin/env python3
"""
Speedrun checker — grades a solved copy of 10_speedrun_challenge.txt

Usage:
    python3 check_speedrun.py path/to/their_saved_file.txt
"""

import sys
import re


def load(path):
    with open(path, "r") as f:
        return f.read()


def has_line(text, exact_line):
    """True if `exact_line` appears as a full line, ignoring surrounding blank lines."""
    lines = [l.rstrip("\n") for l in text.splitlines()]
    return exact_line in lines


def check_indent(text, expected_line_with_indent):
    lines = [l.rstrip("\n") for l in text.splitlines()]
    return expected_line_with_indent in lines


def check_consecutive_duplicate(text, line_content):
    lines = [l.rstrip("\n") for l in text.splitlines()]
    for i in range(len(lines) - 1):
        if lines[i] == line_content and lines[i + 1] == line_content:
            return True
    return False


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 check_speedrun.py <solved_file.txt>")
        sys.exit(1)

    text = load(sys.argv[1])

    checks = [
        ("BUG 1  (typo)",
         has_line(text, "Vim is a fast and powerful text editor.")),

        ("BUG 2  (word order)",
         has_line(text, "the quick brown fox jumped over the lazy dog")),

        ("BUG 3  (uppercase)",
         has_line(text, "WARNING: DRAGONS AHEAD")),

        ("BUG 4  (wrong character)",
         has_line(text, "Vim is great once it clicks.")),

        ("BUG 5  (delete junk line)",
         not has_line(text, "this line should not exist, delete it completely")),

        ("BUG 6  (insert new line)",
         has_line(text, "session complete")),

        ("BUG 7  (fix indentation)",
         check_indent(text, "    beta step runs second")),

        ("BUG 8  (search & replace x3)",
         has_line(text, "step one: done")
         and has_line(text, "step two: done")
         and has_line(text, "step three: done")
         and not has_line(text, "step one: todo")
         and not has_line(text, "step two: todo")
         and not has_line(text, "step three: todo")),

        ("BUG 9  (change inside quotes)",
         has_line(text, 'name = "Ada Lovelace"')),

        ("BUG 10 (change inside parens)",
         has_line(text, "scale(2.5)")),

        ("BUG 11 (comment out block)",
         has_line(text, '// print("alpha")')
         and has_line(text, '// print("beta")')
         and has_line(text, '// print("gamma")')),

        ("BUG 12 (yank & duplicate line)",
         check_consecutive_duplicate(text, "COPY-ME: the final boss line")),
    ]

    passed = 0
    width = max(len(name) for name, _ in checks)
    print()
    for name, ok in checks:
        status = "PASS" if ok else "FAIL"
        symbol = "✅" if ok else "❌"
        print(f"  {symbol}  {name.ljust(width)}  {status}")
        if ok:
            passed += 1

    total = len(checks)
    print()
    print(f"  Score: {passed}/{total}")
    if passed == total:
        print("Congratulations!")
    print()


if __name__ == "__main__":
    main()
