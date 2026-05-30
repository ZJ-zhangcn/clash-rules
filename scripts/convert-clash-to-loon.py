#!/usr/bin/env python3
"""Convert Clash classical payload YAML files under rules/clash to Loon .lsr rule sets."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
CLASH_DIR = ROOT / "rules" / "clash"
LOON_DIR = ROOT / "rules" / "loon"


def convert_text(src_text: str) -> str:
    out = []
    for raw in src_text.splitlines():
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            out.append(stripped)
            continue
        if stripped == "payload:":
            continue
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            if (item.startswith('"') and item.endswith('"')) or (item.startswith("'") and item.endswith("'")):
                item = item[1:-1]
            if item:
                out.append(item)
            continue
        if "," in stripped and not stripped.endswith(":"):
            out.append(stripped)
    seen = set()
    final = []
    for item in out:
        if item.startswith("#"):
            final.append(item)
        elif item not in seen:
            seen.add(item)
            final.append(item)
    return "\n".join(final).rstrip() + "\n"


def main() -> None:
    LOON_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in CLASH_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".yaml", ".yml", ".ymal"})
    for src in files:
        content = convert_text(src.read_text(encoding="utf-8"))
        dst = LOON_DIR / f"{src.stem}.lsr"
        dst.write_text(content, encoding="utf-8")
        print(f"{src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
