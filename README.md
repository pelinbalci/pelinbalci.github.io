# 🧠 Tiny AI World - Interactive Learning Platform

A beautiful, interactive AI platform for organizing and sharing learning notes. Built with D3.js, powered by an AI chatbot, and deployed on GitHub Pages.

## ✨ Features

- **Interactive Knowledge Graph**: Visualize connections between topics
- **🤖 AI Chatbot**: Ask questions about my notes using RAG
- **Easy Content Management**: Write notes in Markdown
- **Search & Filter**: Find topics quickly by category
- **Dark/Light Mode**: Comfortable reading in any environment
- **Mobile Responsive**: Works on all devices
- **Free & Open Source**: No cost, fully transparent

## 🚀 Quick Start

### Browsing
1. Visit [pelinbalci.com](https://pelinbalci.com)
2. Explore the knowledge graph - click nodes to read notes
3. Use the 💬 chat button to ask questions

### Contributing
```bash
git clone https://github.com/pelinbalci/pelinbalci.github.io.git
cd pelinbalci.github.io
cp notes/_template.md notes/your-topic.md  # Create new note
# Edit the note, then:
python generate-data.py  # Update graph data
git add . && git commit -m "Add note" && git push
```

---

## 🤖 AI Chatbot

The website features an AI-powered chatbot that answers questions based on my notes, projects, and CV using **RAG (Retrieval-Augmented Generation)**.

### How It Works

```
┌─────────────────────┐              ┌─────────────────────┐
│  GitHub Repo        │   weekly     │  HuggingFace Space  │
│  ─────────────────  │   sync       │  ─────────────────  │
│  notes/*.md         │ ──────────►  │  chunks.json        │
│  assets/components/ │  (GitHub     │         │           │
│  cv.html            │   Actions)   │         ▼           │
└─────────────────────┘              │  User Question      │
                                     │         │           │
                                     │         ▼           │
                                     │  Find Similar Chunks│
                                     │         │           │
                                     │         ▼           │
                                     │  Groq LLM (Llama)   │
                                     │         │           │
                                     │         ▼           │
                                     │  Answer             │
                                     └─────────────────────┘
```

### Tech Stack

| Component | Technology |
|-----------|------------|
| Embeddings | sentence-transformers |
| LLM | Llama 3.1 via Groq API |
| Hosting | HuggingFace Spaces (free) |
| Automation | GitHub Actions |

### Updating the Chatbot

Content syncs automatically via GitHub Actions, or manually:
```bash
cd chatbot
python create_chunks.py
# Upload chunks.json to HuggingFace Space
```

---

## 📝 Creating Notes

### Template Structure
```markdown
---
title: "Your Note Title" # Display name of the note
id: "unique-note-id" # Unique identifier (used in URLs and connections)
category: "ml" # "genai", "deep-learning", "conference", "machine-learning", "edge-ml", "visualization"
tags: ["tag1", "tag2"]
related: ["other-note-id"]
date: "2025-11-08"
description: "Brief description"
---

# Your Note Title

Your content here...
```

### Categories

"genai", "deep-learning", "conference", "machine-learning", "edge-ml", "visualization"

---

## 🏗️ Project Structure

```
pelinbalci.github.io/
├── index.html              # Main page with graph
├── notes/                  # Markdown notes
├── assets/
│   ├── css/               # Styles
│   ├── js/                # Graph, search, theme
│   ├── components/        # HTML notebooks
│   └── data/notes.json    # Generated graph data
├── chatbot/
│   └── create_chunks.py   # AI chatbot embeddings generator
├── .github/workflows/
│   └── update-chatbot.yml # Auto-sync to HuggingFace
└── cv.html, projects.html, about.html
```

---

## 🔧 Built With

- **D3.js** - Graph visualization
- **Vanilla JS** - No heavy frameworks
- **GitHub Pages** - Free hosting
- **HuggingFace Spaces** - AI chatbot hosting
- **Groq API** - Fast LLM inference

---

## 🎯 Roadmap

- [x] Interactive knowledge graph
- [x] AI Chatbot with RAG
- [x] Automated content sync
- [x] Markdown note support
- [x] Search functionality
- [x] Dark/light mode
- [x] Mobile responsive

---

- [ ] Math equation support (KaTeX)
- [ ] Progress tracking (localStorage)
- [ ] Bookmarking system
- [ ] Enhanced search (fuzzy matching)
- [ ] User accounts (optional)
- [ ] Collaborative learning
- [ ] Export functionality
- [ ] Advanced analytics

---

## 📄 License

MIT License - feel free to use, modify, and share!

## 🔗 Links

- **Website**: [pelinbalci.com](https://pelinbalci.com)
- **Chatbot**: [HuggingFace Space](https://huggingface.co/spaces/pelinbalci/pelin-notes-chat)
- **GitHub**: [@pelinbalci](https://github.com/pelinbalci)
- **LinkedIn**: [pelin-balci](https://www.linkedin.com/in/pelin-balci/)
- **Medium**: [@balci.pelin](https://medium.com/@balci.pelin)

---

**Made with ❤️ for learners and knowledge sharers**

⭐ Star this repo if you find it useful!