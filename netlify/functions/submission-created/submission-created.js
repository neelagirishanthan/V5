// Runs on Netlify every time a form submission is verified (Netlify's "submission-created"
// event). For the intake form it emails the customer a thank-you from the V5 Events Gmail
// account, with their intake summary as a PDF and the service terms PDF attached, and a
// copy to V5.
//
// Needs two environment variables in Netlify (Project configuration > Environment variables):
//   GMAIL_USER          v5eventhub@gmail.com
//   GMAIL_APP_PASSWORD  a Google app password for that account (not the normal password)
// Without them it does nothing, and submissions are still saved in Netlify as usual.
const nodemailer = require("nodemailer");
const { buildIntakePdf } = require("./intake-pdf");

const BUSINESS_EMAIL = "v5eventhub@gmail.com";
const PHONE = "(425) 503-1212";

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const validEmail = (s) => /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(String(s || "").trim());

async function fetchBytes(url) {
  try {
    const res = await fetch(url, { signal: AbortSignal.timeout(4000) });
    return res.ok ? Buffer.from(await res.arrayBuffer()) : null;
  } catch {
    return null;
  }
}

function customerName(d) {
  if (d.contact && d.contact.trim()) return d.contact.trim();
  const couple = [d.bride, d.groom].filter((x) => x && x.trim()).join(" & ");
  return couple || "there";
}

function buildEmail(d, site) {
  const name = customerName(d);
  const first = name === "there" ? "there" : name.split(/[\s&]+/)[0];
  const rows = [["Events", d.events || "-"], ["Total guest covers", d.total_guests || "-"], ["Guest stay", d.accommodation || "No"], ["City / venue", d.venue || "-"]];
  const subject = `Thank you, ${name === "there" ? "we've received your intake" : name + ": we've received your intake"} · V5 Events`;

  const html = `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body style="margin:0;background:#f6efe9;font-family:Helvetica,Arial,sans-serif;color:#2a1418">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f6efe9;padding:24px 12px"><tr><td align="center">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:10px;overflow:hidden">
<tr><td style="background:#9b1c2c;padding:28px 32px">
  <div style="font-family:Georgia,'Times New Roman',serif;font-size:28px;color:#ffffff">V5 Events</div>
  <div style="font-size:11px;letter-spacing:2px;color:#f2c14e;margin-top:6px;font-weight:bold">WEDDINGS · BIRTHDAYS · CORPORATE EVENTS · SEATTLE</div>
</td></tr>
<tr><td style="height:5px;background:#e3a514;font-size:0;line-height:0">&nbsp;</td></tr>
<tr><td style="padding:30px 32px 8px">
  <h1 style="font-family:Georgia,'Times New Roman',serif;font-weight:normal;font-size:26px;margin:0 0 14px">Thank you, ${esc(first)}.</h1>
  <p style="font-size:15px;line-height:1.6;margin:0 0 14px">We've received your intake form and we're excited to start planning your celebration with you.</p>
  <p style="font-size:15px;line-height:1.6;margin:0 0 18px">For your records, we've attached two PDFs:</p>
  <ul style="font-size:15px;line-height:1.7;margin:0 0 22px;padding-left:20px">
    <li><b>Your intake summary</b>: everything you sent us, event by event.</li>
    <li><b>Our service terms</b>: what we deliver for each service and what we ask of you.</li>
  </ul>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#fbf6f2;border-radius:8px;margin:0 0 24px">
    ${rows.map(([k, v]) => `<tr><td style="padding:10px 16px;font-size:12px;color:#6a5558;font-weight:bold;width:40%;border-bottom:1px solid #ece2dc">${esc(k)}</td><td style="padding:10px 16px;font-size:14px;border-bottom:1px solid #ece2dc">${esc(v)}</td></tr>`).join("")}
  </table>
  <h2 style="font-family:Georgia,'Times New Roman',serif;font-weight:normal;font-size:20px;margin:0 0 10px;color:#9b1c2c">What happens next</h2>
  <ol style="font-size:15px;line-height:1.7;margin:0 0 22px;padding-left:20px">
    <li>We review your details and may call you with a few questions.</li>
    <li>We send you a clear quote and your event agreement.</li>
    <li>A non-refundable 30% deposit, due within 24 hours of booking, confirms your dates.</li>
  </ol>
  <p style="font-size:14px;line-height:1.6;margin:0 0 22px;background:#fffaf3;border-left:3px solid #9b1c2c;padding:12px 14px">
    <b>Need to change something?</b> Please submit a new intake form at <a href="${esc(site)}/intake/" style="color:#9b1c2c">v5-events.com/intake</a> with your updated details, and we'll work from the latest one.
  </p>
  <p style="font-size:15px;line-height:1.6;margin:0 0 26px">Questions in the meantime? Call or WhatsApp us on <a href="tel:+14255031212" style="color:#9b1c2c">${PHONE}</a>, or simply reply to this email.</p>
  <p style="font-size:15px;line-height:1.6;margin:0 0 30px">Warm regards,<br><b>The V5 Events team</b></p>
</td></tr>
<tr><td style="background:#2a1418;color:#e9dcd6;padding:18px 32px;font-size:12px;line-height:1.6">
  V5 Events · Seattle area, WA<br>
  <a href="${esc(site)}" style="color:#f2c14e">v5-events.com</a> · <a href="mailto:${BUSINESS_EMAIL}" style="color:#f2c14e">${BUSINESS_EMAIL}</a> · ${PHONE}
</td></tr>
</table></td></tr></table></body></html>`;

  const text = [
    `Thank you, ${first}.`,
    "",
    "We've received your intake form and we're excited to start planning your celebration with you.",
    "Attached: your intake summary (PDF) and our service terms (PDF).",
    "",
    ...rows.map(([k, v]) => `${k}: ${v}`),
    "",
    "What happens next:",
    "1. We review your details and may call you with a few questions.",
    "2. We send you a clear quote and your event agreement.",
    "3. A non-refundable 30% deposit, due within 24 hours of booking, confirms your dates.",
    "",
    `Need to change something? Submit a new intake form at ${site}/intake/ with your updated details.`,
    `Questions? Call or WhatsApp ${PHONE}, or reply to this email.`,
    "",
    "Warm regards,",
    "The V5 Events team",
    `${site} · ${BUSINESS_EMAIL}`,
  ].join("\n");

  return { subject, html, text };
}

async function prepare(d, { site, submittedAt }) {
  const [logoPng, termsPdf] = await Promise.all([fetchBytes(`${site}/assets/mark.png`), fetchBytes(`${site}/assets/V5-Events-Service-Terms.pdf`)]);
  const summaryPdf = await buildIntakePdf(d, { logoPng, submittedAt });
  const safeName = customerName(d).replace(/[^A-Za-z0-9]+/g, "-").replace(/^-|-$/g, "") || "Intake";
  const attachments = [{ filename: `V5-Events-Intake-Summary-${safeName}.pdf`, content: summaryPdf, contentType: "application/pdf" }];
  if (termsPdf) attachments.push({ filename: "V5-Events-Service-Terms.pdf", content: termsPdf, contentType: "application/pdf" });
  return { ...buildEmail(d, site), attachments };
}

exports.handler = async (event) => {
  let payload;
  try {
    ({ payload } = JSON.parse(event.body || "{}"));
  } catch {
    return { statusCode: 200, body: "Not a form submission" };
  }
  if (!payload || payload.form_name !== "intake") return { statusCode: 200, body: "Not the intake form" };

  const d = payload.data || {};
  const to = String(d.email || "").trim();
  if (!validEmail(to)) {
    console.log("Intake submission has no valid email address; no thank-you email sent.");
    return { statusCode: 200, body: "No customer email" };
  }
  const user = process.env.GMAIL_USER, pass = process.env.GMAIL_APP_PASSWORD;
  if (!user || !pass) {
    console.log("GMAIL_USER / GMAIL_APP_PASSWORD are not set; no thank-you email sent.");
    return { statusCode: 200, body: "Email not configured" };
  }

  const site = (process.env.URL || "https://v5-events.com").replace(/\/$/, "");
  const submittedAt = payload.created_at ? new Date(payload.created_at) : new Date();
  try {
    const mail = await prepare(d, { site, submittedAt });
    const transport = nodemailer.createTransport({ host: "smtp.gmail.com", port: 465, secure: true, auth: { user, pass } });
    await transport.sendMail({
      from: { name: "V5 Events", address: user },
      to,
      bcc: user,
      replyTo: BUSINESS_EMAIL,
      ...mail,
    });
    console.log(`Thank-you email sent to ${to}`);
    return { statusCode: 200, body: "Sent" };
  } catch (err) {
    // A failed email never loses the submission: it is already saved in Netlify Forms.
    console.error("Thank-you email failed:", err && err.message);
    return { statusCode: 200, body: "Email failed" };
  }
};

exports.prepare = prepare;
