#!/usr/bin/env python3
"""Check every markdown link under docs/specs.

Rules this enforces, from tig/mike#4 review (2026-10-05):
1. A relative link to a .md file must name a file that exists, and its #anchor
   must match a heading in that file (GitHub slug rules).
2. A link's text must carry context: it may not be only an issue or pull
   number, a bare section number, a bare id (US-01, MS-001, Q3), or a bare
   file:line.
3. A bare reference with no link is reported: factory#NNNN, #NNNN, MS-NNN,
   US-NN, OS-NN, decision NN, gate NN, QNN, `mike.md` N.N, and `path:line`
   cites, outside fenced code and outside headings (a heading is a target).
Exit 1 on any finding. Usage: python3 tools/check_spec_links.py [files...]
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPECS = ROOT / "docs" / "specs"

def slug(heading: str) -> str:
    h = heading.strip().lower()
    h = re.sub(r"[`*_]", "", h)
    h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", h)
    h = re.sub(r"[^\w\s-]", "", h)
    return re.sub(r"\s+", "-", h.strip())

def headings(path: pathlib.Path) -> set[str]:
    out, seen = set(), {}
    fenced = False
    for line in path.read_text().splitlines():
        if line.startswith("```"):
            fenced = not fenced; continue
        if fenced: continue
        m = re.match(r"^#{1,6}\s+(.*)$", line)
        if m:
            s = slug(m.group(1))
            n = seen.get(s, 0); seen[s] = n + 1
            out.add(s if n == 0 else f"{s}-{n}")
    return out

BARE_TEXT = re.compile(r"^(factory)?#?\d+$|^(US|OS|MS)-\d+$|^Q\d+$|^\d+(\.\d+)*$|^[\w./-]+:\d+(-\d+)?$|^`[^`]*`$", re.I)
BARE_REF = re.compile(
    r"(?<![\w/#\[-])(factory#\d+|tig/mike#\d+|#\d{2,}|(?:US|OS|MS)-\d+|decision \d+|gate \d+|Q\d+|`mike\.md` \d+(?:\.\d+)?|\b[\w-]+\.(?:py|mjs|js|md|yaml|sh):\d+)(?![\w\]])")

def strip_links_and_code(line: str) -> str:
    line = re.sub(r"`[^`]*`", "``", line)
    return re.sub(r"\[[^\]]*\]\([^)]*\)", "[]", line)

def check(path: pathlib.Path, cache: dict) -> list[str]:
    findings, fenced = [], False
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if line.startswith("```"):
            fenced = not fenced; continue
        if fenced: continue
        is_heading = bool(re.match(r"^#{1,6}\s", line))
        for text, target in re.findall(r"\[([^\]]*)\]\(([^)\s]+)\)", line):
            if BARE_TEXT.match(text.strip()):
                findings.append(f"{path.name}:{n}: link text has no context: [{text}]")
            if target.startswith("http"):
                continue
            file_part, _, anchor = target.partition("#")
            tgt = (path.parent / file_part).resolve() if file_part else path
            if not tgt.exists():
                findings.append(f"{path.name}:{n}: missing file {file_part}"); continue
            if anchor:
                if tgt not in cache: cache[tgt] = headings(tgt)
                if anchor not in cache[tgt]:
                    findings.append(f"{path.name}:{n}: no heading #{anchor} in {tgt.name}")
        if is_heading:
            continue  # a heading is a link target, not a reference
        for ref in BARE_REF.findall(strip_links_and_code(line)):
            findings.append(f"{path.name}:{n}: bare reference, not a link: {ref}")
    return findings

def main(argv):
    files = [pathlib.Path(a) for a in argv] or sorted(SPECS.glob("*.md"))
    cache, findings = {}, []
    for f in files: findings += check(f, cache)
    for x in findings: print(x)
    print(f"{len(findings)} findings in {len(files)} files")
    return 1 if findings else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
