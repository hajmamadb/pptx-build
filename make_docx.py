# -*- coding: utf-8 -*-
"""اجرای نهایی: ساخت سند DOCX."""
from docx_engine import PersianDoc
from content_front import build_front
from content_ch12 import ch1, ch2
from content_ch0102 import ch12, appendices
from content_ch34 import ch3, ch4
from content_ch56 import ch5, ch6
from content_ch78 import ch7, ch8
from content_ch910 import ch9, ch10
from content_ch11 import ch11

D = PersianDoc()

build_front(D)
ch1(D)
ch2(D)
ch3(D)
ch4(D)
ch5(D)
ch6(D)
ch7(D)
ch8(D)
ch9(D)
ch10(D)
ch11(D)
ch12(D)
appendices(D)

OUT = r"D:\1405 ترم سوم\دکتر بشیر\مک لوهان\مک‌لوهان-سند-پژوهشی.docx"
D.save(OUT)
print("Saved:", OUT)
