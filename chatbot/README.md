# 🧠 Chatbot Chunk Generator

This folder contains the script to generate embeddings from your notes.

## Usage

### First Time Setup

```bash
cd chatbot
pip install -r requirements.txt
python create_chunks.py
```

### After Adding New Notes

```bash
cd chatbot
python create_chunks.py
```

Then upload `chunks.json` to your HuggingFace Space.

## Files

| File | Purpose |
|------|---------|
| `create_chunks.py` | Generates chunks.json from ../notes/*.md |
| `requirements.txt` | Python dependencies |
| `chunks.json` | Generated file (upload to HuggingFace) |

## Note

`chunks.json` is gitignored since it's large (~5-10MB) and should be uploaded directly to HuggingFace Space.
