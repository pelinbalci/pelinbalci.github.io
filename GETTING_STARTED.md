# 🚀 Getting Started Guide

Welcome to your Tiny AI World platform! This guide will help you deploy and start adding content.

## 📦 What You Have

Your project includes:
- ✅ Interactive knowledge graph visualization
- ✅ Clean, modern UI with dark/light mode
- ✅ Search functionality
- ✅ Category filtering
- ✅ Mobile-responsive design
- ✅ Note template system
- ✅ Sample content to get started

## 🎯 Step 1: Deploy to GitHub Pages

### Option A: Replace Existing Site

1. **Extract the files** from `knowledge-graph-site` folder

2. **Copy all files** to your existing `username.github.io` repository

3. **Push to GitHub:**
```bash
cd /path/to/username.github.io
git add .
git commit -m "Deploy knowledge graph platform"
git push origin main
```

4. **Wait 1-2 minutes** for GitHub Pages to build

5. **Visit** `https://username.github.io` to see your site!

### Option B: Keep Both Versions

If you want to keep your current site and add this as a subdirectory:

1. Create a folder like `knowledge-graph/` in your repo
2. Copy all files there
3. Access at `https://username.github.io/knowledge-graph/`

## ✏️ Step 2: Add Your First Note

### Method 1: Using the Template

1. **Copy the template:**
```bash
cp notes/_template.md notes/my-first-note.md
```

2. **Edit the frontmatter:**
```markdown
---
title: "My First Note"
id: "my-first-note"
category: "programming"
tags: ["tutorial", "learning"]
related: ["ml"]
date: "2025-11-08"
description: "My first note in the knowledge graph"
---
```

3. **Write your content** using Markdown

4. **Save and push:**
```bash
git add notes/my-first-note.md
git commit -m "Add my first note"
git push origin main
```

### Method 2: Create from Scratch

Just create a new `.md` file in the `notes/` folder with the required frontmatter!

## 🎨 Step 3: Customize Your Site

### Update Personal Information

**Edit `index.html`:**
- Line 8: Change page title
- Line 21: Update logo/site name
- Line 77-79: Update footer links

**Edit `README.md`:**
- Replace `yourusername` with your GitHub username
- Add your contact information
- Update the description

### Change Colors

**Edit `assets/css/style.css`:**
```css
:root {
    --accent-primary: #6366f1;  /* Change this! */
    --accent-secondary: #8b5cf6; /* And this! */
}
```

### Add Your Photo/Logo

1. Add image to `assets/images/`
2. Update `index.html` or create an `about.html` page

## 📝 Step 4: Understanding the Graph

### How Connections Work

The graph automatically creates connections based on the `related` field in your notes:

```markdown
---
related: ["python", "ml", "dl"]
---
```

This creates edges between your note and the notes with IDs: `python`, `ml`, `dl`.

### Categories

Available categories (colors):
- `ai` - Blue (#6366f1)
- `ml` - Purple (#8b5cf6)
- `programming` - Pink (#ec4899)
- `data` - Teal (#14b8a6)
- `web` - Orange (#f59e0b)
- `math` - Cyan (#06b6d4)

Choose the category that best fits your note's topic.

## 🔍 Step 5: Add More Content

### Recommended Structure

```
notes/
├── machine-learning/
│   ├── basics.md
│   ├── algorithms.md
│   └── applications.md
├── programming/
│   ├── python.md
│   ├── javascript.md
│   └── data-structures.md
└── projects/
    ├── project1.md
    └── project2.md
```

### Best Practices

1. **Keep notes focused**: One topic per note
2. **Link liberally**: Connect related concepts
3. **Use descriptive IDs**: `neural-networks` not `nn`
4. **Add good descriptions**: Helps with search
5. **Tag appropriately**: 3-5 relevant tags per note

## 🎯 Step 6: Test Your Site

### Local Testing

You can test locally by opening `index.html` in a browser, but some features (like loading markdown) work better when served:

**Option 1: Python**
```bash
python -m http.server 8000
# Visit http://localhost:8000
```

**Option 2: Node.js**
```bash
npx serve
```

**Option 3: VS Code**
- Install "Live Server" extension
- Right-click `index.html` → "Open with Live Server"

### Check These Features

- ✅ Graph loads and displays nodes
- ✅ Clicking nodes (currently links to `notes/[id].html`)
- ✅ Search works (press `/` or click search icon)
- ✅ Theme toggle (moon/sun icon)
- ✅ Category filters
- ✅ Mobile responsive (try different screen sizes)

## 🐛 Troubleshooting

### Graph doesn't load
- Check browser console for errors (F12)
- Ensure D3.js CDN is accessible
- Verify `graph.js` is loading

### Notes don't connect
- Check that IDs in `related` field match actual note IDs
- IDs are case-sensitive
- Remove `.md` extension from IDs

### Styling looks broken
- Clear browser cache (Ctrl+Shift+R)
- Check that CSS files are loading
- Verify file paths are correct

### Search isn't working
- Make sure `search.js` is loading
- Check that notes have proper frontmatter
- Look for JavaScript errors in console

## 📱 Mobile Optimization

The site is already mobile-responsive, but test on actual devices:

- **Graph**: Touch to pan, pinch to zoom
- **Navigation**: Hamburger menu on small screens
- **Search**: Full-screen overlay on mobile
- **Reading**: Optimized line length and spacing

## 🚀 Next Steps

### Immediate (This Week)
1. ✅ Deploy to GitHub Pages
2. ✅ Add 5-10 initial notes
3. ✅ Customize colors and branding
4. ✅ Test all features

### Short Term (This Month)
1. Add 20+ notes across different topics
2. Create a consistent note structure
3. Add code examples to technical notes
4. Link notes to create a connected graph

### Long Term (Next Few Months)
1. Add projects page
2. Create about page
3. Add more advanced features from Phase 2
4. Gather feedback from users

## 💡 Tips for Success

1. **Start small**: Begin with topics you know well
2. **Be consistent**: Use the same template for all notes
3. **Update regularly**: Add new notes weekly
4. **Connect everything**: The power is in the connections
5. **Share early**: Get feedback from friends/colleagues

## 📚 Learning Resources

### Markdown
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Markdown](https://guides.github.com/features/mastering-markdown/)

### D3.js (for customization)
- [D3.js Documentation](https://d3js.org/)
- [Observable HQ](https://observablehq.com/)

### GitHub Pages
- [GitHub Pages Docs](https://docs.github.com/en/pages)

## ❓ Common Questions

**Q: Can I use custom domains?**
A: Yes! GitHub Pages supports custom domains. See [GitHub's guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

**Q: How do I add images?**
A: Place images in `assets/images/` and reference them:
```markdown
![Description](../assets/images/myimage.png)
```

**Q: Can I add videos?**
A: Yes! Use HTML:
```html
<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID"></iframe>
```

**Q: How do I backup my content?**
A: Your GitHub repository IS your backup! But you can also:
- Download ZIP from GitHub
- Clone to multiple machines
- Use GitHub's export features

**Q: Can others contribute?**
A: Yes! Enable pull requests in your repo settings, and others can suggest notes.

## 🎉 You're Ready!

You now have everything you need to build an amazing ai platform. 

**Remember:**
- The best knowledge base is one that's actually used
- Start simple, iterate often
- Share your journey
- Have fun learning and sharing!

---

**Need Help?**
- Check the main [README.md](README.md)
- Review the sample note in `notes/ml.md`
- Look at the template in `notes/_template.md`
- Open an issue on GitHub if you're stuck

**Happy Learning! 🚀**
