# 🧠 Knowledge Graph - Interactive Learning Platform

A beautiful, interactive knowledge graph platform for organizing and sharing learning notes. Built with D3.js and deployed on GitHub Pages.

## ✨ Features

- **Interactive Knowledge Graph**: Visualize connections between topics
- **Easy Content Management**: Write notes in Markdown
- **Auto-expanding Graph**: Graph updates automatically when you add notes
- **Search Functionality**: Find topics quickly
- **Category Filtering**: Focus on specific areas
- **Dark/Light Mode**: Comfortable reading in any environment
- **Mobile Responsive**: Works on all devices
- **Code Highlighting**: Beautiful syntax highlighting for code examples
- **Free & Open Source**: No cost, fully transparent

## 🚀 Quick Start

### For Users (Browsing)

1. Visit [pelinbalci.github.io](https://pelinbalci.github.io)
2. Explore the knowledge graph
3. Click on nodes to read notes
4. Use search to find specific topics

### For Contributors (Adding Content)

1. **Clone the repository**
```bash
git clone https://github.com/pelinbalci/pelinbalci.github.io.git
cd pelinbalci.github.io
```

2. **Create a new note**
```bash
cp notes/_template.md notes/your-topic.md
```

3. **Edit the note**
   - Update the frontmatter (title, id, category, tags, related)
   - Write your content in Markdown
   - Save the file

4. **Push to GitHub**
```bash
git add .
git commit -m "Add note on [your topic]"
git push origin main
```

The graph will automatically update when you push!

## 📝 Creating Notes

### Note Template Structure

```markdown
---
title: "Your Note Title"
id: "unique-note-id"
category: "ml"
tags: ["tag1", "tag2"]
related: ["other-note-id"]
date: "2025-11-08"
description: "Brief description"
---

# Your Note Title

Your content here...
```

### Frontmatter Fields

- **title**: Display name of the note
- **id**: Unique identifier (used in URLs and connections)
- **category**: Main category (ai, ml, programming, data, web, math)
- **tags**: Array of relevant keywords
- **related**: Array of IDs for connected notes
- **date**: Creation or update date
- **description**: Brief summary for search and previews

### Categories

Available categories:
- `ai` - Artificial Intelligence
- `ml` - Machine Learning
- `programming` - Programming & Software
- `data` - Data Science & Analysis
- `web` - Web Development
- `math` - Mathematics & Statistics

### Markdown Features

- **Headings**: `# H1`, `## H2`, `### H3`
- **Bold**: `**bold text**`
- **Italic**: `*italic text*`
- **Lists**: `- item` or `1. item`
- **Links**: `[text](url)`
- **Images**: `![alt](path/to/image.png)`
- **Code blocks**: Use triple backticks with language

Example:
````markdown
```python
def hello():
    print("Hello, World!")
```
````

## 🎨 Customization

### Adding New Categories

1. Edit `assets/js/graph.js`:
   - Add color in `getCategoryColor()`
   - Add stroke in `getCategoryStroke()`

2. Edit `assets/css/graph.css`:
   - Add `.node.category-yourname circle` styles

3. Edit `assets/js/main.js`:
   - Add to `categories` array in `CategoryFilter`

### Changing Colors

Edit CSS variables in `assets/css/style.css`:
```css
:root {
    --accent-primary: #6366f1;  /* Main accent color */
    --accent-secondary: #8b5cf6; /* Secondary accent */
    /* ... other colors */
}
```

## 🏗️ Project Structure

```
yourusername.github.io/
├── index.html              # Main page with graph
├── notes/
│   ├── _template.md       # Template for new notes
│   ├── ml.md              # Sample note
│   └── ...                # Your notes
├── projects/
│   └── ...                # Your projects
├── assets/
│   ├── css/
│   │   ├── style.css      # Main styles
│   │   └── graph.css      # Graph-specific styles
│   ├── js/
│   │   ├── graph.js       # Graph visualization
│   │   ├── search.js      # Search functionality
│   │   ├── theme.js       # Dark/light mode
│   │   └── main.js        # General functions
│   └── images/            # Your images
├── LICENSE                # License file
└── README.md              # This file
```

## 🔧 Technical Details

### Built With

- **D3.js v7** - Graph visualization
- **Vanilla JavaScript** - No heavy frameworks
- **CSS3** - Modern styling with CSS variables
- **Markdown** - Content format
- **GitHub Pages** - Free hosting

### Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

### Performance

- Supports 100+ nodes without lag
- Lazy loading for images
- Optimized graph rendering
- Minimal dependencies

## 📚 Documentation

### For Learners
- Browse the graph to discover topics
- Click nodes to read detailed notes
- Use search to find specific content
- Filter by category to focus your learning

### For Contributors
- Follow the note template
- Keep descriptions concise
- Tag notes appropriately
- Link related topics

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a new note or improve existing ones
3. Follow the note template
4. Submit a pull request

### Contribution Guidelines

- Use clear, descriptive titles
- Include proper frontmatter
- Link to related topics
- Add code examples where relevant
- Proofread for clarity

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

You are free to:
- Use this code for your own learning platform
- Modify and customize it
- Share it with others

## 🙏 Acknowledgments

- Inspired by digital gardens and Zettelkasten
- Built with passion for learning and sharing knowledge
- Thanks to the open-source community

## 📞 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Website: [yourusername.github.io](https://yourusername.github.io)

## 🎯 Roadmap

### Phase 1 (Current)
- [x] Interactive knowledge graph
- [x] Markdown note support
- [x] Search functionality
- [x] Dark/light mode
- [x] Mobile responsive

### Phase 2 (Coming Soon)
- [ ] Enhanced search (fuzzy matching)
- [ ] Note templates for different types
- [ ] Progress tracking (localStorage)
- [ ] Bookmarking system
- [ ] Math equation support (KaTeX)

### Phase 3 (Future)
- [ ] User accounts (optional)
- [ ] Collaborative learning
- [ ] Export functionality
- [ ] Advanced analytics

## 💡 Tips

- Start with broad topics, then add details
- Create connections between related notes
- Use consistent naming for IDs
- Keep notes focused on single topics
- Update the `date` field when editing

## ❓ FAQ

**Q: How do I change the graph colors?**
A: Edit `assets/css/style.css` and `assets/css/graph.css`

**Q: Can I use this for my own notes?**
A: Absolutely! Fork the repo and customize it.

**Q: How many notes can I add?**
A: The graph handles 100+ nodes efficiently. For more, consider optimization.

**Q: Do I need to know JavaScript?**
A: No! Just write Markdown. The graph updates automatically.

**Q: Can I embed videos?**
A: Yes! Use standard Markdown or HTML iframe embeds.

---

**Made with ❤️ for learners and knowledge sharers**

⭐ Star this repo if you find it useful!
