const fs = require("fs");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "محمد بختیاری";
pres.title = "مارشال مک‌لوهان؛ پدر رسانه‌شناسی معاصر";

const W = 13.33, H = 7.5, ML = 0.7, CW = 11.93;

/* ---------- پالت (دقیق از فایل HTML) ---------- */
const C = {
  navy: "0B2545", navy2: "123A63", navy3: "1D4E7D",
  teal: "0F9C96", teal2: "17B3AD", tealSoft: "E4F4F3",
  orange: "EF8B1F", orangeSoft: "FFF6EC",
  bg: "F4F8FB", card: "FFFFFF", ink: "0F2038",
  muted: "5B6B80", line: "DBE5EF", white: "FFFFFF",
};
const FONT = "Vazirmatn";
const FA = n => String(n).replace(/\d/g, d => "۰۱۲۳۴۵۶۷۸۹"[+d]);
const sh = (o = {}) => Object.assign({ type: "outer", color: "0B2545", blur: 16, offset: 5, angle: 90, opacity: 0.10 }, o);

/* ---------- صف انیمیشن: همهٔ شکل‌ها/متن‌ها به‌نوبت با تأخیر پلکانی ---------- */
function A(slide, kind, shape, o) { slide._tl = slide._tl || []; slide._tl.push({ kind, shape, o }); }
function flushTl(slide) {
  if (!slide._tl) return;
  let d = 0;
  for (const it of slide._tl) {
    const o = Object.assign({}, it.o);
    const base = o._delay || 0;
    delete o._delay;
    o.delay = Math.round((d + base) * 1000);
    try {
      if (it.kind === "s") slide.addShape(it.shape, o);
      else if (it.kind === "t") slide.addText(o.text, o);
      else if (it.kind === "tbl") slide.addTable(it.data, o);
      else if (it.kind === "img") slide.addImage(o);
    } catch (e) { console.error("tl err:", e.message); }
    d += 0.08;
  }
  slide._tl = [];
}
function S(slide, shape, o) { try { slide.addShape(shape, o); } catch (e) {} }
function T(slide, text, o) { try { slide.addText(text, o); } catch (e) {} }

/* ---------- متن فارسی (انیمیت‌شده) ---------- */
function fa(slide, text, o) {
  const oo = Object.assign({ fontFace: FONT, rtlMode: true, bidi: true }, o);
  if (oo.align === undefined) oo.align = "right";
  A(slide, "t", null, oo);
}
/* متن ساده بدون انیمیشن */
function faPlain(slide, text, o) {
  const oo = Object.assign({ fontFace: FONT, rtlMode: true, bidi: true }, o);
  if (oo.align === undefined) oo.align = "right";
  T(slide, text, oo);
}

/* ---------- هدر: بج + تیتر + خط تأکید گرادیانی ---------- */
function header(slide, badge, title) {
  const badgeW = 0.6 + badge.length * 0.145;
  A(slide, "s", pres.shapes.ROUNDED_RECTANGLE, { x: W - ML - badgeW, y: 0.44, w: badgeW, h: 0.42, rectRadius: 0.21, fill: { color: C.tealSoft }, line: { type: "none" }, _delay: 0 });
  A(slide, "s", pres.shapes.OVAL, { x: W - ML - 0.2, y: 0.57, w: 0.15, h: 0.15, fill: { color: C.teal2 }, line: { type: "none" }, _delay: 0.02 });
  A(slide, "t", null, { x: W - ML - badgeW + 0.24, y: 0.44, w: badgeW - 0.3, h: 0.42, text: badge, fontSize: 11, bold: true, color: "0B6B68", align: "center", valign: "middle", _delay: 0.04 });
  const tw = Math.min(11.6, 0.6 + title.length * 0.29);
  A(slide, "t", null, { x: W - ML - tw, y: 0.94, w: tw, h: 0.58, text: title, fontSize: 25, bold: true, color: C.navy, align: "right", valign: "top", _delay: 0.1 });
  const segs = 20, lw = 0.8 / segs;
  for (let i = 0; i < segs; i++)
    S(slide, pres.shapes.RECTANGLE, { x: W - ML - (i + 1) * lw, y: 1.58, w: lw + 0.005, h: 0.05, fill: { color: i < 10 ? C.teal2 : C.navy }, line: { type: "none" } });
}

/* ---------- کارت ---------- */
function card(slide, x, y, w, h, v = {}) {
  let fill = C.card, lc = C.line, lw = 1;
  if (v.navy) { fill = C.navy; lc = C.navy; lw = 0; }
  else if (v.tint) { fill = "F4FBFA"; lc = "CDECEB"; }
  else if (v.orange) { fill = C.orangeSoft; lc = "F7E0C3"; }
  else if (v.flat) lw = 0;
  A(slide, "s", pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: v.r || 0.14, fill: { color: fill }, line: lw ? { color: lc, width: lw } : { type: "none" }, shadow: v.flat ? { type: "none" } : sh(), _delay: v._delay || 0 });
}
function cardTitle(slide, x, y, w, txt, dark, size) {
  A(slide, "t", null, { x: x + 0.22, y: y + 0.14, w: w - 0.44, h: 0.4, text: txt, fontSize: size || 15, bold: true, color: dark ? C.white : C.navy, align: "right", valign: "top", _delay: 0.08 });
}
function cardBody(slide, x, y, w, h, txt, dark, size, top) {
  const t = top !== undefined ? top : 0.56;
  A(slide, "t", null, { x: x + 0.22, y: y + t, w: w - 0.44, h: h - t - 0.16, text: txt, fontSize: size || 12, color: dark ? "EAF2F9" : C.muted, align: "right", valign: "top", lineSpacingMultiple: 1.26, _delay: 0.14 });
}

/* ---------- warnbox / prompt ---------- */
function warnbox(slide, x, y, w, h, label, txt, size) {
  A(slide, "s", pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.11, fill: { color: C.orangeSoft }, line: { color: "F8D9B4", width: 1 }, _delay: 0.24 });
  A(slide, "s", pres.shapes.RECTANGLE, { x: x + w - 0.08, y: y + 0.12, w: 0.05, h: h - 0.24, fill: { color: C.orange }, line: { type: "none" }, _delay: 0.24 });
  A(slide, "t", null, { x: x + 0.2, y: y + 0.1, w: w - 0.5, h: h - 0.2, text: [{ text: (label || "") + " ", options: { bold: true, color: "6A3C05" } }, { text: txt, options: { color: "7D4708" } }], fontSize: size || 11, valign: "top", lineSpacingMultiple: 1.22, _delay: 0.28 });
}
function promptBox(slide, x, y, w, h, k, txt, size) {
  A(slide, "s", pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.11, fill: { color: "F1F8FA" }, line: { type: "none" }, _delay: 0.1 });
  A(slide, "s", pres.shapes.RECTANGLE, { x: x + w - 0.08, y: y + 0.12, w: 0.05, h: h - 0.24, fill: { color: C.teal2 }, line: { type: "none" }, _delay: 0.1 });
  A(slide, "t", null, { x: x + 0.2, y: y + 0.08, w: w - 0.45, h: 0.28, text: k, fontSize: 10, bold: true, color: C.teal, align: "right", valign: "top", _delay: 0.14 });
  A(slide, "t", null, { x: x + 0.2, y: y + 0.36, w: w - 0.45, h: h - 0.5, text: txt, fontSize: size || 11.5, color: C.navy2, align: "right", valign: "top", lineSpacingMultiple: 1.28, _delay: 0.18 });
}

/* ---------- نوار نقل‌قول ---------- */
function quoteBand(slide, x, y, w, h, quoteRuns, cite, qSize) {
  A(slide, "s", pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.14, fill: { color: C.navy }, line: { type: "none" }, shadow: sh({ blur: 22, offset: 8, opacity: 0.26 }), _delay: 0.08 });
  A(slide, "s", pres.shapes.OVAL, { x: x + 0.1, y: y - 0.25, w: 2.1, h: 2.1, fill: { color: C.teal2, transparency: 84 }, line: { type: "none" }, _delay: 0.12 });
  const q = [{ text: "\u201C", options: { color: C.teal2, fontSize: (qSize || 16) * 1.3, bold: true } }];
  for (const r of quoteRuns) q.push(r);
  q.push({ text: "\u201D", options: { color: C.teal2, fontSize: (qSize || 16) * 1.3, bold: true } });
  A(slide, "t", null, { x: x + 0.4, y: y + 0.2, w: w - 0.8, h: h - 0.72, text: q, fontSize: qSize || 16, bold: true, color: C.white, align: "right", valign: "middle", lineSpacingMultiple: 1.25, _delay: 0.18 });
  A(slide, "t", null, { x: x + 0.4, y: y + h - 0.52, w: w - 0.8, h: 0.36, text: cite, fontSize: 10, color: "A9C6DD", align: "right", valign: "bottom", _delay: 0.26 });
}

/* ---------- جدول ---------- */
function htmlTable(slide, x, y, w, colW, rows, opts = {}) {
  const data = rows.map((r, ri) => r.map(cell => {
    const o = { fontSize: opts.fs || 10.5, color: C.ink, fontFace: FONT, align: "right", valign: "middle", rtlMode: true, bidi: true, margin: [0.03, 0.09, 0.03, 0.09] };
    if (ri === 0) { o.fill = { color: C.navy }; o.color = C.white; o.bold = true; }
    else if (ri % 2 === 0) o.fill = { color: "F7FBFD" };
    if (cell && typeof cell === "object") {
      o.text = cell.t;
      if (cell.b) o.bold = true;
      if (cell.c) o.color = cell.c;
      if (cell.ltr) { o.align = "left"; o.rtlMode = false; o.bidi = false; }
      if (cell.fill) o.fill = { color: cell.fill };
    } else o.text = cell;
    return { text: o.text, options: o };
  }));
  const o = { x, y, w, colW, rowH: opts.rowH || 0.33, border: { type: "solid", pt: 0.5, color: C.line }, fontFace: FONT, rtlMode: true, bidi: true };
  A(slide, "tbl", null, Object.assign(o, { _delay: opts._delay || 0.15 }));
  slide._tl[slide._tl.length - 1].data = data;
}

/* ---------- لیست نقطه‌ای ---------- */
function bulletList(slide, x, y, w, h, items, o = {}) {
  const runs = [];
  items.forEach((it, i) => {
    runs.push({ text: "\u25AA ", options: { color: o.dotColor || C.teal2, fontSize: (o.fs || 11.5) * 0.85 } });
    runs.push({ text: it, options: { breakLine: i < items.length - 1, color: o.color || C.ink } });
  });
  A(slide, "t", null, { x, y, w, h, text: runs, fontSize: o.fs || 11.5, valign: "top", lineSpacingMultiple: 1.3, paraSpaceAfter: 6, _delay: o._delay || 0.12 });
}

/* ---------- لیست شماره‌دار ---------- */
function numList(slide, x, y, w, items, o = {}) {
  const gap = o.gap || 1.05;
  items.forEach((it, i) => {
    const ly = y + i * gap;
    A(slide, "s", pres.shapes.ROUNDED_RECTANGLE, { x: x + w - 0.42, y: ly + 0.04, w: 0.42, h: 0.42, rectRadius: 0.11, fill: { color: C.tealSoft }, line: { color: "C9A55C", width: 0.75 }, _delay: 0.08 + i * 0.1 });
    A(slide, "t", null, { x: x + w - 0.42, y: ly + 0.04, w: 0.42, h: 0.42, text: FA(i + 1), fontSize: 12.5, bold: true, color: "0B6B68", align: "center", valign: "middle", _delay: 0.1 + i * 0.1 });
    A(slide, "t", null, { x: x, y: ly, w: w - 0.6, h: gap - 0.08, text: it, fontSize: o.fs || 11.5, color: o.color || C.ink, align: "right", valign: "top", lineSpacingMultiple: 1.25, _delay: 0.12 + i * 0.1 });
  });
}

/* ---------- نودهای flow ---------- */
function flowNodes(slide, x, y, w, nodes, gap) {
  const n = nodes.length, nw = (w - gap * (n - 1)) / n;
  nodes.forEach((nd, i) => {
    const nx = x + w - (i + 1) * nw - i * gap; // از راست به چپ
    A(slide, "s", pres.shapes.ROUNDED_RECTANGLE, { x: nx, y, w: nw, h: 0.52, rectRadius: 0.1, fill: { color: nd.hot ? C.teal : C.card }, line: { color: nd.hot ? C.teal : C.line, width: 1 }, shadow: nd.hot ? { type: "none" } : sh({ blur: 8, offset: 2, opacity: 0.07 }), _delay: 0.1 + i * 0.08 });
    A(slide, "t", null, { x: nx, y, w: nw, h: 0.52, text: nd.t, fontSize: nd.fs || 11.5, bold: true, color: nd.hot ? C.white : C.navy, align: "center", valign: "middle", _delay: 0.12 + i * 0.08 });
    if (i < n - 1) A(slide, "t", null, { x: nx - gap, y, w: gap, h: 0.52, text: "\u2190", fontSize: 13, bold: true, color: C.teal, align: "center", valign: "middle", _delay: 0.1 + i * 0.08 });
  });
}

/* ---------- چیپ ---------- */
function chip(slide, x, y, w, h, txt, v = {}) {
  A(slide, "s", pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: h / 2, fill: { color: v.solid ? (v.dark ? C.teal2 : C.navy) : C.card }, line: v.solid ? { type: "none" } : { color: v.lc || C.line, width: 1 }, _delay: v._delay || 0 });
  A(slide, "t", null, { x, y, w, h, text: txt, fontSize: v.fs || 11, bold: !!v.solid, color: v.solid ? (v.dark ? "04211F" : C.white) : (v.c || C.navy), align: "center", valign: "middle", _delay: (v._delay || 0) + 0.02 });
}

/* ---------- صفحه‌ی جدید + شماره ---------- */
function newSlide(idx, notes) {
  const s = pres.addSlide();
  s.background = { color: idx % 2 === 0 ? "F7FBFD" : C.white };
  if (notes) s.addNotes(notes);
  faPlain(s, FA(idx) + " / " + FA(30), { x: 0.35, y: 7.14, w: 0.9, h: 0.28, fontSize: 9.5, color: C.muted, align: "left", valign: "middle" });
  return s;
}

module.exports = { pres, C, W, H, ML, CW, FONT, FA, sh, A, S, T, fa, faPlain, header, card, cardTitle, cardBody, warnbox, promptBox, quoteBand, htmlTable, bulletList, numList, flowNodes, chip, newSlide, flushTl };
