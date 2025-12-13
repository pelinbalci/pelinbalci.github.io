// Main JavaScript
// General functionality and category filters

// ==========================================
// SHARED CATEGORY COLOR DEFINITIONS
// ==========================================
// This is the SINGLE SOURCE OF TRUTH for category colors.
// All components (graph, filters, notes list) use these colors.
const CATEGORY_COLORS = {
            'deep-learning': '#ec4899',      // Pink - stands out
            'edge-ml': '#3b82f6',            // Blue - classic tech
            'machine-learning': '#10b981',   // Emerald - fresh green
            'genai': '#a855f7',              // Purple - AI/futuristic
            'visualization': '#06b6d4',      // Cyan - data/charts
            'conference': '#f97316',         // Orange - events/energy
            'default': '#6b7280'
};

const DEFAULT_CATEGORY_COLOR = '#6b7280'; // Gray

function getCategoryColor(category) {
    const normalized = (category || '').toString().trim().toLowerCase();
    return CATEGORY_COLORS[normalized] || DEFAULT_CATEGORY_COLOR;
}

// ==========================================
// CATEGORY FILTER CLASS
// ==========================================
class CategoryFilter {
    constructor() {
        this.filterContainer = document.getElementById('categoryFilters');
        this.clearBtn = document.getElementById('clearFilters');
        this.activeFilters = new Set();
        this.categories = [];

        this.init();
    }

    async init() {
        await this.loadCategories();
        this.renderFilters();

        if (this.clearBtn) {
            this.clearBtn.addEventListener('click', () => this.clearFilters());
        }
    }

    async loadCategories() {
        try {
            const response = await fetch('/assets/data/notes.json');
            if (!response.ok) throw new Error('Could not load notes data');

            const data = await response.json();
            const uniqueCategories = Array.from(new Set((data.nodes || [])
                .map(note => this.normalizeCategory(note.category))
                .filter(Boolean)));

            // Use the SHARED color map instead of index-based colors
            this.categories = uniqueCategories.map(id => ({
                id,
                name: this.formatCategoryName(id),
                color: getCategoryColor(id)
            }));
        } catch (error) {
            console.warn('Could not derive categories:', error);
            this.categories = [];
        }

        // Share palette globally for other components (graph, lists)
        window.categoryPalette = Object.fromEntries(
            this.categories.map(category => [category.id, category.color])
        );

        // Also expose the full color map
        window.CATEGORY_COLORS = CATEGORY_COLORS;

        document.dispatchEvent(new CustomEvent('categoriesLoaded', {
            detail: { categories: this.categories }
        }));
    }

    normalizeCategory(category) {
        return (category || '').toString().trim().toLowerCase();
    }

    formatCategoryName(categoryId) {
        if (!categoryId) return 'Uncategorized';
        return categoryId
            .split(/[-_\s]/)
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    renderFilters() {
        if (!this.filterContainer) return;

        if (this.categories.length === 0) {
            this.filterContainer.innerHTML = '<p class="muted">No categories available</p>';
            if (this.clearBtn) this.clearBtn.style.display = 'none';
            return;
        }

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
        const normalizedId = this.normalizeCategory(categoryId);

        if (this.activeFilters.has(normalizedId)) {
            this.activeFilters.delete(normalizedId);
        } else {
            this.activeFilters.add(normalizedId);
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
        if (!this.filterContainer) return;

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
        const activeArray = Array.from(this.activeFilters);

        // Apply filters to the graph
        if (typeof graph !== 'undefined' && graph) {
            graph.filterByCategory(this.activeFilters);
        }

        // Notify other components (e.g., list views)
        document.dispatchEvent(new CustomEvent('categoryFilterChange', {
            detail: { activeFilters: activeArray }
        }));
    }

    setFilters(newFilters) {
        this.activeFilters = new Set(Array.from(newFilters || []).map(id => this.normalizeCategory(id)));
        this.updateUI();
        this.applyFilters();
    }
}

// ==========================================
// UTILITY FUNCTIONS
// ==========================================
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

// ==========================================
// INITIALIZATION
// ==========================================
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