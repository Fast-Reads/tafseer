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
            print(f"  MISS: '{old[:20]}' in ayah {num}")
    content = content[:start] + ayah_text + content[end:]
    print(f"  Ayah {num}: {count}/{len(replacements)} replacements OK")
    return content

# Ayah 215
content = apply_replacements(content, 215, [
    ('یُنفِقُونَۖ', 'یُ<span class="tj-khf">نفِ</span>قُونَۖ'),
    ('مَاۤ أَنفَقۡتُم', 'مَ<span class="tj-mdd">اۤ</span> أَ<span class="tj-khf">نفَ</span><span class="tj-qlq">قۡ</span>تُم'),
    ('مِّنۡ خَیۡرࣲ فَلِلۡوَ', '<span class="tj-ghn">مِّ</span>نۡ خَیۡ<span class="tj-khf">رࣲ فَ</span>لِلۡوَ'),
    ('وَٱلۡأَقۡرَبِینَ', 'وَ<span class="tj-slt">ٱ</span>لۡأَ<span class="tj-qlq">قۡ</span>رَبِینَ'),
    ('وَٱلۡیَتَـٰمَىٰ', 'وَ<span class="tj-slt">ٱ</span>لۡیَ<span class="tj-mdd">تَـٰ</span>مَىٰ'),
    ('وَٱلۡمَسَـٰكِینِ', 'وَ<span class="tj-slt">ٱ</span>لۡمَ<span class="tj-mdd">سَـٰ</span>كِینِ'),
    ('وَٱبۡنِ', 'وَ<span class="tj-slt">ٱ</span>بۡنِ'),
    ('ٱلسَّبِیلِۗ', '<span class="tj-slt">ٱل</span>سَّبِیلِۗ'),
    ('خَیۡرࣲ فَإِنَّ', 'خَیۡ<span class="tj-khf">رࣲ فَ</span>إِ<span class="tj-ghn">نَّ</span>'),
    ('ٱللَّهَ', '<span class="tj-slt">ٱ</span>للَّهَ'),
])

# Ayah 216
content = apply_replacements(content, 216, [
    ('ٱلۡقِتَالُ', '<span class="tj-slt">ٱ</span>لۡقِتَالُ'),
    ('كُرۡهࣱ لَّكُمۡۖ', 'كُرۡ<span class="tj-dgm">هࣱ لَّ</span>كُمۡۖ'),
    ('وَعَسَىٰۤ أَن تَكۡرَ', 'وَعَسَ<span class="tj-mdd">ىٰۤ</span> أَ<span class="tj-khf">ن تَ</span>كۡرَ'),
    ('شَیۡـࣰٔا وَهُوَ خَیۡرࣱ لَّكُمۡۖ', 'شَیۡ<span class="tj-dgm">ـࣰٔا وَ</span>هُوَ خَیۡ<span class="tj-dgm">رࣱ لَّ</span>كُمۡۖ'),
    ('وَعَسَىٰۤ أَن تُحِبُّوا۟', 'وَعَسَ<span class="tj-mdd">ىٰۤ</span> أَ<span class="tj-khf">ن تُ</span>حِبُّوا۟'),
    ('شَیۡـࣰٔا وَهُوَ شَرࣱّ لَّكُمۡۚ', 'شَیۡ<span class="tj-dgm">ـࣰٔا وَ</span>هُوَ شَ<span class="tj-dgm">رࣱّ لَّ</span>كُمۡۚ'),
    ('وَٱللَّهُ', 'وَ<span class="tj-slt">ٱ</span>للَّهُ'),
    ('أَنتُمۡ', 'أَ<span class="tj-khf">نتُ</span>مۡ'),
])

# Ayah 217
content = apply_replacements(content, 217, [
    ('ٱلشَّهۡرِ', '<span class="tj-slt">ٱل</span>شَّهۡرِ'),
    ('ٱلۡحَرَامِ قِتَالࣲ فِیهِۖ', '<span class="tj-slt">ٱ</span>لۡحَرَامِ قِتَا<span class="tj-khf">لࣲ فِ</span>یهِۖ'),
    ('قِتَالࣱ فِیهِ', 'قِتَا<span class="tj-khf">لࣱ فِ</span>یهِ'),
    ('عَن سَبِیلِ', 'عَ<span class="tj-khf">ن سَ</span>بِیلِ'),
    ('ٱللَّهِ وَكُفۡرُۢ بِهِۦ', '<span class="tj-slt">ٱ</span>للَّهِ وَكُفۡ<span class="tj-qlb">رُۢ بِ</span>هِۦ'),
    ('وَٱلۡمَسۡجِدِ', 'وَ<span class="tj-slt">ٱ</span>لۡمَسۡجِدِ'),
    ('ٱلۡحَرَامِ وَإِخۡرَاجُ', '<span class="tj-slt">ٱ</span>لۡحَرَامِ وَإِخۡرَاجُ'),
    ('عِندَ ٱللَّهِۚ', 'عِ<span class="tj-khf">ندَ</span> <span class="tj-slt">ٱ</span>للَّهِۚ'),
    ('وَٱلۡفِتۡنَةُ', 'وَ<span class="tj-slt">ٱ</span>لۡفِتۡنَةُ'),
    ('ٱلۡقَتۡلِۗ', '<span class="tj-slt">ٱ</span>لۡقَتۡلِۗ'),
    ('یُقَـٰتِلُونَكُمۡ', 'یُ<span class="tj-mdd">قَـٰ</span>تِلُونَكُمۡ'),
    ('ٱسۡتَطَـٰعُوا۟ۚ', '<span class="tj-slt">ٱ</span>سۡتَ<span class="tj-mdd">طَـٰ</span>عُوا۟ۚ'),
    ('عَن دِینِكُمۡ', 'عَ<span class="tj-khf">ن دِ</span>ینِكُمۡ'),
    ('وَمَن یَرۡتَدِدۡ', 'وَمَ<span class="tj-dgm">ن یَ</span>رۡتَدِ<span class="tj-qlq">دۡ</span>'),
    ('مِنكُمۡ', 'مِ<span class="tj-khf">نكُ</span>مۡ'),
    ('عَن دِینِهِۦ', 'عَ<span class="tj-khf">ن دِ</span>ینِهِۦ'),
    ('كَافِرࣱ فَأُو۟لَـٰۤىِٕكَ', 'كَافِ<span class="tj-khf">رࣱ فَ</span>أُ<span class="tj-slt">و۟</span><span class="tj-mdd">لَـٰۤ</span>ىِٕكَ'),
    ('أَعۡمَـٰلُهُمۡ', 'أَعۡ<span class="tj-mdd">مَـٰ</span>لُهُمۡ'),
    ('ٱلدُّنۡیَا', '<span class="tj-slt">ٱل</span>دُّنۡیَا'),
    ('وَٱلۡـَٔاخِرَةِۖ', 'وَ<span class="tj-slt">ٱ</span>لۡـَٔاخِرَةِۖ'),
    ('وَأُو۟لَـٰۤىِٕكَ أَصۡحَـٰبُ', 'وَأُ<span class="tj-slt">و۟</span><span class="tj-mdd">لَـٰۤ</span>ىِٕكَ أَصۡ<span class="tj-mdd">حَـٰ</span>بُ'),
    ('ٱلنَّارِۖ', '<span class="tj-slt">ٱل</span>نَّارِۖ'),
    ('خَـٰلِدُونَ', '<span class="tj-mdd">خَـٰ</span>لِدُونَ'),
])

# Ayah 218
content = apply_replacements(content, 218, [
    ('إِنَّ ٱلَّذِینَ', 'إِ<span class="tj-ghn">نَّ</span> <span class="tj-slt">ٱلَّ</span>ذِینَ'),
    ('وَٱلَّذِینَ', 'وَ<span class="tj-slt">ٱلَّ</span>ذِینَ'),
    ('وَجَـٰهَدُوا۟', 'وَ<span class="tj-mdd">جَـٰ</span>هَدُوا۟'),
    ('ٱللَّهِ أُو۟لَـٰۤىِٕكَ', '<span class="tj-slt">ٱ</span>للَّهِ أُ<span class="tj-slt">و۟</span><span class="tj-mdd">لَـٰۤ</span>ىِٕكَ'),
    ('رَحۡمَتَ ٱللَّهِۚ', 'رَحۡمَتَ <span class="tj-slt">ٱ</span>للَّهِۚ'),
    ('وَٱللَّهُ', 'وَ<span class="tj-slt">ٱ</span>للَّهُ'),
    ('غَفُورࣱ رَّحِیمࣱ', 'غَفُو<span class="tj-dgm">رࣱ رَّ</span>حِیمࣱ'),
])

with open('section-15.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - ayahs 215-218 tajweed applied")
