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

# Ayah 231 - long ayah
content = apply_replacements(content, 231, [
    ('ٱلنِّسَاۤءَ فَبَلَغۡنَ أَجَلَهُنَّ فَأَمۡسِكُوهُنَّ', '<span class="tj-slt">ٱل</span>نِّسَ<span class="tj-mdd">اۤ</span>ءَ فَبَلَغۡنَ أَجَلَهُ<span class="tj-ghn">نَّ</span> فَأَمۡسِكُوهُ<span class="tj-ghn">نَّ</span>'),
    ('سَرِّحُوهُنَّ', 'سَرِّحُوهُ<span class="tj-ghn">نَّ</span>'),
    ('تُمۡسِكُوهُنَّ', 'تُمۡسِكُوهُ<span class="tj-ghn">نَّ</span>'),
    ('ضِرَارࣰا لِّتَعۡتَدُوا۟ۚ', 'ضِرَارَ<span class="tj-dgm">ࣰا لِّ</span>تَعۡتَدُوا۟ۚ'),
    ('وَمَن یَفۡعَلۡ', 'وَمَ<span class="tj-dgm">ن یَ</span>فۡعَلۡ'),
    ('ءَایَـٰتِ ٱللَّهِ هُزُوࣰاۚ', 'ءَا<span class="tj-mdd">یَـٰ</span>تِ <span class="tj-slt">ٱ</span>للَّهِ هُزُوࣰاۚ'),
    ('نِعۡمَتَ ٱللَّهِ', 'نِعۡمَتَ <span class="tj-slt">ٱ</span>للَّهِ'),
    ('وَمَاۤ أَنزَلَ', 'وَمَ<span class="tj-mdd">اۤ</span> أَ<span class="tj-khf">نزَ</span>لَ'),
    ('مِّنَ ٱلۡكِتَـٰبِ', '<span class="tj-ghn">مِّ</span>نَ <span class="tj-slt">ٱ</span>لۡكِ<span class="tj-mdd">تَـٰ</span>بِ'),
    ('وَٱلۡحِكۡمَةِ', 'وَ<span class="tj-slt">ٱ</span>لۡحِكۡمَةِ'),
    ('وَٱتَّقُوا۟ ٱللَّهَ', 'وَ<span class="tj-slt">ٱ</span>تَّقُوا۟ <span class="tj-slt">ٱ</span>للَّهَ'),
    ('أَنَّ ٱللَّهَ', 'أَ<span class="tj-ghn">نَّ</span> <span class="tj-slt">ٱ</span>للَّهَ'),
])

# Ayah 232
content = apply_replacements(content, 232, [
    ('ٱلنِّسَاۤءَ', '<span class="tj-slt">ٱل</span>نِّسَ<span class="tj-mdd">اۤ</span>ءَ'),
    ('أَجَلَهُنَّ', 'أَجَلَهُ<span class="tj-ghn">نَّ</span>'),
    ('تَعۡضُلُوهُنَّ أَن یَنكِحۡنَ', 'تَعۡضُلُوهُ<span class="tj-ghn">نَّ</span> أَ<span class="tj-dgm">ن یَ</span><span class="tj-khf">نكِ</span>حۡنَ'),
    ('أَزۡوَ', 'أَزۡوَ'),
    ('جَهُنَّ', 'جَهُ<span class="tj-ghn">نَّ</span>'),
    ('بِٱلۡمَعۡرُوفِۗ', 'بِ<span class="tj-slt">ٱ</span>لۡمَعۡرُوفِۗ'),
    ('مِنكُمۡ', 'مِ<span class="tj-khf">نكُ</span>مۡ'),
    ('بِٱللَّهِ', 'بِ<span class="tj-slt">ٱ</span>للَّهِ'),
    ('وَٱلۡیَوۡمِ', 'وَ<span class="tj-slt">ٱ</span>لۡیَوۡمِ'),
    ('ٱلۡـَٔاخِرِۗ', '<span class="tj-slt">ٱ</span>لۡـَٔاخِرِۗ'),
    ('وَٱللَّهُ', 'وَ<span class="tj-slt">ٱ</span>للَّهُ'),
    ('أَنتُمۡ', 'أَ<span class="tj-khf">نتُ</span>مۡ'),
])

# Ayah 233 - very long
content = apply_replacements(content, 233, [
    ('وَٱلۡوَ', 'وَ<span class="tj-slt">ٱ</span>لۡوَ'),
    ('أَوۡلَـٰدَهُنَّ', 'أَوۡ<span class="tj-mdd">لَـٰ</span>دَهُ<span class="tj-ghn">نَّ</span>'),
    ('ٱلرَّضَاعَةَۚ', '<span class="tj-slt">ٱل</span>رَّضَاعَةَۚ'),
    ('ٱلۡمَوۡلُودِ', '<span class="tj-slt">ٱ</span>لۡمَوۡلُودِ'),
    ('رِزۡقُهُنَّ', 'رِزۡقُهُ<span class="tj-ghn">نَّ</span>'),
    ('وَكِسۡوَتُهُنَّ', 'وَكِسۡوَتُهُ<span class="tj-ghn">نَّ</span>'),
    ('بِٱلۡمَعۡرُوفِۚ لَا تُكَلَّفُ', 'بِ<span class="tj-slt">ٱ</span>لۡمَعۡرُوفِۚ لَا تُكَلَّفُ'),
    ('نَفۡسٌ إِلَّا', 'نَفۡسٌ إِلَّا'),
    ('لَا تُضَاۤرَّ', 'لَا تُضَ<span class="tj-mdd">اۤ</span>رَّ'),
    ('مَوۡلُودࣱ لَّهُۥ', 'مَوۡلُو<span class="tj-dgm">دࣱ لَّ</span>هُۥ'),
    ('وَعَلَى ٱلۡوَارِثِ', 'وَعَلَى <span class="tj-slt">ٱ</span>لۡوَارِثِ'),
    ('فَإِنۡ أَرَادَا', 'فَإِنۡ أَرَادَا'),
    ('تَرَاضࣲ مِّنۡهُمَا', 'تَرَاضࣲ <span class="tj-ghn">مِّ</span>نۡهُمَا'),
    ('وَإِنۡ أَرَدتُّمۡ أَن تَسۡتَرۡضِعُوۤا۟', 'وَإِنۡ أَرَدتُّمۡ أَ<span class="tj-khf">ن تَ</span>سۡتَرۡضِعُوۤا۟'),
    ('أَوۡلَـٰدَكُمۡ', 'أَوۡ<span class="tj-mdd">لَـٰ</span>دَكُمۡ'),
    ('سَلَّمۡتُم مَّاۤ ءَاتَیۡتُم', 'سَلَّمۡتُم <span class="tj-ghn">مَّ</span><span class="tj-mdd">اۤ</span> ءَاتَیۡتُم'),
    ('بِٱلۡمَعۡرُوفِۗ وَٱتَّقُوا۟ ٱللَّهَ', 'بِ<span class="tj-slt">ٱ</span>لۡمَعۡرُوفِۗ وَ<span class="tj-slt">ٱ</span>تَّقُوا۟ <span class="tj-slt">ٱ</span>للَّهَ'),
    ('أَنَّ ٱللَّهَ', 'أَ<span class="tj-ghn">نَّ</span> <span class="tj-slt">ٱ</span>للَّهَ'),
])

# Ayah 234
content = apply_replacements(content, 234, [
    ('وَٱلَّذِینَ', 'وَ<span class="tj-slt">ٱلَّ</span>ذِینَ'),
    ('مِنكُمۡ', 'مِ<span class="tj-khf">نكُ</span>مۡ'),
    ('أَرۡبَعَةَ', 'أَرۡبَعَةَ'),
    ('بِٱلۡمَعۡرُوفِۗ', 'بِ<span class="tj-slt">ٱ</span>لۡمَعۡرُوفِۗ'),
    ('وَٱللَّهُ', 'وَ<span class="tj-slt">ٱ</span>للَّهُ'),
])

with open('section-15.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - ayahs 231-234 tajweed applied")
