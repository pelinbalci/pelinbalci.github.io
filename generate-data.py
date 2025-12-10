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
import re
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
    body_lines = lines[end_index + 1:]

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

    try:
        return ast.literal_eval(raw)
    except Exception:
        pass

    return raw.strip('"').strip("'")


def render_markdown(markdown_text: str) -> str:
    """Render markdown to HTML.

    Tries to use the ``markdown`` package if available, otherwise uses fallback.
    """
    try:
        import markdown
        md = markdown.Markdown(extensions=['fenced_code', 'tables', 'md_in_html'])
        return md.convert(markdown_text)
    except ImportError:
        return simple_markdown(markdown_text)


def simple_markdown(markdown_text: str) -> str:
    """A markdown-to-HTML converter that preserves raw HTML."""
    lines = markdown_text.splitlines()
    html_parts: List[str] = []

    i = 0
    in_list = False
    list_type = None  # 'ul' or 'ol'
    in_code_block = False
    code_lines: List[str] = []
    code_lang = ""

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # --- Handle fenced code blocks ---
        if stripped.startswith("```"):
            if not in_code_block:
                if in_list:
                    html_parts.append(f"</{list_type}>")
                    in_list = False
                in_code_block = True
                code_lang = stripped[3:].strip()
                code_lines = []
                i += 1
                continue
            else:
                in_code_block = False
                lang_attr = f' class="language-{code_lang}"' if code_lang else ''
                code_content = escape("\n".join(code_lines))
                html_parts.append(f"<pre><code{lang_attr}>{code_content}</code></pre>")
                i += 1
                continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # --- Handle raw HTML blocks ---
        # Check if line starts with an HTML tag (but not a comment)
        html_tag_match = re.match(r'^<([a-zA-Z][a-zA-Z0-9]*)', stripped)
        if html_tag_match and not stripped.startswith("<!"):
            if in_list:
                html_parts.append(f"</{list_type}>")
                in_list = False

            tag_name = html_tag_match.group(1).lower()

            # Self-closing tags or void elements
            void_elements = {'img', 'br', 'hr', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'param',
                             'source', 'track', 'wbr'}

            if tag_name in void_elements or stripped.endswith("/>"):
                html_parts.append(line)
                i += 1
                continue

            # Check if it's a complete single-line tag (opening and closing on same line)
            # Count opening and closing tags for this tag_name
            if is_balanced_html_line(stripped, tag_name):
                html_parts.append(line)
                i += 1
                continue

            # Multi-line HTML block - collect until tags are balanced
            html_block = [line]
            depth = count_tag_depth(line, tag_name)

            while depth > 0 and i + 1 < len(lines):
                i += 1
                next_line = lines[i]
                html_block.append(next_line)
                depth += count_tag_depth(next_line, tag_name)

            html_parts.append("\n".join(html_block))
            i += 1
            continue

        # --- Empty lines ---
        if not stripped:
            if in_list:
                html_parts.append(f"</{list_type}>")
                in_list = False
            i += 1
            continue

        # --- Headings ---
        if stripped.startswith("#"):
            if in_list:
                html_parts.append(f"</{list_type}>")
                in_list = False

            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped[level:].strip()
            level = min(level, 6)
            text = process_inline(text)
            html_parts.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        # --- Horizontal rules ---
        if re.match(r'^[-*_]{3,}$', stripped):
            if in_list:
                html_parts.append(f"</{list_type}>")
                in_list = False
            html_parts.append("<hr>")
            i += 1
            continue

        # --- Unordered list items ---
        if stripped.startswith("- ") or stripped.startswith("* "):
            if in_list and list_type != 'ul':
                html_parts.append(f"</{list_type}>")
                in_list = False
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
                list_type = 'ul'
            item_text = process_inline(stripped[2:].strip())
            html_parts.append(f"<li>{item_text}</li>")
            i += 1
            continue

        # --- Ordered list items ---
        ol_match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if ol_match:
            if in_list and list_type != 'ol':
                html_parts.append(f"</{list_type}>")
                in_list = False
            if not in_list:
                html_parts.append("<ol>")
                in_list = True
                list_type = 'ol'
            item_text = process_inline(ol_match.group(2))
            html_parts.append(f"<li>{item_text}</li>")
            i += 1
            continue

        # --- Regular paragraph ---
        if in_list:
            html_parts.append(f"</{list_type}>")
            in_list = False

        para_text = process_inline(stripped)
        html_parts.append(f"<p>{para_text}</p>")
        i += 1

    # Close any remaining open list
    if in_list:
        html_parts.append(f"</{list_type}>")

    return "\n".join(html_parts)


def count_tag_depth(line: str, tag_name: str) -> int:
    """Count the net depth change for a specific tag in a line.

    Returns positive for opening tags, negative for closing tags.
    """
    # Count opening tags (but not self-closing)
    opening_pattern = f'<{tag_name}(?:\\s[^>]*)?>(?!</{tag_name}>)'
    opening = len(re.findall(opening_pattern, line, re.IGNORECASE))

    # Also count simple opening tags
    simple_opening = len(re.findall(f'<{tag_name}(?:\\s[^>]*)?>', line, re.IGNORECASE))

    # Count closing tags
    closing = len(re.findall(f'</{tag_name}>', line, re.IGNORECASE))

    # Count self-closing tags (these don't affect depth)
    self_closing = len(re.findall(f'<{tag_name}[^>]*/>', line, re.IGNORECASE))

    return simple_opening - self_closing - closing


def is_balanced_html_line(line: str, tag_name: str) -> bool:
    """Check if a single line has balanced opening and closing tags."""
    depth = count_tag_depth(line, tag_name)
    return depth == 0 and f'<{tag_name}' in line.lower()


def process_inline(text: str) -> str:
    """Process inline markdown: bold, italic, code, links, images."""
    # If text already contains HTML tags, return as-is to avoid double processing
    if re.search(r'<[a-zA-Z][^>]*>', text):
        return text

    # Images: ![alt](src) - do this before links
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)

    # Links: [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

    # Bold: **text** or __text__
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)

    # Italic: *text* or _text_
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'<em>\1</em>', text)

    # Inline code: `code`
    text = re.sub(r'`([^`]+)`', lambda m: f'<code>{escape(m.group(1))}</code>', text)

    return text


def build_note_payload(note_path: Path) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
    """Build the JSON payload for a single note."""
    metadata, body = parse_frontmatter(note_path.read_text(encoding="utf-8"))

    note_id = metadata.get("id") or note_path.stem
    title = metadata.get("title") or note_path.stem.replace("-", " ").title()
    category = metadata.get("category", "misc")
    tags = metadata.get("tags") or []
    related = metadata.get("related") or []
    date = metadata.get("date", "")
    description = metadata.get("description", "")

    html_content = render_markdown(body)

    # Create plain text excerpt (strip HTML for this)
    plain_text = re.sub(r'<[^>]+>', '', body)
    plain_text = " ".join(plain_text.split())
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
    """Collect all notes from the notes directory."""
    if not NOTES_DIR.exists():
        raise SystemExit("notes/ directory not found")

    nodes: List[Dict[str, Any]] = []
    links: List[Dict[str, str]] = []
    seen_links = set()

    for note_path in sorted(NOTES_DIR.glob("*.md")):
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