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

# Ayah 208
# یَـٰۤأَیُّهَا ٱلَّذِینَ ءَامَنُوا۟ ٱدۡخُلُوا۟ فِی ٱلسِّلۡمِ كَاۤفَّةࣰ وَلَا تَتَّبِعُوا۟ خُطُوَ ٰ⁠تِ ٱلشَّیۡطَـٰنِۚ إِنَّهُۥ لَكُمۡ عَدُوࣱّ مُّبِینࣱ
content = apply_replacements(content, 208, [
    ('یَـٰۤأَیُّهَا', 'یَ<span class="tj-mdd">ـٰۤ</span>أَیُّهَا'),
    ('ٱلَّذِینَ', '<span class="tj-slt">ٱلَّ</span>ذِینَ'),
    ('ٱدۡخُلُوا۟', '<span class="tj-slt">ٱ</span><span class="tj-qlq">دۡ</span>خُلُوا۟'),
    ('ٱلسِّلۡمِ', '<span class="tj-slt">ٱل</span>سِّلۡمِ'),
    ('كَاۤفَّةࣰ', 'كَ<span class="tj-mdd">اۤ</span>فَّةࣰ'),
    ('ٱلشَّیۡطَـٰنِۚ', '<span class="tj-slt">ٱل</span>شَّیۡ<span class="tj-mdd">طَـٰ</span>نِۚ'),
    ('إِنَّهُۥ', 'إِ<span class="tj-ghn">نَّ</span>هُۥ'),
    ('عَدُوࣱّ مُّبِینࣱ', 'عَدُو<span class="tj-dgm">ࣱّ مُّ</span>بِینࣱ'),
])

# Ayah 209
# فَإِن زَلَلۡتُم مِّنۢ بَعۡدِ مَا جَاۤءَتۡكُمُ ٱلۡبَیِّنَـٰتُ فَٱعۡلَمُوۤا۟ أَنَّ ٱللَّهَ عَزِیزٌ حَكِیمٌ
content = apply_replacements(content, 209, [
    ('فَإِن زَلَلۡتُم', 'فَإِ<span class="tj-khf">ن زَ</span>لَلۡتُم'),
    ('مِّنۢ بَعۡدِ', '<span class="tj-ghn">مِّ</span><span class="tj-qlb">نۢ بَ</span>عۡدِ'),
    ('جَاۤءَتۡكُمُ', 'جَ<span class="tj-mdd">اۤ</span>ءَتۡكُمُ'),
    ('ٱلۡبَیِّنَـٰتُ', '<span class="tj-slt">ٱ</span>لۡبَیِّ<span class="tj-mdd">نَـٰ</span>تُ'),
    ('فَٱعۡلَمُوۤا۟', 'فَ<span class="tj-slt">ٱ</span>عۡلَمُ<span class="tj-mdd">وۤ</span>ا۟'),
    ('أَنَّ ٱللَّهَ', 'أَ<span class="tj-ghn">نَّ</span> <span class="tj-slt">ٱ</span>للَّهَ'),
])

# Ayah 210
# هَلۡ یَنظُرُونَ إِلَّاۤ أَن یَأۡتِیَهُمُ ٱللَّهُ فِی ظُلَلࣲ مِّنَ ٱلۡغَمَامِ وَٱلۡمَلَـٰۤىِٕكَةُ وَقُضِیَ ٱلۡأَمۡرُۚ وَإِلَى ٱللَّهِ تُرۡجَعُ ٱلۡأُمُورُ
content = apply_replacements(content, 210, [
    ('یَنظُرُونَ', 'یَ<span class="tj-khf">نظُ</span>رُونَ'),
    ('إِلَّاۤ أَن یَأۡتِیَهُمُ', 'إِلَّ<span class="tj-mdd">اۤ</span> أَ<span class="tj-dgm">ن یَ</span>أۡتِیَهُمُ'),
    ('ٱللَّهُ فِی', '<span class="tj-slt">ٱ</span>للَّهُ فِی'),
    ('ظُلَلࣲ مِّنَ', 'ظُلَ<span class="tj-dgm">لࣲ</span> <span class="tj-ghn">مِّ</span>نَ'),
    ('ٱلۡغَمَامِ', '<span class="tj-slt">ٱ</span>لۡغَمَامِ'),
    ('وَٱلۡمَلَـٰۤىِٕكَةُ', 'وَ<span class="tj-slt">ٱ</span>لۡمَ<span class="tj-mdd">لَـٰۤ</span>ىِٕكَةُ'),
    ('ٱلۡأَمۡرُۚ', '<span class="tj-slt">ٱ</span>لۡأَمۡرُۚ'),
    ('ٱللَّهِ تُرۡجَعُ', '<span class="tj-slt">ٱ</span>للَّهِ تُرۡجَعُ'),
    ('ٱلۡأُمُورُ', '<span class="tj-slt">ٱ</span>لۡأُمُورُ'),
])

# Ayah 211
# سَلۡ بَنِیۤ إِسۡرَ ٰ⁠ۤءِیلَ كَمۡ ءَاتَیۡنَـٰهُم مِّنۡ ءَایَةِۭ بَیِّنَةࣲۗ وَمَن یُبَدِّلۡ نِعۡمَةَ ٱللَّهِ مِنۢ بَعۡدِ مَا جَاۤءَتۡهُ فَإِنَّ ٱللَّهَ شَدِیدُ ٱلۡعِقَابِ
content = apply_replacements(content, 211, [
    ('بَنِیۤ', 'بَنِ<span class="tj-mdd">یۤ</span>'),
    ('ءَاتَیۡنَـٰهُم', 'ءَاتَیۡ<span class="tj-mdd">نَـٰ</span>هُم'),
    ('مِّنۡ ءَایَةِۭ', '<span class="tj-ghn">مِّ</span>نۡ ءَایَةِۭ'),
    ('وَمَن یُبَدِّلۡ', 'وَمَ<span class="tj-dgm">ن یُ</span>بَدِّلۡ'),
    ('ٱللَّهِ مِنۢ بَعۡدِ', '<span class="tj-slt">ٱ</span>للَّهِ مِ<span class="tj-qlb">نۢ بَ</span>عۡدِ'),
    ('جَاۤءَتۡهُ', 'جَ<span class="tj-mdd">اۤ</span>ءَتۡهُ'),
    ('فَإِنَّ ٱللَّهَ', 'فَإِ<span class="tj-ghn">نَّ</span> <span class="tj-slt">ٱ</span>للَّهَ'),
    ('ٱلۡعِقَابِ', '<span class="tj-slt">ٱ</span>لۡعِقَابِ'),
])

with open('section-14.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - ayahs 208-211 tajweed applied")
