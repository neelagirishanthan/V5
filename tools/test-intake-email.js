// Local check of the thank-you email: serves site/ on a local port, runs the function's
// email builder on a sample submission and writes the email and its PDFs to an output folder.
// Usage: node tools/test-intake-email.js [output-dir]   (sends nothing)
const http = require("http"), fs = require("fs"), path = require("path");
const nodemailer = require("nodemailer");
const fn = require("../netlify/functions/submission-created/submission-created.js");

const root = path.join(__dirname, "..", "site");
const out = path.resolve(process.argv[2] || "intake-email-test");
fs.mkdirSync(out, { recursive: true });

const summary = `V5 EVENTS · CELEBRATION INTAKE
Couple: Sample Bride & Sample Groom
Contact: Sample Contact
Phone / email: (000) 000-0000 · sample@example.com
City / venue: Bellevue, WA
Number of events: 2

1. Haldi — 2027-02-12
   People: 120
   Decor: Floral decor, Garlands, Backdrop / theme (yellow and marigold)
   Food: Veg only
   Live counters: Dosa, Chaat & pani puri
   Alcohol / bartender: No
   DJ: No · Priest: No
   Photography: Photos, Candid
2. Pelli & Reception — 2027-02-14
   People: 300
   Decor: Stage / mandapam, Entrance arch, Floral decor, Lighting, Seating & tables
   Food: Veg + non-veg (veg 180, non-veg 120)
   Live counters: Biryani, Ice cream & paan
   Alcohol / bartender: Yes — Beer & wine
   DJ: Yes · Priest: Yes
   Photography: Photos, Video, Drone

Accommodation: needed for 25 guests, 10 rooms
   Stay: 2027-02-11 to 2027-02-15
   Notes: Two elders need ground-floor rooms

DJ at: Pelli & Reception
Priest at: Pelli & Reception
Bar at: Pelli & Reception

Notes: Sample notes for testing only.`;

const data = {
  bride: "Sample Bride", groom: "Sample Groom", contact: "Sample Contact", phone: "(000) 000-0000", email: "sample@example.com",
  venue: "Bellevue, WA", event_count: "2", events: "Haldi, Pelli & Reception", total_guests: "420",
  accommodation: "Yes, 25 guests", notes: "Sample notes for testing only.", summary,
  terms: "Read and accepted on 11/7/2026, 10:00:00 AM",
};

const server = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(req.url.split("?")[0]));
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.end(fs.readFileSync(p));
}).listen(0, async () => {
  const site = `http://localhost:${server.address().port}`;
  try {
    // Without Gmail settings the handler must do nothing.
    delete process.env.GMAIL_USER; delete process.env.GMAIL_APP_PASSWORD;
    const skipped = await fn.handler({ body: JSON.stringify({ payload: { form_name: "intake", data } }) });
    console.log("handler without Gmail settings:", skipped.body);

    const mail = await fn.prepare(data, { site, submittedAt: new Date("2026-11-07T18:00:00Z") });
    fs.writeFileSync(path.join(out, "email.html"), mail.html);
    fs.writeFileSync(path.join(out, "email.txt"), mail.text);
    for (const a of mail.attachments) fs.writeFileSync(path.join(out, a.filename), a.content);
    const msg = await nodemailer.createTransport({ streamTransport: true, buffer: true })
      .sendMail({ from: { name: "V5 Events", address: "v5eventhub@gmail.com" }, to: data.email, bcc: "v5eventhub@gmail.com", ...mail });
    fs.writeFileSync(path.join(out, "message.eml"), msg.message);
    console.log("subject:", mail.subject);
    console.log("attachments:", mail.attachments.map((a) => `${a.filename} (${a.content.length} bytes)`).join(", "));
    console.log("written to", out);
  } finally {
    server.close();
  }
});
