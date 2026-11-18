from PIL import ImageFont, Image, ImageDraw
FD = "C:/Users/MamaDDelta/.gapcode/plugins/cache/gapgpt/presentations/26.722.10000/skills/presentations/assets/fonts"
img = Image.new("RGB", (10, 10)); dr = ImageDraw.Draw(img)
def wtext(text, fs, b):
    f = ImageFont.truetype(FD + ("/Vazirmatn-Bold.ttf" if b else "/Vazirmatn-Regular.ttf"), fs)
    bb = dr.textbbox((0, 0), text, font=f)
    return (bb[2]-bb[0]), (bb[3]-bb[1]), f.getlength(text)
for txt,fs in [("هربرت",40),("پدر",26),("رسانه پیام است",11),("چتر",10.5),("مک‌لوهان",11)]:
    bw,bh,gl = wtext(txt,fs,False)
    print(f"{txt!r:20} fs={fs:5} textbbox_w={bw:8.2f}px  getlength={gl:8.2f}px  (1in={72}px@72dpi)")
# raw pixel width for a full s28 f1 line
f=ImageFont.truetype(FD+"/Vazirmatn-Regular.ttf",9.5)
print("s28.f1 getlength(px):", f.getlength("ادورنو و هورکهایمر: «صنعت فرهنگ» — رسانه، ابزار کنترل ایدئولوژیک."))
print("3.35in at 96dpi =", 3.35*96, "px")
