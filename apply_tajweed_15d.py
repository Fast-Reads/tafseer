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

# Ayah 227
content = apply_replacements(content, 227, [
    ('ٱلطَّلَـٰقَ', '<span class="tj-slt">ٱل</span>طَّ<span class="tj-mdd">لَـٰ</span>قَ'),
    ('فَإِنَّ ٱللَّهَ', 'فَإِ<span class="tj-ghn">نَّ</span> <span class="tj-slt">ٱ</span>للَّهَ'),
])

# Ayah 228
content = apply_replacements(content, 228, [
    ('وَٱلۡمُطَلَّقَـٰتُ', 'وَ<span class="tj-slt">ٱ</span>لۡمُطَلَّ<span class="tj-mdd">قَـٰ</span>تُ'),
    ('بِأَنفُسِهِنَّ', 'بِأَ<span class="tj-khf">نفُ</span>سِهِ<span class="tj-ghn">نَّ</span>'),
    ('ثَلَـٰثَةَ', 'ثَ<span class="tj-mdd">لَـٰ</span>ثَةَ'),
    ('قُرُوۤءࣲۚ', 'قُرُ<span class="tj-mdd">وۤ</span>ءࣲۚ'),
    ('لَهُنَّ أَن یَكۡتُمۡنَ', 'لَهُ<span class="tj-ghn">نَّ</span> أَ<span class="tj-dgm">ن یَ</span>كۡتُمۡنَ'),
    ('ٱللَّهُ فِیۤ أَرۡحَامِهِنَّ', '<span class="tj-slt">ٱ</span>للَّهُ فِ<span class="tj-mdd">یۤ</span> أَرۡحَامِهِ<span class="tj-ghn">نَّ</span>'),
    ('إِن كُنَّ یُؤۡمِنَّ', 'إِ<span class="tj-khf">ن كُ</span><span class="tj-ghn">نَّ</span> یُؤۡمِ<span class="tj-ghn">نَّ</span>'),
    ('بِٱللَّهِ', 'بِ<span class="tj-slt">ٱ</span>للَّهِ'),
    ('وَٱلۡیَوۡمِ', 'وَ<span class="tj-slt">ٱ</span>لۡیَوۡمِ'),
    ('ٱلۡـَٔاخِرِۚ', '<span class="tj-slt">ٱ</span>لۡـَٔاخِرِۚ'),
    ('بُعُولَتُهُنَّ', 'بُعُولَتُهُ<span class="tj-ghn">نَّ</span>'),
    ('بِرَدِّهِنَّ', 'بِرَدِّهِ<span class="tj-ghn">نَّ</span>'),
    ('إِصۡلَـٰحࣰاۚ', 'إِصۡ<span class="tj-mdd">لَـٰ</span>حࣰاۚ'),
    ('وَلَهُنَّ', 'وَلَهُ<span class="tj-ghn">نَّ</span>'),
    ('ٱلَّذِی', '<span class="tj-slt">ٱلَّ</span>ذِی'),
    ('عَلَیۡهِنَّ بِٱلۡمَعۡرُوفِۚ', 'عَلَیۡهِ<span class="tj-ghn">نَّ</span> بِ<span class="tj-slt">ٱ</span>لۡمَعۡرُوفِۚ'),
    ('عَلَیۡهِنَّ دَرَجَةࣱۗ', 'عَلَیۡهِ<span class="tj-ghn">نَّ</span> دَرَجَةࣱۗ'),
    ('وَٱللَّهُ', 'وَ<span class="tj-slt">ٱ</span>للَّهُ'),
])

# Ayah 229
content = apply_replacements(content, 229, [
    ('ٱلطَّلَـٰقُ', '<span class="tj-slt">ٱل</span>طَّ<span class="tj-mdd">لَـٰ</span>قُ'),
    ('فَإِمۡسَاكُۢ بِمَعۡرُوفٍ', 'فَإِمۡسَا<span class="tj-qlb">كُۢ بِ</span>مَعۡرُوفٍ'),
    ('تَسۡرِیحُۢ بِإِحۡسَـٰنࣲۗ', 'تَسۡرِی<span class="tj-qlb">حُۢ بِ</span>إِحۡ<span class="tj-mdd">سَـٰ</span>نࣲۗ'),
    ('أَن تَأۡخُذُوا۟', 'أَ<span class="tj-khf">ن تَ</span>أۡخُذُوا۟'),
    ('مِمَّاۤ ءَاتَیۡتُمُوهُنَّ', 'مِ<span class="tj-ghn">مَّ</span><span class="tj-mdd">اۤ</span> ءَاتَیۡتُمُوهُ<span class="tj-ghn">نَّ</span>'),
    ('إِلَّاۤ أَن یَخَافَاۤ', 'إِلَّ<span class="tj-mdd">اۤ</span> أَ<span class="tj-dgm">ن یَ</span>خَافَ<span class="tj-mdd">اۤ</span>'),
    ('حُدُودَ ٱللَّهِۖ', 'حُدُودَ <span class="tj-slt">ٱ</span>للَّهِۖ'),
    ('حُدُودَ ٱللَّهِ فَلَا جُنَاحَ', 'حُدُودَ <span class="tj-slt">ٱ</span>للَّهِ فَلَا جُنَاحَ'),
    ('ٱفۡتَدَتۡ', '<span class="tj-slt">ٱ</span>فۡتَدَتۡ'),
    ('حُدُودُ ٱللَّهِ فَلَا', 'حُدُودُ <span class="tj-slt">ٱ</span>للَّهِ فَلَا'),
    ('وَمَن یَتَعَدَّ', 'وَمَ<span class="tj-dgm">ن یَ</span>تَعَدَّ'),
    ('حُدُودَ ٱللَّهِ فَأُو۟لَـٰۤىِٕكَ', 'حُدُودَ <span class="tj-slt">ٱ</span>للَّهِ فَأُ<span class="tj-slt">و۟</span><span class="tj-mdd">لَـٰۤ</span>ىِٕكَ'),
    ('ٱلظَّـٰلِمُونَ', '<span class="tj-slt">ٱل</span>ظَّ<span class="tj-mdd">ـٰ</span>لِمُونَ'),
])

# Ayah 230
content = apply_replacements(content, 230, [
    ('فَإِن طَلَّقَهَا فَلَا تَحِلُّ', 'فَإِ<span class="tj-khf">ن طَ</span>لَّقَهَا فَلَا تَحِلُّ'),
    ('مِنۢ بَعۡدُ', 'مِ<span class="tj-qlb">نۢ بَ</span>عۡدُ'),
    ('تَنكِحَ', 'تَ<span class="tj-khf">نكِ</span>حَ'),
    ('فَإِن طَلَّقَهَا فَلَا جُنَاحَ', 'فَإِ<span class="tj-khf">ن طَ</span>لَّقَهَا فَلَا جُنَاحَ'),
    ('عَلَیۡهِمَاۤ أَن یَتَرَاجَعَاۤ', 'عَلَیۡهِمَ<span class="tj-mdd">اۤ</span> أَ<span class="tj-dgm">ن یَ</span>تَرَاجَعَ<span class="tj-mdd">اۤ</span>'),
    ('إِن ظَنَّاۤ أَن یُقِیمَا', 'إِ<span class="tj-khf">ن ظَ</span><span class="tj-ghn">نَّ</span><span class="tj-mdd">اۤ</span> أَ<span class="tj-dgm">ن یُ</span>قِیمَا'),
    ('حُدُودَ ٱللَّهِۗ', 'حُدُودَ <span class="tj-slt">ٱ</span>للَّهِۗ'),
    ('حُدُودُ ٱللَّهِ', 'حُدُودُ <span class="tj-slt">ٱ</span>للَّهِ'),
    ('لِقَوۡمࣲ یَعۡلَمُونَ', 'لِقَوۡ<span class="tj-dgm">مࣲ یَ</span>عۡلَمُونَ'),
])

with open('section-15.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - ayahs 227-230 tajweed applied")
