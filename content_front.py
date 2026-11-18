# -*- coding: utf-8 -*-
"""بخش آغازین سند: جلد و فهرست مطالب."""
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_front(D):
    # ---------- جلد ----------
    D.cover_page(
        title="مارشال مک‌لوهان",
        subtitle="پدر رسانه‌شناسی معاصر",
        meta_lines=[
            "زندگی، تحصیلات، نظریه‌ها، آثار، مصاحبه‌ها و نقدها",
            "سند پژوهشی برای مک‌لوهان‌شناسی حرفه‌ای",
            "",
            "دوره‌ی درسی: سواد رسانه‌ای و فضای مجازی",
            "برای: دکتر بشیر — ترم سوم ۱۴۰۵",
        ],
        presenter="تهیه‌کننده: محمد بختیاری\nدانشجوی دکتری مدیریت رسانه · مدرس سواد رسانه و فضای مجازی",
    )

    # ---------- فهرست مطالب ----------
    D.h1("فهرست مطالب")
    p = D.doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    from docx_engine import _set_run_font, MUTED
    r = p.add_run("برای نمایش فهرست: در Word کل سند را انتخاب (Ctrl+A) و کلید F9 را بزنید،\nیا راست‌کلیک روی ناحیه‌ی زیر و گزینه‌ی «Update Field» را بزنید.")
    _set_run_font(r, size=10, color=MUTED)
    D.toc_field()
    D.page_break()
