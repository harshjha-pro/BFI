// Shared mockup layout: header, footer, sticky CTA and the invitation
// previews drawn for each design. Pages mark slots with data attributes:
//   <div data-header="designs"></div>  <div data-footer></div>
//   <div data-invite="royal-heritage" data-names="Aditi|Varun"></div>
(function () {
  const A = document.currentScript.src.replace(/mock\.js.*$/, "");
  const page = (p) => `${p}.html`;

  // ── Designs (same six as the studio app) ──
  const DESIGNS = [
    { slug: "royal-heritage", name: "Royal Heritage", tiers: "Premium · Luxury", bg: "#6B1324", gold: "#D6A84F", ink: "#F3DFB2", motif: "arch", note: "Haveli arch, maroon & gold" },
    { slug: "mandap-magic", name: "Mandap Magic", tiers: "Basic · Premium", bg: "#F4E6CF", gold: "#B8862F", ink: "#8A2B1D", motif: "mandap", note: "Ivory mandap, floral" },
    { slug: "golden-elegance", name: "Golden Elegance", tiers: "Luxury", bg: "#5C0D18", gold: "#E2B65C", ink: "#F6E2B8", motif: "mandala", note: "Ornate mandala, rich red" },
    { slug: "desert-dreams", name: "Desert Dreams", tiers: "Basic · Premium", bg: "#EFE0C4", gold: "#A8763A", ink: "#6E3F17", motif: "desert", note: "Thar dunes, minimal sand" },
    { slug: "marwari-classic", name: "Marwari Classic", tiers: "Basic · Premium · Luxury", bg: "#8C1D2C", gold: "#E8C47A", ink: "#F8E9C9", motif: "kalash", note: "Kalash & leaves, classic red" },
    { slug: "royal-palace", name: "Royal Palace", tiers: "Luxury", bg: "#141010", gold: "#D4A64A", ink: "#F2DFB0", motif: "palace", note: "Palace skyline, black & gold" },
  ];
  window.BFI_DESIGNS = DESIGNS;

  const MOTIF = {
    arch: (g) => `<path d="M60 250V150c0-36 28-62 60-72 32 10 60 36 60 72v100" fill="none" stroke="${g}" stroke-width="1.6"/><path d="M72 250V152c0-28 22-50 48-58 26 8 48 30 48 58v98" fill="none" stroke="${g}" stroke-width=".8"/><circle cx="120" cy="122" r="7" fill="none" stroke="${g}"/><circle cx="120" cy="122" r="2.5" fill="${g}"/>`,
    mandap: (g) => `<path d="M58 118 120 82l62 36z" fill="none" stroke="${g}" stroke-width="1.5"/><path d="M62 118h116" stroke="${g}" stroke-width="1.5"/>${[68, 96, 144, 172].map((x) => `<path d="M${x} 120v128" stroke="${g}" stroke-width="2"/>`).join("")}${[74, 92, 110, 128, 146, 164].map((x, i) => `<circle cx="${x}" cy="${126 + (i % 2) * 5}" r="2.4" fill="${g}" opacity=".7"/>`).join("")}<path d="M56 250h128" stroke="${g}" stroke-width="1.5"/>`,
    mandala: (g) => `<g transform="translate(120 140)">${Array.from({ length: 12 }, (_, i) => `<path transform="rotate(${i * 30})" d="M0-12C6-24 6-36 0-46-6-36-6-24 0-12z" fill="none" stroke="${g}" stroke-width="1.1"/>`).join("")}${Array.from({ length: 24 }, (_, i) => `<circle transform="rotate(${i * 15})" cx="0" cy="-54" r="1.8" fill="${g}"/>`).join("")}<circle r="9" fill="none" stroke="${g}"/><circle r="3" fill="${g}"/></g>`,
    desert: (g) => `<circle cx="168" cy="96" r="16" fill="none" stroke="${g}" stroke-width="1.4"/><path d="M70 170v-26h12v-10l9-9 9 9v10h12v-16l12-14 12 14v16h12v26z" fill="none" stroke="${g}" stroke-width="1.3"/><path d="M24 210c34-16 62-16 96 0s62 16 96 0" fill="none" stroke="${g}" stroke-width="1.4"/><path d="M24 228c34-12 62-12 96 0s62 12 96 0" fill="none" stroke="${g}" stroke-width=".9"/>`,
    kalash: (g) => `<path d="M92 156c0 32 12 48 28 48s28-16 28-48z" fill="none" stroke="${g}" stroke-width="1.6"/><path d="M96 156h48M100 146h40l-5 10h-30z" fill="none" stroke="${g}" stroke-width="1.4"/><ellipse cx="120" cy="128" rx="13" ry="15" fill="none" stroke="${g}" stroke-width="1.4"/>${[-1, 1].map((d) => `<path d="M120 142c${d * 16}-2 ${d * 30}-10 ${d * 38}-22 ${d * -12} 0 ${d * -28} 8 ${d * -38} 22z" fill="none" stroke="${g}" stroke-width="1.2"/>`).join("")}<circle cx="120" cy="178" r="3" fill="${g}"/>`,
    palace: (g) => `<path d="M30 206v-52h16v-20l9-9 9 9v20h14v-36l12-14 12 14v36h32v-36l12-14 12 14v36h14v-20l9-9 9 9v20h16v52z" fill="none" stroke="${g}" stroke-width="1.3"/><path d="M108 154v-24c0-10 5-17 12-22 7 5 12 12 12 22v24" fill="none" stroke="${g}" stroke-width="1.3"/>${[48, 70, 162, 184].map((x) => `<path d="M${x} 196v-12a4 4 0 0 1 8 0v12" fill="none" stroke="${g}"/>`).join("")}`,
  };

  // A full invitation screen (240×506 viewBox ≈ phone portrait).
  function invite(d, names = "Aditi|Varun", date = "12 · 02 · 2027", city = "Jaipur") {
    const [a, b] = names.split("|");
    const id = Math.random().toString(36).slice(2, 7);
    const light = parseInt(d.bg.slice(1, 3), 16) > 170;
    const sub = light ? d.ink : d.ink;
    return `<svg viewBox="0 0 240 506" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${d.name} invitation preview">
      <defs><radialGradient id="g${id}" cx="50%" cy="30%" r="80%"><stop offset="0" stop-color="${d.bg}" stop-opacity=".82"/><stop offset="1" stop-color="${d.bg}"/></radialGradient>
      <pattern id="p${id}" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="9" cy="9" r="1" fill="${d.gold}" opacity=".18"/></pattern></defs>
      <rect width="240" height="506" fill="${d.bg}"/><rect width="240" height="506" fill="url(#g${id})"/><rect width="240" height="506" fill="url(#p${id})"/>
      <rect x="12" y="12" width="216" height="482" rx="14" fill="none" stroke="${d.gold}" stroke-width="1.2"/>
      <rect x="18" y="18" width="204" height="470" rx="10" fill="none" stroke="${d.gold}" stroke-width=".5" opacity=".7"/>
      <text x="120" y="52" text-anchor="middle" font-family="Tiro Devanagari Hindi, serif" font-size="12" fill="${d.gold}">॥ श्री गणेशाय नमः ॥</text>
      ${MOTIF[d.motif](d.gold)}
      <text x="120" y="292" text-anchor="middle" font-family="Inter, sans-serif" font-size="7.5" letter-spacing="2.2" fill="${sub}" opacity=".85">TOGETHER WITH THEIR FAMILIES</text>
      <text x="120" y="336" text-anchor="middle" font-family="Cormorant Garamond, serif" font-weight="600" font-size="34" fill="${sub}">${a}</text>
      <text x="120" y="362" text-anchor="middle" font-family="Cormorant Garamond, serif" font-style="italic" font-size="22" fill="${d.gold}">&amp;</text>
      <text x="120" y="398" text-anchor="middle" font-family="Cormorant Garamond, serif" font-weight="600" font-size="34" fill="${sub}">${b}</text>
      <path d="M86 416h68" stroke="${d.gold}" stroke-width=".8"/>
      <text x="120" y="436" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.5" letter-spacing="2.4" fill="${sub}">${date} · ${city.toUpperCase()}</text>
      <rect x="88" y="452" width="64" height="22" rx="11" fill="${d.gold}"/><text x="120" y="467" text-anchor="middle" font-family="Inter, sans-serif" font-weight="600" font-size="9" fill="${light ? "#fff" : d.bg}">RSVP</text>
    </svg>`;
  }
  window.BFI_INVITE = invite;
  window.BFI_PHONE = (slug, size = "", names, date, city) => {
    const d = DESIGNS.find((x) => x.slug === slug) || DESIGNS[0];
    return `<div class="phone ${size}"><div class="screen">${invite(d, names, date, city)}</div></div>`;
  };

  const NAV = [["designs", "Designs"], ["pricing", "Pricing"], ["how-it-works", "How it works"], ["real-weddings", "Real weddings"], ["faq", "FAQ"]];
  const ICON_MENU = `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>`;

  document.querySelectorAll("[data-header]").forEach((el) => {
    const on = el.dataset.header;
    el.outerHTML = `<header class="site-head"><div class="wrap">
      <a class="brand" href="${page("index")}"><img src="${A}logo-mark.png" alt=""><span><b>BFI</b><small>Marwari Invitations</small></span></a>
      <nav class="site-nav" aria-label="Main">${NAV.map(([k, l]) => `<a href="${page(k)}" class="${k === on ? "on" : ""}">${l}</a>`).join("")}</nav>
      <a class="track" href="${page("track")}">Track my invitation</a>
      <a class="btn primary cta" href="${page("contact")}"><span class="lg-label">Plan my invitation</span><span class="sm-label">Enquire</span></a>
      <button class="menu-btn" aria-label="Menu">${ICON_MENU}</button>
    </div></header>`;
  });

  document.querySelectorAll("[data-footer]").forEach((el) => {
    el.outerHTML = `<footer class="site-foot"><div class="wrap">
      <div class="grid">
        <div><img class="logo" src="${A}logo-full.png" alt="BFI Marwari Invitations"><p style="margin-top:14px">Premium digital wedding invitations for Marwari families: every ritual, every name, beautifully delivered.</p></div>
        <div><h4>Explore</h4><a href="${page("designs")}">Designs</a><a href="${page("pricing")}">Pricing</a><a href="${page("how-it-works")}">How it works</a><a href="${page("real-weddings")}">Real weddings</a><a href="${page("about")}">About us</a></div>
        <div><h4>Help</h4><a href="${page("faq")}">FAQ</a><a href="${page("contact")}">Contact & enquiry</a><a href="${page("track")}">Track my invitation</a><a href="${page("partners")}">For wedding professionals</a></div>
        <div><h4>Talk to us</h4><a href="#">WhatsApp +91 98000 00000</a><a href="#">hello@bfi-invitations.in</a><span style="display:block;padding:4px 0">Jaipur, Rajasthan</span><span style="display:block;padding:4px 0">Mon–Sat · 10am–8pm</span></div>
      </div>
      <div class="legal"><span>© 2026 BFI — Marwari Invitations</span><span><a style="display:inline;margin-right:16px" href="${page("legal")}">Terms</a><a style="display:inline;margin-right:16px" href="${page("legal")}">Privacy</a><a style="display:inline" href="${page("legal")}">Refunds</a></span></div>
    </div></footer>
    <div class="sticky-cta"><a class="btn primary" href="${page("designs")}">Explore designs</a><a class="btn secondary" href="#">WhatsApp</a></div>`;
  });

  document.querySelectorAll("[data-invite]").forEach((el) => {
    el.outerHTML = window.BFI_PHONE(el.dataset.invite, el.dataset.size || "", el.dataset.names, el.dataset.date, el.dataset.city);
  });
})();
