/* BFI · Marwari Invitations — website script (no build step).
   One file: shared helpers, auth, and a small init function per page (body[data-page]). */
const CFG = window.BFI_CONFIG;
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const params = new URLSearchParams(location.search);
const IMG = (name) => CFG.imageBase + name;
const inr = (n) => "₹" + Number(n).toLocaleString("en-IN");

/* ---------- icons (24px line icons) ---------- */
const P = {
  check: '<path d="M20 6 9 17l-5-5"/>',
  heart: '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/>',
  left: '<path d="m15 18-6-6 6-6"/>', right: '<path d="m9 18 6-6-6-6"/>',
  edit: '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 1 1 3 3L7 19l-4 1 1-4Z"/>',
  music: '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
  link: '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
  rsvp: '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/><path d="m9 16 2 2 4-4"/>',
  map: '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
  globe: '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20"/>',
  qr: '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 14h3v3h-3zM20 14v.01M14 20h.01M17 20h4v-3"/>',
  image: '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.1-3.1a2 2 0 0 0-2.8 0L6 21"/>',
  clock: '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
  x: '<path d="M18 6 6 18M6 6l12 12"/>',
  trash: '<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>',
  eye: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
};
const ic = (n, cls = "") => `<svg class="${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${P[n] || ""}</svg>`;
const FEATURE_ICON = (f) => /music|audio|shehnai/i.test(f) ? "music" : /rsvp/i.test(f) ? "rsvp" : /link|qr/i.test(f) ? "link" : /map/i.test(f) ? "map" : /hindi|english|bilingual/i.test(f) ? "globe" : /photo/i.test(f) ? "image" : /countdown/i.test(f) ? "clock" : "edit";

/* ---------- small UI helpers ---------- */
function toast(msg, ms = 3200) {
  const t = document.createElement("div");
  t.className = "toast"; t.role = "status"; t.textContent = msg;
  document.body.append(t);
  setTimeout(() => t.remove(), ms);
}
const waHref = (text) => `https://wa.me/${CFG.whatsapp}?text=${encodeURIComponent(text)}`;
const waText = (design, date) => `Namaste BFI 🙏 I'd like to know more about ${design ? `the ${design} invitation` : "your digital wedding invitations"}${date ? ` for our wedding on ${date}` : ""}.`;
function openModal(html) {
  const m = document.createElement("div");
  m.className = "modal open";
  m.innerHTML = `<div class="modal-box" role="dialog" aria-modal="true"><button class="icon-btn modal-x" aria-label="Close">${ic("x")}</button>${html}</div>`;
  const close = () => { m.remove(); document.removeEventListener("keydown", onKey); };
  const onKey = (e) => e.key === "Escape" && close();
  m.addEventListener("click", (e) => { if (e.target === m || e.target.closest(".modal-x")) close(); });
  document.addEventListener("keydown", onKey);
  document.body.append(m);
  $("input,select,textarea,button:not(.modal-x)", m)?.focus();
  return { el: m, close };
}
function formData(form) {
  const o = {};
  for (const [k, v] of new FormData(form)) o[k] = typeof v === "string" ? v.trim() : v;
  return o;
}
function setBusy(btn, busy, label) {
  if (!btn) return;
  if (busy) { btn.dataset.label = btn.innerHTML; btn.disabled = true; btn.textContent = label || "Please wait…"; }
  else { btn.disabled = false; if (btn.dataset.label) btn.innerHTML = btn.dataset.label; }
}
function validate(form) {
  let ok = true;
  $$(".field", form).forEach((f) => { f.classList.remove("err"); $(".msg", f)?.remove(); });
  $$("[required]", form).forEach((inp) => {
    const bad = inp.type === "checkbox" ? !inp.checked : !inp.value.trim() || (inp.type === "email" && !/^\S+@\S+\.\S+$/.test(inp.value)) || (inp.type === "tel" && inp.value.replace(/\D/g, "").length < 10);
    if (bad) {
      ok = false;
      const f = inp.closest(".field") || inp.parentElement;
      f.classList.add("err");
      if (inp.type !== "checkbox") f.insertAdjacentHTML("beforeend", `<div class="msg">${inp.type === "tel" ? "Enter a 10-digit mobile number" : inp.type === "email" ? "Enter a valid email" : "This is required"}</div>`);
    }
  });
  if (!ok) $(".err input,.err select,.err textarea", form)?.focus();
  return ok;
}

/* ---------- Supabase ---------- */
const sb = window.supabase?.createClient(CFG.supabaseUrl, CFG.supabaseKey, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true, flowType: "pkce" },
});
let session = null;
const user = () => session?.user || null;
const displayName = () => user()?.user_metadata?.full_name || user()?.user_metadata?.name || user()?.email?.split("@")[0] || "";

/* Fallback catalogue, used only if the database can't be reached (keeps the site working offline). */
const FALLBACK = [
  ["rajwada-royale","Rajwada Royale","royal","Luxury",11999,"Golden palace and lanterns on deep maroon"],
  ["gulmohar-classic","Gulmohar Classic","traditional","Premium",6999,"Roses and marigolds on ivory"],
  ["gulabi-bagh","Gulabi Bagh","elegant","Premium",6999,"Blush peonies and fine gold"],
  ["mor-pankh","Mor Pankh","modern","Premium",7999,"Peacock on emerald green"],
  ["neel-mahal","Neel Mahal","royal","Luxury",11999,"Moonlit palace on royal navy"],
  ["gajraj-swagat","Gajraj Swagat","traditional","Basic",3999,"Royal elephants and marigold toran"],
  ["sheesh-mahal","Sheesh Mahal","royal","Luxury",14999,"Chandeliers and a golden haveli"],
  ["chhatri","Chhatri","elegant","Basic",3999,"A single gold chhatri, lots of calm"],
].map(([slug, name, collection, tier, price_from, tagline], i) => ({ slug, name, collection, tier, price_from, tagline, description: tagline + ".", features: ["Customizable names, dates and text", "Shareable link and QR code", "RSVP (optional)"], image: `inv-${slug}.jpg`, sort: i + 1 }));
const DARK = new Set(["rajwada-royale", "mor-pankh", "neel-mahal", "sheesh-mahal"]);
const COLLECTIONS = { royal: "Royal", traditional: "Traditional", elegant: "Elegant", modern: "Modern" };
let _inv;
async function invitations() {
  if (_inv) return _inv;
  try {
    if (!sb) throw new Error("offline");
    const { data, error } = await sb.from("invitations").select("*").order("sort");
    if (error || !data?.length) throw error || new Error("empty");
    _inv = data;
  } catch { _inv = FALLBACK; }
  return _inv;
}
let favs = new Set();
async function loadFavs() {
  if (!user()) { favs = new Set(); return; }
  const { data } = await sb.from("favorites").select("slug");
  favs = new Set((data || []).map((r) => r.slug));
}
async function toggleFav(slug, btn) {
  if (!user()) { location.href = `login.html?next=${encodeURIComponent(location.pathname + location.search)}&why=fav`; return; }
  const on = !favs.has(slug);
  btn.setAttribute("aria-pressed", on);
  const { error } = on ? await sb.from("favorites").insert({ slug }) : await sb.from("favorites").delete().eq("slug", slug);
  if (error) { btn.setAttribute("aria-pressed", !on); return toast("Couldn't update favourites. Please try again."); }
  on ? favs.add(slug) : favs.delete(slug);
  toast(on ? "Saved to your favourites" : "Removed from favourites");
}
async function sendEnquiry(row) {
  const { error } = await sb.from("enquiries").insert(row);
  if (error) throw error;
}

/* ---------- shared chrome ---------- */
function renderAuthSlot() {
  $$("[data-auth-slot]").forEach((el) => {
    el.innerHTML = user()
      ? `<a class="avatar" href="account.html" title="My account" aria-label="My account">${esc((displayName()[0] || "B").toUpperCase())}</a>`
      : `<a class="btn btn-outline btn-sm login-link" href="login.html">Login</a><a class="icon-btn menu-login" href="login.html" aria-label="Login"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg></a>`;
  });
  $$("[data-auth-menu]").forEach((el) => {
    el.innerHTML = user()
      ? `<a class="btn btn-ghost btn-block" href="account.html">My account</a>`
      : `<a class="btn btn-ghost btn-block" href="login.html">Login or create account</a>`;
  });
}
function initChrome() {
  $$("[data-wa]").forEach((a) => { a.href = waHref(a.dataset.wa || waText()); a.target = "_blank"; a.rel = "noopener"; });
  $$("[data-img]").forEach((el) => {
    const url = IMG(el.dataset.img);
    if (el.tagName === "IMG") el.src = url; else el.style.backgroundImage = `url("${url}")`;
  });
  $$("[data-cfg]").forEach((el) => (el.textContent = CFG[el.dataset.cfg]));
  $$("[data-mailto]").forEach((a) => (a.href = "mailto:" + CFG.email));
  $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
  const sheet = $("#menu");
  $$("[data-menu-open]").forEach((b) => b.addEventListener("click", () => { sheet.classList.add("open"); $("a", sheet)?.focus(); }));
  sheet?.addEventListener("click", (e) => { if (e.target.closest("[data-menu-close]") || e.target.classList.contains("sheet-bg")) sheet.classList.remove("open"); });
  document.addEventListener("keydown", (e) => e.key === "Escape" && sheet?.classList.remove("open"));
  const io = "IntersectionObserver" in window && new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px" });
  $$(".reveal").forEach((el) => (io ? io.observe(el) : el.classList.add("in")));
  renderAuthSlot();
}

/* ---------- invitation card ---------- */
function card(inv) {
  const on = favs.has(inv.slug);
  return `<article class="card">
    <button class="fav" data-fav="${esc(inv.slug)}" aria-pressed="${on}" aria-label="Save ${esc(inv.name)} to favourites">${ic("heart")}</button>
    <a class="card-img" href="design-${encodeURIComponent(inv.slug)}.html"><img src="${IMG(inv.image)}" alt="${esc(inv.name)} invitation: ${esc(inv.tagline)}" loading="lazy" width="360" height="540">
      <span class="script ${DARK.has(inv.slug) ? "pv-dark" : "pv-light"}">Wedding Invitation</span></a>
    <div class="card-body">
      <span class="tag">${COLLECTIONS[inv.collection]}</span>
      <h3><a href="design-${encodeURIComponent(inv.slug)}.html">${esc(inv.name)}</a></h3>
      <div class="card-meta"><span>${esc(inv.tier)}</span><span>from <b>${inr(inv.price_from)}</b></span></div>
    </div></article>`;
}
function bindFavs(root) {
  root.addEventListener("click", (e) => {
    const b = e.target.closest("[data-fav]");
    if (b) { e.preventDefault(); toggleFav(b.dataset.fav, b); }
  });
}

/* ================= pages ================= */
const pages = {};

pages.index = async () => {
  // Real, studio-approved reviews only; the section stays hidden until there are some.
  if (!sb) return;
  const { data } = await sb.from("reviews").select("name,city,rating,body,design_slug").eq("approved", true).order("created_at", { ascending: false }).limit(6);
  if (!data?.length) return;
  $("#reviews").innerHTML = data.map((r) => `<figure class="review"><div class="stars" aria-label="${r.rating} out of 5">${"★".repeat(r.rating)}${"☆".repeat(5 - r.rating)}</div><p>“${esc(r.body)}”</p><small>${esc(r.name)}${r.city ? ", " + esc(r.city) : ""}</small></figure>`).join("");
  $("#reviews-sec").hidden = false;
};

pages.invitations = async () => {
  const grid = $("#grid"), count = $("#count");
  let col = COLLECTIONS[params.get("c")] ? params.get("c") : "all";
  const all = await invitations();
  const tierSel = $("#tier"), sortSel = $("#sort");
  function draw() {
    let list = all.filter((i) => (col === "all" || i.collection === col) && (!tierSel.value || i.tier === tierSel.value));
    if (sortSel.value === "low") list = [...list].sort((a, b) => a.price_from - b.price_from);
    if (sortSel.value === "high") list = [...list].sort((a, b) => b.price_from - a.price_from);
    grid.innerHTML = list.length ? list.map(card).join("") : `<div class="empty">No invitations match these filters. <button class="linkbtn" id="reset">Show all</button></div>`;
    count.textContent = `Showing ${list.length} invitation${list.length === 1 ? "" : "s"}`;
    $$(".chip").forEach((c) => c.setAttribute("aria-pressed", c.dataset.c === col));
    $("#reset")?.addEventListener("click", () => { col = "all"; tierSel.value = ""; sortSel.value = ""; sync(); draw(); });
  }
  function sync() { const u = new URL(location); col === "all" ? u.searchParams.delete("c") : u.searchParams.set("c", col); history.replaceState(null, "", u); }
  $$(".chip").forEach((c) => c.addEventListener("click", () => { col = c.dataset.c; sync(); draw(); }));
  tierSel.addEventListener("change", draw); sortSel.addEventListener("change", draw);
  bindFavs(grid);
  draw();
};

// Old dynamic URL: invitation.html?slug=x -> design-x.html
pages.invitation = async () => {
  const slug = params.get("slug");
  location.replace(slug && /^[a-z0-9-]+$/.test(slug) ? `design-${slug}.html` : "invitations.html");
};

// Static design page: gallery, favourite, ask modal
function initDesignPage() {
  const root = $("#detail");
  if (!root) return;
  const inv = { slug: root.dataset.slug, name: root.dataset.name };
  const slides = $$("#slide .slide");
  let i = 0;
  const show = (n) => { i = (n + slides.length) % slides.length; slides.forEach((s, k) => (s.hidden = k !== i)); $$(".dots button").forEach((d, k) => d.setAttribute("aria-current", k === i)); };
  $(".prev").onclick = () => show(i - 1); $(".next").onclick = () => show(i + 1);
  $$(".dots button").forEach((d, k) => (d.onclick = () => show(k)));
  let x0 = null; $("#slide").addEventListener("touchstart", (e) => (x0 = e.touches[0].clientX), { passive: true });
  $("#slide").addEventListener("touchend", (e) => { if (x0 == null) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) show(i + (dx < 0 ? 1 : -1)); x0 = null; });
  bindFavs(root); bindFavs($("#similar"));
  $("#ask").onclick = () => enquiryModal(inv);
}

function enquiryModal(inv) {
  const u = user();
  const m = openModal(`<h2 style="font-size:28px;padding-right:40px">Ask about ${esc(inv.name)}</h2><p class="muted" style="margin:6px 0 16px">We reply within an hour, ${esc(CFG.hours)}.</p>
  <form class="form" novalidate id="askf">
    <div class="field"><label for="a-name">Your name <span class="req">*</span></label><input id="a-name" name="name" required autocomplete="name" value="${esc(displayName())}"></div>
    <div class="f2"><div class="field"><label for="a-phone">WhatsApp number <span class="req">*</span></label><input id="a-phone" name="phone" type="tel" required inputmode="tel" autocomplete="tel"></div>
    <div class="field"><label for="a-date">Wedding date</label><input id="a-date" name="wedding_date" type="date"></div></div>
    <div class="field"><label for="a-email">Email</label><input id="a-email" name="email" type="email" autocomplete="email" value="${esc(u?.email || "")}"></div>
    <div class="field"><label for="a-msg">Your question</label><textarea id="a-msg" name="message" placeholder="e.g. Can you add a Mayra page?"></textarea></div>
    <input type="text" name="company" tabindex="-1" autocomplete="off" class="sr" aria-hidden="true">
    <button class="btn btn-primary btn-block" type="submit">Send question</button></form>`);
  $("#askf", m.el).addEventListener("submit", async (e) => {
    e.preventDefault();
    const f = e.target; if (!validate(f)) return;
    const d = formData(f); if (d.company) return m.close();
    const btn = $("button[type=submit]", f); setBusy(btn, true, "Sending…");
    try {
      await sendEnquiry({ name: d.name, phone: d.phone, email: d.email || null, wedding_date: d.wedding_date || null, message: d.message || null, design_slug: inv.slug, source: "details" });
      f.outerHTML = `<div class="notice ok">Dhanyavaad! Your question about ${esc(inv.name)} has been sent. We'll reply on WhatsApp soon.</div>`;
    } catch { setBusy(btn, false); toast("Couldn't send. Please try again or message us on WhatsApp."); }
  });
}

/* ---------- customize ---------- */
const EVENT_TYPES = ["Ganesh Puja", "Mayra", "Haldi", "Mehendi", "Mahila Sangeet", "Baraat", "Phera (Wedding)", "Reception", "Other"];
const CZ_KEY = "bfi.customize.v1";
pages.customize = async () => {
  const all = await invitations();
  let st;
  try { st = JSON.parse(localStorage.getItem(CZ_KEY) || "null"); } catch { st = null; }
  st = st || {};
  st.data = st.data || { events: [{ type: "Phera (Wedding)", date: "", time: "", venue: "", map: "" }], language: "English", blessing: "॥ श्री गणेशाय नमः ॥", music: "Shehnai", rsvp: true, guests: true, meal: false, order: "bride" };
  if (params.get("design")) st.data.design = params.get("design");
  if (!st.data.design || !all.find((i) => i.slug === st.data.design)) st.data.design = all[0].slug;
  st.step = st.step || 0;
  if (params.get("id") && user()) {
    const { data } = await sb.from("customizations").select("*").eq("id", params.get("id")).maybeSingle();
    if (data) { st = { id: data.id, step: 0, data: { ...data.data, design: data.design_slug || data.data.design } }; }
  }
  const D = st.data;
  const steps = ["Design", "Couple", "Events & venues", "Language & music", "RSVP & contact", "Review"];
  const form = $("#cz-form");
  const save = () => { try { localStorage.setItem(CZ_KEY, JSON.stringify(st)); } catch {} };
  const inv = () => all.find((i) => i.slug === D.design);
  const fmtDate = (s) => { if (!s) return ""; const d = new Date(s + "T00:00"); return isNaN(d) ? s : d.toLocaleDateString("en-IN", { weekday: "long", day: "numeric", month: "long", year: "numeric" }); };

  function preview() {
    const i = inv();
    $("#pv").style.backgroundImage = `url("${IMG(i.image)}")`;
    const main = D.events.find((e) => /phera/i.test(e.type)) || D.events[0] || {};
    const [a, b] = D.order === "groom" ? [D.groom, D.bride] : [D.bride, D.groom];
    $("#pv").innerHTML = `<div class="pv-text ${DARK.has(i.slug) ? "pv-dark" : "pv-light"}">
      ${D.blessing ? `<span class="pv-deva" lang="hi">${esc(D.blessing)}</span>` : ""}
      <span class="pv-names">${esc(a || "Bride")}<br><small class="pv-weds">weds</small><br>${esc(b || "Groom")}</span>
      <span class="pv-date">${esc(fmtDate(main.date) || "Wedding date")}</span>
      <span class="pv-ven">${esc(main.venue || "Venue")}</span></div>`;
    $("#pv-name").textContent = i.name;
    $("#pv-events").textContent = `${D.events.length} event${D.events.length === 1 ? "" : "s"} · ${D.language}${D.music && D.music !== "None" ? " · " + D.music : ""}${D.rsvp ? " · RSVP on" : ""}`;
  }
  const f = (name, label, attrs = "", val = D[name]) => `<div class="field"><label for="f-${name}">${label}</label><input id="f-${name}" name="${name}" value="${esc(val || "")}" ${attrs}></div>`;
  const tog = (name, label) => `<label class="check"><input type="checkbox" name="${name}" ${D[name] ? "checked" : ""}> ${label}</label>`;
  // opts: strings, or [value, label] pairs
  const sel = (name, label, opts) => `<div class="field"><label for="f-${name}">${label}</label><select id="f-${name}" name="${name}">${opts.map((o) => { const [v, t] = Array.isArray(o) ? o : [o, o]; return `<option value="${esc(v)}" ${v === (D[name] ?? "") ? "selected" : ""}>${esc(t)}</option>`; }).join("")}</select></div>`;

  function body(n) {
    if (n === 0) return `<div class="opt-grid">${all.map((i) => `<label class="opt"><input type="radio" name="design" value="${i.slug}" ${i.slug === D.design ? "checked" : ""}><img src="${IMG(i.image)}" alt="" loading="lazy"><span>${esc(i.name)}</span></label>`).join("")}</div>`;
    if (n === 1) return `<div class="form"><div class="f2">${f("bride", "Bride's name <span class='req'>*</span>", 'required autocomplete="off" placeholder="e.g. Priya"')}${f("groom", "Groom's name <span class='req'>*</span>", 'required autocomplete="off" placeholder="e.g. Rohan"')}</div>
      ${sel("order", "Name order", [["bride", "Bride's name first"], ["groom", "Groom's name first"]])}
      <div class="f2">${f("bride_family", "Bride's parents", 'placeholder="e.g. Smt. & Shri Ramesh Agarwal"')}${f("groom_family", "Groom's parents", 'placeholder="e.g. Smt. & Shri Suresh Maheshwari"')}</div>
      ${f("blessings", "Blessings from (grandparents, elders)", 'placeholder="Optional"')}</div>`;
    if (n === 2) return `<div class="form" id="events">${D.events.map((e, k) => `<div class="event" data-k="${k}">
        ${D.events.length > 1 ? `<button type="button" class="icon-btn rm" data-rm="${k}" aria-label="Remove event">${ic("trash")}</button>` : ""}
        <div class="field"><label>Event</label><select data-ev="type">${EVENT_TYPES.map((t) => `<option ${t === e.type ? "selected" : ""}>${t}</option>`).join("")}</select></div>
        <div class="f2"><div class="field"><label>Date <span class="req">*</span></label><input type="date" data-ev="date" value="${esc(e.date)}" ${k === 0 ? "required" : ""}></div><div class="field"><label>Time</label><input type="time" data-ev="time" value="${esc(e.time)}"></div></div>
        <div class="field"><label>Venue</label><input data-ev="venue" value="${esc(e.venue)}" placeholder="e.g. Rambagh Palace, Jaipur"></div>
        <div class="field"><label>Google Maps link</label><input type="url" data-ev="map" value="${esc(e.map)}" placeholder="https://maps.app.goo.gl/…" inputmode="url"></div></div>`).join("")}
        <button type="button" class="btn btn-ghost" id="add-ev">${ic("plus")} Add another event</button></div>`;
    if (n === 3) return `<div class="form">${sel("language", "Language", ["English", "Hindi", "Marwari + Hindi", "Bilingual (Hindi + English)"])}
      ${sel("blessing", "Opening blessing", ["॥ श्री गणेशाय नमः ॥", "॥ शुभ विवाह ॥", ["", "No blessing line"]])}
      ${sel("music", "Music", ["Shehnai", "Soft instrumental", "Our own song (we'll send it)", "None"])}
      <div class="field"><label for="f-notes">Anything else?</label><textarea id="f-notes" name="notes" placeholder="Special rituals, dress codes, a family story…">${esc(D.notes || "")}</textarea></div></div>`;
    if (n === 4) return `<div class="form"><div class="toggles">${tog("rsvp", "Collect RSVPs")}${tog("guests", "Ask for guest count")}${tog("meal", "Ask for meal preference")}</div>
      ${f("rsvp_by", "RSVP deadline", 'type="date"')}
      <div class="f2">${f("contact_name", "Your name <span class='req'>*</span>", 'required autocomplete="name"', D.contact_name || displayName())}${f("phone", "WhatsApp number <span class='req'>*</span>", 'type="tel" required inputmode="tel" autocomplete="tel"')}</div>
      ${f("email", "Email", 'type="email" autocomplete="email"', D.email || user()?.email)}
      ${sel("package", "Package", ["Not sure", "Basic", "Premium", "Luxury"])}</div>`;
    const i = inv();
    const rows = [["Design", i.name], ["Couple", [D.bride, D.groom].filter(Boolean).join(" & ") || "—"], ["Families", [D.bride_family, D.groom_family].filter(Boolean).join(" · ") || "—"], ["Events", D.events.map((e) => `${e.type}${e.date ? " – " + fmtDate(e.date) : ""}${e.venue ? ", " + e.venue : ""}`).join("<br>")], ["Language", D.language], ["Music", D.music], ["RSVP", D.rsvp ? `On${D.rsvp_by ? " until " + fmtDate(D.rsvp_by) : ""}` : "Off"], ["Contact", [D.contact_name, D.phone, D.email].filter(Boolean).join(" · ") || "—"], ["Package", D.package || "Not sure"]];
    return `<dl style="display:grid;grid-template-columns:110px 1fr;gap:10px 14px;margin:0">${rows.map(([k, v]) => `<dt class="muted">${k}</dt><dd style="margin:0">${k === "Events" ? v : esc(v)}</dd>`).join("")}</dl>
      <p class="d-price" style="font-size:26px;margin-top:20px">Estimate: from ${inr(i.price_from)}</p>
      <div class="d-actions" style="margin-top:16px"><button type="button" class="btn btn-primary" id="submit-cz">Send for design ${ic("arrow")}</button>
      <a class="btn btn-wa" id="wa-cz">${WA_SVG} Continue on WhatsApp</a></div>
      <p style="margin-top:12px"><button type="button" class="linkbtn" id="save-cz">${user() ? "Save draft to my account" : "Login to save this draft"}</button></p>`;
  }
  function collect() {
    $$("[name]", form).forEach((el) => {
      if (el.type === "radio") { if (el.checked) D[el.name] = el.value; }
      else if (el.type === "checkbox") D[el.name] = el.checked;
      else D[el.name] = el.value.trim();
    });
    $$("#events .event").forEach((box) => { const e = D.events[+box.dataset.k]; $$("[data-ev]", box).forEach((el) => (e[el.dataset.ev] = el.value.trim())); });
    save(); preview();
  }
  function draw() {
    const n = st.step;
    $("#stepper").innerHTML = steps.map((s, k) => `<button type="button" aria-label="Step ${k + 1}: ${s}" class="${k < n ? "done" : k === n ? "cur" : ""}" data-go="${k}"></button>`).join("");
    form.innerHTML = `<div class="step-title"><h2 style="font-size:28px">${steps[n]}</h2><small>Step ${n + 1} of ${steps.length}</small></div>${body(n)}
      <div class="cz-nav">${n ? `<button type="button" class="btn btn-ghost" data-back>${ic("left")} Back</button>` : "<span></span>"}${n < steps.length - 1 ? `<button type="submit" class="btn btn-primary">Next ${ic("right")}</button>` : ""}</div>`;
    preview();
    if (n === steps.length - 1) {
      const i = inv();
      $("#wa-cz").href = waHref(`Namaste BFI 🙏 We'd like the ${i.name} invitation.\nCouple: ${D.bride || "?"} & ${D.groom || "?"}\nEvents: ${D.events.map((e) => `${e.type} ${e.date || ""} ${e.venue || ""}`.trim()).join("; ")}\nLanguage: ${D.language}. Music: ${D.music}. RSVP: ${D.rsvp ? "yes" : "no"}.`);
      $("#wa-cz").target = "_blank";
      $("#submit-cz").onclick = submit;
      $("#save-cz").onclick = saveRemote;
    }
  }
  async function saveRemote(status = "draft") {
    if (!user()) { save(); location.href = `login.html?next=${encodeURIComponent("customize.html")}&why=save`; return null; }
    const row = { design_slug: D.design, data: D, status, updated_at: new Date().toISOString() };
    const q = st.id ? sb.from("customizations").update(row).eq("id", st.id).select("id").single() : sb.from("customizations").insert(row).select("id").single();
    const { data, error } = await q;
    if (error) { toast("Couldn't save. Please try again."); return null; }
    st.id = data.id; save();
    if (status === "draft") toast("Draft saved to your account");
    return data.id;
  }
  async function submit(e) {
    const btn = e.currentTarget;
    for (const [k, s] of [["bride", 1], ["groom", 1], ["contact_name", 4], ["phone", 4]]) if (!D[k]) { st.step = s; draw(); validate(form); return toast("Please fill in the required details"); }
    if (!D.events[0]?.date) { st.step = 2; draw(); validate(form); return toast("Please add the wedding date"); }
    setBusy(btn, true, "Sending…");
    try {
      if (user()) await saveRemote("submitted");
      await sendEnquiry({ name: D.contact_name, phone: D.phone, email: D.email || null, wedding_date: D.events.find((x) => /phera/i.test(x.type))?.date || D.events[0].date || null, package: D.package || "Not sure", design_slug: D.design, source: "customize",
        message: `Couple: ${D.bride} & ${D.groom}. Events: ${D.events.map((x) => `${x.type} ${x.date} ${x.time} ${x.venue}`.replace(/\s+/g, " ").trim()).join("; ")}. Language: ${D.language}. Music: ${D.music}. RSVP: ${D.rsvp ? "on" : "off"}. ${D.notes || ""}`.slice(0, 2000) });
      localStorage.removeItem(CZ_KEY);
      form.innerHTML = `<div class="notice ok" style="font-size:16px"><b>Dhanyavaad!</b> We've received the details for ${esc(inv().name)}. Our designer will share the first preview on WhatsApp within ${inv().tier === "Basic" ? "24" : inv().tier === "Premium" ? "48" : "72"} hours.</div>
        <div class="row" style="margin-top:18px"><a class="btn btn-wa" data-wa="${esc(waText(inv().name))}">${WA_SVG} Chat on WhatsApp</a>${user() ? '<a class="btn btn-ghost" href="account.html">Go to my account</a>' : ""}</div>`;
      $("#stepper").innerHTML = ""; initChrome();
    } catch { setBusy(btn, false); toast("Couldn't send. Please try again or continue on WhatsApp."); }
  }
  form.addEventListener("submit", (e) => { e.preventDefault(); collect(); if (!validate(form)) return; st.step++; save(); draw(); form.scrollIntoView({ block: "start" }); });
  form.addEventListener("input", collect);
  form.addEventListener("change", collect);
  form.addEventListener("click", (e) => {
    if (e.target.closest("[data-back]")) { collect(); st.step--; save(); draw(); }
    if (e.target.closest("#add-ev")) { collect(); D.events.push({ type: "Reception", date: "", time: "", venue: "", map: "" }); draw(); }
    const rm = e.target.closest("[data-rm]"); if (rm) { collect(); D.events.splice(+rm.dataset.rm, 1); draw(); }
  });
  $("#stepper").addEventListener("click", (e) => { const b = e.target.closest("[data-go]"); if (b && +b.dataset.go <= st.step) { collect(); st.step = +b.dataset.go; draw(); } });
  $("#show-pv")?.addEventListener("click", () => $(".cz-preview").classList.add("open"));
  $(".pv-close")?.addEventListener("click", () => $(".cz-preview").classList.remove("open"));
  draw();
};

/* ---------- contact ---------- */
pages.contact = async () => {
  const form = $("#contact-form");
  if (params.get("design")) form.design.value = params.get("design");
  if (user()) { form.name.value = displayName(); form.email.value = user().email || ""; }
  form.addEventListener("submit", async (e) => {
    e.preventDefault(); if (!validate(form)) return;
    const d = formData(form); if (d.company) return;
    const btn = $("button[type=submit]", form); setBusy(btn, true, "Sending…");
    try {
      await sendEnquiry({ name: d.name, phone: d.phone, email: d.email || null, wedding_date: d.wedding_date || null, city: d.city || null, package: d.package || "Not sure", design_slug: d.design || null, message: d.message || null, source: "contact" });
      const waMsg = `Namaste BFI 🙏 I just sent an enquiry on your website.\nName: ${d.name}\nWedding date: ${d.wedding_date || "not fixed"}\nCity: ${d.city || "-"}\nPackage: ${d.package || "Not sure"}\n${d.message || ""}`;
      form.outerHTML = `<div class="notice ok" style="font-size:16px"><b>Dhanyavaad, ${esc(d.name)}!</b> Your enquiry has reached us. We'll reply on WhatsApp within an hour (${esc(CFG.hours)}).</div>
        <p style="margin-top:14px">Want a faster reply? Send the same details on WhatsApp:</p><a class="btn btn-wa" style="margin-top:10px" target="_blank" rel="noopener" href="${waHref(waMsg)}">${WA_SVG} Send on WhatsApp</a>`;
    } catch { setBusy(btn, false); $("#c-status").innerHTML = `<div class="notice bad">Couldn't send your message. Please try again, or message us on WhatsApp.</div>`; }
  });
};

/* ---------- login ---------- */
pages.login = async () => {
  const nx = params.get("next") || "";
  const next = /^[\w\-./?=&%]+$/.test(nx) && !nx.startsWith("//") && !nx.includes("://") ? nx : "account.html";
  if (user()) { location.replace(next); return; }
  const why = { fav: "Login to save favourites.", save: "Login to save your invitation draft.", review: "Login to write a review." }[params.get("why")];
  if (why) $("#why").innerHTML = `<div class="notice info">${why}</div>`;
  const redirectTo = new URL(next, location.href).href;
  const status = $("#auth-status");
  const say = (cls, msg) => (status.innerHTML = `<div class="notice ${cls}">${msg}</div>`);
  const waHelp = `<a href="${waHref("Namaste BFI 🙏 I need help logging in to my account.")}" target="_blank" rel="noopener">message us on WhatsApp</a>`;
  // Email links (magic link, password reset) need the studio's email sender to be set up in Supabase.
  if (!CFG.authEmails) { $("#magic").hidden = true; }
  let mode = "signin";
  const setMode = (m) => {
    mode = m;
    $$(".tabs button").forEach((b) => b.setAttribute("aria-selected", b.dataset.mode === m));
    $("#name-field").hidden = m !== "signup";
    $("#pass-help").hidden = m !== "signup";
    $("#a-name").required = m === "signup";
    $("#a-pass").autocomplete = m === "signup" ? "new-password" : "current-password";
    $("#auth-submit").textContent = m === "signup" ? "Create account" : "Login";
    $("#forgot").hidden = m === "signup";
    status.innerHTML = "";
  };
  $$(".tabs button").forEach((b) => (b.onclick = () => setMode(b.dataset.mode)));
  if (params.get("mode") === "signup") setMode("signup");
  $("#google").onclick = async () => {
    const { error } = await sb.auth.signInWithOAuth({ provider: "google", options: { redirectTo } });
    if (error) say("bad", /provider is not enabled|Unsupported provider/i.test(error.message) ? "Google login is being set up. Please create an account with your email for now." : esc(error.message));
  };
  if (/error_description=/.test(location.hash) || params.get("error_description")) {
    const msg = new URLSearchParams(location.hash.slice(1)).get("error_description") || params.get("error_description");
    say("bad", /provider is not enabled/i.test(msg) ? "Google login is being set up. Please use email for now." : esc(msg));
  }
  const form = $("#auth-form");
  form.addEventListener("submit", async (e) => {
    e.preventDefault(); if (!validate(form)) return;
    const d = formData(form); const btn = $("#auth-submit");
    if (mode === "signup" && d.password.length < 8) { say("bad", "Use at least 8 characters for your password."); return; }
    setBusy(btn, true);
    try {
      if (mode === "signup") {
        const r = await fetch(`${CFG.supabaseUrl}/functions/v1/signup`, { method: "POST", headers: { "content-type": "application/json", apikey: CFG.supabaseKey },
          body: JSON.stringify({ email: d.email, password: d.password, name: d.name, company: d.company }) });
        const out = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(out.error || "Couldn't create the account. Please try again.");
      }
      const { error } = await sb.auth.signInWithPassword({ email: d.email, password: d.password });
      if (error) throw error;
      location.replace(next);
    } catch (err) {
      const m = err.message || "";
      say("bad", /invalid login/i.test(m) ? "Email or password is incorrect." : /not confirmed/i.test(m) ? `This account isn't activated yet. Please ${waHelp} and we'll activate it.` : /already has an account/i.test(m) ? `${esc(m)} <button class="linkbtn" data-to="signin">Go to login</button>` : esc(m));
      $("[data-to=signin]")?.addEventListener("click", () => setMode("signin"));
    } finally { setBusy(btn, false); }
  });
  $("#magic").onclick = async () => {
    const email = form.email.value.trim();
    if (!/^\S+@\S+\.\S+$/.test(email)) { form.email.focus(); return say("bad", "Enter your email above, then tap “Email me a login link”."); }
    const { error } = await sb.auth.signInWithOtp({ email, options: { emailRedirectTo: redirectTo, shouldCreateUser: false } });
    error ? say("bad", esc(error.message)) : say("ok", `Check <b>${esc(email)}</b> for a login link. It works once and expires in an hour.`);
  };
  $("#forgot").onclick = async () => {
    if (!CFG.authEmails) return say("info", `To reset your password, ${waHelp} from your registered number and we'll help you right away.`);
    const email = form.email.value.trim();
    if (!/^\S+@\S+\.\S+$/.test(email)) { form.email.focus(); return say("bad", "Enter your email above first."); }
    const { error } = await sb.auth.resetPasswordForEmail(email, { redirectTo: new URL("account.html#reset", location.href).href });
    error ? say("bad", esc(error.message)) : say("ok", `We've emailed a password reset link to <b>${esc(email)}</b>.`);
  };
};

pages.account = async () => {
  const root = $("#account");
  if (!user()) {
    // Give an OAuth/magic-link redirect a moment to finish before sending to login
    await new Promise((r) => setTimeout(r, 600));
    if (!user()) { location.replace("login.html?next=account.html"); return; }
  }
  const u = user();
  const all = await invitations();
  const bySlug = Object.fromEntries(all.map((i) => [i.slug, i]));
  const [{ data: prof }, { data: drafts }, { data: enq }] = await Promise.all([
    sb.from("profiles").select("*").eq("id", u.id).maybeSingle(),
    sb.from("customizations").select("id,design_slug,data,status,updated_at").order("updated_at", { ascending: false }),
    sb.from("enquiries").select("id,design_slug,status,source,created_at").order("created_at", { ascending: false }),
  ]);
  await loadFavs();
  const when = (s) => new Date(s).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
  const thumb = (slug) => (bySlug[slug] ? `<img src="${IMG(bySlug[slug].image)}" alt="">` : "");
  root.innerHTML = `
  <aside class="panel">
    <div style="display:flex;gap:14px;align-items:center"><span class="avatar" style="width:56px;height:56px;font-size:24px">${esc((displayName()[0] || "B").toUpperCase())}</span>
      <div style="min-width:0"><b style="font:600 22px var(--serif);color:var(--maroon)">${esc(prof?.full_name || displayName())}</b><br><small class="muted" style="word-break:break-all">${esc(u.email || "")}</small></div></div>
    <form class="form" id="prof" style="margin-top:20px" novalidate>
      <div class="field"><label for="p-name">Full name</label><input id="p-name" name="full_name" value="${esc(prof?.full_name || "")}" autocomplete="name"></div>
      <div class="field"><label for="p-phone">WhatsApp number</label><input id="p-phone" name="phone" type="tel" value="${esc(prof?.phone || "")}" autocomplete="tel" inputmode="tel"></div>
      <button class="btn btn-primary" type="submit">Save profile</button></form>
    <div id="pw-box"></div>
    <button class="btn btn-ghost btn-block" id="signout" style="margin-top:18px">Log out</button>
  </aside>
  <div style="display:grid;gap:22px">
    <section class="panel"><div class="step-title"><h2 style="font-size:26px">My invitations</h2><a class="btn btn-sm btn-primary" href="customize.html">${ic("plus")} New</a></div>
      <div class="list">${(drafts || []).length ? drafts.map((c) => `<div class="li">${thumb(c.design_slug)}<div class="grow"><b>${esc(bySlug[c.design_slug]?.name || "Invitation")}${c.data?.bride ? ` · ${esc(c.data.bride)} &amp; ${esc(c.data.groom || "")}` : ""}</b><small>Updated ${when(c.updated_at)}</small></div><span class="status">${c.status === "submitted" ? "Sent to studio" : "Draft"}</span>${c.status === "draft" ? `<a class="btn btn-sm btn-outline" href="customize.html?id=${c.id}">Continue</a>` : ""}</div>`).join("") : `<p class="muted">No saved invitations yet. <a href="invitations.html">Choose a design</a> to start.</p>`}</div></section>
    <section class="panel"><h2 style="font-size:26px;margin-bottom:14px">Favourites</h2>
      <div class="grid-inv" id="fav-grid">${favs.size ? all.filter((i) => favs.has(i.slug)).map(card).join("") : `<p class="muted" style="grid-column:1/-1">Tap the ♡ on any design to save it here.</p>`}</div></section>
    <section class="panel" id="review-box"><h2 style="font-size:26px;margin-bottom:6px">Write a review</h2><p class="muted" style="margin-bottom:14px">Received your invitation? Tell other families about it. Reviews appear on the website after the studio checks them.</p>
      <div id="my-reviews"></div>
      <form class="form" id="rev" novalidate>
        <div class="f2"><div class="field"><label for="rv-name">Name to show</label><input id="rv-name" name="name" required maxlength="80" value="${esc(prof?.full_name || displayName())}"></div>
        <div class="field"><label for="rv-city">City</label><input id="rv-city" name="city" maxlength="60" placeholder="e.g. Jaipur"></div></div>
        <div class="f2"><div class="field"><label for="rv-design">Design</label><select id="rv-design" name="design_slug"><option value="">Choose…</option>${all.map((i) => `<option value="${i.slug}">${esc(i.name)}</option>`).join("")}</select></div>
        <div class="field"><label for="rv-rating">Rating</label><select id="rv-rating" name="rating"><option value="5">★★★★★ Excellent</option><option value="4">★★★★ Very good</option><option value="3">★★★ Good</option><option value="2">★★ Fair</option><option value="1">★ Poor</option></select></div></div>
        <div class="field"><label for="rv-body">Your review</label><textarea id="rv-body" name="body" required minlength="10" maxlength="800" placeholder="What did your family and guests think?"></textarea></div>
        <button class="btn btn-primary" type="submit">Submit review</button></form></section>
    <section class="panel"><h2 style="font-size:26px;margin-bottom:14px">My enquiries</h2>
      <div class="list">${(enq || []).length ? enq.map((q) => `<div class="li">${thumb(q.design_slug)}<div class="grow"><b>${esc(bySlug[q.design_slug]?.name || "General enquiry")}</b><small>${when(q.created_at)} · via ${q.source === "customize" ? "Customize" : q.source === "details" ? "design page" : "Contact"}</small></div><span class="status">${{ new: "Received", contacted: "In touch", won: "Confirmed", lost: "Closed" }[q.status]}</span></div>`).join("") : `<p class="muted">Enquiries you send while logged in appear here.</p>`}</div></section>
  </div>`;
  bindFavs($("#fav-grid"));
  $("#prof").addEventListener("submit", async (e) => {
    e.preventDefault(); const d = formData(e.target); const btn = $("button", e.target); setBusy(btn, true, "Saving…");
    const { error } = await sb.from("profiles").update({ full_name: d.full_name || null, phone: d.phone || null }).eq("id", u.id);
    setBusy(btn, false); toast(error ? "Couldn't save. Please try again." : "Profile saved");
  });
  $("#signout").onclick = async () => { await sb.auth.signOut(); location.href = "index.html"; };
  const drawMine = async () => {
    const { data: mine } = await sb.from("reviews").select("rating,body,approved,created_at").eq("user_id", u.id).order("created_at", { ascending: false });
    $("#my-reviews").innerHTML = (mine || []).map((r) => `<div class="li" style="margin-bottom:10px"><div class="grow"><b>${"★".repeat(r.rating)}</b><small>${esc(r.body.slice(0, 120))}</small></div><span class="status">${r.approved ? "Published" : "Awaiting check"}</span></div>`).join("");
  };
  drawMine();
  $("#rev").addEventListener("submit", async (e) => {
    e.preventDefault(); const f = e.target; if (!validate(f)) return;
    const d = formData(f); if (d.body.length < 10) return toast("Please write at least a sentence");
    const btn = $("button", f); setBusy(btn, true, "Sending…");
    const { error } = await sb.from("reviews").insert({ name: d.name, city: d.city || null, design_slug: d.design_slug || null, rating: +d.rating, body: d.body });
    setBusy(btn, false);
    if (error) return toast("Couldn't send your review. Please try again.");
    f.reset(); f.name.value = prof?.full_name || displayName(); toast("Thank you! Your review will appear after a quick check."); drawMine();
  });
  const pwForm = () => {
    $("#pw-box").innerHTML = `<form class="form" id="pw" style="margin-top:20px;padding-top:18px;border-top:1px solid var(--beige)" novalidate><div class="field"><label for="pw-new">Set a new password</label><input id="pw-new" name="password" type="password" minlength="8" required autocomplete="new-password"></div><button class="btn btn-outline" type="submit">Update password</button></form>`;
    $("#pw").addEventListener("submit", async (e) => {
      e.preventDefault(); const p = e.target.password.value;
      if (p.length < 8) return toast("Use at least 8 characters");
      const { error } = await sb.auth.updateUser({ password: p });
      toast(error ? error.message : "Password updated");
      if (!error) $("#pw-box").innerHTML = "";
    });
  };
  if (location.hash === "#reset" || sessionStorage.getItem("bfi.recovery")) { sessionStorage.removeItem("bfi.recovery"); pwForm(); $("#pw-new").focus(); }
  else $("#pw-box").innerHTML = `<p style="margin-top:14px"><button class="linkbtn" id="pw-open">Change password</button></p>`, ($("#pw-open").onclick = pwForm);
};

/* ---------- live demo invitation ---------- */
pages.demo = async () => {
  const all = await invitations();
  const inv = all.find((i) => i.slug === params.get("design")) || all.find((i) => i.slug === "rajwada-royale") || all[0];
  const cover = $("#dv-cover");
  cover.style.backgroundImage = `url("${IMG(inv.image)}")`;
  cover.classList.toggle("dark", DARK.has(inv.slug));
  $("#demo-cta").href = $("#demo-cta2").href = `customize.html?design=${inv.slug}`;
  document.title = `Live Demo in ${inv.name} · BFI Marwari Invitations`;
  // Sample wedding ~60 days from today so the countdown always runs
  const day = (n) => { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() + n); return d; };
  const wedding = day(60); wedding.setHours(19, 30);
  const fmt = (d) => d.toLocaleDateString("en-IN", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
  $("#dv-date").textContent = fmt(wedding);
  const ev = [
    [56, "Ganesh Puja", "10:00 am", "Agarwal Niwas, C-Scheme, Jaipur"],
    [57, "Mayra", "11:00 am", "Agarwal Niwas, C-Scheme, Jaipur"],
    [58, "Pithi & Mehendi", "4:00 pm", "The Heritage Lawns, Jaipur"],
    [59, "Mahila Sangeet", "7:30 pm", "The Heritage Lawns, Jaipur"],
    [60, "Baraat & Phere", "7:30 pm", "Royal Palace Gardens, Jaipur"],
    [61, "Reception", "8:00 pm", "Royal Palace Gardens, Jaipur"],
  ];
  $("#dv-events").innerHTML = ev.map(([n, name, time, venue]) => { const d = day(n); return `<div class="dv-ev"><div class="d"><b>${d.getDate()}</b><span>${d.toLocaleDateString("en-IN", { month: "short" })}</span></div>
    <div><h3>${name}</h3><p>${d.toLocaleDateString("en-IN", { weekday: "long" })} · ${time}<br>${venue}</p><a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent("Jaipur, Rajasthan")}" target="_blank" rel="noopener">Open in Google Maps →</a></div></div>`; }).join("");
  const tick = () => {
    let t = Math.max(0, wedding - new Date());
    const u = { d: 864e5, h: 36e5, m: 6e4, s: 1e3 };
    for (const k of ["d", "h", "m", "s"]) { const v = Math.floor(t / u[k]); t -= v * u[k]; $(`[data-u=${k}]`).textContent = v; }
  };
  tick(); setInterval(tick, 1000);
  $("#dv-designs").innerHTML = all.map((i) => `<a href="demo.html?design=${i.slug}" aria-current="${i.slug === inv.slug}"><img src="${IMG(i.image)}" alt="" loading="lazy">${esc(i.name)}</a>`).join("");
  $("#dv-rsvp").addEventListener("submit", (e) => {
    e.preventDefault(); if (!validate(e.target)) return;
    e.target.outerHTML = `<div class="notice ok">This is a demo, so nothing was sent. On your real invitation, RSVPs reach you instantly with the guest count.</div>`;
  });
  const link = location.href;
  $("#dv-share").onclick = () => window.open(waHref(`Look at this wedding invitation by BFI: ${link}`).replace(`wa.me/${CFG.whatsapp}`, "wa.me/"), "_blank", "noopener");
  $("#dv-copy").onclick = async () => { try { await navigator.clipboard.writeText(link); toast("Link copied"); } catch { toast(link); } };
};

/* ---------- guide: copy wording ---------- */
pages.guide = () => {
  $$("[data-copy]").forEach((b) => (b.onclick = async () => {
    const text = b.previousElementSibling.innerText.trim();
    try { await navigator.clipboard.writeText(text); toast("Wording copied"); } catch { toast("Select the text to copy it"); }
  }));
};

/* ---------- WhatsApp glyph (brand mark, used only on WhatsApp buttons) ---------- */
var WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3Z"/></svg>';

/* ---------- boot ---------- */
(async function boot() {
  if (sb) {
    try { ({ data: { session } } = await sb.auth.getSession()); } catch {}
    sb.auth.onAuthStateChange((evt, s) => {
      session = s; renderAuthSlot();
      if (evt === "PASSWORD_RECOVERY") { sessionStorage.setItem("bfi.recovery", "1"); if (!location.pathname.endsWith("account.html")) location.href = "account.html#reset"; }
    });
    if (user()) loadFavs().then(() => $$("[data-fav]").forEach((b) => b.setAttribute("aria-pressed", favs.has(b.dataset.fav))));
  }
  initChrome();
  const page = document.body.dataset.page;
  try { page.startsWith("design-") ? initDesignPage() : await pages[page]?.(); } catch (e) { console.error(e); }
})();
