"""Generates the website mockup pages in design/website/.

Each page shares the same <head>, header and footer (injected by
assets/mock.js). Run:  python3 design/build_site.py
"""
from pathlib import Path

OUT = Path(__file__).parent / "website"
FONTS = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Inter:wght@400;500;600&family=Tiro+Devanagari+Hindi&display=swap"


def page(slug, title, desc, nav, body):
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="../assets/og-image.png">
<link rel="icon" href="../assets/favicon-64.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="../assets/bfi.css">
</head>
<body>
<div data-header="{nav}"></div>
{body}
<div data-footer></div>
<script src="../assets/mock.js"></script>
</body>
</html>
"""
    (OUT / f"{slug}.html").write_text(html)


ICON = {
    "lotus": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 20c-4 0-8-2-9-6 3-.5 6 .5 9 6zM12 20c4 0 8-2 9-6-3-.5-6 .5-9 6zM12 20c-2.5-3-3.5-7 0-13 3.5 6 2.5 10 0 13z"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="9"/><path d="m8 12.5 3 3 5-6"/></svg>',
    "lock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 1 1 8 0v3"/></svg>',
    "ganesh": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="9" r="5"/><path d="M12 14c0 3-2 4-4 4M9 7.5h.01M15 7.5h.01M7 5 5 3M17 5l2-2"/></svg>',
    "pot": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M7 11c0 5 2 8 5 8s5-3 5-8zM8 11h8M9 9h6l-1 2h-4z"/><circle cx="12" cy="6" r="2"/></svg>',
    "sun": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M5.6 18.4 7 17M17 7l1.4-1.4"/></svg>',
    "hand": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M8 13V6a1.5 1.5 0 0 1 3 0v5M11 11V4.5a1.5 1.5 0 0 1 3 0V11M14 11V6a1.5 1.5 0 0 1 3 0v8c0 4-3 7-6 7s-5-2-6-4l-2-4a1.5 1.5 0 0 1 2.6-1.5L8 13"/></svg>',
    "music": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M9 18V6l11-2v12"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/></svg>',
    "horse": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M6 21v-6l-2-3 3-6 5-2 3 3-2 3h4l3 3v8"/><path d="M10 8h.01"/></svg>',
    "fire": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 21c-4 0-6-3-6-6 0-4 4-6 4-10 3 2 6 5 6 9 1-1 1-2 1-3 2 2 1 10-5 10z"/></svg>',
    "glass": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M7 3h10l-1 7a4 4 0 0 1-8 0zM12 14v6M8 21h8"/></svg>',
}

RITUALS = [("ganesh", "Ganesh puja", "Auspicious beginning"), ("pot", "Mayra / Bhaat", "Maternal family's blessing"), ("sun", "Haldi", "Turmeric & laughter"),
           ("hand", "Mehendi", "Henna evening"), ("music", "Mahila sangeet", "Songs of the women"), ("horse", "Baraat", "The groom's procession"),
           ("fire", "Phera", "Seven vows"), ("glass", "Reception", "Celebrate with all")]

DESIGNS = [("royal-heritage", "Royal Heritage", "Premium · Luxury", "Haveli arch, maroon & gold"),
           ("mandap-magic", "Mandap Magic", "Basic · Premium", "Ivory mandap, floral"),
           ("golden-elegance", "Golden Elegance", "Luxury", "Ornate mandala, rich red"),
           ("desert-dreams", "Desert Dreams", "Basic · Premium", "Thar dunes, minimal sand"),
           ("marwari-classic", "Marwari Classic", "Basic · Premium · Luxury", "Kalash & leaves, classic red"),
           ("royal-palace", "Royal Palace", "Luxury", "Palace skyline, black & gold")]
NAMES = ["Aditi|Varun", "Pooja|Arjun", "Nidhi|Sahil", "Riddhi|Karan", "Shruti|Yash", "Kavya|Aditya"]


def design_card(slug, name, tiers, note, names, href="design-royal-heritage.html"):
    return f"""<a class="design" href="{href}"><div data-invite="{slug}" data-size="sm" data-names="{names}"></div><b>{name}</b><small>{tiers}</small></a>"""


PRICES = """
<div class="prices">
  <div class="price"><h3>Basic</h3><div class="amt">₹4,999 <small>onwards</small></div><p class="muted small" style="margin:0">A curated Marwari design, personalised with your details.</p>
    <ul><li>Curated Marwari design</li><li>Names, dates, venue & RSVP</li><li>Share link + QR code</li><li>1 revision round</li><li>Ready in about 5 days</li></ul><a class="btn secondary" href="contact.html">Choose Basic</a></div>
  <div class="price hl"><span class="pill">Most chosen</span><h3>Premium</h3><div class="amt">₹11,999 <small>onwards</small></div><p class="small" style="margin:0">Personalised with your photos and every function.</p>
    <ul><li>Personalised design & photo gallery</li><li>Every function: Mehendi to Phera</li><li>Countdown, maps & RSVP</li><li>2 revision rounds</li><li>Ready in about 10 days</li></ul><a class="btn gold" href="contact.html">Choose Premium</a></div>
  <div class="price"><h3>Luxury / Bespoke</h3><div class="amt">₹29,999 <small>onwards</small></div><p class="muted small" style="margin:0">Designed from scratch around your story.</p>
    <ul><li>Fully custom design & development</li><li>Multiple function pages</li><li>Your story, family & traditions</li><li>Unlimited reasonable revisions</li><li>Ready in about 21 days</li></ul><a class="btn secondary" href="contact.html">Choose Luxury</a></div>
</div>"""

FAQS = [
    ("How long does it take?", "Basic is ready in about 5 days, Premium in about 10 and Luxury in about 21. Rush delivery is available for a 25% fee."),
    ("What do we need to send you?", "Names exactly as they should appear, parents' and grandparents' names, your functions with dates, times and venues, RSVP details and a few couple photos. Our guided form makes sure nothing is missed."),
    ("How do changes work?", "You send all your changes together as one revision round from your private page. Your designer works through them as a checklist. Basic includes 1 round, Premium 2 and Luxury unlimited reasonable rounds."),
    ("Can the invitation be in Hindi or Marwari?", "Yes: English, Hindi, Marwari or bilingual, with traditional openings like “Shri Ganeshaya Namah” and blessings written the way your family wants."),
    ("We live abroad. Can you still help?", "Absolutely. Many of our families are NRIs. Everything happens online and guests anywhere can open the invitation on their phones."),
    ("How long does the invitation stay online?", "Through the wedding and at least six months after. Longer hosting and your own web address are available on request."),
    ("How do payments work?", "A booking amount to start and the balance before we publish, by UPI from your private page. Our refund policy is shared before you book."),
    ("Are our photos and details private?", "Yes. Your project page is private and we never use your photos, names or review publicly without your consent."),
]


def faq_html(items):
    return "".join(f'<details class="faq"{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(items))


# ── 1 · Home ──────────────────────────────────────────────
page("index", "BFI · Marwari wedding invitations", "Premium digital wedding invitations for Marwari families: every ritual, every name, delivered as a beautiful invitation website.", "", f"""
<section class="hero"><div class="wrap">
  <div>
    <div class="deva" style="font-size:18px;margin-bottom:14px">॥ श्री गणेशाय नमः ॥</div>
    <h1>Wedding invitations, <em>the Marwari way</em></h1>
    <p class="lead">From Ganesh puja to the pheras, every ritual and every elder's name, written with care and delivered as a beautiful invitation your family opens on their phones.</p>
    <div class="row"><a class="btn primary" href="designs.html">Explore designs</a><a class="btn secondary" href="#">Chat on WhatsApp</a></div>
    <div class="slots"><i></i> 3 of 5 invitation slots open this week</div>
  </div>
  <div class="visual"><div class="arch"><div data-invite="royal-heritage"></div></div></div>
</div></section>

<section class="tint" style="padding:44px 0"><div class="wrap promises">
  <div class="promise">{ICON['lotus']}<div><b>Made for Marwari rituals</b><span>Mayra, Mahila sangeet, Baraat and every function you celebrate.</span></div></div>
  <div class="promise">{ICON['check']}<div><b>Every name checked by hand</b><span>From Dada-Dadi to Nana-Nani, spelt exactly as your family writes them.</span></div></div>
  <div class="promise">{ICON['lock']}<div><b>Private & consent-first</b><span>Your own private page. Nothing shared publicly without your yes.</span></div></div>
</div></section>

<section><div class="wrap">
  <div class="row" style="justify-content:space-between;align-items:flex-end;margin-bottom:30px"><div class="head" style="margin:0"><div class="eyebrow">Designs</div><h2>Invitations your family will forward with pride</h2><div class="divider">✦</div></div><a class="btn secondary sm" href="designs.html">All designs</a></div>
  <div class="carousel">{''.join(design_card(s, n, t, no, NAMES[i]) for i, (s, n, t, no) in enumerate(DESIGNS[:4]))}</div>
</div></section>

<section class="tint"><div class="wrap">
  <div class="head center"><div class="eyebrow">Rituals we design for</div><h2>Every function, given its due</h2><p>Each function gets its own page with the right timing, dress code and venue, written the way your family celebrates it.</p></div>
  <div class="rituals">{''.join(f'<div class="ritual">{ICON[i]}<b>{n}</b><span>{d}</span></div>' for i, n, d in RITUALS)}</div>
</div></section>

<section><div class="wrap">
  <div class="head"><div class="eyebrow">How it works</div><h2>Four simple steps</h2></div>
  <div class="steps">
    <div class="step"><b>Choose a design</b><p>Pick from our Marwari collection, or ask for something bespoke.</p></div>
    <div class="step"><b>Share your details</b><p>A guided form for names, functions and photos. No long WhatsApp threads.</p></div>
    <div class="step"><b>Review your preview</b><p>See it on your phone and send all changes in one go.</p></div>
    <div class="step"><b>Share with family</b><p>Get your link and QR code, and send it to every guest.</p></div>
  </div>
  <p style="margin-top:22px"><a href="how-it-works.html">See the full process →</a></p>
</div></section>

<section class="tint"><div class="wrap">
  <div class="head center"><div class="eyebrow">Pricing</div><h2>Clear packages, no surprises</h2></div>
  {PRICES}
</div></section>

<section><div class="wrap quote">
  <div class="divider" style="margin:0 auto 20px">✦</div>
  <blockquote>“They understood every Marwari ritual we wanted. Our families loved the invitation.”</blockquote>
  <cite>Aditi & Varun · Jaipur · <a href="real-weddings.html">Read their story</a></cite>
</div></section>

<section class="band" style="padding:56px 0"><div class="wrap split" style="align-items:center">
  <div><div class="eyebrow" style="color:var(--gold)">For wedding professionals</div><h2>Partner with BFI</h2><p class="lead" style="margin-top:12px">Planners, photographers, makeup artists and venues earn 15–20% on every completed order they refer.</p></div>
  <div class="row" style="justify-content:flex-start"><a class="btn gold" href="partners.html">Become a partner</a><a class="btn ghost-light" href="partners.html">How it works</a></div>
</div></section>

<section><div class="wrap narrow">
  <div class="head"><div class="eyebrow">Questions</div><h2>Frequently asked</h2></div>
  {faq_html(FAQS[:5])}
  <p style="margin-top:20px"><a href="faq.html">All questions →</a></p>
</div></section>

<section class="band center" style="padding:72px 0"><div class="wrap">
  <img src="../assets/logo-full.png" alt="" style="width:min(320px,70vw);margin:0 auto 12px">
  <h2>Let's write your invitation together</h2>
  <p class="lead" style="margin:12px auto 26px">Tell us your dates and functions. We'll share designs and a clear quote within a day.</p>
  <div class="row" style="justify-content:center"><a class="btn gold" href="contact.html">Plan my invitation</a><a class="btn ghost-light" href="#">Chat on WhatsApp</a></div>
</div></section>
""")

# ── 2 · Designs ───────────────────────────────────────────
page("designs", "Designs · BFI Marwari Invitations", "Marwari wedding invitation designs: haveli, mandap, mandala, desert, kalash and palace themes.", "designs", f"""
<div class="page-hero"><div class="wrap"><div class="crumbs"><a href="index.html">Home</a> / Designs</div>
  <div class="eyebrow">The collection</div><h1>Marwari wedding invitation designs</h1><p class="lead" style="margin-top:14px">Six signature designs, each personalised with your names, functions, colours and photos. Tap a design to see it up close.</p></div></div>
<section><div class="wrap">
  <div class="row" style="justify-content:space-between;margin-bottom:26px">
    <div class="chips"><a class="chip on" href="#">All</a><a class="chip" href="#">Basic</a><a class="chip" href="#">Premium</a><a class="chip" href="#">Luxury</a></div>
    <div class="chips"><a class="chip" href="#">Traditional</a><a class="chip" href="#">Minimal</a><a class="chip" href="#">Royal</a></div>
  </div>
  <div class="designs">{''.join(f'<a class="design" href="design-royal-heritage.html"><div data-invite="{s}" data-size="sm" data-names="{NAMES[i]}"></div><b>{n}</b><small>{t}</small><p class="small muted" style="margin:6px 0 0">{no}</p></a>' for i, (s, n, t, no) in enumerate(DESIGNS))}</div>
</div></section>
<section class="tint"><div class="wrap split" style="align-items:center">
  <div><div class="eyebrow">Bespoke</div><h2>Want something only yours?</h2><p class="lead" style="margin-top:12px">Our Luxury / Bespoke package designs your invitation from scratch: your story, your family's traditions, every function on its own page.</p><a class="btn primary" href="contact.html">Talk to a designer</a></div>
  <div class="arch"><div data-invite="golden-elegance" data-names="Kavya|Aditya" data-city="Udaipur"></div></div>
</div></section>
""")

# ── 3 · Design detail ─────────────────────────────────────
page("design-royal-heritage", "Royal Heritage design · BFI", "Royal Heritage: a haveli-arch Marwari wedding invitation in maroon and gold.", "designs", f"""
<div class="page-hero" style="padding-bottom:20px"><div class="wrap"><div class="crumbs"><a href="index.html">Home</a> / <a href="designs.html">Designs</a> / Royal Heritage</div></div></div>
<section style="padding-top:30px"><div class="wrap split wide-right" style="align-items:center">
  <div class="arch"><div data-invite="royal-heritage"></div></div>
  <div>
    <div class="row" style="gap:8px;margin-bottom:12px"><span class="tier">Premium</span><span class="tier lux">Luxury</span></div>
    <h1 style="color:var(--maroon)">Royal Heritage</h1>
    <p class="lead" style="margin-top:14px">Inspired by the carved jharokhas of Shekhawati havelis: deep maroon, antique gold and a quiet arch that frames your names like a doorway to the celebration.</p>
    <div class="card" style="margin:22px 0">
      <div class="row" style="justify-content:space-between"><b>From ₹11,999</b><span class="small muted">Ready in about 10 days</span></div>
      <ul class="small" style="margin:12px 0 0;padding-left:18px;color:var(--muted)"><li>Every function with timings, venue and Maps</li><li>Couple photo gallery, countdown and RSVP</li><li>English, Hindi or bilingual wording</li><li>Share link for WhatsApp + printable QR code</li></ul>
    </div>
    <div class="row"><a class="btn primary" href="contact.html">Choose this design</a><a class="btn secondary" href="#">View live demo</a></div>
    <div class="slots"><i></i> 3 of 5 slots open this week</div>
  </div>
</div></section>
<section class="tint"><div class="wrap">
  <div class="head center"><div class="eyebrow">Inside the invitation</div><h2>One page for every function</h2></div>
  <div class="carousel">{''.join(f'<div class="design"><div data-invite="royal-heritage" data-size="sm" data-names="{n}" data-date="{d}"></div><b>{t}</b><small>{d}</small></div>' for t, n, d in [("Ganesh puja", "Ganesh|Puja", "10 · 02 · 2027"), ("Mayra", "Mayra|Bhaat", "10 · 02 · 2027"), ("Mehendi", "Mehendi|Raat", "11 · 02 · 2027"), ("Phera", "Aditi|Varun", "12 · 02 · 2027")])}</div>
</div></section>
<section><div class="wrap">
  <div class="head"><div class="eyebrow">You may also like</div><h2>Similar designs</h2></div>
  <div class="carousel">{''.join(design_card(s, n, t, no, NAMES[i + 1]) for i, (s, n, t, no) in enumerate(DESIGNS[1:5]))}</div>
</div></section>
""")

# ── 4 · Pricing ───────────────────────────────────────────
rows = [("Curated Marwari design", "y", "y", "y"), ("Fully custom design", "n", "n", "y"), ("Names, dates, venue & RSVP", "y", "y", "y"), ("Couple photos & gallery", "n", "y", "y"),
        ("Every function on its own section", "n", "y", "y"), ("Countdown & maps", "n", "y", "y"), ("Your story & family pages", "n", "n", "y"), ("Music & animations", "n", "n", "y"),
        ("Revision rounds", "1", "2", "Unlimited*"), ("Ready in", "~5 days", "~10 days", "~21 days")]
cell = lambda v: f'<td class="{"y" if v == "y" else "n" if v == "n" else ""}">{"✓" if v == "y" else "—" if v == "n" else v}</td>'
page("pricing", "Pricing · BFI Marwari Invitations", "Transparent pricing for Marwari wedding invitations: Basic ₹4,999, Premium ₹11,999, Luxury ₹29,999.", "pricing", f"""
<div class="page-hero"><div class="wrap center"><div class="eyebrow">Pricing</div><h1>Clear packages, no surprises</h1><p class="lead" style="margin:14px auto 0">Every package includes a private project page to track progress, share details, send changes and pay.</p></div></div>
<section><div class="wrap">{PRICES}
  <div class="slots" style="display:flex;justify-content:center;margin-top:24px"><i></i> 3 of 5 invitation slots open this week, so every family gets full attention</div>
</div></section>
<section class="tint"><div class="wrap">
  <div class="head center"><div class="eyebrow">Compare</div><h2>What's included</h2></div>
  <div class="table-wrap"><table class="compare"><thead><tr><th></th><th>Basic</th><th class="hl">Premium</th><th>Luxury</th></tr></thead>
  <tbody>{''.join(f'<tr><td>{r[0]}</td>{cell(r[1])}{cell(r[2])}{cell(r[3])}</tr>' for r in rows)}</tbody></table></div>
  <p class="small muted" style="margin-top:10px">*Unlimited reasonable revisions within the agreed scope.</p>
</div></section>
<section><div class="wrap">
  <div class="head"><div class="eyebrow">Add-ons</div><h2>Make it even more special</h2></div>
  <div class="addons">{''.join(f'<div class="addon"><div><b>{n}</b><span>{d}</span></div><span class="p">{p}</span></div>' for n, d, p in [("Digital save-the-date", "Announce the date months ahead with a matching mini-invite.", "₹1,499"), ("Extra function page", "A dedicated page for Mayra, Haldi, Sangeet or any function.", "₹999"), ("Wedding itinerary", "Hour-by-hour plan for guests across all functions.", "₹1,999"), ("Guest travel guide", "Hotels, travel, local tips and contacts for outstation guests.", "₹2,499"), ("Thank-you page", "Share photos and gratitude after the wedding.", "₹999"), ("Rush delivery", "Half the usual turnaround when the date is close.", "+25%")])}</div>
</div></section>
<section class="tint"><div class="wrap split">
  <div><div class="eyebrow">Payments</div><h3>Simple and secure</h3><p class="muted" style="margin-top:10px">A booking amount to start, the balance before we publish. Pay by UPI or bank transfer from your private page; you get a GST invoice for every payment.</p></div>
  <div><div class="eyebrow">Policy</div><h3>Cancellations & refunds</h3><p class="muted" style="margin-top:10px">Before design starts: 80% refund. After design starts: 40%. After the first preview: no refund. Full policy on our <a href="legal.html">refunds page</a>.</p></div>
</div></section>
""")

# ── 5 · How it works ──────────────────────────────────────
steps = [("Consultation", "Tell us about your functions, style and budget on a short call or chat.", "You + client manager"),
         ("Design & scope", "We confirm your design, price, timeline and revision rounds in writing.", "Client manager"),
         ("Your details", "Fill our guided form and upload photos, family names and inspiration.", "You"),
         ("We design", "Your designer personalises everything for your family.", "Designer"),
         ("Preview & changes", "Open the preview on your phone; send all changes together as one round.", "You + designer"),
         ("Quality check", "We check every name, date, time, link and the phone view.", "QA reviewer"),
         ("Final approval", "Nothing goes live until you sign off and the balance is cleared.", "You"),
         ("Share & celebrate", "Get your invitation link and QR code; send it to every guest.", "You")]
page("how-it-works", "How it works · BFI", "From consultation to sharing: the 8-step BFI process for Marwari wedding invitations.", "how-it-works", f"""
<div class="page-hero"><div class="wrap"><div class="eyebrow">How it works</div><h1>From hello to “you're invited”</h1><p class="lead" style="margin-top:14px">One clear process for every order, with one person looking after your family from start to finish.</p></div></div>
<section><div class="wrap split wide-left">
  <div class="timeline">{''.join(f'<div class="tl"><span class="n">{i + 1}</span><div><b>{t}</b><p>{d}</p><div class="who">{w}</div></div></div>' for i, (t, d, w) in enumerate(steps))}</div>
  <div class="card" style="position:sticky;top:100px"><div class="eyebrow">What we need from you</div>
    <ul style="padding-left:18px;margin:0;color:var(--muted)"><li>Bride & groom names, exactly as they should appear</li><li>Parents' and grandparents' names</li><li>Functions with dates, times and venues</li><li>RSVP contact and deadline</li><li>A few couple photos (Premium & Luxury)</li><li>Any wording or language preference</li></ul>
    <div class="divider">✦</div>
    <p class="small muted" style="margin-top:14px">Your private page shows a checklist, so you always know what's left.</p>
    <a class="btn primary block" href="contact.html">Plan my invitation</a></div>
</div></section>
<section class="tint"><div class="wrap">
  <div class="head center"><div class="eyebrow">Your private page</div><h2>Track everything in one place</h2><p>Progress, details, uploads, preview, changes, payments and messages, all on one private link.</p></div>
  <div class="cards">{''.join(f'<div class="card"><h4>{t}</h4><p class="muted small" style="margin:6px 0 0">{d}</p></div>' for t, d in [("Live progress", "See which stage your invitation is in and what we need next."), ("One round of changes", "Pin each change to a section and send them together."), ("Messages", "Talk to your designer and the studio; tag who you need with @."), ("Pay & download", "UPI payment, invoices, your live link and QR code.")])}</div>
</div></section>
""")

# ── 6 · Real weddings ─────────────────────────────────────
stories = [("royal-heritage", "Aditi|Varun", "Aditi & Varun", "Jaipur · Premium", "They understood every Marwari ritual we wanted. Our families loved the invitation."),
           ("marwari-classic", "Pooja|Arjun", "Pooja & Arjun", "Jaipur · Premium", "Dadi-ji's name was finally spelt right on a wedding card. Little things like that made us trust BFI."),
           ("golden-elegance", "Nidhi|Sahil", "Nidhi & Sahil", "Kolkata · Luxury", "Our NRI relatives RSVP'd from three countries in a day. The Mayra page made my mama cry happy tears."),
           ("desert-dreams", "Riddhi|Karan", "Riddhi & Karan", "Jodhpur · Basic", "Quick, beautiful and on time, even with our rush order.")]
page("real-weddings", "Real weddings · BFI", "Marwari families who celebrated with BFI invitations, shared with their consent.", "real-weddings", f"""
<div class="page-hero"><div class="wrap"><div class="eyebrow">Real weddings</div><h1>Families who celebrated with us</h1><p class="lead" style="margin-top:14px">Every story here is shared with the family's consent.</p></div></div>
<section><div class="wrap"><div class="cards">{''.join(f'<article class="story"><div class="cover"><div data-invite="{s}" data-size="sm" data-names="{n}"></div></div><div class="body"><div class="stars">★★★★★</div><blockquote>“{q}”</blockquote><b>{c}</b><div class="small muted">{m}</div></div></article>' for s, n, c, m, q in stories)}</div>
<p class="small muted center" style="margin-top:20px">Sample stories shown in this mockup. The live site shows only real, consented reviews.</p></div></section>
<section class="band center" style="padding:60px 0"><div class="wrap"><h2>Your story could be next</h2><p class="lead" style="margin:12px auto 24px">We take a limited number of weddings each week.</p><a class="btn gold" href="contact.html">Plan my invitation</a></div></section>
""")

# ── 7 · About ─────────────────────────────────────────────
page("about", "About BFI · Marwari Invitations", "Why BFI designs only for Marwari weddings.", "", f"""
<section class="band" style="padding:64px 0"><div class="wrap split" style="align-items:center">
  <img src="../assets/logo-full.png" alt="BFI Marwari Invitations" style="width:min(460px,100%);margin:0 auto">
  <div><div class="eyebrow" style="color:var(--gold)">About us</div><h1 style="color:#F7E7C6">We only do Marwari weddings</h1><p class="lead" style="margin-top:14px">Because getting them right is a craft of its own.</p></div>
</div></section>
<section><div class="wrap narrow">
  <h2>Why Marwari only</h2>
  <p style="margin-top:14px">A Marwari wedding is not a template with Indian colours. It is the Ganesh puja that opens every card, the Mayra that honours the maternal family, the Mahila sangeet, and a long, careful list of elders whose names must appear exactly right.</p>
  <p>Generic invitation apps miss these. Printed cards are beautiful but slow, expensive to post and impossible for relatives abroad. BFI brings both worlds together: the care of a traditional <i>kankotri</i>, delivered as an invitation your family opens on their phones.</p>
  <div class="divider">✦</div>
  <h2 style="margin-top:34px">How we work</h2>
  <div class="cards" style="margin-top:18px">{''.join(f'<div class="card"><h4>{t}</h4><p class="small muted" style="margin:6px 0 0">{d}</p></div>' for t, d in [("One person for your family", "A client manager looks after you from first call to delivery."), ("Designers who know the rituals", "Every design is checked against our cultural checklist."), ("Quality before publishing", "A second person checks every name, date and link."), ("Limited each week", "We cap our weekly slots so no family is rushed.")])}</div>
</div></section>
""")

# ── 8 · FAQ ───────────────────────────────────────────────
page("faq", "FAQ · BFI Marwari Invitations", "Answers about timelines, details, revisions, language, payments and privacy.", "faq", f"""
<div class="page-hero"><div class="wrap"><div class="eyebrow">Help</div><h1>Frequently asked questions</h1></div></div>
<section><div class="wrap split wide-left">
  <div>{faq_html(FAQS)}</div>
  <div class="card" style="position:sticky;top:100px"><h3>Still have a question?</h3><p class="muted" style="margin-top:8px">Message us. We usually reply within an hour, 10am–8pm.</p><a class="btn primary block" href="#">Chat on WhatsApp</a><a class="btn secondary block" style="margin-top:10px" href="contact.html">Send an enquiry</a></div>
</div></section>
""")

# ── 9 · Partners ──────────────────────────────────────────
page("partners", "Partner with BFI · Wedding professionals", "Planners, photographers, makeup artists and venues earn 15–20% on referred orders.", "", f"""
<section class="band" style="padding:64px 0"><div class="wrap split" style="align-items:center">
  <div><div class="eyebrow" style="color:var(--gold)">For wedding professionals</div><h1 style="color:#F7E7C6">Recommend BFI. Earn on every order.</h1><p class="lead" style="margin-top:14px">For planners, photographers, makeup & mehendi artists, venues and Marwari creators.</p><div class="row" style="margin-top:22px"><a class="btn gold" href="contact.html">Become a partner</a><a class="btn ghost-light" href="#">Partner login</a></div></div>
  <img src="../assets/logo-full.png" alt="" style="width:min(400px,100%);margin:0 auto">
</div></section>
<section><div class="wrap">
  <div class="head center"><div class="eyebrow">Commission</div><h2>Paid on every completed order</h2></div>
  <div class="cards">
    <div class="card center"><div class="eyebrow">Basic</div><div class="rate">15%</div><p class="small muted">≈ ₹750 per order</p></div>
    <div class="card center" style="border-color:var(--gold)"><div class="eyebrow">Premium</div><div class="rate">15%</div><p class="small muted">≈ ₹1,800 per order</p></div>
    <div class="card center"><div class="eyebrow">Luxury</div><div class="rate">20%</div><p class="small muted">≈ ₹6,000 per order</p></div>
  </div>
  <p class="small muted center" style="margin-top:12px">Paid monthly by UPI or bank transfer once the order is delivered and fully paid. Or start with a one-time trade: free invitations for your next 3 clients.</p>
</div></section>
<section class="tint"><div class="wrap">
  <div class="head center"><h2>How it works</h2></div>
  <div class="steps"><div class="step"><b>Join</b><p>Get your personal referral code and link.</p></div><div class="step"><b>Share</b><p>Send your link, or submit a couple directly from your partner app.</p></div><div class="step"><b>Track</b><p>See each referral's status and your commission live.</p></div><div class="step"><b>Get paid</b><p>Monthly payouts to your UPI or bank account.</p></div></div>
</div></section>
""")

# ── 10 · Contact / enquiry ────────────────────────────────
page("contact", "Plan my invitation · BFI", "Tell us about your wedding and get designs and a clear quote within a day.", "", f"""
<div class="page-hero"><div class="wrap"><div class="eyebrow">Plan my invitation</div><h1>Tell us about your wedding</h1><p class="lead" style="margin-top:14px">We'll reply with designs and a clear quote within a day.</p></div></div>
<section><div class="wrap split wide-left">
  <form class="card form" onsubmit="return false">
    <div class="cols"><label class="f">Your name(s)<input class="input" placeholder="Priya & Rohan"></label><label class="f">WhatsApp number<input class="input" placeholder="+91 98…"></label></div>
    <div class="cols"><label class="f">Wedding date<input class="input" placeholder="dd / mm / yyyy"></label><label class="f">City<input class="input" placeholder="Jaipur"></label></div>
    <label class="f">Package<select class="input"><option>Help me choose</option><option>Basic · from ₹4,999</option><option>Premium · from ₹11,999</option><option>Luxury · from ₹29,999</option></select></label>
    <label class="f">Functions & anything else<textarea class="input" placeholder="Ganesh puja, Mayra, Mehendi, Phera… style, colours, language"></textarea></label>
    <label class="f">Referral code (optional)<input class="input" placeholder="If a planner or friend referred you"></label>
    <label class="check"><i></i>I agree to be contacted on WhatsApp about my enquiry.</label>
    <button class="btn primary">Send enquiry</button>
  </form>
  <div style="display:grid;gap:16px">
    <div class="card"><div class="eyebrow">Fastest</div><h3>Chat on WhatsApp</h3><p class="muted" style="margin:8px 0 14px">+91 98000 00000 · 10am–8pm, Mon–Sat</p><a class="btn secondary block" href="#">Open WhatsApp</a></div>
    <div class="card"><div class="eyebrow">This week</div><h3>3 of 5 slots open</h3><p class="muted small" style="margin:8px 0 0">We take a limited number of invitations each week.</p></div>
    <div class="card"><div class="eyebrow">Studio</div><p class="muted" style="margin:6px 0 0">Jaipur, Rajasthan · serving families across India and abroad · hello@bfi-invitations.in</p></div>
  </div>
</div></section>
""")

# ── 11 · Track my invitation ──────────────────────────────
page("track", "Track my invitation · BFI", "Open your private BFI invitation page.", "", f"""
<section style="min-height:70vh;display:grid;place-items:center"><div class="wrap" style="max-width:520px">
  <div class="card center" style="padding:36px 28px">
    <img src="../assets/logo-mark.png" alt="" style="width:84px;border-radius:18px;margin:0 auto 18px">
    <h1 style="font-size:36px;color:var(--maroon)">Track your invitation</h1>
    <p class="muted" style="margin:10px 0 22px">Open the private link we sent you on WhatsApp, or paste it below.</p>
    <div class="form"><input class="input" placeholder="Paste your private link"><button class="btn primary block">Open my invitation</button></div>
    <p class="small muted" style="margin-top:18px">Lost your link? <a href="#">Email me a new one</a></p>
  </div>
  <p class="small muted center" style="margin-top:18px">Studio team or partner? <a href="#">Sign in</a></p>
</div></section>
""")

# ── 12 · Legal ────────────────────────────────────────────
page("legal", "Terms, privacy & refunds · BFI", "BFI terms of service, privacy policy and refund policy.", "", f"""
<div class="page-hero"><div class="wrap"><div class="eyebrow">Legal</div><h1>Terms, privacy & refunds</h1><p class="lead" style="margin-top:14px">Last updated: November 2026. Draft for legal review.</p></div></div>
<section><div class="wrap split legal-grid">
  <nav class="toc"><a class="on" href="#">Terms of service</a><a href="#">Privacy policy</a><a href="#">Refunds & cancellations</a><a href="#">Consent & showcase</a></nav>
  <div class="legal-body narrow">
    <h2 style="margin-top:0">Terms of service</h2><p>These terms explain how BFI — Marwari Invitations designs and delivers digital wedding invitations… <span class="muted">(full text to be provided by your lawyer)</span></p>
    <h2>Privacy policy</h2><p>We collect only what we need to make your invitation: names, contact details, event details and the photos you share. We never sell your data and never use it publicly without consent, in line with India's Digital Personal Data Protection Act, 2023…</p>
    <h2>Refunds & cancellations</h2><ul><li>Before design starts: 80% refund</li><li>After design starts: 40% refund</li><li>After the first preview: no refund</li><li>Late changes after final approval are charged as a new revision round</li></ul>
    <h2>Consent & showcase</h2><p>Your photos, names and review are used publicly only if you switch these on in your private page. You can change your mind at any time.</p>
  </div>
</div></section>
""")

print("written:", sorted(p.name for p in OUT.glob("*.html")))
