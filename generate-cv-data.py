#!/usr/bin/env python3
"""Generate site data from Markdown.

1. Notes:  notes/*.md  ->  assets/data/notes.json  (knowledge graph, search, note pages)
2. CV:     cv/**/*.md  ->  assets/data/cv.json     (cv.html)

Run from the repository root:  python generate-data.py
No extra packages needed. If the ``markdown`` package is installed it is used;
otherwise a small built-in converter handles headings, lists, code blocks,
bold/italic, inline code and links.
"""

from __future__ import annotations

import ast
import json
import re
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Tuple

NOTES_DIR = Path("notes")
OUTPUT_PATH = Path("assets/data/notes.json")
COMPONENTS_DIR = Path("assets/components")

CV_DIR = Path("cv")
CV_OUTPUT_PATH = Path("assets/data/cv.json")


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Return frontmatter dict and markdown body from a note string."""
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Missing frontmatter delimiter '---' at start of file")

    try:
        end_index = [l.strip() for l in lines[1:]].index("---") + 1
    except ValueError as exc:
        raise ValueError("Closing frontmatter delimiter '---' not found") from exc

    metadata: Dict[str, Any] = {}
    for line in lines[1:end_index]:
        if not line.strip() or ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        metadata[key.strip()] = parse_value(raw_value.strip())

    body = "\n".join(lines[end_index + 1:]).strip()
    return metadata, body


def parse_value(raw: str) -> Any:
    """Parse a frontmatter value without external dependencies."""
    if not raw:
        return ""
    lowered = raw.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    try:
        return ast.literal_eval(raw)
    except Exception:
        pass
    return raw.strip('"').strip("'")


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def process_components(markdown_text: str, note_id: str) -> str:
    """Replace {{component:name}} with actual component HTML."""
    if not COMPONENTS_DIR.exists():
        return markdown_text

    def replace_component(match):
        component_name = match.group(1)
        component_file = COMPONENTS_DIR / f"{component_name}.html"
        if not component_file.exists():
            return f"<p style='color: red;'>Component '{component_name}' not found</p>"
        try:
            component_html = component_file.read_text(encoding="utf-8")
            return component_html.replace("{ID}", f"{note_id}-{component_name}")
        except Exception as e:
            return f"<p style='color: red;'>Error loading component '{component_name}': {e}</p>"

    return re.sub(r"\{\{component:([a-zA-Z0-9_-]+)\}\}", replace_component, markdown_text)


def render_markdown(markdown_text: str) -> str:
    """Render markdown to HTML (``markdown`` package if available, else fallback)."""
    try:
        import markdown  # type: ignore
        return markdown.markdown(markdown_text, extensions=["fenced_code", "tables"])
    except Exception:
        return simple_markdown(markdown_text)


def render_inline(text: str) -> str:
    """Escape text, then apply **bold**, *italic*, `code` and [links](url)."""
    t = escape(text)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*\s][^*]*)\*(?![*\w])", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return t


def simple_markdown(markdown_text: str) -> str:
    """Small markdown-to-HTML fallback."""
    html_parts: List[str] = []
    list_tag = ""          # "", "ul" or "ol"
    in_code_block = False
    code_lines: List[str] = []
    code_language = ""

    def close_list():
        nonlocal list_tag
        if list_tag:
            html_parts.append(f"</{list_tag}>")
            list_tag = ""

    for line in markdown_text.splitlines():
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_code_block:
                close_list()
                in_code_block = True
                code_language = stripped[3:].strip() or "text"
                code_lines = []
            else:
                in_code_block = False
                code_content = "\n".join(code_lines)
                html_parts.append(
                    f'<pre><code class="language-{escape(code_language)}">{escape(code_content)}</code></pre>'
                )
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        if not stripped:
            close_list()
            continue

        if stripped.startswith("<!--"):
            continue

        if stripped.startswith("#"):
            close_list()
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped[level:].strip()
            level = min(level, 6)
            html_parts.append(f"<h{level}>{render_inline(text)}</h{level}>")
            continue

        ordered = re.match(r"^\d+[.)]\s+(.*)$", stripped)
        if stripped.startswith(("- ", "* ")) or ordered:
            wanted = "ol" if ordered else "ul"
            if list_tag != wanted:
                close_list()
                html_parts.append(f"<{wanted}>")
                list_tag = wanted
            item = ordered.group(1) if ordered else stripped[2:].strip()
            html_parts.append(f"<li>{render_inline(item)}</li>")
            continue

        close_list()
        html_parts.append(f"<p>{render_inline(stripped)}</p>")

    close_list()
    return "\n".join(html_parts)


# ---------------------------------------------------------------------------
# Notes  (unchanged behaviour)
# ---------------------------------------------------------------------------

def build_note_payload(note_path: Path) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
    metadata, body = parse_frontmatter(note_path.read_text(encoding="utf-8"))

    note_id = metadata.get("id") or note_path.stem
    title = metadata.get("title") or note_path.stem.replace("-", " ").title()
    category = metadata.get("category", "misc")
    tags = metadata.get("tags") or []
    related = metadata.get("related") or []
    date = metadata.get("date", "")
    description = metadata.get("description", "")

    body = process_components(body, note_id)
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

    return {"generated_at": now_iso(), "nodes": nodes, "links": links}


# ---------------------------------------------------------------------------
# CV
# ---------------------------------------------------------------------------

META_LINE = re.compile(r"^([a-z_]+):\s*(.*)$")
TODO = re.compile(r"\[([^\]<>]{1,120})\](?!\()")
YOUTUBE_ID = re.compile(r"(?:youtube\.com/(?:watch\?v=|embed/|shorts/|live/)|youtu\.be/)([A-Za-z0-9_-]{11})")


def mark_todos(html: str) -> str:
    """Wrap leftover [placeholders] so the page can hide or highlight them."""
    return TODO.sub(r'<mark class="todo">[\1]</mark>', html)


def md(text: str) -> str:
    return mark_todos(render_markdown(text.strip())) if text.strip() else ""


def read_file(path: Path) -> Tuple[Dict[str, Any], str]:
    """Read a file that may or may not have frontmatter."""
    content = path.read_text(encoding="utf-8")
    if content.lstrip().startswith("---"):
        return parse_frontmatter(content.lstrip())
    return {}, content.strip()


def split_sections(body: str) -> Tuple[str, List[Dict[str, Any]]]:
    """Split a body on '## ' headings.

    Returns (intro_text, sections). Each section has its heading, a meta dict
    from 'key: value' lines right under the heading, and the remaining text.
    Lines starting with a single '# ' before the first section are comments.
    """
    intro: List[str] = []
    raw: List[Dict[str, Any]] = []
    for line in body.splitlines():
        if line.startswith("## "):
            raw.append({"heading": line[3:].strip(), "lines": []})
        elif raw:
            raw[-1]["lines"].append(line)
        elif not line.startswith("# "):
            intro.append(line)

    sections = []
    for s in raw:
        rest = s["lines"]
        while rest and not rest[0].strip():
            rest.pop(0)
        meta: Dict[str, Any] = {}
        while rest:
            m = META_LINE.match(rest[0].strip())
            if not m:
                break
            meta[m.group(1)] = parse_value(m.group(2))
            rest.pop(0)
        sections.append({"heading": s["heading"], "meta": meta, "text": "\n".join(rest).strip()})
    return "\n".join(intro).strip(), sections


def s(value: Any) -> str:
    return "" if value is None else str(value)


def cv_profile() -> Dict[str, Any]:
    path = CV_DIR / "profile.md"
    if not path.exists():
        return {}
    meta, body = read_file(path)
    intro, sections = split_sections(body)
    links = []
    for sec in sections:
        if sec["heading"].lower() == "links":
            for label, url in re.findall(r"\[([^\]]+)\]\(([^)\s]+)\)", sec["text"]):
                links.append({"label": label, "url": url})
    return {
        "name": s(meta.get("name")),
        "title": s(meta.get("title")),
        "meta": s(meta.get("meta")),
        "email": s(meta.get("email")),
        "summary_html": md(intro),
        "links": links,
    }


def cv_section_file(name: str, fields: List[str]) -> List[Dict[str, Any]]:
    path = CV_DIR / name
    if not path.exists():
        return []
    _, body = read_file(path)
    _, sections = split_sections(body)
    out = []
    for sec in sections:
        item = {"title": mark_todos(escape(sec["heading"])), "html": md(sec["text"])}
        for f in fields:
            item[f] = s(sec["meta"].get(f))
        out.append(item)
    return out


def cv_experience() -> List[Dict[str, Any]]:
    folder = CV_DIR / "experience"
    items = []
    for path in sorted(folder.glob("*.md")) if folder.exists() else []:
        if path.name.startswith("_"):
            continue
        try:
            meta, body = read_file(path)
        except Exception as exc:
            print(f"Skipping cv/experience/{path.name}: {exc}", file=sys.stderr)
            continue
        items.append({
            "title": s(meta.get("title")),
            "org": s(meta.get("org")),
            "start": s(meta.get("start")),
            "end": s(meta.get("end")),
            "location": s(meta.get("location")),
            "stack": s(meta.get("stack")),
            "earlier": meta.get("earlier") is True,
            "html": md(body),
        })
    items.sort(key=lambda x: x["start"], reverse=True)
    return items


def cv_public_work() -> List[Dict[str, Any]]:
    folder = CV_DIR / "public-work"
    items = []
    for path in sorted(folder.glob("*.md")) if folder.exists() else []:
        if path.name.startswith("_"):
            continue
        try:
            meta, body = read_file(path)
        except Exception as exc:
            print(f"Skipping cv/public-work/{path.name}: {exc}", file=sys.stderr)
            continue
        url = s(meta.get("url"))
        yt = YOUTUBE_ID.search(url)
        items.append({
            "id": path.stem,
            "date": s(meta.get("date")),
            "type": s(meta.get("type")) or "post",
            "title": s(meta.get("title")),
            "role": s(meta.get("role")),
            "org": s(meta.get("org")),
            "url": url,
            "link_label": s(meta.get("link_label")) or "Open",
            "image": s(meta.get("image")),
            "thumbnail": f"https://img.youtube.com/vi/{yt.group(1)}/hqdefault.jpg" if yt else "",
            "featured": meta.get("featured") is True,
            "draft": meta.get("draft") is True,
            "html": md(body),
        })
    items.sort(key=lambda x: x["date"], reverse=True)
    return items


def collect_cv() -> Dict[str, Any]:
    return {
        "generated_at": now_iso(),
        "profile": cv_profile(),
        "featured": cv_section_file("featured.md", ["label"]),
        "focus": cv_section_file("focus.md", ["tools"]),
        "experience": cv_experience(),
        "projects": cv_section_file("projects.md", ["kind", "stack", "link", "url"]),
        "work": cv_public_work(),
        "education": cv_section_file("education.md", []),
    }


# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    if NOTES_DIR.exists():
        notes = collect_notes()
        write_json(OUTPUT_PATH, notes)
        print(f"Wrote {OUTPUT_PATH} with {len(notes['nodes'])} nodes and {len(notes['links'])} links")
    else:
        print("notes/ not found - skipped notes", file=sys.stderr)

    if CV_DIR.exists():
        cv = collect_cv()
        write_json(CV_OUTPUT_PATH, cv)
        live = sum(1 for w in cv["work"] if not w["draft"])
        print(f"Wrote {CV_OUTPUT_PATH}: {len(cv['experience'])} roles, "
              f"{len(cv['projects'])} projects, {len(cv['work'])} public-work items ({live} live)")
    else:
        print("cv/ not found - skipped CV", file=sys.stderr)


if __name__ == "__main__":
    main()
