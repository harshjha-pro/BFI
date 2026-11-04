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
  sliders: '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
  book: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M8 7h8M8 11h6"/>',
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
let SID = "";
try { SID = sessionStorage.getItem("bfi.sid") || Math.random().toString(36).slice(2, 12); sessionStorage.setItem("bfi.sid", SID); } catch {}
function track(name, meta = {}) {
  try {
    if (!sb || navigator.webdriver || /localhost|127\.0\.0\.1/.test(location.hostname)) return;
    sb.from("analytics_events").insert({ name: String(name).slice(0, 40), page: location.pathname.slice(0, 120), meta, sid: SID }).then(() => {}, () => {});
  } catch {}
}
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
const TAGS = { "rajwada-royale": "royal luxury rajasthani", "gulmohar-classic": "traditional floral rajasthani", "gulabi-bagh": "elegant floral",
  "mor-pankh": "modern rajasthani", "neel-mahal": "royal luxury modern", "gajraj-swagat": "traditional rajasthani", "sheesh-mahal": "royal luxury rajasthani", "chhatri": "elegant minimal modern" };
const BEST = { "rajwada-royale": "Grand traditional weddings", "gulmohar-classic": "Classic family weddings", "gulabi-bagh": "Romantic day weddings",
  "mor-pankh": "Modern couples & destination weekends", "neel-mahal": "Evening receptions & sangeet nights", "gajraj-swagat": "Big Marwari family weddings",
  "sheesh-mahal": "Palace & destination weddings", "chhatri": "Intimate, minimal weddings" };
const tagsOf = (inv) => `${inv.collection} ${TAGS[inv.slug] || ""}`;
const COLLECTIONS = { royal: "Royal", traditional: "Traditional", elegant: "Elegant", modern: "Modern" };
const INSET = { "rajwada-royale": "24% 20% 37% 20%", "gulmohar-classic": "15% 17% 15% 17%", "gulabi-bagh": "17% 19% 17% 19%",
  "mor-pankh": "14% 24% 30% 16%", "neel-mahal": "13% 16% 40% 16%", "gajraj-swagat": "12% 15% 43% 15%",
  "sheesh-mahal": "23% 22% 47% 22%", "chhatri": "14% 17% 30% 17%" };
function inviteText(slug, o = {}) {
  const tone = DARK.has(slug) ? "pv-dark" : "pv-light";
  const [a, b] = [o.a || "Priya", o.b || "Rohan"];
  if (o.mini) return `<div class="inv-text ${tone}" style="inset:${INSET[slug] || "15%"}"><span class="it-caps">Wedding Invitation</span><span class="it-script">${esc(a)} <small>&amp;</small> ${esc(b)}</span><span class="it-rule"></span></div>`;
  return `<div class="inv-text ${tone}" style="inset:${INSET[slug] || "15%"}">${o.blessing === "" ? "" : `<span class="it-deva" lang="hi">${esc(o.blessing || "॥ श्री गणेशाय नमः ॥")}</span>`}
    <span class="it-caps">Together with their families</span><span class="it-script">${esc(a)}<small>weds</small>${esc(b)}</span>
    <span class="it-rule"></span><span class="it-date">${esc(o.date || "Saturday, 14 February")}</span><span class="it-ven">${esc(o.venue || "Rambagh Gardens, Jaipur")}</span></div>`;
}
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
  const groups = [".sec-head", ".grid-inv > .card", ".pkgs > .pkg", ".steps > .step", ".hrow", ".values > .value", ".timeline > .tl", ".next3 > div",
    ".occasions > div", ".policy > div", ".reviews > .review", ".ritual-list > li", ".why-list > div", ".trust-row > div", ".wording > .word-card",
    ".cinfo > *", ".strip-item", ".tiles > .tile", "details.acc", ".tbl-wrap", ".about-hero > *", ".split > *", ".panel", ".phead .wrap > *"];
  for (const sel of groups) $$(sel).forEach((el) => { if (el.closest(".hero, .dv, .modal, .sheet") || el.classList.contains("reveal")) return;
    const sib = [...el.parentElement.children].filter((x) => x.matches(sel.split(" > ").pop()));
    el.classList.add("reveal"); el.style.setProperty("--d", Math.min(sib.indexOf(el), 6) * 0.08 + "s"); });
  const io = "IntersectionObserver" in window && new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -6% 0px" });
  // hero motion: typing names (Customize) and the shuffling card stack (Free Cards)
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const typer = $(".typer");
  if (typer && !still && !typer.dataset.on) {
    typer.dataset.on = 1; const names = typer.dataset.names.split("|"); let n = 0, i = names[0].length, del = true;
    const step = () => { const w = names[n]; if (del) { i--; if (i <= 0) { del = false; n = (n + 1) % names.length; } } else { i++; if (i >= names[n].length) { del = true; typer.textContent = names[n]; return setTimeout(step, 1800); } }
      typer.textContent = names[n].slice(0, Math.max(i, 0)) || "\u00a0"; setTimeout(step, del ? 45 : 85); };
    setTimeout(step, 2200);
  }
  const stack = $("[data-stack]");
  if (stack && !still && !stack.dataset.on) {
    stack.dataset.on = 1; const imgs = [...stack.children]; let off = 0;
    setInterval(() => { if (document.hidden) return; off = (off + 1) % imgs.length; imgs.forEach((im, k) => { im.className = im.className.replace(/\bp\d\b/, "p" + ((k - off + imgs.length) % imgs.length)); }); }, 2600);
  }
  $$(".reveal").forEach((el) => (io ? io.observe(el) : el.classList.add("in")));
  renderAuthSlot();
}

/* ---------- invitation card ---------- */
function card(inv) {
  const on = favs.has(inv.slug);
  return `<article class="card" data-tags="${esc(tagsOf(inv))}">
    <button class="fav" data-fav="${esc(inv.slug)}" aria-pressed="${on}" aria-label="Save ${esc(inv.name)} to favourites">${ic("heart")}</button>
    <a class="card-img" href="design-${encodeURIComponent(inv.slug)}.html"><img src="${IMG(inv.image)}" alt="${esc(inv.name)} invitation: ${esc(inv.tagline)}" loading="lazy" width="360" height="540">${inviteText(inv.slug, { mini: true })}</a>
    <div class="card-body">
      <span class="tag">${COLLECTIONS[inv.collection]}</span>
      <h3><a href="design-${encodeURIComponent(inv.slug)}.html">${esc(inv.name)}</a></h3>
      <p class="card-desc">${esc(inv.tagline)}</p>${BEST[inv.slug] ? `<p class="card-best">Best for: ${esc(BEST[inv.slug])}</p>` : ""}
      <div class="card-meta"><span>${esc(inv.tier)}</span><span>from <b>${inr(inv.price_from)}</b></span></div>
      <div class="card-acts"><a class="btn btn-sm btn-ghost" href="demo.html?design=${encodeURIComponent(inv.slug)}">${ic("eye")} Live demo</a><a class="btn btn-sm btn-primary" href="customize.html?design=${encodeURIComponent(inv.slug)}">Customize</a></div>
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
  const box = $("#hero-petals");
  if (box && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const drop = () => { if (document.hidden) return; const p = document.createElement("i"); p.style.left = Math.random() * 100 + "%"; p.style.setProperty("--dx", (Math.random() * 120 - 60) + "px");
      p.style.animationDuration = 9 + Math.random() * 6 + "s"; box.append(p); setTimeout(() => p.remove(), 16000); };
    for (let k = 0; k < 6; k++) setTimeout(drop, k * 700);
    setInterval(drop, 1600);
  }
  // Real, studio-approved reviews only; the section stays hidden until there are some.
  if (!sb) return;
  const { data } = await sb.from("reviews").select("name,city,rating,body,design_slug").eq("approved", true).order("created_at", { ascending: false }).limit(6);
  if (!data?.length) return;
  $("#reviews").innerHTML = data.map((r) => `<figure class="review"><div class="stars" aria-label="${r.rating} out of 5">${"★".repeat(r.rating)}${"☆".repeat(5 - r.rating)}</div><p>“${esc(r.body)}”</p><small>${esc(r.name)}${r.city ? ", " + esc(r.city) : ""}</small></figure>`).join("");
  $("#reviews-sec").hidden = false;
};

pages.invitations = async () => {
  const grid = $("#grid"), count = $("#count");
  const FILT = ["all", "royal", "traditional", "elegant", "modern", "floral", "minimal", "luxury", "rajasthani"];
  let col = FILT.includes(params.get("c")) ? params.get("c") : "all";
  const all = await invitations();
  const tierSel = $("#tier"), sortSel = $("#sort");
  function draw() {
    let list = all.filter((i) => (col === "all" || tagsOf(i).split(" ").includes(col)) && (!tierSel.value || i.tier === tierSel.value));
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
const EVENT_TYPES = ["Ganesh Sthapana", "Mayra", "Pithi", "Haldi", "Mehendi", "Mahila Sangeet", "Sangeet", "Baraat", "Phere", "Reception", "Other"];
const CZ_KEY = "bfi.customize.v1";
pages.customize = async () => {
  const all = await invitations();
  const PKG = { Basic: { price: 3999, days: 24, events: 3, music: false, gallery: false, rsvp: false, colours: false, story: false },
    Premium: { price: 6999, days: 48, events: 8, music: true, gallery: true, rsvp: true, colours: false, story: false },
    Luxury: { price: 11999, days: 72, events: 99, music: true, gallery: true, rsvp: true, colours: true, story: true } };
  const TIERS = ["Basic", "Premium", "Luxury"];
  let st;
  try { st = JSON.parse(localStorage.getItem(CZ_KEY) || "null"); } catch { st = null; }
  st = st || {};
  st.data = st.data || { events: [{ type: "Phere", name: "", date: "", time: "", venue: "", map: "", notes: "" }], language: "English", blessing: "॥ श्री गणेशाय नमः ॥", music: "Shehnai", rsvp: true, guests: true, meal: false, gallery: false, order: "bride" };
  if (params.get("design")) st.data.design = params.get("design");
  if (!st.data.design || !all.find((i) => i.slug === st.data.design)) st.data.design = all[0].slug;
  st.step = Math.min(st.step || 0, 4);
  if (params.get("id") && user()) {
    const { data } = await sb.from("customizations").select("*").eq("id", params.get("id")).maybeSingle();
    if (data) st = { id: data.id, step: 0, data: { ...data.data, design: data.design_slug || data.data.design } };
  }
  const D = st.data;
  D.events = (D.events || []).map((e) => ({ name: "", notes: "", ...e, type: /phera/i.test(e.type) ? "Phere" : e.type }));
  const steps = ["Design & package", "Couple & family", "Wedding events", "Personalise", "Review & confirm", "Confirmed"];
  const form = $("#cz-form");
  const save = () => { try { localStorage.setItem(CZ_KEY, JSON.stringify(st)); } catch {} };
  const inv = () => all.find((i) => i.slug === D.design);
  const minTier = () => inv().tier;
  const fixPkg = () => { if (!TIERS.includes(D.package) || TIERS.indexOf(D.package) < TIERS.indexOf(minTier())) D.package = minTier(); };
  fixPkg();
  const P = () => PKG[D.package];
  const price = () => Math.max(P().price, inv().price_from);
  const fmtDate = (s) => { if (!s) return ""; const d = new Date(s + "T00:00"); return isNaN(d) ? s : d.toLocaleDateString("en-IN", { weekday: "long", day: "numeric", month: "long", year: "numeric" }); };
  const evName = (e) => (e.type === "Other" ? e.name || "Other function" : e.type);
  const mainEv = () => D.events.find((e) => /pher/i.test(e.type)) || D.events[0] || {};

  function preview() {
    const i = inv(), main = mainEv();
    const [a, b] = D.order === "groom" ? [D.groom, D.bride] : [D.bride, D.groom];
    const pv = $("#pv"); pv.classList.add("inv-wrap"); pv.style.backgroundImage = "";
    pv.innerHTML = `<img src="${IMG(i.image)}" alt="">` + inviteText(i.slug, { a: a || "Bride", b: b || "Groom", blessing: D.blessing, date: fmtDate(main.date || D.wedding_date) || "Wedding date", venue: main.venue || "Venue" });
    $("#pv-name").textContent = `${i.name} · ${D.package}`;
    $("#pv-events").textContent = `${D.events.length} event${D.events.length === 1 ? "" : "s"} · ${D.language} · est. ${inr(price())}`;
  }
  const f = (name, label, attrs = "", val = D[name]) => `<div class="field"><label for="f-${name}">${label}</label><input id="f-${name}" name="${name}" value="${esc(val || "")}" ${attrs}></div>`;
  const tog = (name, label, ok = true, lockMsg = "") => ok ? `<label class="check"><input type="checkbox" name="${name}" ${D[name] ? "checked" : ""}> ${label}</label>`
    : `<p class="locked">${ic("plus")} ${label} <span>${lockMsg}</span></p>`;
  const sel = (name, label, opts) => `<div class="field"><label for="f-${name}">${label}</label><select id="f-${name}" name="${name}">${opts.map((o) => { const [v, t] = Array.isArray(o) ? o : [o, o]; return `<option value="${esc(v)}" ${v === (D[name] ?? "") ? "selected" : ""}>${esc(t)}</option>`; }).join("")}</select></div>`;
  const upsell = (tier) => `<button type="button" class="linkbtn" data-upgrade="${tier}">Upgrade to ${tier}</button>`;

  function body(n) {
    if (n === 0) return `<p class="muted" style="margin-bottom:12px">1. Pick a design</p>
      <div class="opt-grid">${all.map((i) => `<label class="opt"><input type="radio" name="design" value="${i.slug}" ${i.slug === D.design ? "checked" : ""}><img src="${IMG(i.image)}" alt="" loading="lazy"><span>${esc(i.name)}<small style="display:block;font-weight:400;color:var(--muted)">${i.tier} · from ${inr(i.price_from)}</small></span></label>`).join("")}</div>
      <p class="muted" style="margin:22px 0 12px">2. Choose a package</p>
      <div class="pkg-pick">${TIERS.map((t) => { const p = PKG[t], off = TIERS.indexOf(t) < TIERS.indexOf(minTier());
        return `<label class="pp${off ? " off" : ""}"><input type="radio" name="package" value="${t}" ${D.package === t ? "checked" : ""} ${off ? "disabled" : ""}>
        <b>${t}</b><span class="pp-price">${inr(Math.max(p.price, t === minTier() ? inv().price_from : 0))}</span>
        <span>${p.events === 99 ? "Unlimited" : "Up to " + p.events} events · ${p.days} hrs</span><span>${[p.music && "Music", p.gallery && "Gallery", p.rsvp && "RSVP", p.colours && "Custom colours", p.story && "Family story"].filter(Boolean).join(" · ") || "Names, events, maps, QR"}</span>
        ${off ? `<em>${esc(inv().name)} starts in ${minTier()}</em>` : ""}</label>`; }).join("")}</div>
      <p class="muted" style="font-size:13.5px;margin-top:10px">Not sure? Pick the closest; we'll confirm with you on WhatsApp before you pay anything. <a href="pricing.html" target="_blank">Compare packages</a></p>`;
    if (n === 1) return `<div class="form"><div class="f2">${f("bride", "Bride's name <span class='req'>*</span>", 'required autocomplete="off" placeholder="e.g. Priya"')}${f("groom", "Groom's name <span class='req'>*</span>", 'required autocomplete="off" placeholder="e.g. Rohan"')}</div>
      <div class="f2">${sel("order", "Name order", [["bride", "Bride's name first"], ["groom", "Groom's name first"]])}${f("wedding_date", "Wedding date <span class='req'>*</span>", 'type="date" required')}</div>
      <div class="f2">${f("bride_family", "Bride's parents", 'placeholder="e.g. Smt. Sunita & Shri Mahesh Agarwal"')}${f("groom_family", "Groom's parents", 'placeholder="e.g. Smt. Rekha & Shri Anil Maheshwari"')}</div>
      ${f("blessings", "Grandparents / blessings from", 'placeholder="e.g. Smt. Kamla Devi & Late Shri Ramniwas Agarwal"')}
      ${sel("language", "Invitation language", ["English", "Hindi", "Marwari + Hindi", "Bilingual (Hindi + English)"])}
      <p class="help muted" style="font-size:13.5px">Write names exactly as they should appear. We check every name again before your preview.</p></div>`;
    if (n === 2) {
      const lim = P().events, over = D.events.length >= lim;
      return `<p class="muted" style="margin-bottom:12px">${D.package}: ${lim === 99 ? "unlimited events" : `up to ${lim} events`}. Use ↑ ↓ to set the order guests will see.</p>
      <div class="form" id="events">${D.events.map((e, k) => `<div class="event" data-k="${k}">
        <div class="ev-tools"><b>${k + 1}</b>
          <button type="button" class="icon-btn" data-mv="${k}:-1" aria-label="Move event up" ${k === 0 ? "disabled" : ""}>↑</button>
          <button type="button" class="icon-btn" data-mv="${k}:1" aria-label="Move event down" ${k === D.events.length - 1 ? "disabled" : ""}>↓</button>
          ${D.events.length > 1 ? `<button type="button" class="icon-btn" data-rm="${k}" aria-label="Remove event">${ic("trash")}</button>` : ""}</div>
        <div class="f2"><div class="field"><label>Function</label><select data-ev="type">${EVENT_TYPES.map((t) => `<option ${t === e.type ? "selected" : ""}>${t}</option>`).join("")}</select></div>
          ${e.type === "Other" ? `<div class="field"><label>Function name</label><input data-ev="name" value="${esc(e.name)}" placeholder="e.g. Tilak, Bhaat"></div>` : "<span></span>"}</div>
        <div class="f2"><div class="field"><label>Date <span class="req">*</span></label><input type="date" data-ev="date" value="${esc(e.date)}" required></div><div class="field"><label>Time</label><input type="time" data-ev="time" value="${esc(e.time)}"></div></div>
        <div class="field"><label>Venue</label><input data-ev="venue" value="${esc(e.venue)}" placeholder="e.g. Agarwal Niwas, C-Scheme, Jaipur"></div>
        <div class="field"><label>Google Maps link</label><input type="url" data-ev="map" value="${esc(e.map)}" placeholder="https://maps.app.goo.gl/…" inputmode="url"><div class="help">Open the venue in Google Maps → Share → Copy link.</div></div>
        <div class="field"><label>Notes (dress code, family only…)</label><input data-ev="notes" value="${esc(e.notes)}" maxlength="120"></div></div>`).join("")}
        ${over ? `<p class="notice info">You've reached the ${D.package} limit of ${lim} events. ${D.package !== "Luxury" ? upsell(D.package === "Basic" ? "Premium" : "Luxury") + " to add more." : ""}</p>`
          : `<button type="button" class="btn btn-ghost" id="add-ev">${ic("plus")} Add a function</button>`}</div>`;
    }
    if (n === 3) {
      const p = P(), nx = D.package === "Basic" ? "Premium" : "Luxury";
      return `<div class="form">${sel("blessing", "Opening blessing", ["॥ श्री गणेशाय नमः ॥", "॥ शुभ विवाह ॥", "॥ श्री गणेशाय नमः ॥ ॥ शुभ विवाह ॥", ["", "No blessing line"]])}
      ${p.music ? sel("music", "Music", ["Shehnai", "Soft instrumental", "Our own song (we'll send it)", "None"]) : `<p class="locked">${ic("music")} Background music or shehnai <span>Premium & Luxury · ${upsell("Premium")}</span></p>`}
      <div class="toggles">
        ${tog("gallery", "Photo gallery (send photos on WhatsApp later)", p.gallery, `Premium & Luxury · ${upsell("Premium")}`)}
        ${tog("rsvp", "Collect RSVPs", p.rsvp, `Premium & Luxury · ${upsell("Premium")}`)}
        ${p.rsvp ? tog("guests", "Ask for guest count") : ""}
        ${p.rsvp ? tog("meal", "Ask for meal preference") : ""}</div>
      ${p.rsvp ? f("rsvp_by", "RSVP deadline", 'type="date"') : ""}
      ${p.colours ? f("colours", "Colour preferences", 'placeholder="e.g. maroon and gold, or match the lehenga"') : `<p class="locked">${ic("sliders")} Custom colours & motifs <span>Luxury · ${upsell("Luxury")}</span></p>`}
      ${p.story ? `<div class="field"><label for="f-story">Family story / video page</label><textarea id="f-story" name="story" placeholder="How you met, family history, or a video link">${esc(D.story || "")}</textarea></div>` : `<p class="locked">${ic("book")} Family story or video page <span>Luxury · ${upsell("Luxury")}</span></p>`}
      <div class="field"><label for="f-notes">Anything else?</label><textarea id="f-notes" name="notes" placeholder="Special rituals, how elders' names should be written, wording you like…">${esc(D.notes || "")}</textarea></div></div>`;
    }
    if (n === 4) {
      const i = inv(), pr = price(), half = Math.ceil(pr / 2);
      const rows = [["Design", `${i.name} (${i.tier} collection)`], ["Package", `${D.package} · ready in ${P().days} hours`], ["Couple", [D.bride, D.groom].filter(Boolean).join(" & ") || "—"], ["Wedding date", fmtDate(D.wedding_date) || "—"],
        ["Families", [D.bride_family, D.groom_family].filter(Boolean).join(" · ") || "—"], ["Blessings", D.blessings || "—"], ["Language", D.language],
        ["Functions", D.events.map((e) => `<b>${esc(evName(e))}</b>${e.date ? " · " + esc(fmtDate(e.date)) : ""}${e.time ? " · " + esc(e.time) : ""}${e.venue ? "<br><span class='muted'>" + esc(e.venue) + "</span>" : ""}`).join("<br>")],
        ["Extras", [P().music && D.music && D.music !== "None" && D.music, P().gallery && D.gallery && "Photo gallery", P().rsvp && D.rsvp && "RSVP", P().colours && D.colours && "Custom colours", P().story && D.story && "Family story"].filter(Boolean).join(" · ") || "—"]];
      return `<div class="review-box"><dl class="rv">${rows.map(([k, v]) => `<dt>${k}</dt><dd>${k === "Functions" ? v : esc(v)}</dd>`).join("")}</dl>
        <button type="button" class="linkbtn" data-goto="1">Edit names</button> · <button type="button" class="linkbtn" data-goto="2">Edit functions</button></div>
      <div class="price-box"><div><span class="muted">Estimated price</span><b>${inr(pr)}</b></div><div><span class="muted">Advance (50%)</span><b>${inr(half)}</b></div><div><span class="muted">After approval</span><b>${inr(pr - half)}</b></div></div>
      <p class="muted" style="font-size:13.5px;margin-top:8px">Nothing is charged online. We confirm the final price with you on WhatsApp first.</p>
      <div class="form" style="margin-top:18px"><div class="f2">${f("contact_name", "Your name <span class='req'>*</span>", 'required autocomplete="name"', D.contact_name || displayName())}${f("phone", "WhatsApp number <span class='req'>*</span>", 'type="tel" required inputmode="tel" autocomplete="tel"')}</div>
        ${f("email", "Email", 'type="email" autocomplete="email"', D.email || user()?.email)}
        <label class="check"><input type="checkbox" name="verified" required ${D.verified ? "checked" : ""}> I have checked every name, date and venue above.</label></div>
      <div class="d-actions" style="margin-top:16px"><button type="button" class="btn btn-primary" id="submit-cz">Confirm &amp; send to BFI ${ic("arrow")}</button>
      <a class="btn btn-wa" id="wa-cz">${WA_SVG} Send on WhatsApp instead</a></div>
      <p style="margin-top:12px"><button type="button" class="linkbtn" id="save-cz">${user() ? "Save draft to my account" : "Login to save this draft"}</button> <span class="muted" style="font-size:13px">· Your progress is also saved on this device.</span></p>`;
    }
    return "";
  }
  function collect() {
    $$("[name]", form).forEach((el) => {
      if (el.type === "radio") { if (el.checked) D[el.name] = el.value; }
      else if (el.type === "checkbox") D[el.name] = el.checked;
      else D[el.name] = el.value.trim();
    });
    $$("#events .event").forEach((box) => { const e = D.events[+box.dataset.k]; $$("[data-ev]", box).forEach((el) => (e[el.dataset.ev] = el.value.trim())); });
    fixPkg(); save(); preview();
  }
  function draw() {
    const n = st.step;
    $("#stepper").innerHTML = steps.map((s, k) => `<button type="button" aria-label="Step ${k + 1}: ${s}" class="${k < n ? "done" : k === n ? "cur" : ""}" data-go="${k}" ${k === 5 ? "disabled" : ""}></button>`).join("");
    form.innerHTML = `<div class="step-title"><h2 style="font-size:28px">${steps[n]}</h2><small>Step ${n + 1} of ${steps.length}</small></div>${body(n)}
      <div class="cz-nav">${n ? `<button type="button" class="btn btn-ghost" data-back>${ic("left")} Back</button>` : "<span></span>"}${n < 4 ? `<button type="submit" class="btn btn-primary">Next ${ic("right")}</button>` : ""}</div>`;
    preview();
    if (n === 4) {
      const i = inv();
      $("#wa-cz").href = waHref(`Namaste BFI 🙏 We'd like the ${i.name} invitation (${D.package}).\nCouple: ${D.bride || "?"} & ${D.groom || "?"}\nWedding date: ${fmtDate(D.wedding_date) || "?"}\nFunctions: ${D.events.map((e) => `${evName(e)} ${e.date || ""} ${e.venue || ""}`.trim()).join("; ")}\nLanguage: ${D.language}.`);
      $("#wa-cz").target = "_blank";
      $("#submit-cz").onclick = submit;
      $("#save-cz").onclick = () => saveRemote();
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
    const btn = e.currentTarget; collect();
    for (const [k, s] of [["bride", 1], ["groom", 1], ["wedding_date", 1]]) if (!D[k]) { st.step = s; draw(); validate(form); return toast("Please fill in the required details"); }
    if (D.events.some((x) => !x.date)) { st.step = 2; draw(); validate(form); return toast("Please add a date for every function"); }
    if (!validate(form)) return toast(D.verified ? "Please add your name and WhatsApp number" : "Please confirm you've checked the details");
    if (!confirm(`Send ${D.bride} & ${D.groom}'s invitation details to BFI?\n\nWe'll message you on WhatsApp to confirm the price and the 50% advance. Nothing is charged now.`)) return;
    setBusy(btn, true, "Sending…");
    const pr = price();
    try {
      if (user()) await saveRemote("submitted");
      await sendEnquiry({ name: D.contact_name, phone: D.phone, email: D.email || null, wedding_date: D.wedding_date || mainEv().date || null, package: D.package, design_slug: D.design, source: "customize",
        message: `Package: ${D.package} (est. ₹${pr}). Couple: ${D.bride} & ${D.groom}. Parents: ${D.bride_family || "-"} / ${D.groom_family || "-"}. Blessings: ${D.blessings || "-"}. Language: ${D.language}. Functions: ${D.events.map((x) => `${evName(x)} ${x.date} ${x.time} @ ${x.venue} ${x.map} ${x.notes}`.replace(/\s+/g, " ").trim()).join("; ")}. Music: ${P().music ? D.music : "-"}. Gallery: ${P().gallery && D.gallery ? "yes" : "no"}. RSVP: ${P().rsvp && D.rsvp ? "yes" : "no"}. Colours: ${D.colours || "-"}. Story: ${D.story || "-"}. Notes: ${D.notes || "-"}`.slice(0, 2000) });
      track("customize_submit", { design: D.design, package: D.package, price: pr });
      localStorage.removeItem(CZ_KEY);
      st.step = 5;
      $("#stepper").innerHTML = steps.map((s, k) => `<button type="button" class="${k < 5 ? "done" : "cur"}" disabled aria-label="${s}"></button>`).join("");
      const half = Math.ceil(pr / 2);
      form.innerHTML = `<div class="step-title"><h2 style="font-size:28px">Confirmed: we've received your details</h2><small>Step 6 of 6</small></div>
        <div class="notice ok" style="font-size:16px"><b>Dhanyavaad, ${esc(D.contact_name)}!</b> ${esc(D.bride)} &amp; ${esc(D.groom)}'s ${esc(inv().name)} invitation (${D.package}) is with our designers.</div>
        <ol class="next-steps">
          <li><b>We message you on WhatsApp</b> within an hour (10am–8pm) to confirm the design, package and final price.</li>
          <li><b>You pay the 50% advance</b> (about ${inr(half)}) by UPI or bank transfer.</li>
          <li><b>We prepare your invitation</b>: ready in ${P().days} hours once we have all details and the advance.</li>
          <li><b>You review the preview</b> on your phone. One round of changes is included; spelling fixes are always free.</li>
          <li><b>You pay the remaining 50%</b> after you approve.</li>
          <li><b>You receive your link, QR code and a ready-to-forward WhatsApp message.</b></li></ol>
        <div class="row" style="margin-top:18px"><a class="btn btn-wa" data-wa="${esc(waText(inv().name))}">${WA_SVG} Chat on WhatsApp</a>${user() ? '<a class="btn btn-ghost" href="account.html">Go to my account</a>' : ""}</div>`;
      initChrome();
    } catch { setBusy(btn, false); toast("Couldn't send. Please try again or send on WhatsApp."); }
  }
  form.addEventListener("submit", (e) => { e.preventDefault(); collect(); if (!validate(form)) return; st.step++; save(); draw(); form.scrollIntoView({ block: "start" }); if (st.step === 1) track("customize_start", { design: D.design, package: D.package }); });
  form.addEventListener("input", collect);
  form.addEventListener("change", (e) => { collect(); if (e.target.name === "design" || e.target.name === "package" || e.target.dataset.ev === "type") draw(); });
  form.addEventListener("click", (e) => {
    if (e.target.closest("[data-back]")) { collect(); st.step--; save(); draw(); }
    const g = e.target.closest("[data-goto]"); if (g) { collect(); st.step = +g.dataset.goto; save(); draw(); }
    const up = e.target.closest("[data-upgrade]"); if (up) { collect(); D.package = up.dataset.upgrade; save(); draw(); toast(`Switched to ${D.package}`); }
    if (e.target.closest("#add-ev")) { collect(); if (D.events.length < P().events) D.events.push({ type: "Reception", name: "", date: "", time: "", venue: "", map: "", notes: "" }); draw(); }
    const rm = e.target.closest("[data-rm]"); if (rm) { collect(); D.events.splice(+rm.dataset.rm, 1); draw(); }
    const mv = e.target.closest("[data-mv]"); if (mv) { collect(); const [k, d] = mv.dataset.mv.split(":").map(Number); const j = k + d; if (j >= 0 && j < D.events.length) { [D.events[k], D.events[j]] = [D.events[j], D.events[k]]; save(); draw(); } }
  });
  $("#stepper").addEventListener("click", (e) => { const b = e.target.closest("[data-go]"); if (b && +b.dataset.go <= st.step && st.step < 5) { collect(); st.step = +b.dataset.go; draw(); } });
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
      track("contact_submit", { package: d.package || "Not sure" });
      const waMsg = `Namaste BFI 🙏 I just sent an enquiry on your website.\nName: ${d.name}\nWedding date: ${d.wedding_date || "not fixed"}\nCity: ${d.city || "-"}\nPackage: ${d.package || "Not sure"}\n${d.message || ""}`;
      form.outerHTML = `<div class="notice ok" style="font-size:16px"><b>Dhanyavaad, ${esc(d.name)}!</b> Your enquiry has reached us. We'll reply on WhatsApp within an hour (${esc(CFG.hours)}).</div>
        <p style="margin-top:14px">Want a faster reply? Send the same details on WhatsApp:</p><a class="btn btn-wa" style="margin-top:10px" target="_blank" rel="noopener" href="${waHref(waMsg)}">${WA_SVG} Send on WhatsApp</a>`;
    } catch { setBusy(btn, false); $("#c-status").innerHTML = `<div class="notice bad">Couldn't send your message. Please try again, or message us on WhatsApp.</div>`; }
  });
};

/* ---------- partners (planners, photographers, venues) ---------- */
pages.partners = async () => {
  const form = $("#partner-form");
  form.addEventListener("submit", async (e) => {
    e.preventDefault(); if (!validate(form)) return;
    const d = formData(form); if (d.company) return;
    const btn = $("button[type=submit]", form); setBusy(btn, true, "Sending…");
    try {
      await sendEnquiry({ name: d.name, phone: d.phone, email: d.email || null, city: d.city || null, source: "partner",
        message: `PARTNER APPLICATION · ${d.type} · ${d.business}${d.city ? " · " + d.city : ""}. ${d.message || ""}`.slice(0, 2000) });
      track("partner_apply", { type: d.type });
      form.outerHTML = `<div class="notice ok" style="font-size:16px"><b>Thank you, ${esc(d.name)}!</b> We've received ${esc(d.business)}'s application and will message you on WhatsApp.</div>`;
    } catch { setBusy(btn, false); $("#p-status").innerHTML = `<div class="notice bad">Couldn't send. Please try again or message us on WhatsApp.</div>`; }
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

/* ---------- sample content for each demo design (fictional families) ---------- */
const DEMO_CONTENT = {
  "rajwada-royale": { a: "Priya", b: "Rohan", city: "Jaipur", line: "॥ शुभ विवाह ॥", coverLine: "॥ श्री गणेशाय नमः ॥",
    h: { bless: "With the blessings of our elders", story: "Our story", count: "Counting down to the wedding", events: "Wedding celebrations", venue: "The royal venue", rsvp: "Will you join us?", wishes: "Blessings & wishes" },
    elders: ["Smt. Kamla Devi & Late Shri Ramniwas Agarwal", "Smt. Shanti Devi & Shri Gopal Maheshwari"],
    aFam: "D/o Smt. Sunita & Shri Mahesh Agarwal, Jaipur", bFam: "S/o Smt. Rekha & Shri Anil Maheshwari, Jodhpur",
    story: [["2023 · Jodhpur", "We met at a cousin's sangeet", "One dance, one long walk along the fort walls, and a lot of chai."], ["2025 · Udaipur", "The question by the lake", "Rohan asked; Priya said yes before he finished."], ["This winter · Jaipur", "Now, forever", "Our families are coming together. We'd love you to be there."]],
    events: [[56, "Ganesh Puja", "10:00", "Agarwal Niwas, C-Scheme, Jaipur", "Family only", [["#F2C230", "Yellow"], ["#E86A2C", "Orange"]]], [57, "Mayra", "11:00", "Agarwal Niwas, C-Scheme, Jaipur", "Traditional", [["#B0122C", "Red"], ["#C6A15B", "Gold"]]], [58, "Pithi & Mehendi", "16:00", "The Heritage Lawns, Jaipur", "Leheriya & florals", [["#F7D84A", "Yellow"], ["#3E9B5B", "Green"]]], [59, "Mahila Sangeet", "19:30", "The Heritage Lawns, Jaipur", "Indo-western glam", [["#D8457A", "Pink"], ["#7B3FA0", "Purple"]]], [60, "Baraat & Phere", "19:30", "Royal Palace Gardens, Jaipur", "Royal traditional", [["#641E2B", "Maroon"], ["#F3E3C3", "Ivory"]]], [61, "Reception", "20:00", "Royal Palace Gardens, Jaipur", "Formal: sherwani & saree", [["#1B2A4A", "Navy"], ["#C6A15B", "Gold"]]]],
    venue: ["Royal Palace Gardens", "Amer Road, Jaipur, Rajasthan", "Amer Road, Jaipur"], stay: "Rooms are booked for outstation guests near Amer. Message the family for details.", rsvp: "Please let us know by one week before the wedding.",
    wishes: [["Nani", "Sada sukhi raho, mere bachchon. Bahut saara aashirwad."], ["Ankit & Shruti", "Can't wait to dance at the sangeet! Love you both."]] },
  "gulmohar-classic": { a: "Ananya", b: "Vikram", city: "Bikaner", line: "॥ श्री गणेशाय नमः ॥", coverLine: "॥ शुभ विवाह ॥", weds: "sang",
    h: { bless: "Aashirwad of our elders", story: "From neighbours to forever", count: "Days to the shubh muhurat", events: "Rasmein & functions", venue: "Shaadi ka sthaan", rsvp: "Kindly confirm your presence", wishes: "Your aashirwad" },
    elders: ["Smt. Bhanwari Devi & Shri Mohanlal Goyal", "Smt. Saraswati Devi & Late Shri Ramdev Khandelwal"],
    aFam: "D/o Smt. Kiran & Shri Suresh Goyal, Bikaner", bFam: "S/o Smt. Lata & Shri Rajendra Khandelwal, Bikaner",
    story: [["Childhood · Rampuria lane", "Two houses, one gali", "We grew up sharing bhujia, kites and terrace Diwalis."], ["Gangaur 2024", "A fair, a question", "Vikram proposed between the swings at the Gangaur mela."], ["This Akshaya Tritiya", "Gathbandhan", "Our families finally fixed the muhurat. Please come."]], pics: [2, 0, 1],
    events: [[55, "Vinayak Sthapna", "09:30", "Goyal Haveli, Rampuria, Bikaner", "Traditional", [["#E36414", "Saffron"], ["#F7D84A", "Yellow"]]], [57, "Mayra", "12:00", "Goyal Haveli, Rampuria, Bikaner", "Bandhej & safa", [["#B0122C", "Red"], ["#2E7D32", "Green"]]], [58, "Pithi Dastoor", "10:00", "Goyal Haveli, Rampuria, Bikaner", "Yellow & white", [["#F7D84A", "Yellow"], ["#FFFFFF", "White"]]], [59, "Mehendi & Geet", "17:00", "Laxmi Niwas Lawns, Bikaner", "Leheriya", [["#3E9B5B", "Green"], ["#E36414", "Orange"]]], [60, "Phere", "21:00", "Laxmi Niwas Lawns, Bikaner", "Poshak & achkan", [["#A4272F", "Red"], ["#C6A15B", "Gold"]]]],
    venue: ["Laxmi Niwas Lawns", "Lalgarh area, Bikaner, Rajasthan", "Lalgarh, Bikaner"], stay: "Dharamshala rooms are reserved near Junagarh for our guests.", rsvp: "Please reply by Akhatij so we can arrange your stay.",
    wishes: [["Bua ji", "Mhari laadli ne ghani ghani badhai! Khush raho sada."], ["Tanmay", "Finally! The gali's longest love story gets its happy ending."]] },
  "gulabi-bagh": { a: "Meera", b: "Arjun", city: "Udaipur", line: "✿ with love ✿", coverLine: "॥ शुभ विवाह ॥",
    h: { bless: "With love from our families", story: "Our little love story", count: "Until we say forever", events: "The celebrations", venue: "Where we'll be", rsvp: "Save us a dance?", wishes: "Leave us some love" },
    elders: ["Smt. Pushpa & Shri Hari Prasad Bansal", "Smt. Usha & Shri Om Prakash Singhal"],
    aFam: "D/o Smt. Neelam & Shri Ashok Bansal, Udaipur", bFam: "S/o Smt. Anita & Shri Vinod Singhal, Ahmedabad",
    story: [["Spring 2022 · Udaipur", "A friend's mehendi", "Arjun spilled kesar thandai on Meera's dupatta. She forgave him."], ["2024 · Lake Pichola", "Coffee became sunsets", "Every weekend, the same ghat, the same corner table."], ["This Basant Panchami", "Blossoming into forever", "Join us as two families become one garden."]], pics: [1, 0, 2],
    events: [[57, "Haldi in the garden", "11:00", "Bansal Bagh, Fatehpura, Udaipur", "Pastel yellow", [["#FFE8A3", "Butter"], ["#F8C8D4", "Blush"]]], [58, "Mehendi & high tea", "16:00", "Bansal Bagh, Fatehpura, Udaipur", "Florals", [["#F3B6C6", "Pink"], ["#BFE3C9", "Mint"]]], [59, "Sangeet under the stars", "19:30", "Lakeview Terrace, Udaipur", "Shimmer & sequins", [["#E7A6B4", "Rose"], ["#C9A15B", "Gold"]]], [60, "Phere by the lake", "18:00", "Lakeview Terrace, Udaipur", "Blush & ivory", [["#F8D7DE", "Blush"], ["#FFF8EC", "Ivory"]]]],
    venue: ["Lakeview Terrace", "Lake Pichola, Udaipur, Rajasthan", "Lake Pichola, Udaipur"], stay: "We've reserved lake-facing rooms in the old city for our guests.", rsvp: "Please let us know by the end of this month. Pretty please.",
    wishes: [["Mausi", "Meera beta, tum dono ki jodi gulab jaisi hai. Bahut pyaar."], ["The college gang", "From canteen chai to mandap! So proud of you two."]] },
  "mor-pankh": { a: "Kavya", b: "Siddharth", city: "Jaipur", line: "॥ मंगलम् ॥", coverLine: "॥ श्री गणेशाय नमः ॥",
    h: { bless: "Blessed by our families", story: "Chapter by chapter", count: "The countdown is on", events: "The weekend", venue: "Find us here", rsvp: "RSVP", wishes: "Guestbook" },
    elders: ["Smt. Sushila & Shri Ramesh Chandra Mittal", "Smt. Kaushalya & Shri Banwarilal Jindal"],
    aFam: "D/o Smt. Rachna & Shri Pradeep Mittal, Mumbai", bFam: "S/o Smt. Seema & Shri Naresh Jindal, Jaipur",
    story: [["2019 · Pune", "Same college, different hostels", "A group project, three all-nighters and one shared Maggi."], ["2023 · Bengaluru", "Co-founders first", "We built a startup together. Then we built a life."], ["2025 · Jawai", "A leopard, a sunset, a ring", "Siddharth proposed on a safari. The leopard approved."]], pics: [0, 2, 1],
    events: [[58, "Welcome brunch", "12:00", "The Courtyard Hotel, Jaipur", "Smart casuals", [["#0E7C72", "Teal"], ["#F5F5F0", "White"]]], [59, "Mehendi & cocktails", "17:00", "The Courtyard Hotel, Jaipur", "Peacock tones", [["#14473F", "Emerald"], ["#4FC3B4", "Teal"]]], [60, "Baraat & Phere", "18:30", "Garden Pavilion, Jaipur", "Indian festive", [["#D9B86A", "Gold"], ["#0B2420", "Bottle green"]]], [61, "After-party", "21:30", "Rooftop Lounge, Jaipur", "Black tie", [["#111111", "Black"], ["#D9B86A", "Gold"]]]],
    venue: ["Garden Pavilion", "Tonk Road, Jaipur, Rajasthan", "Tonk Road, Jaipur"], stay: "Airport pickups and rooms are arranged for flying-in guests.", rsvp: "Kindly RSVP by the 15th so we can plan your stay.",
    wishes: [["Team Startup", "Best merger we've ever seen. Congratulations!"], ["Dadi", "Dono khush raho, aur jaldi se Jaipur aao."]] },
  "neel-mahal": { a: "Riya", b: "Kunal", city: "Jodhpur", line: "॥ शुभ विवाह ॥", coverLine: "॥ श्री गणेशाय नमः ॥",
    h: { bless: "Under our elders' blessings", story: "Written in the stars", count: "Nights to go", events: "Evenings to remember", venue: "In the Blue City", rsvp: "Will you light up our night?", wishes: "Send a star our way" },
    elders: ["Smt. Gyarsi Devi & Shri Rameshwar Somani", "Smt. Kesar Devi & Late Shri Jethmal Daga"],
    aFam: "D/o Smt. Mamta & Shri Dinesh Somani, Jodhpur", bFam: "S/o Smt. Kavita & Shri Sunil Daga, Surat",
    story: [["2021 · Sam dunes", "A desert camp, a meteor shower", "Strangers at a bonfire, wishing on the same shooting star."], ["2023 · Mehrangarh", "Midnight letters", "Two years of long-distance calls under the same moon."], ["This winter · Jodhpur", "Our forever night", "Join us for evenings of music, lights and blessings."]], pics: [0, 1, 2],
    events: [[58, "Mehendi night", "19:00", "Neel Bagh, Jodhpur", "Indigo & silver", [["#1C2D63", "Indigo"], ["#C0C7D6", "Silver"]]], [59, "Sangeet under the stars", "20:00", "Neel Bagh, Jodhpur", "Sequins", [["#0B1736", "Midnight"], ["#F2D58A", "Gold"]]], [60, "Phere at moonrise", "21:30", "Blue City Palace Lawns, Jodhpur", "Royal traditional", [["#8B1E2D", "Red"], ["#F2D58A", "Gold"]]], [61, "Reception", "20:00", "Blue City Palace Lawns, Jodhpur", "Black tie", [["#111111", "Black"], ["#EAF0FF", "Pearl"]]]],
    venue: ["Blue City Palace Lawns", "Below Mehrangarh, Jodhpur, Rajasthan", "Mehrangarh, Jodhpur"], stay: "Rooms with fort views are held for you in the old city.", rsvp: "Let us know by the next full moon.",
    wishes: [["Chachi", "Tum dono ki jodi chaand-sitaron jaisi chamke!"], ["Neha", "Saving my best dance for the sangeet night!"]] },
  "gajraj-swagat": { a: "Pooja", b: "Rahul", city: "Kolkata", line: "॥ श्री गणेशाय नमः ॥", coverLine: "॥ श्री गणेशाय नमः ॥", weds: "संग",
    h: { bless: "Padharo mhare des", story: "Do parivaar, ek kahani", count: "Shubh din aane mein", events: "Rasmon ka utsav", venue: "Vivah sthal", rsvp: "Aapki upasthiti prarthaniya hai", wishes: "Shubhkamnayein" },
    elders: ["Smt. Gulab Devi & Shri Bhagwandas Lohia", "Smt. Prem Devi & Shri Ghanshyam Das Bajaj"],
    aFam: "D/o Smt. Sangeeta & Shri Vinod Lohia, Kolkata", bFam: "S/o Smt. Madhu & Shri Kailash Bajaj, Kolkata",
    story: [["Generations ago · Fatehpur", "Families from Shekhawati", "Our grandfathers left Fatehpur for Calcutta in the same year."], ["Durga Puja 2023", "A pandal, a meeting", "Our mothers planned it. We pretended not to notice."], ["This Dev Uthani Ekadashi", "The elephants are coming", "Gaje-baje ke saath, please join the baraat!"]], pics: [2, 1, 0],
    events: [[54, "Ganesh Sthapna", "10:00", "Lohia Bhawan, Alipore, Kolkata", "Traditional", [["#E98A15", "Saffron"], ["#B5541C", "Rust"]]], [56, "Mayra", "11:00", "Lohia Bhawan, Alipore, Kolkata", "Bandhej & safa", [["#C2185B", "Rani pink"], ["#E98A15", "Orange"]]], [57, "Haldi & Mehendi", "15:00", "Rajasthan Club Lawns, Kolkata", "Leheriya", [["#F7D84A", "Yellow"], ["#3E9B5B", "Green"]]], [58, "Mahila Geet", "19:00", "Rajasthan Club Lawns, Kolkata", "Gota-patti", [["#E36414", "Orange"], ["#C6A15B", "Gold"]]], [60, "Baraat with Gajraj", "18:00", "Marwari Bhawan, Ballygunge, Kolkata", "Poshak & achkan", [["#B5541C", "Saffron"], ["#7A2E0E", "Maroon"]]]],
    venue: ["Marwari Bhawan", "Ballygunge, Kolkata, West Bengal", "Ballygunge, Kolkata"], stay: "Guests from Rajasthan: rooms are arranged near Burrabazar.", rsvp: "Kripya do din pehle soochit karein.",
    wishes: [["Dadaji", "Ghano aashirwad, mhara laadla. Sukhi raho."], ["Cousins of Fatehpur", "Gajraj ready hai, baraat ready hai, hum ready hain!"]] },
  "sheesh-mahal": { a: "Nandini", b: "Aditya", city: "Samode", line: "✦ शुभ विवाह ✦", coverLine: "॥ श्री गणेशाय नमः ॥",
    h: { bless: "With the grace of our elders", story: "A story in a thousand mirrors", count: "The grand day draws near", events: "A royal weekend", venue: "The palace", rsvp: "Kindly reply", wishes: "Words of blessing" },
    elders: ["Smt. Rajrani & Shri Gopikishan Poddar", "Smt. Vimla & Late Shri Shyamsundar Ruia"],
    aFam: "D/o Smt. Shobha & Shri Arun Poddar, Mumbai", bFam: "S/o Smt. Rekha & Shri Manoj Ruia, Delhi",
    story: [["2020 · A family wedding", "Across a mirrored hall", "We first saw each other reflected in the walls of a sheesh mahal."], ["2024 · London", "The ring at midnight", "Aditya proposed on a bridge, in the rain, with a jasmine garland."], ["This season · Samode", "Our grand celebration", "Three days of music, feasts and festivities. Be our guest."]], pics: [2, 1, 0],
    events: [[58, "Royal welcome & haldi", "11:00", "Palace Courtyard, Samode", "Yellow & gold", [["#F5D27A", "Gold"], ["#F7D84A", "Yellow"]]], [58, "Mehendi in the Diwan-e-Khas", "17:00", "Palace Courtyard, Samode", "Mirrorwork", [["#7A1219", "Ruby"], ["#C0C7D6", "Silver"]]], [59, "Sangeet at the Sheesh Mahal", "20:00", "Mirror Hall, Samode", "Sparkle", [["#5A0B12", "Wine"], ["#F5D27A", "Gold"]]], [60, "Baraat & Phere", "17:30", "Palace Lawns, Samode", "Royal Rajputana", [["#A4272F", "Red"], ["#F5D27A", "Gold"]]], [61, "Farewell brunch", "11:00", "Palace Lawns, Samode", "Pastels", [["#F8D7DE", "Blush"], ["#BFE3C9", "Mint"]]]],
    venue: ["Palace Lawns", "Samode, near Jaipur, Rajasthan", "Samode, Rajasthan"], stay: "The palace is reserved for all three nights. Transfers from Jaipur airport are arranged.", rsvp: "Please reply three weeks ahead so we can reserve your suite.",
    wishes: [["Maasi", "Itni roshni tumhari zindagi mein bhi rahe. Ashirwad."], ["Kabir", "The wedding of the year! Bringing my best sherwani."]] },
  "chhatri": { a: "Isha", b: "Varun", city: "Mandawa", line: "॥ शुभ विवाह ॥", coverLine: "॥ ॐ ॥",
    h: { bless: "With gratitude", story: "Briefly, us", count: "Until then", events: "The day", venue: "The place", rsvp: "Respond", wishes: "Notes" },
    elders: ["Smt. Savitri & Shri Hanuman Prasad Kedia", "Smt. Leela & Shri Girdhari Lal Jhunjhunwala"],
    aFam: "D/o Smt. Asha & Shri Pawan Kedia", bFam: "S/o Smt. Nirmala & Shri Sanjay Jhunjhunwala",
    story: [["2018", "Met", "At an architecture workshop in Mandawa."], ["2022", "Built", "A small studio, a slow life, many sketches."], ["Now", "Promised", "A quiet ceremony with the people we love."]], pics: [2, 0, 1],
    events: [[59, "Haldi", "10:00", "Kedia Haveli, Mandawa", "White", [["#FFFFFF", "White"], ["#E6D7B5", "Sand"]]], [60, "Phere", "11:30", "Kedia Haveli courtyard, Mandawa", "Ivory & gold", [["#FFF8EC", "Ivory"], ["#B8975A", "Gold"]]], [60, "Lunch", "13:30", "Kedia Haveli, Mandawa", "As you like", [["#E6D7B5", "Sand"], ["#7A7065", "Stone"]]]],
    venue: ["Kedia Haveli", "Mandawa, Shekhawati, Rajasthan", "Mandawa, Rajasthan"], stay: "An intimate wedding; we'll share stay details personally.", rsvp: "A small gathering. Please reply soon.",
    wishes: [["Ma", "Simple, beautiful, yours. Bless you both."], ["Arjun", "Quietly the best wedding we'll attend."]] },
};

/* ---------- live demo invitation ---------- */
pages.demo = async () => {
  const all = await invitations();
  const inv = all.find((i) => i.slug === params.get("design")) || all.find((i) => i.slug === "rajwada-royale") || all[0];
  const day = (n) => { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() + n); return d; };
  const wedding = day(60); wedding.setHours(19, 30);
  const fmt = (d) => d.toLocaleDateString("en-IN", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
  $("#demo-cta").href = $("#demo-cta2").href = `customize.html?design=${inv.slug}`;

  // ---- each design has its own theme, opening animation and floating effect ----
  const TH = {
    "rajwada-royale": { intro: "doors", fx: "gold", btn: "Open the palace doors", tone: 146.83 },
    "gulmohar-classic": { intro: "envelope", fx: "petals", btn: "Tap the seal to open", tone: 164.81 },
    "gulabi-bagh": { intro: "bloom", fx: "pink", btn: "Open with love", tone: 174.61 },
    "mor-pankh": { intro: "feather", fx: "feathers", btn: "Open invitation", tone: 155.56 },
    "neel-mahal": { intro: "stars", fx: "stars", btn: "Step into the night", tone: 130.81 },
    "gajraj-swagat": { intro: "curtain", fx: "marigold", btn: "Lift the toran", tone: 196 },
    "sheesh-mahal": { intro: "tiles", fx: "glitter", btn: "Enter the Sheesh Mahal", tone: 138.59 },
    "chhatri": { intro: "line", fx: "dust", btn: "Open invitation", tone: 220 },
  };
  const th = TH[inv.slug] || TH["rajwada-royale"];

  // ---- each design tells its own sample story, in its own fonts ----
  const FONTS = {
    "rajwada-royale": ["Cinzel:wght@500;700&family=Pinyon+Script&family=Lora:wght@400;500;600", "'Cinzel',serif", "26px", "normal", 700, "none", ".04em", "'Pinyon Script',cursive", "44px", "'Lora',serif"],
    "gulmohar-classic": ["Rozha+One&family=Yatra+One&family=Poppins:wght@400;500;600", "'Rozha One',serif", "32px", "normal", 400, "none", "0", "'Yatra One',cursive", "36px", "'Poppins',sans-serif"],
    "gulabi-bagh": ["Parisienne&family=Josefin+Sans:wght@400;600", "'Parisienne',cursive", "42px", "normal", 400, "none", "0", "'Parisienne',cursive", "46px", "'Josefin Sans',sans-serif"],
    "mor-pankh": ["Marcellus&family=Alex+Brush&family=Mulish:wght@400;600", "'Marcellus',serif", "30px", "normal", 400, "none", ".02em", "'Alex Brush',cursive", "48px", "'Mulish',sans-serif"],
    "neel-mahal": ["Italiana&family=Great+Vibes&family=Raleway:wght@400;600", "'Italiana',serif", "34px", "normal", 400, "none", ".06em", "'Great Vibes',cursive", "48px", "'Raleway',sans-serif"],
    "gajraj-swagat": ["Amita:wght@400;700&family=Kaushan+Script&family=Hind:wght@400;500;600", "'Amita',serif", "30px", "normal", 700, "none", "0", "'Kaushan Script',cursive", "40px", "'Hind',sans-serif"],
    "sheesh-mahal": ["Cinzel+Decorative:wght@700&family=Tangerine:wght@700&family=Cormorant+Garamond:wght@500;600", "'Cinzel Decorative',serif", "24px", "normal", 700, "none", ".02em", "'Tangerine',cursive", "60px", "'Cormorant Garamond',serif"],
    "chhatri": ["Josefin+Sans:wght@300;400;600&family=Italiana&family=Jost:wght@300;400;500", "'Josefin Sans',sans-serif", "15px", "normal", 300, "uppercase", ".32em", "'Italiana',serif", "40px", "'Jost',sans-serif"],
  }[inv.slug];
  if (FONTS) {
    const l = document.createElement("link"); l.rel = "stylesheet"; l.href = `https://fonts.googleapis.com/css2?family=${FONTS[0]}&display=swap`; document.head.append(l);
    const st = document.body.style; [["--dv-hf", 1], ["--dv-hs", 2], ["--dv-hst", 3], ["--dv-hw", 4], ["--dv-ht", 5], ["--dv-hls", 6], ["--dv-nf", 7], ["--dv-ns", 8], ["--dv-bf", 9]].forEach(([k, i]) => st.setProperty(k, FONTS[i]));
  }
  const C = DEMO_CONTENT[inv.slug] || DEMO_CONTENT["rajwada-royale"];
  const H = C.h;
  $$("[data-h]").forEach((h) => { if (H[h.dataset.h]) h.textContent = H[h.dataset.h]; });
  $("#dv-bless-line").textContent = C.line;
  $("#dv-elders").innerHTML = C.elders.map(esc).join("<br>");
  $("#dv-fam").innerHTML = `<div><b>${esc(C.a)}</b><span>${esc(C.aFam)}</span></div><div class="dv-weds">${esc(C.weds || "weds")}</div><div><b>${esc(C.b)}</b><span>${esc(C.bFam)}</span></div>`;
  const pics = [["demo-fort.jpg", "Illustration of a couple on a fort rampart"], ["demo-lake.jpg", "Illustration of a couple in a boat by a lake palace"], ["demo-rings.jpg", "Illustration of mehendi hands holding a ring box"]];
  const order = C.pics || [0, 1, 2];
  $("#dv-story-list").innerHTML = C.story.map(([when, title, text], k) => `<figure><img src="${IMG(pics[order[k]][0])}" alt="${pics[order[k]][1]}" loading="lazy"><figcaption><small>${esc(when)}</small><b>${esc(title)}</b><p>${esc(text)}</p></figcaption></figure>`).join("");
  $("#dv-venue").innerHTML = `<b>${esc(C.venue[0])}</b><br>${esc(C.venue[1])}`;
  $("#dv-map-frame").src = `https://maps.google.com/maps?q=${encodeURIComponent(C.venue[2] + ", India")}&z=14&hl=en&output=embed`;
  try {
    if (window.qrcode) { const q = qrcode(0, "M"); q.addData(location.origin + location.pathname + "?design=" + inv.slug); q.make();
      $("#dv-qr").innerHTML = q.createSvgTag({ cellSize: 5, margin: 2, scalable: true }); }
  } catch {}
  $("#dv-stay").textContent = C.stay;
  $("#dv-rsvp-note").textContent = C.rsvp;
  $("#wishes").innerHTML = C.wishes.map(([n, w]) => `<div class="wish"><b>${esc(n)}</b><p>${esc(w)}</p></div>`).join("");
  document.title = `Live Demo: ${C.a} & ${C.b} in ${inv.name} · BFI`;
  $("#dv-card").innerHTML = `<img src="${IMG(inv.image)}" alt="${esc(inv.name)} invitation cover">` + inviteText(inv.slug, { a: C.a, b: C.b, blessing: C.coverLine, date: fmt(wedding), venue: C.venue[0] + ", " + C.city });
  document.body.dataset.theme = inv.slug;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fxBox = $("#petals");
  const spawn = (n, burst) => {
    if (reduce) return;
    for (let k = 0; k < n; k++) {
      const p = document.createElement("i"); p.className = "pt pt-" + th.fx;
      p.style.left = Math.random() * 100 + "vw"; p.style.setProperty("--dx", (Math.random() * 160 - 80) + "px");
      if (th.fx === "stars") { p.style.top = Math.random() * 100 + "vh"; p.style.animationDelay = Math.random() * 3 + "s"; }
      else p.style.animationDelay = (burst ? Math.random() * 1.5 : Math.random() * 3) + "s";
      p.style.animationDuration = (th.fx === "gold" || th.fx === "dust" ? 7 : th.fx === "stars" ? 2.5 : 6) + Math.random() * 5 + "s";
      fxBox.append(p); setTimeout(() => p.remove(), 16000);
    }
  };
  const ambient = () => { spawn(th.fx === "stars" ? 30 : 26, true); if (!reduce) setInterval(() => !document.hidden && spawn(3), 2600); };
  const names = `<p class="in-names">${esc(C.a)} <span>&amp;</span> ${esc(C.b)}</p>`;
  const btn = `<button class="in-btn" type="button">${th.btn}</button>`;
  const img = `url("${IMG(inv.image)}")`;
  const markup = {
    doors: `<div class="in-doors"><div class="door l" style="background-image:${img}"></div><div class="door r" style="background-image:${img}"></div><div class="in-mid">${names}${btn}</div></div>`,
    envelope: `<div class="env"><div class="env-box"><p class="env-names">${esc(C.a)} &amp; ${esc(C.b)}</p><div class="env-body"></div><div class="env-card" style="background-image:${img}"></div><div class="env-flap"></div><button class="env-seal in-btn" aria-label="Open the invitation">${esc(C.a[0])}&amp;${esc(C.b[0])}</button><p class="env-hint">Tap the seal to open</p></div></div>`,
    bloom: `<div class="in-bloom"><div class="bloom-ring"></div><div class="in-mid">${names}<p class="in-sub">A celebration of love</p>${btn}</div></div>`,
    feather: `<div class="in-feather"><div class="big-feather"></div><div class="in-mid">${names}${btn}</div></div>`,
    stars: `<div class="in-stars">${Array.from({ length: 70 }, () => `<i style="left:${Math.random() * 100}%;top:${Math.random() * 100}%;animation-delay:${(Math.random() * 3).toFixed(2)}s"></i>`).join("")}<div class="moon"></div><div class="in-mid">${names}<p class="in-sub">under the moonlit sky</p>${btn}</div></div>`,
    curtain: `<div class="in-curtain">${Array.from({ length: 16 }, (_, k) => `<span style="animation-delay:${(Math.abs(7.5 - k) * 0.05).toFixed(2)}s;transition-delay:${(Math.abs(7.5 - k) * 0.04).toFixed(2)}s"></span>`).join("")}<div class="in-mid">${names}${btn}</div></div>`,
    tiles: `<div class="in-tiles"><div class="tile-grid">${Array.from({ length: 96 }, () => `<span style="transition-delay:${(Math.random() * 0.7).toFixed(2)}s"></span>`).join("")}</div><div class="in-mid">${names}${btn}</div></div>`,
    line: `<div class="in-line"><svg viewBox="0 0 200 220" aria-hidden="true"><path d="M30 210 V120 Q30 60 100 40 Q170 60 170 120 V210 M50 210 V125 Q50 80 100 64 Q150 80 150 125 V210 M20 210 H180 M100 40 V22 M92 26 H108 M60 118 H140" /></svg><div class="in-mid">${names}${btn}</div></div>`,
  };
  const host = $("#intro");
  host.innerHTML = `<div class="intro intro-${th.intro}" role="dialog" aria-label="Open the invitation">${markup[th.intro]}</div>`;
  const ov = host.firstElementChild;
  const open = () => {
    if (ov.classList.contains("open")) return;
    ov.classList.add("open");
    setTimeout(() => { ov.classList.add("gone"); ambient(); }, th.intro === "tiles" ? 1300 : 1000);
    setTimeout(() => host.remove(), 2400);
  };
  $$(".in-btn", ov).forEach((b) => (b.onclick = open));
  if (params.get("open") === "1") open();
  const petals = (n) => spawn(n, true);

  // gentle music: a soft tanpura-like drone made in the browser (real invitations use your chosen track)
  let ctx, nodes = [];
  $("#music").onclick = (e) => {
    const btn = e.currentTarget, on = btn.getAttribute("aria-pressed") !== "true";
    btn.setAttribute("aria-pressed", on); btn.setAttribute("aria-label", on ? "Pause music" : "Play music");
    if (!on) { nodes.forEach((n) => { try { n.stop(); } catch {} }); nodes = []; return; }
    ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
    const gain = ctx.createGain(); gain.gain.value = 0.05; gain.connect(ctx.destination);
    const base = th.tone; [base, base * 1.5, base * 2, base * 2.0045].forEach((f, k) => {
      const o = ctx.createOscillator(); o.type = k % 2 ? "triangle" : "sine"; o.frequency.value = f;
      const lfo = ctx.createOscillator(), lg = ctx.createGain(); lfo.frequency.value = 0.15 + k * 0.07; lg.gain.value = 0.6; lfo.connect(lg); lg.connect(o.frequency);
      o.connect(gain); o.start(); lfo.start(); nodes.push(o, lfo);
    });
  };

  const tick = () => {
    let t = Math.max(0, wedding - new Date());
    const u = { d: 864e5, h: 36e5, m: 6e4, s: 1e3 };
    for (const k of ["d", "h", "m", "s"]) { const v = Math.floor(t / u[k]); t -= v * u[k]; $(`[data-u=${k}]`).textContent = v; }
  };
  tick(); setInterval(tick, 1000);

  const ev = C.events;
  const ics = (name, d, time, venue) => {
    const [hh, mm] = time.split(":"); const st = new Date(d); st.setHours(+hh, +mm); const en = new Date(st.getTime() + 3 * 36e5);
    const z = (x) => x.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
    const body = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//BFI//Invitation//EN", "BEGIN:VEVENT", `UID:${Date.now()}@bfi`, `DTSTAMP:${z(new Date())}`, `DTSTART:${z(st)}`, `DTEND:${z(en)}`, `SUMMARY:${name} · ${C.a} & ${C.b}`, `LOCATION:${venue}`, "END:VEVENT", "END:VCALENDAR"].join("\r\n");
    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([body], { type: "text/calendar" })); a.download = `${name.replace(/\W+/g, "-")}.ics`; a.click();
  };
  $("#dv-events").innerHTML = ev.map(([n, name, time, venue, dress, cols], k) => { const d = day(n); const t = new Date(d); t.setHours(+time.split(":")[0], +time.split(":")[1]);
    return `<div class="dv-ev"><div class="d"><b>${d.getDate()}</b><span>${d.toLocaleDateString("en-IN", { month: "short" })}</span></div>
    <div><h3>${name}</h3><p>${d.toLocaleDateString("en-IN", { weekday: "long" })} · ${t.toLocaleTimeString("en-IN", { hour: "numeric", minute: "2-digit" })}<br>${venue}</p>
    <div class="dress">Dress code: ${dress} ${cols.map(([c, l]) => `<i style="background:${c}" title="${l}"></i>`).join("")}</div>
    <div class="acts"><a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(venue)}" target="_blank" rel="noopener">Directions</a><button type="button" data-ics="${k}">Add to calendar</button></div></div></div>`; }).join("");
  $("#dv-events").addEventListener("click", (e) => { const b = e.target.closest("[data-ics]"); if (b) { const [n, name, time, venue] = ev[+b.dataset.ics]; ics(name, day(n), time, venue); } });

  $("#dv-designs").innerHTML = all.map((i) => `<a href="demo.html?design=${i.slug}" aria-current="${i.slug === inv.slug}"><img src="${IMG(i.image)}" alt="" loading="lazy">${esc(i.name)}</a>`).join("");
  $("#dv-rsvp").addEventListener("submit", (e) => {
    e.preventDefault(); if (!validate(e.target)) return;
    e.target.outerHTML = `<div class="notice ok">Thank you! (This is a demo, so nothing was sent. On your real invitation, RSVPs reach you instantly with the guest count.)</div>`;
    petals(20);
  });
  $("#dv-wish").addEventListener("submit", (e) => {
    e.preventDefault(); if (!validate(e.target)) return;
    $("#wishes").insertAdjacentHTML("afterbegin", `<div class="wish"><b>${esc($("#w-name").value)}</b><p>${esc($("#w-msg").value)}</p></div>`);
    e.target.reset(); toast("Wish posted (demo only)");
  });
  const link = location.href.split("&open")[0];
  $("#dv-share").onclick = () => window.open(`https://wa.me/?text=${encodeURIComponent(`${C.a} & ${C.b} invite you to their wedding: ${link}`)}`, "_blank", "noopener");
  $("#dv-copy").onclick = async () => { try { await navigator.clipboard.writeText(link); toast("Link copied"); } catch { toast(link); } };
  const io = "IntersectionObserver" in window && new IntersectionObserver((es) => es.forEach((x) => { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }), { rootMargin: "0px 0px -10% 0px" });
  $$(".reveal-dv").forEach((el) => (io ? io.observe(el) : el.classList.add("in")));
};

/* ---------- free card maker ---------- */
const TEMPLATES = [
  { id: "wedding", cat: "wedding", name: "Wedding", note: "Red & gold mandap", dark: true, color: "#FFE3A3", inset: [17, 14, 46, 14],
    d: { top: "॥ श्री गणेशाय नमः ॥", title: "Priya weds Rohan", sub: "Together with their families, request the honour of your presence", venue: "Royal Palace Gardens, Jaipur", host: "Agarwal & Maheshwari families" } },
  { id: "save-the-date", cat: "wedding", name: "Save the Date", note: "Blush & varmala", dark: false, color: "#8A2E3B", inset: [16, 16, 38, 16],
    d: { top: "Save the date", title: "Priya & Rohan", sub: "are getting married! Formal invitation to follow", venue: "Jaipur, Rajasthan", host: "#PriyaWedsRohan" } },
  { id: "sagai", cat: "wedding", name: "Sagai / Engagement", note: "Teal & gold arch", dark: true, color: "#F3DFA8", inset: [22, 20, 30, 20],
    d: { top: "Together with their families", title: "Priya & Rohan", sub: "request your presence at their Sagai ceremony", venue: "Hotel Royal Orchid, Jaipur", host: "Agarwal & Maheshwari families" } },
  { id: "anniversary", cat: "wedding", name: "Anniversary", note: "Roses & rings", dark: false, color: "#7A1F2B", inset: [18, 16, 20, 16],
    d: { top: "With love and gratitude", title: "Sunita & Mahesh", sub: "invite you to celebrate their 25th wedding anniversary", venue: "Agarwal Bhawan, Jaipur", host: "With best compliments: Agarwal family" } },
  { id: "birthday-kids", cat: "birthday", name: "Kids' Birthday", note: "Balloons & elephant", dark: false, color: "#3A3F8F", inset: [16, 14, 34, 14],
    d: { top: "You're invited to", title: "Aarav's 5th Birthday", sub: "Join us for cake, games and lots of fun!", venue: "Our home, Malviya Nagar, Jaipur", host: "RSVP: Neha (98xxx xxxxx)" } },
  { id: "birthday-gold", cat: "birthday", name: "Birthday (Elegant)", note: "Black & gold", dark: true, color: "#F3DFA8", inset: [22, 14, 26, 14],
    d: { top: "Please join us to celebrate", title: "Neha turns 30", sub: "An evening of music, dinner and memories", venue: "The Terrace, C-Scheme, Jaipur", host: "Hosted by Rahul" } },
  { id: "godh-bharai", cat: "baby", name: "Godh Bharai", note: "Jhoola & florals", dark: false, color: "#8A3252", inset: [16, 16, 38, 16],
    d: { top: "A little one is on the way", title: "Godh Bharai", sub: "for Priya. Join us for blessings, songs and sweets", venue: "Agarwal Niwas, Jaipur", host: "RSVP: Sunita (98xxx xxxxx)" } },
  { id: "naamkaran", cat: "baby", name: "Naamkaran", note: "Cradle & stars", dark: false, color: "#2F4F7A", inset: [14, 16, 46, 16],
    d: { top: "With joy we invite you to the", title: "Naamkaran", sub: "of our little princess. Join us for the naming ceremony and blessings", venue: "Agarwal Niwas, Jaipur", host: "Neha & Rahul Agarwal" } },
  { id: "mundan", cat: "baby", name: "Mundan", note: "Puja thali & toran", dark: false, color: "#7A2E0E", inset: [20, 16, 28, 16],
    d: { top: "॥ श्री गणेशाय नमः ॥", title: "Mundan Sanskar", sub: "of our son Vivaan. Please bless him with your presence", venue: "Balaji Mandir, Jaipur", host: "Sharma family" } },
  { id: "griha-pravesh", cat: "festival", name: "Griha Pravesh", note: "Kalash & toran", dark: false, color: "#7A2E0E", inset: [14, 16, 38, 16],
    d: { top: "॥ श्री गणेशाय नमः ॥", title: "Griha Pravesh", sub: "Please bless our new home with your presence at the puja and lunch", venue: "B-12, Vaishali Nagar, Jaipur", host: "Maheshwari family" } },
  { id: "puja", cat: "festival", name: "Puja / Bhajan Sandhya", note: "Diya & bells", dark: true, color: "#FFE7A8", inset: [20, 18, 36, 18],
    d: { top: "॥ जय श्री कृष्ण ॥", title: "Bhajan Sandhya", sub: "Join us for an evening of bhajans, aarti and prasad", venue: "Shiv Mandir Hall, Jaipur", host: "Agarwal family" } },
  { id: "diwali", cat: "festival", name: "Diwali Party", note: "Diyas & lanterns", dark: true, color: "#FFD98A", inset: [24, 14, 32, 14],
    d: { top: "Shubh Deepavali", title: "Diwali Get-Together", sub: "Lights, laughter, sweets and card games", venue: "Our home, Raja Park, Jaipur", host: "The Agarwals" } },
  { id: "holi", cat: "festival", name: "Holi Milan", note: "Gulal splash", dark: false, color: "#B0204E", inset: [24, 16, 24, 16],
    d: { top: "Bura na mano, Holi hai!", title: "Holi Milan", sub: "Colours, thandai, gujiya and music", venue: "Community Park, Raja Park, Jaipur", host: "RSVP: Sharma family" } },
  { id: "gangaur-teej", cat: "festival", name: "Teej & Gangaur", note: "Leheriya & swing", dark: true, color: "#FFE9B0", inset: [30, 20, 26, 20],
    d: { top: "Ladies, you're invited", title: "Teej Utsav", sub: "Swings, mehendi, ghevar and folk songs", venue: "Mahila Mandal Hall, Jaipur", host: "Hosted by Mahila Mandal" } },
  { id: "retirement", cat: "other", name: "Retirement", note: "Navy & gold", dark: true, color: "#F3DFA8", inset: [8, 12, 40, 12],
    d: { top: "Please join us to honour", title: "Shri R. K. Agarwal", sub: "on his retirement after 35 years of dedicated service", venue: "Hotel Clarks, Jaipur", host: "Family & colleagues" } },
  { id: "prayer-meet", cat: "other", name: "Prayer Meet", note: "Lotus & diya", dark: false, color: "#5A4A42", inset: [14, 14, 26, 14],
    d: { top: "॥ ॐ शान्ति ॥", title: "Prayer Meet", sub: "in loving memory of Late Shri Ramniwas Agarwal", venue: "Agarwal Bhawan, Jaipur", host: "Agarwal family" } },
];
const SIZES = { card: { w: 1080, h: 1620, pt: [432, 648] }, status: { w: 1080, h: 1920, pt: [405, 720] }, square: { w: 1080, h: 1080, pt: [540, 540] } };

// Minimal one-page PDF that embeds a JPEG (no library needed)
function jpegToPdf(jpg, wPx, hPx, [wPt, hPt]) {
  const enc = new TextEncoder(), parts = [], offs = [];
  let len = 0; const push = (x) => { const b = typeof x === "string" ? enc.encode(x) : x; parts.push(b); len += b.length; };
  const obj = (n, body) => { offs[n] = len; push(`${n} 0 obj\n${body}\nendobj\n`); };
  push("%PDF-1.4\n%\xE2\xE3\xCF\xD3\n");
  obj(1, "<< /Type /Catalog /Pages 2 0 R >>");
  obj(2, "<< /Type /Pages /Kids [3 0 R] /Count 1 >>");
  obj(3, `<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${wPt} ${hPt}] /Resources << /XObject << /Im0 4 0 R >> >> /Contents 5 0 R >>`);
  offs[4] = len; push(`4 0 obj\n<< /Type /XObject /Subtype /Image /Width ${wPx} /Height ${hPx} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${jpg.length} >>\nstream\n`); push(jpg); push("\nendstream\nendobj\n");
  const content = `q ${wPt} 0 0 ${hPt} 0 0 cm /Im0 Do Q`;
  obj(5, `<< /Length ${content.length} >>\nstream\n${content}\nendstream`);
  const xref = len;
  push(`xref\n0 6\n0000000000 65535 f \n${[1, 2, 3, 4, 5].map((n) => String(offs[n]).padStart(10, "0") + " 00000 n \n").join("")}trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF`);
  return new Blob(parts, { type: "application/pdf" });
}

pages["free-cards"] = () => {
  const grid = $("#tpl-grid"), form = $("#mk-form"), card = $("#mk-card");
  let t = TEMPLATES.find((x) => x.id === params.get("t")) || TEMPLATES[0];
  let size = "card", cat = "all";
  const nextSat = () => { const d = new Date(); d.setDate(d.getDate() + ((6 - d.getDay() + 7) % 7 || 7) + 14); return d.toISOString().slice(0, 10); };
  grid.innerHTML = TEMPLATES.map((x) => `<button type="button" class="tpl" data-t="${x.id}" data-cat="${x.cat}" aria-pressed="${x.id === t.id}"><img src="${IMG("tpl-" + x.id + ".jpg")}" alt="" loading="lazy" crossorigin="anonymous"><span>${x.name}<small>${x.note}</small></span></button>`).join("");
  $("#tpl-cats").addEventListener("click", (e) => { const b = e.target.closest("[data-cat]"); if (!b) return; cat = b.dataset.cat;
    $$("#tpl-cats .chip").forEach((c) => c.setAttribute("aria-pressed", c === b)); $$(".tpl").forEach((x) => x.classList.toggle("hide", cat !== "all" && x.dataset.cat !== cat)); });
  const fill = () => { for (const k of ["top", "title", "sub", "venue", "host"]) form[k].value = t.d[k]; form.date.value = form.date.value || nextSat(); form.time.value = form.time.value || "18:00"; };
  const val = () => { const v = formData(form); const d = v.date ? new Date(v.date + "T00:00") : null;
    v.when = [d && !isNaN(d) ? d.toLocaleDateString("en-IN", { weekday: "long", day: "numeric", month: "long", year: "numeric" }) : "", v.time ? new Date("2000-01-01T" + v.time).toLocaleTimeString("en-IN", { hour: "numeric", minute: "2-digit" }) : ""].filter(Boolean).join(" · "); return v; };
  const blank = () => $("#mk-blank").checked;
  const draw = () => {
    const v = val(), [T, R, B, L] = t.inset;
    card.innerHTML = `<img src="${IMG("tpl-" + t.id + ".jpg")}" alt="${esc(t.name)} card" crossorigin="anonymous">` + (blank() ? "" : `
      <div class="inv-text" style="inset:${T}% ${R}% ${B}% ${L}%;color:${t.color};${t.dark ? "text-shadow:0 1px 6px rgba(0,0,0,.4)" : ""}">
      ${v.top ? `<span class="${/[ऀ-ॿ]/.test(v.top) ? "it-deva" : "it-caps"}">${esc(v.top)}</span>` : ""}<span class="it-script" style="font-size:12cqw">${esc(v.title)}</span>
      ${v.sub ? `<span class="it-ven" style="font-size:3.8cqw">${esc(v.sub)}</span>` : ""}<span class="it-rule"></span>
      ${v.when ? `<span class="it-date">${esc(v.when)}</span>` : ""}${v.venue ? `<span class="it-ven">${esc(v.venue)}</span>` : ""}${v.host ? `<span class="it-caps" style="font-size:2.8cqw;margin-top:1cqw">${esc(v.host)}</span>` : ""}</div>`);
  };
  grid.addEventListener("click", (e) => { const b = e.target.closest("[data-t]"); if (!b) return; t = TEMPLATES.find((x) => x.id === b.dataset.t); $$(".tpl").forEach((x) => x.setAttribute("aria-pressed", x === b)); fill(); draw(); history.replaceState(null, "", "?t=" + t.id); $("#maker").scrollIntoView({ behavior: "smooth", block: "start" }); });
  form.addEventListener("input", draw);
  $("#mk-blank").addEventListener("change", draw);
  $("#mk-size").addEventListener("click", (e) => { const b = e.target.closest("[data-size]"); if (!b) return; size = b.dataset.size; $$("#mk-size button").forEach((x) => x.setAttribute("aria-pressed", x === b)); });
  fill(); draw();

  const loadImg = (src) => new Promise((res, rej) => { const i = new Image(); i.crossOrigin = "anonymous"; i.onload = () => res(i); i.onerror = rej; i.src = src; });
  // 1) the card itself at 1080x1620
  async function renderCard() {
    await document.fonts.ready;
    await Promise.all(["400 40px 'Great Vibes'", "600 40px 'Cormorant Garamond'", "500 40px 'DM Sans'", "600 40px 'DM Sans'", "400 40px 'Tiro Devanagari Hindi'"].map((f) => document.fonts.load(f).catch(() => {})));
    const W = 1080, H = 1620, c = document.createElement("canvas"); c.width = W; c.height = H; const g = c.getContext("2d");
    g.drawImage(await loadImg(IMG("tpl-" + t.id + ".jpg")), 0, 0, W, H);
    if (blank()) return c;
    const v = val(), [T, R, B, L] = t.inset; const x0 = W * L / 100, x1 = W * (1 - R / 100), boxW = x1 - x0, cx = (x0 + x1) / 2;
    const lines = [];
    const wrap = (text, font, size, gap) => { g.font = font.replace("SIZE", size + "px"); const words = String(text).split(" "); let line = ""; const out = [];
      for (const w of words) { const test = line ? line + " " + w : w; if (g.measureText(test).width > boxW && line) { out.push(line); line = w; } else line = test; } if (line) out.push(line);
      out.forEach((l) => lines.push({ l, font: font.replace("SIZE", size + "px"), size, gap })); };
    const deva = /[ऀ-ॿ]/;
    if (v.top) wrap(deva.test(v.top) ? v.top : v.top.toUpperCase(), deva.test(v.top) ? "400 SIZE 'Tiro Devanagari Hindi'" : "600 SIZE 'DM Sans'", 30, 14);
    wrap(v.title, deva.test(v.title) ? "400 SIZE 'Tiro Devanagari Hindi'" : "400 SIZE 'Great Vibes'", deva.test(v.title) ? 90 : 120, 18);
    if (v.sub) wrap(v.sub, "500 SIZE 'DM Sans'", 38, 10);
    lines.push({ rule: true, size: 30, gap: 10 });
    if (v.when) wrap(v.when, "600 SIZE 'Cormorant Garamond'", 46, 8);
    if (v.venue) wrap(v.venue, "500 SIZE 'DM Sans'", 34, 8);
    if (v.host) wrap(deva.test(v.host) ? v.host : v.host.toUpperCase(), "600 SIZE 'DM Sans'", 27, 8);
    const total = lines.reduce((a, l) => a + l.size * 1.15 + l.gap, 0);
    const top = H * T / 100, bottom = H * (1 - B / 100); let y = top + Math.max(0, (bottom - top - total) / 2);
    g.textAlign = "center"; g.textBaseline = "top"; g.fillStyle = t.color;
    if (t.dark) { g.shadowColor = "rgba(0,0,0,.45)"; g.shadowBlur = 8; }
    for (const ln of lines) {
      if (ln.rule) { g.globalAlpha = .6; g.fillRect(cx - 150, y + ln.size / 2, 300, 2); g.save(); g.translate(cx, y + ln.size / 2 + 1); g.rotate(Math.PI / 4); g.fillRect(-9, -9, 18, 18); g.restore(); g.globalAlpha = 1; y += ln.size + ln.gap; continue; }
      g.font = ln.font; g.fillText(ln.l, cx, y); y += ln.size * 1.15 + ln.gap;
    }
    g.shadowBlur = 0; g.globalAlpha = .7; g.font = "500 22px 'DM Sans'"; g.fillStyle = t.dark ? "#fff" : "#392820"; g.fillText("Made free with BFI · bfi-royal-heritage.vercel.app", W / 2, H - 40); g.globalAlpha = 1;
    return c;
  }
  // 2) place it on the chosen canvas size (status/square get a soft blurred backdrop)
  async function render() {
    const cardC = await renderCard(), S = SIZES[size];
    if (size === "card") return cardC;
    const c = document.createElement("canvas"); c.width = S.w; c.height = S.h; const g = c.getContext("2d");
    const sc = Math.max(S.w / cardC.width, S.h / cardC.height);
    g.filter = "blur(28px) brightness(.8)"; g.drawImage(cardC, (S.w - cardC.width * sc) / 2 - 40, (S.h - cardC.height * sc) / 2 - 40, cardC.width * sc + 80, cardC.height * sc + 80); g.filter = "none";
    g.fillStyle = "rgba(0,0,0,.18)"; g.fillRect(0, 0, S.w, S.h);
    const fit = Math.min((S.w * .86) / cardC.width, (S.h * .86) / cardC.height), w = cardC.width * fit, h = cardC.height * fit;
    g.shadowColor = "rgba(0,0,0,.45)"; g.shadowBlur = 40; g.shadowOffsetY = 16;
    g.drawImage(cardC, (S.w - w) / 2, (S.h - h) / 2, w, h); g.shadowBlur = 0;
    return c;
  }
  const blobOf = (c, type, q) => new Promise((res) => c.toBlob(res, type, q));
  const fname = (ext) => `bfi-${t.id}-${size}${blank() ? "-blank" : ""}.${ext}`;
  const save = (blob, name) => { const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name; document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 4000); };
  $$("[data-fmt]").forEach((btn) => (btn.onclick = async () => {
    const fmt = btn.dataset.fmt; setBusy(btn, true, "…");
    try {
      const c = await render();
      if (fmt === "png") save(await blobOf(c, "image/png"), fname("png"));
      else if (fmt === "jpg") save(await blobOf(c, "image/jpeg", .92), fname("jpg"));
      else { const jpg = new Uint8Array(await (await blobOf(c, "image/jpeg", .92)).arrayBuffer()); save(jpegToPdf(jpg, c.width, c.height, SIZES[size].pt), fname("pdf")); }
      toast(`${fmt.toUpperCase()} downloaded`);
    } catch { toast("Couldn't create the file. Please try again."); } finally { setBusy(btn, false); }
  }));
  $("#mk-share").onclick = async (e) => { const btn = e.currentTarget; setBusy(btn, true, "Preparing…");
    try { const blob = await blobOf(await render(), "image/png"); const file = new File([blob], fname("png"), { type: "image/png" });
      if (navigator.canShare?.({ files: [file] })) await navigator.share({ files: [file], text: `${val().title} – you're invited!` });
      else { save(blob, fname("png")); window.open(`https://wa.me/?text=${encodeURIComponent(`${val().title} – you're invited! (card image attached)`)}`, "_blank", "noopener"); toast("Card downloaded: attach it in WhatsApp"); }
    } catch (err) { if (err?.name !== "AbortError") toast("Couldn't share. Try a download instead."); } finally { setBusy(btn, false); } };
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
  track("page_view", { ref: document.referrer ? new URL(document.referrer).hostname : "", q: location.search.slice(0, 60) });
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a,button"); if (!a) return;
    const href = a.getAttribute("href") || "";
    if (a.dataset.track) track(a.dataset.track, { label: (a.textContent || "").trim().slice(0, 40) });
    else if (/wa\.me\//.test(href) || a.hasAttribute("data-wa")) track("whatsapp_click", { from: page });
    else if (/^tel:/.test(href)) track("call_click", { from: page });
    else if (/^mailto:/.test(href)) track("email_click", { from: page });
    else if (/demo\.html/.test(href)) track("demo_open", { from: page, to: href.slice(0, 60) });
    else if (/customize\.html/.test(href)) track("customize_click", { from: page });
    else if (/design-[\w-]+\.html/.test(href)) track("design_click", { from: page, to: href.slice(0, 60) });
    else if (a.matches("[data-fmt]")) track("free_card_download", { fmt: a.dataset.fmt });
  }, { capture: true });
  try { page.startsWith("design-") ? initDesignPage() : await pages[page]?.(); } catch (e) { console.error(e); }
})();
