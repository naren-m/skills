#!/usr/bin/env python3
"""Preservation gate for the STE100 issue rewrites.

For each orig/<n>.md with a new/<n>.md, extract the load-bearing tokens from the
original (issue refs, inline code, file paths, file:line, numbers with units or
decimals, Devanagari words) and report any that are missing from the rewrite.
A rewrite with missing tokens is not posted until reviewed.

usage: check.py DIR [N ...]    exit 1 if any issue has missing tokens
"""
import re, sys, pathlib

TOKEN_RES = [
    r"#\d{2,4}",                                  # issue / PR refs
    r"`[^`\n]{1,80}`",                            # inline code
    r"[\w./-]+\.(?:py|ts|tsx|js|yaml|yml|json|md|jsonl|pkl|toml|ini|sh)(?::\d+)?",  # paths, file:line
    r"\b\d+\.\d+\b",                              # decimals (recall 0.70, sutra 6.5.16 parts)
    r"\b\d+(?:\.\d+)*\s?(?:%|ms|s|MB|GB|q)\b",    # numbers with units
    r"[ऀ-ॿ]+",                          # Devanagari terms
]

def tokens(text: str) -> set[str]:
    found = set()
    for rx in TOKEN_RES:
        for m in re.findall(rx, text):
            t = m.strip()
            if len(t) > 1:
                found.add(t)
    return found

def norm(s: str) -> str:
    return s.replace("`", "")

def main() -> int:
    d = pathlib.Path(sys.argv[1])
    nums = sys.argv[2:] or sorted(p.stem for p in (d / "new").glob("*.md"))
    bad = 0
    for n in nums:
        o, w = d / "orig" / f"{n}.md", d / "new" / f"{n}.md"
        if not w.exists():
            print(f"#{n}: NO REWRITE"); bad += 1; continue
        orig, new = o.read_text(), w.read_text()
        newn = norm(new)
        missing = sorted(t for t in tokens(orig) if t not in new and norm(t) not in newn)
        first = new.splitlines()[0] if new else ""
        if not first.startswith("TITLE: "):
            print(f"#{n}: first line is not 'TITLE: ...'"); bad += 1
        status = "ok" if not missing else f"MISSING {len(missing)}: " + " | ".join(missing[:12])
        print(f"#{n}: words {len(orig.split())} -> {len(new.split())}  {status}")
        bad += bool(missing)
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
