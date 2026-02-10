#!/usr/bin/env python3
"""Fix section-12.html to comply with Guide 1 structure."""
import re

filepath = '/home/abdulfe/Documents/tafseer/section-12.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# FIX 1: Flow header text
# ============================================================
old_header = '\u062a\u0633\u0644\u0633\u0644 \u0627\u0644\u0645\u0648\u0636\u0648\u0639\u0627\u062a'  # تسلسل الموضوعات
new_header = '\u0627\u0644\u062a\u0633\u0644\u0633\u0644 \u0627\u0644\u0645\u0648\u0636\u0648\u0639\u064a'  # التسلسل الموضوعي
assert old_header in content, "FIX 1 FAILED: Flow header text not found"
content = content.replace(old_header, new_header)
print("FIX 1: Flow header text - DONE")

# ============================================================
# FIX 2: Flow container (flow-content -> flow-body + flow-track)
# ============================================================
# Replace opening tag
old_flow_open = '<div class="flow-content">'
new_flow_open = '<div class="flow-body">\n                <div class="flow-track">'
assert old_flow_open in content, "FIX 2a FAILED: flow-content not found"
content = content.replace(old_flow_open, new_flow_open)

# Add closing </div> for flow-track before flow-body closes
# Pattern: 12sp </div> (was flow-content, now closes flow-track) + 8sp </div> (flow-diagram)
old_flow_close = '            </div>\n        </div>\n\n        <div class="ayah-list">'
new_flow_close = '                </div>\n            </div>\n        </div>\n\n        <div class="ayah-list">'
assert old_flow_close in content, "FIX 2b FAILED: flow close pattern not found"
content = content.replace(old_flow_close, new_flow_close)
print("FIX 2: Flow container classes - DONE")

# ============================================================
# FIX 3: Tajweed legend format
# ============================================================
# Use regex to match the entire legend block (no inner <div> tags in original)
legend_match = re.search(
    r'    <div class="tajweed-legend"[^>]*>.*?</div>(?=\n)',
    content,
    flags=re.DOTALL
)
assert legend_match, "FIX 3 FAILED: Tajweed legend not found"

new_legend = '''    <div class="tajweed-legend">
        <div class="legend-header">
            <span class="legend-title">\u0623\u062d\u0643\u0627\u0645 \u0627\u0644\u062a\u062c\u0648\u064a\u062f</span>
        </div>
        <div class="legend-item"><span class="legend-swatch sw-ghn"></span>\u063a\u0646\u0629</div>
        <div class="legend-item"><span class="legend-swatch sw-khf"></span>\u0625\u062e\u0641\u0627\u0621</div>
        <div class="legend-item"><span class="legend-swatch sw-dgm"></span>\u0625\u062f\u063a\u0627\u0645</div>
        <div class="legend-item"><span class="legend-swatch sw-qlb"></span>\u0625\u0642\u0644\u0627\u0628</div>
        <div class="legend-item"><span class="legend-swatch sw-qlq"></span>\u0642\u0644\u0642\u0644\u0629</div>
        <div class="legend-item"><span class="legend-swatch sw-mdd"></span>\u0645\u062f</div>
        <div class="legend-item"><span class="legend-swatch sw-slt"></span>\u062d\u0631\u0641 \u0644\u0627 \u064a\u064f\u0644\u0641\u0638</div>
    </div>'''

content = content[:legend_match.start()] + new_legend + content[legend_match.end():]
print("FIX 3: Tajweed legend format - DONE")

# ============================================================
# FIX 4: Move tafseer-block inside ayah div (all 11 ayahs)
# ============================================================
lines = content.split('\n')
new_lines = []
i = 0
moved_count = 0

while i < len(lines):
    line = lines[i]

    # Check if this </div> is immediately before <div class="tafseer-block">
    if (line.strip() == '</div>' and
        i + 1 < len(lines) and
        lines[i + 1].strip().startswith('<div class="tafseer-block">')):
        # Skip this premature </div> (ayah close)
        i += 1
        continue

    # Check if this line opens a tafseer-block
    if line.strip().startswith('<div class="tafseer-block">'):
        new_lines.append(line)
        depth = 1
        i += 1
        while i < len(lines) and depth > 0:
            l = lines[i]
            depth += l.count('<div') - l.count('</div')
            new_lines.append(l)
            if depth == 0:
                # This line closed the tafseer-block; add </div> for the ayah
                new_lines.append('            </div>')
                moved_count += 1
            i += 1
        continue

    # Normal line
    new_lines.append(line)
    i += 1

content = '\n'.join(new_lines)
print(f"FIX 4: Moved tafseer-block inside ayah div - {moved_count} ayahs fixed")
assert moved_count == 11, f"Expected 11 ayahs, got {moved_count}"

# ============================================================
# Write the fixed file
# ============================================================
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# ============================================================
# Verification
# ============================================================
with open(filepath, 'r', encoding='utf-8') as f:
    verify = f.read()

errors = []

# Check flow structure
if 'flow-body' not in verify:
    errors.append("flow-body not found")
if 'flow-track' not in verify:
    errors.append("flow-track not found")
if 'flow-content' in verify:
    errors.append("flow-content should be replaced")

# Check legend
if 'legend-header' not in verify:
    errors.append("legend-header not found")
if 'legend-swatch' not in verify:
    errors.append("legend-swatch not found")
if 'tajweedLegend' in verify:
    errors.append("old legend id should be gone")
if 'display:none' in verify and 'tajweed-legend' in verify:
    errors.append("legend should not have display:none")

# Check flow header text
if new_header not in verify:
    errors.append("New flow header text not found")
if old_header in verify:
    errors.append("Old flow header text still present")

# Check tafseer-block is inside ayah (no </div> before tafseer-block)
sibling_count = len(re.findall(r'</div>\s*\n\s*<div class="tafseer-block">', verify))
if sibling_count > 0:
    errors.append(f"Found {sibling_count} tafseer-blocks still outside ayah div")

if errors:
    print("\nVERIFICATION FAILED:")
    for e in errors:
        print(f"  - {e}")
else:
    print("\nAll verifications passed!")
