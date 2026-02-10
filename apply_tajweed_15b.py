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

# Ayah 219
content = apply_replacements(content, 219, [
    ('ٱلۡخَمۡرِ', '<span class="tj-slt">ٱ</span>لۡخَمۡرِ'),
    ('وَٱلۡمَیۡسِرِۖ', 'وَ<span class="tj-slt">ٱ</span>لۡمَیۡسِرِۖ'),
    ('فِیهِمَاۤ إِثۡمࣱ كَبِیرࣱ', 'فِیهِمَ<span class="tj-mdd">اۤ</span> إِثۡ<span class="tj-khf">مࣱ كَ</span>بِیرࣱ'),
    ('وَمَنَـٰفِعُ', 'وَمَ<span class="tj-mdd">نَـٰ</span>فِعُ'),
    ('لِلنَّاسِ', 'لِل<span class="tj-ghn">نَّ</span>اسِ'),
    ('وَإِثۡمُهُمَاۤ أَكۡبَرُ', 'وَإِثۡمُهُمَ<span class="tj-mdd">اۤ</span> أَكۡبَرُ'),
    ('مِن نَّفۡعِهِمَاۗ', 'مِ<span class="tj-dgm">ن نَّ</span>فۡعِهِمَاۗ'),
    ('یُنفِقُونَۖ', 'یُ<span class="tj-khf">نفِ</span>قُونَۖ'),
    ('ٱلۡعَفۡوَۗ', '<span class="tj-slt">ٱ</span>لۡعَفۡوَۗ'),
    ('ٱللَّهُ لَكُمُ', '<span class="tj-slt">ٱ</span>للَّهُ لَكُمُ'),
    ('ٱلۡـَٔایَـٰتِ', '<span class="tj-slt">ٱ</span>لۡـَٔا<span class="tj-mdd">یَـٰ</span>تِ'),
])

# Ayah 220
content = apply_replacements(content, 220, [
    ('ٱلدُّنۡیَا', '<span class="tj-slt">ٱل</span>دُّنۡیَا'),
    ('وَٱلۡـَٔاخِرَةِۗ', 'وَ<span class="tj-slt">ٱ</span>لۡـَٔاخِرَةِۗ'),
    ('ٱلۡیَتَـٰمَىٰۖ', '<span class="tj-slt">ٱ</span>لۡیَ<span class="tj-mdd">تَـٰ</span>مَىٰۖ'),
    ('إِصۡلَاحࣱ لَّهُمۡ', 'إِصۡلَا<span class="tj-dgm">حࣱ لَّ</span>هُمۡ'),
    ('وَإِن تُخَالِطُوهُمۡ', 'وَإِ<span class="tj-khf">ن تُ</span>خَالِطُوهُمۡ'),
    ('وَٱللَّهُ یَعۡلَمُ', 'وَ<span class="tj-slt">ٱ</span>للَّهُ یَعۡلَمُ'),
    ('ٱلۡمُفۡسِدَ', '<span class="tj-slt">ٱ</span>لۡمُفۡسِدَ'),
    ('ٱلۡمُصۡلِحِۚ', '<span class="tj-slt">ٱ</span>لۡمُصۡلِحِۚ'),
    ('شَاۤءَ ٱللَّهُ', 'شَ<span class="tj-mdd">اۤ</span>ءَ <span class="tj-slt">ٱ</span>للَّهُ'),
    ('إِنَّ ٱللَّهَ', 'إِ<span class="tj-ghn">نَّ</span> <span class="tj-slt">ٱ</span>للَّهَ'),
])

# Ayah 221
content = apply_replacements(content, 221, [
    ('تَنكِحُوا۟ ٱلۡمُشۡرِكَـٰتِ', 'تَ<span class="tj-khf">نكِ</span>حُوا۟ <span class="tj-slt">ٱ</span>لۡمُشۡرِ<span class="tj-mdd">كَـٰ</span>تِ'),
    ('یُؤۡمِنَّۚ', 'یُؤۡمِ<span class="tj-ghn">نَّ</span>ۚ'),
    ('وَلَأَمَةࣱ مُّؤۡمِنَةٌ', 'وَلَأَمَ<span class="tj-dgm">ةࣱ مُّ</span>ؤۡمِنَةٌ'),
    ('خَیۡرࣱ مِّن مُّشۡرِكَةࣲ وَلَوۡ', 'خَیۡ<span class="tj-dgm">رࣱ مِّ</span><span class="tj-dgm">ن مُّ</span>شۡرِ<span class="tj-dgm">كَةࣲ وَ</span>لَوۡ'),
    ('تُنكِحُوا۟ ٱلۡمُشۡرِكِینَ', 'تُ<span class="tj-khf">نكِ</span>حُوا۟ <span class="tj-slt">ٱ</span>لۡمُشۡرِكِینَ'),
    ('وَلَعَبۡدࣱ مُّؤۡمِنٌ', 'وَلَعَبۡ<span class="tj-dgm">دࣱ مُّ</span>ؤۡمِنٌ'),
    ('خَیۡرࣱ مِّن مُّشۡرِكࣲ وَلَوۡ', 'خَیۡ<span class="tj-dgm">رࣱ مِّ</span><span class="tj-dgm">ن مُّ</span>شۡرِ<span class="tj-dgm">كࣲ وَ</span>لَوۡ'),
    ('أُو۟لَـٰۤىِٕكَ', 'أُ<span class="tj-slt">و۟</span><span class="tj-mdd">لَـٰۤ</span>ىِٕكَ'),
    ('ٱلنَّارِۖ', '<span class="tj-slt">ٱل</span>نَّارِۖ'),
    ('وَٱللَّهُ', 'وَ<span class="tj-slt">ٱ</span>للَّهُ'),
    ('ٱلۡجَنَّةِ', '<span class="tj-slt">ٱ</span>لۡجَ<span class="tj-ghn">نَّ</span>ةِ'),
    ('وَٱلۡمَغۡفِرَةِ', 'وَ<span class="tj-slt">ٱ</span>لۡمَغۡفِرَةِ'),
    ('ءَایَـٰتِهِۦ', 'ءَا<span class="tj-mdd">یَـٰ</span>تِهِۦ'),
    ('لِلنَّاسِ', 'لِل<span class="tj-ghn">نَّ</span>اسِ'),
])

# Ayah 222
content = apply_replacements(content, 222, [
    ('ٱلۡمَحِیضِۖ', '<span class="tj-slt">ٱ</span>لۡمَحِیضِۖ'),
    ('أَذࣰى فَٱعۡتَزِلُوا۟', 'أَ<span class="tj-khf">ذࣰى فَ</span><span class="tj-slt">ٱ</span>عۡتَزِلُوا۟'),
    ('ٱلنِّسَاۤءَ', '<span class="tj-slt">ٱل</span>نِّسَ<span class="tj-mdd">اۤ</span>ءَ'),
    ('ٱلۡمَحِیضِ وَلَا', '<span class="tj-slt">ٱ</span>لۡمَحِیضِ وَلَا'),
    ('تَقۡرَبُوهُنَّ', 'تَقۡرَبُوهُ<span class="tj-ghn">نَّ</span>'),
    ('فَأۡتُوهُنَّ', 'فَأۡتُوهُ<span class="tj-ghn">نَّ</span>'),
    ('ٱللَّهُۚ', '<span class="tj-slt">ٱ</span>للَّهُۚ'),
    ('إِنَّ ٱللَّهَ', 'إِ<span class="tj-ghn">نَّ</span> <span class="tj-slt">ٱ</span>للَّهَ'),
    ('ٱلتَّوَّ', '<span class="tj-slt">ٱل</span>تَّوَّ'),
    ('ٱلۡمُتَطَهِّرِینَ', '<span class="tj-slt">ٱ</span>لۡمُتَطَهِّرِینَ'),
])

with open('section-15.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - ayahs 219-222 tajweed applied")
