from PIL import ImageFont, Image, ImageDraw
FD = "C:/Users/MamaDDelta/.gapcode/plugins/cache/gapgpt/presentations/26.722.10000/skills/presentations/assets/fonts"
img = Image.new("RGB", (10, 10)); dr = ImageDraw.Draw(img)
PPIN = 96.0  # PIL text is in physical pixels; ~96 px per inch
def fnt(fs,b): return ImageFont.truetype(FD+("/Vazirmatn-Bold.ttf" if b else "/Vazirmatn-Regular.ttf"), fs)
def width_in(text, fs, b):  # width in INCHES
    return fnt(fs,b).getlength(text)/PPIN
def wrap_count(text, fs, b, availW_in):
    full = width_in(text, fs, b)
    if full <= availW_in: return 1
    words = text.split(); cur=""; n=0
    for wd in words:
        t = cur+" "+wd if cur else wd
        if width_in(t,fs,b) > availW_in and cur:
            n+=1; cur=wd
        else: cur=t
    return n+1
def need_h(n, fs, lsm, leading=1.2):  # inches
    return n*(fs/72.0)*lsm*leading
def chk(label, fs, b, availW_in, availH_in, text, lsm=1.25):
    n = wrap_count(text, fs, b, availW_in)
    need = need_h(n, fs, lsm)
    flag = "OVERFLOW" if need>availH_in*1.04 else ("TIGHT" if need>availH_in*0.9 else "OK")
    print(f"[{flag:9}] {label}: fs={fs} lines={n} need~{need:.2f}in / box {availH_in}in (w={availW_in})")

print("==== S16 ====")
chk("s16.prompt",11.5,False,11.48,0.55,"هر فناوری، گسترشی از یکی از حواس یا اندام‌های انسان است. چتر، گسترش پوست است؛ عینک، گسترش چشم؛ رادیو، گسترش گوش؛ تلویزیون، گسترش سیستم عصبی مرکزی.",1.28)
chk("s16.warnbox",10.5,False,11.43,1.05,"نتیجه‌ی عمیق: وقتی یک حس را «بیرون» می‌کنیم، توازن حواس به‌هم می‌خورد. چاپ، چشم را بزرگ کرد و گوش/لمس/سایر حواس را کوچک کرد — این «تخصص‌گرایی حسی» است. فناوری‌های الکترونیکی، این توازن را بازمی‌گردانند — و ما را به «حس‌های چندگانهٔ هم‌زمان» برمی‌گردانند.",1.22)
for lbl,it in [("s16.col_navy",["رادیو ← حلقه‌ی عصبی","تلویزیون ← مغز الکترونیکی","اینترنت ← مغز بیرونی (noosphere)","هوش مصنوعی ← تفکر بیرونی"]),
               ("s16.col_mid",["چتر ← پوست","کفش ← پا","ماشین ← پاهای بلندتر","موشک ← بدن پرتابی"]),
               ("s16.col_tint",["عینک ← چشم","هدفون ← گوش","فونت ← صدا (تصویر صدا)","کتاب ← حافظه"])]:
    tot=0
    for b in it:
        n=wrap_count(b,10.5,False,3.35)
        tot+= n*(10.5/72.0)*1.3*1.2 + 6/72.0
    print(f"  {lbl}: bullets need~{tot:.2f}in / 1.7in -> {'OK' if tot<=1.74 else 'OVERFLOW'}")

print("==== S3 numlist (availW=5.33, slot 0.92) ====")
for lbl,t in [("s3.i1","هربرت مارشال مک‌لوهان — اندیشمند کانادایی که در ادمونتون (آلبرتا) متولد شد، در وینیپگ (مانیتوبا) بزرگ شد و ۳۴ سال استاد دانشگاه تورنتو بود."),
              ("s3.i2","ادیب، معلم و نظریه‌پرداز ارتباطات — بیش از آن که رسانه‌شناس باشد، نقاد ادبی بود که به فناوری سرگشت."),
              ("s3.i3","بنیان‌گذار «مرکز مطالعات رسانه‌ای» در دانشگاه تورنتو — جایی که مطالعات رسانه از یک صندلیِ تدریس به یک حوزهٔ مستقل پژوهش رسید."),
              ("s3.i4","شهرت جهانی در دههٔ ۱۹۶۰؛ برندهٔ نشان کانادا (Order of Canada, 1970) — «شاید تنها نظریه‌پرداز رسانه‌ای که چهرهٔ مشهور شد»؛ در فیلم آنی‌هال (1977) وودی آلن، نقش خودش را بازی کرد.")]:
    n=wrap_count(t,11,False,5.33); need=need_h(n,11,1.25)
    print(f"  {lbl}: lines={n} need~{need:.2f}in / slot 0.92in -> {'TIGHT' if need>0.94 else 'OK'}")
print(f"  s3.caption: {width_in('مارشال مک‌لوهان در سال ۱۹۶۷؛ اوج شهرت جهانی',9.5,False):.2f}in / 3.3in")

print("==== S28 ====")
for lbl,t in [("s28.f1","ادورنو و هورکهایمر: «صنعت فرهنگ» — رسانه، ابزار کنترل ایدئولوژیک. مک‌لوهان: رسانه، بازطرح‌کردنِ ساختارِ حس است — نه محتوا، نه ایدئولوژی."),
              ("s28.f2","کاستلز شهودِ «دهکدهٔ جهانی» را گرفت و تحلیلِ شبکه را ساخت: نه دهکده، «شبکهٔ جهانی» — با گره‌ها، جریان‌ها و دسترسی."),
              ("s28.f3","«مک‌لوهانِ فرانسوی» — شباهت ظاهری در توصیفِ عصر نشانه، اما مخالفتِ عمیق: رسانه تصویرِ شفاف نمی‌دهد؛ «پیام، رسانه است».")]:
    n=wrap_count(t,9.5,False,3.35); need=need_h(n,9.5,1.25)
    print(f"  {lbl}: lines={n} need~{need:.2f}in / 1.3in -> {'OVERFLOW' if need>1.36 else 'OK'}")
for lbl,t in [("s28.up1","سوگیری ارتباط — امپراتوری‌ها با سوگیریِ زمان/فاصله می‌افتند"),
              ("s28.up2","شفاهیت ← کتابت ← الکترونیک"),
              ("s28.up3","نقد نو (کمبریج) — خوانش نزدیک ← تحلیل الگو"),
              ("s28.dn1","بوم‌شناسی رسانه‌ای — Laws of Media (1990)"),
              ("s28.dn2","وارث و منتقد — Amusing Ourselves to Death (1985)"),
              ("s28.dn3","No Sense of Place (1985) — نقش‌های اجتماعی")]:
    n=wrap_count(t,8,False,3.35); need=need_h(n,8,1.15)
    print(f"  {lbl}: lines={n} need~{need:.2f}in / 0.36in -> {'OVERFLOW' if need>0.40 else 'TIGHT' if need>0.36 else 'OK'}")
chk("s28.bar",13,True,4.6,0.6,"مارشال مک‌لوهان  1911–1980 — رسانه پیام است / دهکده جهانی / گرم و سود",1.2)

print("==== S30 ====")
chk("s30.quote",19,True,11.93,0.7,"مک‌لوهان، «پیش‌گو» نبود؛ او «آینه» بود. آینه‌ای که فناوری‌های ما را — از تلویزیون تا هوش مصنوعی — به ما نشان می‌داد.",1.3)
chk("s30.navy",11,False,5.59,1.54,"هر فناوری، گسترشی از ما است. قبل از آن که یک فناوری «استفاده» کنیم، باید بفهمیم کدام حسی را گسترش می‌دهد — و کدام توازن حسی را به‌هم می‌زند. این، «سواد رسانه‌ای» به‌معنای عمیق آن است.",1.26)
chk("s30.tint",11,False,5.59,1.54,"آیا «رسانه پیام است» هنوز درست است؟ آیا «دهکده جهانی» ساخت، یا شکست؟ آیا هوش مصنوعی، «گسترش جدید» است یا «تغییر ماهیت»؟",1.26)
chk("s30.footer",10,False,11.93,0.35,"ارائه: محمد بختیاری | درس: سواد رسانه‌ای و فضای مجازی | منابع کامل: اسلاید ۲۹ | Music: CBC Explorations / Ubuweb — CC BY-SA 4.0",1.2)

print("==== S1 ====")
for lbl,fs,b,aw,ah,t in [("s1.title",40,True,11.93,0.78,"هربرت مارشال مک‌لوهان"),
                       ("s1.subtitle",26,True,11.93,0.6,"پدر رسانه‌شناسی معاصر"),
                       ("s1.tagline",14,False,11.93,0.45,"یک سفر کامل: زندگی، نظریه‌ها، کتاب‌ها، منتقدان و میراثی که هنوز ما را شکل می‌دهد"),
                       ("s1.pres1",14.5,True,4.5,0.4,"ارائه‌دهنده: محمد بختیاری")]:
    n=wrap_count(t,fs,b,aw); need=need_h(n,fs,1.2)
    print(f"  {lbl}: lines={n} need~{need:.2f}in / {ah}in -> {'OVERFLOW' if need>ah*1.08 else 'OK'}")
for lbl,t,ww in [("s1.meta1","۲۱ ژوئیه ۱۹۱۱ · ۳۱ دسامبر ۱۹۸۰",2.6),("s1.meta3","مرکز مطالعات رسانه‌ای",2.3),("s1.meta4","درس: سواد رسانه‌ای و فضای مجازی",3.2),
                 ("s1.ch1","رسانه پیام است",1.75),("s1.ch2","دهکده جهانی",1.4),("s1.ch3","رسانه‌های گرم و سرد",2.0),("s1.ch4","گوتنبرگ‌گالاکسی",1.9),("s1.ch5","گسترش‌های بدن",1.6)]:
    wid=width_in(t,11,False); flag='OVERFLOW' if wid>ww*0.92 else 'OK'
    print(f"  {lbl}: text~{wid:.2f}in / {ww}in -> {flag}")
