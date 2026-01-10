"""
create_chunks.py - Generate chunks.json from your markdown files

Location: pelinbalci.github.io/chatbot/create_chunks.py

Run this script whenever you add or update your notes:
    cd chatbot
    python create_chunks.py

It will:
1. Load all .md files from ../notes folder
2. Split them into chunks
3. Create embeddings using sentence-transformers (free, runs locally)
4. Save chunks.json (upload this to HuggingFace Space)
"""

import os
import json
import glob
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# =============================================================================
# CONFIGURATION
# =============================================================================

# Path to notes folder (relative to this script's location)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NOTES_PATH = os.path.join(SCRIPT_DIR, "..", "notes")

# Output file
OUTPUT_FILE = "chunks.json"

# Embedding model - same model used in HuggingFace Space (must match!)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Chunk settings
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# =============================================================================
# FUNCTIONS
# =============================================================================

def load_markdown_files(notes_path: str) -> list:
    """Load all markdown files and their content."""
    documents = []
    
    # Normalize path
    notes_path = os.path.normpath(notes_path)
    
    # Find all .md files
    pattern = os.path.join(notes_path, "**", "*.md")
    md_files = glob.glob(pattern, recursive=True)
    
    print(f"📄 Found {len(md_files)} markdown files in {notes_path}")
    
    for filepath in md_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get relative filename for source
            filename = os.path.basename(filepath)
            
            # Skip template files or empty files
            if filename.startswith('_') or len(content.strip()) < 50:
                print(f"   ⏭️  Skipping: {filename} (template or too short)")
                continue
                
            documents.append({
                "content": content,
                "source": filename
            })
            print(f"   ✅ Loaded: {filename}")
            
        except Exception as e:
            print(f"   ❌ Error loading {filepath}: {e}")
    
    return documents


def split_into_chunks(documents: list) -> list:
    """Split documents into smaller chunks."""
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "]
    )
    
    chunks = []
    for doc in documents:
        splits = text_splitter.split_text(doc["content"])
        for i, split in enumerate(splits):
            chunks.append({
                "text": split,
                "source": doc["source"],
                "chunk_id": f"{doc['source']}_{i}"
            })
    
    print(f"✂️  Created {len(chunks)} chunks")
    return chunks


def create_embeddings(chunks: list) -> list:
    """Create embeddings for each chunk using sentence-transformers."""
    
    print(f"🔄 Loading embedding model: {EMBEDDING_MODEL}")
    print("   (First run will download the model ~90MB)")
    
    # Load the model (runs locally, no API needed)
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    # Extract just the text for embedding
    texts = [chunk["text"] for chunk in chunks]
    
    print(f"🔄 Creating embeddings for {len(texts)} chunks...")
    
    # Create embeddings
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Add embeddings to chunks (convert to list for JSON serialization)
    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()
    
    print(f"✅ Created {len(embeddings)} embeddings")
    return chunks


def save_chunks(chunks: list, output_file: str):
    """Save chunks with embeddings to JSON file."""
    
    output_path = os.path.join(SCRIPT_DIR, output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    
    file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    print(f"💾 Saved to {output_path} ({file_size:.2f} MB)")


def main():
    print("\n" + "=" * 60)
    print("🧠 CHUNK GENERATOR - Pelin's Notes Chatbot")
    print("=" * 60 + "\n")
    
    # Check if notes path exists
    if not os.path.exists(NOTES_PATH):
        print(f"❌ Notes path not found: {NOTES_PATH}")
        print("   Make sure you're running this from the chatbot/ folder")
        return
    
    # Step 1: Load markdown files
    print("Step 1/4: Loading markdown files...")
    documents = load_markdown_files(NOTES_PATH)
    
    if not documents:
        print("❌ No documents found!")
        return
    
    # Step 2: Split into chunks
    print("\nStep 2/4: Splitting into chunks...")
    chunks = split_into_chunks(documents)
    
    # Step 3: Create embeddings
    print("\nStep 3/4: Creating embeddings...")
    chunks_with_embeddings = create_embeddings(chunks)
    
    # Step 4: Save to JSON
    print("\nStep 4/4: Saving to JSON...")
    save_chunks(chunks_with_embeddings, OUTPUT_FILE)
    
    print("\n" + "=" * 60)
    print("🎉 DONE!")
    print("=" * 60)
    print(f"\nNext step:")
    print(f"  Upload 'chatbot/{OUTPUT_FILE}' to your HuggingFace Space")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
