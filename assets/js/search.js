// Search Functionality
// Allows users to search through notes and topics

class SearchManager {
    constructor() {
        this.searchBtn = document.getElementById('searchBtn');
        this.searchOverlay = document.getElementById('searchOverlay');
        this.searchInput = document.getElementById('searchInput');
        this.closeSearchBtn = document.getElementById('closeSearch');
        this.searchResults = document.getElementById('searchResults');
        this.searchData = [];
        
        this.init();
    }
    
    init() {
        // Load search data
        this.loadSearchData();
        
        // Event listeners
        if (this.searchBtn) {
            this.searchBtn.addEventListener('click', () => this.openSearch());
        }
        
        if (this.closeSearchBtn) {
            this.closeSearchBtn.addEventListener('click', () => this.closeSearch());
        }
        
        if (this.searchInput) {
            this.searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Open search with '/'
            if (e.key === '/' && !this.searchOverlay.classList.contains('hidden')) {
                e.preventDefault();
                this.openSearch();
            }
            // Close search with 'Escape'
            if (e.key === 'Escape') {
                this.closeSearch();
            }
        });
        
        // Close on overlay click
        if (this.searchOverlay) {
            this.searchOverlay.addEventListener('click', (e) => {
                if (e.target === this.searchOverlay) {
                    this.closeSearch();
                }
            });
        }
    }
    
    async loadSearchData() {
        // This will eventually load from all markdown files
        // For now, use the same data as the graph
        try {
            this.searchData = [
                { id: 'ml', title: 'Machine Learning', category: 'ml', tags: ['AI', 'algorithms'], description: 'Introduction to ML concepts and algorithms' },
                { id: 'dl', title: 'Deep Learning', category: 'ml', tags: ['neural networks', 'AI'], description: 'Neural networks and deep architectures' },
                { id: 'python', title: 'Python Basics', category: 'programming', tags: ['programming', 'python'], description: 'Python programming fundamentals' },
                { id: 'numpy', title: 'NumPy', category: 'programming', tags: ['python', 'data'], description: 'Numerical computing with Python' },
                { id: 'cv', title: 'Computer Vision', category: 'ai', tags: ['AI', 'images'], description: 'Image processing and analysis' },
                { id: 'nlp', title: 'NLP', category: 'ai', tags: ['AI', 'text', 'language'], description: 'Natural language processing' },
                { id: 'data-viz', title: 'Data Visualization', category: 'data', tags: ['data', 'visualization'], description: 'Visualizing data effectively' },
                { id: 'statistics', title: 'Statistics', category: 'math', tags: ['math', 'data'], description: 'Statistical methods and analysis' },
            ];
        } catch (error) {
            console.error('Error loading search data:', error);
        }
    }
    
    openSearch() {
        this.searchOverlay.classList.remove('hidden');
        this.searchInput.focus();
    }
    
    closeSearch() {
        this.searchOverlay.classList.add('hidden');
        this.searchInput.value = '';
        this.searchResults.innerHTML = '';
    }
    
    handleSearch(query) {
        if (!query.trim()) {
            this.searchResults.innerHTML = '';
            return;
        }
        
        const results = this.search(query);
        this.displayResults(results);
    }
    
    search(query) {
        const lowerQuery = query.toLowerCase();
        
        return this.searchData.filter(item => {
            // Search in title
            if (item.title.toLowerCase().includes(lowerQuery)) return true;
            
            // Search in description
            if (item.description.toLowerCase().includes(lowerQuery)) return true;
            
            // Search in tags
            if (item.tags.some(tag => tag.toLowerCase().includes(lowerQuery))) return true;
            
            // Search in category
            if (item.category.toLowerCase().includes(lowerQuery)) return true;
            
            return false;
        }).slice(0, 10); // Limit to 10 results
    }
    
    displayResults(results) {
        if (results.length === 0) {
            this.searchResults.innerHTML = '<p style="color: var(--text-secondary); padding: 1rem;">No results found</p>';
            return;
        }
        
        const resultsHTML = results.map(item => `
            <div class="search-result-item" onclick="window.location.href='notes/${item.id}.html'" style="
                padding: 1rem;
                margin-bottom: 0.5rem;
                background-color: var(--bg-primary);
                border-radius: var(--radius-md);
                cursor: pointer;
                transition: all 0.2s ease;
            " onmouseover="this.style.backgroundColor='var(--bg-secondary)'" onmouseout="this.style.backgroundColor='var(--bg-primary)'">
                <h4 style="margin-bottom: 0.25rem; color: var(--text-primary);">${item.title}</h4>
                <p style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 0.5rem;">${item.description}</p>
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span style="
                        padding: 0.125rem 0.5rem;
                        background-color: var(--accent-primary);
                        color: white;
                        border-radius: 0.25rem;
                        font-size: 0.75rem;
                        font-weight: 600;
                    ">${item.category}</span>
                    ${item.tags.map(tag => `
                        <span style="
                            padding: 0.125rem 0.5rem;
                            background-color: var(--bg-secondary);
                            border-radius: 0.25rem;
                            font-size: 0.75rem;
                            color: var(--text-secondary);
                        ">${tag}</span>
                    `).join('')}
                </div>
            </div>
        `).join('');
        
        this.searchResults.innerHTML = resultsHTML;
    }
}

// Initialize search manager
document.addEventListener('DOMContentLoaded', () => {
    new SearchManager();
});
