import subprocess, sys, json, os
try:
    from pypdf import PdfReader
except Exception:
    sys.exit("need pypdf")
p="D:/pptx-build/mcluhan-makaleh.pdf"
r=PdfReader(p)
print("pages:",len(r.pages))
box=r.pages[0].mediabox
print("mediabox:",float(box.width),"x",float(box.height),"pts")
# check each of our 5 slides: slide index n -> page n-1 (1-based)
def check(n):
    pg=r.pages[n-1]
    t=pg.extract_text() or ""
    # count non-empty
    print(f"--- slide {n}: {len(t)} chars text ---")
    return t
for n in [1,3,16,28,30]:
    t=check(n)
    # print first 120 chars
    print(repr(t[:120]))
