#!/usr/bin/env python3
"""Generate the Royal Heritage website pages in site/ from shared templates.

Run:  python3 tools/build_website.py
Pages share one header, footer, mobile menu and WhatsApp buttons. Page logic lives in site/js/app.js.
Also writes robots.txt, sitemap.xml, llms.txt and the studio contact card (bfi-contact.vcf).
"""
import json
import re
from datetime import date
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "site"
V = "20261127b"  # bump to bust browser caches for css/js
BASE = "https://bfiluxe.com"
ART = "img/art/"
IMGBASE = "https://oaosapkkzoynaqpnmvrj.supabase.co/storage/v1/object/public/site/"
BIZ = {
    "name": "Bfiluxe",
    "phone": "+91 89495 09745", "tel": "+918949509745", "wa": "918949509745",
    "email": "myselfhkjha@gmail.com", "city": "Jaipur", "region": "Rajasthan", "country": "IN",
    "hours": "10am – 8pm, all days",
}
TODAY = date.today().isoformat()

# Catalogue (mirrors the `invitations` table seed in supabase/migrations)
CATALOG = [
    ("rajwada-royale", "Rajwada Royale", "royal", "Luxury", 24999, "Golden palace and lanterns on deep maroon",
     "A grand invitation inspired by Rajasthani palaces: hanging lanterns, a golden haveli and fine filigree for a traditional Marwari wedding.",
     ["Customizable names, dates and text", "Music or shehnai audio", "Shareable link and QR code", "RSVP (optional)", "Event pages with Google Maps"]),
    ("gulmohar-classic", "Gulmohar Classic", "traditional", "Premium", 8999, "Roses and marigolds on ivory",
     "A warm, festive border of roses and marigolds in Rajasthani folk style, loved by families who want a classic kankotri feel.",
     ["Customizable names, dates and text", "Hindi, English or bilingual", "Shareable link and QR code", "RSVP (optional)"]),
    ("gulabi-bagh", "Gulabi Bagh", "elegant", "Premium", 8999, "Blush peonies and fine gold",
     "Soft blush florals and delicate gold for a romantic, elegant celebration.",
     ["Customizable names, dates and text", "Music option", "Photo gallery", "Shareable link and QR code", "RSVP (optional)"]),
    ("mor-pankh", "Mor Pankh", "modern", "Premium", 8999, "Peacock on emerald green",
     "A majestic peacock on emerald green: modern, bold and unmistakably Rajasthani.",
     ["Customizable names, dates and text", "Music option", "Countdown to the wedding", "Shareable link and QR code", "RSVP (optional)"]),
    ("neel-mahal", "Neel Mahal", "royal", "Luxury", 24999, "Moonlit palace on royal navy",
     "A glowing palace under a crescent moon on royal navy, made for evening receptions and sangeet nights.",
     ["Customizable names, dates and text", "Music or shehnai audio", "Event pages with Google Maps", "Shareable link and QR code", "RSVP (optional)"]),
    ("gajraj-swagat", "Gajraj Swagat", "traditional", "Basic", 3999, "Royal elephants and marigold toran",
     "Two royal elephants welcome your guests under a marigold toran: auspicious, joyful and simple to share.",
     ["Customizable names, dates and text", "Hindi, English or bilingual", "Shareable link and QR code"]),
    ("sheesh-mahal", "Sheesh Mahal", "royal", "Luxury", 24999, "Chandeliers and a golden haveli",
     "Our grandest design: crystal chandeliers, a scalloped Mughal arch and a detailed golden haveli facade.",
     ["Customizable names, dates and text", "Music or shehnai audio", "Photo gallery", "Event pages with Google Maps", "RSVP with guest count", "Shareable link and QR code"]),
    ("chhatri", "Chhatri", "elegant", "Basic", 3999, "A single gold chhatri, lots of calm",
     "Minimal and refined: one gold-line chhatri pavilion and plenty of ivory space for your words.",
     ["Customizable names, dates and text", "Hindi, English or bilingual", "Shareable link and QR code"]),
]
CATALOG = [dict(slug=s, name=n, collection=c, tier=t, price=p, tagline=tg, desc=d, features=f, image=f"cover-{s}.webp")
           for s, n, c, t, p, tg, d, f in CATALOG]
COLL = {"royal": "Royal", "traditional": "Traditional", "elegant": "Elegant", "modern": "Modern"}
TAGS = {"rajwada-royale": "royal luxury rajasthani", "gulmohar-classic": "traditional floral rajasthani", "gulabi-bagh": "elegant floral",
        "mor-pankh": "modern rajasthani", "neel-mahal": "royal luxury modern", "gajraj-swagat": "traditional rajasthani",
        "sheesh-mahal": "royal luxury rajasthani", "chhatri": "elegant minimal modern"}
BEST = {"rajwada-royale": "Grand traditional weddings", "gulmohar-classic": "Classic family weddings", "gulabi-bagh": "Romantic day weddings",
        "mor-pankh": "Modern couples & destination weekends", "neel-mahal": "Evening receptions & sangeet nights", "gajraj-swagat": "Big Marwari family weddings",
        "sheesh-mahal": "Palace & destination weddings", "chhatri": "Intimate, minimal weddings"}
FILTERS = [("all", "All"), ("royal", "Royal"), ("traditional", "Traditional"), ("elegant", "Elegant"), ("modern", "Modern"),
           ("floral", "Floral"), ("minimal", "Minimal"), ("luxury", "Luxury"), ("rajasthani", "Rajasthani")]
DARK = {"rajwada-royale", "mor-pankh", "neel-mahal", "sheesh-mahal"}
INSET = {"rajwada-royale": "47% 14% 18% 14%", "gulmohar-classic": "40% 16% 22% 16%", "gulabi-bagh": "41% 14% 22% 14%", "mor-pankh": "16% 38% 32% 10%", "neel-mahal": "44% 14% 23% 14%", "gajraj-swagat": "15% 14% 50% 14%", "sheesh-mahal": "49% 14% 17% 14%", "chhatri": "36% 14% 12% 14%"}


def invite_text(inv, full=True, names=("Priya", "Rohan"), date="Saturday, 14 February", venue="Rambagh Gardens, Jaipur"):
    tone = "pv-dark" if inv["slug"] in DARK else "pv-light"
    if not full:
        return (f'<div class="inv-text {tone}" style="inset:{INSET[inv["slug"]]}"><span class="it-caps">Wedding Invitation</span>'
                f'<span class="it-script">{names[0]} <small>&amp;</small> {names[1]}</span><span class="it-rule"></span></div>')
    return (f'<div class="inv-text {tone}" style="inset:{INSET[inv["slug"]]}"><span class="it-deva" lang="hi">॥ श्री गणेशाय नमः ॥</span>'
            f'<span class="it-caps">Together with their families</span><span class="it-script">{names[0]}<small>weds</small>{names[1]}</span>'
            f'<span class="it-rule"></span><span class="it-date">{date}</span><span class="it-ven">{venue}</span></div>')
inr = lambda n: "₹" + format(n, ",d").replace(",", ",")  # 11,999 style (fine below 1 lakh)


LIVE = [
    (1, "Rajmahal", "Aarohi & Vivaan", "Royal · shehnai · Jaipur", "Tap the wax seal: the embossed envelope opens into a golden swirl. Scratch the gold to reveal the date."),
    (2, "Gulabi Nagri", "Ishita & Kabir", "Pink City · santoor · Jaipur", "Carved jharokha doors swing open into rose petals. Tap each window to reveal the date."),
    (3, "Thar ki Raat", "Meher & Arjun", "Desert night · bansuri · Jaisalmer", "Light the diya and the desert sky fills with stars. Light three lanterns to reveal the date."),
    (4, "Haldi Haveli", "Saanvi & Raghav", "Hindi-first · shehnai & dhol · Bikaner", "A marigold curtain lifts on a हिंदी / English invitation. Slide the diya to unveil the date."),
    (5, "Line & Light", "Nitya & Aditya", "Modern minimal · piano · Mumbai", "A monogram draws itself, gold dust rises, and the date rolls into place like an odometer."),
]


def live_cards():
    return '<div class="live-grid">' + "".join(
        f'<a class="live-card" href="live-demo-{n}/" target="_blank" rel="noopener" data-track="live_demo_{n}"><span class="live-img"><img src="img/live-demo/live-demo-{n}.jpg" alt="{t} sample invitation website for {c} (fictional)" width="600" height="1200" loading="lazy"></span>'
        f'<span class="live-meta">{m}</span><b>{t}</b><span class="live-desc">{d}</span><span class="tlink">Open live demo</span></a>' for n, t, c, m, d in LIVE) + "</div>"


VIDEO_PACKAGES = [
    ("Basic", 1499, "2–3 working days", "30-second video", "A short, elegant video invite to forward on WhatsApp.",
     ["30-second animated video", "1 design from our collection", "Couple and both families' names", "Main wedding date, time and venue",
      "Soft instrumental music", "Vertical MP4 for WhatsApp, Instagram and Status", "One free round of changes"]),
    ("Premium", 2499, "2–3 working days", "60-second video", "Every function, your photos and music.",
     ["60-second animated video", "Everything in Basic", "Up to 5 functions with dates and venues", "Your photos in the video",
      "Shehnai or instrumental music", "Hindi, English or bilingual text", "One free round of changes"]),
    ("Luxury", 3999, "2–3 working days", "90-second video", "A custom-illustrated video with every function.",
     ["90-second animated video", "Everything in Premium", "Custom illustration for your video", "All functions, from Ganesh puja to reception",
      "Animated opening with your initials", "One free round of changes"]),
]


def video_cards():
    out = []
    for name, price, days, length, blurb, feats in VIDEO_PACKAGES:
        out.append(f'''<div class="pkg{' pkg-pop' if name == 'Premium' else ''}">
      <h3>{name}</h3><p class="muted" style="font-size:14.5px;margin-top:4px">{blurb}</p>
      <p class="pkg-price">{wk("v", name)[0]} {pk("v", name)} {wk("v", name)[1]}</p><p class="pkg-time">{length} · ready in {dk("v", name)} after complete details and the 50% advance</p>
      <ul class="checks" style="margin:16px 0 20px">{"".join(f"<li>{icon(I['check'])}{f}</li>" for f in feats)}</ul>
      <a class="btn {'btn-primary' if name == 'Premium' else 'btn-outline'} btn-block" data-wa="Namaste Bfiluxe 🙏 I'd like the {name} invitation video ({inr(price)}).">Order the {name} video</a></div>''')
    return '<div class="pkgs">' + "".join(out) + "</div>"


MRP = {"Basic": 5999, "Premium": 14999, "Luxury": 35999}
VMRP = {"Basic": 2499, "Premium": 3999, "Luxury": 5999}
DAYS = {"Basic": "3–5 working days", "Premium": "7–14 working days", "Luxury": "15–21 working days"}


def was(mrp, pr):
    off = round((mrp - pr) * 100 / mrp)
    return f'<s class="mrp" aria-label="Regular price {inr(mrp)}">{inr(mrp)}</s>', f'<span class="save-off">{off}% off</span>'


# Live prices: every price carries data-k="kind:tier:field" so the site can update it from the
# admin's settings (kind p = invitation website packages, v = videos). The text here is the fallback.
def _pk(kind):
    return {n: (pr, d) for n, pr, d, *_ in (PACKAGES if kind == "p" else VIDEO_PACKAGES)}


def pk(kind, t):
    return f'<span data-k="{kind}:{t}:price">{inr(_pk(kind)[t][0])}</span>'


def mk(kind, t, cls="mrp"):
    m = (MRP if kind == "p" else VMRP)[t]
    if cls == "plain":
        return f'<span data-k="{kind}:{t}:mrp">{inr(m)}</span>'
    return f'<s class="{cls}" data-k="{kind}:{t}:mrp">{inr(m)}</s>'


def dk(kind, t):
    return f'<span data-k="{kind}:{t}:days">{_pk(kind)[t][1]}</span>'


def wk(kind, t):
    m, pr = (MRP if kind == "p" else VMRP)[t], _pk(kind)[t][0]
    return mk(kind, t), f'<span class="save-off" data-k="{kind}:{t}:off">{round((m - pr) * 100 / m)}% off</span>'


PACKAGES = [
    ("Basic", 3999, "3–5 working days", "For simple, elegant invitations shared quickly.",
     ["1 design from the Basic collection", "Couple and both families' names", "Up to 3 events with Google Maps", "English, Hindi or bilingual",
      "Private share link + QR code", "One free round of changes"]),
    ("Premium", 8999, "7–14 working days", "For full Marwari weddings with several functions.",
     ["Any Premium or Basic design", "Everything in Basic", "Up to 8 events: Ganesh puja to reception", "Background music or shehnai",
      "Photo gallery and countdown", "RSVP with guest count", "One free round of changes"]),
    ("Luxury", 24999, "15–21 working days", "Our grandest designs, or one made only for you.",
     ["Any design, or a bespoke design", "Everything in Premium", "Unlimited events and pages", "Custom colours and motifs",
      "Family story and video page", "Priority WhatsApp support", "One free round of changes"]),
]

WA = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3Z"/></svg>')


def icon(paths, cls=""):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>')


I = {
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "left": '<path d="m15 18-6-6 6-6"/>', "right": '<path d="m9 18 6-6-6-6"/>',
    "diamond": '<path d="M6 3h12l4 6-10 12L2 9Z"/><path d="M2 9h20M12 21 8 9l4-6 4 6-4 12"/>',
    "phone": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M11 18h2"/>',
    "call": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/>',
    "sliders": '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
    "crown": '<path d="m2 18 2-11 5 5 3-7 3 7 5-5 2 11Z"/><path d="M4 21h16"/>',
    "heart": '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/>',
    "clock": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2 2M9 2h6"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.1-3.1a2 2 0 0 0-2.8 0L6 21"/>',
    "edit": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 1 1 3 3L7 19l-4 1 1-4Z"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
    "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "lotus": '<path d="M12 20c-4 0-8-2-9-6 3 0 6 1 9 4 3-3 6-4 9-4-1 4-5 6-9 6Z"/><path d="M12 18c-2-2-3-5-3-8 1 0 2 1 3 2 1-1 2-2 3-2 0 3-1 6-3 8Z"/><path d="M12 12V4c1.5 1.5 2 3 2 4"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2a5 5 0 0 1 5.5 4.8"/>',
    "music": '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
    "rsvp": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/><path d="m9 16 2 2 4-4"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20"/>',
    "qr": '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 14h3v3h-3zM20 14v.01M14 20h.01M17 20h4v-3"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
    "refresh": '<path d="M21 12a9 9 0 0 1-15.5 6.2L3 16"/><path d="M3 12a9 9 0 0 1 15.5-6.2L21 8"/><path d="M21 3v5h-5M3 21v-5h5"/>',
    "download": '<path d="M12 3v12M7 10l5 5 5-5"/><path d="M5 21h14"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M8 7h8M8 11h6"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
}
ORN = f'<div class="orn" aria-hidden="true">{icon(I["lotus"])}</div>'

NAV = [("invitations", "Invitations"), ("videos", "Videos"), ("free-cards", "Free Card Maker"), ("how-it-works", "How It Works"), ("pricing", "Pricing")]
MORE = [("features", "Features"), ("customize", "Start your invitation"), ("demo", "Live demo"), ("resources", "Guides"), ("faq", "FAQ"),
        ("partners", "Partner with us"), ("contact", "Contact")]


def faq_html(items):
    return "".join(f'<details class="acc"><summary>{escape(q)}</summary><p>{a}</p></details>' for q, a in items)


def faq_ld(items):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}


ORG_LD = {
    "@context": "https://schema.org", "@type": "ProfessionalService", "@id": BASE + "/#business",
    "name": BIZ["name"], "alternateName": "Bfiluxe", "url": BASE + "/",
    "logo": BASE + "/img/icon-512.png", "image": BASE + "/img/og-image.jpg",
    "description": "Premium digital wedding invitations for Marwari families: mobile invitation websites with every ritual, family names, venues with maps, RSVP and a QR code, shared on WhatsApp.",
    "telephone": BIZ["tel"], "email": BIZ["email"], "priceRange": "₹1,499 – ₹24,999",
    "address": {"@type": "PostalAddress", "addressLocality": BIZ["city"], "addressRegion": BIZ["region"], "addressCountry": BIZ["country"]},
    "areaServed": [{"@type": "Country", "name": "India"}, "Worldwide (NRI families)"],
    "openingHoursSpecification": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "10:00", "closes": "20:00"},
    "knowsLanguage": ["en", "hi"],
    "contactPoint": {"@type": "ContactPoint", "telephone": BIZ["tel"], "contactType": "customer service", "availableLanguage": ["English", "Hindi"]},
}


def header(active):
    links = "".join(f'<a href="{k}.html"{" aria-current=page" if k == active else ""}>{t}</a>' for k, t in NAV)
    mlinks = '<a href="index.html">Home</a>' + "".join(f'<a href="{k}.html"{" aria-current=page" if k == active else ""}>{t}</a>' for k, t in NAV)
    more = "".join(f'<a href="{k}.html">{t}</a>' for k, t in MORE)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap hdr-in">
  <a class="brand" href="index.html" aria-label="Bfiluxe, home"><img class="brand-el" src="img/elephant.webp" alt="" width="40" height="30"><span class="wordmark">BFILUXE</span></a>
  <nav class="nav" aria-label="Main">{links}</nav>
  <div class="hdr-actions">
    <span data-auth-slot class="auth-slot"><a class="util-link" href="login.html">Sign in</a></span>
    <a class="btn btn-primary btn-sm hdr-cta" href="customize.html" data-track="hdr_start">Start your invitation</a>
    <button class="icon-btn menu-btn" data-menu-open aria-label="Open menu" aria-controls="menu" aria-expanded="false">{icon(I["menu"])}</button>
  </div>
</div></header>
<div class="sheet" id="menu" role="dialog" aria-modal="true" aria-label="Menu" hidden><div class="sheet-bg"></div><div class="sheet-panel">
  <div class="sheet-top"><a class="brand" href="index.html" aria-label="Bfiluxe, home"><img class="brand-el" src="img/elephant.webp" alt="" width="40" height="30"><span class="wordmark">BFILUXE</span></a><button class="icon-btn" data-menu-close aria-label="Close menu">{icon(I["x"])}</button></div>
  <nav class="sheet-main" aria-label="Menu">{mlinks}</nav>
  <nav class="sheet-more" aria-label="More">{more}</nav>
  <div class="sheet-foot"><div data-auth-menu><a class="btn btn-outline btn-block" href="login.html">Sign in</a></div><a class="btn btn-primary btn-block" data-wa>{WA} Enquire on WhatsApp</a></div>
</div></div>'''


def footer():
    return f'''<footer class="ftr"><div class="wrap">
  <div class="ftr-grid">
    <div class="ftr-brand"><a href="index.html" class="ftr-logo" aria-label="Bfiluxe, home"><img class="brand-el" src="img/elephant.webp" alt="" width="40" height="30"><span class="wordmark">BFILUXE</span></a>
      <p>Invitations made extraordinary. Digital Marwari wedding invitations, invitation websites and videos, rooted in family tradition.</p></div>
    <div><h4>Explore</h4><ul><li><a href="invitations.html">Invitations</a></li><li><a href="videos.html">Invitation videos</a></li><li><a href="how-it-works.html">How It Works</a></li><li><a href="pricing.html">Pricing</a></li><li><a href="contact.html">Contact</a></li></ul></div>
    <div><h4>Resources</h4><ul><li><a href="features.html">Features</a></li><li><a href="resources.html">Guides</a></li><li><a href="faq.html">FAQ</a></li><li><a href="free-cards.html">Free card maker</a></li><li><a href="partners.html">Partner with us</a></li><li><a href="login.html">My account</a></li></ul></div>
    <div><h4>Contact</h4><ul><li><a data-wa>WhatsApp {BIZ["phone"]}</a></li><li><a href="tel:{BIZ["tel"]}">Call {BIZ["phone"]}</a></li><li><a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></li><li>{BIZ["city"]}, {BIZ["region"]}, India</li><li>{BIZ["hours"]}</li><li><a href="bfi-contact.vcf" download>Save our contact card</a></li></ul></div>
  </div>
  <div class="ftr-bot"><span>© <span data-year></span> Bfiluxe</span><span><a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></span></div>
</div></footer>'''



# Every inner page gets a visual hero: the plain ".phead" header becomes text + an arch-framed illustration.
HERO = {
    "invitations": ("hero-invitations.jpg", "Ornate wedding invitation cards and a phone fanned out on maroon velvet"),
    "pricing": ("hero-pricing.jpg", "Three Rajasthani jewellery boxes of increasing size on ivory silk"),
    "how-it-works": ("hero-how-it-works.jpg", "A sketch, a phone with the finished invitation and a sealed envelope on a haveli table"),
    "customize": ("hero-customize.jpg", "A hand with mehendi writing on an ornate invitation with a gold pen"),
    "faq": ("hero-faq.jpg", "A grandmother and granddaughter chatting over chai at a jharokha window"),
    "guide": ("hero-guide.jpg", "An antique Rajasthani scroll painting of a wedding procession"),
    "free-cards": ("hero-free-cards.jpg", "Festive invitation cards for birthday, Diwali, housewarming and baby shower"),
    "contact": ("contact-studio.jpg", "The Bfiluxe studio: a desk by a jharokha window overlooking Jaipur"),
}
ARCH_SVG = ('<svg class="phero-svg" viewBox="0 0 240 260" aria-hidden="true"><g fill="none" stroke="#C6A15B" stroke-width="1.4" stroke-linecap="round">'
            '<path d="M30 250V130Q30 60 120 34Q210 60 210 130V250"/><path d="M52 250V136Q52 84 120 62Q188 84 188 136V250" opacity=".6"/>'
            '<path d="M14 250H226"/><path d="M120 34V16M112 20H128"/><circle cx="120" cy="12" r="3"/>'
            '<path d="M120 150c-14 0-26-6-30-18 9 0 18 3 30 12 12-9 21-12 30-12-4 12-16 18-30 18Z"/><path d="M120 146c-6-6-9-15-9-24 3 0 6 3 9 6 3-3 6-6 9-6 0 9-3 18-9 24Z"/>'
            '<path d="M84 200h72M96 212h48" opacity=".7"/></g></svg>')


LANDING_DESIGN = {"marwari-wedding-invitation-website": "sheesh-mahal", "marwari-kankotri-online": "gulmohar-classic", "hindi-wedding-invitation": "gajraj-swagat",
                  "wedding-invitation-website-rsvp": "neel-mahal", "rajasthani-digital-wedding-invitation": "mor-pankh"}


LIVE_HERO = {"pricing": 2, "videos": 4, "how-it-works": 1, "features": 5, "faq": 3, "contact": 2, "guide": 4, "resources": 3, "partners": 1}


def hero_parts(slug):
    """Each page gets its own hero design: (variant, extra copy, art html, section style)."""
    I_ = lambda n: (ART + n) if n.startswith("cover-") else (IMGBASE + n)
    if slug in LIVE_HERO:
        n = LIVE_HERO[slug]; t = next(x for x in LIVE if x[0] == n)
        chips = ""
        if slug == "pricing":
            chips = "".join(f'<span class="lh-chip c{k}"><b>{nm}</b>{pk("p", nm)}</span>' for k, (nm, pr, *_r) in enumerate(PACKAGES))
        elif slug == "videos":
            chips = '<span class="lh-chip c0"><b>9:16</b>Status &amp; Reels</span><span class="lh-chip c1"><b>Music</b>Shehnai · Santoor</span><span class="lh-chip c2"><b>{0}</b>From ₹1,499</span>'.format("Videos")
        art = (f'<div class="live-hero"><div class="lh-phone"><div class="lh-screen" data-lh><iframe src="live-demo-{n}/?preview=1" title="Live sample invitation: {t[1]} (fictional names)" loading="eager"></iframe></div></div>'
               f'<p class="lh-cap"><span class="lh-dot"></span>Live sample · {t[1]} · fictional names <a href="live-demo-{n}/" target="_blank" rel="noopener">Open full screen</a></p></div>')
        extra = ""
        return "live", extra, art, ""
    if slug == "invitations":
        art = ('<div class="fan">' + "".join(f'<img class="f{k}" src="{I_(n)}" alt="{a}" width="360" height="645">' for k, (n, a) in enumerate(
            [("cover-mor-pankh.webp", "Mor Pankh invitation"), ("cover-rajwada-royale.webp", "Rajwada Royale invitation"), ("cover-gulabi-bagh.webp", "Gulabi Bagh invitation")]))
            + f'<span class="fan-badge"><b>8</b> designs<br>from {pk("p", "Basic")}</span></div>')
        extra = '<div class="row hero-mini"><a class="btn btn-primary" href="#grid">Browse designs</a><a class="btn btn-ghost" href="demo.html">Open a live demo</a></div>'
        return "fan", extra, art, ""
    if slug == "pricing":
        art = ('<ul class="tags">' + "".join(f'<li style="--i:{k}"><span>{n}</span><b>{mk("p", n)} {pk("p", n)}</b><small>{dk("p", n)}</small></li>' for k, (n, pr, d, *_r) in enumerate(PACKAGES)) + '</ul>')
        return "banner", "", art, f' style="--bg:url({I_("hero-pricing.jpg")})"'
    if slug == "how-it-works":
        steps = ["Choose", "Share details", "Preview", "Share"]
        art = (f'<div class="pathstrip"><img src="{I_("hero-how-it-works.jpg")}" alt="A sketch, a phone with the finished invitation and a sealed envelope" width="1100" height="825">'
               '<svg viewBox="0 0 100 20" preserveAspectRatio="none" aria-hidden="true"><path d="M6 14 C 25 2, 35 18, 50 10 S 75 2, 94 12"/></svg>'
               + "".join(f'<span class="ps" style="--i:{k};left:{[8, 34, 60, 88][k]}%"><b>{k + 1}</b>{t}</span>' for k, t in enumerate(steps)) + '</div>')
        return "path", "", art, ""
    if slug == "videos":
        inv = next(i for i in CATALOG if i["slug"] == "gulmohar-classic")
        art = (f'<div class="vid"><div class="phone vid-phone"><div class="phone-screen vid-screen">'
               f'<img class="vid-bg" src="{I_(inv["image"])}" alt="" width="720" height="1290">'
               '<p class="vs1" lang="hi">॥ श्री गणेशाय नमः ॥</p><p class="vs2">Priya <small>weds</small> Rohan</p>'
               '<p class="vs3">Mayra · Pithi · Sangeet · Phere</p><p class="vs4">Saturday, 14 February<br><small>Rambagh Gardens, Jaipur</small></p>'
               '<span class="vid-bar"><i></i></span><span class="vid-play" aria-hidden="true">▶</span></div></div>'
               '<p class="vid-cap">Preview animation · sample names</p></div>')
        return "video", "", art, ""
    if slug == "customize":
        art = (f'<div class="circ"><svg class="mandala" viewBox="0 0 200 200" aria-hidden="true">' + "".join(f'<ellipse cx="100" cy="22" rx="7" ry="20" transform="rotate({k * 22.5} 100 100)"/>' for k in range(16)) +
               '<circle cx="100" cy="100" r="94"/><circle cx="100" cy="100" r="86" stroke-dasharray="2 6"/></svg>'
               f'<img src="{I_("hero-customize.jpg")}" alt="A hand with mehendi writing on an invitation with a gold pen" width="1100" height="825">'
               '<div class="mini-inv"><small>॥ शुभ विवाह ॥</small><b class="typer" data-names="Priya weds Rohan|Ananya weds Vikram|Meera weds Arjun|Your names here">Priya weds Rohan</b><span>Live preview as you type</span></div></div>')
        return "circle", "", art, ""
    if slug == "faq":
        chat = [("q", "Can the invitation be in Hindi?"), ("a", "Yes! Hindi, English, Marwari + Hindi or bilingual."), ("q", "Can we add Mayra and Pithi?"), ("a", "Of course: every function, with its own map."), ("q", "When do we pay the rest?"), ("a", "Only after you approve the preview 🙏")]
        art = (f'<div class="chatwrap"><img src="{I_("hero-faq.jpg")}" alt="A grandmother and granddaughter chatting over chai at a jharokha window" width="1100" height="825">'
               '<div class="chat">' + "".join(f'<p class="b {w}" style="--i:{k}">{t}</p>' for k, (w, t) in enumerate(chat)) + '</div></div>')
        return "chat", "", art, ""
    if slug == "guide":
        return "scroll", "", "", f' style="--bg:url({I_("hero-guide.jpg")})"'
    if slug == "free-cards":
        cards = ["birthday-kids", "diwali", "griha-pravesh", "godh-bharai", "holi", "wedding"]
        art = ('<div class="stack" data-stack>' + "".join(f'<img class="s{k} p{k}" src="{I_("tpl-" + c + ".jpg")}" alt="{c.replace("-", " ").title()} card template" width="360" height="645" loading="{"eager" if k < 3 else "lazy"}">' for k, c in enumerate(cards))
               + '</div>')
        extra = '<ul class="hero-chips"><li>16 templates</li><li>PNG · JPG · PDF</li><li>No sign-up</li></ul><div class="row hero-mini"><a class="btn btn-primary" href="#tpl-grid">Start making a card</a></div>'
        return "stack", extra, art, ""
    if slug == "contact":
        art = (f'<div class="postcard"><img src="{I_("contact-studio.jpg")}" alt="The Bfiluxe studio: a desk by a jharokha window overlooking Jaipur" width="1100" height="733">'
               '<span class="stamp"><img src="img/icon-192.png" alt="" width="64" height="64"></span><span class="postmark">JAIPUR<br>RAJASTHAN</span>'
               '<span class="cchip c1"><i></i>Usually replies within an hour</span><span class="cchip c2">10am – 8pm, all days</span></div>')
        return "postcard", "", art, ""
    if slug == "features":
        ics = ["pin", "music", "rsvp", "qr", "globe", "image", "clock", "share"]
        art = ('<div class="orbit"><div class="phone orbit-phone"><div class="phone-screen inv-wrap">' + f'<img src="{I_("cover-rajwada-royale.webp")}" alt="Invitation on a phone" width="720" height="1290">' + invite_text(CATALOG[0]) + '</div></div>'
               '<div class="ring">' + "".join(f'<span style="--a:{k * 45}deg">{icon(I[c])}</span>' for k, c in enumerate(ics)) + '</div></div>')
        return "orbit", "", art, ""
    if slug == "resources":
        art = ('<div class="papers">' + "".join(f'<a class="paper p{k}" href="{u}"><small>Guide</small><b>{t}</b><span>Read →</span></a>' for k, (u, t) in enumerate(
            [("guide.html", "Marwari wedding rituals, in order"), ("hindi-wedding-invitation.html", "Hindi invitation wording & honorifics"), ("digital-vs-printed-kankotri.html", "Digital vs printed kankotri")])) + '</div>')
        return "papers", "", art, ""
    if slug == "partners":
        roles = [("users", "Wedding planners"), ("image", "Photographers"), ("pin", "Venues & hotels"), ("lotus", "Decorators")]
        art = ('<div class="roles">' + "".join(f'<div class="role" style="--i:{k}">{icon(I[ic])}<b>{t}</b></div>' for k, (ic, t) in enumerate(roles))
               + f'<div class="role-badge"><b>15–20%</b>referral commission</div></div>')
        return "roles", "", art, ""
    if slug in LANDING_DESIGN:
        inv = next(i for i in CATALOG if i["slug"] == LANDING_DESIGN[slug])
        art = (f'<div class="land"><div class="phone land-phone"><div class="phone-screen inv-wrap"><img src="{I_(inv["image"])}" alt="{inv["name"]} invitation" width="720" height="1290">{invite_text(inv)}</div></div>'
               f'<a class="land-tag" href="design-{inv["slug"]}.html">Shown: {inv["name"]} →</a></div>')
        extra = '<div class="row hero-mini"><a class="btn btn-primary" href="invitations.html">See designs</a><a class="btn btn-ghost" href="demo.html">Open live demo</a></div>'
        return "landing", extra, art, ""
    if slug == "digital-vs-printed-kankotri":
        art = (f'<div class="versus"><figure class="vs-card"><img src="{I_("cover-chhatri.webp")}" alt="A printed card" width="360" height="645"><figcaption>Printed</figcaption></figure>'
               '<span class="vs">VS</span>'
               f'<figure class="vs-phone"><div class="phone"><div class="phone-screen inv-wrap"><img src="{I_("cover-gulmohar-classic.webp")}" alt="A digital invitation on a phone" width="720" height="1290">' + invite_text(CATALOG[1]) + '</div></div><figcaption>Digital</figcaption></figure></div>')
        return "versus", "", art, ""
    if slug == "inviting-guests-mayra-pithi-phere":
        art = (f'<div class="ritpic"><img src="{I_("ritual-baraat.jpg")}" alt="Miniature-style painting of a baraat procession" width="1000" height="666">'
               + "".join(f'<span class="rchip" style="--i:{k}">{t}</span>' for k, t in enumerate(["Mayra · family", "Pithi · family", "Phere · everyone"])) + '</div>')
        return "ritpic", "", art, ""
    word = {"privacy": "PRIVACY", "terms": "TERMS", "account": "ACCOUNT"}.get(slug, "Bfiluxe")
    art = (f'<div class="seal"><svg viewBox="0 0 200 200" aria-hidden="true"><defs><path id="ring-{slug}" d="M100 100 m-74 0 a74 74 0 1 1 148 0 a74 74 0 1 1 -148 0"/></defs>'
           f'<text><textPath href="#ring-{slug}">BFILUXE · INVITATIONS MADE EXTRAORDINARY · {word} · TRUST · </textPath></text></svg><img src="img/logo-sm.webp" alt="" width="200" height="174"></div>')
    return "seal", "", art, ""


PAGE_OBJS = [("kalash", "wax-seal"), ("diya", "rings"), ("potli", "envelope"), ("bangles", "scroll"), ("mehendi-cone", "toran"), ("rings", "kalash"), ("envelope", "diya")]


def with_hero(slug, body):
    m = re.search(r'<section class="phead"[^>]*><div class="wrap">(.*?)</div></section>', body, re.S)
    if not m:
        return body
    variant, extra, art, style = hero_parts(slug)
    objs = PAGE_OBJS[sum(map(ord, slug)) % len(PAGE_OBJS)]
    deco = ""
    hero = f'<section class="phero h-{variant}"{style}>{deco}<div class="wrap phero-grid"><div class="phero-copy">{m.group(1)}{extra}</div>{art}</div></section>'
    return body[:m.start()] + hero + '<!--/hero-->' + body[m.end():]


# Search snippets: titles stay under ~60 characters and descriptions under 160 so Google shows them whole.
TITLES = {
    "index": "Digital Marwari Wedding Invitations & Kankotri | Bfiluxe",
    "invitations": "Wedding Invitation Designs: Royal to Minimal | Bfiluxe",
    "pricing": "Digital Wedding Invitation Pricing from ₹3,999 | Bfiluxe",
    "faq": "FAQ: Digital Marwari Wedding Invitations | Bfiluxe",
    "features": "Invitation Features: Maps, RSVP, Music & QR | Bfiluxe",
    "free-cards": "Free Invitation Card Maker: PNG, JPG & PDF | Bfiluxe",
    "guide": "Marwari Wedding Rituals & Invitation Wording | Bfiluxe",
    "hindi-wedding-invitation": "Hindi Wedding Invitation Wording & Designs | Bfiluxe",
    "digital-vs-printed-kankotri": "Digital vs Printed Kankotri: Which to Choose? | Bfiluxe",
    "inviting-guests-mayra-pithi-phere": "Inviting Guests to Mayra, Pithi & Phere | Bfiluxe",
    "marwari-kankotri-online": "Marwari Kankotri Online: Digital Kankotri | Bfiluxe",
    "rajasthani-digital-wedding-invitation": "Rajasthani Digital Wedding Invitations | Bfiluxe",
    "wedding-invitation-website-rsvp": "Wedding Invitation Website with RSVP | Bfiluxe",
    "partners": "Partner With Bfiluxe: Planners, Photographers, Venues",
}
DESCS = {
    "index": "Digital Marwari wedding invitations and kankotri: royal Rajasthani designs, every ritual, maps, RSVP and QR. From ₹3,999, ready in 3–5 working days.",
    "faq": "Answers about digital Marwari wedding invitations: Hindi wording, Mayra and Pithi, RSVP, WhatsApp sharing, delivery times, payment and link validity.",
    "features": "Every feature of a Bfiluxe digital wedding invitation in plain words: family names, every function with maps, Hindi wording, music, RSVP, QR code and sharing.",
    "free-cards": "Make a free invitation card for a birthday, Griha Pravesh, Godh Bharai, puja, Diwali and more. 16 templates, live preview, PNG, JPG or PDF. No sign-up.",
    "privacy": "How Bfiluxe collects, uses, stores and protects your enquiry details, account data and the information shown on your wedding invitation.",
    "terms": "Terms for Bfiluxe digital wedding invitations: orders, payment in two parts, delivery times, rounds of changes, refunds and how long invitation links stay live.",
}
for _k, _v in {**TITLES, **DESCS}.items():
    assert len(_v) <= (60 if _v in TITLES.values() else 160), (_k, len(_v))
PAGE_TYPE = {"about": "AboutPage", "contact": "ContactPage", "resources": "CollectionPage"}


NO_CTA_RIBBON = {"index", "404", "customize", "login", "account", "privacy", "terms", "demo", "invitation", "videos"}
NO_CTA = {"index", "404", "contact", "customize", "login", "account", "privacy", "terms", "demo", "free-cards", "invitation"}


def page(slug, title, desc, body, active=None, bar=True, ld=None, index=True, og_image=None, chrome=True, path=None):
    body = with_hero(slug, body)
    if index and slug not in NO_CTA_RIBBON:
        add = page_extra(slug)
        body = body.replace("<!--/hero-->", add, 1) if "<!--/hero-->" in body else body + page_extra(slug)
    body = body.replace("<!--/hero-->", "")
    if index and slug not in NO_CTA and "cta-min" not in body and "{cta" not in body:
        body += cta()  # every marketing page ends on the same minimal call to action
    title, desc = TITLES.get(slug, title), DESCS.get(slug, desc)
    url = f"{BASE}/{path if path is not None else (slug + '.html' if slug != 'index' else '')}"
    ld = list(ld or [])
    if index and slug not in ("index", "404"):
        have = {x.get("@type") for x in ld}
        name = title.split(" | ")[0]
        # every indexable page says what it is and where it sits (helps search and AI answers cite the right page)
        if not have & {"WebPage", "AboutPage", "ContactPage", "CollectionPage", "Article", "FAQPage", "Product"}:
            ld.append({"@context": "https://schema.org", "@type": PAGE_TYPE.get(slug, "WebPage"), "name": name, "description": desc, "url": url,
                       "inLanguage": "en-IN", "isPartOf": {"@type": "WebSite", "name": "Bfiluxe", "url": BASE + "/"}, "publisher": {"@id": BASE + "/#business"}})
        if "BreadcrumbList" not in have:
            ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}, {"@type": "ListItem", "position": 2, "name": name, "item": url}]})
    lds = "".join(f'\n<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    mbar = f'''<div class="mbar"><a class="btn btn-primary" href="invitations.html">Explore invitations</a><a class="btn btn-outline" data-wa>{WA} WhatsApp</a></div>''' if bar else ""
    og = og_image or BASE + "/img/og-image.jpg"
    head = f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
{'' if index else '<meta name="robots" content="noindex">'}
<meta name="theme-color" content="#F7F3EB">
<meta property="og:site_name" content="Bfiluxe">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:alt" content="{escape(title)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="img/favicon.ico?v=2" sizes="any">
<link rel="icon" href="img/favicon-32.png?v=2" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png?v=2">
<link rel="manifest" href="manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://oaosapkkzoynaqpnmvrj.supabase.co" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400;1,500&family=Montserrat:wght@400;500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Tiro+Devanagari+Hindi&family=Great+Vibes&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css?v={V}">{lds}
</head>'''
    scripts = (f'<script src="js/vendor/qrcode.js?v=1.4.4"></script>\n' if slug == "demo" else "") + f'''<script src="js/vendor/supabase.js?v=2.45.4"></script>
<script src="js/config.js?v={V}"></script>
<script src="js/app.js?v={V}"></script>'''
    if chrome:
        html = f'''{head}
<body data-page="{slug}"{'' if bar else ' class="no-mbar"'}>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
{mbar}
{scripts}
</body>
</html>
'''
    else:
        html = f'''{head}
<body data-page="{slug}" class="no-mbar">
{body}
{scripts}
</body>
</html>
'''
    (OUT / f"{slug}.html").write_text(html.replace("\n\n<meta name=\"theme-color\"", "\n<meta name=\"theme-color\""))


def strip_item(ic, t, s):
    return f'<div class="strip-item">{icon(I[ic])}<div><b>{t}</b><span>{s}</span></div></div>'


def card(inv):
    tone = "pv-dark" if inv["slug"] in DARK else "pv-light"
    return f'''<article class="card" data-tags="{TAGS[inv["slug"]]}">
    <button class="fav" data-fav="{inv["slug"]}" aria-pressed="false" aria-label="Save {inv["name"]} to favourites">{icon(I["heart"])}</button>
    <a class="card-img card-stage" href="design-{inv["slug"]}.html" aria-label="{inv["name"]}: view design"><span class="h-badge">{COLL[inv["collection"]]}</span>
      <span class="h-print"><img src="{ART}{inv["image"]}" alt="" loading="lazy" width="360" height="645"></span>
      <span class="h-phone"><span class="phone-screen inv-wrap"><img src="{ART}{inv["image"]}" alt="{inv["name"]} invitation: {inv["tagline"]}" loading="lazy" width="360" height="645">{invite_text(inv, full=False)}</span></span></a>
    <div class="card-body"><h3><a href="design-{inv["slug"]}.html">{inv["name"]}</a></h3>
      <p class="card-desc">{inv["tagline"]}</p><p class="card-best">Best for: {BEST[inv["slug"]]}</p>
      <div class="card-meta"><span>{inv["tier"]}</span><span>from <b>{inr(inv["price"])}</b></span></div>
      <div class="card-acts"><a class="btn btn-sm btn-outline" href="demo.html?design={inv["slug"]}">Live demo</a><a class="btn btn-sm btn-primary" href="design-{inv["slug"]}.html">View design</a></div></div></article>'''


def package_cards(compact=False):
    out = []
    for name, price, days, blurb, feats in PACKAGES:
        pop = name == "Premium"
        out.append(f'''<div class="pkg{' pkg-pop' if pop else ''}">
      <h3>{name}</h3><p class="muted" style="font-size:14.5px;margin-top:4px">{blurb}</p>
      <p class="pkg-price">{wk("p", name)[0]} {pk("p", name)} {wk("p", name)[1]}</p><p class="pkg-time">Ready in {dk("p", name)} after complete details and the 50% advance</p>
      <ul class="checks" style="margin:16px 0 20px">{"".join(f"<li>{icon(I['check'])}{f}</li>" for f in (feats[:4] if compact else feats))}</ul>
      <a class="btn {'btn-primary' if pop else 'btn-outline'} btn-block" href="invitations.html?tier={name}">View {name} designs</a></div>''')
    return '<div class="pkgs">' + "".join(out) + "</div>"


HOME_FAQ = [
    ("What is a digital Marwari wedding invitation?", "A mobile invitation website for your wedding: couple and family names, every function with date, time and Google Maps, plus music, photos and RSVP on higher packages. Guests open it from a WhatsApp link or a QR code."),
    ("How much does it cost?", f"Basic {pk('p', 'Basic')} (regular {mk('p', 'Basic', 'plain')}), Premium {pk('p', 'Premium')} (regular {mk('p', 'Premium', 'plain')}) and Luxury {pk('p', 'Luxury')} (regular {mk('p', 'Luxury', 'plain')}). You pay 50% to start and 50% after you approve. See <a href='pricing.html'>pricing</a>."),
    ("How fast will it be ready?", "Basic in 3–5 working days, Premium in 7–14 working days and Luxury in 15–21 working days, counted from when we have all your details and the advance."),
    ("Can it include Mayra, Pithi and other rituals?", "Yes. Add any function: Ganesh Sthapana, Mayra, Pithi, Mehendi, Mahila Sangeet, Baraat, Phere, Reception or your own family rituals."),
    ("Can the invitation be in Hindi or Marwari?", "Yes: English, Hindi, Marwari with Hindi, or bilingual, with traditional lines like ॥ श्री गणेशाय नमः ॥."),
    ("Can I see it before paying the balance?", "Yes. You review a private preview on your phone, get one round of changes, and pay the remaining 50% only after you approve."),
]

# ---------------- Home ----------------
RITUAL_STRIP = [("Ganesh Sthapana", "The first invitation goes to Ganpati ji"), ("Mayra", "The mama's family arrives with gifts"),
                ("Pithi", "Turmeric, songs and family blessings"), ("Mehendi", "Henna and the groom's hidden initials"),
                ("Mahila Sangeet", "An evening led by the women of the family"), ("Baraat & Nikasi", "The groom rides out with music"),
                ("Toran & Varmala", "At the bride's door, garlands exchanged"), ("Phere", "Seven vows around the sacred fire")]
FEATURED = ["rajwada-royale", "gulmohar-classic", "neel-mahal", "chhatri"]
HERO_INV = next(i for i in CATALOG if i["slug"] == "rajwada-royale")
XP_INV = next(i for i in CATALOG if i["slug"] == "neel-mahal")
SAMPLE = dict(names=("Aarohi", "Vivaan"), date="Sunday · 17 January 2027", venue="Rajmahal Gardens, Jaipur")
PROD_BADGE = {"rajwada-royale": "Royal", "gulmohar-classic": "Floral", "gulabi-bagh": "Pink City", "mor-pankh": "Modern",
              "neel-mahal": "Night", "gajraj-swagat": "Grand", "sheesh-mahal": "Luxury", "chhatri": "Minimal"}


def mini_phone(inv, cls="h-phone"):
    return (f'<span class="{cls}"><span class="phone-screen inv-wrap"><img src="{ART}{inv["image"]}" alt="" loading="lazy" width="360" height="645">'
            f'{invite_text(inv, full=False)}</span></span>')


def prod_card(inv):
    return f"""<article class="h-prod">
  <a class="h-prod-stage" href="design-{inv["slug"]}.html" aria-label="{inv["name"]}: view design">
    <span class="h-badge">{PROD_BADGE[inv["slug"]]}</span>
    <span class="h-print"><img src="{ART}{inv["image"]}" alt="" loading="lazy" width="360" height="645"></span>
    {mini_phone(inv)}
  </a>
  <button class="fav" data-fav="{inv["slug"]}" aria-pressed="false" aria-label="Save {inv["name"]} to favourites">{icon(I["heart"])}</button>
  <h3><a href="design-{inv["slug"]}.html">{inv["name"]}</a></h3>
  <p class="h-prod-desc">{inv["tagline"]}</p>
  <p class="h-prod-meta"><span>From <b data-dp="{inv["slug"]}" data-tier="{inv["tier"]}">{inr(inv["price"])}</b></span><a href="demo.html?design={inv["slug"]}">Live demo</a></p>
</article>"""


def plan_cards():
    out = []
    for n, pr, d, bl, feats in PACKAGES:
        rec = n == "Premium"
        checks = "".join(f"<li>{icon(I['check'])}{f}</li>" for f in feats[:5])
        out.append(f'<div class="h-plan{" rec" if rec else ""}">{"<span class=h-rec>Recommended</span>" if rec else ""}'
                   f'<p class="h-plan-name">{n}</p><p class="h-plan-price">{wk("p", n)[0]}{pk("p", n)}<small>{wk("p", n)[1]} · ready in {dk("p", n)}</small></p>'
                   f'<p class="h-plan-blurb">{bl}</p><ul class="checks">{checks}</ul>'
                   f'<a class="btn {"btn-primary" if rec else "btn-outline"} btn-block" href="invitations.html?tier={n}">See {n} designs</a></div>')
    return '<div class="h-plan-grid">' + "".join(out) + "</div>"


INSIDE = [("cover", "Cover & wax seal", "Guests tap the seal and the invitation opens, with your music."),
          ("names", "Blessings & family names", "॥ श्री गणेशाय नमः ॥, elders first, in Hindi, English or both."),
          ("date", "Scratch to reveal the date", "A little game: guests scratch the gold to see the muhurat."),
          ("countdown", "Countdown to the phere", "Days, hours and minutes, live on every phone."),
          ("functions", "Every function", "Mayra, Pithi, Sangeet, Baraat… each with its time and directions."),
          ("venue", "Venue & maps", "One tap opens Google Maps to the right gate."),
          ("rsvp", "RSVP with guest count", "Plan rooms and catering without fifty phone calls.")]
HOW2 = [("cover", "Choose a design", "Browse the collection and open any live demo on your phone."),
        ("names", "Share your details", "Names, functions and venues, online or on WhatsApp, in Hindi or English."),
        ("date", "Preview and approve", "We set every name by hand. You check a private preview; one round of changes is included."),
        ("wa", "Send one link", "A ready WhatsApp message, your private link and a QR code for printed cards.")]
QUOTE = "Long before the shehnai plays, your family's blessing travels to every home. Let it arrive beautifully."
FACTS = [("8", "invitation designs"), ("5", "live openings to try"), ('<span lang="hi">हिं</span> · En', "Hindi, English or both"), ("3–5<small>days</small>", "for a Basic invitation")]
CHIPS = ["Ganesh Sthapana", "Mayra", "Pithi", "Mehendi", "Mahila Sangeet", "Baraat", "Phere", "Reception", "+ any family ritual"]


def wa_screen():
    return ('<span class="h-wa"><span class="h-wa-top"><b>Mausi ji</b><small>online</small></span>'
            '<span class="h-wa-msg in">Beta, card bhej do 🙏</span>'
            '<span class="h-wa-msg out"><span class="h-wa-link"><img src="img/screens/cover.webp" alt="" width="540" height="1041" loading="lazy">'
            '<b>Aarohi weds Vivaan</b><small>Tap to open the invitation</small></span>Our invitation 💌 Please bless us!</span>'
            '<span class="h-wa-msg in">Kitna sundar hai! ❤️ Hum zaroor aayenge</span></span>')


def how_screens():
    out = []
    for n, (k, t, d) in enumerate(HOW2):
        inner = wa_screen() if k == "wa" else f'<img src="img/screens/{k}.webp" alt="" width="540" height="1041" loading="lazy">'
        out.append(f'<span data-step="{n}" class="h-how-scr{" on" if n == 0 else ""}">{inner}</span>')
    return "".join(out)


def inside_tabs():
    return "".join(f'<li><button type="button" role="tab" aria-selected="{"true" if n == 0 else "false"}" data-screen="{k}"><span>{n + 1:02d}</span><b>{t}</b><small>{d}</small></button></li>'
                   for n, (k, t, d) in enumerate(INSIDE))


def inside_imgs():
    return "".join(f'<img data-s="{k}"{" class=on" if n == 0 else ""} src="img/screens/{k}.webp" alt="{t} screen of a sample invitation" width="540" height="1041" loading="lazy">'
                   for n, (k, t, d) in enumerate(INSIDE))

RIT_ICON = {"Ganesh Sthapana": "lotus", "Mayra": "users", "Pithi": "diamond", "Mehendi": "edit", "Mahila Sangeet": "music",
            "Baraat & Nikasi": "crown", "Toran & Varmala": "heart", "Phere": "refresh"}


def journey(items):
    lis = "".join(f'<li style="--i:{n}"><span class="rj-dot">{icon(I[ic])}</span><span class="rj-n">{n + 1:02d}</span><b>{t}</b><p>{d}</p></li>'
                  for n, (ic, t, d) in enumerate(items))
    return f'<div class="rj" data-progress><span class="rj-line"><i></i></span><ol>{lis}</ol></div>'


def ritual_journey(items):
    lis = "".join(f'<li style="--i:{n}"><span class="rj-dot">{icon(I[RIT_ICON.get(t, "lotus")])}</span><span class="rj-n">{n + 1:02d}</span><b>{t}</b><p>{d}</p></li>'
                  for n, (t, d) in enumerate(items))
    return f'<div class="rj" data-progress><span class="rj-line"><i></i></span><ol>{lis}</ol></div>'


PROMISES = [("Payment in two parts", "50% to begin, 50% only after you approve the preview."),
            ("One round of changes", "Send all your changes together after the first preview."),
            ("Spelling corrections, always free", "Names and spellings are fixed at no cost, any time."),
            ("Live long after the wedding", "Your link stays live through the wedding and at least six months after."),
            ("Private by default", "Only people you share the link with can open it.")]
CHECK = '<svg class="pr-check" viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="14"/><path d="M10 16.5l4 4 8-9"/></svg>'


def promises(title="Clear terms, <em>before you begin.</em>", eyebrow="Our promise"):
    rows = "".join(f'<li style="--i:{n}">{CHECK}<div><b>{t}</b><p>{d}</p></div></li>' for n, (t, d) in enumerate(PROMISES))
    return (f'<section class="sec"><div class="wrap pr-grid"><div class="pr-head"><p class="eyebrow">{eyebrow}</p><h2 class="h-display">{title}</h2>'
            f'<p class="h-lead">No surprises: what you see in the preview is what your guests get.</p></div><ol class="pr-list">{rows}</ol></div></section>')


def cta(title="Your celebration deserves <em>a beautiful beginning.</em>", text="Tell us your names and wedding date. We'll suggest designs and confirm the price before you pay anything.",
        primary=("customize.html", "Start your invitation")):
    return (f'<section class="cta-min"><div class="wrap"><div class="cta-min-in"><p class="deva" lang="hi">॥ शुभ विवाह ॥</p><h2>{title}</h2><p>{text}</p>'
            f'<div class="row"><a class="btn btn-primary" href="{primary[0]}">{primary[1]}</a><a class="btn btn-outline" data-wa>{WA} WhatsApp us</a></div></div></div></section>')


CTA_HOME = cta()


RIBBON_WORDS = ["Ganesh Sthapana", "Mayra", "Pithi", "Mehendi", "Mahila Sangeet", "Baraat", "Toran", "Varmala", "Phere", '<span lang="hi">॥ शुभ विवाह ॥</span>']
RIBBON_SUB = ["Hindi &amp; English", "A map for every function", "RSVP with guest count", "Music &amp; shehnai", "One link + QR code", "Set by hand"]


def ribbon():
    big = "".join(f"<span>{w}</span><i>✦</i>" for w in RIBBON_WORDS)
    small = "".join(f"<span>{w}</span><i>·</i>" for w in RIBBON_SUB)
    return (f'<div class="ribbon" aria-hidden="true"><div class="rb-row rb-a"><div class="rb-track">{big}{big}</div></div>'
            f'<div class="rb-row rb-b"><div class="rb-track">{small}{small}{small}</div></div></div>')


PICK = {"Basic": (["names", "venue"], "Your names, blessing and up to 3 functions, each with its own map."),
        "Premium": (["countdown", "functions", "rsvp"], "Every function, music, photo gallery, a live countdown and RSVP."),
        "Luxury": (["cover", "date"], "Our grandest openings, or a design made only for you, with unlimited pages.")}


def picker_sec():
    tabs = "".join(f'<button type="button" role="tab" aria-selected="{"true" if k == 0 else "false"}" data-tier="{n}"><b>{n}</b><span>{mk("p", n)} {pk("p", n)}</span><small>Ready in {dk("p", n)}</small></button>'
                   for k, (n, pr, d, bl, f) in enumerate(PACKAGES))
    lists = "".join(f'<div class="pk-list" data-tier="{n}"{"" if k == 0 else " hidden"}><p>{PICK[n][1]}</p><ul class="checks">{"".join(f"<li>{icon(I['check'])}{x}</li>" for x in f[:5])}</ul></div>'
                    for k, (n, pr, d, bl, f) in enumerate(PACKAGES))
    imgs = "".join(f'<img data-tier="{n}" data-i="{i}"{" class=on" if (n == "Basic" and i == 0) else ""} src="img/screens/{sc}.webp" alt="" width="540" height="1041" loading="lazy">'
                   for n in PICK for i, sc in enumerate(PICK[n][0]))
    return (f'<section class="sec pk-sec"><div class="wrap pk-grid"><div><div class="h-rule"><span>Compare at a glance</span><span>Tap a package</span></div>'
            f'<h2 class="h-display">See what <em>each package opens.</em></h2><div class="pk-tabs" role="tablist" aria-label="Packages">{tabs}</div>{lists}'
            f'<a class="btn btn-primary" href="customize.html">Start your invitation</a></div>'
            f'<div class="pk-phone" data-picker aria-hidden="true"><span class="h-bigphone"><span class="phone-screen">{imgs}</span></span></div></div></section>')


def guests_say():
    return ('<section class="sec gs"><div class="wrap center"><p class="eyebrow">The first impression</p><h2>What your guests will say</h2>'
            '<p class="gs-lead">The memory of your wedding doesn\'t start on the big day. It starts the second they open your invitation.</p>'
            '<div class="gs-chat"><div class="gs-msg out"><span class="gs-card"><img src="img/art/cover-rajwada-royale.webp" alt="" width="720" height="1290" loading="lazy">'
            '<b>Aarohi &amp; Vivaan · 17 January 2027</b><span>With the blessings of our families, join us in Jaipur. Every function, maps and RSVP.</span><i>Tap to open the invitation</i></span><em>18:41 ✓✓</em></div>'
            '<div class="gs-msg in">Kitna sundar hai!! 😍 Hum zaroor aayenge 🙏<em>18:42</em></div></div>'
            '<p class="gs-note">Sample chat · names are fictional</p></div></section>')


def page_extra(slug):
    if slug in ("invitations", "resources", "faq"):
        return FAN_SEC
    if slug == "how-it-works":
        return HOW_SEC
    if slug == "pricing":
        return guests_say() + picker_sec()
    if slug == "features" or slug.startswith("design-") or slug in LANDING_DESIGN or slug == "digital-vs-printed-kankotri":
        return INSIDE_SEC
    return ""


FAN_SEC = f'''<section class="h-fan-sec" aria-label="The collection"><div class="wrap">
  <div class="h-rule"><span>The collection</span><span>8 designs · 5 live openings</span></div>
  <h2 class="h-display">8 designs. <em>Every one set by hand.</em></h2></div>
  <div class="h-fan" aria-hidden="true"><div class="h-fan-track">{"".join(f'<a class="h-fan-item" href="design-{i["slug"]}.html" tabindex="-1">{mini_phone(i, "h-fan-phone")}<span class="h-fan-name">{i["name"]}</span></a>' for i in CATALOG * 2)}</div></div>
</section>'''

INSIDE_SEC = f'''<section class="sec h-inside"><div class="wrap h-inside-grid">
  <div>
    <div class="h-rule"><span>Inside your invitation</span><span>Real screens from a live demo</span></div>
    <h2 class="h-display">Everything your guests need. <em>Nothing they don't.</em></h2>
    <p class="h-lead">One link holds it all, in the order your family follows. Tap a section to see it.</p>
    <ol class="h-tabs" role="tablist" aria-label="Sections of the invitation">{inside_tabs()}</ol>
    <p class="h-chips-label">Your functions, in your order</p>
    <ul class="h-chips">{"".join(f"<li>{x}</li>" for x in CHIPS)}</ul>
    <a class="btn btn-primary" href="customize.html">Start my invitation</a>
  </div>
  <div class="h-inside-phone"><span class="h-bigphone"><span class="phone-screen">{inside_imgs()}</span></span></div>
</div></section>'''

HOW_SEC = f'''<section class="sec h-how"><div class="wrap">
  <div class="h-rule"><span>How it works</span><span>Four steps, all on your phone</span></div>
  <div class="h-how-grid">
    <div class="h-how-sticky"><span class="h-bigphone"><span class="phone-screen">{how_screens()}</span></span></div>
    <ol class="h-how-steps">{"".join(f'<li data-step="{n}"><span>{n + 1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for n, (k, t, d) in enumerate(HOW2))}</ol>
  </div>
</div></section>'''


HOME = f'''
<section class="h-hero"><div class="wrap h-hero-grid">
  <div class="h-hero-copy">
    <p class="eyebrow">Digital Marwari wedding invitations</p>
    <h1>Every ritual. Every name. <em>Every blessing.</em></h1>
    <p class="h-sub">Your wedding invitation as one beautiful link. It opens like a real card, with every function, a map for each venue, music and RSVP. Set by hand, ready from 3 working days.</p>
    <div class="row h-ctas"><a class="btn btn-primary" href="invitations.html" data-track="hero_explore">Explore designs</a><a class="btn btn-outline" href="live-demo-1/" target="_blank" rel="noopener" data-track="hero_demo">Open a live invitation</a></div>
    <p class="h-note">From {pk("p", "Basic")} · Hindi &amp; English · balance paid after you approve</p>
  </div>
  <div class="h-stage" data-parallax aria-hidden="true">
    <span class="h-glow"></span>
    <img class="h-obj h-kalash" data-depth="18" src="img/art/obj-kalash.webp" alt="" width="809" height="660">
    <span class="h-hero-phone" data-depth="6"><span class="phone-screen">
      <img src="img/art/cover-rajwada-royale.webp" alt="" width="720" height="1290" fetchpriority="high">
      <span class="h-names"><span class="it-deva" lang="hi">॥ श्री गणेशाय नमः ॥</span><span class="it-caps">Together with their families</span>
        <span class="it-script">{SAMPLE["names"][0]}<small>weds</small>{SAMPLE["names"][1]}</span><span class="it-rule"></span><span class="it-date">{SAMPLE["date"]}</span></span>
    </span></span>
    <img class="h-obj h-seal" data-depth="26" src="img/art/obj-wax-seal.webp" alt="" width="900" height="579">
    <img class="h-obj h-rings" data-depth="30" src="img/art/obj-rings.webp" alt="" width="747" height="323">
    <img class="h-obj h-diya" data-depth="14" src="img/art/obj-diya.webp" alt="" width="661" height="540">
    {"".join(f'<span class="h-petal p{n}" data-depth="{10 + n * 4}"></span>' for n in range(1, 7))}
  </div>
</div>
<p class="wrap h-sample">Sample invitation · names are fictional</p></section>

{FAN_SEC}

<section class="sec h-shop"><div class="wrap">
  <div class="h-rule"><span>Collection</span><span>Every design is personalised for your family by our team</span></div>
  <div class="h-shop-head"><h2 class="h-display">Wedding invitations <span class="h-count">8</span></h2><a class="btn btn-outline" href="invitations.html">View all designs</a></div>
  <div class="h-prods">{"".join(prod_card(i) for i in CATALOG)}</div>
  <a class="h-custom" href="customize.html"><span><b>Want something made only for you?</b>Luxury includes a bespoke design around your story.</span><span class="tlink">Start your invitation</span></a>
</div></section>

{INSIDE_SEC}

{HOW_SEC}

<section class="h-quote" aria-label="Our promise"><div class="wrap">
  <p class="deva" lang="hi">॥ शुभ विवाह ॥</p>
  <p class="h-quote-text" data-words>{QUOTE}</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="h-atelier">
    <figure><img src="img/art/cover-rajwada-royale.webp" alt="Rajwada Royale invitation artwork: a golden palace at dusk" width="720" height="1290" loading="lazy"></figure>
    <div><p class="eyebrow">Made by people, not a template</p><h2>Set by hand, <em>checked twice.</em></h2>
      <p>We are a small team in Jaipur. Every invitation is set by a person who knows that the elders come first, that चि. and सौ. कां. matter, and that Mayra has its own place.</p>
      <ol><li><span>01</span>Names in the order your family follows</li><li><span>02</span>Hindi spellings and honorifics checked by hand</li><li><span>03</span>A private preview before you pay the balance</li></ol></div>
  </div>
</div></section>

<section class="sec sec-tint"><div class="wrap">
  <div class="h-rule"><span>Marwari heritage</span><span>Your rituals, your order</span></div>
  <h2 class="h-display">Every ritual <em>has its place.</em></h2>
  {ritual_journey(RITUAL_STRIP)}
  <p style="margin-top:28px"><a class="tlink" href="guide.html">Read the Marwari wedding guide</a></p>
</div></section>

<section class="sec h-plans"><div class="wrap">
  <div class="h-rule"><span>Pricing</span><span>One payment per wedding · 50% now, 50% after you approve</span></div>
  <h2 class="h-display center">Choose <em>your package.</em></h2>
  {plan_cards()}
  <p class="lx-fine center">Delivery times start once we have your complete details and the 50% advance.</p>
  <a class="lx-video" href="videos.html"><span><b>Invitation videos</b> for WhatsApp, Reels and Status</span><span>{" · ".join(f"{n} {mk('v', n)} {pk('v', n)}" for n, pr, *_ in VIDEO_PACKAGES)}</span><span class="tlink">See videos</span></a>
</div></section>

{promises()}

<section class="sec" id="reviews-sec" hidden><div class="wrap">
  <div class="lx-head"><div><p class="eyebrow">Kind words</p><h2>From families we have worked with</h2></div></div>
  <div class="reviews" id="reviews"></div>
</div></section>

<section class="sec"><div class="wrap lx-split lx-faq">
  <div><p class="eyebrow">Questions</p><h2>Frequently asked</h2><p class="lead">Anything else? Ask us on WhatsApp.</p>
    <div class="row"><a class="tlink" href="faq.html">All questions</a><a class="tlink" data-wa>Ask on WhatsApp</a></div></div>
  <div>{faq_html(HOME_FAQ)}</div>
</div></section>

{CTA_HOME}
'''


OCC = [("wedding", "Wedding"), ("save-the-date", "Save the Date"), ("sagai", "Sagai"), ("birthday-kids", "Kids' Birthday"),
       ("birthday-gold", "Birthday"), ("anniversary", "Anniversary"), ("griha-pravesh", "Griha Pravesh"), ("godh-bharai", "Godh Bharai"),
       ("naamkaran", "Naamkaran"), ("mundan", "Mundan"), ("puja", "Bhajan Sandhya"), ("diwali", "Diwali"), ("holi", "Holi Milan"),
       ("gangaur-teej", "Teej & Gangaur"), ("retirement", "Retirement"), ("prayer-meet", "Prayer Meet")]
page("index", "Digital Wedding Invitations for Marwari Families | Bfiluxe",
     "Premium digital wedding invitations for Marwari families: royal Rajasthani designs, every ritual and family name, maps, RSVP and QR code. From ₹3,999, ready from 3 working days.",
     HOME, "index", ld=[ORG_LD, {"@context": "https://schema.org", "@type": "WebSite", "name": "Bfiluxe", "url": BASE + "/", "inLanguage": "en-IN"}, faq_ld(HOME_FAQ)])

# ---------------- Invitations ----------------
INV = f'''
<section class="phead"><div class="wrap">
  <p class="eyebrow">Digital Marwari wedding invitations</p>
  <h1>The Invitation Collection</h1>
  <p class="lead">Eight design directions, from palace grandeur to quiet minimal lines. Each one opens as a live demo on your phone and shows its starting price.</p>
</div></section>
<section class="sec" style="padding-top:28px"><div class="wrap">
  <div class="chips" role="group" aria-label="Filter by collection">
    {"".join(f'<button class="chip" data-c="{k}" aria-pressed="{str(k == "all").lower()}">{v}</button>' for k, v in FILTERS)}
  </div>
  <div class="toolbar"><span class="muted" id="count" aria-live="polite">Showing {len(CATALOG)} invitations</span>
    <div class="row" style="gap:8px"><label class="sr" for="tier">Package</label><select id="tier"><option value="">All packages</option><option>Basic</option><option>Premium</option><option>Luxury</option></select>
    <label class="sr" for="sort">Sort</label><select id="sort"><option value="">Popular</option><option value="low">Price: low to high</option><option value="high">Price: high to low</option></select></div></div>
  <div class="grid-inv" id="grid">{"".join(card(i) for i in CATALOG)}</div>
  <div class="live-sec" id="live">
    <div class="lx-head"><div><p class="eyebrow">Live sample invitations</p><h2>Open one like a guest would</h2></div>
      <p class="lx-head-note">Each opens like a real invitation, with its own animation, music and a little game to reveal the date. Turn your sound on: couples, families and venues are fictional.</p></div>
    {live_cards()}
  </div>
  <div class="lx-helps">
    <div><p class="eyebrow">Need help choosing?</p><h2>Tell us your colours and venue</h2><p>Send your wedding colours, city and functions, and we'll suggest two or three designs that suit them.</p>
      <a class="btn btn-outline" data-wa="Namaste Bfiluxe 🙏 Please help us choose an invitation design. Our colours / city / functions:">{WA} Ask on WhatsApp</a></div>
    <div><p class="eyebrow">Luxury bespoke</p><h2>Something only yours</h2><p>A design created from scratch around your family, your city and your story, on the Luxury package.</p>
      <a class="btn btn-outline" href="contact.html">Request a bespoke design</a></div>
  </div>
</div></section>'''
page("invitations", "Wedding Invitation Designs: Royal, Traditional, Elegant, Modern | Bfiluxe",
     "Browse digital Marwari wedding invitation designs: Royal palaces, Traditional florals, Elegant pastels and Modern peacocks. Prices from ₹3,999.", INV, "invitations",
     ld=[{"@context": "https://schema.org", "@type": "ItemList", "name": "Bfiluxe invitation designs",
          "itemListElement": [{"@type": "ListItem", "position": n + 1, "url": f"{BASE}/design-{i['slug']}.html", "name": i["name"]} for n, i in enumerate(CATALOG)]}])

# ---------------- Design detail pages (static, one per design) ----------------

TIER_RANK = {"Basic": 0, "Premium": 1, "Luxury": 2}
PLAN_SUB = {"Basic": "The design as it is, with your names and details", "Premium": "Every function, music, gallery, countdown and RSVP", "Luxury": "Our grandest openings, or a design made only for you"}


def plan_opts(inv):
    return [(n, max(pr, inv["price"]), d, bl, f) for n, pr, d, bl, f in PACKAGES if TIER_RANK[n] >= TIER_RANK[inv["tier"]]]


def plan_pick(inv):
    out = []
    for k, (n, pr, d, bl, f) in enumerate(plan_opts(inv)):
        rec = '<span class="pp-rec">Recommended</span>' if n == "Premium" else ""
        out.append(f'''<label class="pp-o pp-{n.lower()}">{rec}<input type="radio" name="plan" value="{n}" data-price="{inr(pr)}" data-tier="{n}" data-dmin="{inv["slug"]}"{" checked" if k == 0 else ""}>
          <span class="pp-top"><span class="pp-dot"></span><b>{n}</b><em>{mk("p", n)} <span data-dp="{inv["slug"]}" data-tier="{n}">{inr(pr)}</span></em></span><strong>{PLAN_SUB[n]}</strong><span class="pp-bl">{bl} Ready in {dk("p", n)}.</span>
          <details><summary>See everything included</summary><ul>{"".join(f"<li>{x}</li>" for x in f)}</ul></details></label>''')
    return "".join(out)


for inv in CATALOG:
    tone = "pv-dark" if inv["slug"] in DARK else "pv-light"
    sim = [x for x in CATALOG if x["slug"] != inv["slug"] and x["collection"] == inv["collection"]] + [x for x in CATALOG if x["collection"] != inv["collection"]]
    def ficon(f):
        return ("edit" if "Custom" in f else "music" if "usic" in f else "rsvp" if "RSVP" in f else "link" if "link" in f
                else "pin" if "Maps" in f else "globe" if "Hindi" in f else "image" if "Photo" in f else "clock")
    feats = "".join(f'<li>{icon(I[ficon(f)])}<span>{f}</span></li>' for f in inv["features"])
    days = DAYS[inv["tier"]]
    body = f'''
<section class="sec" style="padding-top:22px"><div class="wrap">
  <p class="crumbs"><a href="invitations.html">Invitations</a> › <a href="invitations.html?c={inv["collection"]}">{COLL[inv["collection"]]} Collection</a> › <span aria-current="page">{inv["name"]}</span></p>
  <div class="detail" id="detail" data-slug="{inv["slug"]}" data-name="{inv["name"]}">
    <div class="gallery">
      <div class="big" id="slide">
        <div class="slide slide-phone"><div class="phone"><div class="phone-screen inv-wrap"><img src="{ART}{inv["image"]}" alt="{inv["name"]} invitation cover with sample wording" width="720" height="1290" fetchpriority="high">{invite_text(inv)}</div></div></div>
        <div class="slide slide-phone" hidden><div class="phone"><div class="phone-screen"><img src="img/screens/names.webp" alt="Blessing and family names screen of a sample invitation" loading="lazy" width="540" height="1041"></div></div></div>
        <div class="slide slide-phone" hidden><div class="phone"><div class="phone-screen"><img src="img/screens/functions.webp" alt="Every function with times and directions" loading="lazy" width="540" height="1041"></div></div></div>
      </div>
      <button class="nav-arrow prev" aria-label="Previous image">{icon(I["left"])}</button>
      <button class="nav-arrow next" aria-label="Next image">{icon(I["right"])}</button>
      <p class="sample-note">Sample wording: names, date and venue are fictional</p>
      <div class="dots"><button aria-label="Cover" aria-current="true"></button><button aria-label="Names" aria-current="false"></button><button aria-label="Functions" aria-current="false"></button></div>
    </div>
    <div class="d-side">
      <p class="eyebrow">Digital invitation · {COLL[inv["collection"]]} collection</p>
      <div class="d-head"><h1 class="d-title">{inv["name"]}</h1>
        <button class="d-fav" data-fav="{inv["slug"]}" aria-pressed="false" aria-label="Save to favourites">{icon(I["heart"])}</button></div>
      <p class="d-tag">{inv["desc"]}</p>
      <p class="d-from">From</p><p class="d-price">{wk("p", inv["tier"])[0]} <span data-dp="{inv["slug"]}" data-tier="{inv["tier"]}">{inr(inv["price"])}</span> {wk("p", inv["tier"])[1]}</p>
      <p class="d-sub">One payment per wedding · {len(plan_opts(inv))} level{"s" if len(plan_opts(inv)) > 1 else ""} of personalisation</p>
      <h2 class="d-h2">How personalised should it be?</h2>
      <p class="d-ticks"><span>RSVP built in</span><span>Hindi &amp; English</span><span>A map for every function</span></p>
      <div class="pp" role="radiogroup" aria-label="Choose your package">{plan_pick(inv)}</div>
      <a class="btn btn-primary btn-block d-cta" data-plan-cta data-design="{inv["slug"]}" href="customize.html?design={inv["slug"]}&amp;tier={plan_opts(inv)[0][0]}">Continue with <span data-plan-label>{plan_opts(inv)[0][0]} · {inr(plan_opts(inv)[0][1])}</span> {icon(I["arrow"])}</a>
      <p class="d-ticks d-ticks-c"><span>Set by hand</span><span>One round of changes</span><span>Balance after you approve</span></p>
      <div class="d-links"><a href="demo.html?design={inv["slug"]}" data-track="detail_demo">{icon(I["eye"])} Live demo</a><a data-wa="Namaste Bfiluxe 🙏 I'd like to know more about the {inv["name"]} invitation.">{WA} Ask on WhatsApp</a><button class="linkbtn" id="ask">Ask a question</button></div>
      <div class="d-time"><ol><li><b>Details received</b><small>Names, functions, venues</small></li><li><b>Design &amp; preview</b><small>A private link to check</small></li><li><b>Ready</b><small>{days}</small></li></ol>
        <p>Counted from when we have your complete details and the 50% advance.</p></div>
      <div class="d-card"><p class="eyebrow">Made by hand, only for you</p><h3>This is your invitation</h3>
        <ul><li>{icon(I["edit"])}<div><b>Set by a real person</b><span>Our team in Jaipur types and checks every name.</span></div></li>
          <li>{icon(I["refresh"])}<div><b>One round of changes</b><span>See your preview and send all changes together.</span></div></li>
          <li>{icon(I["clock"])}<div><b>At your own pace</b><span>Share details online or on WhatsApp, whenever you are ready.</span></div></li>
          <li>{icon(I["lock"])}<div><b>One payment, no subscription</b><span>Your link stays live through the wedding and six months after.</span></div></li></ul></div>
      <div class="d-acc">
        <details class="acc"><summary>What's included</summary><p>A mobile invitation website with your names, families, every function with date, time and Google Maps, a private share link, a QR code for printed cards, and a ready-to-send WhatsApp message.</p></details>
        <details class="acc"><summary>Customization</summary><p>Change names, dates, venues, the number of events, language (English, Hindi, Marwari + Hindi or bilingual), opening blessing and music. Colours can be adjusted on Premium and Luxury.</p></details>
        <details class="acc"><summary>Delivery, payment &amp; changes</summary><p>Ready in {days} after we receive your details. Pay 50% to start and 50% after you approve. One free round of changes; spelling fixes are always free.</p></details>
      </div>
    </div>
  </div>
</div></section>
<section class="sec sec-tint" style="padding-top:56px"><div class="wrap">
  <div class="h-rule"><span>You may also like</span><span></span></div>
  <div class="grid-inv" id="similar">{"".join(card(x) for x in sim[:4])}</div>
</div></section>'''
    page(f"design-{inv['slug']}", f"{inv['name']}: {COLL[inv['collection']]} Digital Wedding Invitation | Bfiluxe",
         f"{inv['name']} digital wedding invitation: {inv['tagline'].lower()}. {COLL[inv['collection']]} collection, from {inr(inv['price'])}, ready in {days}.",
         body, "invitations", og_image=BASE + "/" + ART + inv["image"],
         ld=[{"@context": "https://schema.org", "@type": "Product", "name": f"{inv['name']} digital wedding invitation", "image": BASE + "/" + ART + inv["image"],
              "description": inv["desc"], "brand": {"@type": "Brand", "name": "Bfiluxe"}, "category": "Digital wedding invitation",
              "offers": {"@type": "Offer", "price": inv["price"], "priceCurrency": "INR", "availability": "https://schema.org/InStock", "url": f"{BASE}/design-{inv['slug']}.html", "seller": {"@id": BASE + "/#business"}}},
             {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Invitations", "item": BASE + "/invitations.html"},
                 {"@type": "ListItem", "position": 2, "name": COLL[inv["collection"]] + " Collection", "item": f"{BASE}/invitations.html?c={inv['collection']}"},
                 {"@type": "ListItem", "position": 3, "name": inv["name"], "item": f"{BASE}/design-{inv['slug']}.html"}]}])

# Old dynamic detail URL (invitation.html?slug=...) forwards to the static page
page("invitation", "Invitation · Bfiluxe", "Redirecting to the invitation design.",
     '<section class="sec center"><div class="wrap"><p class="lead" style="margin:0 auto">Opening the design… <a href="invitations.html">See all invitations</a></p></div></section>',
     "invitations", index=False)

# ---------------- Pricing ----------------
PRICE_FAQ = [
    ("Are there any hidden charges?", "No. The package price covers design, your invitation website, the share link and QR code, and one round of changes. Extra rounds or extra pages are quoted before we start."),
    ("How do I pay?", "On WhatsApp we confirm your package and share a UPI or bank transfer link. You pay 50% to start and 50% after you approve the final invitation."),
    ("Can I upgrade later?", "Yes. You can move from Basic to Premium or Luxury at any time; you only pay the difference."),
    ("How long does the invitation link stay live?", "Your link stays live through your wedding and for at least 6 months after, so guests can revisit the photos and details."),
    ("Do you offer a discount for multiple events or family weddings?", "Message us on WhatsApp. For sibling weddings or extra functions we quote a combined price."),
]
ROWS = [("Designs available", "Basic collection", "Basic + Premium", "All + bespoke"), ("Events / functions", "Up to 3", "Up to 8", "Unlimited"),
        ("Family names &amp; blessings", "✓", "✓", "✓"), ("Google Maps for venues", "✓", "✓", "✓"), ("Share link + QR code", "✓", "✓", "✓"),
        ("Hindi / English / bilingual", "✓", "✓", "✓"), ("Music or shehnai", "–", "✓", "✓"), ("Photo gallery &amp; countdown", "–", "✓", "✓"),
        ("RSVP with guest count", "–", "✓", "✓"), ("Custom colours &amp; motifs", "–", "–", "✓"), ("Family story / video page", "–", "–", "✓"),
        ("Priority WhatsApp support", "–", "–", "✓"), ("Pages", "One scrolling page", "One page with gallery &amp; RSVP sections", "Multiple pages (story, video)"),
        ("Delivery", "3–5 working days", "7–14 working days", "15–21 working days"), ("Free change rounds", "1", "1", "1"), ("Link stays live", "Wedding + 6 months", "Wedding + 6 months", "Wedding + 6 months"),
        ("Payment", "50% / 50%", "50% / 50%", "50% / 50%")]
PRICING = f'''
<section class="phead"><div class="wrap"><h1>Digital Wedding Invitation Pricing</h1><p class="lead">Three clear packages. Pay 50% to start and 50% only after you approve your invitation.</p></div></section>
<section class="sec" style="padding-top:36px"><div class="wrap">
  {plan_cards()}
  <div class="trust-row">
    <div>{icon(I["shield"])}<span><b>Pay half after approval</b>50% advance, 50% when you love it</span></div>
    <div>{icon(I["refresh"])}<span><b>Free spelling fixes</b>Always, even after sharing</span></div>
    <div>{icon(I["lock"])}<span><b>Private link</b>Only people you share it with can open it</span></div>
    <div>{icon(I["card"])}<span><b>UPI or bank transfer</b>No card needed</span></div>
  </div>
</div></section>
<section class="sec" id="videos"><div class="wrap">
  <div class="lx-head"><div><p class="eyebrow">Invitation videos</p><h2>Video packages</h2></div>
    <p class="lx-head-note">An animated video invite for WhatsApp, Instagram and Status. <a href="videos.html">What's in a video</a></p></div>
  {video_cards()}
</div></section>
<section class="sec sec-tint"><div class="wrap">
  <div class="sec-head center"><h2>Compare Packages</h2>{ORN}</div>
  <div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col">Feature</th><th scope="col">Basic<br><small>{mk("p", "Basic")} {pk("p", "Basic")}</small></th><th scope="col" class="hl">Premium<br><small>{mk("p", "Premium")} {pk("p", "Premium")}</small></th><th scope="col">Luxury<br><small>{mk("p", "Luxury")} {pk("p", "Luxury")}</small></th></tr></thead>
  <tbody>{"".join(f"<tr><th scope='row'>{a}</th><td>{b}</td><td class='hl'>{c}</td><td>{d}</td></tr>" for a, b, c, d in ROWS)}</tbody></table></div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="split" style="align-items:start">
    <div class="panel"><h3>What "one round of changes" means</h3>
      <p class="muted" style="margin-top:8px">After your first preview, send all your changes together in one message (text, names, timings, order of functions, music choice). We apply them and send the updated preview. Spelling and name corrections are always free, even later.</p>
      <h3 style="margin-top:18px">Not included</h3>
      <ul class="checks" style="margin-bottom:0"><li>{icon(I["x"])}Printed cards, photography or video shooting</li><li>{icon(I["x"])}Changing to a different design after the preview is approved</li><li>{icon(I["x"])}Writing a family story or translation from scratch on Basic</li></ul></div>
    <div class="panel"><h3>Add-ons, quoted before any work</h3>
      <p class="muted" style="margin:8px 0 12px">Tell us on WhatsApp and we'll quote first. Nothing is added to your bill unless you agree.</p>
      <ul class="addons"><li>Extra change round</li><li>Urgent delivery</li><li>Extra function pages beyond your package</li><li>An additional language</li><li>Custom illustration of your venue or family deity</li><li>Wedding video on the invitation</li><li>Keeping the link live for longer</li><li>Printed QR inserts for physical cards</li></ul>
      <a class="btn btn-wa" style="margin-top:14px" data-wa="Namaste Bfiluxe 🙏 Please share a quote for these add-ons:">{WA} Ask for a quote</a></div>
  </div>
</div></section>
<section class="sec sec-tint"><div class="wrap split" style="align-items:start">
  <div><h2>Pricing Questions</h2><p class="lead" style="margin-top:12px">Need a custom quote for several functions or family weddings? We'll reply within an hour.</p><div class="row" style="margin-top:18px"><a class="btn btn-wa" data-wa="Namaste Bfiluxe 🙏 Please share a quote for our wedding invitation.">{WA} Get a quote</a><a class="btn btn-ghost" href="contact.html">Send an enquiry</a></div></div>
  <div>{faq_html(PRICE_FAQ)}</div>
</div></section>'''
page("pricing", "Pricing: Digital Wedding Invitations from ₹3,999 | Bfiluxe",
     "Launch prices: Basic ₹3,999, Premium ₹8,999 and Luxury ₹24,999 digital wedding invitation packages. Pay 50% to start, 50% after approval. Compare features.",
     PRICING, "pricing", ld=[faq_ld(PRICE_FAQ), {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Bfiluxe invitation packages",
     "itemListElement": [{"@type": "Offer", "name": f"{n} digital wedding invitation", "price": p, "priceCurrency": "INR", "description": b} for n, p, d, b, f in PACKAGES]}])

# ---------------- How it works ----------------
HOW_FAQ = [
    ("How long does it take?", "Basic in 3–5 working days, Premium in 7–14 working days and Luxury in 15–21 working days after we receive your complete details."),
    ("Can I change details after it's shared?", "Yes. Your link stays the same, so guests always see the latest version. One round of changes is free; spelling fixes are always free."),
    ("Is it available in Hindi?", "Choose English, Hindi, Marwari + Hindi or bilingual. We add traditional blessings like ॥ श्री गणेशाय नमः ॥ on request."),
    ("How do guests receive it?", "You get a private link, a ready-to-forward WhatsApp message and a QR code you can print on physical cards."),
    ("Do you collect RSVPs?", "Yes, on Premium and Luxury: guests confirm attendance and guest count, and you see the list."),
    ("How do I pay?", "We confirm the package on WhatsApp and share a UPI or bank link. 50% to start, 50% after you approve."),
    ("What if I don't like the first preview?", "Tell us what to change. One full round of changes is included, and we can switch to another design of the same package."),
]
HOW_STEPS = [
    ("1", "Choose a Design", "image", "step-choose.jpg", "Browse Royal, Traditional, Elegant and Modern designs, or ask for a bespoke Luxury design. Not sure? Send us your wedding colours and we'll suggest three.",
     ["Large preview of every design", "Live demo on your phone", "Prices shown upfront"], ("invitations.html", "Browse designs")),
    ("2", "Share Your Details", "edit", "step-details.jpg", "Fill our simple form or just send the details on WhatsApp: names, families, functions, venues, language and music. Voice notes are fine too.",
     ["6-step form with live preview", "Save a draft and finish later", "Or send everything on WhatsApp"], ("customize.html", "Start customizing")),
    ("3", "Preview & Approve", "eye", "step-preview.jpg", "Our designer builds your invitation and sends a private preview link. Check every name and date on your own phone, and ask for changes.",
     ["Every name checked by hand", "One free round of changes", "Pay the balance only after approval"], None),
    ("4", "Share With Everyone", "share", "step-share.jpg", "You receive the final link, a ready-to-forward WhatsApp message and a QR code for printed cards. Update details anytime; the link stays the same.",
     ["One link for all guests", "QR code for printed kankotri", "Updates without re-sending"], ("demo.html", "See what guests receive")),
]
how_rows = "".join(f'''<div class="hrow reveal">
  <div class="hrow-img"><img data-img="{img}" alt="" loading="lazy" width="360" height="645"><span class="hrow-num">{n}</span></div>
  <div><p class="eyebrow">Step {n}</p><h3 style="font-size:clamp(26px,3.6vw,34px);color:var(--maroon);margin-top:6px">{t}</h3><p class="lead" style="margin-top:10px">{d}</p>
    <ul class="checks">{"".join(f"<li>{icon(I['check'])}{x}</li>" for x in pts)}</ul>
    {f'<a class="btn btn-outline" href="{cta[0]}">{cta[1]} {icon(I["arrow"])}</a>' if cta else ''}</div></div>''' for n, t, ic, img, d, pts, cta in HOW_STEPS)
HOW_LINE = ["Pick a design and package. Open any live demo on your phone first.", "Names, functions, venues and photos, online or on WhatsApp, in Hindi or English.", "We set every name by hand and send a private preview. One round of changes is included.", "Your link, QR code and a ready WhatsApp message. Guests open it in one tap."]
HOW = f'''
<section class="phead"><div class="wrap"><h1>How Bfiluxe Invitations Work</h1><p class="lead">From choosing a design to sharing with every relative: four simple steps, all on your phone.</p>
  <div class="stepchips">{"".join(f'<a href="#step-{n}"><b>{n}</b>{t}</a>' for n, t, *_ in HOW_STEPS)}</div></div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head center"><p class="eyebrow">The process</p><h2>Four steps, zero stress</h2></div>
  <ol class="roman">{"".join(f'<li id="step-{n}"><span class="rn">{"I II III IV".split()[k]}</span><h3>{t}</h3><p>{HOW_LINE[k]}</p><small>{tg}</small></li>' for k, ((n, t, ic, *_), tg) in enumerate(zip(HOW_STEPS, ["5 minutes", "At your own pace", "Ready from 3 working days", "Updates until the wedding"])))}</ol>
  <p class="center" style="margin-top:34px"><a class="btn btn-primary" href="customize.html">Start my invitation {icon(I["arrow"])}</a></p>
  <div class="incl4"><h2>Always included</h2><ul><li><b>Set by hand</b><span>A real person, never an automatic editor.</span></li><li><b>One round of changes</b><span>Spelling fixes are always free.</span></li><li><b>Live RSVP</b><span>See who is coming and how many (Premium and Luxury).</span></li><li><b>Hindi &amp; English</b><span>Or both, with every honorific checked.</span></li></ul></div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap hrows">{how_rows}</div></section>
<section class="sec sec-tint" style="padding-top:48px"><div class="wrap">
  <div class="sec-head center"><h2>Delivery Timeline</h2>{ORN}</div>
  <div class="timeline">
    <div class="tl"><span class="tag">Basic · {pk("p", "Basic")}</span><p style="margin-top:12px"><b>{dk("p", "Basic")}</b></p><p class="muted">One design, your names and up to 3 events, share link and QR.</p></div>
    <div class="tl tl-pop"><span class="tag">Premium · {pk("p", "Premium")}</span><p style="margin-top:12px"><b>{dk("p", "Premium")}</b></p><p class="muted">Up to 8 events, music, photo gallery, countdown and RSVP.</p></div>
    <div class="tl"><span class="tag">Luxury · {pk("p", "Luxury")}</span><p style="margin-top:12px"><b>{dk("p", "Luxury")}</b></p><p class="muted">Our grandest or a bespoke design, unlimited pages, priority support.</p></div>
  </div>
</div></section>
<section class="sec"><div class="wrap lx-split">
  <div><p class="eyebrow">Digital and printed</p><h2>Keep the printed kankotri for elders</h2></div>
  <div><p class="lead">Many families still post printed cards to elders and close relatives. Every Bfiluxe invitation comes with a QR code you can print on those cards, so the printed kankotri and the digital link work together.</p>
    <p style="margin-top:22px"><a class="tlink" href="digital-vs-printed-kankotri.html">Digital vs printed kankotri</a></p></div>
</div></section>
<section class="sec sec-tint"><div class="wrap">
  <div class="split" style="align-items:start">
    <div class="panel"><h3>What we need from you</h3><ul class="checks" style="margin-bottom:0">
      <li>{icon(I["check"])}Bride's and groom's names, exactly as they should appear</li>
      <li>{icon(I["check"])}Parents', grandparents' and elders' names (both families)</li>
      <li>{icon(I["check"])}Every function: date, time, venue and Google Maps link</li>
      <li>{icon(I["check"])}Language, blessing line and music choice</li>
      <li>{icon(I["check"])}Photos (optional, Premium and Luxury)</li></ul>
      <a class="btn btn-ghost" style="margin-top:16px" href="guide.html">{icon(I["book"])} Use our wording guide</a></div>
    <div class="policy">
      <div>{icon(I["card"])}<b>Payment</b><p>50% to start, 50% after approval. UPI or bank transfer.</p></div>
      <div>{icon(I["refresh"])}<b>Changes</b><p>One free round; spelling fixes always free. The link never changes.</p></div>
      <div>{icon(I["lock"])}<b>Privacy</b><p>Only people with your link can open it. We never share your details.</p></div>
      <div>{icon(I["clock"])}<b>Link validity</b><p>Live through the wedding and at least 6 months after.</p></div>
    </div>
  </div>
</div></section>
<section class="sec sec-tint"><div class="wrap">
  <div class="sec-head center"><h2>Digital vs Printed Cards</h2><p class="lead" style="margin:10px auto 0">Many families do both: a printed kankotri for elders and a Bfiluxe link for everyone. Add our QR code to your printed card.</p>{ORN}</div>
  <div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col"></th><th scope="col">Printed card</th><th scope="col" class="hl">Bfiluxe digital invitation</th></tr></thead><tbody>
    <tr><th scope="row">Reaching guests</th><td>Printing, then hand delivery or courier</td><td class="hl">One WhatsApp link, instantly</td></tr>
    <tr><th scope="row">Changing a date or venue</th><td>Reprint</td><td class="hl">Update; same link</td></tr>
    <tr><th scope="row">Maps, music, photos</th><td>–</td><td class="hl">✓</td></tr>
    <tr><th scope="row">RSVP and guest count</th><td>Phone calls</td><td class="hl">Collected for you</td></tr>
    <tr><th scope="row">NRI and outstation guests</th><td>Slow and costly</td><td class="hl">Same as local guests</td></tr>
  </tbody></table></div>
</div></section>
<section class="sec"><div class="wrap split" style="align-items:start">
  <div><h2>Questions</h2><p class="lead" style="margin-top:12px">Anything else? A designer answers on WhatsApp within an hour.</p><div class="row" style="margin-top:18px"><a class="btn btn-wa" data-wa>{WA} Ask on WhatsApp</a></div></div>
  <div>{faq_html(HOW_FAQ)}</div>
</div></section>
{cta()}'''
page("how-it-works", "How It Works: Digital Wedding Invitation in 4 Steps | Bfiluxe",
     "Choose a design, share your details, preview and approve, then share on WhatsApp. Ready from 3 working days; pay 50% after approval.", HOW, "how-it-works",
     ld=[faq_ld(HOW_FAQ), {"@context": "https://schema.org", "@type": "HowTo", "name": "How to get a digital Marwari wedding invitation from Bfiluxe",
         "totalTime": "P3D", "step": [{"@type": "HowToStep", "position": int(n), "name": t, "text": d} for n, t, ic, img, d, pts, cta in HOW_STEPS]}])

# ---------------- Customize ----------------
CUST = f'''
<section class="phead" style="padding:30px 0 26px"><div class="wrap"><h1 style="font-size:clamp(30px,5vw,44px)">Customize Your Invitation</h1><p class="lead">Add your wedding details and watch your invitation come to life.</p></div></section>
<section class="sec" style="padding-top:28px"><div class="wrap cz">
  <div class="panel">
    <div class="stepper" id="stepper"></div>
    <form id="cz-form" novalidate><div class="skel" style="height:300px;border-radius:12px"></div></form>
    <button type="button" class="btn btn-ghost btn-block mob-preview" id="show-pv" style="margin-top:14px">{icon(I["eye"])} See live preview</button>
  </div>
  <aside class="cz-preview" aria-label="Live preview">
    <button class="icon-btn pv-close" aria-label="Close preview">{icon(I["x"])}</button>
    <p class="eyebrow center" style="margin-bottom:14px">Live preview · <span id="pv-name"></span></p>
    <div class="preview-card" id="pv"></div>
    <p class="pv-events" id="pv-events"></p>
    <p class="center muted" style="font-size:13px;margin-top:6px">Preview only. Your designer will set the final typography.</p>
  </aside>
</div></section>'''
page("customize", "Customize Your Wedding Invitation | Bfiluxe", "Add names, events, venues, language, music and RSVP options to your Marwari wedding invitation, with a live preview.", CUST, None, bar=False)

# ---------------- Live demo invitation ----------------
DEMO = f'''
<div id="intro"></div>
<div class="petals" id="petals" aria-hidden="true"></div>
<div class="demo-ribbon"><span><b>Sample invitation</b> · names, venues and photos are fictional</span><a class="btn btn-sm btn-gold" id="demo-cta" href="customize.html">Create yours</a></div>
<header class="dv-cover"><div class="inv-wrap" id="dv-card"></div><a class="dv-scroll" href="#dv-blessing">Scroll to see the celebrations ↓</a></header>
<main id="main" class="dv">
  <h1 class="sr">Live demo of a Bfiluxe digital Marwari wedding invitation (sample names and venues)</h1>
  <section class="dv-sec reveal-dv" id="dv-blessing">
    <p class="deva" lang="hi" id="dv-bless-line">॥ शुभ विवाह ॥</p>
    <h2 data-h="bless">With the blessings of our elders</h2>
    <p id="dv-elders">Smt. Kamla Devi &amp; Late Shri Ramniwas Agarwal<br>Smt. Shanti Devi &amp; Shri Gopal Maheshwari</p>
    <div class="dv-fam" id="dv-fam"><div><b>Priya</b><span>D/o Smt. Sunita &amp; Shri Mahesh Agarwal, Jaipur</span></div><div class="dv-weds">weds</div><div><b>Rohan</b><span>S/o Smt. Rekha &amp; Shri Anil Maheshwari, Jodhpur</span></div></div>
  </section>
  <section class="dv-sec reveal-dv"><h2 data-h="story">Our story</h2>
    <div class="dv-story" id="dv-story-list">
      <figure><img data-img="demo-fort.jpg" alt="Illustration of the couple on the ramparts of a hill fort" loading="lazy"><figcaption><small>2023 · Jodhpur</small><b>We met at a cousin's sangeet</b><p>One dance, one long walk along the fort walls, and a lot of chai.</p></figcaption></figure>
      <figure><img data-img="demo-lake.jpg" alt="Illustration of the couple in a boat by a lake palace" loading="lazy"><figcaption><small>2025 · Udaipur</small><b>The question by the lake</b><p>Rohan asked; Priya said yes before he finished.</p></figcaption></figure>
      <figure><img data-img="demo-rings.jpg" alt="Illustration of mehendi hands holding a ring box" loading="lazy"><figcaption><small>This winter · Jaipur</small><b>Now, forever</b><p>Our families are coming together. We'd love you to be there.</p></figcaption></figure>
    </div></section>
  <section class="dv-sec dv-count reveal-dv"><h2 data-h="count">Counting down to the wedding</h2>
    <div class="count" id="count"><div><b data-u="d">0</b><span>Days</span></div><div><b data-u="h">0</b><span>Hours</span></div><div><b data-u="m">0</b><span>Minutes</span></div><div><b data-u="s">0</b><span>Seconds</span></div></div></section>
  <section class="dv-sec reveal-dv"><h2 data-h="events">Wedding celebrations</h2><p class="muted" style="margin-bottom:14px">Tap “Add to calendar” so you never miss a function.</p><div class="dv-events" id="dv-events"></div></section>
  <section class="dv-sec reveal-dv"><h2 data-h="venue">Wedding venue</h2><p id="dv-venue"><b>Royal Palace Gardens</b><br>Amer Road, Jaipur, Rajasthan</p>
    <div class="dv-map"><iframe id="dv-map-frame" title="Map of the wedding venue" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=Amer+Road,+Jaipur,+Rajasthan,+India&amp;z=14&amp;hl=en&amp;output=embed"></iframe></div>
    <p style="margin-top:14px"><a class="dv-dir" id="dv-dir" href="#" target="_blank" rel="noopener">Get directions</a> <small class="muted">· sample venue: directions open the area</small></p>
    <p class="muted" id="dv-stay" style="margin-top:12px;font-size:14px">Stay: rooms are booked for outstation guests. Message the family for details.</p></section>
  <section class="dv-sec reveal-dv" id="rsvp"><h2 data-h="rsvp">Will you join us?</h2><p class="muted" id="dv-rsvp-note">Please let us know by one week before the wedding.</p>
    <form class="form dv-rsvp" id="dv-rsvp" novalidate>
      <div class="field"><label for="r-name">Your name</label><input id="r-name" required autocomplete="name"></div>
      <div class="f2"><div class="field"><label for="r-att">Attending?</label><select id="r-att"><option>Yes, with joy</option><option>Sorry, can't make it</option></select></div>
      <div class="field"><label for="r-n">Number of guests</label><input id="r-n" type="number" min="1" max="20" value="2" inputmode="numeric"></div></div>
      <button class="btn btn-primary btn-block" type="submit">Send RSVP</button>
    </form></section>
  <section class="dv-sec reveal-dv"><h2 data-h="wishes">Blessings &amp; wishes</h2>
    <form class="form dv-rsvp" id="dv-wish" novalidate><div class="field"><label for="w-name">Your name</label><input id="w-name" required></div>
      <div class="field"><label for="w-msg">Your wish for the couple</label><textarea id="w-msg" required style="min-height:80px"></textarea></div><button class="btn btn-outline btn-block" type="submit">Post wish</button></form>
    <div class="wishes" id="wishes">
      <div class="wish"><b>Nani</b><p>Sada sukhi raho, mere bachchon. Bahut saara aashirwad.</p></div>
      <div class="wish"><b>Ankit &amp; Shruti</b><p>Can't wait to dance at the sangeet! Love you both.</p></div></div></section>
  <section class="dv-sec reveal-dv"><h2>Share the invitation</h2><p class="muted" style="margin-bottom:14px">Every invitation comes with a QR code for printed cards. Scan this one to open the demo.</p>
    <div class="qr-box" id="dv-qr" aria-label="QR code for this invitation"></div><div class="row" style="justify-content:center;margin-top:16px"><button class="btn btn-wa" id="dv-share">{WA} Share on WhatsApp</button><button class="btn btn-ghost" id="dv-copy">{icon(I["link"])} Copy link</button></div></section>
  <section class="dv-sec dv-switch"><p class="eyebrow">See this demo in another design</p><div class="dv-designs" id="dv-designs"></div></section>
  <footer class="dv-cta">
    <p class="eyebrow">Liked this invitation?</p>
    <h2>Make one for your family</h2>
    <p class="muted">Your names, every function and your favourite design, ready from 3 working days.</p>
    <ul class="dv-pills"><li>From ₹3,999</li><li>Hindi &amp; English</li><li>Pay 50% after approval</li></ul>
    <div class="dv-cta-btns"><a class="btn btn-primary" id="demo-cta2" href="customize.html">Create my invitation {icon(I["arrow"])}</a><a class="btn btn-wa" data-wa="Namaste Bfiluxe 🙏 I saw the live demo and would like an invitation like this.">{WA} WhatsApp us</a></div>
    <a class="dv-brand" href="index.html" aria-label="Bfiluxe home"><img src="img/logo-sm.webp" alt="Bfiluxe" width="200" height="174" loading="lazy"><span>Made with love by Bfiluxe</span></a>
  </footer>
</main>
<button class="music-btn" id="music" aria-pressed="false" aria-label="Play music">{icon(I["music"])}</button>'''
page("demo", "Live Demo: Digital Marwari Wedding Invitation | Bfiluxe",
     "Open a sample Bfiluxe digital wedding invitation: blessings, family names, countdown, every function with maps, gallery and RSVP. See it in any design.",
     DEMO, None, chrome=False)

# ---------------- Wedding guide (content for SEO / AEO / GEO) ----------------
RITUALS = [
    ("Sagai / Roka", "The formal engagement: families exchange blessings, gifts and shagun, and the wedding is fixed."),
    ("Ganesh Puja (Vinayak Sthapna)", "The first ritual at both homes: Lord Ganesha is invited so the wedding happens without obstacles. Most Marwari invitations open with ॥ श्री गणेशाय नमः ॥ for this reason."),
    ("Mayra (Bhaat)", "The bride's or groom's maternal uncle (mama) and his family arrive with clothes, jewellery and gifts for the mother and the family. It is usually a separate function on the invitation."),
    ("Pithi / Haldi", "A paste of turmeric, gram flour and oil is applied to the bride and groom by family women, with folk songs."),
    ("Mehendi", "Henna for the bride and the women of the family, often with the groom's initials hidden in the design."),
    ("Mahila Sangeet", "An evening of songs and dance led by the women of the family; today often a full sangeet night."),
    ("Nikasi and Baraat", "The groom, dressed in sehra and safa, leaves on a mare after his sister-in-law and family perform rituals. The baraat travels to the wedding venue with music."),
    ("Toran and Varmala", "At the bride's door the groom touches the toran (decorated arch) with a neem branch or sword, then the couple exchange garlands."),
    ("Phere", "The couple take seven rounds around the sacred fire, each with a vow. This is the main wedding ceremony and usually the main date on the invitation."),
    ("Vidaai and Griha Pravesh", "The emotional farewell of the bride, followed by her welcome into the groom's home."),
]
RIMG = {"Mayra (Bhaat)": ("ritual-mayra.jpg", "Miniature-style painting of the Mayra procession arriving with gifts"),
        "Pithi / Haldi": ("ritual-pithi.jpg", "Miniature-style painting of women applying pithi to the bride"),
        "Nikasi and Baraat": ("ritual-baraat.jpg", "Miniature-style painting of the groom on a mare in the baraat"),
        "Phere": ("ritual-phere.jpg", "Miniature-style painting of the couple taking phere around the sacred fire")}
GUIDE_FAQ = [
    ("When should we send a Marwari wedding invitation?", "Send it 4–8 weeks before the wedding (8–12 weeks for NRI guests), and a reminder on WhatsApp about one week before. A digital link makes the reminder easy."),
    ("What should a Marwari wedding invitation include?", "An opening blessing, the couple's names, both sets of parents (and often grandparents), the list of functions with date, time and venue, the RSVP contact, and a line of welcome. Many families also list the Mayra and Mahila Sangeet separately."),
    ("Which events go on the invitation?", "Usually Ganesh Puja, Mayra, Pithi/Haldi, Mehendi, Mahila Sangeet, Baraat, Phere and the Reception. Close-family rituals are often shared on a separate page for family only."),
    ("Should the invitation be in Hindi or English?", "Many families choose bilingual: Hindi for elders and the blessing, English for friends and NRI guests. Bfiluxe supports English, Hindi, Marwari + Hindi and bilingual."),
]
GUIDE = f'''
<section class="phead"><div class="wrap"><p class="eyebrow">Free guide</p><h1 style="margin-top:8px">Marwari Wedding Guide: Rituals, Invitation Wording &amp; Checklist</h1>
  <p class="lead">Everything families ask us before sending their invitations: the rituals in order, ready-to-use wording in Hindi and English, and when to send.</p>
  <div class="stepchips"><a href="#rituals">Rituals in order</a><a href="#wording">Invitation wording</a><a href="#checklist">Send-out checklist</a><a href="#faq">Questions</a></div></div></section>
<article class="sec guide"><div class="wrap narrow">
  <h2 id="rituals">Marwari wedding rituals, in order</h2>
  <p class="lead" style="margin-top:10px">Customs vary by family and region, so always check with your elders. This is the order most Marwari weddings follow.</p>
  <ol class="ritual-list">{"".join(f"<li><h3>{t}</h3><p>{d}</p>" + (f'<figure><img data-img="{RIMG[t][0]}" alt="{RIMG[t][1]}" loading="lazy" width="1000" height="666"></figure>' if t in RIMG else "") + "</li>" for t, d in RITUALS)}</ol>

  <h2 id="wording" style="margin-top:56px">Invitation wording you can use</h2>
  <p class="lead" style="margin-top:10px">Copy, change the names and send to us, or paste it into the <a href="customize.html">customize form</a>.</p>
  <div class="wording">
    <div class="word-card"><p class="eyebrow">Hindi</p><p lang="hi" class="hi">॥ श्री गणेशाय नमः ॥<br><br>सादर आमंत्रण<br><br>श्रीमती सुनीता एवं श्री महेश अग्रवाल<br>की सुपुत्री<br><b>चि. प्रिया</b><br>संग<br><b>चि. रोहन</b><br>सुपुत्र श्रीमती रेखा एवं श्री अनिल माहेश्वरी<br><br>के शुभ विवाह के पावन अवसर पर<br>आप सपरिवार सादर आमंत्रित हैं।</p>
      <button class="btn btn-sm btn-ghost" data-copy>{icon(I["link"])} Copy</button></div>
    <div class="word-card"><p class="eyebrow">English</p><p>॥ Shri Ganeshaya Namah ॥<br><br>With the blessings of our elders,<br>Mrs Sunita &amp; Mr Mahesh Agarwal<br>request the pleasure of your company<br>at the wedding of their daughter<br><b>Priya</b><br>with<br><b>Rohan</b><br>son of Mrs Rekha &amp; Mr Anil Maheshwari.</p>
      <button class="btn btn-sm btn-ghost" data-copy>{icon(I["link"])} Copy</button></div>
    <div class="word-card"><p class="eyebrow">WhatsApp message</p><p>Namaste 🙏<br>With great joy we invite you and your family to the wedding of Priya &amp; Rohan.<br>All functions, venues and maps are here: <i>[your Bfiluxe link]</i><br>Please RSVP on the link. Your blessings mean everything to us.<br>— Agarwal &amp; Maheshwari families</p>
      <button class="btn btn-sm btn-ghost" data-copy>{icon(I["link"])} Copy</button></div>
  </div>

  <h2 id="checklist" style="margin-top:56px">Invitation send-out checklist</h2>
  <ul class="checks big">
    <li>{icon(I["check"])}<span><b>8–10 weeks before:</b> finalise the guest list and the list of functions with your elders.</span></li>
    <li>{icon(I["check"])}<span><b>6–8 weeks before:</b> choose a design and send names, dates and venues (double-check spellings of elders' names).</span></li>
    <li>{icon(I["check"])}<span><b>4–8 weeks before:</b> share the invitation link on WhatsApp; post printed cards with the QR code to elders.</span></li>
    <li>{icon(I["check"])}<span><b>2 weeks before:</b> check RSVPs and guest counts; share with your caterer and hotel.</span></li>
    <li>{icon(I["check"])}<span><b>1 week before:</b> send a reminder with the same link; update any timing changes.</span></li>
  </ul>
  <div class="panel panel-gold center" style="margin-top:40px"><h2 style="font-size:30px">Want us to handle the wording?</h2><p class="lead" style="margin:10px auto 18px">Every Bfiluxe invitation includes wording help in Hindi or English, checked by hand.</p>
    <div class="row" style="justify-content:center"><a class="btn btn-primary" href="invitations.html">Choose a design</a><a class="btn btn-wa" data-wa>{WA} Ask on WhatsApp</a></div></div>

  <h2 id="faq" style="margin-top:56px">Questions families ask</h2>
  <div style="margin-top:10px">{faq_html(GUIDE_FAQ)}</div>
</div></article>'''
page("guide", "Marwari Wedding Rituals & Invitation Wording Guide (Hindi & English) | Bfiluxe",
     "Marwari wedding rituals in order (Ganesh puja, Mayra, Pithi, Mahila Sangeet, Baraat, Phere), invitation wording in Hindi and English, and a send-out checklist.",
     GUIDE, None, ld=[faq_ld(GUIDE_FAQ), {"@context": "https://schema.org", "@type": "Article", "headline": "Marwari Wedding Guide: Rituals, Invitation Wording & Checklist",
     "author": {"@id": BASE + "/#business"}, "publisher": {"@id": BASE + "/#business"}, "dateModified": TODAY, "inLanguage": "en-IN", "image": IMGBASE + "hero.jpg"}])

# ---------------- About ----------------
ABOUT = f'''
<section class="sec" style="padding-top:44px"><div class="wrap about-hero">
  <div>
    <p class="eyebrow">About Bfiluxe</p>
    <h1 style="margin-top:10px">Preserving Marwari Traditions in a Digital Way</h1>
    <p class="lead" style="margin-top:16px">Bfiluxe is a digital invitation studio in {BIZ["city"]}, {BIZ["region"]}, that designs wedding invitations only for Marwari families.</p>
    <p style="margin-top:14px">We blend Marwari customs, royal Rajasthani art and modern convenience: from the first ॥ श्री गणेशाय नमः ॥ to the last reception dinner, every function and every elder's name is in its right place.</p>
    <div class="row" style="margin-top:22px"><a class="btn btn-primary" href="invitations.html">See our designs</a><a class="btn btn-wa" data-wa>{WA} Talk to us</a></div>
  </div>
  <div class="arch-img" data-img="about-haveli.jpg" role="img" aria-label="Shekhawati haveli courtyard with painted frescoes"></div>
</div></section>
<section class="sec sec-tint"><div class="wrap split">
  <div><p class="eyebrow">Our story</p><h2 style="margin-top:8px">From kankotri to your phone</h2>
    <p class="lead" style="margin-top:14px">Every Marwari wedding begins with a kankotri: an invitation carried with care to every relative. Families now share invitations on WhatsApp, but most digital cards forget the rituals, the elders and the language that make a Marwari wedding what it is.</p>
    <p style="margin-top:12px">Bfiluxe was started to fix that: invitations that honour every ritual, list every elder correctly and still feel effortless for guests to open.</p>
    <img class="wide-img" style="margin-top:22px" data-img="about-studio-desk.jpg" alt="Designer's desk with invitation sketches, gold pen and colour swatches" loading="lazy" width="1200" height="800"></div>
  <div><p class="eyebrow">Our heritage</p><h2 style="margin-top:8px">Inspired by Rajasthan</h2>
    <p class="lead" style="margin-top:14px">Shekhawati havelis, jharokha windows, royal elephants, peacocks and the colours of Gangaur: our designs carry the same craft, made for the screens your family uses every day.</p>
    <a class="guide-teaser" href="guide.html" style="margin-top:12px">{icon(I["book"])}<span><b>Read our Marwari Wedding Guide</b><br><small>Rituals in order and invitation wording in Hindi &amp; English.</small></span></a></div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head center"><h2>What We Stand For</h2>{ORN}</div>
  <div class="values">
    <div class="value">{icon(I["lotus"])}<h3>Respect for tradition</h3><p>Correct ritual names, blessings and the order of elders, as your family follows them.</p></div>
    <div class="value">{icon(I["users"])}<h3>Craft &amp; accuracy</h3><p>Every name is checked by hand before you see a preview.</p></div>
    <div class="value">{icon(I["shield"])}<h3>Privacy &amp; trust</h3><p>Private links, no ads, and you pay the balance only after approval.</p></div>
  </div>
</div></section>
{cta()}'''
# About page removed (19 Nov 2026): about.html now forwards to the homepage (see redirects below)

# ---------------- Contact ----------------
CONTACT_FAQ = [
    ("How quickly will you reply?", f"Within an hour on WhatsApp during studio hours ({BIZ['hours']}). Messages after hours are answered the next morning."),
    ("Can I call instead?", f"Yes, call {BIZ['phone']} during studio hours. If we miss your call we'll call back the same day."),
    ("Do I need to visit the studio?", "No. Everything happens on WhatsApp and email, so families anywhere in India or abroad can order."),
    ("What should I send in my first message?", "Your wedding date, city, the functions you want on the invitation and any design you liked. We'll suggest designs and a package."),
]
CONTACT = f'''
<section class="phead"><div class="wrap"><h1>Contact Bfiluxe</h1><p class="lead">Have a question or want a custom invitation? Talk to a designer today; we reply within an hour.</p>
  <div class="quick">
    <a class="btn btn-wa" data-wa>{WA} WhatsApp</a>
    <a class="btn btn-outline" href="tel:{BIZ["tel"]}">{icon(I["call"])} Call</a>
    <a class="btn btn-outline" href="mailto:{BIZ["email"]}">{icon(I["mail"])} Email</a>
  </div></div></section>
<section class="sec" style="padding-top:36px"><div class="wrap contact">
  <div class="cinfo">
    <a class="wa" data-wa><span class="ci-ic">{WA}</span><span><b>WhatsApp (fastest)</b><span>{BIZ["phone"]} · replies within an hour</span></span></a>
    <a href="tel:{BIZ["tel"]}"><span class="ci-ic">{icon(I["call"])}</span><span><b>Call us</b><span>{BIZ["phone"]}</span></span></a>
    <a href="mailto:{BIZ["email"]}"><span class="ci-ic">{icon(I["mail"])}</span><span><b>Email</b><span>{BIZ["email"]}</span></span></a>
    <div class="ci"><span class="ci-ic">{icon(I["pin"])}</span><span><b>Studio</b><span>{BIZ["city"]}, {BIZ["region"]}, India · working online with families everywhere</span></span></div>
    <div class="ci"><span class="ci-ic">{icon(I["clock"])}</span><span><b>Hours</b><span>{BIZ["hours"]}</span></span></div>
    <a href="bfi-contact.vcf" download><span class="ci-ic">{icon(I["download"])}</span><span><b>Save our contact</b><span>Add Bfiluxe to your phone in one tap</span></span></a>
  </div>
  <div class="panel panel-gold">
    <h2 style="font-size:30px;margin-bottom:6px">Send an enquiry</h2><p class="muted" style="margin-bottom:18px">Tell us a little about your wedding. We'll reply on WhatsApp with design suggestions and a price.</p>
    <div id="c-status"></div>
    <form class="form" id="contact-form" novalidate>
      <div class="f2"><div class="field"><label for="c-name">Your name <span class="req">*</span></label><input id="c-name" name="name" required autocomplete="name" placeholder="Enter your name"></div>
      <div class="field"><label for="c-phone">WhatsApp number <span class="req">*</span></label><input id="c-phone" name="phone" type="tel" required inputmode="tel" autocomplete="tel" placeholder="10-digit mobile"></div></div>
      <div class="f2"><div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" autocomplete="email" placeholder="you@example.com"></div>
      <div class="field"><label for="c-date">Wedding date</label><input id="c-date" name="wedding_date" type="date"></div></div>
      <div class="f2"><div class="field"><label for="c-city">City</label><input id="c-city" name="city" autocomplete="address-level2" placeholder="e.g. Jaipur"></div>
      <div class="field"><label for="c-pkg">Package</label><select id="c-pkg" name="package"><option>Not sure</option><option>Basic</option><option>Premium</option><option>Luxury</option></select></div></div>
      <div class="field"><label for="c-design">Preferred design</label><select id="c-design" name="design"><option value="">Not decided yet</option>{"".join(f'<option value="{i["slug"]}">{i["name"]}</option>' for i in CATALOG)}</select></div>
      <div class="field"><label for="c-msg">Your message <span class="req">*</span></label><textarea id="c-msg" name="message" required placeholder="Functions, number of guests, colours you love…"></textarea></div>
      <input type="text" name="company" tabindex="-1" autocomplete="off" class="sr" aria-hidden="true">
      <label class="check"><input type="checkbox" name="consent" required> I agree to be contacted on WhatsApp about my enquiry.</label>
      <button class="btn btn-primary btn-block" type="submit">Send Enquiry {icon(I["arrow"])}</button>
    </form>
  </div>
</div></section>
<section class="sec sec-tint"><div class="wrap">
  <div class="sec-head center"><h2>What Happens Next</h2>{ORN}</div>
  <div class="next3">
    <div><span>1</span><h3>We reply within an hour</h3><p>A designer messages you on WhatsApp with 2–3 design suggestions.</p></div>
    <div><span>2</span><h3>You confirm a package</h3><p>Pay 50% by UPI or bank transfer and send your details.</p></div>
    <div><span>3</span><h3>Preview from 3 working days</h3><p>Approve, pay the balance and share with every guest.</p></div>
  </div>
</div></section>
<section class="sec"><div class="wrap split" style="align-items:start">
  <div><h2>Working with us</h2><p class="lead" style="margin-top:10px">We are a {BIZ["city"]} studio working online, so families anywhere in India or abroad can order without travelling. Everything happens on WhatsApp and email.</p></div>
  <div><h2>Contact Questions</h2><div style="margin-top:10px">{faq_html(CONTACT_FAQ)}</div></div>
</div></section>'''
page("contact", "Contact Bfiluxe | WhatsApp +91 89495 09745", "Talk to Bfiluxe on WhatsApp, phone or email, or send an enquiry. We reply within an hour, 10am–8pm. Studio in Jaipur, serving families everywhere.",
     CONTACT, "contact", ld=[ORG_LD, faq_ld(CONTACT_FAQ)])

# ---------------- Login / Account ----------------
GOOGLE = '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3 0 5.8 1.1 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3 0 5.8 1.1 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3a12 12 0 0 1-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'
LOGIN = '''
<section class="sec ap-page"><div class="wrap">
  <div class="ap-card" id="auth-root"><noscript><p>Please turn on JavaScript to sign in, or message us on WhatsApp.</p></noscript></div>
</div></section>'''
page("login", "Sign in · Bfiluxe", "Sign in or create your Bfiluxe account with email or Google.", LOGIN, None, bar=False, index=False)
ACCT = '''
<section class="phead" style="padding:30px 0 26px"><div class="wrap"><h1 style="font-size:clamp(30px,5vw,44px)">My Account</h1></div></section>
<section class="sec" style="padding-top:28px"><div class="wrap"><div class="acct" id="account"><div class="panel skel" style="height:320px"></div><div class="panel skel" style="height:320px"></div></div></div></section>'''
page("account", "My Account · Bfiluxe", "Your saved invitations, favourites and enquiries.", ACCT, None, bar=False, index=False)

# ---------------- Legal ----------------
PRIV = f'''<section class="phead"><div class="wrap"><h1>Privacy Policy</h1><p class="lead">Last updated {date.today().strftime("%d %B %Y")}</p></div></section>
<article class="sec guide"><div class="wrap narrow legal">
<p>Bfiluxe ("Bfiluxe", "we") respects your privacy. This policy explains what we collect and why.</p>
<h2>What we collect</h2><ul><li>Details you send in enquiry and customize forms: names, phone, email, wedding date, city, functions, venues and messages.</li><li>Account details if you create an account: name, email, phone, saved drafts, favourites and reviews.</li><li>Basic technical data needed to run the website securely.</li></ul>
<h2>How we use it</h2><ul><li>To reply to your enquiry and make your invitation.</li><li>To contact you on WhatsApp, phone or email about your order.</li><li>We never sell your data and never use it for unrelated advertising.</li></ul>
<h2>Your invitation</h2><p>Your invitation is published at a private link. Anyone you share the link with can open it. Ask us at any time to take it down.</p>
<h2>Storage</h2><p>Data is stored with our hosting providers (Supabase and Vercel) using encrypted connections. Only you and the Bfiluxe team can see your enquiries and drafts.</p>
<h2>Your choices</h2><p>Ask us to view, correct or delete your data by writing to <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a> or WhatsApp {BIZ["phone"]}.</p>
</div></article>'''
page("privacy", "Privacy Policy · Bfiluxe", "How Bfiluxe collects, uses and protects your information.", PRIV, None)
TERMS = f'''<section class="phead"><div class="wrap"><h1>Terms of Service</h1><p class="lead">Last updated {date.today().strftime("%d %B %Y")}</p></div></section>
<article class="sec guide"><div class="wrap narrow legal">
<h2>Orders and payment</h2><p>Package prices are shown on the <a href="pricing.html">pricing page</a> and each design page. Work starts after a 50% advance; the balance is due after you approve the final invitation and before the final link is shared.</p>
<h2>Delivery</h2><p>Delivery times (3–5, 7–14 or 15–21 working days) start once we have your complete details. We tell you in advance if a date is not possible.</p>
<h2>Changes</h2><p>One round of changes is included in every package: after the first preview, send all your changes together in one message and we apply them. Spelling and name corrections are always free. Further rounds, a different design after approval, or extra pages are quoted before we make them.</p>
<h2>Your responsibilities</h2><p>Please check every name, date, time and venue in the preview before approving. After approval, we are not responsible for details you supplied incorrectly, though we will still correct spellings for free.</p>
<h2>Cancellations and refunds</h2><p>If you cancel before we share the first preview, we refund the advance minus any work already done. After the first preview, the advance is not refundable.</p>
<h2>Your content</h2><p>You confirm you have the right to use the names, photos and music you send. We may show a design in our portfolio only with your permission and never with your personal details.</p>
<h2>Link availability</h2><p>Invitation links stay live through the wedding and for at least 6 months after.</p>
<h2>Contact</h2><p><a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a> · WhatsApp {BIZ["phone"]}</p>
</div></article>'''
page("terms", "Terms of Service · Bfiluxe", "Orders, payment, delivery, changes and refunds for Bfiluxe digital wedding invitations.", TERMS, None)

# ---------------- 404 ----------------
NF = f'''<section class="sec center"><div class="wrap"><p class="deva" lang="hi">॥ शुभ विवाह ॥</p><h1 style="margin-top:10px">This door is closed</h1><p class="lead" style="margin:14px auto 24px">The page you're looking for isn't here. Let's take you somewhere beautiful.</p><div class="row" style="justify-content:center"><a class="btn btn-primary" href="index.html">Go home</a><a class="btn btn-ghost" href="invitations.html">See invitations</a></div></div></section>
'''
page("404", "Page not found · Bfiluxe", "Page not found.", NF, None, index=False)



FAQ_GROUPS = [
    ("Marwari invitations", [
        ("What is a Marwari kankotri?", "A kankotri is the traditional Marwari wedding invitation. It opens with a blessing to Lord Ganesha, names the couple with both families and elders, and lists each function, from Ganesh Sthapana and Mayra to Phere. A digital kankotri carries the same content as a mobile invitation website."),
        ("What should a Marwari wedding invitation include?", "An opening blessing, the couple's names, both sets of parents (often grandparents too), each function with date, time and venue, an RSVP contact and a line of welcome. See our <a href='guide.html#wording'>wording guide</a>."),
        ("How can I create a digital Marwari wedding invitation?", "Choose a design, share names, functions and venues through our <a href='customize.html'>online form</a> or on WhatsApp, review the preview on your phone, then share the final link and QR code."),
        ("Can a digital invitation include Mayra and Pithi?", "Yes. Add any function your family celebrates, including Mayra (Bhaat), Pithi, Mahila Sangeet, Nikasi and Toran, each with its own date, time, venue and notes."),
        ("Can wedding invitations be written in Hindi?", "Yes. Choose English, Hindi, Marwari with Hindi, or bilingual. Many families use Hindi for the blessing and elders' names and English for friends and NRI guests."),
        ("What is the difference between a video invitation and an invitation website?", "A video plays once and cannot be updated. An invitation website stays open on the guest's phone, has a separate entry for every function with maps, can collect RSVPs and can be updated without re-sending."),
    ]),
    ("Features", [
        ("Can I include multiple wedding events?", "Yes. Basic includes up to 3 functions, Premium up to 8, and Luxury has no limit."),
        ("How does RSVP work on a wedding invitation website?", "On Premium and Luxury, guests tap RSVP on the invitation, choose whether they are attending and how many people are coming. You receive the responses, so you can share numbers with your caterer and hotel."),
        ("Can I share the invitation through WhatsApp?", "Yes. You receive a private link and a ready-to-forward WhatsApp message. The link opens directly in the phone's browser, with no app to install."),
        ("Can I add Google Maps directions?", "Yes. Every function can have its own Google Maps link, so guests get directions in one tap."),
        ("Do you provide a QR code?", "Yes, every package includes a QR code you can print on physical cards or show at the venue."),
    ]),
    ("Ordering, delivery and payment", [
        ("How long does it take to create a wedding invitation website?", "Basic in 3–5 working days, Premium in 7–14 working days and Luxury in 15–21 working days, counted from when we have all your details and the advance."),
        ("How long does the invitation link remain active?", "Through your wedding and for at least 6 months after it."),
        ("How do I pay?", "50% advance by UPI or bank transfer to start, and the remaining 50% after you approve the preview, before the final link is delivered."),
        ("What does one free revision mean?", "After your first preview, send all your changes together in one message and we apply them. Spelling and name corrections are always free."),
        ("Can I cancel?", "If you cancel before the first preview, we refund the advance minus any work already done. After the first preview the advance is not refundable. See <a href='terms.html'>terms</a>."),
    ]),
]
FAQ_ALL = [q for _, g in FAQ_GROUPS for q in g]
FAQ_BODY = f'''
<section class="phead"><div class="wrap"><h1>Frequently Asked Questions</h1><p class="lead">Clear answers about digital Marwari wedding invitations, features, delivery and payment.</p>
  <div class="stepchips">{"".join(f'<a href="#g{n}">{t}</a>' for n, (t, _) in enumerate(FAQ_GROUPS))}</div></div></section>
<section class="sec"><div class="wrap narrow">
  {"".join(f'<h2 id="g{n}" style="font-size:30px;margin:{0 if n == 0 else 40}px 0 10px">{t}</h2>' + "".join(f'<details class="acc" {"open" if k == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for k, (q, a) in enumerate(g)) for n, (t, g) in enumerate(FAQ_GROUPS))}
  <div class="panel panel-gold center" style="margin-top:40px"><h2 style="font-size:28px">Still have a question?</h2><p class="lead" style="margin:10px auto 18px">Message us and a designer will answer.</p>
    <div class="row" style="justify-content:center"><a class="btn btn-wa" data-wa>{WA} Ask on WhatsApp</a><a class="btn btn-ghost" href="contact.html">Contact page</a></div></div>
</div></section>'''
page("faq", "FAQ: Digital Marwari Wedding Invitations, Kankotri, RSVP & Pricing | Bfiluxe",
     "Answers about digital Marwari wedding invitations: what a kankotri includes, Mayra and Pithi, Hindi wording, RSVP, WhatsApp sharing, maps, delivery time, link validity and payment.",
     FAQ_BODY, None, ld=[faq_ld(FAQ_ALL)])


# ---------------- Our Work was removed (13 Nov 2026): old addresses forward to the invitations ----------------
(OUT / "about.html").write_text(f'''<!doctype html><html lang="en-IN"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=index.html"><link rel="canonical" href="{BASE}/"><title>Bfiluxe</title></head>
<body><p><a href="index.html">Go to Bfiluxe</a></p></body></html>
''')
for _old in ("work", "work-mahi-ayush", "work-chittorgarh-engagement"):
    (OUT / f"{_old}.html").write_text(f'''<!doctype html><html lang="en-IN"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=invitations.html"><link rel="canonical" href="{BASE}/invitations.html"><title>Invitations · Bfiluxe</title></head>
<body><p><a href="invitations.html">See our invitations</a></p></body></html>
''')



# ---------------- Invitation videos ----------------
VIDEO_FAQ = [
    ("What is an invitation video?", "A short animated video with your blessing, names, families, functions and venues, set to music. Guests watch it on WhatsApp or Instagram, and you can share it as a Status."),
    ("What format will I receive?", "A vertical MP4 video (9:16), the size that fits WhatsApp, Instagram Reels and Status."),
    ("How long does it take?", "Every video is ready in 2–3 working days, counted from when we have your complete details and the 50% advance."),
    ("Can the video be in Hindi?", "Yes: Hindi, English or bilingual. Traditional lines such as ॥ श्री गणेशाय नमः ॥ can be added."),
    ("Can I have a video and an invitation website?", "Yes. Many families send the video first and the website link for maps, RSVP and details. Ask on WhatsApp for both together."),
    ("How do I pay?", "50% to start and 50% after you approve the video. One round of changes is included."),
]
VP_SCENES = [("cover", "The seal breaks"), ("names", "Blessing and family names"), ("date", "The date is revealed"), ("countdown", "Countdown to the phere"), ("functions", "Every function"), ("venue", "Venue and maps"), ("rsvp", "Please join us")]
VP_MOODS = [("Shehnai", "Classic and auspicious"), ("Santoor", "Soft and romantic"), ("Bansuri", "Calm, for evenings"), ("Dhol", "Festive, for the baraat"), ("Piano", "Modern and minimal")]
VIDEO_BODY = f"""
<section class="phead"><div class="wrap"><p class="eyebrow">Invitation videos</p><h1>Wedding Invitation Videos</h1>
  <p class="lead">A short animated video invitation with your blessing, names and every function, set to music and ready to forward on WhatsApp. From {inr(1499)}.</p>
  <div class="row hero-mini"><a class="btn btn-primary" href="#video-prices">See video prices</a><a class="btn btn-outline" data-wa="Namaste Bfiluxe 🙏 I'd like an invitation video.">Ask on WhatsApp</a></div></div></section>

<section class="sec vp-sec"><div class="wrap vp-grid">
  <div><div class="h-rule"><span>Watch it play</span><span>Scenes from a sample invitation</span></div>
    <h2 class="h-display">Thirty seconds, <em>every name in its place.</em></h2>
    <p class="h-lead">Each scene holds long enough for elders to read, then moves on with the music.</p>
    <ol class="vp-scenes">{"".join(f'<li data-scene="{n}"{" class=on" if n == 0 else ""}><span>{n + 1:02d}</span>{t}</li>' for n, (k, t) in enumerate(VP_SCENES))}</ol></div>
  <div class="vp-player" data-player aria-hidden="true"><span class="h-bigphone"><span class="phone-screen">
    <span class="vp-bars">{"".join('<i><b></b></i>' for _ in VP_SCENES)}</span>
    {"".join(f'<img data-scene="{n}"{" class=on" if n == 0 else ""} src="img/screens/{k}.webp" alt="" width="540" height="1041" loading="lazy">' for n, (k, t) in enumerate(VP_SCENES))}
    <span class="vp-eq"><i></i><i></i><i></i><i></i><i></i></span></span></span></div>
</div></section>

<section class="sec sec-tint"><div class="wrap">
  <div class="h-rule"><span>What's inside</span><span>Short enough to watch in one go</span></div>
  <h2 class="h-display">Made for WhatsApp, <em>Reels and Status.</em></h2>
  {journey([("lotus", "The blessing", "॥ श्री गणेशाय नमः ॥ or your family's line, to open the video."), ("users", "Names and families", "The couple, parents and elders, in Hindi, English or both."), ("clock", "Every function", "Dates, times and venues, from Mayra to the reception (Premium and Luxury)."), ("music", "Music and photos", "Shehnai or instrumental music, with your photos on Premium and Luxury.")])}
</div></section>

<section class="sec"><div class="wrap">
  <div class="h-rule"><span>One video, every screen</span><span>Sized for where it will be watched</span></div>
  <h2 class="h-display">Status, chats <em>and the big screen.</em></h2>
  <div class="vp-formats">
    <figure class="vf vf-916"><span class="vf-frame"><img src="img/art/cover-gulabi-bagh.webp" alt="" width="720" height="1290" loading="lazy"><i class="vf-play"></i></span><figcaption><b>9:16</b>WhatsApp Status &amp; Reels</figcaption></figure>
    <figure class="vf vf-11"><span class="vf-frame"><img src="img/art/cover-neel-mahal.webp" alt="" width="720" height="1290" loading="lazy"><i class="vf-play"></i></span><figcaption><b>1:1</b>WhatsApp chats &amp; posts</figcaption></figure>
    <figure class="vf vf-169"><span class="vf-frame"><img src="img/art/bg-flatlay.webp" alt="" width="1264" height="848" loading="lazy"><i class="vf-play"></i></span><figcaption><b>16:9</b>TV at the venue &amp; YouTube</figcaption></figure>
  </div>
  <p class="lx-fine center">9:16 comes with every package. Ask us for 1:1 or 16:9 versions.</p>
</div></section>

<section class="sec sec-tint"><div class="wrap">
  <div class="h-rule"><span>The music</span><span>Choose the mood</span></div>
  <h2 class="h-display">Set it to <em>your family's sound.</em></h2>
  <div class="vp-moods">{"".join(f'<div class="vm" style="--i:{n}"><span class="vm-eq"><i></i><i></i><i></i><i></i></span><b>{t}</b><small>{d}</small></div>' for n, (t, d) in enumerate(VP_MOODS))}</div>
</div></section>

<section class="sec sec-tint" id="video-prices"><div class="wrap">
  <div class="lx-head"><div><p class="eyebrow">Prices</p><h2>Three video packages</h2></div>
    <p class="lx-head-note">Pay 50% to start and 50% after you approve the video. Delivery time starts once we have your complete details and the advance.</p></div>
  {video_cards()}
</div></section>

<section class="sec"><div class="wrap lx-split">
  <div><p class="eyebrow">Video and website</p><h2>Send the video, share the link</h2></div>
  <div><p class="lead">A video is perfect for the first message on WhatsApp. An invitation website keeps every detail in one place afterwards: maps for each venue, RSVP, countdown and photos.</p>
    <div class="row" style="margin-top:22px"><a class="btn btn-outline" href="invitations.html">See invitation websites</a><a class="tlink" href="invitations.html#live">Open a live sample</a></div></div>
</div></section>

<section class="sec sec-tint"><div class="wrap lx-split lx-faq">
  <div><p class="eyebrow">Questions</p><h2>Invitation video FAQ</h2><p class="lead">Anything else? Ask us on WhatsApp.</p></div>
  <div>{faq_html(VIDEO_FAQ)}</div>
</div></section>
"""
page("videos", "Wedding Invitation Videos from ₹1,499 | Bfiluxe",
     "Animated wedding invitation videos for WhatsApp, Instagram and Status: blessing, names, functions and music. Basic ₹1,499, Premium ₹2,499, Luxury ₹3,999.",
     VIDEO_BODY, "videos", ld=[faq_ld(VIDEO_FAQ), {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Bfiluxe invitation videos",
     "itemListElement": [{"@type": "Offer", "name": f"{n} invitation video ({ln})", "price": pr, "priceCurrency": "INR", "description": b} for n, pr, d, ln, b, f in VIDEO_PACKAGES]}])

# ---------------- Free digital card maker (any occasion) ----------------
FREE_FAQ = [
    ("Is the card maker really free?", "Yes. Choose a template, type your details and download the card as an image or share it on WhatsApp. No sign-up and no watermark on your text."),
    ("Which occasions are included?", "16 templates: wedding, save the date, Sagai, anniversary, kids' and adult birthdays, Godh Bharai, Naamkaran, Mundan, Griha Pravesh, puja or bhajan sandhya, Diwali, Holi, Teej and Gangaur, retirement and prayer meet."),
    ("Can I download a PDF to print?", "Yes. Download as PNG, JPG or a print-ready PDF. Choose Card size for printing, Status size for WhatsApp or Instagram stories, or Square for posts. You can also download any template blank, without text."),
    ("Can I write in Hindi?", "Yes. Type in Hindi or English; Devanagari is supported in every text box."),
    ("Can Bfiluxe make a full invitation website for my event?", "Yes. For weddings and big family functions we make a full invitation website with every event, maps, music and RSVP. See <a href='pricing.html'>pricing</a>."),
]
FREE_PAGE = f'''
<section class="phead"><div class="wrap"><p class="eyebrow">Free tool</p><h1 style="margin-top:8px">Free Digital Invitation Card Maker</h1>
  <p class="lead">16 free templates for weddings, birthdays, Griha Pravesh, Godh Bharai, Naamkaran, Mundan, puja, Diwali, Holi and more. Add your details and download as PNG, JPG or PDF, or share on WhatsApp. Free, no sign-up.</p></div></section>
<section class="sec" style="padding-top:32px"><div class="wrap">
  <h2 style="font-size:26px;margin-bottom:14px">1. Choose a template <small class="muted" style="font:500 15px var(--sans)">(16 free designs)</small></h2>
  <div class="chips tpl-cats" id="tpl-cats" role="group" aria-label="Filter templates">
    <button class="chip" data-cat="all" aria-pressed="true">All</button><button class="chip" data-cat="wedding" aria-pressed="false">Wedding &amp; Sagai</button>
    <button class="chip" data-cat="birthday" aria-pressed="false">Birthday</button><button class="chip" data-cat="baby" aria-pressed="false">Baby</button>
    <button class="chip" data-cat="festival" aria-pressed="false">Puja &amp; Festivals</button><button class="chip" data-cat="other" aria-pressed="false">Other</button></div>
  <div class="tpl-grid" id="tpl-grid"></div>
  <div class="maker" id="maker">
    <div class="panel"><h2 style="font-size:26px;margin-bottom:14px">2. Add your details</h2>
      <form class="form" id="mk-form" novalidate>
        <div class="field"><label for="mk-top">Top line</label><input id="mk-top" name="top" maxlength="60"></div>
        <div class="field"><label for="mk-title">Main title</label><input id="mk-title" name="title" maxlength="40"></div>
        <div class="field"><label for="mk-sub">Message</label><textarea id="mk-sub" name="sub" maxlength="140" style="min-height:70px"></textarea></div>
        <div class="f2"><div class="field"><label for="mk-date">Date</label><input id="mk-date" name="date" type="date"></div><div class="field"><label for="mk-time">Time</label><input id="mk-time" name="time" type="time"></div></div>
        <div class="field"><label for="mk-venue">Venue</label><input id="mk-venue" name="venue" maxlength="80"></div>
        <div class="field"><label for="mk-host">Hosted by / RSVP</label><input id="mk-host" name="host" maxlength="70"></div>
      </form></div>
    <aside class="maker-preview"><p class="eyebrow center" style="margin-bottom:12px">3. Preview, download &amp; share</p>
      <div class="mk-card inv-wrap" id="mk-card"></div>
      <div class="mk-actions">
        <div class="dl-panel">
          <p class="label">Size</p>
          <div class="seg" id="mk-size" role="group" aria-label="Size"><button type="button" data-size="card" aria-pressed="true">Card<small>2:3 print</small></button><button type="button" data-size="status" aria-pressed="false">Status<small>WhatsApp / Insta</small></button><button type="button" data-size="square" aria-pressed="false">Square<small>Post</small></button></div>
          <label class="check"><input type="checkbox" id="mk-blank"> Blank template (no text, write by hand or in any app)</label>
          <p class="label">Download as</p>
          <div class="fmt"><button class="btn btn-primary" type="button" data-fmt="png">PNG</button><button class="btn btn-outline" type="button" data-fmt="jpg">JPG</button><button class="btn btn-outline" type="button" data-fmt="pdf">PDF</button></div>
        </div>
        <button class="btn btn-wa" id="mk-share" type="button">{WA} Share on WhatsApp</button>
        <p class="center muted" style="font-size:13px">Planning a wedding? <a href="demo.html">See a full invitation website</a>.</p></div></aside>
  </div>
</div></section>
<section class="sec sec-tint"><div class="wrap">
  <div class="sec-head center"><h2>Cards for Every Family Occasion</h2>{ORN}</div>
  <div class="occasions">
    <div><h3>Birthday invitations</h3><p>Cheerful cards for kids' parties and elegant gold cards for 30th, 50th or 60th birthdays.</p></div>
    <div><h3>Anniversary invitations</h3><p>Celebrate 25 or 50 years with roses, rings and your family's blessings.</p></div>
    <div><h3>Griha Pravesh invitations</h3><p>Auspicious kalash, toran and rangoli designs for your new home's puja.</p></div>
    <div><h3>Godh Bharai &amp; baby shower</h3><p>Soft jhoola and floral designs to welcome the little one.</p></div>
    <div><h3>Sagai &amp; ring ceremony</h3><p>Rich teal and gold for the engagement; upgrade to a full wedding website later.</p></div>
    <div><h3>Puja, jagran &amp; Diwali</h3><p>Diyas, bells and rangoli for satsang, bhajan sandhya and festival get-togethers.</p></div>
    <div><h3>Naamkaran &amp; Mundan</h3><p>Cradle and puja-thali designs for your little one's naming and first-haircut ceremonies.</p></div>
    <div><h3>Holi, Teej &amp; Gangaur</h3><p>Colourful gulal and leheriya designs for festival parties and kitty get-togethers.</p></div>
    <div><h3>Save the date &amp; wedding</h3><p>Announce the date early, then upgrade to a full Bfiluxe invitation website.</p></div>
    <div><h3>Retirement &amp; prayer meet</h3><p>Dignified designs to honour a career, or to remember a loved one.</p></div>
  </div>
</div></section>
<section class="sec"><div class="wrap split" style="align-items:start">
  <div><h2>Questions</h2><p class="lead" style="margin-top:12px">Want something more? We make full invitation websites for weddings and big family functions.</p>
    <div class="row" style="margin-top:18px"><a class="btn btn-primary" href="invitations.html">Wedding invitations</a><a class="btn btn-wa" data-wa>{WA} Ask on WhatsApp</a></div></div>
  <div>{faq_html(FREE_FAQ)}</div>
</div></section>'''
page("free-cards", "Free Invitation Card Maker: 16 Templates, PNG, JPG & PDF | Bfiluxe",
     "Free digital invitation cards for weddings, birthdays, Griha Pravesh, Godh Bharai, Naamkaran, Mundan, puja, Diwali, Holi and more. Download PNG, JPG or PDF, or share on WhatsApp.",
     FREE_PAGE, "free-cards", ld=[faq_ld(FREE_FAQ), {"@context": "https://schema.org", "@type": "WebApplication", "name": "Bfiluxe Free Digital Invitation Card Maker",
     "url": BASE + "/free-cards.html", "applicationCategory": "DesignApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": 0, "priceCurrency": "INR"},
     "provider": {"@id": BASE + "/#business"}}])


# ---------------- Features, resources, partners, landing pages & articles ----------------
def section_html(sections):
    out = []
    for h, body in sections:
        out.append(f'<h2>{h}</h2>{body}')
    return "".join(out)


def content_page(slug, title, desc, h1, lead, sections, faqs, related, extra_ld=None, cta=None, eyebrow=""):
    body = f"""
<section class="phead"><div class="wrap">{f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ''}<h1>{h1}</h1><p class="lead">{lead}</p></div></section>
<article class="sec guide"><div class="wrap narrow prose">
  {section_html(sections)}
  {cta or f'<div class="panel panel-gold center" style="margin-top:40px"><h2 style="font-size:28px;margin:0">Ready to create yours?</h2><p class="lead" style="margin:10px auto 18px">See a live demo, then tell us your names and functions.</p><div class="row" style="justify-content:center"><a class="btn btn-primary" href="invitations.html">See designs</a><a class="btn btn-ghost" href="demo.html">Open live demo</a><a class="btn btn-wa" data-wa>{WA} WhatsApp</a></div></div>'}
  {('<h2 id="faq">Questions</h2>' + faq_html(faqs)) if faqs else ''}
  <div class="related"><p class="eyebrow">Keep reading</p><div class="rel-links">{"".join(f'<a href="{u}">{t} →</a>' for t, u in related)}</div></div>
</div></article>"""
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc, "author": {"@id": BASE + "/#business"},
           "publisher": {"@id": BASE + "/#business"}, "dateModified": TODAY, "inLanguage": "en-IN", "mainEntityOfPage": f"{BASE}/{slug}.html"}]
    if faqs:
        ld.append(faq_ld(faqs))
    page(slug, title, desc, body, None, ld=ld + (extra_ld or []))


P_ = lambda *xs: "".join(f"<p>{x}</p>" for x in xs)
UL = lambda *xs: "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"
OL = lambda *xs: "<ol>" + "".join(f"<li>{x}</li>" for x in xs) + "</ol>"

# ---- Features (what each feature means for a non-technical family) ----
FEATURES = [
    ("link", "Your own invitation website", "One private link that opens like an app on any phone, with no download needed.", "Guests tap the link on WhatsApp and the invitation opens instantly.", "BPL"),
    ("rsvp", "Every function, in order", "Ganesh Sthapana to Reception: each function gets its own date, time, venue and notes.", "Guests see exactly which functions they're invited to and when.", "BPL"),
    ("lotus", "Marwari traditions, done right", "Opening blessings, both families, grandparents and elders, listed the way your family wants.", "Elders see their names written correctly and respectfully.", "BPL"),
    ("globe", "Hindi, English or both", "Write in English, Hindi, Marwari with Hindi, or bilingual.", "Elders read in Hindi; friends and NRI guests read in English.", "BPL"),
    ("pin", "Maps and directions", "A Google Maps link for every venue.", "One tap opens directions; no more “bhai, location bhejo” calls.", "BPL"),
    ("qr", "QR code", "A QR code that opens your invitation.", "Print it on physical kankotri cards or show it at the venue.", "BPL"),
    ("share", "WhatsApp sharing", "A ready-to-forward WhatsApp message with your link.", "Send it to family groups in seconds.", "BPL"),
    ("refresh", "Update without re-sending", "Change a time or venue and the same link shows the update.", "Guests always see the latest details.", "BPL"),
    ("music", "Background music or shehnai", "Shehnai, soft instrumental, or a song you choose.", "The invitation opens with music, like a celebration should.", "PL"),
    ("image", "Photo gallery", "Pre-wedding photos or family pictures in a gallery.", "Relatives get a glimpse of the couple before the big day.", "PL"),
    ("clock", "Countdown", "A live countdown to the wedding.", "Builds excitement every time guests open the link.", "PL"),
    ("users", "RSVP and guest count", "Guests confirm attendance and how many are coming.", "You get numbers for catering and rooms without dozens of calls.", "PL"),
    ("book", "Family story or video page", "A page for your story, family history or a video.", "Guests feel part of your journey, not just your guest list.", "L"),
    ("sliders", "Custom colours and motifs", "Colours matched to your theme; motifs like your family deity or city.", "An invitation that feels made only for your family.", "L"),
]
feat_rows = "".join(
    f'<div class="feat-card"><span class="fi">{icon(I[ic])}</span><h3>{t}</h3><p>{what}</p><p class="guest"><b>For guests:</b> {guest}</p>'
    f'<div class="avail">{"".join(f"<span class={chr(34)}on{chr(34) if k in av else chr(34)+chr(34)}>{n}</span>" for k, n in (("B", "Basic"), ("P", "Premium"), ("L", "Luxury")))}</div></div>'
    for ic, t, what, guest, av in FEATURES)
FEAT_BODY = f"""
<section class="phead"><div class="wrap"><p class="eyebrow">What you get</p><h1>Everything Your Invitation Can Do</h1><p class="lead">Every feature explained simply, with the packages it comes in. Open the <a href="demo.html">live demo</a> to try them on your phone.</p></div></section>
<section class="sec" style="padding-top:36px"><div class="wrap">
  <div class="avail-key"><span class="on">Basic</span><span class="on">Premium</span><span class="on">Luxury</span> = included in that package</div>
  <div class="feat-grid">{feat_rows}</div>
  <div class="panel panel-gold center" style="margin-top:40px"><h2 style="font-size:30px">See it working</h2><p class="lead" style="margin:10px auto 18px">Every feature above is in our live demos. Open one on your phone.</p>
    <div class="row" style="justify-content:center"><a class="btn btn-primary" href="demo.html">Open the live demo</a><a class="btn btn-ghost" href="pricing.html">Compare packages</a></div></div>
</div></section>"""
page("features", "Features: Maps, RSVP, Music, Hindi, QR & WhatsApp | Bfiluxe Digital Wedding Invitations",
     "What a Bfiluxe digital wedding invitation can do: every function in order, Hindi or bilingual text, maps, QR code, WhatsApp sharing, music, gallery, countdown, RSVP and family story.",
     FEAT_BODY, "features", ld=[{"@context": "https://schema.org", "@type": "ItemList", "name": "Bfiluxe invitation features", "itemListElement": [{"@type": "ListItem", "position": k + 1, "name": f[1]} for k, f in enumerate(FEATURES)]}])

# ---- Partners ----
PART_BODY = f"""
<section class="phead"><div class="wrap"><p class="eyebrow">For wedding professionals</p><h1>Partner With Bfiluxe</h1><p class="lead">Wedding planners, photographers, venues and decorators: recommend Bfiluxe invitations to your clients and earn a referral commission on every confirmed order.</p></div></section>
<section class="sec" style="padding-top:36px"><div class="wrap">
  <div class="next3">
    <div><span>1</span><h3>Apply below</h3><p>Tell us about your business. We'll call you to say hello.</p></div>
    <div><span>2</span><h3>Get your referral code</h3><p>Share it with couples and families you work with.</p></div>
    <div><span>3</span><h3>Earn on confirmed orders</h3><p>15% on Basic and Premium, 20% on Luxury orders that use your code.</p></div>
  </div>
  <div class="split" style="margin-top:44px;align-items:start">
    <div><h2>Why partners recommend us</h2><ul class="checks" style="margin-top:14px">
      <li>{icon(I["check"])}Invitations made only for Marwari and Rajasthani weddings</li>
      <li>{icon(I["check"])}Every function, with maps, so guests reach your venue on time</li>
      <li>{icon(I["check"])}Ready from 3 working days, so it never delays your planning</li>
      <li>{icon(I["check"])}Clients pay 50% after approving, which keeps the experience stress-free</li></ul>
      <p class="muted" style="margin-top:14px;font-size:14px">Commission is paid after the client completes payment. Full terms are shared when you join.</p></div>
    <div class="panel panel-gold"><h2 style="font-size:28px;margin-bottom:6px">Apply to partner</h2><p class="muted" style="margin-bottom:16px">We reply on WhatsApp.</p>
      <div id="p-status"></div>
      <form class="form" id="partner-form" novalidate>
        <div class="f2"><div class="field"><label for="pa-name">Your name <span class="req">*</span></label><input id="pa-name" name="name" required autocomplete="name"></div>
        <div class="field"><label for="pa-biz">Business name <span class="req">*</span></label><input id="pa-biz" name="business" required autocomplete="organization"></div></div>
        <div class="f2"><div class="field"><label for="pa-type">You are a</label><select id="pa-type" name="type"><option>Wedding planner</option><option>Photographer / videographer</option><option>Venue / hotel</option><option>Decorator</option><option>Other</option></select></div>
        <div class="field"><label for="pa-city">City</label><input id="pa-city" name="city" autocomplete="address-level2"></div></div>
        <div class="f2"><div class="field"><label for="pa-phone">WhatsApp number <span class="req">*</span></label><input id="pa-phone" name="phone" type="tel" required inputmode="tel" autocomplete="tel"></div>
        <div class="field"><label for="pa-email">Email</label><input id="pa-email" name="email" type="email" autocomplete="email"></div></div>
        <div class="field"><label for="pa-msg">Anything to add?</label><textarea id="pa-msg" name="message" placeholder="Website or Instagram, number of weddings a year…"></textarea></div>
        <input type="text" name="company" tabindex="-1" autocomplete="off" class="sr" aria-hidden="true">
        <button class="btn btn-primary btn-block" type="submit">Send application</button></form></div>
  </div>
</div></section>"""
page("partners", "Partner With Bfiluxe: Referral Programme for Wedding Planners, Photographers & Venues",
     "Wedding planners, photographers, venues and decorators can recommend Bfiluxe digital wedding invitations and earn 15–20% referral commission on confirmed orders.", PART_BODY, None)

# ---- Landing pages (distinct intent each) ----
LANDING = {
    "marwari-wedding-invitation-website": dict(design="sheesh-mahal", eyebrow="Marwari wedding invitation website",
        title="Marwari Wedding Invitation Website: Every Ritual, One Link | Bfiluxe",
        desc="What a Marwari wedding invitation website includes, how it is different from a card or video, and how to get one made with every function, elder and venue.",
        h1="A Wedding Invitation Website Made for Marwari Weddings",
        lead="One private link that holds your whole wedding: blessings, both families, every function from Ganesh Sthapana to Reception, maps, music and RSVP.",
        sections=[("What is a wedding invitation website?", P_("It is a small, private website made only for your wedding. Guests open it from a WhatsApp link or a QR code, and it works like an app on their phone without installing anything.", "Unlike a picture card, it can hold as many functions as your family celebrates, and it can be updated if a time or venue changes.")),
                  ("What a Marwari invitation website usually contains", OL("<b>Cover</b> with the opening blessing (॥ श्री गणेशाय नमः ॥) and the couple's names", "<b>Blessings</b> from grandparents and elders", "<b>Both families</b>: the bride's and groom's parents, written the way your family prefers", "<b>Functions</b>: Ganesh Sthapana, Mayra, Pithi, Mehendi, Mahila Sangeet, Baraat, Phere, Reception, each with date, time, venue and dress code", "<b>Venue</b> directions with Google Maps", "<b>RSVP</b> so guests confirm attendance and numbers (Premium and Luxury)", "<b>Gallery, countdown and music</b> (Premium and Luxury)")),
                  ("Why families choose a website over a PDF or video", UL("A PDF is hard to read on a phone and cannot be updated.", "A video plays once, and guests cannot tap to get directions.", "A website keeps every function, map and RSVP in one place and stays live after the wedding.")),
                  ("How to get one made", P_('Choose a design from the <a href="invitations.html">collection</a>, share your names and functions through our <a href="customize.html">form</a> or on WhatsApp, review the preview on your phone, then share the link. It takes 3–21 working days depending on the package.'))],
        faqs=[("Do guests need to install an app?", "No. The invitation opens in the phone's browser from a link or QR code."),
              ("Can I keep some functions for family only?", "Yes. Tell us which functions are for close family and we will mark them or keep them on a separate page."),
              ("How much does it cost?", f"From {pk('p', 'Basic')} (Basic) to {pk('p', 'Luxury')} (Luxury). See <a href='pricing.html'>pricing</a>.")]),
    "marwari-kankotri-online": dict(design="gulmohar-classic", eyebrow="Online kankotri",
        title="Marwari Kankotri Online: Digital Kankotri with Traditional Wording | Bfiluxe",
        desc="What a Marwari kankotri is, the traditions around sending it, and how to make an online kankotri that keeps the blessings, family order and wording intact.",
        h1="Marwari Kankotri, Now Online",
        lead="The kankotri is the first and most respected part of a Marwari wedding. An online kankotri keeps its traditions, and adds maps, RSVP and instant sharing.",
        sections=[("What is a kankotri?", P_("A kankotri (कंकोत्री) is the traditional Marwari wedding invitation. It traditionally opens with an invocation to Lord Ganesha, carries the names of the couple, both families and elders, and lists each function in order.", "In many families the first kankotri is offered to Ganesh ji or the family deity before any guest receives one.")),
                  ("Traditions to keep when going digital", UL("Keep the opening blessing: ॥ श्री गणेशाय नमः ॥ or your family's own.", "List elders and both families in the order your family follows.", "Use respectful honorifics, such as Shri, Shrimati, Chi. and Sau. Ka.", "Many families still hand-deliver a printed kankotri to the closest elders, and share the online version with everyone else.")),
                  ("Printed kankotri and online kankotri together", P_('A popular approach is to print a smaller number of cards with a QR code that opens the online kankotri. Elders receive the card by hand; everyone gets every function and map on their phone. Read more in <a href="digital-vs-printed-kankotri.html">digital vs printed kankotri</a>.')),
                  ("Sample kankotri wording", '<p lang="hi" class="hi-block">॥ श्री गणेशाय नमः ॥<br>सादर आमंत्रण<br>श्रीमती सुनीता एवं श्री महेश अग्रवाल की सुपुत्री<br><b>सौ. कां. प्रिया</b><br>संग<br><b>चि. रोहन</b><br>के शुभ विवाह पर आप सपरिवार सादर आमंत्रित हैं।</p><p>More wording in our <a href="guide.html#wording">wording guide</a>.</p>')],
        faqs=[("Is an online kankotri respectful enough for elders?", "Many families do both: a printed card for elders, and the online kankotri for everyone. The online version carries the same blessings and wording."),
              ("Can the kankotri be fully in Hindi?", "Yes. The whole invitation can be in Hindi, or bilingual."),
              ("Can it include Mayra and Pithi?", "Yes, each as its own function with date, time and venue.")]),
    "hindi-wedding-invitation": dict(design="gajraj-swagat", eyebrow="Hindi wedding invitation",
        title="Hindi Wedding Invitation Online: Wording, Honorifics & Bilingual Options | Bfiluxe",
        desc="How to write a Hindi wedding invitation: common lines, honorifics like Chi. and Sau. Ka., bilingual options and a ready sample, made as a digital invitation.",
        h1="Hindi Wedding Invitations, Written Properly",
        lead="Hindi wording carries the warmth and respect that elders expect. Here's how families usually write it, and how we set it beautifully on a digital invitation.",
        sections=[("Common lines in a Hindi invitation", UL("<b>॥ श्री गणेशाय नमः ॥</b>: the opening invocation", "<b>सादर आमंत्रण</b>: “a respectful invitation”", "<b>शुभ विवाह</b>: the auspicious wedding", "<b>स्वागतोत्सुक</b>: family members eager to welcome you, often listed at the end", "<b>दर्शनाभिलाषी</b>: those who look forward to your presence, often children of the family")),
                  ("Honorifics", UL("<b>चि.</b> (Chiranjeevi) before the groom's name", "<b>सौ. कां.</b> (Saubhagyakankshini) before the bride's name", "<b>श्रीमती / श्री</b> for parents and elders; <b>स्व.</b> for late family members")),
                  ("Hindi, English or bilingual?", P_("Many families choose bilingual: Hindi for the blessing, elders and families, and English for function details so younger and NRI guests can read easily. We set Devanagari in a proper Hindi typeface so it looks as good as the English.")),
                  ("Sample", '<p lang="hi" class="hi-block">॥ श्री गणेशाय नमः ॥<br>श्रीमती रेखा एवं श्री अनिल माहेश्वरी के सुपुत्र<br><b>चि. रोहन</b><br>संग<br><b>सौ. कां. प्रिया</b><br>(सुपुत्री श्रीमती सुनीता एवं श्री महेश अग्रवाल)<br>के शुभ विवाह के पावन अवसर पर आप सादर आमंत्रित हैं।</p>')],
        faqs=[("Can you write the Hindi wording for us?", "Yes. Share names and functions, and we prepare the wording for you to check."),
              ("Can I mix Hindi and English?", "Yes. Bilingual invitations are one of our most requested options."),
              ("Will Hindi display correctly on all phones?", "Yes. We use a web font for Devanagari so it displays the same on Android and iPhone.")]),
    "wedding-invitation-website-rsvp": dict(design="neel-mahal", eyebrow="Wedding website with RSVP",
        title="Wedding Invitation Website with RSVP: Guest Count Without the Phone Calls | Bfiluxe",
        desc="How RSVP works on a wedding invitation website: what guests are asked, how you see responses, and how it helps with catering, rooms and transport.",
        h1="A Wedding Invitation Website with RSVP",
        lead="Know who's coming, and how many, without calling every relative. RSVP is built into our Premium and Luxury invitations.",
        sections=[("How RSVP works", OL("Guests open your invitation and tap <b>RSVP</b>.", "They enter their name, whether they're attending and the number of guests.", "Optionally, they choose a meal preference.", "You receive the responses and can share totals with your caterer, hotel and transport team.")),
                  ("Why it helps Indian weddings", UL("Large guest lists across many functions are hard to track by phone.", "Caterers and hotels need numbers days in advance.", "Outstation and NRI guests can reply in one tap from anywhere.")),
                  ("Set a deadline", P_("Most families ask for RSVPs one to two weeks before the wedding. Send a reminder on WhatsApp with the same link a few days before the deadline."))],
        faqs=[("Which packages include RSVP?", "Premium and Luxury. Basic invitations include a contact number instead."),
              ("Can guests change their RSVP?", "Yes, they can send it again with updated details."),
              ("Is guest information private?", "Yes. Responses are only for you and the Bfiluxe team; we never share them.")]),
    "rajasthani-digital-wedding-invitation": dict(design="mor-pankh", eyebrow="Rajasthani digital invitation",
        title="Rajasthani Digital Wedding Invitation: Royal Designs from Jaipur to Jodhpur | Bfiluxe",
        desc="Rajasthani design elements for a digital wedding invitation: jharokhas, havelis, elephants, peacocks and leheriya, and how they suit weddings across Rajasthan.",
        h1="Rajasthani Digital Wedding Invitations",
        lead="Jharokhas, haveli arches, royal elephants, peacocks and leheriya colours: the art of Rajasthan, made for the phones your guests carry.",
        sections=[("Rajasthani motifs and what they mean", UL("<b>Jharokha</b>: the carved window, a frame for the couple's names", "<b>Gaj (elephant)</b>: auspicious, a symbol of welcome and prosperity", "<b>Mor (peacock)</b>: grace and love", "<b>Leheriya and bandhej</b>: the colours of Teej, Gangaur and celebration", "<b>Haveli and fort skylines</b>: the grandeur of Rajput and Marwari heritage")),
                  ("Designs in our collection", P_('<a href="design-rajwada-royale.html">Rajwada Royale</a> and <a href="design-sheesh-mahal.html">Sheesh Mahal</a> bring palace grandeur; <a href="design-gajraj-swagat.html">Gajraj Swagat</a> welcomes guests with elephants; <a href="design-mor-pankh.html">Mor Pankh</a> uses the peacock; <a href="design-chhatri.html">Chhatri</a> is a minimal take on the Rajasthani pavilion.')),
                  ("Matching your city", P_("Jaipur weddings often lean pink and gold; Jodhpur's blue city suits navy and indigo, as in <a href='design-neel-mahal.html'>Neel Mahal</a>; Udaipur's lakes suit soft pastels; Shekhawati families often love fresco-inspired detail. We can tune colours on Premium and Luxury."))],
        faqs=[("Can you include our family deity or kuldevi?", "Yes, on Luxury we can add custom motifs such as your family deity or temple."),
              ("Do you only work with families in Rajasthan?", "No. We work on WhatsApp with Marwari and Rajasthani families across India and abroad."),
              ("Can I see the designs live?", "Yes, every design has a <a href='demo.html'>live demo</a>.")]),
}
for slug, L in LANDING.items():
    content_page(slug, L["title"], L["desc"], L["h1"], L["lead"], L["sections"], L["faqs"],
                 [("All invitation designs", "invitations.html"), ("Pricing", "pricing.html"), ("Marwari wedding guide", "guide.html"), ("Frequently asked questions", "faq.html")], eyebrow=L["eyebrow"])

# ---- Articles ----
content_page("digital-vs-printed-kankotri", "Digital vs Printed Kankotri: Which Should Marwari Families Choose? | Bfiluxe",
    "An honest comparison of digital and printed Marwari kankotri: cost, time, elders, NRI guests, updates and the hybrid approach most families now use.",
    "Digital vs Printed Kankotri", "Most families no longer choose one or the other. Here's an honest look at both, and how to combine them.",
    [("At a glance", '<div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col"></th><th scope="col">Printed kankotri</th><th scope="col" class="hl">Digital kankotri</th></tr></thead><tbody>'
      '<tr><th scope="row">Feels traditional</th><td>✓ Strongest</td><td class="hl">✓ With blessings and Hindi wording</td></tr>'
      '<tr><th scope="row">Reaching outstation &amp; NRI guests</th><td>Courier, slow</td><td class="hl">Instant on WhatsApp</td></tr>'
      '<tr><th scope="row">Changing a time or venue</th><td>Reprint</td><td class="hl">Update; same link</td></tr>'
      '<tr><th scope="row">Directions</th><td>Address only</td><td class="hl">One-tap Google Maps</td></tr>'
      '<tr><th scope="row">Guest count</th><td>Phone calls</td><td class="hl">RSVP (Premium &amp; Luxury)</td></tr>'
      '<tr><th scope="row">Lead time</th><td>Design, printing and delivery</td><td class="hl">3–21 working days</td></tr></tbody></table></div>'),
     ("When printed still matters", P_("For grandparents, the family guru and the closest elders, a hand-delivered card carries respect that a message cannot. Many families also keep a printed kankotri as a keepsake.")),
     ("The hybrid approach", OL("Print a small number of cards for elders and close family.", "Add the Bfiluxe QR code on the printed card so every function and map is one scan away.", "Share the digital invitation with everyone else on WhatsApp.", "Send a reminder with the same link a week before the wedding.")),
     ("What to put on each", P_("Keep the printed card short: blessing, names, families and the main wedding date. Put the full list of functions, timings, venues, dress codes and RSVP on the digital invitation, where it can be updated."))],
    [("Is a digital kankotri cheaper than printing?", "For large guest lists and outstation guests it usually is, because there is no printing or courier. Many families still print a few cards for elders."),
     ("Can I add a QR code to my printed card?", "Yes, every Bfiluxe package includes a QR code you can print on your cards.")],
    [("Online Marwari kankotri", "marwari-kankotri-online.html"), ("Inviting guests to Mayra, Pithi and Phere", "inviting-guests-mayra-pithi-phere.html"), ("Marwari wedding guide", "guide.html")], eyebrow="Article")

content_page("inviting-guests-mayra-pithi-phere", "How to Invite Guests to Mayra, Pithi and Phere | Bfiluxe Marwari Wedding Guide",
    "Who is usually invited to Mayra, Pithi, Mahila Sangeet and Phere, how to show family-only functions on the invitation, and wording that keeps everyone comfortable.",
    "How to Invite Guests to Mayra, Pithi and Phere", "Not every guest is invited to every function. Here's how Marwari families usually decide, and how to show it clearly on one invitation.",
    [("Who usually attends which function", '<div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col">Function</th><th scope="col">Usually for</th></tr></thead><tbody>'
      '<tr><th scope="row">Ganesh Sthapana</th><td>Close family</td></tr><tr><th scope="row">Mayra (Bhaat)</th><td>Family, and the maternal side who bring the mayra</td></tr>'
      '<tr><th scope="row">Pithi / Haldi</th><td>Family and close relatives, often women of the family</td></tr><tr><th scope="row">Mehendi &amp; Mahila Sangeet</th><td>Women of the family and friends; many families now invite everyone</td></tr>'
      '<tr><th scope="row">Baraat &amp; Phere</th><td>All invited guests</td></tr><tr><th scope="row">Reception</th><td>All invited guests, colleagues and friends</td></tr></tbody></table></div>'
      '<p class="muted">Customs differ by family and region; always follow your elders.</p>'),
     ("Showing family-only functions on one invitation", UL("Mark close-family functions with a small note such as “Family only”.", "Or create a separate family page, shared only with relatives.", "Keep the public invitation to the functions everyone attends.")),
     ("Wording that works", P_("For family functions: <i>“With the blessings of our elders, we invite our family to the Mayra ceremony.”</i>", "For everyone: <i>“Your presence at the Phere and Reception will make our joy complete.”</i>")),
     ("Timing", P_("Share the invitation 4–8 weeks before the wedding. Send the family page when the Mayra and Pithi dates are fixed, and a reminder to everyone a week before."))],
    [("Can one invitation have different functions for different guests?", "Yes. We can mark family-only functions or make a separate family page."),
     ("Should the Mayra be on the invitation?", "Many families list it, especially for relatives who travel. Some keep it for the family page only.")],
    [("Marwari wedding rituals in order", "guide.html#rituals"), ("Digital vs printed kankotri", "digital-vs-printed-kankotri.html"), ("Hindi wedding invitation wording", "hindi-wedding-invitation.html")], eyebrow="Article")

# ---- Resources hub ----
RES = [("guide.html", "Marwari Wedding Guide", "Rituals in order, Hindi and English wording, and a send-out checklist."),
       ("digital-vs-printed-kankotri.html", "Digital vs Printed Kankotri", "An honest comparison, and the hybrid approach most families use."),
       ("inviting-guests-mayra-pithi-phere.html", "Inviting Guests to Mayra, Pithi & Phere", "Who attends which function, and how to show it."),
       ("hindi-wedding-invitation.html", "Hindi Wedding Invitations", "Common lines, honorifics and a ready sample."),
       ("marwari-kankotri-online.html", "Marwari Kankotri Online", "Traditions to keep when your kankotri goes digital."),
       ("marwari-wedding-invitation-website.html", "Marwari Invitation Websites", "What one contains, and why families choose it."),
       ("wedding-invitation-website-rsvp.html", "Invitations with RSVP", "How RSVP works and why it saves phone calls."),
       ("rajasthani-digital-wedding-invitation.html", "Rajasthani Designs", "Jharokhas, elephants, peacocks and city colours."),
       ("faq.html", "Frequently Asked Questions", "Delivery, payment, revisions and features."),
       ("free-cards.html", "Free Card Maker", "16 free templates for every family occasion.")]
RES_BODY = f"""
<section class="phead"><div class="wrap"><p class="eyebrow">Learn</p><h1>Wedding Invitation Resources</h1><p class="lead">Free guides for Marwari and Rajasthani families: rituals, wording, etiquette and everything about digital invitations.</p></div></section>
<section class="sec" style="padding-top:36px"><div class="wrap"><div class="res-grid">{"".join(f'<a class="res-card" href="{u}"><span class="res-n">{k + 1:02d}</span><h3>{t}</h3><p>{d}</p><span class="res-go">Read →</span></a>' for k, (u, t, d) in enumerate(RES))}</div></div></section>"""
page("resources", "Marwari Wedding Invitation Guides & Resources | Bfiluxe", "Free guides on Marwari wedding rituals, kankotri wording in Hindi and English, digital vs printed invitations, RSVP and Rajasthani design.", RES_BODY, None,
     ld=[{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Bfiluxe resources", "url": BASE + "/resources.html", "hasPart": [{"@type": "Article", "name": t, "url": f"{BASE}/{u}"} for u, t, d in RES]}])

LIVE_LLMS = ", ".join(f"[{t}]({BASE}/live-demo-{n}/) ({m})" for n, t, c, m, d in LIVE)
# ---------------- robots, sitemap, llms.txt, vCard ----------------
PUBLIC = ["", "invitations.html", "pricing.html", "how-it-works.html", "demo.html", "features.html", "live-demo-1/", "live-demo-2/", "live-demo-3/", "live-demo-4/", "live-demo-5/", "guide.html", "resources.html", "digital-vs-printed-kankotri.html", "inviting-guests-mayra-pithi-phere.html", "marwari-wedding-invitation-website.html", "marwari-kankotri-online.html", "hindi-wedding-invitation.html", "wedding-invitation-website-rsvp.html", "rajasthani-digital-wedding-invitation.html", "partners.html", "videos.html", "free-cards.html", "faq.html", "contact.html", "customize.html",
          "privacy.html", "terms.html"] + [f"design-{i['slug']}.html" for i in CATALOG]
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /account.html\nDisallow: /login.html\nDisallow: /admin/\n\nSitemap: {BASE}/sitemap.xml\n")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{BASE}/{p}</loc><lastmod>{TODAY}</lastmod></url>\n" for p in PUBLIC) + "</urlset>\n")
(OUT / "llms.txt").write_text(f"""# Bfiluxe

> Studio in {BIZ['city']}, {BIZ['region']}, India that designs premium digital wedding invitations only for Marwari families. Each invitation is a mobile website with the couple's and families' names, every function (Ganesh puja, Mayra, Pithi/Haldi, Mehendi, Mahila Sangeet, Baraat, Phere, Reception) with date, time and Google Maps, music, photo gallery, RSVP and a QR code, shared on WhatsApp.

## Key facts
- Packages: Basic ₹3,999 (regular ₹5,999, ready in 3–5 working days), Premium ₹8,999 (regular ₹14,999, 7–14 working days), Luxury ₹24,999 (regular ₹35,999, 15–21 working days).
- Payment: 50% to start, 50% after the customer approves the invitation. UPI or bank transfer.
- Languages: English, Hindi, Marwari + Hindi, bilingual.
- One free round of changes; spelling fixes always free. Links stay live at least 6 months after the wedding.
- Contact: WhatsApp/phone {BIZ['phone']}, email {BIZ['email']}, {BIZ['hours']}.

## Pages
- [Invitation designs]({BASE}/invitations.html): Royal, Traditional, Elegant and Modern collections
- [Pricing]({BASE}/pricing.html): packages and feature comparison
- [Invitation videos]({BASE}/videos.html): animated video invites for WhatsApp, Basic ₹1,499 (30 s), Premium ₹2,499 (60 s), Luxury ₹3,999 (90 s), each ready in 2–3 working days
- [How it works]({BASE}/how-it-works.html): choose, share details, preview and approve, share
- [Live demo]({BASE}/demo.html): a sample invitation as guests see it
- [Marwari wedding guide]({BASE}/guide.html): rituals in order, invitation wording in Hindi and English, send-out checklist
- [Features]({BASE}/features.html): every feature in plain language, with the packages it comes in
- [Guides & resources]({BASE}/resources.html): kankotri wording, Hindi honorifics, digital vs printed kankotri, inviting guests to Mayra/Pithi/Phere, RSVP
- [Partner programme]({BASE}/partners.html): planners, photographers and venues earn 15% (Basic/Premium) or 20% (Luxury) on confirmed referred orders
- Five sample invitation websites (fictional couples): {LIVE_LLMS}
- [FAQ]({BASE}/faq.html): kankotri, Mayra and Pithi, Hindi wording, RSVP, WhatsApp sharing, delivery, link validity, payment and revisions
- [Free card maker]({BASE}/free-cards.html): 16 free templates (wedding, save the date, Sagai, anniversary, birthdays, Godh Bharai, Naamkaran, Mundan, Griha Pravesh, puja, Diwali, Holi, Teej/Gangaur, retirement, prayer meet); download PNG, JPG or PDF
- [Contact]({BASE}/contact.html)
""" + "".join(f"- [{i['name']}]({BASE}/design-{i['slug']}.html): {COLL[i['collection']]} collection, from ₹{i['price']:,}\n" for i in CATALOG))
(OUT / "bfi-contact.vcf").write_text(f"""BEGIN:VCARD\r\nVERSION:3.0\r\nFN:Bfiluxe\r\nORG:Bfiluxe\r\nTITLE:Digital wedding invitations\r\nTEL;TYPE=CELL,VOICE:{BIZ['tel']}\r\nEMAIL;TYPE=INTERNET:{BIZ['email']}\r\nURL:{BASE}/\r\nADR;TYPE=WORK:;;;{BIZ['city']};{BIZ['region']};;India\r\nNOTE:WhatsApp us for wedding invitations. {BIZ['hours']}.\r\nEND:VCARD\r\n""")

print("built", sorted(p.name for p in OUT.glob("*.html")))
