/* BFI live-demo runtime: shared by /live-demo-1 … /live-demo-5.
   Everything here is a sample: dates are always in the future, RSVPs are never sent anywhere. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const html = document.documentElement;
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const params = new URLSearchParams(location.search);

  /* ---- dates: every date is "N days from today", so the sample never goes stale ---- */
  const at = (n, t = "00:00") => { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() + +n); const [h, m] = t.split(":"); d.setHours(+h, +m); return d; };
  const FMT = { long: { weekday: "long", day: "numeric", month: "long", year: "numeric" }, dm: { day: "numeric", month: "long" }, short: { day: "numeric", month: "short" },
    day: { day: "numeric" }, month: { month: "short" }, monthlong: { month: "long" }, wd: { weekday: "long" }, wds: { weekday: "short" }, year: { year: "numeric" }, time: { hour: "numeric", minute: "2-digit" } };
  $$("[data-day]").forEach((el) => {
    if (el.matches("[data-countdown],[data-ics]")) return;
    el.textContent = at(el.dataset.day, el.dataset.time).toLocaleString(el.dataset.loc || "en-IN", FMT[el.dataset.fmt || "long"]);
  });

  /* ---- countdown ---- */
  $$("[data-countdown]").forEach((box) => {
    const target = at(box.dataset.day, box.dataset.time); let timer;
    const tick = () => {
      let t = target - new Date();
      if (t <= 0) { clearInterval(timer); box.innerHTML = `<p class="ld-done">${box.dataset.done || "The celebrations have begun. Thank you for your blessings."}</p>`; return; }
      for (const [k, u] of [["d", 864e5], ["h", 36e5], ["m", 6e4], ["s", 1e3]]) { const v = Math.floor(t / u); t -= v * u; const el = $(`[data-u=${k}]`, box); if (el) el.textContent = String(v).padStart(k === "d" ? 1 : 2, "0"); }
    };
    tick(); timer = setInterval(tick, 1000);
  });

  /* ---- directions: sample venues are fictional, so maps open the real locality ---- */
  $$("[data-dir]").forEach((a) => { a.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(a.dataset.dir + ", India")}`; a.target = "_blank"; a.rel = "noopener"; });
  $$("iframe[data-map]").forEach((f) => { f.src = `https://maps.google.com/maps?q=${encodeURIComponent(f.dataset.map + ", India")}&z=14&hl=en&output=embed`; });

  /* ---- add to calendar (.ics download) ---- */
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-ics]"); if (!b) return;
    const st = at(b.dataset.day, b.dataset.time), en = new Date(st.getTime() + (+b.dataset.hours || 3) * 36e5);
    const z = (x) => x.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
    const body = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//BFI//Sample invitation//EN", "BEGIN:VEVENT", `UID:${Date.now()}@bfi-sample`, `DTSTAMP:${z(new Date())}`,
      `DTSTART:${z(st)}`, `DTEND:${z(en)}`, `SUMMARY:${b.dataset.ics}`, `LOCATION:${b.dataset.place || ""}`, "DESCRIPTION:Sample invitation by BFI Marwari Invitations", "END:VEVENT", "END:VCALENDAR"].join("\r\n");
    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([body], { type: "text/calendar" })); a.download = b.dataset.ics.replace(/\W+/g, "-") + ".ics"; a.click();
    toast("Calendar file downloaded");
  });

  /* ---- toast ---- */
  let toastT;
  function toast(msg) {
    let t = $(".ld-toast"); if (!t) { t = document.createElement("div"); t.className = "ld-toast"; t.setAttribute("role", "status"); document.body.append(t); }
    t.textContent = msg; t.classList.add("on"); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove("on"), 2400);
  }

  /* ---- sample ribbon (always visible, so nobody mistakes a demo for a real wedding) ---- */
  const rib = document.createElement("div"); rib.className = "ld-ribbon";
  rib.innerHTML = `<span class="l"><b>Sample invitation by BFI</b> · names, venues and photos are fictional</span><span class="s"><b>Sample</b> · fictional names</span><a href="../customize.html">Create yours</a>`;
  document.body.prepend(rib);

  /* ---- opening sequence ---- */
  const cover = $("[data-cover]");
  const open = () => {
    if (!cover || cover.classList.contains("is-open")) return;
    cover.classList.add("is-open"); html.classList.add("opened");
    setTimeout(() => { cover.remove(); html.classList.remove("locked"); document.dispatchEvent(new Event("ld:open")); $("main")?.focus({ preventScroll: true }); }, still ? 0 : +(cover.dataset.dur || 1500));
  };
  if (cover) {
    html.classList.add("locked");
    $$("[data-open]", cover).forEach((b) => b.addEventListener("click", open));
    cover.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } });
    if (params.get("open") === "1") open();
  } else document.dispatchEvent(new Event("ld:open"));

  /* ---- reveal on scroll ---- */
  const io = "IntersectionObserver" in window && !still && new IntersectionObserver((es) => es.forEach((x) => { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }), { rootMargin: "0px 0px -8% 0px" });
  $$("[data-reveal]").forEach((el) => (io ? io.observe(el) : el.classList.add("in")));

  /* ---- language switch (Hindi / English) ---- */
  $$("[data-lang-to]").forEach((b) => b.addEventListener("click", () => {
    html.dataset.lang = b.dataset.langTo; $$("[data-lang-to]").forEach((x) => x.setAttribute("aria-pressed", x.dataset.langTo === b.dataset.langTo));
  }));

  /* ---- music: a soft tanpura-style drone made in the browser; only ever starts on a tap ---- */
  const mb = $("[data-music]"); let ctx, nodes = [];
  mb?.addEventListener("click", () => {
    const on = mb.getAttribute("aria-pressed") !== "true";
    mb.setAttribute("aria-pressed", on); mb.setAttribute("aria-label", on ? "Pause music" : "Play music");
    if (!on) { nodes.forEach((n) => { try { n.stop(); } catch {} }); nodes = []; return; }
    ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
    const g = ctx.createGain(); g.gain.value = 0.0001; g.connect(ctx.destination); g.gain.exponentialRampToValueAtTime(0.05, ctx.currentTime + 2);
    for (const [f, type] of [[130.8, "sine"], [196, "sine"], [261.6, "triangle"], [130.8 * 1.005, "sine"]]) {
      const o = ctx.createOscillator(); o.type = type; o.frequency.value = f;
      const lfo = ctx.createOscillator(), lg = ctx.createGain(); lfo.frequency.value = 0.08 + Math.random() * 0.1; lg.gain.value = 0.6; lfo.connect(lg).connect(o.frequency);
      o.connect(g); o.start(); lfo.start(); nodes.push(o, lfo);
    }
  });

  /* ---- RSVP in steps: validates, then thanks the guest; nothing is sent from a sample ---- */
  $$("form[data-rsvp]").forEach((form) => {
    const steps = $$(".rs-step", form); let i = 0;
    const bar = $(".rs-bar i", form);
    const show = () => { steps.forEach((s, k) => (s.hidden = k !== i)); if (bar) bar.style.width = ((i + 1) / steps.length) * 100 + "%"; $("input,select,textarea,button", steps[i])?.focus({ preventScroll: true }); };
    const ok = () => { const bad = $$("[required]", steps[i]).find((x) => !x.checkValidity()); if (bad) { bad.reportValidity(); return false; } return true; };
    form.addEventListener("click", (e) => {
      if (e.target.closest("[data-next]")) { e.preventDefault(); if (ok()) { i = Math.min(i + 1, steps.length - 1); show(); } }
      if (e.target.closest("[data-back]")) { e.preventDefault(); i = Math.max(i - 1, 0); show(); }
    });
    form.addEventListener("change", (e) => { if (e.target.name === "attending") form.dataset.attending = e.target.value; });
    form.addEventListener("submit", (e) => {
      e.preventDefault(); if (!ok()) return;
      const name = (new FormData(form).get("name") || "").toString().trim().split(" ")[0];
      form.outerHTML = `<div class="rs-done" role="status"><p class="rs-done-t">${form.dataset.thanks || "Thank you"}${name ? ", " + name.replace(/[<>&"]/g, "") : ""}!</p>
        <p>On a real BFI invitation your reply reaches the family's private guest list instantly. This is a sample, so nothing was sent.</p></div>`;
    });
    show();
  });

  /* ---- share ---- */
  $$("[data-share]").forEach((b) => b.addEventListener("click", () => window.open(`https://wa.me/?text=${encodeURIComponent(document.title.split(" · ")[0] + "\n" + location.href.split("?")[0])}`, "_blank", "noopener")));
  $$("[data-copy]").forEach((b) => b.addEventListener("click", async () => { try { await navigator.clipboard.writeText(location.href.split("?")[0]); toast("Link copied"); } catch { toast(location.href.split("?")[0]); } }));
})();
