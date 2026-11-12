/* BFI cinematic invitation engine, shared by /live-demo-1 … /live-demo-5.
   Flow: preloader → cover ("tap to open") → burst transition + music → the invitation, with falling petals,
   a "reveal the date" game, countdown, story, venue, festivities and closing.
   Each page sets window.LD = { burst, petals, music, ... }. Everything is a sample: dates are always in the
   future and RSVPs are never sent anywhere. */
(() => {
  const C = Object.assign({ burst: "swirl", petals: { type: "leaf", colors: ["#D4AF37"], count: 26 }, music: null }, window.LD || {});
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const html = document.documentElement;
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const params = new URLSearchParams(location.search);
  const rnd = (a, b) => a + Math.random() * (b - a);

  /* ---------- dates: always N days from today ---------- */
  const at = (n, t = "00:00") => { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() + +n); const [h, m] = t.split(":"); d.setHours(+h, +m); return d; };
  const FMT = { long: { weekday: "long", day: "numeric", month: "long", year: "numeric" }, dm: { day: "numeric", month: "long" }, day: { day: "numeric" }, d2: { day: "2-digit" },
    month: { month: "short" }, monthlong: { month: "long" }, wd: { weekday: "long" }, year: { year: "numeric" }, time: { hour: "numeric", minute: "2-digit" }, num: { day: "2-digit", month: "2-digit", year: "numeric" } };
  $$("[data-day]").forEach((el) => {
    if (el.matches("[data-countdown],[data-ics]")) return;
    let s = at(el.dataset.day, el.dataset.time).toLocaleString(el.dataset.loc || "en-IN", FMT[el.dataset.fmt || "long"]);
    if (el.dataset.fmt === "num") s = s.replace(/\//g, " · ");
    if (el.dataset.case === "up") s = s.toUpperCase();
    el.textContent = s;
  });

  /* ---------- sample ribbon ---------- */
  const rib = document.createElement("div"); rib.className = "ld-ribbon";
  rib.innerHTML = `<span class="l"><b>Sample invitation by BFI</b> · names, venues and photos are fictional</span><span class="s"><b>Sample</b> · fictional names</span><a href="../customize.html">Create yours</a>`;
  document.body.prepend(rib);

  /* ---------- full-screen effects canvas (petals + bursts) ---------- */
  const cv = document.createElement("canvas"); cv.className = "ld-fx"; cv.setAttribute("aria-hidden", "true"); document.body.append(cv);
  const cx = cv.getContext("2d"); let W, H, DPR;
  const size = () => { DPR = Math.min(devicePixelRatio || 1, 2); W = innerWidth; H = innerHeight; cv.width = W * DPR; cv.height = H * DPR; cx.setTransform(DPR, 0, 0, DPR, 0, 0); };
  size(); addEventListener("resize", size);
  const parts = []; let bursts = [], petalsOn = false, raf;
  const pick = (a) => a[Math.floor(Math.random() * a.length)];
  const newPetal = (top) => ({ x: rnd(0, W), y: top ? rnd(-H, 0) : rnd(-40, -10), s: rnd(6, 13), vx: rnd(-.35, .35), vy: rnd(.45, 1.15), r: rnd(0, 6.3), vr: rnd(-.03, .03), sw: rnd(0, 6.3), c: pick(C.petals.colors), tw: rnd(0, 6.3) });
  function drawPetal(p) {
    cx.save(); cx.translate(p.x, p.y); cx.rotate(p.r); cx.fillStyle = p.c; cx.globalAlpha = .85;
    const t = C.petals.type, s = p.s;
    if (t === "leaf") { cx.beginPath(); cx.ellipse(0, 0, s * .45, s, 0, 0, 6.3); cx.fill(); cx.globalAlpha = .35; cx.strokeStyle = "#fff"; cx.beginPath(); cx.moveTo(0, -s); cx.lineTo(0, s); cx.stroke(); }
    else if (t === "rose") { cx.beginPath(); cx.moveTo(0, -s); cx.bezierCurveTo(s, -s * .6, s * .7, s * .7, 0, s); cx.bezierCurveTo(-s * .7, s * .7, -s, -s * .6, 0, -s); cx.fill(); }
    else if (t === "marigold") { for (let k = 0; k < 8; k++) { cx.rotate(.785); cx.beginPath(); cx.ellipse(0, s * .45, s * .28, s * .5, 0, 0, 6.3); cx.fill(); } cx.fillStyle = "#B4530F"; cx.beginPath(); cx.arc(0, 0, s * .28, 0, 6.3); cx.fill(); }
    else if (t === "star") { const a = .4 + .6 * Math.abs(Math.sin(p.tw)); cx.globalAlpha = a; cx.beginPath(); for (let k = 0; k < 4; k++) { cx.rotate(1.5708); cx.moveTo(0, 0); cx.quadraticCurveTo(s * .12, s * .12, 0, s * .7); cx.quadraticCurveTo(-s * .12, s * .12, 0, 0); } cx.fill(); }
    else { cx.globalAlpha = .4 + .5 * Math.abs(Math.sin(p.tw)); cx.beginPath(); cx.arc(0, 0, s * .22, 0, 6.3); cx.fill(); }
    cx.restore();
  }
  function frame() {
    cx.clearRect(0, 0, W, H);
    if (petalsOn) for (const p of parts) {
      p.sw += .02; p.tw += .05; p.x += p.vx + Math.sin(p.sw) * .45; p.y += C.petals.type === "dust" ? -p.vy * .6 : p.vy; p.r += p.vr;
      if (p.y > H + 30 || p.y < -60 || p.x < -40 || p.x > W + 40) Object.assign(p, newPetal(false), C.petals.type === "dust" ? { y: H + 20 } : {});
      drawPetal(p);
    }
    bursts = bursts.filter((b) => b(performance.now()));
    raf = (petalsOn || bursts.length) ? requestAnimationFrame(frame) : null;
  }
  const kick = () => { if (!raf && !still) raf = requestAnimationFrame(frame); };
  const startPetals = () => { if (still || !C.petals.count) return; for (let k = 0; k < C.petals.count; k++) parts.push(Object.assign(newPetal(true), C.petals.type === "dust" ? { y: rnd(0, H) } : {})); petalsOn = true; kick(); };
  document.addEventListener("visibilitychange", () => { if (document.hidden) { cancelAnimationFrame(raf); raf = null; } else kick(); });

  /* bursts: short cinematic transitions drawn on the canvas */
  function burst(kind, ms = 1700, ox = W / 2, oy = H / 2) {
    if (still) return;
    const t0 = performance.now(), cols = C.burstColors || ["#FFF4C2", "#F2C96B", "#D4AF37", "#E8890C"];
    const P = Array.from({ length: kind === "glow" ? 70 : 160 }, (_, k) => ({ a: rnd(0, 6.3), d: rnd(.2, 1), s: rnd(1, 3.2), c: pick(cols), k }));
    bursts.push((now) => {
      const t = Math.min(1, (now - t0) / ms), e = 1 - Math.pow(1 - t, 3), R = Math.hypot(W, H) * .62;
      cx.save(); cx.globalCompositeOperation = "lighter";
      const g = cx.createRadialGradient(ox, oy, 0, ox, oy, R * (kind === "glow" ? e * 1.2 : .45 + e * .5));
      g.addColorStop(0, `rgba(255,240,200,${.85 * (1 - t)})`); g.addColorStop(.35, `rgba(242,201,107,${.45 * (1 - t)})`); g.addColorStop(1, "rgba(0,0,0,0)");
      cx.fillStyle = g; cx.fillRect(0, 0, W, H);
      for (const p of P) {
        let x, y, s = p.s;
        if (kind === "swirl") { const ang = p.a + e * 5 * p.d, rr = e * R * p.d; x = ox + Math.cos(ang) * rr; y = oy + Math.sin(ang) * rr * .9; }
        else if (kind === "bloom" || kind === "marigold") { const rr = e * R * p.d; x = ox + Math.cos(p.a) * rr; y = oy + Math.sin(p.a) * rr + (kind === "marigold" ? e * e * 260 : 0); s *= kind === "marigold" ? 2.6 : 2; }
        else if (kind === "ink") { const rr = R * p.d * (.2 + e * .8); x = ox + Math.cos(p.a) * rr; y = oy + Math.sin(p.a) * rr; s *= .8; }
        else { const rr = e * R * p.d * .9; x = ox + Math.cos(p.a) * rr; y = oy - Math.abs(Math.sin(p.a)) * rr; }
        cx.globalAlpha = 1 - t; cx.fillStyle = p.c; cx.beginPath(); cx.arc(x, y, s, 0, 6.3); cx.fill();
      }
      if (kind === "ink") { cx.globalCompositeOperation = "source-over"; cx.globalAlpha = 1 - t; cx.strokeStyle = cols[2]; cx.lineWidth = 1.2; cx.beginPath(); cx.arc(ox, oy, e * R, 0, 6.3); cx.stroke(); }
      cx.restore(); return t < 1;
    });
    kick();
  }
  window.LDburst = burst;

  /* ---------- music: an original instrumental made live in the browser (or the family's own file) ---------- */
  const mb = $("[data-music]"); let ac, master, playing = false, timer, step = 0, nextT = 0, file;
  const M = C.music;
  const SCALES = { bilawal: [0, 2, 4, 5, 7, 9, 11], yaman: [0, 2, 4, 6, 7, 9, 11], bhimpalasi: [0, 2, 3, 5, 7, 9, 10], kafi: [0, 2, 3, 5, 7, 9, 10], pentatonic: [0, 2, 4, 7, 9] };
  const freq = (deg) => { const sc = SCALES[M.scale] || SCALES.bilawal, n = sc.length, o = Math.floor(deg / n), i = ((deg % n) + n) % n; return M.root * Math.pow(2, o + sc[i] / 12); };
  function voice(f, t, dur) {
    const o = ac.createOscillator(), g = ac.createGain(), inst = M.inst;
    let out = g;
    o.type = { shehnai: "sawtooth", flute: "sine", santoor: "triangle", sitar: "sawtooth", piano: "triangle" }[inst] || "sine";
    o.frequency.setValueAtTime(f, t);
    if (inst === "shehnai" || inst === "sitar") { const lp = ac.createBiquadFilter(); lp.type = inst === "sitar" ? "bandpass" : "lowpass"; lp.frequency.value = inst === "sitar" ? 1400 : 1700; lp.Q.value = inst === "sitar" ? 3 : .7; o.connect(lp); lp.connect(g); } else o.connect(g);
    if (inst === "shehnai" || inst === "flute") { const v = ac.createOscillator(), vg = ac.createGain(); v.frequency.value = 5.2; vg.gain.value = f * .006; v.connect(vg).connect(o.frequency); v.start(t); v.stop(t + dur + .3); }
    if (inst === "sitar") o.frequency.exponentialRampToValueAtTime(f * 1.003, t + .08);
    const pk = { shehnai: .16, flute: .2, santoor: .26, sitar: .2, piano: .22 }[inst] || .2;
    const pluck = inst === "santoor" || inst === "sitar" || inst === "piano";
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(pk, t + (pluck ? .01 : .06));
    g.gain.exponentialRampToValueAtTime(0.0001, t + (pluck ? Math.max(.5, dur * 1.4) : dur + .08));
    out.connect(master); o.start(t); o.stop(t + dur + 1.5);
    if (inst === "santoor" && Math.random() < .5) voice(f * 2, t + .07, dur * .5);
  }
  function drum(t, low) {
    const o = ac.createOscillator(), g = ac.createGain(); o.type = "sine";
    o.frequency.setValueAtTime(low ? 110 : 190, t); o.frequency.exponentialRampToValueAtTime(low ? 55 : 120, t + .18);
    g.gain.setValueAtTime(low ? .5 : .22, t); g.gain.exponentialRampToValueAtTime(.0001, t + (low ? .35 : .15));
    o.connect(g).connect(master); o.start(t); o.stop(t + .4);
  }
  function drone() {
    for (const [f, a] of [[M.root / 2, .07], [M.root * .75, .045], [M.root, .035]]) {
      const o = ac.createOscillator(), g = ac.createGain(), l = ac.createOscillator(), lg = ac.createGain();
      o.type = "sine"; o.frequency.value = f; g.gain.value = a; l.frequency.value = rnd(.1, .25); lg.gain.value = a * .5;
      l.connect(lg).connect(g.gain); o.connect(g).connect(master); o.start(); l.start(); drone.nodes = (drone.nodes || []).concat(o, l);
    }
  }
  function schedule() {
    const beat = 60 / M.tempo;
    while (nextT < ac.currentTime + .25) {
      const [deg, len] = M.melody[step % M.melody.length];
      if (deg !== null) voice(freq(deg), nextT, len * beat * .95);
      if (M.tabla) { const pos = M.melody.slice(0, step % M.melody.length).reduce((a, n) => a + n[1], 0); for (let b = 0; b < len; b++) { const bp = (pos + b) % 4; if (bp === 0 || bp === 2) drum(nextT + b * beat, bp === 0); else if (M.tabla > 1) drum(nextT + b * beat + beat / 2, false); } }
      nextT += len * beat; step++;
    }
  }
  function playMusic(on) {
    if (!mb) return; playing = on; mb.setAttribute("aria-pressed", on); mb.setAttribute("aria-label", on ? "Pause music" : "Play music");
    if (M && M.src) { file = file || Object.assign(new Audio(M.src), { loop: true, volume: .55 }); on ? file.play().catch(() => {}) : file.pause(); return; }
    if (!M) return;
    if (on) {
      ac = ac || new (window.AudioContext || window.webkitAudioContext)(); ac.resume();
      if (!master) { master = ac.createGain(); const comp = ac.createDynamicsCompressor(); master.connect(comp).connect(ac.destination); }
      master.gain.cancelScheduledValues(ac.currentTime); master.gain.setValueAtTime(.0001, ac.currentTime); master.gain.exponentialRampToValueAtTime(.8, ac.currentTime + 1.5);
      if (M.drone && !drone.nodes) drone();
      nextT = ac.currentTime + .15; clearInterval(timer); timer = setInterval(schedule, 90); schedule();
    } else if (ac) { master.gain.setTargetAtTime(.0001, ac.currentTime, .2); clearInterval(timer); }
  }
  mb?.addEventListener("click", () => playMusic(!playing));

  /* ---------- preloader → cover → open ---------- */
  const pre = $("[data-pre]"), cover = $("[data-cover]");
  html.classList.add("locked");
  const imgs = $$("[data-preload]").map((e) => e.dataset.preload).concat(C.preload || []);
  let done = 0; const bar = $("[data-pre-bar]");
  const tickBar = () => { if (bar) bar.style.transform = `scaleX(${Math.min(1, (done + 1) / (imgs.length + 1))})`; };
  const preloadAll = Promise.all(imgs.map((u) => new Promise((r) => { const i = new Image(); i.onload = i.onerror = () => { done++; tickBar(); r(); }; i.src = u; })));
  const minWait = new Promise((r) => setTimeout(r, still ? 0 : 1500));
  Promise.race([Promise.all([preloadAll, minWait]), new Promise((r) => setTimeout(r, 6000))]).then(() => {
    if (bar) bar.style.transform = "scaleX(1)";
    setTimeout(() => { pre?.classList.add("gone"); setTimeout(() => pre?.remove(), 700); if (!cover) start(); else if (params.get("open") === "1") open(); }, still ? 0 : 300);
  });
  function start() { html.classList.remove("locked"); html.classList.add("opened"); startPetals(); document.dispatchEvent(new Event("ld:open")); }
  function open() {
    if (!cover || cover.classList.contains("is-open")) return;
    cover.classList.add("is-open"); if (params.get("open") !== "1") playMusic(true);
    const d = +(cover.dataset.burstAt || 700);
    setTimeout(() => burst(C.burst, +(C.burstMs || 1800)), still ? 0 : d);
    setTimeout(() => { cover.remove(); start(); $("main")?.focus({ preventScroll: true }); }, still ? 0 : +(cover.dataset.dur || 1800));
  }
  if (cover) { $$("[data-open]", cover).forEach((b) => b.addEventListener("click", open)); cover.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } }); }

  /* ---------- scroll animations ---------- */
  const io = "IntersectionObserver" in window && !still && new IntersectionObserver((es) => es.forEach((x) => { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }), { rootMargin: "0px 0px -10% 0px" });
  $$("[data-anim]").forEach((el, k) => { if (el.dataset.delay) el.style.transitionDelay = el.dataset.delay + "s"; io ? io.observe(el) : el.classList.add("in"); });

  /* ---------- reveal-the-date games ---------- */
  const groups = $$("[data-reveal-group]");
  const celebrate = (g) => { if (g.dataset.done) return; g.dataset.done = 1; g.classList.add("revealed"); const r = g.getBoundingClientRect(); burst(C.revealBurst || "bloom", 1500, r.left + r.width / 2, r.top + r.height / 2); };
  const check = (g) => { if ($$("[data-hidden]", g).every((x) => x.classList.contains("shown"))) celebrate(g); };
  // 1) scratch: a canvas coat over each value
  $$("[data-scratch]").forEach((box) => {
    const c = document.createElement("canvas"), g = c.getContext("2d"); box.append(c); box.setAttribute("data-hidden", "");
    const paint = () => { const r = box.getBoundingClientRect(); c.width = r.width * 2; c.height = r.height * 2; g.scale(2, 2);
      const gr = g.createLinearGradient(0, 0, r.width, r.height); (box.dataset.coat || "#B8860B,#F2D58A,#A87A1E").split(",").forEach((col, i, a) => gr.addColorStop(i / (a.length - 1), col));
      g.fillStyle = gr; g.fillRect(0, 0, r.width, r.height); g.fillStyle = "rgba(255,255,255,.75)"; g.font = "600 11px system-ui"; g.textAlign = "center"; g.fillText(box.dataset.label || "SCRATCH", r.width / 2, r.height / 2 + 4); };
    paint();
    let down = false, n = 0, last = null;
    const scratch = (e) => { if (!down) return; const r = c.getBoundingClientRect(), p = e.touches ? e.touches[0] : e;
      const x = p.clientX - r.left, y = p.clientY - r.top; g.globalCompositeOperation = "destination-out"; g.strokeStyle = g.fillStyle = "#000"; g.lineWidth = 44; g.lineCap = "round"; g.beginPath(); if (last) { g.moveTo(last[0], last[1]); g.lineTo(x, y); g.stroke(); } else { g.arc(x, y, 22, 0, 6.3); g.fill(); } last = [x, y];
      if (++n % 6 === 0) measure(); };
    const measure = () => { if (box.classList.contains("shown")) return; const d = g.getImageData(0, 0, c.width, c.height).data; let clear = 0; for (let i = 3; i < d.length; i += 64) if (d[i] < 40) clear++; if (clear / (d.length / 64) > .4) { c.style.opacity = 0; box.classList.add("shown"); check(box.closest("[data-reveal-group]")); } };
    c.addEventListener("pointerdown", (e) => { down = true; last = null; c.setPointerCapture(e.pointerId); scratch(e); }); c.addEventListener("pointermove", scratch);
    c.addEventListener("pointerup", () => { down = false; last = null; measure(); }); c.addEventListener("pointercancel", () => (down = false));
    box.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); c.style.opacity = 0; box.classList.add("shown"); check(box.closest("[data-reveal-group]")); } });
    box.tabIndex = 0; box.setAttribute("role", "button"); box.setAttribute("aria-label", "Scratch to reveal");
  });
  // 2) flip / tap / light: tap a card to turn it
  $$("[data-tap]").forEach((b) => { b.setAttribute("data-hidden", ""); b.tabIndex = 0; b.setAttribute("role", "button");
    const go = () => { b.classList.add("shown"); check(b.closest("[data-reveal-group]")); }; b.addEventListener("click", go); b.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } }); });
  // 3) slide: drag a handle across to draw back a curtain
  $$("[data-slide]").forEach((s) => { s.setAttribute("data-hidden", ""); const h = $(".slide-handle", s), tr = $(".slide-track", s); let down = false;
    const set = (x) => { const r = tr.getBoundingClientRect(), v = Math.max(0, Math.min(1, (x - r.left) / r.width)); s.style.setProperty("--p", v); if (v > .92) { s.classList.add("shown"); s.style.setProperty("--p", 1); check(s.closest("[data-reveal-group]")); } };
    h.addEventListener("pointerdown", (e) => { down = true; h.setPointerCapture(e.pointerId); }); h.addEventListener("pointermove", (e) => down && set(e.clientX)); h.addEventListener("pointerup", () => { down = false; if (!s.classList.contains("shown")) s.style.setProperty("--p", 0); });
    h.addEventListener("keydown", (e) => { if (e.key === "ArrowRight" || e.key === "Enter") { s.classList.add("shown"); s.style.setProperty("--p", 1); check(s.closest("[data-reveal-group]")); } }); });
  // 4) roll: numbers spin like an odometer when they come into view
  const ro = "IntersectionObserver" in window && new IntersectionObserver((es) => es.forEach((x) => { if (!x.isIntersecting) return; ro.unobserve(x.target); const g = x.target;
    $$("[data-roll]", g).forEach((r, k) => { r.setAttribute("data-hidden", ""); setTimeout(() => { r.classList.add("shown"); check(g); }, still ? 0 : 500 + k * 450); }); }), { threshold: .5 });
  $$("[data-reveal-group][data-auto]").forEach((g) => (ro ? ro.observe(g) : $$("[data-roll]", g).forEach((r) => r.classList.add("shown"))));

  /* ---------- countdown ---------- */
  $$("[data-countdown]").forEach((box) => { const target = at(box.dataset.day, box.dataset.time); let timer;
    const tick = () => { let t = target - new Date(); if (t <= 0) { clearInterval(timer); box.innerHTML = `<p class="ld-done">${box.dataset.done || "The celebrations have begun. Thank you for your blessings."}</p>`; return; }
      for (const [k, u] of [["d", 864e5], ["h", 36e5], ["m", 6e4], ["s", 1e3]]) { const v = Math.floor(t / u); t -= v * u; const el = $(`[data-u=${k}]`, box); if (el) el.textContent = String(v).padStart(2, "0"); } };
    tick(); timer = setInterval(tick, 1000); });

  /* ---------- directions, calendar, RSVP, share ---------- */
  $$("[data-dir]").forEach((a) => { a.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(a.dataset.dir + ", India")}`; a.target = "_blank"; a.rel = "noopener"; });
  document.addEventListener("click", (e) => { const b = e.target.closest("[data-ics]"); if (!b) return;
    const st = at(b.dataset.day, b.dataset.time), en = new Date(st.getTime() + (+b.dataset.hours || 3) * 36e5), z = (x) => x.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
    const body = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//BFI//Sample invitation//EN", "BEGIN:VEVENT", `UID:${Date.now()}@bfi-sample`, `DTSTAMP:${z(new Date())}`, `DTSTART:${z(st)}`, `DTEND:${z(en)}`, `SUMMARY:${b.dataset.ics}`, `LOCATION:${b.dataset.place || ""}`, "END:VEVENT", "END:VCALENDAR"].join("\r\n");
    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([body], { type: "text/calendar" })); a.download = b.dataset.ics.replace(/\W+/g, "-") + ".ics"; a.click(); toast("Calendar file downloaded"); });
  let toastT; function toast(msg) { let t = $(".ld-toast"); if (!t) { t = document.createElement("div"); t.className = "ld-toast"; t.setAttribute("role", "status"); document.body.append(t); } t.textContent = msg; t.classList.add("on"); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove("on"), 2400); }
  $$("form[data-rsvp]").forEach((form) => form.addEventListener("submit", (e) => { e.preventDefault(); const bad = $$("[required]", form).find((x) => !x.checkValidity()); if (bad) { bad.reportValidity(); return; }
    const name = (new FormData(form).get("name") || "").toString().trim().split(" ")[0].replace(/[<>&"]/g, "");
    form.outerHTML = `<div class="rs-done" role="status"><p class="rs-done-t">${form.dataset.thanks || "Thank you"}${name ? ", " + name : ""}!</p><p>On a real BFI invitation your reply reaches the family's private guest list instantly. This is a sample, so nothing was sent.</p></div>`;
    burst(C.revealBurst || "bloom", 1400); }));
  $$("[data-share]").forEach((b) => b.addEventListener("click", () => window.open(`https://wa.me/?text=${encodeURIComponent(document.title.split(" · ")[0] + "\n" + location.href.split("?")[0])}`, "_blank", "noopener")));
  $$("[data-copy]").forEach((b) => b.addEventListener("click", async () => { try { await navigator.clipboard.writeText(location.href.split("?")[0]); toast("Link copied"); } catch { toast(location.href.split("?")[0]); } }));
  $$("[data-lang-to]").forEach((b) => b.addEventListener("click", () => { html.dataset.lang = b.dataset.langTo; $$("[data-lang-to]").forEach((x) => x.setAttribute("aria-pressed", x.dataset.langTo === b.dataset.langTo)); }));
})();
