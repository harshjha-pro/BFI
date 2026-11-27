/* Bfiluxe admin. Security model: every read/write is checked by the database
   (row level security + private.is_admin(), which needs an admin account AND
   a two-factor (aal2) session). This page never holds any secret key. */
(() => {
"use strict";
const CFG = { url: "https://oaosapkkzoynaqpnmvrj.supabase.co", key: "sb_publishable_6uDnEKLsGMUyEUuDo7zRIg_MnI173-j", site: "https://bfiluxe.com" };
const IDLE_MIN = 30;
const sb = window.supabase.createClient(CFG.url, CFG.key, {
  auth: { storage: window.sessionStorage, storageKey: "bfx-admin", persistSession: true, autoRefreshToken: true, detectSessionInUrl: false }
});

/* ---------- helpers ---------- */
const root = document.getElementById("root");
const esc = (v) => String(v ?? "").replace(/[&<>"'`=]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;", "`": "&#96;", "=": "&#61;" }[c]));
const inr = (n) => "₹" + Number(n || 0).toLocaleString("en-IN");
const num = (n) => Number(n || 0).toLocaleString("en-IN");
const initials = (s) => String(s || "?").trim().split(/\s+/).slice(0, 2).map((w) => w[0] || "").join("").toUpperCase() || "?";
const ago = (d) => { if (!d) return "—"; const s = (Date.now() - new Date(d)) / 1000;
  if (s < 60) return "just now"; if (s < 3600) return Math.floor(s / 60) + " min ago"; if (s < 86400) return Math.floor(s / 3600) + " h ago";
  if (s < 86400 * 7) return Math.floor(s / 86400) + " d ago"; return new Date(d).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }); };
const fdate = (d) => d ? new Date(d).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }) : "—";
const cover = (slug) => `${CFG.site}/img/art/cover-${encodeURIComponent(slug)}.webp`;
const digits = (p) => String(p || "").replace(/\D/g, "");
const waLink = (p) => { let d = digits(p); if (d.length === 10) d = "91" + d; return d.length >= 11 && d.length <= 15 ? "https://wa.me/" + d : ""; };
const okEmail = (e) => /^[^\s@<>"']+@[^\s@<>"']+\.[^\s@<>"']+$/.test(String(e || ""));
let toastT = 0;
function toast(msg, bad = false) { const t = document.getElementById("toast"); t.textContent = msg; t.className = "on" + (bad ? " bad" : ""); clearTimeout(toastT); toastT = setTimeout(() => { t.className = ""; }, 3200); }
const fail = (e) => { console.error(e); toast(e?.message?.includes("not allowed") || e?.code === "42501" ? "Not allowed: please sign in again." : "Something went wrong: " + (e?.message || "please try again"), true); };
const intIn = (v) => { const n = Math.round(Number(String(v).replace(/[^\d.]/g, ""))); return Number.isFinite(n) && n >= 0 && n <= 10000000 ? n : null; };

const I = {
  dash: '<path d="M4 4h7v7H4zM13 4h7v4h-7zM13 10h7v10h-7zM4 13h7v7H4z" fill="currentColor" opacity=".9"/>',
  enq: '<path d="M4 5h16v11H8l-4 4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M8 9h8M8 12h5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
  ord: '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 8h6M9 12h6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
  price: '<path d="M3 12V4h8l10 10-8 8z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="7.5" cy="8.5" r="1.5" fill="currentColor"/>',
  des: '<rect x="6" y="2.5" width="12" height="19" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M9 7h6M9 10.5h6M10 18h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
  rev: '<path d="M12 3l2.6 5.6 6.1.6-4.6 4.1 1.3 6-5.4-3.1-5.4 3.1 1.3-6L3.3 9.2l6.1-.6z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
  cus: '<circle cx="9" cy="8" r="3.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3 20c.8-3.6 3.2-5.5 6-5.5s5.2 1.9 6 5.5M16 4.8a3.4 3.4 0 0 1 0 6.4M18 14.8c1.6.7 2.6 2.4 3 5.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
  ana: '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
  set: '<circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
  arrow: '<path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
  dots: '<circle cx="12" cy="5" r="1.7" fill="currentColor"/><circle cx="12" cy="12" r="1.7" fill="currentColor"/><circle cx="12" cy="19" r="1.7" fill="currentColor"/>',
  down: '<path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
  menu: '<path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  x: '<path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  search: '<circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 16l4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  ext: '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
};
const ic = (k, s = 20) => `<svg viewBox="0 0 24 24" width="${s}" height="${s}" aria-hidden="true">${I[k]}</svg>`;

/* Illustrations: line art with soft yellow fills, drawn for Bfiluxe. */
const ART = {
  invite: `<svg class="art" viewBox="0 0 360 300" aria-hidden="true">
    <ellipse cx="180" cy="268" rx="150" ry="16" fill="#E9D9A6" opacity=".6"/>
    <path d="M62 150c-14-46 22-94 76-96 40-2 58 22 92 14 40-9 74 20 72 62-2 52-44 70-94 72-64 3-128-4-146-52z" fill="#FFF3CC"/>
    <g transform="rotate(-8 150 150)"><rect x="96" y="70" width="104" height="186" rx="16" fill="#fff" stroke="#2B241A" stroke-width="3"/>
      <rect x="106" y="84" width="84" height="158" rx="8" fill="#4B202A"/>
      <path d="M118 120q30-26 60 0v70h-60z" fill="#F8D46B" opacity=".95"/><circle cx="148" cy="110" r="7" fill="#F8D46B"/>
      <path d="M126 205h44M132 216h32" stroke="#F8D46B" stroke-width="3" stroke-linecap="round"/><rect x="138" y="76" width="20" height="4" rx="2" fill="#2B241A"/></g>
    <g transform="rotate(10 250 190)"><rect x="196" y="150" width="120" height="82" rx="8" fill="#fff" stroke="#2B241A" stroke-width="3"/>
      <path d="M196 156l60 42 60-42" fill="none" stroke="#2B241A" stroke-width="3" stroke-linejoin="round"/>
      <circle cx="256" cy="198" r="13" fill="#C8463F" stroke="#2B241A" stroke-width="3"/><path d="M251 198h10M256 193v10" stroke="#FFD9A0" stroke-width="2.4" stroke-linecap="round"/></g>
    <g fill="#F2A33A" stroke="#2B241A" stroke-width="2.5"><circle cx="72" cy="232" r="13"/><circle cx="96" cy="248" r="10"/><circle cx="300" cy="96" r="11"/></g>
    <g fill="#8FB07A" stroke="#2B241A" stroke-width="2.5"><path d="M58 248c-14-2-22-12-20-22 12 0 20 8 20 22z"/><path d="M314 112c10 4 18 2 22-6-8-6-18-4-22 6z"/></g>
    <path d="M286 50l4 10 10 4-10 4-4 10-4-10-10-4 10-4z" fill="#F8D46B" stroke="#2B241A" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="M60 78l3 7 7 3-7 3-3 7-3-7-7-3 7-3z" fill="#F8D46B" stroke="#2B241A" stroke-width="2" stroke-linejoin="round"/></svg>`,
  side: `<svg class="art" viewBox="0 0 220 130" aria-hidden="true">
    <path d="M30 100c-10-30 18-62 56-62 26 0 34 14 58 9 30-6 52 12 50 38-2 30-30 40-62 41-48 2-92-2-102-26z" fill="#FFF7DF"/>
    <g transform="rotate(-10 92 72)"><rect x="66" y="18" width="54" height="96" rx="10" fill="#fff" stroke="#2B241A" stroke-width="2.6"/><rect x="72" y="27" width="42" height="78" rx="5" fill="#4B202A"/>
      <path d="M79 48q14-12 28 0v34H79z" fill="#F8D46B"/><path d="M83 92h20" stroke="#F8D46B" stroke-width="2.4" stroke-linecap="round"/></g>
    <g transform="rotate(8 150 82)"><rect x="124" y="58" width="66" height="46" rx="6" fill="#fff" stroke="#2B241A" stroke-width="2.6"/><path d="M124 62l33 24 33-24" fill="none" stroke="#2B241A" stroke-width="2.6" stroke-linejoin="round"/><circle cx="157" cy="86" r="8" fill="#C8463F" stroke="#2B241A" stroke-width="2.2"/></g>
    <circle cx="40" cy="104" r="9" fill="#F2A33A" stroke="#2B241A" stroke-width="2.2"/><circle cx="194" cy="34" r="7" fill="#F2A33A" stroke="#2B241A" stroke-width="2.2"/>
    <path d="M178 16l2.6 6 6 2.6-6 2.6-2.6 6-2.6-6-6-2.6 6-2.6z" fill="#F8D46B" stroke="#2B241A" stroke-width="1.8" stroke-linejoin="round"/></svg>`,
  empty: `<svg class="art" viewBox="0 0 160 110" aria-hidden="true"><ellipse cx="80" cy="100" rx="60" ry="7" fill="#EFE5C8"/>
    <rect x="34" y="34" width="92" height="60" rx="7" fill="#fff" stroke="#2B241A" stroke-width="2.6"/><path d="M34 39l46 32 46-32" fill="none" stroke="#2B241A" stroke-width="2.6" stroke-linejoin="round"/>
    <circle cx="80" cy="70" r="9" fill="#F8D46B" stroke="#2B241A" stroke-width="2.2"/><path d="M118 14l2.6 6 6 2.6-6 2.6-2.6 6-2.6-6-6-2.6 6-2.6z" fill="#F8D46B" stroke="#2B241A" stroke-width="1.8"/></svg>`,
};
const empty = (t) => `<div class="empty">${ART.empty}<p>${esc(t)}</p></div>`;

/* ---------- state ---------- */
const S = { view: "dashboard", user: null, stats: null, days: 30, enq: null, orders: null, designs: null, settings: null, reviews: null, customers: null, audit: null,
  enqTab: "all", enqQ: "", ordTab: "all", revTab: "pending" };
const VIEWS = [["dashboard", "Dashboard", "dash"], ["enquiries", "Enquiries", "enq"], ["orders", "Orders", "ord"], ["prices", "Prices", "price"],
  ["designs", "Designs", "des"], ["reviews", "Reviews", "rev"], ["customers", "Customers", "cus"], ["analytics", "Analytics", "ana"], ["settings", "Settings", "set"]];
const ENQ_ST = ["new", "contacted", "won", "lost"];
const ORD_ST = ["draft", "submitted", "in_progress", "preview_sent", "approved", "delivered", "cancelled"];
const stLabel = (s) => ({ new: "New", contacted: "Contacted", won: "Won", lost: "Lost", draft: "Draft", submitted: "Submitted", in_progress: "In progress",
  preview_sent: "Preview sent", approved: "Approved", delivered: "Delivered", cancelled: "Cancelled" }[s] || s);
const pill = (s) => `<span class="pill st-${esc(s)}">${esc(stLabel(s))}</span>`;
const EVN = { design_click: "Opened a design", demo_open: "Opened a live demo", hero_demo: "Hero: live demo", hero_explore: "Hero: explore", hdr_start: "Header: start",
  customize_click: "Start invitation clicked", customize_start: "Order form started", customize_submit: "Order form submitted", contact_submit: "Contact form sent",
  partner_apply: "Partner application", work_live_open: "Opened a real invitation", wa_click: "WhatsApp clicked" };

/* ---------- auth flow ---------- */
let idleT = 0;
function resetIdle() { clearTimeout(idleT); idleT = setTimeout(async () => { await sb.auth.signOut(); toast("Signed out after " + IDLE_MIN + " minutes of inactivity."); login(); }, IDLE_MIN * 60000); }
["click", "keydown", "pointermove", "scroll"].forEach((e) => addEventListener(e, () => { if (S.user) resetIdle(); }, { passive: true }));

function authShell(inner) {
  root.className = "";
  root.innerHTML = `<div class="auth"><div class="auth-card"><div class="auth-art"><div><div class="brand"><img src="img/elephant.webp" alt="" width="40" height="30"><span>Bfiluxe<small>Admin studio</small></span></div></div>
    ${ART.invite}<div><h2>Every invitation, enquiry and rupee in one place.</h2><p>Private area. Only the Bfiluxe team can open it.</p></div></div>
    <div class="auth-form">${inner}</div></div></div>`;
}
function login(msg = "") {
  S.user = null;
  authShell(`<form id="f-login" novalidate><h1>Sign in</h1><p class="muted">Use your admin email and password.</p>
    <label class="f" for="em">Email</label><input class="in" id="em" type="email" autocomplete="username" required maxlength="200">
    <label class="f" for="pw">Password</label><input class="in" id="pw" type="password" autocomplete="current-password" required maxlength="200">
    <button class="btn" type="submit">Continue</button><p class="err" id="err">${esc(msg)}</p></form>`);
  const f = document.getElementById("f-login");
  f.addEventListener("submit", async (e) => {
    e.preventDefault(); const b = f.querySelector("button"); b.disabled = true; document.getElementById("err").textContent = "";
    const { error } = await sb.auth.signInWithPassword({ email: f.em.value.trim(), password: f.pw.value });
    b.disabled = false; f.pw.value = "";
    if (error) { document.getElementById("err").textContent = /rate|many/i.test(error.message) ? "Too many attempts. Wait a few minutes." : "Email or password is not correct."; return; }
    gate();
  });
  document.getElementById("em").focus();
}
async function gate() {
  const { data: sess } = await sb.auth.getSession();
  if (!sess.session) return login();
  const { data: who, error } = await sb.rpc("admin_whoami");
  if (error || !who?.listed) { await sb.auth.signOut(); return login("This account does not have admin access."); }
  const { data: aal } = await sb.auth.mfa.getAuthenticatorAssuranceLevel();
  if (aal?.currentLevel === "aal2") { S.user = sess.session.user; resetIdle(); return app(); }
  const { data: fl } = await sb.auth.mfa.listFactors();
  const totp = (fl?.totp || []).find((f) => f.status === "verified");
  return totp ? codeStep(totp.id) : enrollStep();
}
function codeStep(factorId) {
  authShell(`<form id="f-code" novalidate><h1>Two-step check</h1><p class="muted">Open your authenticator app (Google Authenticator, Microsoft Authenticator or Authy) and type the 6-digit code for <b>Bfiluxe</b>.</p>
    <label class="f" for="code">6-digit code</label><input class="in code-in" id="code" inputmode="numeric" autocomplete="one-time-code" maxlength="6" pattern="\\d{6}" required>
    <button class="btn" type="submit">Verify</button><button class="btn btn-ghost" type="button" id="back" style="margin-top:8px">Use a different account</button><p class="err" id="err"></p></form>`);
  bindCode(factorId);
}
async function enrollStep() {
  const { data: fl } = await sb.auth.mfa.listFactors();
  for (const f of (fl?.all || []).filter((x) => x.status !== "verified")) await sb.auth.mfa.unenroll({ factorId: f.id });
  const { data, error } = await sb.auth.mfa.enroll({ factorType: "totp", friendlyName: "Bfiluxe admin " + new Date().toISOString().slice(0, 10) });
  if (error) { await sb.auth.signOut(); return login("Could not start two-step setup: " + error.message); }
  authShell(`<form id="f-code" novalidate><h1>Protect your admin</h1><p class="muted">One-time setup. Scan this QR code with an authenticator app (Google Authenticator, Microsoft Authenticator or Authy), then type the 6-digit code it shows. After this, signing in always needs your phone, so a stolen password alone can't open the admin.</p>
    <img class="qr" id="qr" alt="QR code for your authenticator app" width="190" height="190">
    <p class="small muted" style="margin:0 0 4px">Can't scan? Type this key into the app:</p><div class="secret" id="secret"></div>
    <label class="f" for="code">6-digit code</label><input class="in code-in" id="code" inputmode="numeric" autocomplete="one-time-code" maxlength="6" pattern="\\d{6}" required>
    <button class="btn" type="submit">Turn on and continue</button><button class="btn btn-ghost" type="button" id="back" style="margin-top:8px">Cancel</button><p class="err" id="err"></p></form>`);
  const qr = String(data.totp.qr_code || "");
  if (qr.startsWith("data:image/svg+xml")) document.getElementById("qr").src = qr;
  document.getElementById("secret").textContent = data.totp.secret;
  bindCode(data.id);
}
function bindCode(factorId) {
  const f = document.getElementById("f-code"), c = document.getElementById("code");
  c.addEventListener("input", () => { c.value = c.value.replace(/\D/g, "").slice(0, 6); if (c.value.length === 6) f.requestSubmit(); });
  document.getElementById("back").addEventListener("click", async () => { await sb.auth.signOut(); login(); });
  f.addEventListener("submit", async (e) => {
    e.preventDefault(); if (!/^\d{6}$/.test(c.value)) return;
    const b = f.querySelector("button[type=submit]"); b.disabled = true;
    const { error } = await sb.auth.mfa.challengeAndVerify({ factorId, code: c.value });
    b.disabled = false;
    if (error) { c.value = ""; document.getElementById("err").textContent = /rate|many/i.test(error.message) ? "Too many attempts. Wait a minute." : "That code didn't work. Check the time on your phone and try the newest code."; c.focus(); return; }
    gate();
  });
  c.focus();
}
sb.auth.onAuthStateChange((ev) => { if (ev === "SIGNED_OUT" && S.user) { S.user = null; login(); } });

/* ---------- data ---------- */
async function q(p) { const { data, error } = await p; if (error) throw error; return data; }
const load = {
  stats: async () => (S.stats = await q(sb.rpc("admin_stats", { p_days: S.days }))),
  enq: async () => (S.enq = await q(sb.from("enquiries").select("*").order("created_at", { ascending: false }).limit(1000))),
  orders: async () => (S.orders = await q(sb.from("customizations").select("*").order("updated_at", { ascending: false }).limit(1000))),
  designs: async () => (S.designs = await q(sb.from("invitations").select("*").order("sort"))),
  settings: async () => { const rows = await q(sb.from("site_settings").select("*")); S.settings = Object.fromEntries(rows.map((r) => [r.key, r.value])); return S.settings; },
  reviews: async () => (S.reviews = await q(sb.from("reviews").select("*").order("created_at", { ascending: false }).limit(500))),
  customers: async () => (S.customers = await q(sb.rpc("admin_customers"))),
  audit: async () => (S.audit = await q(sb.rpc("admin_audit", { p_limit: 60 }))),
};
const custEmail = (id) => (S.customers || []).find((c) => c.id === id)?.email || "Customer";

/* ---------- frame ---------- */
function app() {
  root.className = "";
  root.innerHTML = `<div class="app"><aside class="side" id="side">
      <div class="brand"><img src="img/elephant.webp" alt="" width="40" height="30"><span>Bfiluxe<small>Admin studio</small></span></div>
      <nav class="nav" aria-label="Admin sections">${VIEWS.map(([k, t, i]) => `<button type="button" data-nav="${k}"><span class="ico">${ic(i)}</span>${t}<span class="badge" data-badge="${k}" hidden></span></button>`).join("")}</nav>
      <div class="side-card">${ART.side}<b id="side-num">—</b><span>visitors in the last 30 days</span></div>
    </aside><main class="main" id="main" tabindex="-1"></main></div>`;
  root.querySelectorAll("[data-nav]").forEach((b) => b.addEventListener("click", () => go(b.dataset.nav)));
  const v = (location.hash || "").slice(1); go(VIEWS.some(([k]) => k === v) ? v : "dashboard");
  load.stats().then(badges).catch(() => {});
}
function badges() {
  const st = S.stats; if (!st) return;
  document.getElementById("side-num").textContent = num(st.visitors);
  const set = (k, n) => { const b = root.querySelector(`[data-badge="${k}"]`); if (b) { b.hidden = !n; b.textContent = n; } };
  set("enquiries", st.enquiries_new); set("reviews", st.reviews_pending);
}
async function go(view) {
  S.view = view; history.replaceState(null, "", "#" + view);
  root.querySelectorAll("[data-nav]").forEach((b) => b.setAttribute("aria-current", b.dataset.nav === view ? "page" : "false"));
  document.getElementById("side").classList.remove("open");
  const m = document.getElementById("main");
  m.innerHTML = `<div class="topbar"><button class="icon-btn" id="burger" aria-label="Open menu">${ic("menu", 22)}</button><div class="brand"><img src="img/elephant.webp" alt="" width="34" height="26"><span>Bfiluxe</span></div><span style="width:32px"></span></div><div class="boot" style="min-height:50vh"><div class="spinner"></div></div>`;
  m.querySelector("#burger").addEventListener("click", () => document.getElementById("side").classList.add("open"));
  try { await RENDER[view](m); } catch (e) { fail(e); m.querySelector(".boot")?.replaceWith(Object.assign(document.createElement("div"), { innerHTML: empty("Could not load this page.") })); }
  m.querySelector("#burger")?.addEventListener("click", () => document.getElementById("side").classList.add("open"));
  m.focus({ preventScroll: true });
}
const top = () => `<div class="topbar"><button class="icon-btn" id="burger" aria-label="Open menu">${ic("menu", 22)}</button><div class="brand"><img src="img/elephant.webp" alt="" width="34" height="26"><span>Bfiluxe</span></div><span style="width:32px"></span></div>`;
const head = (t, sub, right = "") => `${top()}<div class="page-h"><div><h1>${t}</h1>${sub ? `<p>${sub}</p>` : ""}</div><div class="row">${right}</div></div>`;
const animate = (m) => requestAnimationFrame(() => m.querySelectorAll("[data-w]").forEach((el) => { el.style[el.dataset.prop || "width"] = Math.max(0, Math.min(100, +el.dataset.w)) + "%"; }));
document.addEventListener("click", (e) => { if (!e.target.closest(".menu")) document.querySelectorAll(".menu-pop").forEach((p) => p.remove()); });

/* ---------- views ---------- */
const RENDER = {};

RENDER.dashboard = async (m) => {
  await Promise.all([load.stats(), load.enq(), load.audit().catch(() => (S.audit = []))]); badges();
  const st = S.stats, pop = (st.designs || []).slice(0, 3), maxV = Math.max(1, ...pop.map((d) => d.views));
  const tint = ["#F9CF86", "#F8AE84", "#F6A6A8"];
  const name = (S.user?.email || "").split("@")[0];
  m.innerHTML = `${top()}<div class="dash"><div>
    <div class="sec-h"><h2>Popular designs</h2><span class="muted small">Last ${st.days} days</span></div>
    <div class="pop">${pop.map((d, k) => `<div class="pop-c"><div class="pop-art" data-bg="${tint[k]}"><span class="rank">#${k + 1}</span><img src="${cover(d.slug)}" alt="" loading="lazy"></div>
      <div class="pop-b"><h3>${esc(d.name)}</h3><div class="bar"><i data-w="${Math.round(d.views * 100 / maxV)}"></i></div>
      <div class="pop-meta"><span>Views: <b>${num(d.views)}</b></span><span>Enquiries: <b>${num(d.enquiries)}</b></span></div></div></div>`).join("")}</div>
    <div class="sec-h"><h2>Recent enquiries</h2><div class="tabs" role="tablist">${["all", ...ENQ_ST].map((t) => `<button role="tab" type="button" data-tab="${t}" aria-selected="${S.enqTab === t}">${t === "all" ? "All" : stLabel(t)}</button>`).join("")}</div></div>
    <div class="list" id="enq-list"></div>
    </div><div class="rail">
      <div class="hello"><span class="blob"></span><img class="el" src="img/elephant.webp" alt=""><h3>Namaste${name ? ", " + esc(name) : ""}</h3><p>${num(st.enquiries_new)} new enquir${st.enquiries_new === 1 ? "y" : "ies"} waiting</p><button class="btn btn-round go" data-go="enquiries" aria-label="Open enquiries">${ic("arrow", 18)}</button></div>
      <div class="me"><span class="av">${esc(initials(name))}</span><div><b>${esc(S.user?.email || "")}</b><span>Admin · 2-step on</span></div>
        <div class="menu"><button class="icon-btn" id="me-menu" aria-label="Account menu">${ic("down", 18)}</button></div></div>
      <div class="tiles">
        <div class="tile"><b>${num(st.visitors)}</b><span>Visitors<br>${st.days} days</span></div>
        <div class="tile"><b>${num(st.enquiries)}</b><span>Enquiries<br>${st.days} days</span></div>
        <div class="tile"><b>${num(st.won)}</b><span>Bookings<br>won</span></div>
        <div class="tile"><b>${num(st.orders)}</b><span>Orders<br>submitted</span></div>
      </div>
      <div class="card"><div class="sec-h"><h2>Money</h2></div><div class="kv">
        <div><span>Booked value</span><b>${inr(st.revenue)}</b></div><div><span>Advance received</span><b>${inr(st.advance)}</b></div>
        <div><span>Balance to collect</span><b>${inr(Math.max(0, st.revenue - st.advance))}</b></div></div></div>
      <div class="card"><div class="sec-h"><h2>Latest changes</h2><button class="btn btn-ghost btn-sm" data-go="settings">All</button></div><div class="feed">${(S.audit || []).slice(0, 4).map((a) => `<div class="feed-i"><span class="ph">${ic({ site_settings: "price", enquiries: "enq", customizations: "ord", reviews: "rev", invitations: "des" }[a.tbl] || "set")}</span><div><b>${esc(auditLine(a))}</b><span>${esc(ago(a.at))}</span></div></div>`).join("") || '<p class="muted small">Nothing changed yet.</p>'}</div></div>
    </div></div>`;
  m.querySelectorAll("[data-bg]").forEach((el) => { el.style.background = el.dataset.bg; });
  m.querySelectorAll("[data-go]").forEach((b) => b.addEventListener("click", () => go(b.dataset.go)));
  m.querySelectorAll("[data-tab]").forEach((b) => b.addEventListener("click", () => { S.enqTab = b.dataset.tab; m.querySelectorAll("[data-tab]").forEach((x) => x.setAttribute("aria-selected", x === b)); drawEnq(m.querySelector("#enq-list"), 6); }));
  m.querySelector("#me-menu").addEventListener("click", (e) => { e.stopPropagation(); const w = e.currentTarget.parentElement; if (w.querySelector(".menu-pop")) return w.querySelector(".menu-pop").remove();
    w.insertAdjacentHTML("beforeend", `<div class="menu-pop"><button data-go2="settings">Account &amp; security</button><a href="${CFG.site}/" target="_blank" rel="noopener noreferrer">Open the website</a><button data-out>Sign out</button></div>`);
    w.querySelector("[data-go2]").addEventListener("click", () => go("settings")); w.querySelector("[data-out]").addEventListener("click", signOut); });
  drawEnq(m.querySelector("#enq-list"), 6); animate(m);
};
function auditLine(a) {
  const n = a.new || {}, o = a.old || {};
  if (a.tbl === "site_settings") return `Updated ${String(a.row_key || "").replace(/_/g, " ")}`;
  if (a.tbl === "enquiries") return a.action === "DELETE" ? `Deleted enquiry from ${o.name || ""}` : `Enquiry ${n.name || ""} → ${stLabel(n.status)}`;
  if (a.tbl === "customizations") return `Order → ${stLabel(n.status || o.status)}`;
  if (a.tbl === "reviews") return a.action === "DELETE" ? "Deleted a review" : `Review ${n.approved ? "approved" : "hidden"}`;
  if (a.tbl === "invitations") return `Design ${n.name || a.row_key} updated`;
  return `${a.action} ${a.tbl}`;
}
async function signOut() { await sb.auth.signOut(); S.user = null; login(); }

function drawEnq(box, limit = 0) {
  let rows = (S.enq || []).filter((r) => S.enqTab === "all" || r.status === S.enqTab);
  const qq = S.enqQ.trim().toLowerCase();
  if (qq) rows = rows.filter((r) => [r.name, r.phone, r.email, r.city, r.design_slug, r.message].some((v) => String(v || "").toLowerCase().includes(qq)));
  if (limit) rows = rows.slice(0, limit);
  if (!rows.length) { box.innerHTML = empty(S.enq?.length ? "No enquiries in this list." : "No enquiries yet. They appear here as soon as someone writes to you."); return; }
  box.innerHTML = rows.map((r, k) => `<div class="item"><span class="av c${k % 6}">${esc(initials(r.name))}</span>
    <div class="t"><b>${esc(r.name)}</b><span>${esc([r.package, r.design_slug && r.design_slug.replace(/-/g, " "), r.city, r.wedding_date && "Wedding " + fdate(r.wedding_date)].filter(Boolean).join(" · ") || r.source)}</span></div>
    <span class="val">${pill(r.status)}</span><span class="val">${r.deal_value ? "<b>" + inr(r.deal_value) + "</b>" : esc(ago(r.created_at))}</span>
    <button class="btn btn-sm" data-open="${esc(r.id)}">Open</button></div>`).join("");
  box.querySelectorAll("[data-open]").forEach((b) => b.addEventListener("click", () => enqDrawer(b.dataset.open)));
}

function drawer(html, onMount) {
  const s = document.createElement("div"); s.className = "scrim"; s.innerHTML = `<div class="drawer" role="dialog" aria-modal="true">${html}</div>`;
  const close = () => { s.remove(); document.removeEventListener("keydown", key); };
  const key = (e) => { if (e.key === "Escape") close(); };
  s.addEventListener("click", (e) => { if (e.target === s || e.target.closest("[data-close]")) close(); });
  document.addEventListener("keydown", key); document.body.appendChild(s); onMount?.(s.firstElementChild, close);
  s.querySelector("input,select,textarea,button")?.focus();
}
function enqDrawer(id) {
  const r = (S.enq || []).find((x) => x.id === id); if (!r) return;
  const wa = waLink(r.phone), tel = digits(r.phone);
  drawer(`<div class="row" style="justify-content:space-between"><h2>${esc(r.name)}</h2><button class="icon-btn" data-close aria-label="Close">${ic("x")}</button></div>
    <p class="muted small" style="margin:4px 0 0">Received ${esc(fdate(r.created_at))} · from the ${esc(r.source)} form</p>
    <div class="actions">${wa ? `<a class="btn btn-sm" href="${wa}" target="_blank" rel="noopener noreferrer">WhatsApp</a>` : ""}${tel ? `<a class="btn btn-ghost btn-sm" href="tel:+${tel.length === 10 ? "91" + tel : tel}">Call</a>` : ""}${okEmail(r.email) ? `<a class="btn btn-ghost btn-sm" href="mailto:${encodeURIComponent(r.email)}">Email</a>` : ""}</div>
    <dl class="info"><dt>Phone</dt><dd>${esc(r.phone || "—")}</dd><dt>Email</dt><dd>${esc(r.email || "—")}</dd><dt>Wedding date</dt><dd>${esc(r.wedding_date ? fdate(r.wedding_date) : "—")}</dd>
      <dt>City</dt><dd>${esc(r.city || "—")}</dd><dt>Package</dt><dd>${esc(r.package || "—")}</dd><dt>Design</dt><dd>${esc(r.design_slug || "—")}</dd><dt>Message</dt><dd>${esc(r.message || "—")}</dd></dl>
    <form id="ef" novalidate><div class="grid2"><div><label class="f" for="e-st">Status</label><select class="in" id="e-st">${ENQ_ST.map((s) => `<option value="${s}"${s === r.status ? " selected" : ""}>${stLabel(s)}</option>`).join("")}</select></div>
      <div><label class="f" for="e-val">Booked value (₹)</label><input class="in" id="e-val" inputmode="numeric" value="${esc(r.deal_value ?? "")}" placeholder="e.g. 8999"></div>
      <div><label class="f" for="e-adv">Advance received (₹)</label><input class="in" id="e-adv" inputmode="numeric" value="${esc(r.advance_paid ?? "")}" placeholder="e.g. 4500"></div></div>
      <label class="f" for="e-note" style="margin-top:12px">Private note</label><textarea class="in" id="e-note" maxlength="2000" placeholder="Only you can see this">${esc(r.admin_note || "")}</textarea>
      <div class="row" style="margin-top:14px;justify-content:space-between"><button class="btn" type="submit">Save</button><button class="btn btn-danger btn-sm" type="button" id="e-del">Delete enquiry</button></div></form>`,
  (d, close) => {
    d.querySelector("#ef").addEventListener("submit", async (e) => {
      e.preventDefault();
      const val = d.querySelector("#e-val").value.trim(), adv = d.querySelector("#e-adv").value.trim();
      const patch = { status: d.querySelector("#e-st").value, admin_note: d.querySelector("#e-note").value.slice(0, 2000) || null,
        deal_value: val ? intIn(val) : null, advance_paid: adv ? intIn(adv) : null, updated_at: new Date().toISOString() };
      if ((val && patch.deal_value === null) || (adv && patch.advance_paid === null)) return toast("Amounts must be whole rupees.", true);
      if (!ENQ_ST.includes(patch.status)) return;
      try { await q(sb.from("enquiries").update(patch).eq("id", r.id)); Object.assign(r, patch); toast("Saved"); close(); go(S.view); } catch (err) { fail(err); }
    });
    d.querySelector("#e-del").addEventListener("click", async () => {
      if (!confirm(`Delete the enquiry from ${r.name}? This can't be undone.`)) return;
      try { await q(sb.from("enquiries").delete().eq("id", r.id)); S.enq = S.enq.filter((x) => x.id !== r.id); toast("Deleted"); close(); go(S.view); } catch (err) { fail(err); }
    });
  });
}

RENDER.enquiries = async (m) => {
  await load.enq();
  const c = (s) => (S.enq || []).filter((r) => s === "all" || r.status === s).length;
  m.innerHTML = `${head("Enquiries", "Everyone who wrote to you from the website. Open one to call, WhatsApp, set the status and track money.",
    `<label class="search"><span class="sr">Search enquiries</span>${ic("search", 16)}<input class="in" id="q" type="search" placeholder="Search name, phone, city…" value="${esc(S.enqQ)}"></label>`)}
    <div class="sec-h"><div class="tabs" role="tablist">${["all", ...ENQ_ST].map((t) => `<button role="tab" type="button" data-tab="${t}" aria-selected="${S.enqTab === t}">${t === "all" ? "All" : stLabel(t)} (${c(t)})</button>`).join("")}</div>
    <button class="btn btn-ghost btn-sm" id="csv">Download CSV</button></div><div class="list" id="enq-list"></div>`;
  const box = m.querySelector("#enq-list");
  m.querySelectorAll("[data-tab]").forEach((b) => b.addEventListener("click", () => { S.enqTab = b.dataset.tab; m.querySelectorAll("[data-tab]").forEach((x) => x.setAttribute("aria-selected", x === b)); drawEnq(box); }));
  m.querySelector("#q").addEventListener("input", (e) => { S.enqQ = e.target.value; drawEnq(box); });
  m.querySelector("#csv").addEventListener("click", () => csv("bfiluxe-enquiries.csv", S.enq, ["created_at", "name", "phone", "email", "wedding_date", "city", "package", "design_slug", "status", "deal_value", "advance_paid", "message", "admin_note", "source"]));
  drawEnq(box);
};
function csv(name, rows, cols) {
  const cell = (v) => { let s = String(v ?? ""); if (/^[=+\-@\t\r]/.test(s)) s = "'" + s; return '"' + s.replace(/"/g, '""') + '"'; };
  const text = [cols.join(","), ...(rows || []).map((r) => cols.map((c) => cell(r[c])).join(","))].join("\r\n");
  const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob(["﻿" + text], { type: "text/csv" })); a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
}

RENDER.orders = async (m) => {
  await Promise.all([load.orders(), S.customers ? 0 : load.customers().catch(() => (S.customers = []))]);
  m.innerHTML = `${head("Orders", "Invitations customers started or sent from the order form. Move each one along as you work on it.")}
    <div class="sec-h"><div class="tabs" role="tablist">${["all", ...ORD_ST].map((t) => `<button role="tab" type="button" data-tab="${t}" aria-selected="${S.ordTab === t}">${t === "all" ? "All" : stLabel(t)}</button>`).join("")}</div></div><div class="list" id="ord-list"></div>`;
  const box = m.querySelector("#ord-list");
  const draw = () => {
    const rows = (S.orders || []).filter((r) => S.ordTab === "all" || r.status === S.ordTab);
    if (!rows.length) { box.innerHTML = empty("No orders here yet."); return; }
    box.innerHTML = rows.map((r, k) => { const d = r.data || {}; return `<div class="item"><span class="av c${k % 6}">${esc(initials(d.bride || d.groom || d.name || custEmail(r.user_id)))}</span>
      <div class="t"><b>${esc([d.bride, d.groom].filter(Boolean).join(" & ") || d.name || custEmail(r.user_id))}</b><span>${esc([r.design_slug && r.design_slug.replace(/-/g, " "), d.package, custEmail(r.user_id)].filter(Boolean).join(" · "))}</span></div>
      <span class="val">${pill(r.status)}</span><span class="val">${esc(ago(r.updated_at))}</span><button class="btn btn-sm" data-open="${esc(r.id)}">Open</button></div>`; }).join("");
    box.querySelectorAll("[data-open]").forEach((b) => b.addEventListener("click", () => ordDrawer(b.dataset.open, draw)));
  };
  m.querySelectorAll("[data-tab]").forEach((b) => b.addEventListener("click", () => { S.ordTab = b.dataset.tab; m.querySelectorAll("[data-tab]").forEach((x) => x.setAttribute("aria-selected", x === b)); draw(); }));
  draw();
};
function flat(o, pre = "") {
  const out = [];
  for (const [k, v] of Object.entries(o || {})) {
    if (v && typeof v === "object" && !Array.isArray(v)) out.push(...flat(v, pre + k + " › "));
    else if (Array.isArray(v)) out.push([pre + k, v.map((x) => (typeof x === "object" ? Object.values(x || {}).join(" · ") : x)).join(" | ")]);
    else out.push([pre + k, v]);
  }
  return out;
}
function ordDrawer(id, redraw) {
  const r = (S.orders || []).find((x) => x.id === id); if (!r) return;
  const rows = flat(r.data).filter(([, v]) => v !== "" && v !== null && v !== undefined).slice(0, 80);
  drawer(`<div class="row" style="justify-content:space-between"><h2>Order</h2><button class="icon-btn" data-close aria-label="Close">${ic("x")}</button></div>
    <p class="muted small" style="margin:4px 0 0">${esc(custEmail(r.user_id))} · started ${esc(fdate(r.created_at))} · updated ${esc(ago(r.updated_at))}</p>
    <dl class="info"><dt>Design</dt><dd>${esc(r.design_slug || "—")}</dd>${rows.map(([k, v]) => `<dt>${esc(k.replace(/_/g, " "))}</dt><dd>${esc(v)}</dd>`).join("")}</dl>
    <form id="of" novalidate><label class="f" for="o-st">Status</label><select class="in" id="o-st">${ORD_ST.map((s) => `<option value="${s}"${s === r.status ? " selected" : ""}>${stLabel(s)}</option>`).join("")}</select>
    <label class="f" for="o-note" style="margin-top:12px">Private note</label><textarea class="in" id="o-note" maxlength="2000">${esc(r.admin_note || "")}</textarea>
    <div class="row" style="margin-top:14px"><button class="btn" type="submit">Save</button></div></form>`,
  (d, close) => d.querySelector("#of").addEventListener("submit", async (e) => {
    e.preventDefault(); const patch = { status: d.querySelector("#o-st").value, admin_note: d.querySelector("#o-note").value.slice(0, 2000) || null, updated_at: new Date().toISOString() };
    if (!ORD_ST.includes(patch.status)) return;
    try { await q(sb.from("customizations").update(patch).eq("id", r.id)); Object.assign(r, patch); toast("Saved"); close(); redraw(); } catch (err) { fail(err); }
  }));
}

RENDER.prices = async (m) => {
  await Promise.all([load.settings(), load.designs()]);
  const tierForm = (key, title, sub) => { const v = S.settings[key] || {}; return `<div class="card"><div class="sec-h"><div><h2>${title}</h2><p class="muted small" style="margin:2px 0 0">${sub}</p></div><button class="btn" data-save="${key}">Save ${title.toLowerCase()}</button></div>
    <div class="tiers">${["Basic", "Premium", "Luxury"].map((t) => { const p = v[t] || {}; return `<div class="tier ${t.toLowerCase()}" data-k="${key}" data-t="${t}"><div class="tier-h"><b>${t}</b><span class="off" data-off></span></div><div class="tier-b">
      <label class="f">Price customers pay (₹)<input class="in" data-f="price" inputmode="numeric" value="${esc(p.price ?? "")}"></label>
      <label class="f">Regular price shown struck through (₹, optional)<input class="in" data-f="mrp" inputmode="numeric" value="${esc(p.mrp ?? "")}"></label>
      <label class="f">Delivery time<input class="in" data-f="days" maxlength="40" value="${esc(p.days ?? "")}"></label>
      <div class="preview" data-pv></div></div></div>`; }).join("")}</div></div>`; };
  m.innerHTML = `${head("Prices", "Change a price here and the website shows it within a minute: package cards, pricing, videos, design pages and the order form.")}
    ${tierForm("packages", "Website packages", "Invitation websites")}
    <div class="row" style="margin:-6px 0 16px 4px"><label class="switch"><input type="checkbox" id="sync-designs" checked><i></i></label><label for="sync-designs" class="small">When I save website packages, set every design in that package to the same price</label></div>${tierForm("video_packages", "Video packages", "Invitation videos")}
    <div class="card"><div class="sec-h"><div><h2>Price per design</h2><p class="muted small" style="margin:2px 0 0">A design's "From" price. It can't be lower than its package price.</p></div></div>
    <div class="tbl-wrap"><table class="t"><thead><tr><th></th><th>Design</th><th>Package</th><th>From (₹)</th><th></th></tr></thead><tbody>${(S.designs || []).map((d) => `<tr data-slug="${esc(d.slug)}"><td><img class="thumb" src="${cover(d.slug)}" alt="" loading="lazy"></td><td><b>${esc(d.name)}</b></td><td>${esc(d.tier)}</td>
      <td><input class="in" data-dp inputmode="numeric" value="${esc(d.price_from)}" style="max-width:120px" aria-label="${esc(d.name)} price"></td><td><button class="btn btn-sm" data-dsave>Save</button></td></tr>`).join("")}</tbody></table></div></div>
    <p class="note">Tip: the struck-through price must be a real regular price you charge outside offers. Indian consumer rules don't allow invented "was" prices.</p>`;
  const pv = (tier) => { const g = (f) => intIn(tier.querySelector(`[data-f="${f}"]`).value); const p = g("price"), r = g("mrp");
    const off = p && r && r > p ? Math.round((r - p) * 100 / r) : 0; tier.querySelector("[data-off]").textContent = off ? off + "% off" : "";
    tier.querySelector("[data-pv]").innerHTML = p === null ? '<span class="err">Enter a price</span>' : `${off ? `<s>${inr(r)}</s>` : ""}<b>${inr(p)}</b><span class="muted small">${esc(tier.querySelector('[data-f="days"]').value)}</span>`; };
  m.querySelectorAll(".tier").forEach((t) => { pv(t); t.addEventListener("input", () => pv(t)); });
  m.querySelectorAll("[data-save]").forEach((b) => b.addEventListener("click", async () => {
    const key = b.dataset.save, val = {};
    for (const t of m.querySelectorAll(`.tier[data-k="${key}"]`)) {
      const g = (f) => t.querySelector(`[data-f="${f}"]`).value.trim(); const price = intIn(g("price")), mrpRaw = g("mrp"), mrp = mrpRaw ? intIn(mrpRaw) : null, days = g("days").slice(0, 40);
      if (!price) return toast(`${t.dataset.t}: enter a price in whole rupees.`, true);
      if (mrpRaw && (mrp === null || mrp <= price)) return toast(`${t.dataset.t}: the regular price must be higher than the price, or empty.`, true);
      if (!days) return toast(`${t.dataset.t}: enter the delivery time.`, true);
      val[t.dataset.t] = { price, mrp, days };
    }
    b.disabled = true;
    try {
      await q(sb.from("site_settings").upsert({ key, value: val, updated_at: new Date().toISOString() })); S.settings[key] = val;
      if (key === "packages" && m.querySelector("#sync-designs")?.checked) {
        for (const t of ["Basic", "Premium", "Luxury"]) {
          if (!(S.designs || []).some((d) => d.tier === t && d.price_from !== val[t].price)) continue;
          await q(sb.from("invitations").update({ price_from: val[t].price }).eq("tier", t));
          S.designs.forEach((d) => { if (d.tier === t) d.price_from = val[t].price; });
          m.querySelectorAll("tr[data-slug]").forEach((tr) => { const d = S.designs.find((x) => x.slug === tr.dataset.slug); if (d) tr.querySelector("[data-dp]").value = d.price_from; });
        }
      }
      toast("Saved. The website shows the new prices now.");
    } catch (e) { fail(e); }
    b.disabled = false;
  }));
  m.querySelectorAll("[data-dsave]").forEach((b) => b.addEventListener("click", async () => {
    const tr = b.closest("tr"), d = S.designs.find((x) => x.slug === tr.dataset.slug), p = intIn(tr.querySelector("[data-dp]").value);
    const base = S.settings.packages?.[d.tier]?.price || 0;
    if (!p) return toast("Enter a price in whole rupees.", true);
    if (p < base) return toast(`${d.tier} designs can't be below the ${d.tier} package price (${inr(base)}).`, true);
    b.disabled = true; try { await q(sb.from("invitations").update({ price_from: p }).eq("slug", d.slug)); d.price_from = p; toast(`${d.name} saved`); } catch (e) { fail(e); } b.disabled = false;
  }));
};

RENDER.designs = async (m) => {
  await load.designs();
  m.innerHTML = `${head("Designs", "Rename designs, change their package and short line, reorder them or hide one from the website.")}
    <div class="tbl-wrap"><table class="t"><thead><tr><th></th><th>Name</th><th>Short line</th><th>Package</th><th>Order</th><th>Shown</th><th></th></tr></thead><tbody>${(S.designs || []).map((d) => `<tr data-slug="${esc(d.slug)}">
      <td><img class="thumb" src="${cover(d.slug)}" alt="" loading="lazy"></td>
      <td><input class="in" data-f="name" maxlength="60" value="${esc(d.name)}" aria-label="Name"></td>
      <td><input class="in" data-f="tagline" maxlength="120" value="${esc(d.tagline)}" aria-label="Short line" style="min-width:220px"></td>
      <td><select class="in" data-f="tier" aria-label="Package">${["Basic", "Premium", "Luxury"].map((t) => `<option${t === d.tier ? " selected" : ""}>${t}</option>`).join("")}</select></td>
      <td><input class="in" data-f="sort" inputmode="numeric" value="${esc(d.sort)}" style="max-width:70px" aria-label="Order"></td>
      <td><label class="switch"><input type="checkbox" data-f="active"${d.active ? " checked" : ""} aria-label="Show on website"><i></i></label></td>
      <td><div class="row"><button class="btn btn-sm" data-save>Save</button><a class="icon-btn" href="${CFG.site}/design-${encodeURIComponent(d.slug)}.html" target="_blank" rel="noopener noreferrer" aria-label="Open design page">${ic("ext", 18)}</a></div></td></tr>`).join("")}</tbody></table></div>
    <p class="note" style="margin-top:14px">Hiding a design removes it from the invitations page and order form straight away. Its own page stays reachable by direct link until the next site update.</p>`;
  m.querySelectorAll("[data-save]").forEach((b) => b.addEventListener("click", async () => {
    const tr = b.closest("tr"), d = S.designs.find((x) => x.slug === tr.dataset.slug), g = (f) => tr.querySelector(`[data-f="${f}"]`);
    const patch = { name: g("name").value.trim().slice(0, 60), tagline: g("tagline").value.trim().slice(0, 120), tier: g("tier").value, sort: intIn(g("sort").value) ?? d.sort, active: g("active").checked };
    if (!patch.name) return toast("Name can't be empty.", true);
    if (!["Basic", "Premium", "Luxury"].includes(patch.tier)) return;
    b.disabled = true; try { await q(sb.from("invitations").update(patch).eq("slug", d.slug)); Object.assign(d, patch); toast(`${patch.name} saved`); } catch (e) { fail(e); } b.disabled = false;
  }));
};

RENDER.reviews = async (m) => {
  await load.reviews();
  m.innerHTML = `${head("Reviews", "Reviews customers wrote. Only approved ones show on the website.")}
    <div class="sec-h"><div class="tabs" role="tablist">${[["pending", "Waiting"], ["approved", "Approved"], ["all", "All"]].map(([k, t]) => `<button role="tab" type="button" data-tab="${k}" aria-selected="${S.revTab === k}">${t}</button>`).join("")}</div></div><div class="list" id="rev"></div>`;
  const box = m.querySelector("#rev");
  const draw = () => {
    const rows = (S.reviews || []).filter((r) => S.revTab === "all" || (S.revTab === "approved" ? r.approved : !r.approved));
    if (!rows.length) { box.innerHTML = empty("No reviews here yet."); return; }
    box.innerHTML = rows.map((r, k) => `<div class="card" style="margin:0"><div class="row" style="justify-content:space-between"><div class="row"><span class="item" style="all:unset"><span class="av c${k % 6}" style="width:40px;height:40px;border-radius:12px;display:grid;place-items:center;font-weight:600">${esc(initials(r.name))}</span></span>
      <div><b>${esc(r.name)}</b><div class="muted small">${esc([r.city, r.design_slug, fdate(r.created_at)].filter(Boolean).join(" · "))}</div></div></div><span aria-label="${r.rating} out of 5">${"★".repeat(Math.max(0, Math.min(5, r.rating)))}<span class="muted">${"★".repeat(5 - Math.max(0, Math.min(5, r.rating)))}</span></span></div>
      <p style="margin:10px 0 12px">${esc(r.body)}</p><div class="row">${pill(r.approved ? "approved" : "pending")}<span style="flex:1"></span>
      <button class="btn btn-sm${r.approved ? " btn-ghost" : ""}" data-ap="${esc(r.id)}">${r.approved ? "Hide from website" : "Approve"}</button><button class="btn btn-danger btn-sm" data-del="${esc(r.id)}">Delete</button></div></div>`).join("");
    box.querySelectorAll("[data-ap]").forEach((b) => b.addEventListener("click", async () => { const r = S.reviews.find((x) => x.id === b.dataset.ap);
      try { await q(sb.from("reviews").update({ approved: !r.approved }).eq("id", r.id)); r.approved = !r.approved; toast(r.approved ? "Approved: now on the website" : "Hidden"); draw(); } catch (e) { fail(e); } }));
    box.querySelectorAll("[data-del]").forEach((b) => b.addEventListener("click", async () => { if (!confirm("Delete this review for good?")) return;
      try { await q(sb.from("reviews").delete().eq("id", b.dataset.del)); S.reviews = S.reviews.filter((x) => x.id !== b.dataset.del); toast("Deleted"); draw(); } catch (e) { fail(e); } }));
  };
  m.querySelectorAll("[data-tab]").forEach((b) => b.addEventListener("click", () => { S.revTab = b.dataset.tab; m.querySelectorAll("[data-tab]").forEach((x) => x.setAttribute("aria-selected", x === b)); draw(); }));
  draw();
};

RENDER.customers = async (m) => {
  await load.customers();
  m.innerHTML = `${head("Customers", `${num(S.customers.length)} accounts on the website.`, '<button class="btn btn-ghost btn-sm" id="csv">Download CSV</button>')}
    ${S.customers.length ? `<div class="tbl-wrap"><table class="t"><thead><tr><th>Customer</th><th>Phone</th><th>Signed up with</th><th>Joined</th><th>Last sign-in</th><th>Orders</th><th>Saved</th></tr></thead><tbody>${S.customers.map((c) => `<tr>
      <td><b>${esc(c.name || "—")}</b><div class="muted small">${esc(c.email)}</div></td><td>${esc(c.phone || "—")}</td><td>${esc(c.provider === "google" ? "Google" : "Email")}</td>
      <td>${esc(fdate(c.created_at))}</td><td>${esc(c.last_sign_in_at ? ago(c.last_sign_in_at) : "Never")}</td><td>${num(c.orders)}</td><td>${num(c.favorites)}</td></tr>`).join("")}</tbody></table></div>` : empty("No customer accounts yet.")}`;
  m.querySelector("#csv")?.addEventListener("click", () => csv("bfiluxe-customers.csv", S.customers, ["email", "name", "phone", "provider", "created_at", "last_sign_in_at", "orders", "favorites"]));
};

RENDER.analytics = async (m) => {
  await load.stats(); badges();
  const st = S.stats, daily = st.daily || [], maxD = Math.max(1, ...daily.map((d) => d.views));
  const growth = st.views_prev ? Math.round((st.views - st.views_prev) * 100 / st.views_prev) : null;
  const bars = (rows, label, val) => { const mx = Math.max(1, ...rows.map(val)); return rows.length ? `<div class="kv">${rows.map((r) => `<div><span>${esc(label(r))}</span><b>${num(val(r))}</b><div class="bar"><i data-w="${Math.round(val(r) * 100 / mx)}"></i></div></div>`).join("")}</div>` : '<p class="muted small">No data yet.</p>'; };
  m.innerHTML = `${head("Analytics", "Visits and clicks on bfiluxe.com. No cookies, no personal data: just counts.",
    `<div class="tabs" role="tablist">${[7, 30, 90].map((d) => `<button role="tab" type="button" data-days="${d}" aria-selected="${S.days === d}">${d} days</button>`).join("")}</div>`)}
    <div class="tiles" style="grid-template-columns:repeat(4,minmax(0,1fr));margin-bottom:16px">
      <div class="tile"><b>${num(st.views)}</b><span>Page views${growth === null ? "" : `<br>${growth >= 0 ? "+" : ""}${growth}% vs before`}</span></div>
      <div class="tile"><b>${num(st.visitors)}</b><span>Visitors</span></div><div class="tile"><b>${num(st.enquiries)}</b><span>Enquiries</span></div>
      <div class="tile"><b>${st.visitors ? ((st.enquiries * 100) / st.visitors).toFixed(1) : "0"}%</b><span>Visitors who<br>enquired</span></div></div>
    <div class="card"><div class="sec-h"><h2>Page views per day</h2></div>${daily.length ? `<div class="chart">${daily.map((d) => `<div class="col" title="${esc(fdate(d.day))}: ${d.views} views, ${d.visitors} visitors"><i data-w="${Math.round(d.views * 100 / maxD)}" data-prop="height"></i><small>${esc(new Date(d.day).getDate())}</small></div>`).join("")}</div>` : '<p class="muted small">No visits yet in this period.</p>'}</div>
    <div class="grid2" style="margin-top:16px"><div class="card" style="margin:0"><div class="sec-h"><h2>Top pages</h2></div>${bars(st.pages || [], (r) => (r.page || "/").replace(/^\//, "") || "Home", (r) => r.views)}</div>
      <div class="card" style="margin:0"><div class="sec-h"><h2>Where visitors come from</h2></div>${bars(st.referrers || [], (r) => r.ref, (r) => r.n)}</div>
      <div class="card" style="margin:0"><div class="sec-h"><h2>What visitors click</h2></div>${bars(st.events || [], (r) => EVN[r.name] || r.name.replace(/_/g, " "), (r) => r.n)}</div>
      <div class="card" style="margin:0"><div class="sec-h"><h2>Designs</h2></div>${bars(st.designs || [], (r) => `${r.name} · ${r.enquiries} enq · ${r.favorites} saved`, (r) => r.views)}</div></div>`;
  m.querySelectorAll("[data-days]").forEach((b) => b.addEventListener("click", () => { S.days = +b.dataset.days; go("analytics"); }));
  animate(m);
};

RENDER.settings = async (m) => {
  await Promise.all([load.settings(), load.audit()]);
  const an = S.settings.announcement || {};
  const { data: fl } = await sb.auth.mfa.listFactors();
  const factors = (fl?.totp || []).filter((f) => f.status === "verified");
  m.innerHTML = `${head("Settings", "Website offer bar, your account and a record of every change.")}
    <div class="grid2"><div class="card" style="margin:0"><div class="sec-h"><h2>Offer bar on the website</h2></div>
      <form id="anf" novalidate><div class="row" style="margin-bottom:12px"><label class="switch"><input type="checkbox" id="an-on"${an.on ? " checked" : ""}><i></i></label><label for="an-on">Show a thin bar at the top of every page</label></div>
      <label class="f" for="an-t">Text (up to 120 characters)</label><input class="in" id="an-t" maxlength="120" value="${esc(an.text || "")}" placeholder="Wedding season offer: up to 40% off until 31 January">
      <label class="f" for="an-l" style="margin-top:12px">Link (optional, a bfiluxe.com page or WhatsApp)</label><input class="in" id="an-l" maxlength="200" value="${esc(an.link || "")}" placeholder="https://bfiluxe.com/pricing.html">
      <div class="row" style="margin-top:14px"><button class="btn" type="submit">Save offer bar</button></div></form></div>
    <div class="card" style="margin:0"><div class="sec-h"><h2>Your account</h2></div>
      <dl class="info" style="margin:0 0 14px;box-shadow:none;background:#FBF8F2"><dt>Email</dt><dd>${esc(S.user?.email)}</dd><dt>Two-step sign-in</dt><dd>${factors.length ? `On · ${esc(factors[0].friendly_name || "authenticator app")}` : "Off"}</dd><dt>Auto sign-out</dt><dd>After ${IDLE_MIN} minutes without activity, and when you close the tab</dd></dl>
      <form id="pwf" novalidate><label class="f" for="p1">New password (12+ characters)</label><input class="in" id="p1" type="password" autocomplete="new-password" minlength="12" maxlength="200">
      <label class="f" for="p2" style="margin-top:10px">Type it again</label><input class="in" id="p2" type="password" autocomplete="new-password" maxlength="200">
      <div class="row" style="margin-top:14px"><button class="btn" type="submit">Change password</button><button class="btn btn-ghost" type="button" id="out-all">Sign out on all devices</button></div></form></div></div>
    <div class="card"><div class="sec-h"><h2>Change history</h2><span class="muted small">Every change made in this admin, newest first</span></div>
      ${(S.audit || []).length ? `<div class="tbl-wrap"><table class="t"><thead><tr><th>When</th><th>Who</th><th>What</th></tr></thead><tbody>${S.audit.map((a) => `<tr><td>${esc(new Date(a.at).toLocaleString("en-IN"))}</td><td>${esc(a.who || "—")}</td><td>${esc(auditLine(a))}</td></tr>`).join("")}</tbody></table></div>` : '<p class="muted small">No changes yet.</p>'}</div>`;
  m.querySelector("#anf").addEventListener("submit", async (e) => {
    e.preventDefault(); const link = m.querySelector("#an-l").value.trim();
    if (link && !/^(https:\/\/(bfiluxe\.com|www\.bfiluxe\.com|wa\.me)(\/|$)|\/[^/])/.test(link)) return toast("The link must be a bfiluxe.com page or a wa.me WhatsApp link.", true);
    const value = { on: m.querySelector("#an-on").checked, text: m.querySelector("#an-t").value.trim().slice(0, 120), link };
    if (value.on && !value.text) return toast("Write the offer text first.", true);
    try { await q(sb.from("site_settings").upsert({ key: "announcement", value, updated_at: new Date().toISOString() })); S.settings.announcement = value; toast("Saved"); } catch (err) { fail(err); }
  });
  m.querySelector("#pwf").addEventListener("submit", async (e) => {
    e.preventDefault(); const a = m.querySelector("#p1").value, b = m.querySelector("#p2").value;
    if (a.length < 12) return toast("Use at least 12 characters.", true);
    if (a !== b) return toast("The two passwords don't match.", true);
    const { error } = await sb.auth.updateUser({ password: a });
    m.querySelector("#p1").value = m.querySelector("#p2").value = "";
    if (error) return toast(error.message.includes("same") ? "Choose a new password, not the current one." : "Could not change it: " + error.message, true);
    toast("Password changed.");
  });
  m.querySelector("#out-all").addEventListener("click", async () => { if (!confirm("Sign out on every device, including this one?")) return; await sb.auth.signOut({ scope: "global" }); S.user = null; login("Signed out everywhere."); });
};

gate().catch(() => login());
})();
