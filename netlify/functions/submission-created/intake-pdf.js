// Builds the "Your intake summary" PDF that is emailed back to the customer.
// It lays out the fields Netlify Forms received from the intake form, and turns the
// event-by-event summary text into one card per event.
const { PDFDocument, StandardFonts, rgb } = require("pdf-lib");

const MAROON = rgb(0.608, 0.11, 0.173);
const HALDI = rgb(0.89, 0.647, 0.078);
const LEAF = rgb(0.184, 0.42, 0.227);
const INK = rgb(0.165, 0.078, 0.094);
const MUTED = rgb(0.416, 0.333, 0.345);
const LINE = rgb(0.925, 0.886, 0.863);
const BLUSH = rgb(0.984, 0.965, 0.949);
const WHITE = rgb(1, 1, 1);

const PAGE_W = 612, PAGE_H = 792, MARGIN = 48;
const CONTACT = "V5 Events  ·  v5-events.com  ·  v5eventhub@gmail.com  ·  (425) 503-1212";

// The standard PDF fonts only cover Western European characters.
function clean(text) {
  return String(text ?? "")
    .replace(/\r/g, "")
    .replace(/→/g, "->").replace(/[✓✔]/g, "x")
    .replace(/[^\n\x20-\x7E -ÿ–—‘’“”•…€]/g, "?");
}

function wrap(text, font, size, width) {
  const lines = [];
  for (const para of clean(text).split("\n")) {
    let line = "";
    for (const word of para.split(/\s+/).filter(Boolean)) {
      const next = line ? line + " " + word : word;
      if (font.widthOfTextAtSize(next, size) <= width) { line = next; continue; }
      if (line) lines.push(line);
      line = word;
      while (font.widthOfTextAtSize(line, size) > width) {  // one very long word
        let cut = line.length - 1;
        while (cut > 1 && font.widthOfTextAtSize(line.slice(0, cut), size) > width) cut--;
        lines.push(line.slice(0, cut));
        line = line.slice(cut);
      }
    }
    lines.push(line);
  }
  return lines;
}

// Splits the intake summary text into the couple/contact header, event blocks,
// the accommodation block and the closing "DJ at / Priest at / Bar at / Notes" lines.
function parseSummary(summary) {
  const events = [], extras = [];
  let accommodation = null, current = null;
  for (const raw of clean(summary).split("\n")) {
    const line = raw.replace(/\s+$/, "");
    if (!line.trim()) { current = null; continue; }
    const ev = line.match(/^(\d+)\.\s+(.*)$/);
    if (ev) {
      const [name, date] = ev[2].split(/\s+—\s+/);
      current = { n: ev[1], name, date: date || "", rows: [] };
      events.push(current);
      continue;
    }
    if (/^Accommodation:/.test(line)) {
      accommodation = { head: line.replace(/^Accommodation:\s*/, ""), rows: [] };
      current = accommodation;
      continue;
    }
    if (/^\s{2,}\S/.test(line) && current) {
      const t = line.trim();
      if (current === accommodation) { const m = t.match(/^([^:]+):\s*(.*)$/); accommodation.rows.push(m ? [m[1], m[2]] : ["", t]); continue; }
      // "DJ: Yes · Priest: No" holds two fields on one line.
      for (const part of t.split(/\s+·\s+/)) {
        const m = part.match(/^([^:]+):\s*(.*)$/);
        current.rows.push(m ? [m[1], m[2]] : ["", part]);
      }
      continue;
    }
    if (/^(DJ at|Priest at|Bar at|Notes):/.test(line)) {
      const m = line.match(/^([^:]+):\s*(.*)$/);
      extras.push([m[1], m[2]]);
    }
  }
  return { events, accommodation, extras };
}

async function buildIntakePdf(data, { logoPng, submittedAt = new Date() } = {}) {
  const doc = await PDFDocument.create();
  doc.setTitle("V5 Events · Your intake summary");
  doc.setAuthor("V5 Events");
  const sans = await doc.embedFont(StandardFonts.Helvetica);
  const bold = await doc.embedFont(StandardFonts.HelveticaBold);
  const serif = await doc.embedFont(StandardFonts.TimesRomanBold);
  let logo = null;
  if (logoPng) { try { logo = await doc.embedPng(logoPng); } catch { logo = null; } }

  const contentW = PAGE_W - MARGIN * 2;
  let page, y;
  const pages = [];

  function newPage() {
    page = doc.addPage([PAGE_W, PAGE_H]);
    pages.push(page);
    y = PAGE_H - MARGIN;
  }
  function ensure(h) { if (y - h < MARGIN + 30) newPage(); }
  function text(t, x, yy, { font = sans, size = 10, color = INK } = {}) {
    page.drawText(clean(t), { x, y: yy, size, font, color });
  }
  function paragraph(t, x, width, { font = sans, size = 10, color = INK, lead = 1.4 } = {}) {
    for (const line of wrap(t, font, size, width)) {
      ensure(size * lead);
      text(line, x, y - size, { font, size, color });
      y -= size * lead;
    }
  }
  function heading(t) {
    ensure(40);
    y -= 14;
    text(t, MARGIN, y - 16, { font: serif, size: 16, color: MAROON });
    y -= 24;
    page.drawLine({ start: { x: MARGIN, y }, end: { x: PAGE_W - MARGIN, y }, thickness: 0.8, color: LINE });
    y -= 10;
  }
  function kvRows(rows, x, width, labelW = 120) {
    for (const [k, v] of rows) {
      const lines = wrap(v || "-", sans, 10, width - labelW);
      const h = lines.length * 14 + 6;
      ensure(h);
      text(k, x, y - 11, { font: bold, size: 9, color: MUTED });
      lines.forEach((l, i) => text(l, x + labelW, y - 11 - i * 14, { size: 10 }));
      y -= h;
      page.drawLine({ start: { x, y: y + 2 }, end: { x: x + width, y: y + 2 }, thickness: 0.5, color: LINE });
    }
  }

  // Header band.
  newPage();
  page.drawRectangle({ x: 0, y: PAGE_H - 104, width: PAGE_W, height: 104, color: MAROON });
  page.drawRectangle({ x: 0, y: PAGE_H - 110, width: PAGE_W, height: 6, color: HALDI });
  let tx = MARGIN;
  if (logo) { page.drawImage(logo, { x: MARGIN, y: PAGE_H - 88, width: 64, height: 64 }); tx = MARGIN + 78; }
  text("V5 Events", tx, PAGE_H - 52, { font: serif, size: 26, color: WHITE });
  text("YOUR CELEBRATION INTAKE SUMMARY", tx, PAGE_H - 72, { font: bold, size: 9, color: HALDI });
  const when = submittedAt.toLocaleString("en-US", { dateStyle: "long", timeStyle: "short", timeZone: "America/Los_Angeles" });
  const sub = "Submitted " + when + " (Pacific)";
  text(sub, PAGE_W - MARGIN - sans.widthOfTextAtSize(clean(sub), 9), PAGE_H - 72, { size: 9, color: WHITE });
  y = PAGE_H - 140;

  const name = data.contact || [data.bride, data.groom].filter(Boolean).join(" & ") || "Our client";
  paragraph(`Thank you, ${name}. This is a copy of the details you sent us through the intake form on v5-events.com. We'll use it to prepare your quote and agreement.`, MARGIN, contentW, { size: 10.5, color: MUTED });

  // Snapshot boxes.
  y -= 10;
  const boxes = [["EVENTS", data.event_count || "-"], ["TOTAL GUEST COVERS", data.total_guests || "-"], ["GUEST STAY", data.accommodation || "No"]];
  const bw = (contentW - 20) / 3;
  ensure(62);
  boxes.forEach(([k, v], i) => {
    const bx = MARGIN + i * (bw + 10);
    page.drawRectangle({ x: bx, y: y - 56, width: bw, height: 56, color: BLUSH, borderColor: LINE, borderWidth: 0.8 });
    const val = wrap(v, serif, 18, bw - 24)[0];
    text(val, bx + 12, y - 28, { font: serif, size: 18, color: MAROON });
    text(k, bx + 12, y - 45, { font: bold, size: 7.5, color: MUTED });
  });
  y -= 66;

  heading("Your details");
  const details = [["Contact", data.contact], ["Bride", data.bride], ["Groom", data.groom], ["Phone / WhatsApp", data.phone], ["Email", data.email], ["City / venue", data.venue]]
    .filter(([, v]) => v && String(v).trim());
  kvRows(details, MARGIN, contentW);

  const parsed = parseSummary(data.summary || "");
  heading(`Your events${data.events ? "  ·  " + clean(data.events) : ""}`);
  if (!parsed.events.length) paragraph("No event details were included.", MARGIN, contentW, { color: MUTED });
  for (const ev of parsed.events) {
    const rows = ev.rows.length ? ev.rows : [["", "No details given"]];
    const est = 30 + rows.reduce((h, [, v]) => h + wrap(v || "-", sans, 10, contentW - 140).length * 14 + 6, 0);
    ensure(Math.min(est, 260));
    page.drawRectangle({ x: MARGIN, y: y - 24, width: contentW, height: 24, color: BLUSH });
    page.drawRectangle({ x: MARGIN, y: y - 24, width: 4, height: 24, color: MAROON });
    text(`${ev.n}.  ${ev.name}`, MARGIN + 14, y - 16, { font: bold, size: 11 });
    if (ev.date) text(ev.date, PAGE_W - MARGIN - 10 - bold.widthOfTextAtSize(clean(ev.date), 9.5), y - 16, { font: bold, size: 9.5, color: MAROON });
    y -= 30;
    kvRows(rows, MARGIN + 14, contentW - 14);
    y -= 10;
  }

  if (parsed.accommodation) {
    heading("Guest accommodation");
    kvRows([["Guests and rooms", parsed.accommodation.head.replace(/^needed for\s*/i, "")], ...parsed.accommodation.rows], MARGIN, contentW);
  }
  if (parsed.extras.length) {
    heading("At a glance");
    kvRows(parsed.extras, MARGIN, contentW);
  }
  if (data.notes && !parsed.extras.some(([k]) => k === "Notes")) {
    heading("Notes");
    paragraph(data.notes, MARGIN, contentW);
  }

  heading("Service terms");
  paragraph(`Accepted: ${data.terms || "Yes"}. Our service terms are attached to this email as a separate PDF. Each service needs at least 30 days' notice (60 days for guest accommodation), and a non-refundable 30% deposit confirms your booking. If your plans change, please submit a new intake form with your updated details.`, MARGIN, contentW, { size: 10, color: MUTED });

  // Footer on every page.
  pages.forEach((p, i) => {
    p.drawLine({ start: { x: MARGIN, y: 40 }, end: { x: PAGE_W - MARGIN, y: 40 }, thickness: 0.6, color: LINE });
    p.drawText(clean(CONTACT), { x: MARGIN, y: 26, size: 8, font: sans, color: MUTED });
    const pn = `Page ${i + 1} of ${pages.length}`;
    p.drawText(pn, { x: PAGE_W - MARGIN - sans.widthOfTextAtSize(pn, 8), y: 26, size: 8, font: sans, color: MUTED });
  });

  return Buffer.from(await doc.save());
}

module.exports = { buildIntakePdf, parseSummary };
