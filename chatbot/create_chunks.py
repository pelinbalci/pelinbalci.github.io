"""
create_chunks.py - Generate chunks.json from your markdown AND HTML files

Location: pelinbalci.github.io/chatbot/create_chunks.py

Run this script whenever you add or update your notes:
    cd chatbot
    python create_chunks.py

It will:
1. Load all .md files from ../notes folder
2. Load all .html notebooks from ../assets/components folder
3. Load cv.html, projects.html, about.html from root
4. Split them into chunks
5. Create embeddings using sentence-transformers
6. Save chunks.json (upload this to HuggingFace Space)
"""

import os
import json
import glob
import re
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# =============================================================================
# CONFIGURATION
# =============================================================================

# Paths (relative to this script's location)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.join(SCRIPT_DIR, "..")

# Folders and files to process
NOTES_PATH = os.path.join(REPO_ROOT, "notes")
COMPONENTS_PATH = os.path.join(REPO_ROOT, "assets", "components")
ROOT_HTML_FILES = ["cv.html", "projects.html", "about.html"]

# Output file
OUTPUT_FILE = "chunks.json"

# Embedding model - same model used in HuggingFace Space (must match!)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Chunk settings
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


# =============================================================================
# HTML TEXT EXTRACTION
# =============================================================================

def extract_text_from_html(html_content: str) -> str:
    """
    Extract readable text from HTML content.
    Works without BeautifulSoup using regex (simpler dependency).
    """
    # Remove script and style elements
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    # Replace common elements with spacing
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?p[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?div[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?h[1-6][^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?li[^>]*>', '\n• ', text, flags=re.IGNORECASE)
    text = re.sub(r'</?tr[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?td[^>]*>', ' | ', text, flags=re.IGNORECASE)

    # Remove all remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Decode common HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")

    # Clean up whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Multiple newlines to double
    text = re.sub(r' +', ' ', text)  # Multiple spaces to single
    text = '\n'.join(line.strip() for line in text.split('\n'))  # Strip each line
    text = text.strip()

    return text


# =============================================================================
# DOCUMENT LOADING
# =============================================================================

def load_markdown_files(notes_path: str) -> list:
    """Load all markdown files from notes folder."""
    documents = []

    if not os.path.exists(notes_path):
        print(f"   ⚠️  Notes path not found: {notes_path}")
        return documents

    pattern = os.path.join(notes_path, "**", "*.md")
    md_files = glob.glob(pattern, recursive=True)

    print(f"📄 Found {len(md_files)} markdown files in notes/")

    for filepath in md_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            filename = os.path.basename(filepath)

            # Skip template files or empty files
            if filename.startswith('_') or len(content.strip()) < 50:
                print(f"   ⏭️  Skipping: {filename}")
                continue

            documents.append({
                "content": content,
                "source": filename,
                "type": "markdown"
            })
            print(f"   ✅ Loaded: {filename}")

        except Exception as e:
            print(f"   ❌ Error loading {filepath}: {e}")

    return documents


def load_html_notebooks(components_path: str) -> list:
    """Load HTML notebooks from assets/components folder."""
    documents = []

    if not os.path.exists(components_path):
        print(f"   ⚠️  Components path not found: {components_path}")
        return documents

    pattern = os.path.join(components_path, "*.html")
    html_files = glob.glob(pattern)

    print(f"📓 Found {len(html_files)} HTML notebooks in assets/components/")

    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Extract text from HTML
            text_content = extract_text_from_html(html_content)

            filename = os.path.basename(filepath)

            # Skip if too little content after extraction
            if len(text_content.strip()) < 100:
                print(f"   ⏭️  Skipping (too short): {filename}")
                continue

            documents.append({
                "content": text_content,
                "source": f"notebook: {filename}",
                "type": "html_notebook"
            })
            print(f"   ✅ Loaded: {filename}")

        except Exception as e:
            print(f"   ❌ Error loading {filepath}: {e}")

    return documents


def load_root_html_files(repo_root: str, filenames: list) -> list:
    """Load specific HTML files from repo root (cv.html, projects.html, etc.)"""
    documents = []

    print(f"📋 Loading root HTML files...")

    for filename in filenames:
        filepath = os.path.join(repo_root, filename)

        if not os.path.exists(filepath):
            print(f"   ⏭️  Not found: {filename}")
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Extract text from HTML
            text_content = extract_text_from_html(html_content)

            # Skip if too little content
            if len(text_content.strip()) < 100:
                print(f"   ⏭️  Skipping (too short): {filename}")
                continue

            # Add context based on file type
            if filename == "cv.html":
                source_name = "CV / Resume"
            elif filename == "projects.html":
                source_name = "Projects Page"
            elif filename == "about.html":
                source_name = "About Page"
            else:
                source_name = filename

            documents.append({
                "content": text_content,
                "source": source_name,
                "type": "html_page"
            })
            print(f"   ✅ Loaded: {filename} → {source_name}")

        except Exception as e:
            print(f"   ❌ Error loading {filepath}: {e}")

    return documents


# =============================================================================
# CHUNKING AND EMBEDDING
# =============================================================================

def split_into_chunks(documents: list) -> list:
    """Split documents into smaller chunks."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "]
    )

    chunks = []
    for doc in documents:
        splits = text_splitter.split_text(doc["content"])
        for i, split in enumerate(splits):
            # Clean up the chunk
            clean_split = split.strip()
            if len(clean_split) < 50:  # Skip very short chunks
                continue

            chunks.append({
                "text": clean_split,
                "source": doc["source"],
                "type": doc["type"],
                "chunk_id": f"{doc['source']}_{i}"
            })

    print(f"✂️  Created {len(chunks)} chunks")
    return chunks


def create_embeddings(chunks: list) -> list:
    """Create embeddings for each chunk using sentence-transformers."""

    print(f"🔄 Loading embedding model: {EMBEDDING_MODEL}")
    print("   (First run will download the model ~90MB)")

    model = SentenceTransformer(EMBEDDING_MODEL)
    texts = [chunk["text"] for chunk in chunks]

    print(f"🔄 Creating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True)

    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()

    print(f"✅ Created {len(embeddings)} embeddings")
    return chunks


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
    print("🧠 CHUNK GENERATOR - Pelin's Notes Chatbot")
    print("=" * 60 + "\n")

    all_documents = []

    # Step 1: Load markdown files from notes/
    print("Step 1/5: Loading markdown files from notes/...")
    md_docs = load_markdown_files(NOTES_PATH)
    all_documents.extend(md_docs)

    # Step 2: Load HTML notebooks from assets/components/
    print("\nStep 2/5: Loading HTML notebooks from assets/components/...")
    notebook_docs = load_html_notebooks(COMPONENTS_PATH)
    all_documents.extend(notebook_docs)

    # Step 3: Load root HTML files (cv.html, projects.html, about.html)
    print("\nStep 3/5: Loading root HTML files...")
    root_docs = load_root_html_files(REPO_ROOT, ROOT_HTML_FILES)
    all_documents.extend(root_docs)

    # Summary
    print(f"\n📊 Total documents loaded: {len(all_documents)}")
    print(f"   - Markdown notes: {len(md_docs)}")
    print(f"   - HTML notebooks: {len(notebook_docs)}")
    print(f"   - Root HTML pages: {len(root_docs)}")

    if not all_documents:
        print("❌ No documents found!")
        return

    # Step 4: Split into chunks
    print("\nStep 4/5: Splitting into chunks...")
    chunks = split_into_chunks(all_documents)

    # Step 5: Create embeddings
    print("\nStep 5/5: Creating embeddings...")
    chunks_with_embeddings = create_embeddings(chunks)

    # Save
    print("\nSaving to JSON...")
    save_chunks(chunks_with_embeddings, OUTPUT_FILE)

    print("\n" + "=" * 60)
    print("🎉 DONE!")
    print("=" * 60)
    print(f"\nNext step:")
    print(f"  Upload 'chatbot/{OUTPUT_FILE}' to your HuggingFace Space")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()