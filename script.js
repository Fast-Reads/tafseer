// === INITIALIZATION ===
document.addEventListener('DOMContentLoaded', () => {
    const t = localStorage.getItem('bq-theme');
    if (t) document.body.className = t;
    const fs = localStorage.getItem('bq-fontscale');
    if (fs) { fontScale = parseInt(fs); updateFont(); }
    applyBookmarks();
    applyThemeLabel();
    // Flow diagram restore
    const diagram = document.getElementById('flowDiagram');
    if (diagram && localStorage.getItem('bq-flow-collapsed') === 'true') {
        diagram.classList.add('collapsed');
    }
    // Tajweed restore
    if (localStorage.getItem('bq-tajweed') === 'true') {
        document.body.classList.add('tajweed-on');
        const tb = document.getElementById('tajweedBtn');
        if (tb) tb.classList.add('active');
    }
});

// === THEME & FONT ===
let baseFontSize = 2;
let fontScale = 100;

function toArabicNum(n) {
    return String(n).replace(/[0-9]/g, d => '٠١٢٣٤٥٦٧٨٩'[d]);
}

function changeFontSize(dir) {
    fontScale = Math.max(70, Math.min(150, fontScale + dir * 10));
    localStorage.setItem('bq-fontscale', fontScale);
    updateFont();
}
function updateFont() {
    const size = baseFontSize * (fontScale / 100);
    document.querySelectorAll('.ayah-text').forEach(el => el.style.fontSize = size + 'rem');
    const label = document.getElementById('fontLabel');
    if (label) label.textContent = toArabicNum(fontScale) + '%';
}

const THEMES = [
    { cls: '',           name: 'كريمي' },
    { cls: 'white-mode', name: 'أبيض'  },
    { cls: 'dark-mode',  name: 'داكن'  },
    { cls: 'sepia-mode', name: 'بنّي'  }
];

function currentThemeIndex() {
    const i = THEMES.findIndex(t => t.cls && document.body.classList.contains(t.cls));
    return i === -1 ? 0 : i;
}

function applyThemeLabel() {
    const btn = document.querySelector('[onclick="cycleTheme()"]');
    if (btn) btn.textContent = 'المظهر: ' + THEMES[currentThemeIndex()].name;
}

function cycleTheme() {
    const b = document.body;
    const next = THEMES[(currentThemeIndex() + 1) % THEMES.length];
    THEMES.forEach(t => { if (t.cls) b.classList.remove(t.cls); });   // لا يمسّ الحفظ والتجويد
    if (next.cls) b.classList.add(next.cls);
    localStorage.setItem('bq-theme', next.cls);
    applyThemeLabel();
}

// === MEMORIZE MODE (Multi-Level) ===
let memorizeLevel = 0; // 0=off, 1=reading, 2=first-words, 3=full-test

function toggleMemorize() {
    memorizeLevel = (memorizeLevel + 1) % 4;
    const body = document.body;

    // Remove all memorize classes
    body.classList.remove('memorize-mode', 'memorize-level-1', 'memorize-level-2', 'memorize-level-3');
    document.querySelectorAll('.ayah.revealed').forEach(a => a.classList.remove('revealed'));

    const btn = document.getElementById('memorizeBtn');
    const labels = ['وضع الحفظ', '١ — القراءة', '٢ — الكلمة الأولى', '٣ — الاختبار'];

    if (memorizeLevel > 0) {
        body.classList.add('memorize-level-' + memorizeLevel);
        if (memorizeLevel >= 2) body.classList.add('memorize-mode');
        if (btn) { btn.classList.add('active'); btn.textContent = labels[memorizeLevel]; }
    } else {
        if (btn) { btn.classList.remove('active'); btn.textContent = labels[0]; }
    }

    // For level 2, inject first-word overlays
    if (memorizeLevel === 2) injectFirstWordOverlays();
}

function injectFirstWordOverlays() {
    document.querySelectorAll('.ayah').forEach(ayah => {
        if (ayah.querySelector('.first-word-overlay')) return;
        const textEl = ayah.querySelector('.ayah-text');
        if (!textEl) return;
        const fullText = textEl.textContent.trim().replace(/^۞\s*/, '');
        const firstWord = fullText.split(/\s+/)[0];
        const overlay = document.createElement('div');
        overlay.className = 'first-word-overlay';
        overlay.textContent = firstWord + ' ...';
        ayah.appendChild(overlay);
    });
}

// Click handler for memorize reveal + mastery tracking
document.addEventListener('click', e => {
    const a = e.target.closest('.ayah');
    if (!a) return;
    if (document.body.classList.contains('memorize-level-2') ||
        document.body.classList.contains('memorize-level-3')) {
        if (!a.classList.contains('revealed')) {
            a.classList.add('revealed');
        } else {
            a.classList.remove('revealed');
        }
    }
});

// === HINTS PANEL ===
function toggleHintsPanel() {
    let panel = document.getElementById('hintsPanel');
    if (!panel) {
        panel = createHintsPanel();
        document.body.appendChild(panel);
    }
    panel.classList.toggle('open');
    const btn = document.getElementById('hintsBtn');
    if (btn) btn.classList.toggle('active');
}

function createHintsPanel() {
    const panel = document.createElement('div');
    panel.id = 'hintsPanel';
    panel.className = 'hints-panel';

    let html = '<div class="hints-header">';
    html += '<span class="hints-title">الكلمات الأولى</span>';
    html += '<button class="hints-close" onclick="toggleHintsPanel()">&times;</button>';
    html += '</div>';
    html += '<div class="hints-list">';

    document.querySelectorAll('.ayah').forEach(ayah => {
        const textEl = ayah.querySelector('.ayah-text');
        const badgeEl = ayah.querySelector('.ayah-badge');
        if (!textEl || !badgeEl) return;

        const fullText = textEl.textContent.trim().replace(/^۞\s*/, '');
        const firstWord = fullText.split(/\s+/)[0];
        const num = badgeEl.textContent.trim();
        const ayahId = ayah.id;

        html += '<div class="hint-item" data-target="' + ayahId + '">';
        html += '<span class="hint-num">' + num + '</span>';
        html += '<span class="hint-word">' + firstWord + '</span>';
        html += '</div>';
    });

    html += '</div>';
    panel.innerHTML = html;

    // Click hint to scroll to ayah
    panel.addEventListener('click', e => {
        const item = e.target.closest('.hint-item');
        if (!item) return;
        const target = document.getElementById(item.dataset.target);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
            target.classList.add('highlighted');
            setTimeout(() => target.classList.remove('highlighted'), 2000);
        }
    });

    return panel;
}

// === FLOW DIAGRAM ===
function toggleFlowDiagram() {
    const diagram = document.getElementById('flowDiagram');
    if (!diagram) return;
    diagram.classList.toggle('collapsed');
    localStorage.setItem('bq-flow-collapsed', diagram.classList.contains('collapsed'));
}

// Click flow node to scroll to ayah
document.addEventListener('click', e => {
    const node = e.target.closest('.flow-node');
    if (!node) return;
    const ayahs = node.dataset.ayahs;
    if (!ayahs) return;
    const firstAyah = ayahs.split('-')[0];
    const el = document.getElementById('ayah-' + firstAyah);
    if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.classList.add('highlighted');
        setTimeout(() => el.classList.remove('highlighted'), 2000);
    }
});

// === BOOKMARKS ===
let bookmarks = JSON.parse(localStorage.getItem('bq-bookmarks') || '[]');
function applyBookmarks() {
    bookmarks.forEach(n => {
        const el = document.getElementById('ayah-' + n);
        if (el) el.classList.add('bookmarked');
    });
}
document.addEventListener('dblclick', e => {
    const a = e.target.closest('.ayah');
    if (!a) return;
    const n = parseInt(a.id.replace('ayah-', ''));
    a.classList.toggle('bookmarked');
    if (bookmarks.includes(n)) bookmarks = bookmarks.filter(x => x !== n);
    else bookmarks.push(n);
    localStorage.setItem('bq-bookmarks', JSON.stringify(bookmarks));
    updateBookmarksPanel();
});

// === BOOKMARKS PANEL ===
function toggleBookmarksPanel() {
    let panel = document.getElementById('bookmarksPanel');
    if (!panel) {
        panel = createBookmarksPanel();
        document.body.appendChild(panel);
    }
    updateBookmarksPanel();
    panel.classList.toggle('open');
    const btn = document.getElementById('bookmarksBtn');
    if (btn) btn.classList.toggle('active');
}

function createBookmarksPanel() {
    const panel = document.createElement('div');
    panel.id = 'bookmarksPanel';
    panel.className = 'bookmarks-panel';
    panel.innerHTML = '<div class="bm-header">' +
        '<span class="bm-title">العلامات المرجعية</span>' +
        '<button class="bm-close" onclick="toggleBookmarksPanel()">&times;</button>' +
        '</div><div class="bm-list" id="bmList"></div>';

    panel.addEventListener('click', e => {
        const removeBtn = e.target.closest('.bm-remove');
        if (removeBtn) {
            e.stopPropagation();
            const n = parseInt(removeBtn.dataset.ayah);
            const el = document.getElementById('ayah-' + n);
            if (el) el.classList.remove('bookmarked');
            bookmarks = bookmarks.filter(x => x !== n);
            localStorage.setItem('bq-bookmarks', JSON.stringify(bookmarks));
            updateBookmarksPanel();
            return;
        }
        const item = e.target.closest('.bm-item');
        if (!item) return;
        const target = document.getElementById(item.dataset.target);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
            target.classList.add('highlighted');
            setTimeout(() => target.classList.remove('highlighted'), 2000);
        }
    });

    return panel;
}

function updateBookmarksPanel() {
    const list = document.getElementById('bmList');
    if (!list) return;
    const items = [];
    document.querySelectorAll('.ayah').forEach(ayah => {
        const n = parseInt(ayah.id.replace('ayah-', ''));
        if (!bookmarks.includes(n)) return;
        const textEl = ayah.querySelector('.ayah-text');
        const badgeEl = ayah.querySelector('.ayah-badge');
        if (!textEl || !badgeEl) return;
        const words = textEl.textContent.trim().replace(/^۞\s*/, '').split(/\s+/).slice(0, 3).join(' ');
        items.push({ n, num: badgeEl.textContent.trim(), words, id: ayah.id });
    });
    if (items.length === 0) {
        list.innerHTML = '<div class="bm-empty">لا توجد علامات مرجعية<br>انقر مرتين على آية لإضافتها</div>';
        return;
    }
    let html = '';
    items.forEach(bm => {
        html += '<div class="bm-item" data-target="' + bm.id + '">';
        html += '<span class="bm-num">' + bm.num + '</span>';
        html += '<span class="bm-word">' + bm.words + ' ...</span>';
        html += '<button class="bm-remove" data-ayah="' + bm.n + '" title="إزالة">&times;</button>';
        html += '</div>';
    });
    list.innerHTML = html;
}

// === SCROLL ===
window.addEventListener('scroll', () => {
    const btn = document.getElementById('backToTop');
    if (btn) btn.classList.toggle('visible', window.scrollY > 400);
});

// === KEYBOARD SHORTCUTS ===
document.addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT') return;
    if (e.key === 'm' || e.key === 'M') toggleMemorize();
    if (e.key === 't' || e.key === 'T') cycleTheme();
    if (e.key === 'h' || e.key === 'H') toggleHintsPanel();
    if (e.key === 'j' || e.key === 'J') toggleTajweed();
    if (e.key === 'b' || e.key === 'B') toggleBookmarksPanel();
});

// === TAJWEED TOGGLE ===
function toggleTajweed() {
    document.body.classList.toggle('tajweed-on');
    const btn = document.getElementById('tajweedBtn');
    const on = document.body.classList.contains('tajweed-on');
    if (btn) btn.classList.toggle('active', on);
    localStorage.setItem('bq-tajweed', on);
    // على الهاتف تعود البطاقة مطوية في كل مرة تُفعَّل
    if (!on) document.querySelector('.tajweed-legend')?.classList.remove('legend-open');
}

// طيّ/فتح بطاقة أحكام التجويد (تعمل على الهاتف فقط عبر الـ CSS)
document.addEventListener('click', e => {
    const header = e.target.closest('.tajweed-legend .legend-header');
    if (header) header.closest('.tajweed-legend').classList.toggle('legend-open');
});

// === TAFSEER TOGGLE (shared) ===
function toggleTafseerText(id, btn) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.toggle('collapsed-text');
    btn.textContent = el.classList.contains('collapsed-text') ? 'عرض المزيد' : 'عرض أقل';
}

// === TAFSEER TABS ===
document.addEventListener('click', e => {
    const tab = e.target.closest('.tafseer-tab-btn');
    if (!tab) return;
    const block = tab.closest('.tafseer-block');
    if (!block) return;
    block.querySelectorAll('.tafseer-tab-btn').forEach(t => t.classList.remove('active'));
    block.querySelectorAll('.tafseer-tab-content').forEach(c => c.classList.remove('active'));
    tab.classList.add('active');
    const target = block.querySelector('#' + tab.dataset.tab);
    if (target) target.classList.add('active');
});

// === لمسات بيانية: شرح يظهر عند الضغط على كلمة معلَّمة ===
function closeLamsa() {
    const p = document.getElementById('lamsaPop');
    if (p) p.classList.remove('open');
    document.querySelectorAll('.lamsa.active').forEach(el => el.classList.remove('active'));
}

document.addEventListener('click', e => {
    const el = e.target.closest('.lamsa');
    if (!el) {
        if (!e.target.closest('.lamsa-pop')) closeLamsa();
        return;
    }
    e.stopPropagation();          // لئلّا يُفعِّل كشفَ آية وضع الحفظ
    let pop = document.getElementById('lamsaPop');
    if (!pop) {
        pop = document.createElement('div');
        pop.id = 'lamsaPop';
        pop.className = 'lamsa-pop';
        pop.innerHTML = '<div class="lamsa-pop-head">' +
            '<span class="lamsa-pop-title">لمسة بيانية</span>' +
            '<button class="lamsa-pop-close" onclick="closeLamsa()">&times;</button></div>' +
            '<div class="lamsa-pop-word"></div><div class="lamsa-pop-body"></div>';
        document.body.appendChild(pop);
    }
    closeLamsa();
    el.classList.add('active');
    pop.querySelector('.lamsa-pop-word').textContent = el.dataset.lamsaWord || el.textContent.trim();
    pop.querySelector('.lamsa-pop-body').textContent = el.dataset.lamsa || '';
    requestAnimationFrame(() => pop.classList.add('open'));
});

document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLamsa(); });

