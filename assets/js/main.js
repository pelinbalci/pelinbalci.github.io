// Main JavaScript
// General functionality and category filters

class CategoryFilter {
    constructor() {
        this.filterContainer = document.getElementById('categoryFilters');
        this.clearBtn = document.getElementById('clearFilters');
        this.activeFilters = new Set();
        this.categories = [];
        
        this.init();
    }
    
    init() {
        this.loadCategories();
        this.renderFilters();
        
        if (this.clearBtn) {
            this.clearBtn.addEventListener('click', () => this.clearFilters());
        }
    }
    
    loadCategories() {
        // Extract unique categories from graph data
        // For now, hardcode categories
        this.categories = [
            { id: 'ai', name: 'AI', color: '#6366f1' },
            { id: 'ml', name: 'Machine Learning', color: '#8b5cf6' },
            { id: 'programming', name: 'Programming', color: '#ec4899' },
            { id: 'data', name: 'Data', color: '#14b8a6' },
            { id: 'web', name: 'Web', color: '#f59e0b' },
            { id: 'math', name: 'Math', color: '#06b6d4' },
        ];
    }
    
    renderFilters() {
        if (!this.filterContainer) return;
        
        const filtersHTML = this.categories.map(category => `
            <button 
                class="category-tag" 
                data-category="${category.id}"
                style="border-color: ${category.color};"
                onclick="categoryFilter.toggleFilter('${category.id}')"
            >
                ${category.name}
            </button>
        `).join('');
        
        this.filterContainer.innerHTML = filtersHTML;
    }
    
    toggleFilter(categoryId) {
        if (this.activeFilters.has(categoryId)) {
            this.activeFilters.delete(categoryId);
        } else {
            this.activeFilters.add(categoryId);
        }
        
        this.updateUI();
        this.applyFilters();
    }
    
    clearFilters() {
        this.activeFilters.clear();
        this.updateUI();
        this.applyFilters();
    }
    
    updateUI() {
        const tags = this.filterContainer.querySelectorAll('.category-tag');
        tags.forEach(tag => {
            const category = tag.dataset.category;
            if (this.activeFilters.has(category)) {
                tag.classList.add('active');
            } else {
                tag.classList.remove('active');
            }
        });
    }
    
    applyFilters() {
        // Apply filters to the graph
        if (typeof graph !== 'undefined' && graph) {
            graph.filterByCategory(this.activeFilters);
        }
    }
}

// Utility Functions
const utils = {
    // Format date
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
    },
    
    // Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Get query parameter
    getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    },
    
    // Smooth scroll to element
    scrollToElement(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    }
};

// Initialize category filter
let categoryFilter;
document.addEventListener('DOMContentLoaded', () => {
    categoryFilter = new CategoryFilter();
});

// Handle window resize
window.addEventListener('resize', utils.debounce(() => {
    // Recalculate graph dimensions if needed
    if (typeof graph !== 'undefined' && graph) {
        const container = document.getElementById('graph');
        if (container) {
            graph.width = container.clientWidth;
            graph.height = container.clientHeight;
        }
    }
}, 250));

// Export utils for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = utils;
}
