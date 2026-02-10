#!/usr/bin/env python3
"""Apply tajweed markup to ayah texts in section-06.html"""
import re
import unicodedata

# Unicode constants
ALIF_WASLA = '\u0671'  # ٱ
SHADDAH = '\u0651'     # ّ
SUKOON = '\u06e1'      # ۡ (small high dotless head of khah)
SMALL_HIGH_MADDA = '\u06e4'  # ۤ
SMALL_HIGH_ROUNDED_ZERO = '\u06df'  # ۟ (silent marker)
SMALL_HIGH_MEEM = '\u06e2'  # ۢ (iqlab marker)
SUPERSCRIPT_ALIF = '\u0670'  # ٰ (dagger alif)
TATWEEL = '\u0640'     # ـ
TANWEEN_FATHA = '\u08f0'   # ࣰ
TANWEEN_DAMMA = '\u08f1'   # ࣱ
TANWEEN_KASRA = '\u08f2'   # ࣲ
FATHATAN = '\u064b'    # ً
DAMMATAN = '\u064c'    # ٌ
KASRATAN = '\u064d'    # ٍ
FATHA = '\u064e'       # َ
DAMMA = '\u064f'       # ُ
KASRA = '\u0650'       # ِ

# Letter sets
SUN_LETTERS = set('تثدذرزسشصضطظلن')
MOON_LETTERS = set('ابجحخعغفقكموهي')
IKHFA_LETTERS = set('تثجدذزسشصضطظفقك')
IDGHAM_LETTERS = set('يرملون')
QALQALAH_LETTERS = set('قطبجد')

# All tanween markers
TANWEEN_MARKS = {TANWEEN_FATHA, TANWEEN_DAMMA, TANWEEN_KASRA, FATHATAN, DAMMATAN, KASRATAN}

# Combining marks
COMBINING_MARKS = {
    SHADDAH, SUKOON, SMALL_HIGH_MADDA, SMALL_HIGH_ROUNDED_ZERO,
    SMALL_HIGH_MEEM, SUPERSCRIPT_ALIF,
    FATHA, DAMMA, KASRA, FATHATAN, DAMMATAN, KASRATAN,
    TANWEEN_FATHA, TANWEEN_DAMMA, TANWEEN_KASRA,
    '\u0652',  # Sukun
    '\u0653',  # Maddah
    '\u0654',  # Hamza above
    '\u0655',  # Hamza below
    '\u0656',  # Subscript alif
    '\u0657',  # Inverted damma
    '\u0658',  # Mark noon ghunna
    '\u065c',  # Vowel sign dot below
    '\u06d6', '\u06d7', '\u06d8', '\u06d9', '\u06da', '\u06db', '\u06dc',
    '\u06dd', '\u06de',
    '\u06e0', '\u06e1', '\u06e2', '\u06e3', '\u06e4',
    '\u06e7', '\u06e8',
    '\u06ea', '\u06eb', '\u06ec', '\u06ed',
    '\u08f0', '\u08f1', '\u08f2',
}

def is_combining(ch):
    """Check if character is a combining mark"""
    if ch in COMBINING_MARKS:
        return True
    cat = unicodedata.category(ch)
    return cat.startswith('M')

def is_format_char(ch):
    """Check if character is a format/invisible character"""
    cat = unicodedata.category(ch)
    return cat == 'Cf'

def is_arabic_letter(ch):
    """Check if character is a base Arabic letter"""
    cp = ord(ch)
    return (0x0620 <= cp <= 0x064A) or (0x0671 <= cp <= 0x06D3) or ch == TATWEEL

def parse_clusters(text):
    """Parse text into grapheme clusters (base char + combining marks)"""
    clusters = []
    current = ''
    for ch in text:
        if current == '':
            current = ch
        elif is_combining(ch) or is_format_char(ch):
            current += ch
        else:
            clusters.append(current)
            current = ch
    if current:
        clusters.append(current)
    return clusters

def get_base_letter(cluster):
    """Get the base letter from a cluster"""
    for ch in cluster:
        if not is_combining(ch) and not is_format_char(ch):
            return ch
    return ''

def has_shaddah(cluster):
    """Check if cluster has shaddah"""
    return SHADDAH in cluster

def has_sukoon(cluster):
    """Check if cluster has sukoon marker"""
    return SUKOON in cluster

def has_tanween(cluster):
    """Check if cluster contains any tanween mark"""
    return bool(set(cluster) & TANWEEN_MARKS)

def has_silent_marker(cluster):
    """Check if cluster has the silent marker (small high rounded zero)"""
    return SMALL_HIGH_ROUNDED_ZERO in cluster

def has_superscript_alif(cluster):
    """Check if cluster contains superscript alif (dagger alif)"""
    return SUPERSCRIPT_ALIF in cluster

def has_madda(cluster):
    """Check if cluster contains small high madda"""
    return SMALL_HIGH_MADDA in cluster

def wrap_span(text, css_class):
    return f'<span class="{css_class}">{text}</span>'

def apply_tajweed(text):
    """Apply tajweed color coding to Quranic text"""
    clusters = parse_clusters(text)
    n = len(clusters)

    # Track which clusters are already tagged
    tags = [None] * n  # None = no tag, string = css class
    # Track groupings: (start_idx, end_idx, css_class)
    spans = []

    i = 0
    while i < n:
        cluster = clusters[i]
        base = get_base_letter(cluster)

        # === SILENT MARKERS ===
        # Silent alif (ا۟) or silent waw (و۟)
        if has_silent_marker(cluster):
            if base in ('ا', 'و', 'ى'):
                spans.append((i, i, 'tj-slt'))
                i += 1
                continue

        # === ALIF WASL ===
        if base == ALIF_WASLA:
            # Check if next cluster is ل (lam)
            if i + 1 < n and get_base_letter(clusters[i+1]) == 'ل':
                # Case 1: Lam itself has shaddah (ال + ل → الّ)
                if has_shaddah(clusters[i+1]):
                    spans.append((i, i+1, 'tj-slt'))
                    i += 2
                    continue
                # Case 2: Letter AFTER lam is sun letter with shaddah
                if i + 2 < n:
                    next_base = get_base_letter(clusters[i+2])
                    if next_base in SUN_LETTERS and has_shaddah(clusters[i+2]):
                        # Lam shamsiyyah: mark ٱل as silent
                        spans.append((i, i+1, 'tj-slt'))
                        i += 2
                        continue
                # Moon letter or no shaddah: only mark ٱ
                spans.append((i, i, 'tj-slt'))
                i += 1
                continue
            else:
                # Standalone alif wasl (e.g., ٱذۡكُرُوا)
                spans.append((i, i, 'tj-slt'))
                i += 1
                continue

        # === GHUNNAH ===
        if base in ('ن', 'م') and has_shaddah(cluster):
            spans.append((i, i, 'tj-ghn'))
            i += 1
            continue

        # === QALQALAH ===
        if base in QALQALAH_LETTERS and has_sukoon(cluster):
            spans.append((i, i, 'tj-qlq'))
            i += 1
            continue

        # === MADD ===
        # Dagger alif / superscript alif
        if has_superscript_alif(cluster):
            spans.append((i, i, 'tj-mdd'))
            i += 1
            continue

        # Small high madda (elongation marker)
        if has_madda(cluster):
            spans.append((i, i, 'tj-mdd'))
            i += 1
            continue

        # Alif madd: ا followed by hamza in different word (madd munfasil)
        # or ا before ء in same word (madd muttasil)
        if base == 'ا' and has_madda(cluster):
            spans.append((i, i, 'tj-mdd'))
            i += 1
            continue

        # === IQLAB MARKER (small low meem ۭ) ===
        if '\u06ed' in cluster:
            # This is an explicit iqlab marker in Uthmani text
            spans.append((i, i, 'tj-qlb'))
            i += 1
            continue

        # === NOON SAKINAH / TANWEEN RULES ===
        # Find the next meaningful letter after current position
        def find_next_letter(start):
            """Find the next Arabic letter cluster after position start"""
            j = start + 1
            while j < n:
                b = get_base_letter(clusters[j])
                if b and is_arabic_letter(b) and b != TATWEEL:
                    return j, b
                elif clusters[j].strip() == '' or b == ' ':
                    j += 1
                    continue
                else:
                    j += 1
                    continue
            return None, None

        # Check if noon has no vowel (implicit sukoon)
        def has_no_vowel(cluster):
            vowels = {FATHA, DAMMA, KASRA, FATHATAN, DAMMATAN, KASRATAN,
                      TANWEEN_FATHA, TANWEEN_DAMMA, TANWEEN_KASRA, SHADDAH}
            return not bool(set(cluster) & vowels)

        # Noon with sukoon (explicit or implicit)
        if base == 'ن' and (has_sukoon(cluster) or (has_no_vowel(cluster) and not has_shaddah(cluster))):
            next_idx, next_letter = find_next_letter(i)
            if next_letter:
                if next_letter == 'ب':
                    # Iqlab
                    spans.append((i, i, 'tj-qlb'))
                    i += 1
                    continue
                elif next_letter in IKHFA_LETTERS:
                    # Ikhfa
                    spans.append((i, i, 'tj-khf'))
                    i += 1
                    continue
                elif next_letter in IDGHAM_LETTERS:
                    # Idgham
                    spans.append((i, i, 'tj-dgm'))
                    i += 1
                    continue

        # Tanween before next letter
        if has_tanween(cluster):
            next_idx, next_letter = find_next_letter(i)
            if next_letter:
                if next_letter == 'ب':
                    # Iqlab
                    spans.append((i, i, 'tj-qlb'))
                    i += 1
                    continue
                elif next_letter in IKHFA_LETTERS:
                    # Ikhfa
                    spans.append((i, i, 'tj-khf'))
                    i += 1
                    continue
                elif next_letter in IDGHAM_LETTERS:
                    # Idgham
                    spans.append((i, i, 'tj-dgm'))
                    i += 1
                    continue

        i += 1

    # Now build output with spans applied
    # Sort spans by start position (reverse for safe insertion)
    # Convert cluster indices to character-level output

    # Build output
    output_clusters = list(clusters)  # copy

    # Process spans in reverse order to maintain indices
    spans.sort(key=lambda x: x[0], reverse=True)

    for start, end, css_class in spans:
        # Combine clusters in range
        span_text = ''.join(output_clusters[start:end+1])
        wrapped = wrap_span(span_text, css_class)
        output_clusters[start:end+1] = [wrapped]

    return ''.join(output_clusters)


def strip_tajweed_spans(text):
    """Remove existing tajweed spans to allow re-processing"""
    return re.sub(r'<span class="tj-[a-z]+">(.*?)</span>', r'\1', text)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all ayah-text divs and apply tajweed
    pattern = r'(<div class="ayah-text">)(.*?)(</div>)'
    count = 0

    def replace_ayah_text(match):
        nonlocal count
        prefix = match.group(1)
        text = match.group(2).strip()
        suffix = match.group(3)

        # Strip existing tajweed spans first
        text = strip_tajweed_spans(text)

        marked = apply_tajweed(text)
        count += 1
        return f'{prefix}{marked}{suffix}'

    new_content = re.sub(pattern, replace_ayah_text, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Processed {count} ayahs in {filepath}")

    # Count total tajweed marks
    tj_count = new_content.count('tj-')
    print(f"Total tajweed marks applied: {tj_count}")


if __name__ == '__main__':
    process_file('section-06.html')
    print("Done!")
