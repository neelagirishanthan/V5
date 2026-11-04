# V5 Event Management

Customer-facing documents for V5 Event Management's Indian wedding planning.

| Folder | What it is |
|---|---|
| `intake-form/` | Online customer intake form (events, guest counts, decor, food, bar, DJ, priest, photography, accommodation) |
| `intake-flyer/` | Printable 3-page A4 intake flyer, HTML source and PDF |
| `quotes/feb-2027-wedding/` | Price quote for the February 2027 wedding, HTML source and PDF |
| `agreements/feb-2027-wedding/` | Wedding services agreement for the February 2027 wedding, HTML source and PDF |

Each PDF is rendered from the HTML file next to it with headless Chromium (Playwright) at A4 size.
Placeholders in square brackets, such as `[COUPLE NAMES]`, still need filling in before the documents go to a client.
