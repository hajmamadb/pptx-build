# -*- coding: utf-8 -*-
"""
موتور تولید سند Word (DOCX) به فارسی با چیدمان راست‌به‌چپ.
فونت: Vazirmatn (وزیرمتن) — با فونت پشتیبان IRANSans برای محیط‌های بدون وزیرمتن.
"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------- پالت ----------
NAVY   = RGBColor(0x0B, 0x25, 0x45)
NAVY2  = RGBColor(0x12, 0x3A, 0x63)
TEAL   = RGBColor(0x0F, 0x9C, 0x96)
INK    = RGBColor(0x0F, 0x20, 0x38)
MUTED  = RGBColor(0x5B, 0x6B, 0x80)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT  = RGBColor(0xF4, 0xF8, 0xFB)

FA_FONT = "Vazirmatn"        # فونت اصلی فارسی
FA_FONT_ALT = "IRANSans"     # فونت پشتیبان
EN_FONT = "Vazirmatn"        # برای متن انگلیسی داخل سند

def _set_run_font(run, size=11.5, bold=False, color=INK, italic=False, font=FA_FONT):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font
    # فونت فarsi (complex script) و east-asian را هم روی همان فونت بگذار
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts'); rpr.append(rfonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rfonts.set(qn(attr), font)

def _set_para_rtl(para):
    """راست‌به‌چپ کردن پاراگراف + راست‌چین کردن."""
    pPr = para._p.get_or_add_pPr()
    bidi = pPr.find(qn('w:bidi'))
    if bidi is None:
        bidi = OxmlElement('w:bidi'); pPr.append(bidi)
    bidi.set(qn('w:val'), '1')
    # راست‌چین
    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def _set_para_spacing(para, before=0, after=8, line=1.5):
    pf = para.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line

def _add_shading(para, hex_fill):
    """سایه‌زنی پس‌زمینه‌ی پاراگراف."""
    pPr = para._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hex_fill)
    pPr.append(shd)

class PersianDoc:
    def __init__(self):
        self.doc = Document()
        self._setup_base()
        self._setup_styles()

    def _setup_base(self):
        sec = self.doc.sections[0]
        sec.page_width = Cm(21); sec.page_height = Cm(29.7)  # A4
        sec.top_margin = Cm(2.4); sec.bottom_margin = Cm(2.4)
        sec.left_margin = Cm(2.6); sec.right_margin = Cm(2.6)

    def _setup_styles(self):
        # استایل پایه‌ی Normal
        normal = self.doc.styles['Normal']
        normal.font.name = FA_FONT
        normal.font.size = Pt(11.5)
        normal.font.color.rgb = INK
        rpr = normal.element.get_or_add_rPr()
        rfonts = rpr.find(qn('w:rFonts'))
        if rfonts is None:
            rfonts = OxmlElement('w:rFonts'); rpr.append(rfonts)
        for attr in ('w:ascii','w:hAnsi','w:cs','w:eastAsia'):
            rfonts.set(qn(attr), FA_FONT)

    # ---------- عناصر ----------
    def h1(self, fa_text, num=None):
        """تیتر فصل (سطح ۱) — با شماره."""
        p = self.doc.add_paragraph()
        _set_para_rtl(p)
        _set_para_spacing(p, before=18, after=10, line=1.2)
        # خط جداکننده‌ی بالا
        if num is not None:
            label = f"فصل {num}  ·  {fa_text}"
        else:
            label = fa_text
        run = p.add_run(label)
        _set_run_font(run, size=18, bold=True, color=NAVY)
        # نوار زبر زیر تیتر (با شدم‌کردن)
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '18')
        bottom.set(qn('w:space'), '4'); bottom.set(qn('w:color'), '0F9C96')
        pBdr.append(bottom); pPr.append(pBdr)
        # style برای TOC
        p.style = self.doc.styles['Heading 1']
        # بازگرداندن فونت و رنگ (چون Heading 1 استایل خودش را دارد)
        for r in p.runs:
            _set_run_font(r, size=18, bold=True, color=NAVY)
        _set_para_rtl(p)
        _set_para_spacing(p, before=18, after=10, line=1.2)
        return p

    def h2(self, fa_text):
        p = self.doc.add_paragraph()
        p.style = self.doc.styles['Heading 2']
        _set_para_rtl(p)
        _set_para_spacing(p, before=14, after=6, line=1.2)
        run = p.add_run(fa_text)
        _set_run_font(run, size=14.5, bold=True, color=NAVY2)
        return p

    def h3(self, fa_text):
        p = self.doc.add_paragraph()
        p.style = self.doc.styles['Heading 3']
        _set_para_rtl(p)
        _set_para_spacing(p, before=10, after=4, line=1.2)
        run = p.add_run(fa_text)
        _set_run_font(run, size=12.5, bold=True, color=TEAL)
        return p

    def para(self, text, size=11.5, after=8, color=INK, bold=False, italic=False,
             align=None, line=1.6, first_indent=False):
        """پاراگراف فارسی (یا انگلیسی)."""
        p = self.doc.add_paragraph()
        # تشخیص جهت: اگر بیشتر کاراکترها انگلیسی بود LTR
        en_chars = sum(1 for c in text if ord(c) < 0x600)
        is_ltr = en_chars > len(text) * 0.5
        if align is None:
            if is_ltr:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                _set_para_spacing(p, before=0, after=after, line=line)
            else:
                _set_para_rtl(p)
                _set_para_spacing(p, before=0, after=after, line=line)
        else:
            p.alignment = align
            _set_para_spacing(p, before=0, after=after, line=line)
        run = p.add_run(text)
        _set_run_font(run, size=size, bold=bold, color=color, italic=italic)
        if first_indent and not is_ltr:
            p.paragraph_format.first_line_indent = Cm(0.8)
        return p

    def para_runs(self, runs, size=11.5, after=8, line=1.6):
        """پاراگراف با چند run (برای mix فارسی/انگلیسی و bold).
        runs: list of (text, dict_options)"""
        p = self.doc.add_paragraph()
        _set_para_rtl(p)
        _set_para_spacing(p, before=0, after=after, line=line)
        for text, opts in runs:
            run = p.add_run(text)
            _set_run_font(run,
                          size=opts.get('size', size),
                          bold=opts.get('bold', False),
                          color=opts.get('color', INK),
                          italic=opts.get('italic', False),
                          font=opts.get('font', FA_FONT))
            if opts.get('rtl') is False:
                # run انگلیسی چپ‌چین
                rpr = run._element.get_or_add_rPr()
        return p

    def bullet(self, text, size=11.5, color=INK):
        p = self.doc.add_paragraph()
        _set_para_rtl(p)
        _set_para_spacing(p, before=0, after=5, line=1.5)
        p.paragraph_format.left_indent = Cm(0.6)
        run = p.add_run("▪  " + text)
        _set_run_font(run, size=size, color=color)
        return p

    def quote(self, fa_text, en_text=None, cite=None, size=12.5):
        """نقل‌قول — با سایه‌ی ملایم و خط راست‌چین."""
        p = self.doc.add_paragraph()
        _set_para_rtl(p)
        _set_para_spacing(p, before=6, after=4, line=1.5)
        _add_shading(p, "E4F4F3")
        # خط عمودی راست (border right)
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        right = OxmlElement('w:right')
        right.set(qn('w:val'), 'single'); right.set(qn('w:sz'), '24')
        right.set(qn('w:space'), '6'); right.set(qn('w:color'), '0F9C96')
        pBdr.append(right); pPr.append(pBdr)
        run = p.add_run(fa_text)
        _set_run_font(run, size=size, bold=True, color=NAVY, italic=True)
        if en_text:
            p2 = self.doc.add_paragraph()
            _set_para_rtl(p2)
            _set_para_spacing(p2, before=0, after=2, line=1.3)
            _add_shading(p2, "E4F4F3")
            pPr2 = p2._p.get_or_add_pPr()
            pBdr2 = OxmlElement('w:pBdr')
            right2 = OxmlElement('w:right')
            right2.set(qn('w:val'), 'single'); right2.set(qn('w:sz'), '24')
            right2.set(qn('w:space'), '6'); right2.set(qn('w:color'), '0F9C96')
            pBdr2.append(right2); pPr2.append(pBdr2)
            run2 = p2.add_run(en_text)
            _set_run_font(run2, size=size-1.5, italic=True, color=NAVY2, font=FA_FONT)
        if cite:
            p3 = self.doc.add_paragraph()
            _set_para_rtl(p3)
            _set_para_spacing(p3, before=0, after=10, line=1.2)
            run3 = p3.add_run("— " + cite)
            _set_run_font(run3, size=10, color=MUTED, bold=True)
        return p

    def callout(self, title, text, fill="F4F8FB", bar="0F9C96"):
        """جعبه‌ی نکته (نظیر warnbox در PPTX)."""
        p = self.doc.add_paragraph()
        _set_para_rtl(p)
        _set_para_spacing(p, before=6, after=2, line=1.4)
        _add_shading(p, fill)
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        right = OxmlElement('w:right')
        right.set(qn('w:val'), 'single'); right.set(qn('w:sz'), '28')
        right.set(qn('w:space'), '6'); right.set(qn('w:color'), bar)
        pBdr.append(right); pPr.append(pBdr)
        run = p.add_run(title + "  ")
        _set_run_font(run, size=11, bold=True, color=NAVY)
        run2 = p.add_run(text)
        _set_run_font(run2, size=10.5, color=MUTED)
        return p

    def table(self, headers, rows, col_widths=None, header_fill="0B2545"):
        """جدول با هدر تیره و ردیف‌های زبرا."""
        tbl = self.doc.add_table(rows=1, cols=len(headers))
        tbl.style = 'Table Grid'
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        # هدر
        hdr = tbl.rows[0].cells
        for i, h in enumerate(headers):
            cell = hdr[i]
            cell.text = ""
            p = cell.paragraphs[0]
            _set_para_rtl(p)
            _set_para_spacing(p, before=2, after=2, line=1.2)
            _add_shading(p, header_fill)
            run = p.add_run(h)
            _set_run_font(run, size=10.5, bold=True, color=WHITE)
            if col_widths:
                cell.width = Cm(col_widths[i])
        # ردیف‌ها
        for ri, row in enumerate(rows):
            cells = tbl.add_row().cells
            for ci, val in enumerate(row):
                cell = cells[ci]
                cell.text = ""
                p = cell.paragraphs[0]
                _set_para_rtl(p)
                _set_para_spacing(p, before=2, after=2, line=1.3)
                if ri % 2 == 0:
                    _add_shading(p, "F7FBFD")
                run = p.add_run(str(val))
                _set_run_font(run, size=10, color=INK)
                if col_widths:
                    cell.width = Cm(col_widths[ci])
        self.doc.add_paragraph().paragraph_format.space_after = Pt(4)
        return tbl

    def spacer(self, pts=8):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(pts)
        p.paragraph_format.space_before = Pt(0)
        return p

    def page_break(self):
        self.doc.add_page_break()

    def toc_field(self):
        """فهرست مطالب (TOC) — فیلد Word که در Word به‌روز می‌شود."""
        p = self.doc.add_paragraph()
        run = p.add_run()
        fldChar1 = OxmlElement('w:fldChar'); fldChar1.set(qn('w:fldCharType'), 'begin')
        instrText = OxmlElement('w:instrText'); instrText.set(qn('xml:space'), 'preserve')
        instrText.text = ' TOC \\o "1-3" \\h \\z \\u '
        fldChar2 = OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'), 'separate')
        t = OxmlElement('w:t'); t.text = "برای به‌روزرسانی فهرست، در Word راست‌کلیک و Update Field را بزنید."
        fldChar3 = OxmlElement('w:fldChar'); fldChar3.set(qn('w:fldCharType'), 'end')
        run._r.append(fldChar1); run._r.append(instrText); run._r.append(fldChar2)
        run._r.append(t); run._r.append(fldChar3)
        return p

    def cover_page(self, title, subtitle, meta_lines, presenter):
        """صفحه‌ی جلد."""
        # فضای بالا
        for _ in range(4):
            self.spacer(12)
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        _set_run_font(run, size=30, bold=True, color=NAVY)
        p2 = self.doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = p2.add_run(subtitle)
        _set_run_font(run2, size=16, bold=True, color=TEAL)
        self.spacer(10)
        # خط جداکننده
        p3 = self.doc.add_paragraph()
        p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run3 = p3.add_run("◆ ◆ ◆")
        _set_run_font(run3, size=12, color=MUTED)
        self.spacer(16)
        for ml in meta_lines:
            pm = self.doc.add_paragraph()
            pm.alignment = WD_ALIGN_PARAGRAPH.CENTER
            rm = pm.add_run(ml)
            _set_run_font(rm, size=12, color=MUTED)
            _set_para_spacing(pm, before=0, after=4, line=1.3)
        self.spacer(24)
        # ارائه‌دهنده
        pp = self.doc.add_paragraph()
        pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rp = pp.add_run(presenter)
        _set_run_font(rp, size=13, bold=True, color=NAVY2)
        self.page_break()

    def save(self, path):
        self.doc.save(path)
