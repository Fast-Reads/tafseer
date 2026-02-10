import unicodedata
n = lambda s: unicodedata.normalize('NFC', s)

with open('section-14.html', 'r', encoding='utf-8') as f:
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
            print(f"  MISS: '{old[:40]}' in ayah {num}")
    content = content[:start] + ayah_text + content[end:]
    print(f"  Ayah {num}: {count}/{len(replacements)} replacements OK")
    return content

# Ayah 204
# وَمِنَ ٱلنَّاسِ مَن یُعۡجِبُكَ قَوۡلُهُۥ فِی ٱلۡحَیَوٰةِ ٱلدُّنۡیَا وَیُشۡهِدُ ٱللَّهَ عَلَىٰ مَا فِی قَلۡبِهِۦ وَهُوَ أَلَدُّ ٱلۡخِصَامِ
content = apply_replacements(content, 204, [
    ('ٱلنَّاسِ مَن یُعۡجِبُكَ', '<span class="tj-slt">ٱل</span>نَّاسِ مَ<span class="tj-dgm">ن یُ</span>عۡجِبُكَ'),
    ('ٱلۡحَیَوٰةِ', '<span class="tj-slt">ٱ</span>لۡحَیَ<span class="tj-mdd">وٰ</span>ةِ'),
    ('ٱلدُّنۡیَا', '<span class="tj-slt">ٱل</span>دُّنۡیَا'),
    ('ٱللَّهَ عَلَىٰ', '<span class="tj-slt">ٱ</span>للَّهَ عَلَ<span class="tj-mdd">ىٰ</span>'),
    ('ٱلۡخِصَامِ', '<span class="tj-slt">ٱ</span>لۡخِصَامِ'),
])

# Ayah 205
# وَإِذَا تَوَلَّىٰ سَعَىٰ فِی ٱلۡأَرۡضِ لِیُفۡسِدَ فِیهَا وَیُهۡلِكَ ٱلۡحَرۡثَ وَٱلنَّسۡلَۚ وَٱللَّهُ لَا یُحِبُّ ٱلۡفَسَادَ
content = apply_replacements(content, 205, [
    ('تَوَلَّىٰ', 'تَوَلَّ<span class="tj-mdd">ىٰ</span>'),
    ('سَعَىٰ', 'سَعَ<span class="tj-mdd">ىٰ</span>'),
    ('ٱلۡأَرۡضِ', '<span class="tj-slt">ٱ</span>لۡأَرۡضِ'),
    ('ٱلۡحَرۡثَ', '<span class="tj-slt">ٱ</span>لۡحَرۡثَ'),
    ('وَٱلنَّسۡلَۚ', 'وَ<span class="tj-slt">ٱل</span>نَّسۡلَۚ'),
    ('وَٱللَّهُ', 'وَ<span class="tj-slt">ٱ</span>للَّهُ'),
    ('ٱلۡفَسَادَ', '<span class="tj-slt">ٱ</span>لۡفَسَادَ'),
])

# Ayah 206
# وَإِذَا قِیلَ لَهُ ٱتَّقِ ٱللَّهَ أَخَذَتۡهُ ٱلۡعِزَّةُ بِٱلۡإِثۡمِۚ فَحَسۡبُهُۥ جَهَنَّمُۖ وَلَبِئۡسَ ٱلۡمِهَادُ
content = apply_replacements(content, 206, [
    ('ٱتَّقِ', '<span class="tj-slt">ٱ</span>تَّقِ'),
    ('ٱللَّهَ', '<span class="tj-slt">ٱ</span>للَّهَ'),
    ('ٱلۡعِزَّةُ', '<span class="tj-slt">ٱ</span>لۡعِزَّةُ'),
    ('بِٱلۡإِثۡمِۚ', 'بِ<span class="tj-slt">ٱ</span>لۡإِثۡمِۚ'),
    ('جَهَنَّمُۖ', 'جَهَ<span class="tj-ghn">نَّ</span>مُۖ'),
    ('ٱلۡمِهَادُ', '<span class="tj-slt">ٱ</span>لۡمِهَادُ'),
])

# Ayah 207
# وَمِنَ ٱلنَّاسِ مَن یَشۡرِی نَفۡسَهُ ٱبۡتِغَاۤءَ مَرۡضَاتِ ٱللَّهِۚ وَٱللَّهُ رَءُوفُۢ بِٱلۡعِبَادِ
content = apply_replacements(content, 207, [
    ('ٱلنَّاسِ مَن یَشۡرِی', '<span class="tj-slt">ٱل</span>نَّاسِ مَ<span class="tj-dgm">ن یَ</span>شۡرِی'),
    ('ٱبۡتِغَاۤءَ', '<span class="tj-slt">ٱ</span><span class="tj-qlq">بۡ</span>تِغَ<span class="tj-mdd">اۤ</span>ءَ'),
    ('ٱللَّهِۚ', '<span class="tj-slt">ٱ</span>للَّهِۚ'),
    ('وَٱللَّهُ', 'وَ<span class="tj-slt">ٱ</span>للَّهُ'),
    ('رَءُوفُۢ بِٱلۡعِبَادِ', 'رَءُو<span class="tj-qlb">فُۢ بِ</span><span class="tj-slt">ٱ</span>لۡعِبَادِ'),
])

with open('section-14.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - ayahs 204-207 tajweed applied")
