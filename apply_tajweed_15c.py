import unicodedata
n = lambda s: unicodedata.normalize('NFC', s)

with open('section-15.html', 'r', encoding='utf-8') as f:
    content = n(f.read())

def get_ayah(content, num):
    marker = n(f'id="ayah-{num}"')
    start = content.index(marker)
    text_start = content.index(n('<div class="ayah-text">'), start)
    text_end = content.index(n('</div>'), text_start)
    return text_start, text_end + len(n('</div>'))

def apply_replacements(content, num, replacements):
    start, end = get_ayah(content, num)
    ayah_text = content[start:end]
    count = 0
    for old, new in replacements:
        old_n = n(old)
        new_n = n(new)
        if old_n in ayah_text:
            ayah_text = ayah_text.replace(old_n, new_n, 1)
            count += 1
        else:
            print(f"  MISS: '{old[:30]}' in ayah {num}")
    content = content[:start] + ayah_text + content[end:]
    print(f"  Ayah {num}: {count}/{len(replacements)} replacements OK")
    return content

# Ayah 223
content = apply_replacements(content, 223, [
    ('نِسَاۤؤُكُمۡ', 'نِسَ<span class="tj-mdd">اۤ</span>ؤُكُمۡ'),
    ('حَرۡثࣱ لَّكُمۡ', 'حَرۡ<span class="tj-dgm">ثࣱ لَّ</span>كُمۡ'),
    ('وَٱتَّقُوا۟ ٱللَّهَ', 'وَ<span class="tj-slt">ٱ</span>تَّقُوا۟ <span class="tj-slt">ٱ</span>للَّهَ'),
    ('أَنَّكُم مُّلَـٰقُوهُۗ', 'أَ<span class="tj-ghn">نَّ</span>كُم <span class="tj-ghn">مُّ</span><span class="tj-mdd">لَـٰ</span>قُوهُۗ'),
    ('ٱلۡمُؤۡمِنِینَ', '<span class="tj-slt">ٱ</span>لۡمُؤۡمِنِینَ'),
])

# Ayah 224
content = apply_replacements(content, 224, [
    ('ٱللَّهَ عُرۡضَةࣰ لِّأَیۡمَـٰنِكُمۡ', '<span class="tj-slt">ٱ</span>للَّهَ عُرۡضَ<span class="tj-dgm">ةࣰ لِّ</span>أَیۡ<span class="tj-mdd">مَـٰ</span>نِكُمۡ'),
    ('أَن تَبَرُّوا۟', 'أَ<span class="tj-khf">ن تَ</span>بَرُّوا۟'),
    ('ٱلنَّاسِۚ', '<span class="tj-slt">ٱل</span>نَّاسِۚ'),
    ('وَٱللَّهُ', 'وَ<span class="tj-slt">ٱ</span>للَّهُ'),
])

# Ayah 225
content = apply_replacements(content, 225, [
    ('ٱللَّهُ بِٱللَّغۡوِ', '<span class="tj-slt">ٱ</span>للَّهُ بِ<span class="tj-slt">ٱل</span>لَّغۡوِ'),
    ('فِیۤ أَیۡمَـٰنِكُمۡ', 'فِ<span class="tj-mdd">یۤ</span> أَیۡ<span class="tj-mdd">مَـٰ</span>نِكُمۡ'),
    ('وَلَـٰكِن', 'وَ<span class="tj-mdd">لَـٰ</span>كِن'),
    ('وَٱللَّهُ غَفُورٌ', 'وَ<span class="tj-slt">ٱ</span>للَّهُ غَفُورٌ'),
])

# Ayah 226
content = apply_replacements(content, 226, [
    ('مِن نِّسَاۤىِٕهِمۡ', 'مِ<span class="tj-dgm">ن نِّ</span>سَ<span class="tj-mdd">اۤ</span>ىِٕهِمۡ'),
    ('أَشۡهُرࣲۖ فَإِن فَاۤءُو', 'أَشۡهُ<span class="tj-khf">رࣲۖ فَ</span>إِ<span class="tj-khf">ن فَ</span><span class="tj-mdd">اۤ</span>ءُو'),
    ('فَإِنَّ ٱللَّهَ', 'فَإِ<span class="tj-ghn">نَّ</span> <span class="tj-slt">ٱ</span>للَّهَ'),
    ('غَفُورࣱ رَّحِیمࣱ', 'غَفُو<span class="tj-dgm">رࣱ رَّ</span>حِیمࣱ'),
])

with open('section-15.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - ayahs 223-226 tajweed applied")
