// Mobile menu toggle, shared by every page.
const toggle = document.querySelector(".menu-toggle");
const menu = document.getElementById("menu");
if (toggle && menu) {
  toggle.addEventListener("click", () => {
    const open = menu.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open);
  });
  menu.addEventListener("click", (e) => {
    if (e.target.closest("a")) { menu.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); }
  });
}
document.querySelectorAll("[data-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });

// Shared calendar helpers: ceremony colours and loading the public calendar.
window.V5 = {
  CEREMONIES: {
    "Haldi": "#e3a514",
    "Pelli Koduku & Kooturu": "#d0662a",
    "Sangeeth": "#7a3d8f",
    "Mehandi & Bangles": "#2f6b3a",
    "Pelli & Reception": "#9b1c2c",
    "Pelli (Wedding)": "#9b1c2c",
    "Vratham": "#1f5f8b"
  },
  color(name) { return this.CEREMONIES[name] || "#6a5558"; },
  async loadCalendar() {
    const res = await fetch("/data/calendar.json", { cache: "no-cache" });
    if (!res.ok) throw new Error("calendar " + res.status);
    return res.json();
  },
  fmtDate(iso, opts = { weekday: "short", month: "short", day: "numeric", year: "numeric" }) {
    const [y, m, d] = iso.split("-").map(Number);
    return new Date(y, m - 1, d || 1).toLocaleDateString("en-US", opts);
  },
  today() {
    const t = new Date();
    return `${t.getFullYear()}-${String(t.getMonth() + 1).padStart(2, "0")}-${String(t.getDate()).padStart(2, "0")}`;
  }
};
