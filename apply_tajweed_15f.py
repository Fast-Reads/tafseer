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

# Ayah 235 - long ayah about khitbah
# Text: وَلَا جُنَاحَ عَلَیۡكُمۡ فِیمَا عَرَّضۡتُم بِهِۦ مِنۡ خِطۡبَةِ ٱلنِّسَاۤءِ أَوۡ أَكۡنَنتُمۡ فِیۤ أَنفُسِكُمۡۚ عَلِمَ ٱللَّهُ أَنَّكُمۡ سَتَذۡكُرُونَهُنَّ وَلَـٰكِن لَّا تُوَاعِدُوهُنَّ سِرًّا إِلَّاۤ أَن تَقُولُوا۟ قَوۡلࣰا مَّعۡرُوفࣰاۚ وَلَا تَعۡزِمُوا۟ عُقۡدَةَ ٱلنِّكَاحِ حَتَّىٰ یَبۡلُغَ ٱلۡكِتَـٰبُ أَجَلَهُۥۚ وَٱعۡلَمُوۤا۟ أَنَّ ٱللَّهَ یَعۡلَمُ مَا فِیۤ أَنفُسِكُمۡ فَٱحۡذَرُوهُۚ وَٱعۡلَمُوۤا۟ أَنَّ ٱللَّهَ غَفُورٌ حَلِیمࣱ
content = apply_replacements(content, 235, [
    ('مِنۡ خِطۡبَةِ', 'مِنۡ خِطۡبَةِ'),
    ('ٱلنِّسَاۤءِ', '<span class="tj-slt">ٱل</span>نِّسَ<span class="tj-mdd">اۤ</span>ءِ'),
    ('فِیۤ أَنفُسِكُمۡۚ', 'فِ<span class="tj-mdd">یۤ</span> أَ<span class="tj-khf">نفُ</span>سِكُمۡۚ'),
    ('ٱللَّهُ أَنَّكُمۡ', '<span class="tj-slt">ٱ</span>للَّهُ أَ<span class="tj-ghn">نَّ</span>كُمۡ'),
    ('سَتَذۡكُرُونَهُنَّ', 'سَتَذۡكُرُونَهُ<span class="tj-ghn">نَّ</span>'),
    ('وَلَـٰكِن لَّا تُوَاعِدُوهُنَّ', 'وَ<span class="tj-mdd">لَـٰ</span>كِ<span class="tj-dgm">ن لَّ</span>ا تُوَاعِدُوهُ<span class="tj-ghn">نَّ</span>'),
    ('إِلَّاۤ أَن تَقُولُوا۟', 'إِلَّ<span class="tj-mdd">اۤ</span> أَ<span class="tj-khf">ن تَ</span>قُولُوا۟'),
    ('قَوۡلࣰا مَّعۡرُوفࣰاۚ', 'قَوۡلَ<span class="tj-dgm">ࣰا مَّ</span>عۡرُوفࣰاۚ'),
    ('عُقۡدَةَ ٱلنِّكَاحِ', 'عُقۡدَةَ <span class="tj-slt">ٱل</span>نِّكَاحِ'),
    ('ٱلۡكِتَـٰبُ', '<span class="tj-slt">ٱ</span>لۡكِ<span class="tj-mdd">تَـٰ</span>بُ'),
    ('أَنَّ ٱللَّهَ یَعۡلَمُ', 'أَ<span class="tj-ghn">نَّ</span> <span class="tj-slt">ٱ</span>للَّهَ یَعۡلَمُ'),
    ('فِیۤ أَنفُسِكُمۡ فَٱحۡذَرُوهُۚ', 'فِ<span class="tj-mdd">یۤ</span> أَ<span class="tj-khf">نفُ</span>سِكُمۡ فَ<span class="tj-slt">ٱ</span>حۡذَرُوهُۚ'),
    ('أَنَّ ٱللَّهَ غَفُورٌ', 'أَ<span class="tj-ghn">نَّ</span> <span class="tj-slt">ٱ</span>للَّهَ غَفُورٌ'),
])

# Ayah 236
# Text: لَّا جُنَاحَ عَلَیۡكُمۡ إِن طَلَّقۡتُمُ ٱلنِّسَاۤءَ مَا لَمۡ تَمَسُّوهُنَّ أَوۡ تَفۡرِضُوا۟ لَهُنَّ فَرِیضَةࣰۚ وَمَتِّعُوهُنَّ عَلَى ٱلۡمُوسِعِ قَدَرُهُۥ وَعَلَى ٱلۡمُقۡتِرِ قَدَرُهُۥ مَتَـٰعَۢا بِٱلۡمَعۡرُوفِۖ حَقًّا عَلَى ٱلۡمُحۡسِنِینَ
content = apply_replacements(content, 236, [
    ('إِن طَلَّقۡتُمُ', 'إِ<span class="tj-khf">ن طَ</span>لَّقۡتُمُ'),
    ('ٱلنِّسَاۤءَ', '<span class="tj-slt">ٱل</span>نِّسَ<span class="tj-mdd">اۤ</span>ءَ'),
    ('تَمَسُّوهُنَّ', 'تَمَسُّوهُ<span class="tj-ghn">نَّ</span>'),
    ('لَهُنَّ', 'لَهُ<span class="tj-ghn">نَّ</span>'),
    ('وَمَتِّعُوهُنَّ', 'وَمَتِّعُوهُ<span class="tj-ghn">نَّ</span>'),
    ('ٱلۡمُوسِعِ', '<span class="tj-slt">ٱ</span>لۡمُوسِعِ'),
    ('ٱلۡمُقۡتِرِ', '<span class="tj-slt">ٱ</span>لۡمُقۡتِرِ'),
    ('مَتَـٰعَۢا بِٱلۡمَعۡرُوفِۖ', 'مَ<span class="tj-mdd">تَـٰ</span>عَ<span class="tj-qlb">ۢا بِ</span><span class="tj-slt">ٱ</span>لۡمَعۡرُوفِۖ'),
    ('ٱلۡمُحۡسِنِینَ', '<span class="tj-slt">ٱ</span>لۡمُحۡسِنِینَ'),
])

# Ayah 237
# Text: وَإِن طَلَّقۡتُمُوهُنَّ مِن قَبۡلِ أَن تَمَسُّوهُنَّ وَقَدۡ فَرَضۡتُمۡ لَهُنَّ فَرِیضَةࣰ فَنِصۡفُ مَا فَرَضۡتُمۡ إِلَّاۤ أَن یَعۡفُونَ أَوۡ یَعۡفُوَا۟ ٱلَّذِی بِیَدِهِۦ عُقۡدَةُ ٱلنِّكَاحِۚ وَأَن تَعۡفُوۤا۟ أَقۡرَبُ لِلتَّقۡوَىٰۚ وَلَا تَنسَوُا۟ ٱلۡفَضۡلَ بَیۡنَكُمۡۚ إِنَّ ٱللَّهَ بِمَا تَعۡمَلُونَ بَصِیرٌ
content = apply_replacements(content, 237, [
    ('إِن طَلَّقۡتُمُوهُنَّ', 'إِ<span class="tj-khf">ن طَ</span>لَّقۡتُمُوهُ<span class="tj-ghn">نَّ</span>'),
    ('مِن قَبۡلِ أَن تَمَسُّوهُنَّ', 'مِ<span class="tj-khf">ن قَ</span>بۡلِ أَ<span class="tj-khf">ن تَ</span>مَسُّوهُ<span class="tj-ghn">نَّ</span>'),
    ('لَهُنَّ', 'لَهُ<span class="tj-ghn">نَّ</span>'),
    ('إِلَّاۤ أَن یَعۡفُونَ', 'إِلَّ<span class="tj-mdd">اۤ</span> أَ<span class="tj-dgm">ن یَ</span>عۡفُونَ'),
    ('ٱلَّذِی بِیَدِهِۦ', '<span class="tj-slt">ٱلَّ</span>ذِی بِیَدِهِۦ'),
    ('ٱلنِّكَاحِۚ', '<span class="tj-slt">ٱل</span>نِّكَاحِۚ'),
    ('لِلتَّقۡوَىٰۚ', 'لِل<span class="tj-slt">تَّ</span>قۡوَىٰۚ'),
    ('ٱلۡفَضۡلَ', '<span class="tj-slt">ٱ</span>لۡفَضۡلَ'),
    ('إِنَّ ٱللَّهَ', 'إِ<span class="tj-ghn">نَّ</span> <span class="tj-slt">ٱ</span>للَّهَ'),
])

# Ayah 238
# Text: حَـٰفِظُوا۟ عَلَى ٱلصَّلَوَ ٰ⁠تِ وَٱلصَّلَوٰةِ ٱلۡوُسۡطَىٰ وَقُومُوا۟ لِلَّهِ قَـٰنِتِینَ
content = apply_replacements(content, 238, [
    ('ٱلصَّلَوَ', '<span class="tj-slt">ٱل</span>صَّلَوَ'),
    ('وَٱلصَّلَوٰةِ', 'وَ<span class="tj-slt">ٱل</span>صَّلَوٰةِ'),
    ('ٱلۡوُسۡطَىٰ', '<span class="tj-slt">ٱ</span>لۡوُسۡطَىٰ'),
    ('قَـٰنِتِینَ', '<span class="tj-mdd">قَـٰ</span>نِتِینَ'),
])

with open('section-15.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - ayahs 235-238 tajweed applied")
