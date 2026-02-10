#!/usr/bin/env python3
"""Fix section-12.html for Guide 2: flow diagram + tajweed on ayahs 178-179."""
import re

filepath = '/home/abdulfe/Documents/tafseer/section-12.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# PART 1: FLOW DIAGRAM FIXES
# ============================================================

# 1a. Replace node class names
content = content.replace('class="flow-num"', 'class="flow-node-num"')
content = content.replace('class="flow-title"', 'class="flow-node-text"')
print("  1a. Node class names replaced")

# 1b. Replace arrow symbols (▼ → ↓)
content = content.replace(
    '<div class="flow-arrow">\u25bc</div>',
    '<div class="flow-arrow">\u2193</div>'
)
print("  1b. Arrow symbols replaced")

# 1c. Remove onclick from flow nodes
content = re.sub(r' onclick="scrollToAyah\(\d+\)"', '', content)
print("  1c. onclick attributes removed")

# 1d. Add flow-node-key after each flow-node-text
key_phrases = [
    ('178-179', '\u0643\u064f\u062a\u0650\u0628\u064e \u0639\u064e\u0644\u064e\u064a\u0652\u0643\u064f\u0645\u064f \u0671\u0644\u0652\u0642\u0650\u0635\u064e\u0627\u0635\u064f'),
    ('180-182', '\u0671\u0644\u0652\u0648\u064e\u0635\u0650\u064a\u0651\u064e\u0629\u064f \u0644\u0650\u0644\u0652\u0648\u064e\u0640\u0670\u0644\u0650\u062f\u064e\u064a\u0652\u0646\u0650'),
    ('183-184', '\u0643\u064f\u062a\u0650\u0628\u064e \u0639\u064e\u0644\u064e\u064a\u0652\u0643\u064f\u0645\u064f \u0671\u0644\u0635\u0651\u0650\u064a\u064e\u0627\u0645\u064f'),
    ('185', '\u0634\u064e\u0647\u0652\u0631\u064f \u0631\u064e\u0645\u064e\u0636\u064e\u0627\u0646\u064e'),
    ('186', '\u0641\u064e\u0625\u0650\u0646\u0651\u0650\u06cc \u0642\u064e\u0631\u0650\u064a\u0628\u064c'),
    ('187', '\u0623\u064f\u062d\u0650\u0644\u0651\u064e \u0644\u064e\u0643\u064f\u0645\u0652 \u0644\u064e\u064a\u0652\u0644\u064e\u0629\u064e \u0671\u0644\u0635\u0651\u0650\u064a\u064e\u0627\u0645\u0650'),
    ('188', '\u0644\u064e\u0627 \u062a\u064e\u0623\u0652\u0643\u064f\u0644\u064f\u0648\u0627 \u0623\u064e\u0645\u0652\u0648\u064e\u0640\u0670\u0644\u064e\u0643\u064f\u0645'),
]

for ayahs, key in key_phrases:
    # Find the flow-node-text closing tag within the correct node
    pattern = rf'(data-ayahs="{re.escape(ayahs)}">\n\s*<div class="flow-node-num">.*?</div>\n\s*<div class="flow-node-text">.*?</div>)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        old = match.group(1)
        new = old + f'\n                    <div class="flow-node-key">{key}</div>'
        content = content.replace(old, new)
    else:
        print(f"  WARNING: flow node for ayahs {ayahs} not found!")

print("  1d. flow-node-key phrases added")
print("PART 1: Flow diagram fixes - DONE\n")


# ============================================================
# PART 2: TAJWEED MARKUP
# ============================================================

def apply_tajweed(content, ayah_id, rules):
    """Apply tajweed spans to an ayah using position-based rules."""
    # Find the ayah-text content
    pattern = f'id="ayah-{ayah_id}">'
    idx = content.find(pattern)
    assert idx != -1, f"ayah-{ayah_id} not found!"

    text_tag = '<div class="ayah-text">'
    text_start = content.find(text_tag, idx)
    assert text_start != -1, f"ayah-text not found for ayah-{ayah_id}!"

    content_start = text_start + len(text_tag)
    content_end = content.find('\n', content_start)
    ayah_text = content[content_start:content_end]

    # Sort rules by start position
    rules.sort(key=lambda r: r[0])

    # Verify no overlaps and positions are valid
    for i, (s, e, c) in enumerate(rules):
        assert 0 <= s < e <= len(ayah_text), \
            f"Rule {i} ({s},{e},{c}) out of bounds (text len={len(ayah_text)})"
        if i > 0:
            assert rules[i-1][1] <= s, \
                f"Overlap: rule {i-1} ends at {rules[i-1][1]}, rule {i} starts at {s}"

    # Build new text with spans
    new_text = ""
    pos = 0
    for start, end, cls in rules:
        new_text += ayah_text[pos:start]
        new_text += f'<span class="{cls}">{ayah_text[start:end]}</span>'
        pos = end
    new_text += ayah_text[pos:]

    content = content[:content_start] + new_text + content[content_end:]
    print(f"  Ayah {ayah_id}: {len(rules)} spans applied ({len(ayah_text)} → {len(new_text)} chars)")
    return content


# ---- Ayah 178: 27 tajweed rules ----
# Positions verified from codepoint dump
rules_178 = [
    # MADD: یَـٰۤ (ya+fatha+tatweel+dagger_alif+madda) before hamza
    (0, 5, 'tj-mdd'),
    # SILENT: ٱلَّ in ٱلَّذِینَ (ذ = sun letter)
    (14, 18, 'tj-slt'),
    # SILENT: ا۟ in ءَامَنُوا۟ (silent alif)
    (32, 34, 'tj-slt'),
    # SILENT: ٱ in ٱلۡقِصَاصُ (ق = moon)
    (53, 54, 'tj-slt'),
    # SILENT: ٱ in ٱلۡقَتۡلَى (ق = moon)
    (68, 69, 'tj-slt'),
    # SILENT: ٱ in ٱلۡحُرُّ (ح = moon)
    (80, 81, 'tj-slt'),
    # SILENT: ٱ in بِٱلۡحُرِّ (ح = moon)
    (91, 92, 'tj-slt'),
    # SILENT: ٱ in وَٱلۡعَبۡدُ (ع = moon)
    (102, 103, 'tj-slt'),
    # QALQALAH: بۡ in عَبۡدُ
    (107, 109, 'tj-qlq'),
    # SILENT: ٱ in بِٱلۡعَبۡدِ (ع = moon)
    (114, 115, 'tj-slt'),
    # QALQALAH: بۡ in عَبۡدِ
    (119, 121, 'tj-qlq'),
    # SILENT: ٱ in وَٱلۡأُنثَىٰ (أ = moon)
    (126, 127, 'tj-slt'),
    # MADD: ىٰ in أُنثَىٰ (alif maqsura + dagger alif)
    (134, 136, 'tj-mdd'),
    # SILENT: ٱ in بِٱلۡأُنثَىٰ (أ = moon)
    (139, 140, 'tj-slt'),
    # MADD: ىٰ in أُنثَىٰۚ
    (147, 149, 'tj-mdd'),
    # IKHFA: ءࣱ in شَیۡءࣱ (tanween before ف)
    (188, 190, 'tj-khf'),
    # SILENT: ٱ in فَٱتِّبَاعُۢ (alif wasl in verb)
    (193, 194, 'tj-slt'),
    # IQLAB: ۢ بِ in فَٱتِّبَاعُۢ بِٱلۡمَعۡرُوفِ (noon→meem before ب)
    (202, 206, 'tj-qlb'),
    # SILENT: ٱ in بِٱلۡمَعۡرُوفِ (م = moon)
    (206, 207, 'tj-slt'),
    # MADD: اۤ in أَدَاۤءٌ (madd muttasil, alif+madda before hamza)
    (225, 227, 'tj-mdd'),
    # MADD: سَـٰ in إِحۡسَـٰنࣲ (dagger alif)
    (245, 249, 'tj-mdd'),
    # IKHFA: نࣲ in إِحۡسَـٰنࣲ (tanween before ذ)
    (249, 251, 'tj-khf'),
    # IDGHAM: فࣱ in تَخۡفِیفࣱ (tanween before م = يرملون)
    (270, 272, 'tj-dgm'),
    # GHUNNAH: مِّ in مِّن (meem mushaddadah)
    (273, 276, 'tj-ghn'),
    # IKHFA: ةࣱ in وَرَحۡمَةࣱ (tanween before ف)
    (297, 299, 'tj-khf'),
    # SILENT: ٱ in ٱعۡتَدَىٰ (alif wasl in verb)
    (308, 309, 'tj-slt'),
    # MADD: ىٰ in ٱعۡتَدَىٰ
    (315, 317, 'tj-mdd'),
]

# ---- Ayah 179: 7 tajweed rules ----
rules_179 = [
    # SILENT: ٱ in ٱلۡقِصَاصِ (ق = moon)
    (13, 14, 'tj-slt'),
    # MADD: وٰ in حَیَوٰةࣱ (waw + dagger alif)
    (28, 30, 'tj-mdd'),
    # IDGHAM: ةࣱ in حَیَوٰةࣱ (tanween before ی = يرملون)
    (30, 32, 'tj-dgm'),
    # MADD: یَـٰۤ in یَـٰۤأُو۟لِی (madd before hamza)
    (33, 38, 'tj-mdd'),
    # SILENT: و۟ in أُو۟لِی (silent waw)
    (40, 42, 'tj-slt'),
    # SILENT: ٱ in ٱلۡأَلۡبَـٰبِ (أ = moon)
    (46, 47, 'tj-slt'),
    # MADD: بَـٰ in ٱلۡأَلۡبَـٰبِ (dagger alif)
    (53, 57, 'tj-mdd'),
]

print("PART 2: Applying tajweed...")
content = apply_tajweed(content, 178, rules_178)
content = apply_tajweed(content, 179, rules_179)
print("PART 2: Tajweed - DONE\n")

# ============================================================
# Write output
# ============================================================
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("File written successfully!\n")

# ============================================================
# Verification
# ============================================================
with open(filepath, 'r', encoding='utf-8') as f:
    verify = f.read()

print("=== VERIFICATION ===")

# Count tajweed spans per ayah
for aid in [178, 179]:
    pat = f'id="ayah-{aid}"'
    start = verify.find(pat)
    next_id = f'id="ayah-{aid+1}"'
    end = verify.find(next_id, start)
    if end == -1:
        end = verify.find('</div>\n            </div>\n        </div>', start)
    section = verify[start:end]
    spans = re.findall(r'class="(tj-\w+)"', section)
    print(f"\nAyah {aid}: {len(spans)} tajweed spans")
    from collections import Counter
    for cls, count in sorted(Counter(spans).items()):
        print(f"  {cls}: {count}")

# Flow diagram checks
errors = []
if 'class="flow-node-num"' not in verify:
    errors.append("flow-node-num missing")
if 'class="flow-node-text"' not in verify:
    errors.append("flow-node-text missing")
if 'class="flow-node-key"' not in verify:
    errors.append("flow-node-key missing")
if 'class="flow-num"' in verify:
    errors.append("old flow-num still present")
if 'class="flow-title"' in verify:
    errors.append("old flow-title still present")
if 'scrollToAyah' in verify:
    errors.append("onclick still present")

key_count = verify.count('flow-node-key')
print(f"\nFlow: {key_count} flow-node-key elements (expected 7)")

if errors:
    print("\nERRORS:")
    for e in errors:
        print(f"  - {e}")
else:
    print("\nAll checks passed!")
