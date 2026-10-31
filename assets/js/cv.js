// CV page renderer.
// Reads assets/data/cv.json (built by generate-data.py from the cv/ folder)
// and fills cv.html. You should not need to edit this file to update the CV.

(function () {
    'use strict';

    var TABS = ['overview', 'experience', 'projects', 'work', 'education'];
    var TYPE_LABELS = {
        video: 'Video', talk: 'Talk', oss: 'Open source', volunteer: 'Volunteering',
        teaching: 'Teaching', post: 'Writing'
    };
    var FILTERS = [
        { id: 'all', label: 'All', types: null },
        { id: 'talks', label: 'Talks & videos', types: ['talk', 'video'] },
        { id: 'oss', label: 'Open source', types: ['oss'] },
        { id: 'volunteer', label: 'Volunteering', types: ['volunteer'] },
        { id: 'teaching', label: 'Teaching', types: ['teaching'] },
        { id: 'writing', label: 'Writing', types: ['post'] }
    ];
    var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    var preview = document.documentElement.classList.contains('preview');
    var state = { filter: 'all', work: [] };

    // ---- helpers ------------------------------------------------------------
    function $(id) { return document.getElementById(id); }

    function esc(value) {
        return String(value == null ? '' : value).replace(/[&<>"']/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
        });
    }

    // Plain text -> safe HTML, with [placeholders] marked
    function text(value) {
        return esc(value).replace(/\[([^\]]{1,120})\]/g, '<mark class="todo">[$1]</mark>');
    }

    function isPlaceholder(url) {
        return !url || /^\s*\[/.test(url);
    }

    function fmtDate(value) {
        var m = /^(\d{4})-(\d{2})/.exec(value || '');
        if (m) return MONTHS[parseInt(m[2], 10) - 1] + ' ' + m[1];
        return esc(value || '');
    }

    function visible(item) { return preview || !item.draft; }

    // ---- hero ---------------------------------------------------------------
    function renderProfile(p) {
        if (!p) return;
        $('cvMeta').textContent = p.meta || '';
        $('cvName').textContent = p.name || '';
        $('cvTitle').textContent = p.title || '';
        $('cvSummary').innerHTML = p.summary_html || '';
        if (p.name) document.title = 'CV — ' + p.name;

        var email = $('cvEmail');
        if (isPlaceholder(p.email)) {
            if (!preview) email.hidden = true;
        } else {
            email.href = 'mailto:' + p.email;
        }

        $('cvLinks').innerHTML = (p.links || []).map(function (l) {
            return '<li><a href="' + esc(l.url) + '" target="_blank" rel="noopener">' + esc(l.label) + ' ↗</a></li>';
        }).join('');
    }

    // ---- overview -----------------------------------------------------------
    function renderOverview(data) {
        var featured = data.featured || [];
        $('featuredBlock').hidden = !featured.length;
        $('featuredList').innerHTML = featured.map(function (f) {
            return '<article class="feat">' +
                (f.label ? '<p class="feat__label">' + text(f.label) + '</p>' : '') +
                '<h3>' + f.title + '</h3>' +
                '<div class="prose">' + f.html + '</div>' +
                '</article>';
        }).join('');

        var focus = data.focus || [];
        $('focusBlock').hidden = !focus.length;
        $('focusList').innerHTML = focus.map(function (f) {
            return '<div>' +
                '<h3>' + f.title + '</h3>' +
                '<div class="prose">' + f.html + '</div>' +
                (f.tools ? '<p class="mono-line">' + text(f.tools) + '</p>' : '') +
                '</div>';
        }).join('');

        var recent = (data.work || []).filter(visible).slice().sort(function (a, b) {
            if (a.featured !== b.featured) return a.featured ? -1 : 1;
            return (b.date || '').localeCompare(a.date || '');
        }).slice(0, 3);
        $('recentBlock').hidden = !recent.length;
        $('recentList').innerHTML = recent.map(function (w) {
            return '<div class="recent">' +
                '<span class="recent__date">' + fmtDate(w.date) + '</span>' +
                '<span class="recent__text"><strong>' + text(w.title) + '</strong> ' +
                '<span>— ' + text(w.role) + (w.org ? ', ' + text(w.org) : '') + '</span>' +
                draftFlag(w) + '</span>' +
                '<span class="recent__kind">' + esc(TYPE_LABELS[w.type] || w.type) + '</span>' +
                '</div>';
        }).join('');
    }

    function draftFlag(item) {
        return item.draft ? '<span class="draft-flag">draft</span>' : '';
    }

    // ---- experience ---------------------------------------------------------
    function renderExperience(list) {
        list = list || [];
        var main = list.filter(function (j) { return !j.earlier; });
        var earlier = list.filter(function (j) { return j.earlier; });

        var html = main.map(function (j) {
            return '<article class="job row">' +
                '<div class="row__aside">' +
                '<p>' + esc(j.start) + (j.end ? ' — ' + esc(j.end) : '') + '</p>' +
                (j.location ? '<p>' + esc(j.location) + '</p>' : '') +
                '</div>' +
                '<div class="row__main">' +
                '<h2>' + text(j.title) + '</h2>' +
                (j.org ? '<p class="job__org">' + text(j.org) + '</p>' : '') +
                '<div class="prose">' + j.html + '</div>' +
                (j.stack ? '<p class="mono-line">' + text(j.stack) + '</p>' : '') +
                '</div>' +
                '</article>';
        }).join('');

        if (earlier.length) {
            html += '<section class="earlier row">' +
                '<h2 class="row__aside">Earlier</h2>' +
                '<div class="row__main">' +
                earlier.map(function (j) {
                    var summary = (j.html || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
                    return '<div class="earlier__item">' +
                        '<span class="earlier__date">' + esc(j.start) + (j.end ? '—' + esc(j.end).slice(-2) : '') + '</span>' +
                        '<span class="earlier__text"><strong>' + text(j.title) + '</strong> · ' + text(j.org) +
                         (summary ? ' — ' + summary : '') + '</span>' +
                        '</div>';
                }).join('') +
                '</div></section>';
        }

        $('experienceList').innerHTML = html || '<p class="empty">No roles yet.</p>';
    }

    // ---- projects -----------------------------------------------------------
    function renderProjects(list) {
        $('projectList').innerHTML = (list || []).map(function (p) {
            var link = '';
            if (!isPlaceholder(p.url)) {
                link = '<a href="' + esc(p.url) + '" target="_blank" rel="noopener">' + esc(p.link || 'Open') + ' ↗</a>';
            } else if (preview) {
                link = text(p.url || '[link]');
            }
            return '<article class="project row">' +
                '<p class="row__aside">' + text(p.kind) + '</p>' +
                '<div class="row__main">' +
                '<h2>' + p.title + '</h2>' +
                '<div class="prose">' + p.html + '</div>' +
                '<div class="project__foot">' +
                (p.stack ? '<span class="mono-line">' + text(p.stack) + '</span>' : '') +
                link +
                '</div></div></article>';
        }).join('') || '<p class="empty">No projects yet.</p>';
    }

    // ---- public work --------------------------------------------------------
    function renderFilters() {
        var present = {};
        state.work.forEach(function (w) { present[w.type] = true; });
        var shown = FILTERS.filter(function (f) {
            return !f.types || f.types.some(function (t) { return present[t]; });
        });
        $('workFilters').hidden = shown.length <= 2;
        $('workFilters').innerHTML = shown.map(function (f) {
            return '<button type="button" class="chip" data-filter="' + f.id + '" aria-pressed="' +
                (state.filter === f.id) + '">' + esc(f.label) + '</button>';
        }).join('');
    }

    function renderWork() {
        var filter = FILTERS.filter(function (f) { return f.id === state.filter; })[0] || FILTERS[0];
        var items = state.work.filter(function (w) {
            return !filter.types || filter.types.indexOf(w.type) !== -1;
        });

        $('workList').innerHTML = items.map(function (w) {
            var hasUrl = !isPlaceholder(w.url);
            var thumb = '';
            if (w.thumbnail) {
                thumb = '<a class="work__thumb work__thumb--video" href="' + esc(w.url) + '" target="_blank" rel="noopener" aria-label="Watch: ' + esc(w.title) + '">' +
                    '<img src="' + esc(w.thumbnail) + '" alt="" loading="lazy">' +
                    '<span class="work__play"><svg width="44" height="44" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="rgba(0,0,0,0.55)"/><path d="M10 8.5v7l6-3.5z" fill="#fff"/></svg></span>' +
                    '</a>';
            } else if (w.image) {
                thumb = '<div class="work__thumb"><img src="' + esc(w.image) + '" alt="' + esc(w.title + ' — ' + w.org) + '" loading="lazy"></div>';
            }

            var link = '';
            if (hasUrl) {
                link = '<a class="work__link" href="' + esc(w.url) + '" target="_blank" rel="noopener">' + esc(w.link_label) + ' ↗</a>';
            } else if (preview) {
                link = text(w.url || '[link]');
            }

            return '<article class="work">' +
                '<div class="work__body">' +
                '<p class="work__meta">' + fmtDate(w.date) + ' · ' + esc(TYPE_LABELS[w.type] || w.type) + draftFlag(w) + '</p>' +
                '<h3>' + text(w.title) + '</h3>' +
                '<p class="work__role"><strong>' + text(w.role) + '</strong>' + (w.org ? ' · ' + text(w.org) : '') + '</p>' +
                (w.html ? '<div class="prose">' + w.html + '</div>' : '') +
                link +
                '</div>' + thumb +
                '</article>';
        }).join('') || '<p class="empty">Nothing here yet — new talks, contributions and posts will appear here.</p>';
    }

    // ---- education ----------------------------------------------------------
    function renderEducation(list) {
        var html = '';
        (list || []).forEach(function (sec, i) {
            var plain = sec.title.replace(/<[^>]+>/g, '').toLowerCase();
            if (/^more\b/.test(plain) && html) {
                var count = (sec.html.match(/<li>/g) || []).length;
                html = html.replace(/<\/div><\/section>$/,
                    '<div class="prose more-courses" id="more-' + i + '" hidden style="margin-top:8px">' + sec.html + '</div>' +
                    '<button type="button" class="more-toggle" aria-expanded="false" data-count="' + count + '" aria-controls="more-' + i + '">Show ' + count + ' more ↓</button>' +
                    '</div></section>');
                return;
            }
            html += '<section class="edu row">' +
                '<h2 class="row__aside">' + sec.title + '</h2>' +
                '<div class="row__main"><div class="prose">' + sec.html + '</div></div></section>';
        });
        $('educationList').innerHTML = html || '<p class="empty">No entries yet.</p>';
    }

    // ---- tabs ---------------------------------------------------------------
    function showTab(id, focus) {
        if (TABS.indexOf(id) === -1) id = 'overview';
        TABS.forEach(function (t) {
            var tab = $('tab-' + t);
            var on = t === id;
            tab.setAttribute('aria-selected', on ? 'true' : 'false');
            tab.tabIndex = on ? 0 : -1;
            $('panel-' + t).hidden = !on;
        });
        if (focus) $('tab-' + id).focus();

        var bar = document.querySelector('.tabbar');
        if (bar && window.scrollY > bar.offsetTop) window.scrollTo(0, bar.offsetTop);
    }

    function currentHash() { return (location.hash || '').replace('#', ''); }

    function bindEvents() {
        document.querySelector('.tabbar__inner').addEventListener('click', function (e) {
            var tab = e.target.closest('[data-tab]');
            if (!tab) return;
            if (currentHash() === tab.dataset.tab) showTab(tab.dataset.tab);
            else location.hash = tab.dataset.tab;
        });

        document.querySelector('.tabbar__inner').addEventListener('keydown', function (e) {
            if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
            var i = TABS.indexOf(currentHash() || 'overview');
            var next = TABS[(i + (e.key === 'ArrowRight' ? 1 : TABS.length - 1)) % TABS.length];
            location.hash = next;
            setTimeout(function () { $('tab-' + next).focus(); }, 0);
            e.preventDefault();
        });

        window.addEventListener('hashchange', function () { showTab(currentHash()); });

        $('workFilters').addEventListener('click', function (e) {
            var chip = e.target.closest('[data-filter]');
            if (!chip) return;
            state.filter = chip.dataset.filter;
            renderFilters();
            renderWork();
        });

        $('educationList').addEventListener('click', function (e) {
            var btn = e.target.closest('.more-toggle');
            if (!btn) return;
            var target = $(btn.getAttribute('aria-controls'));
            var open = target.hidden;
            target.hidden = !open;
            btn.setAttribute('aria-expanded', String(open));
            btn.textContent = open ? 'Show less ↑' : 'Show ' + btn.getAttribute('data-count') + ' more ↓';
        });

        $('cvPrint').addEventListener('click', function () { window.print(); });

        $('cvThemeToggle').addEventListener('click', function () {
            var root = document.documentElement;
            var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            root.setAttribute('data-theme', next);
            try { localStorage.setItem('theme', next); } catch (err) {}
        });
    }

    // ---- boot ---------------------------------------------------------------
    function render(data) {
        renderProfile(data.profile);
        state.work = (data.work || []).filter(visible);
        renderOverview(data);
        renderExperience(data.experience);
        renderProjects(data.projects);
        renderFilters();
        renderWork();
        $('panel-work').classList.toggle('is-empty', !state.work.length);
        renderEducation(data.education);

        if (data.generated_at) {
            $('cvUpdated').textContent = 'Last updated ' + fmtDate(data.generated_at.slice(0, 7));
        }
        $('cvStatus').hidden = true;
        showTab(currentHash());
    }

    bindEvents();

    fetch('assets/data/cv.json', { cache: 'no-cache' })
        .then(function (r) {
            if (!r.ok) throw new Error('status ' + r.status);
            return r.json();
        })
        .then(render)
        .catch(function (err) {
            console.error('CV data could not be loaded:', err);
            $('cvStatus').innerHTML = 'Could not load the CV data. If you are the site owner, run ' +
                '<code>python generate-data.py</code> and push <code>assets/data/cv.json</code>.';
        });
})();
