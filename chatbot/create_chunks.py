"""
create_chunks.py - Parses YAML Frontmatter from Markdown Notes

Reads metadata directly from your notes' frontmatter:
---
title: "GNN Architecture Deep Dive"
category: "deep-learning"
tags: ["gnn", "graph", "pytorch"]
date: "2026-01-11"
description: "..."
---

Run: python create_chunks.py
Then upload chunks.json to your HuggingFace Space.
"""

import os
import json
import glob
import re
import yaml
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
from collections import defaultdict

# =============================================================================
# CONFIGURATION
# =============================================================================

# Paths (relative to this script's location)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.join(SCRIPT_DIR, "..")

# Folders and files to process
NOTES_PATH = os.path.join(REPO_ROOT, "notes")
COMPONENTS_PATH = os.path.join(REPO_ROOT, "assets", "components")
CV_PATH = os.path.join(REPO_ROOT, "cv")  # CV content lives here (Markdown), not in cv.html


EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"  # was "all-MiniLM-L6-v2" "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
OUTPUT_FILE = "chunks.json"

# Your predefined categories (for reference/validation)
VALID_CATEGORIES = [
    "genai", "deep-learning", "conference",
    "machine-learning", "edge-ml", "visualization"
]


# =============================================================================
# YAML FRONTMATTER PARSER
# =============================================================================

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    Parse YAML frontmatter from markdown content.

    Returns:
        (metadata_dict, content_without_frontmatter)
    """
    # Match frontmatter between --- markers
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if match:
        try:
            yaml_content = match.group(1)
            body_content = match.group(2)
            metadata = yaml.safe_load(yaml_content) or {}
            return metadata, body_content
        except yaml.YAMLError as e:
            print(f"      ⚠️  YAML parse error: {e}")
            return {}, content

    return {}, content


# =============================================================================
# DOCUMENT LOADERS
# =============================================================================

def load_markdown_files(notes_path: str) -> list:
    """Load all markdown files and parse their frontmatter."""
    documents = []

    if not os.path.exists(notes_path):
        print(f"⚠️  Notes path not found: {notes_path}")
        return documents

    md_files = glob.glob(os.path.join(notes_path, "**/*.md"), recursive=True)
    print(f"📄 Found {len(md_files)} markdown files in {notes_path}")

    for filepath in md_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            filename = os.path.basename(filepath)
            relative_path = os.path.relpath(filepath, notes_path)

            # Parse frontmatter
            metadata, body = parse_frontmatter(content)

            # Extract fields from frontmatter (with fallbacks)
            title = metadata.get("title", filename.replace('.md', '').replace('-', ' ').title())
            category = metadata.get("category", "general")
            tags = metadata.get("tags", [])
            date = metadata.get("date", "")
            description = metadata.get("description", "")
            doc_id = metadata.get("id", filename.replace('.md', ''))
            related = metadata.get("related", [])

            documents.append({
                "content": body,  # Content without frontmatter
                "source": filename,
                "source_path": relative_path,
                "title": title,
                "category": category,
                "tags": tags if isinstance(tags, list) else [tags],
                "date": str(date),
                "description": description,
                "doc_id": doc_id,
                "related": related if isinstance(related, list) else [related],
                "type": "note"
            })

            # Display info
            tags_str = ", ".join(tags) if tags else "none"
            print(f"   ✅ {filename}")
            print(f"      → category: {category} | tags: [{tags_str}]")

        except Exception as e:
            print(f"   ❌ Error loading {filepath}: {e}")

    return documents


def load_html_notebooks(notebooks_path: str) -> list:
    """Load HTML notebooks from assets/components folder."""
    documents = []

    if not os.path.exists(notebooks_path):
        print(f"⚠️  Notebooks path not found: {notebooks_path}")
        return documents

    html_files = glob.glob(os.path.join(notebooks_path, "*.html"))
    print(f"📓 Found {len(html_files)} HTML notebooks")

    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()

            soup = BeautifulSoup(html_content, 'html.parser')
            for element in soup(['script', 'style', 'head']):
                element.decompose()

            text_content = soup.get_text(separator='\n', strip=True)
            filename = os.path.basename(filepath)

            # Extract title from filename (e.g., "2021-12-19-Fast Fourier Transform.html")
            title_match = re.search(r'\d{4}-\d{2}-\d{2}-(.+)\.html', filename)
            title = title_match.group(1) if title_match else filename.replace('.html', '')

            # Extract date from filename
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
            date = date_match.group(1) if date_match else ""

            documents.append({
                "content": text_content,
                "source": filename,
                "source_path": f"assets/components/{filename}",
                "title": title,
                "category": "notebook",  # Default category for notebooks
                "tags": [],
                "date": date,
                "description": "",
                "doc_id": filename.replace('.html', ''),
                "related": [],
                "type": "notebook"
            })
            print(f"   ✅ {filename} → {title}")

        except Exception as e:
            print(f"   ❌ Error loading {filepath}: {e}")

    return documents


def load_root_html_files(repo_root: str) -> list:
    """Load CV, projects, and about pages."""
    documents = []

    pages = [
        # cv.html is now an empty shell filled by JavaScript, so the CV is
        # read from the cv/ Markdown files instead (see load_cv_files).
        ("projects.html", "Projects Page", "projects"),
        ("about.html", "About Page", "about")
    ]

    print("📋 Loading root HTML files...")

    for filename, title, page_category in pages:
        filepath = os.path.join(repo_root, filename)

        if not os.path.exists(filepath):
            print(f"   ⚠️  {filename} not found")
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()

            soup = BeautifulSoup(html_content, 'html.parser')
            for element in soup(['script', 'style', 'head', 'nav', 'footer']):
                element.decompose()

            text_content = soup.get_text(separator='\n', strip=True)

            documents.append({
                "content": text_content,
                "source": filename,
                "source_path": filename,
                "title": title,
                "category": page_category,
                "tags": [],
                "date": "",
                "description": "",
                "doc_id": page_category,
                "related": [],
                "type": "page"
            })
            print(f"   ✅ {filename}")

        except Exception as e:
            print(f"   ❌ Error loading {filepath}: {e}")

    return documents


def clean_cv_text(text: str) -> str:
    """Remove things that should not reach the chatbot:
    [placeholders], '# ' comment lines and <!-- --> comments."""
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'\[[^\]\n]{1,120}\](?!\()', '', text)          # [outcome], [result] ...
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'\1 (\2)', text)  # [label](url) -> label (url)
    lines = [l for l in text.splitlines() if not re.match(r'^#\s', l)]
    text = "\n".join(lines)
    text = re.sub(r'[ \t]+\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def split_cv_sections(body: str) -> list:
    """Split a CV file on '## ' headings -> [(heading, text), ...]."""
    sections, heading, buf = [], None, []
    for line in body.splitlines():
        if line.startswith("## "):
            if heading is not None:
                sections.append((heading, "\n".join(buf)))
            heading, buf = line[3:].strip(), []
        elif heading is not None:
            buf.append(line)
    if heading is not None:
        sections.append((heading, "\n".join(buf)))
    return sections


def cv_document(title: str, content: str, source: str, doc_id: str, date: str = "") -> dict:
    return {
        "content": content,
        "source": source,
        "source_path": f"cv/{source}",
        "title": title,
        "category": "cv",
        "tags": ["cv", "resume", "pelin balci"],
        "date": str(date),
        "description": "",
        "doc_id": doc_id,
        "related": [],
        "type": "page"
    }


def load_cv_files(cv_path: str) -> list:
    """Load the CV from the cv/ folder (the same files that build cv.html).

    One document per role, per project and per public-work item, so the
    chatbot can retrieve them separately. Drafts, files starting with '_'
    and [placeholders] are skipped.
    """
    documents = []

    if not os.path.exists(cv_path):
        print(f"⚠️  CV path not found: {cv_path}")
        return documents

    def read(relpath):
        path = os.path.join(cv_path, relpath)
        if not os.path.exists(path):
            return None, None
        with open(path, 'r', encoding='utf-8') as f:
            return parse_frontmatter(f.read())

    who = "Pelin Balcı"

    # Profile: name, title, summary, links
    meta, body = read("profile.md")
    if body is not None:
        header = f"{meta.get('name', who)} — {meta.get('title', '')}\n{meta.get('meta', '')}"
        documents.append(cv_document(
            "CV — Profile and summary",
            clean_cv_text(f"{header}\n\n{body}"),
            "profile.md", "cv-profile"))

    # Selected work and focus areas (one document each)
    for filename, label, doc_id in [("featured.md", "Selected work", "cv-featured"),
                                    ("focus.md", "Focus areas / skills", "cv-focus")]:
        _, body = read(filename)
        if body:
            documents.append(cv_document(
                f"CV — {label}",
                clean_cv_text(f"{who}'s CV — {label}\n\n{body}"),
                filename, doc_id))

    # Experience: one document per role
    exp_dir = os.path.join(cv_path, "experience")
    for path in sorted(glob.glob(os.path.join(exp_dir, "*.md")), reverse=True):
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        meta, body = read(os.path.join("experience", name))
        period = f"{meta.get('start', '')} – {meta.get('end', '')}".strip(" –")
        header = (f"{who}'s work experience: {meta.get('title', '')} at {meta.get('org', '')} "
                  f"({period}{', ' + meta['location'] if meta.get('location') else ''})")
        stack = f"\nTools: {meta['stack']}" if meta.get("stack") else ""
        documents.append(cv_document(
            f"CV — Experience: {meta.get('title', '')} · {meta.get('org', '')}",
            clean_cv_text(f"{header}\n\n{body}{stack}"),
            f"experience/{name}", f"cv-exp-{name[:-3]}", meta.get("start", "")))

    # Projects: one document per '## ' section
    _, body = read("projects.md")
    for i, (heading, text) in enumerate(split_cv_sections(body or "")):
        text = re.sub(r'(?m)^link:.*\n?', '', text)                 # button label, not useful
        text = re.sub(r'(?m)^url:\s*$\n?', '', text)               # empty url (client work)
        text = re.sub(r'(?m)^(kind|stack|url):', lambda m: m.group(1).capitalize() + ':', text)
        documents.append(cv_document(
            f"CV — Project: {heading}",
            clean_cv_text(f"{who}'s project: {heading}\n{text}"),
            "projects.md", f"cv-project-{i}"))

    # Public work: one document per item, drafts skipped
    work_dir = os.path.join(cv_path, "public-work")
    for path in sorted(glob.glob(os.path.join(work_dir, "*.md")), reverse=True):
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        meta, body = read(os.path.join("public-work", name))
        if meta.get("draft") is True:
            continue
        url = meta.get("url", "")
        url_line = f"\nLink: {url}" if url and not str(url).startswith("[") else ""
        header = (f"{who}'s public work ({meta.get('type', '')}, {meta.get('date', '')}): "
                  f"{meta.get('title', '')} — {meta.get('role', '')}, {meta.get('org', '')}")
        documents.append(cv_document(
            f"CV — Public work: {meta.get('title', '')}",
            clean_cv_text(f"{header}\n\n{body}{url_line}"),
            f"public-work/{name}", f"cv-work-{name[:-3]}", meta.get("date", "")))

    # Education, training, awards, languages
    _, body = read("education.md")
    if body:
        documents.append(cv_document(
            "CV — Education, training, awards and languages",
            clean_cv_text(f"{who}'s education, certifications, awards and languages\n\n{body}"),
            "education.md", "cv-education"))

    for doc in documents:
        print(f"   ✅ {doc['source']} → {doc['title']}")
    return documents


# =============================================================================
# INDEX CHUNK CREATION
# =============================================================================

def create_index_chunk(documents: list) -> dict:
    """
    Create a special index chunk that summarizes all content.
    Helps answer: "How many notes?", "What categories?", "List all X notes"
    """

    by_category = defaultdict(list)
    by_type = defaultdict(list)
    all_tags = defaultdict(int)

    for doc in documents:
        by_category[doc["category"]].append(doc)
        by_type[doc["type"]].append(doc)
        for tag in doc.get("tags", []):
            all_tags[tag] += 1

    # Build index content
    lines = [
        "=== CONTENT INDEX ===",
        "",
        f"Total documents: {len(documents)}",
        f"- Notes (markdown): {len(by_type.get('note', []))}",
        f"- Notebooks (HTML): {len(by_type.get('notebook', []))}",
        f"- Pages: {len(by_type.get('page', []))}",
        "",
        "=== DOCUMENTS BY CATEGORY ===",
        ""
    ]

    for category in sorted(by_category.keys()):
        docs = by_category[category]
        category_display = category.replace('-', ' ').replace('_', ' ').title()
        lines.append(f"## {category_display} ({len(docs)} documents)")

        for doc in sorted(docs, key=lambda x: x.get("date", ""), reverse=True):
            title = doc['title']
            source = doc['source']
            date = doc.get('date', '')
            date_str = f" ({date})" if date else ""
            lines.append(f"  - {title}{date_str} [{source}]")

        lines.append("")

    # Add tag summary
    if all_tags:
        lines.append("=== ALL TAGS ===")
        lines.append("")
        sorted_tags = sorted(all_tags.items(), key=lambda x: x[1], reverse=True)
        tag_list = [f"{tag} ({count})" for tag, count in sorted_tags[:20]]
        lines.append(", ".join(tag_list))
        lines.append("")

    index_content = "\n".join(lines)

    return {
        "content": index_content,
        "source": "INDEX",
        "source_path": "index",
        "title": "Content Index",
        "category": "index",
        "tags": [],
        "date": "",
        "description": "Index of all available content",
        "doc_id": "index",
        "related": [],
        "type": "index"
    }


# =============================================================================
# CHUNKING
# =============================================================================

def split_into_chunks(documents: list) -> list:
    """Split documents into smaller chunks, preserving all metadata."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "]
    )

    chunks = []

    for doc in documents:
        splits = text_splitter.split_text(doc["content"])

        for i, split in enumerate(splits):
            chunks.append({
                "text": split,
                "source": doc["source"],
                "source_path": doc.get("source_path", doc["source"]),
                "title": doc["title"],
                "category": doc["category"],
                "tags": doc.get("tags", []),
                "date": doc.get("date", ""),
                "description": doc.get("description", ""),
                "doc_id": doc.get("doc_id", ""),
                "type": doc["type"],
                "chunk_id": f"{doc['source']}_{i}"
            })

    print(f"✂️  Created {len(chunks)} chunks")
    return chunks


# =============================================================================
# EMBEDDINGS
# =============================================================================

def create_embeddings(chunks: list) -> list:
    """Create embeddings for each chunk."""

    print(f"🔄 Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    texts = [chunk["text"] for chunk in chunks]

    print(f"🔄 Creating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True)

    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()

    print(f"✅ Created {len(embeddings)} embeddings")
    return chunks


# =============================================================================
# SAVE
# =============================================================================

def save_chunks(chunks: list, output_file: str):
    """Save chunks with embeddings to JSON file."""

    output_path = os.path.join(SCRIPT_DIR, output_file)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"💾 Saved to {output_path} ({file_size:.2f} MB)")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "=" * 60)
    print("🧠 CHUNK GENERATOR")
    print("   Parses YAML Frontmatter + Creates Index")
    print("=" * 60 + "\n")

    all_documents = []

    # Step 1: Load markdown notes (with frontmatter parsing)
    print("Step 1/6: Loading markdown files...")
    md_docs = load_markdown_files(NOTES_PATH)
    all_documents.extend(md_docs)

    # Step 2: Load HTML notebooks
    print("\nStep 2/6: Loading HTML notebooks...")
    notebook_docs = load_html_notebooks(COMPONENTS_PATH)
    all_documents.extend(notebook_docs)

    # Step 3: Load root HTML files
    print("\nStep 3/6: Loading root HTML files...")
    page_docs = load_root_html_files(REPO_ROOT)
    all_documents.extend(page_docs)

    # Step 3b: Load the CV from the cv/ Markdown folder
    print("\nStep 3b/6: Loading CV (cv/ folder)...")
    cv_docs = load_cv_files(CV_PATH)
    all_documents.extend(cv_docs)

    if not all_documents:
        print("❌ No documents found!")
        return

    # Print summary
    print("\n" + "-" * 40)
    print("📊 Summary by Category:")
    by_category = defaultdict(int)
    for doc in all_documents:
        by_category[doc["category"]] += 1

    for cat, count in sorted(by_category.items()):
        print(f"   {cat}: {count}")

    print("\n📊 Summary by Type:")
    by_type = defaultdict(int)
    for doc in all_documents:
        by_type[doc["type"]] += 1

    for t, count in sorted(by_type.items()):
        print(f"   {t}: {count}")
    print("-" * 40)

    # Step 4: Create index chunk
    print("\nStep 4/6: Creating index chunk...")
    index_chunk = create_index_chunk(all_documents)
    all_documents.append(index_chunk)
    print(f"   ✅ Index created with {len(all_documents) - 1} documents listed")

    # Step 5: Split into chunks
    print("\nStep 5/6: Splitting into chunks...")
    chunks = split_into_chunks(all_documents)

    # Step 6: Create embeddings
    print("\nStep 6/6: Creating embeddings...")
    chunks_with_embeddings = create_embeddings(chunks)

    # Save
    print("\nSaving to JSON...")
    save_chunks(chunks_with_embeddings, OUTPUT_FILE)

    # Final summary
    print("\n" + "=" * 60)
    print("🎉 DONE!")
    print("=" * 60)
    print(f"\n📈 Final Summary:")
    print(f"   Total documents: {len(all_documents)}")
    print(f"   Total chunks: {len(chunks_with_embeddings)}")
    print(f"   Categories: {list(by_category.keys())}")
    print(f"\n📁 Output: {OUTPUT_FILE}")
    print(f"\n🚀 Next: Upload chunks.json to your HuggingFace Space")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
