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

# Ayah 212
# زُیِّنَ لِلَّذِینَ كَفَرُوا۟ ٱلۡحَیَوٰةُ ٱلدُّنۡیَا وَیَسۡخَرُونَ مِنَ ٱلَّذِینَ ءَامَنُوا۟ۘ وَٱلَّذِینَ ٱتَّقَوۡا۟ فَوۡقَهُمۡ یَوۡمَ ٱلۡقِیَـٰمَةِۗ وَٱللَّهُ یَرۡزُقُ مَن یَشَاۤءُ بِغَیۡرِ حِسَابࣲ
content = apply_replacements(content, 212, [
    ('ٱلۡحَیَوٰةُ', '<span class="tj-slt">ٱ</span>لۡحَیَ<span class="tj-mdd">وٰ</span>ةُ'),
    ('ٱلدُّنۡیَا', '<span class="tj-slt">ٱل</span>دُّنۡیَا'),
    ('مِنَ ٱلَّذِینَ', 'مِنَ <span class="tj-slt">ٱلَّ</span>ذِینَ'),
    ('وَٱلَّذِینَ ٱتَّقَوۡا۟', 'وَ<span class="tj-slt">ٱلَّ</span>ذِینَ <span class="tj-slt">ٱ</span>تَّقَوۡا۟'),
    ('ٱلۡقِیَـٰمَةِۗ', '<span class="tj-slt">ٱ</span>لۡقِ<span class="tj-mdd">یَـٰ</span>مَةِۗ'),
    ('وَٱللَّهُ', 'وَ<span class="tj-slt">ٱ</span>للَّهُ'),
    ('مَن یَشَاۤءُ', 'مَ<span class="tj-dgm">ن یَ</span>شَ<span class="tj-mdd">اۤ</span>ءُ'),
])

# Ayah 213 (very long ayah)
# كَانَ ٱلنَّاسُ أُمَّةࣰ وَ ٰ⁠حِدَةࣰ فَبَعَثَ ٱللَّهُ ٱلنَّبِیِّـۧنَ مُبَشِّرِینَ وَمُنذِرِینَ وَأَنزَلَ مَعَهُمُ ٱلۡكِتَـٰبَ بِٱلۡحَقِّ لِیَحۡكُمَ بَیۡنَ ٱلنَّاسِ فِیمَا ٱخۡتَلَفُوا۟ فِیهِۚ وَمَا ٱخۡتَلَفَ فِیهِ إِلَّا ٱلَّذِینَ أُوتُوهُ مِنۢ بَعۡدِ مَا جَاۤءَتۡهُمُ ٱلۡبَیِّنَـٰتُ بَغۡیَۢا بَیۡنَهُمۡۖ فَهَدَى ٱللَّهُ ٱلَّذِینَ ءَامَنُوا۟ لِمَا ٱخۡتَلَفُوا۟ فِیهِ مِنَ ٱلۡحَقِّ بِإِذنِهِۦۗ وَٱللَّهُ یَهۡدِی مَن یَشَاۤءُ إِلَىٰ صِرَ ٰ⁠طࣲ مُّسۡتَقِیمٍ
content = apply_replacements(content, 213, [
    ('ٱلنَّاسُ أُمَّةࣰ', '<span class="tj-slt">ٱل</span>نَّاسُ أُ<span class="tj-ghn">مَّ</span>ةࣰ'),
    ('ٱللَّهُ ٱلنَّبِیِّـۧنَ', '<span class="tj-slt">ٱ</span>للَّهُ <span class="tj-slt">ٱل</span>نَّبِیِّـۧنَ'),
    ('وَمُنذِرِینَ', 'وَمُ<span class="tj-khf">نذِ</span>رِینَ'),
    ('وَأَنزَلَ', 'وَأَ<span class="tj-khf">نزَ</span>لَ'),
    ('ٱلۡكِتَـٰبَ بِٱلۡحَقِّ', '<span class="tj-slt">ٱ</span>لۡكِ<span class="tj-mdd">تَـٰ</span>بَ بِ<span class="tj-slt">ٱ</span>لۡحَقِّ'),
    ('ٱلنَّاسِ فِیمَا ٱخۡتَلَفُوا۟', '<span class="tj-slt">ٱل</span>نَّاسِ فِیمَا <span class="tj-slt">ٱ</span>خۡتَلَفُوا۟'),
    ('وَمَا ٱخۡتَلَفَ', 'وَمَا <span class="tj-slt">ٱ</span>خۡتَلَفَ'),
    ('إِلَّا ٱلَّذِینَ أُوتُوهُ مِنۢ بَعۡدِ', 'إِلَّا <span class="tj-slt">ٱلَّ</span>ذِینَ أُوتُوهُ مِ<span class="tj-qlb">نۢ بَ</span>عۡدِ'),
    ('جَاۤءَتۡهُمُ ٱلۡبَیِّنَـٰتُ', 'جَ<span class="tj-mdd">اۤ</span>ءَتۡهُمُ <span class="tj-slt">ٱ</span>لۡبَیِّ<span class="tj-mdd">نَـٰ</span>تُ'),
    ('بَغۡیَۢا بَیۡنَهُمۡۖ', 'بَغۡ<span class="tj-qlb">یَۢا بَ</span>یۡنَهُمۡۖ'),
    ('فَهَدَى ٱللَّهُ ٱلَّذِینَ', 'فَهَدَى <span class="tj-slt">ٱ</span>للَّهُ <span class="tj-slt">ٱلَّ</span>ذِینَ'),
    ('لِمَا ٱخۡتَلَفُوا۟', 'لِمَا <span class="tj-slt">ٱ</span>خۡتَلَفُوا۟'),
    ('ٱلۡحَقِّ بِإِذنِهِۦۗ', '<span class="tj-slt">ٱ</span>لۡحَقِّ بِإِذنِهِۦۗ'),
    ('وَٱللَّهُ یَهۡدِی', 'وَ<span class="tj-slt">ٱ</span>للَّهُ یَهۡدِی'),
    ('مَن یَشَاۤءُ إِلَىٰ', 'مَ<span class="tj-dgm">ن یَ</span>شَ<span class="tj-mdd">اۤ</span>ءُ إِلَ<span class="tj-mdd">ىٰ</span>'),
    ('طࣲ مُّسۡتَقِیمٍ', '<span class="tj-dgm">طࣲ</span> <span class="tj-ghn">مُّ</span>سۡتَقِیمٍ'),
])

# Ayah 214
# أَمۡ حَسِبۡتُمۡ أَن تَدۡخُلُوا۟ ٱلۡجَنَّةَ وَلَمَّا یَأۡتِكُم مَّثَلُ ٱلَّذِینَ خَلَوۡا۟ مِن قَبۡلِكُمۖ مَّسَّتۡهُمُ ٱلۡبَأۡسَاۤءُ وَٱلضَّرَّاۤءُ وَزُلۡزِلُوا۟ حَتَّىٰ یَقُولَ ٱلرَّسُولُ وَٱلَّذِینَ ءَامَنُوا۟ مَعَهُۥ مَتَىٰ نَصۡرُ ٱللَّهِۗ أَلَاۤ إِنَّ نَصۡرَ ٱللَّهِ قَرِیبࣱ
content = apply_replacements(content, 214, [
    ('حَسِبۡتُمۡ أَن تَدۡخُلُوا۟', 'حَسِ<span class="tj-qlq">بۡ</span>تُمۡ أَ<span class="tj-khf">ن تَ</span><span class="tj-qlq">دۡ</span>خُلُوا۟'),
    ('ٱلۡجَنَّةَ', '<span class="tj-slt">ٱ</span>لۡجَ<span class="tj-ghn">نَّ</span>ةَ'),
    ('وَلَمَّا', 'وَلَ<span class="tj-ghn">مَّ</span>ا'),
    ('یَأۡتِكُم مَّثَلُ', 'یَأۡتِكُم <span class="tj-ghn">مَّ</span>ثَلُ'),
    ('ٱلَّذِینَ خَلَوۡا۟', '<span class="tj-slt">ٱلَّ</span>ذِینَ خَلَوۡا۟'),
    ('مِن قَبۡلِكُمۖ', 'مِ<span class="tj-khf">ن قَ</span><span class="tj-qlq">بۡ</span>لِكُمۖ'),
    ('مَّسَّتۡهُمُ', '<span class="tj-ghn">مَّ</span>سَّتۡهُمُ'),
    ('ٱلۡبَأۡسَاۤءُ', '<span class="tj-slt">ٱ</span>لۡبَأۡسَ<span class="tj-mdd">اۤ</span>ءُ'),
    ('وَٱلضَّرَّاۤءُ', 'وَ<span class="tj-slt">ٱل</span>ضَّرَّ<span class="tj-mdd">اۤ</span>ءُ'),
    ('حَتَّىٰ یَقُولَ', 'حَتَّ<span class="tj-mdd">ىٰ</span> یَقُولَ'),
    ('ٱلرَّسُولُ', '<span class="tj-slt">ٱل</span>رَّسُولُ'),
    ('وَٱلَّذِینَ ءَامَنُوا۟', 'وَ<span class="tj-slt">ٱلَّ</span>ذِینَ ءَامَنُوا۟'),
    ('مَتَىٰ نَصۡرُ ٱللَّهِۗ', 'مَتَ<span class="tj-mdd">ىٰ</span> نَصۡرُ <span class="tj-slt">ٱ</span>للَّهِۗ'),
    ('أَلَاۤ إِنَّ نَصۡرَ ٱللَّهِ', 'أَلَ<span class="tj-mdd">اۤ</span> إِ<span class="tj-ghn">نَّ</span> نَصۡرَ <span class="tj-slt">ٱ</span>للَّهِ'),
])

with open('section-14.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - ayahs 212-214 tajweed applied")
