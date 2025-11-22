#!/usr/bin/env python3
"""Generate graph/search data from markdown notes.

Reads frontmatter metadata from all Markdown files in ``notes/`` and writes a
combined JSON payload to ``assets/data/notes.json``. The payload includes node
metadata, rendered HTML snippets, and graph edges derived from each note's
``related`` field.
"""

from __future__ import annotations

import ast
import json
import sys
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Tuple

NOTES_DIR = Path("notes")
OUTPUT_PATH = Path("assets/data/notes.json")


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Return frontmatter dict and markdown body from a note string."""
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Missing frontmatter delimiter '---' at start of file")

    try:
        end_index = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError("Closing frontmatter delimiter '---' not found") from exc

    frontmatter_lines = lines[1:end_index]
    body_lines = lines[end_index + 1 :]

    metadata: Dict[str, Any] = {}
    for line in frontmatter_lines:
        if not line.strip():
            continue
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        metadata[key] = parse_value(value)

    body = "\n".join(body_lines).strip()
    return metadata, body


def parse_value(raw: str) -> Any:
    """Parse a frontmatter value without external dependencies."""
    if not raw:
        return ""

    # Try Python literal evaluation for lists/strings/numbers
    try:
        return ast.literal_eval(raw)
    except Exception:
        pass

    return raw.strip('"').strip("'")


def render_markdown(markdown_text: str) -> str:
    """Render markdown to HTML.

    Tries to use the ``markdown`` package if available, and otherwise falls back
    to a very small converter that handles headings, lists, and paragraphs.
    """
    try:
        import markdown  # type: ignore

        return markdown.markdown(markdown_text, extensions=["fenced_code", "tables"])
    except Exception:
        return simple_markdown(markdown_text)


def simple_markdown(markdown_text: str) -> str:
    """A small markdown-to-HTML fallback for headings, lists, and paragraphs."""
    html_parts: List[str] = []
    in_list = False

    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            continue

        if stripped.startswith("#"):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped[level:].strip()
            level = min(level, 6)
            html_parts.append(f"<h{level}>{escape(text)}</h{level}>")
        elif stripped.startswith("- "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{escape(stripped[2:].strip())}</li>")
        else:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<p>{escape(stripped)}</p>")

    if in_list:
        html_parts.append("</ul>")

    return "\n".join(html_parts)


def build_note_payload(note_path: Path) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
    metadata, body = parse_frontmatter(note_path.read_text(encoding="utf-8"))

    note_id = metadata.get("id") or note_path.stem
    title = metadata.get("title") or note_path.stem.replace("-", " ").title()
    category = metadata.get("category", "misc")
    tags = metadata.get("tags") or []
    related = metadata.get("related") or []
    date = metadata.get("date", "")
    description = metadata.get("description", "")

    html_content = render_markdown(body)
    plain_text = " ".join(body.split())
    excerpt = plain_text[:200] + ("..." if len(plain_text) > 200 else "")

    node = {
        "id": str(note_id),
        "name": str(title),
        "category": str(category),
        "tags": tags,
        "date": str(date),
        "description": str(description),
        "related": related,
        "file": note_path.name,
        "html": html_content,
        "excerpt": excerpt,
    }

    links = [{"source": str(note_id), "target": str(target)} for target in related]
    return node, links


def collect_notes() -> Dict[str, Any]:
    if not NOTES_DIR.exists():
        raise SystemExit("notes/ directory not found")

    nodes: List[Dict[str, Any]] = []
    links: List[Dict[str, str]] = []
    seen_links = set()

    for note_path in sorted(NOTES_DIR.glob("*.md")):
        # Skip templates or helper files prefixed with an underscore
        if note_path.name.startswith("_"):
            continue

        try:
            node, note_links = build_note_payload(note_path)
        except Exception as exc:
            print(f"Skipping {note_path.name}: {exc}", file=sys.stderr)
            continue

        nodes.append(node)
        for link in note_links:
            key = (link["source"], link["target"])
            if key not in seen_links:
                links.append(link)
                seen_links.add(key)

    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "nodes": nodes,
        "links": links,
    }


def main() -> None:
    payload = collect_notes()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} with {len(payload['nodes'])} nodes and {len(payload['links'])} links")


if __name__ == "__main__":
    main()
