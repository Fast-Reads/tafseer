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

# Ayah 239
# Text: فَإِنۡ خِفۡتُمۡ فَرِجَالًا أَوۡ رُكۡبَانࣰاۖ فَإِذَاۤ أَمِنتُمۡ فَٱذۡكُرُوا۟ ٱللَّهَ كَمَا عَلَّمَكُم مَّا لَمۡ تَكُونُوا۟ تَعۡلَمُونَ
content = apply_replacements(content, 239, [
    ('فَإِذَاۤ أَمِنتُمۡ', 'فَإِذَ<span class="tj-mdd">اۤ</span> أَمِ<span class="tj-khf">نتُ</span>مۡ'),
    ('فَٱذۡكُرُوا۟', 'فَ<span class="tj-slt">ٱ</span>ذۡكُرُوا۟'),
    ('ٱللَّهَ', '<span class="tj-slt">ٱ</span>للَّهَ'),
    ('عَلَّمَكُم مَّا', 'عَلَّمَكُم <span class="tj-ghn">مَّ</span>ا'),
])

# Ayah 240
# Text: وَٱلَّذِینَ یُتَوَفَّوۡنَ مِنكُمۡ وَیَذَرُونَ أَزۡوَ ٰ⁠جࣰا وَصِیَّةࣰ لِّأَزۡوَ ٰ⁠جِهِم مَّتَـٰعًا إِلَى ٱلۡحَوۡلِ غَیۡرَ إِخۡرَاجࣲۚ فَإِنۡ خَرَجۡنَ فَلَا جُنَاحَ عَلَیۡكُمۡ فِی مَا فَعَلۡنَ فِیۤ أَنفُسِهِنَّ مِن مَّعۡرُوفࣲۗ وَٱللَّهُ عَزِیزٌ حَكِیمࣱ
content = apply_replacements(content, 240, [
    ('وَٱلَّذِینَ', 'وَ<span class="tj-slt">ٱلَّ</span>ذِینَ'),
    ('مِنكُمۡ', 'مِ<span class="tj-khf">نكُ</span>مۡ'),
    ('جࣰا وَصِیَّةࣰ لِّ', 'جَ<span class="tj-dgm">ࣰا وَ</span>صِیَّ<span class="tj-dgm">ةࣰ لِّ</span>'),
    ('جِهِم مَّتَـٰعًا', 'جِهِم <span class="tj-ghn">مَّ</span><span class="tj-mdd">تَـٰ</span>عًا'),
    ('ٱلۡحَوۡلِ', '<span class="tj-slt">ٱ</span>لۡحَوۡلِ'),
    ('خَرَجۡنَ', 'خَرَ<span class="tj-qlq">جۡ</span>نَ'),
    ('فِیۤ أَنفُسِهِنَّ', 'فِ<span class="tj-mdd">یۤ</span> أَ<span class="tj-khf">نفُ</span>سِهِ<span class="tj-ghn">نَّ</span>'),
    ('مِن مَّعۡرُوفࣲۗ', 'مِ<span class="tj-dgm">ن مَّ</span>عۡرُوفࣲۗ'),
    ('وَٱللَّهُ', 'وَ<span class="tj-slt">ٱ</span>للَّهُ'),
])

# Ayah 241
# Text: وَلِلۡمُطَلَّقَـٰتِ مَتَـٰعُۢ بِٱلۡمَعۡرُوفِۖ حَقًّا عَلَى ٱلۡمُتَّقِینَ
content = apply_replacements(content, 241, [
    ('مُطَلَّقَـٰتِ', 'مُطَلَّ<span class="tj-mdd">قَـٰ</span>تِ'),
    ('مَتَـٰعُۢ بِٱلۡمَعۡرُوفِۖ', 'مَ<span class="tj-mdd">تَـٰ</span><span class="tj-qlb">عُۢ بِ</span><span class="tj-slt">ٱ</span>لۡمَعۡرُوفِۖ'),
    ('ٱلۡمُتَّقِینَ', '<span class="tj-slt">ٱ</span>لۡمُتَّقِینَ'),
])

# Ayah 242
# Text: كَذَ ٰ⁠لِكَ یُبَیِّنُ ٱللَّهُ لَكُمۡ ءَایَـٰتِهِۦ لَعَلَّكُمۡ تَعۡقِلُونَ
content = apply_replacements(content, 242, [
    ('ٱللَّهُ لَكُمۡ', '<span class="tj-slt">ٱ</span>للَّهُ لَكُمۡ'),
    ('ءَایَـٰتِهِۦ', 'ءَا<span class="tj-mdd">یَـٰ</span>تِهِۦ'),
])

with open('section-15.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - ayahs 239-242 tajweed applied")
