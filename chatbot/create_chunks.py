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
        ("cv.html", "CV / Resume", "cv"),
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