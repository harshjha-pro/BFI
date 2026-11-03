#!/usr/bin/env python3
"""Generate the Royal Heritage website pages in site/ from shared templates.

Run:  python3 tools/build_website.py
Pages share one header, footer, mobile menu and WhatsApp buttons. Page logic lives in site/js/app.js.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "site"
V = "20261103b"  # bump to bust browser caches for css/js

WA = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3Z"/></svg>')


def icon(paths, cls=""):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>')


I = {
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "diamond": '<path d="M6 3h12l4 6-10 12L2 9Z"/><path d="M2 9h20M12 21 8 9l4-6 4 6-4 12"/>',
    "phone": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M11 18h2"/>',
    "sliders": '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
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
    "star": '<path d="m12 2 3 6.5 7 .8-5.2 4.8 1.4 7L12 17.6 5.8 21.1l1.4-7L2 9.3l7-.8Z"/>',
}
ORN = f'<div class="orn" aria-hidden="true">{icon(I["lotus"])}</div>'

NAV = [("index", "Home"), ("invitations", "Invitations"), ("how-it-works", "How It Works"), ("about", "About"), ("contact", "Contact")]


def header(active):
    links = "".join(
        f'<a href="{k}.html"{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for k, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap hdr-in">
  <a class="brand" href="index.html"><img src="img/logo-sm.webp" alt="BFI Marwari Invitations, home" width="200" height="174"></a>
  <nav class="nav" aria-label="Main">{links}</nav>
  <div class="hdr-actions">
    <a class="btn btn-wa btn-sm" data-wa>{WA} Enquire on WhatsApp</a>
    <a class="icon-btn wa" data-wa aria-label="Chat on WhatsApp">{WA}</a>
    <span data-auth-slot style="display:contents"><a class="btn btn-outline btn-sm login-link" href="login.html">Login</a></span>
    <button class="icon-btn menu-btn" data-menu-open aria-label="Open menu" aria-controls="menu">{icon(I["menu"])}</button>
  </div>
</div></header>
<div class="sheet" id="menu" role="dialog" aria-modal="true" aria-label="Menu"><div class="sheet-bg"></div><div class="sheet-panel">
  <div style="display:flex;justify-content:space-between;align-items:center"><a class="brand" href="index.html"><img src="img/logo-sm.webp" alt="BFI Marwari Invitations, home" width="200" height="174"></a><button class="icon-btn" data-menu-close aria-label="Close menu">{icon(I["x"])}</button></div>
  <nav aria-label="Mobile">{"".join(f'<a href="{k}.html">{t}</a>' for k, t in NAV)}<a href="customize.html">Customize</a></nav>
  <div style="margin-top:auto"><div data-auth-menu><a class="btn btn-ghost btn-block" href="login.html">Login or create account</a></div><a class="btn btn-wa btn-block" data-wa>{WA} Chat on WhatsApp</a></div>
</div></div>'''


def footer():
    return f'''<footer class="ftr"><div class="wrap">
  <div class="ftr-grid">
    <div><img class="ftr-logo" src="img/logo-gold.webp" alt="BFI Marwari Invitations" width="431" height="374" loading="lazy"><p style="margin-top:10px;max-width:280px">Premium digital wedding invitations, crafted with Marwari tradition and shared with love.</p></div>
    <div><h4>Explore</h4><ul><li><a href="invitations.html">All invitations</a></li><li><a href="invitations.html?c=royal">Royal collection</a></li><li><a href="invitations.html?c=traditional">Traditional collection</a></li><li><a href="invitations.html?c=elegant">Elegant collection</a></li><li><a href="invitations.html?c=modern">Modern collection</a></li></ul></div>
    <div><h4>Studio</h4><ul><li><a href="how-it-works.html">How it works</a></li><li><a href="customize.html">Customize an invitation</a></li><li><a href="about.html">About BFI</a></li><li><a href="login.html">My account</a></li></ul></div>
    <div><h4>Contact</h4><ul><li><a data-wa>WhatsApp <span data-cfg="whatsappDisplay"></span></a></li><li><a data-mailto><span data-cfg="email"></span></a></li><li><span data-cfg="city"></span></li><li><span data-cfg="hours"></span></li></ul></div>
  </div>
  <div class="ftr-bot"><span>© <span data-year></span> BFI · Marwari Invitations. Made with love in Rajasthan.</span><span lang="hi" style="font-family:var(--deva);color:var(--gold)">॥ शुभ विवाह ॥</span></div>
</div></footer>'''


def page(slug, title, desc, body, active=None, bar=True, extra_head=""):
    mbar = f'''<div class="mbar"><a class="btn btn-primary" href="invitations.html">Explore invitations</a><a class="btn btn-wa" data-wa>{WA} WhatsApp</a></div>''' if bar else ""
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#641E2B">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="img/og-image.png">
<meta property="og:type" content="website">
<link rel="icon" href="img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://oaosapkkzoynaqpnmvrj.supabase.co" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Tiro+Devanagari+Hindi&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css?v={V}">{extra_head}
</head>
<body data-page="{slug}"{'' if bar else ' class="no-mbar"'}>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<a class="wa-float" data-wa aria-label="Chat with BFI on WhatsApp">{WA}</a>
{mbar}
<script src="js/vendor/supabase.js?v=2.45.4"></script>
<script src="js/config.js?v={V}"></script>
<script src="js/app.js?v={V}"></script>
</body>
</html>
'''
    (OUT / f"{slug}.html").write_text(html)


def strip_item(ic, t, s):
    return f'<div class="strip-item">{icon(I[ic])}<div><b>{t}</b><span>{s}</span></div></div>'


# ---------------- Home ----------------
HOME = f'''
<section class="hero">
  <div class="hero-art" data-img="hero.jpg" role="img" aria-label="Rajasthani palace arch with royal elephants and palace skyline"></div>
  <div class="hero-glow"></div>
  <div class="hero-in"><div class="hero-content">
    <p class="deva" lang="hi">॥ श्री गणेशाय नमः ॥</p>
    <h1 class="sr">BFI Marwari Invitations</h1>
    <img class="hero-logo" src="img/logo.webp" alt="BFI Marwari Invitations" width="431" height="374" fetchpriority="high">
    <p class="h1 hero-title" style="font:600 clamp(26px,5vw,38px)/1.15 var(--serif);color:var(--brown);margin-top:14px">Premium Digital Wedding Invitations <br>for Your <em style="color:var(--maroon)">Grand Celebrations</em></p>
    <div class="row"><a class="btn btn-primary" href="invitations.html">Explore Invitations {icon(I["arrow"])}</a><a class="btn btn-outline" href="customize.html">Create Your Invitation</a></div>
    <p class="trust">Made in Jaipur · Ready in 24 hours · Private &amp; secure</p>
  </div></div>
</section>
<section class="strip"><div class="wrap strip-grid">
  {strip_item("diamond", "Premium Designs", "Royal &amp; elegant")}
  {strip_item("phone", "Digital &amp; Shareable", "WhatsApp, email &amp; more")}
  {strip_item("sliders", "Customizable", "As per your theme")}
  {strip_item("zap", "Quick Delivery", "Ready in 24 hours")}
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head center reveal"><h2>Explore Our Invitation Collections</h2>{ORN}</div>
  <div class="tiles reveal">
    <a class="tile dark" href="invitations.html?c=royal"><img data-img="inv-rajwada-royale.jpg" alt="" loading="lazy" width="360" height="540"><span>Royal<small>Collection</small></span></a>
    <a class="tile light" href="invitations.html?c=traditional"><img data-img="inv-gulmohar-classic.jpg" alt="" loading="lazy" width="360" height="540"><span>Traditional<small>Collection</small></span></a>
    <a class="tile light" href="invitations.html?c=elegant"><img data-img="inv-gulabi-bagh.jpg" alt="" loading="lazy" width="360" height="540"><span>Elegant<small>Collection</small></span></a>
    <a class="tile dark" href="invitations.html?c=modern"><img data-img="inv-mor-pankh.jpg" alt="" loading="lazy" width="360" height="540"><span>Modern<small>Collection</small></span></a>
  </div>
  <div class="center" style="margin-top:30px"><a class="btn btn-primary" href="invitations.html">View All Collections {icon(I["arrow"])}</a></div>
</div></section>

<section class="why"><div class="why-grid">
  <div class="why-img" data-img="palace.jpg" role="img" aria-label="Rajasthani palace with bougainvillea"></div>
  <div class="why-body"><h2>Why Choose BFI?</h2>
    <div class="why-list">
      <div>{icon(I["crown"])}Culturally Authentic</div>
      <div>{icon(I["heart"])}Beautiful &amp; Unique Designs</div>
      <div>{icon(I["clock"])}Fast Turnaround</div>
      <div>{icon(I["shield"])}Trusted by Families</div>
    </div></div>
</div></section>

<section class="sec"><div class="wrap split">
  <div class="reveal"><div class="phone"><div class="phone-screen" data-img="couple.jpg" role="img" aria-label="Wedding invitation on a phone showing the couple under a floral arch"><div class="pv-text pv-light" style="inset:7% 12% 64%"><span class="pv-names" style="font-size:22px">Wedding<br>Invitation</span></div></div></div></div>
  <div class="reveal">
    <p class="eyebrow">Made for every Marwari ritual</p>
    <h2 style="margin-top:10px">Digital Invitations for Your Special Day</h2>
    <p class="lead" style="margin-top:14px">Create, customise and share your wedding invitation with your loved ones in a modern and elegant way, with every function, every elder's name and every venue in one beautiful link.</p>
    <ul class="checks">
      <li>{icon(I["check"])}Bilingual (Hindi / English) and Marwari blessings</li>
      <li>{icon(I["check"])}Share via WhatsApp, email or link, plus a QR code</li>
      <li>{icon(I["check"])}RSVP &amp; guest confirmation (optional)</li>
      <li>{icon(I["check"])}Ganesh puja to reception: every event with maps</li>
    </ul>
    <div class="row"><a class="btn btn-primary" href="customize.html">Get Started {icon(I["arrow"])}</a><a class="btn btn-ghost" href="how-it-works.html">How it works</a></div>
  </div>
</div></section>

<section class="sec sec-tint" style="padding-top:56px"><div class="wrap">
  <div class="sec-head center reveal"><p class="eyebrow">Most loved</p><h2 style="margin-top:8px">Featured Invitations</h2>{ORN}</div>
  <div class="grid-inv" id="featured"><div class="card skel" style="aspect-ratio:2/3.6"></div><div class="card skel" style="aspect-ratio:2/3.6"></div><div class="card skel" style="aspect-ratio:2/3.6"></div><div class="card skel" style="aspect-ratio:2/3.6"></div></div>
</div></section>

<div class="skyline" data-img="skyline.jpg" aria-hidden="true"></div>
<section class="quote">“A Perfect Blend of Marwari Tradition and Modern Convenience”</section>
'''
page("index", "BFI Marwari Invitations · Premium Digital Wedding Invitations",
     "Premium digital wedding invitations for Marwari families: royal Rajasthani designs, every ritual, shared on WhatsApp.", HOME, "index")

# ---------------- Invitations ----------------
INV = f'''
<section class="phead"><div class="wrap">
  <h1>Our Invitation Collections</h1>
  <p class="lead">A curated collection of digital wedding invitations inspired by Marwari heritage and royal traditions.</p>
</div></section>
<section class="sec" style="padding-top:28px"><div class="wrap">
  <div class="chips" role="group" aria-label="Filter by collection">
    <button class="chip" data-c="all" aria-pressed="true">All</button><button class="chip" data-c="royal" aria-pressed="false">Royal</button><button class="chip" data-c="traditional" aria-pressed="false">Traditional</button><button class="chip" data-c="elegant" aria-pressed="false">Elegant</button><button class="chip" data-c="modern" aria-pressed="false">Modern</button>
  </div>
  <div class="toolbar"><span class="muted" id="count" aria-live="polite">Loading…</span>
    <div class="row" style="gap:8px"><label class="sr" for="tier">Package</label><select id="tier"><option value="">All packages</option><option>Basic</option><option>Premium</option><option>Luxury</option></select>
    <label class="sr" for="sort">Sort</label><select id="sort"><option value="">Popular</option><option value="low">Price: low to high</option><option value="high">Price: high to low</option></select></div></div>
  <div class="grid-inv" id="grid">{'<div class="card skel" style="aspect-ratio:2/3.6"></div>' * 8}</div>
  <div class="panel panel-gold center" style="margin-top:44px"><p class="eyebrow">Luxury bespoke</p><h2 style="margin:8px 0 10px;font-size:32px">Want something only yours?</h2><p class="lead" style="margin:0 auto 18px">Our designers can create an invitation from scratch around your family, your city and your story.</p><div class="row" style="justify-content:center"><a class="btn btn-primary" href="contact.html">Request bespoke design</a><a class="btn btn-wa" data-wa="Namaste BFI 🙏 We'd like a bespoke (Luxury) wedding invitation.">{WA} Ask on WhatsApp</a></div></div>
</div></section>'''
page("invitations", "Invitation Collections · BFI Marwari Invitations",
     "Browse Royal, Traditional, Elegant and Modern digital wedding invitations for Marwari weddings.", INV, "invitations")

# ---------------- Invitation detail ----------------
DET = '''
<section class="sec" style="padding-top:22px"><div class="wrap">
  <p class="crumbs"><a href="invitations.html">Invitations</a> › <a id="crumb-col" href="invitations.html">Collection</a> › <span id="crumb" aria-current="page">Design</span></p>
  <div class="detail" id="detail"><div class="gallery"><div class="big skel"></div></div><div><div class="skel" style="height:40px;border-radius:8px;width:60%"></div></div></div>
</div></section>
<section class="sec sec-tint" style="padding-top:56px"><div class="wrap">
  <div class="sec-head center"><h2>You may also like</h2>''' + ORN + '''</div>
  <div class="grid-inv" id="similar"></div>
</div></section>'''
page("invitation", "Invitation · BFI Marwari Invitations", "A digital wedding invitation design by BFI Marwari Invitations.", DET, "invitations")

# ---------------- How it works ----------------
def step(n, ic, t, s):
    return f'<div class="step reveal"><div class="step-ic">{icon(I[ic])}</div><h3>{n}. {t}</h3><p>{s}</p></div>'


FAQ = [
    ("How long does it take?", "Basic invitations are ready in 24 hours, Premium in 48 hours and Luxury in 72 hours after we receive your details."),
    ("Can I change details after it's shared?", "Yes. Your link stays the same, so guests always see the latest version. One round of changes is free; spelling fixes are always free."),
    ("Is it in Hindi?", "Choose English, Hindi, Marwari + Hindi or bilingual. We add traditional blessings like ॥ श्री गणेशाय नमः ॥ on request."),
    ("How do guests receive it?", "You get a private link, a WhatsApp-ready message and a QR code for printed cards."),
    ("Do you collect RSVPs?", "Yes, optionally: guests confirm attendance and guest count, and you see the list."),
    ("How do I pay?", "We confirm the package with you on WhatsApp and share a UPI or bank payment link. 50% to start, 50% on approval."),
]
HOW = f'''
<section class="phead"><div class="wrap"><h1>How It Works</h1><p class="lead">Get your digital wedding invitation in four simple steps.</p></div></section>
<section class="sec"><div class="wrap">
  <div class="steps">
    {step(1, "image", "Choose a Design", "Browse our curated collection or ask for a bespoke design.")}
    {step(2, "edit", "Customize", "Share names, functions, venues, language and music.")}
    {step(3, "eye", "Preview", "Review the invitation on your phone; one round of changes included.")}
    {step(4, "share", "Share", "Send your link and QR code to every guest on WhatsApp.")}
  </div>
  <div class="center" style="margin-top:36px"><a class="btn btn-primary" href="invitations.html">Choose a design {icon(I["arrow"])}</a></div>
</div></section>
<div class="skyline" data-img="skyline.jpg" aria-hidden="true"></div>
<section class="sec sec-tint" style="padding-top:48px"><div class="wrap">
  <div class="sec-head center"><h2>Delivery timeline</h2>{ORN}</div>
  <div class="timeline">
    <div class="tl"><span class="tag">Basic</span><p style="margin-top:12px"><b>24 hrs</b></p><p class="muted">One design, your names and events, shareable link and QR.</p></div>
    <div class="tl"><span class="tag">Premium</span><p style="margin-top:12px"><b>48 hrs</b></p><p class="muted">Music, photo gallery, RSVP, maps for every event.</p></div>
    <div class="tl"><span class="tag">Luxury</span><p style="margin-top:12px"><b>72 hrs</b></p><p class="muted">Our grandest designs or a bespoke invitation, with priority support.</p></div>
  </div>
  <div class="split" style="margin-top:48px;align-items:start">
    <div class="panel"><h3>What we need from you</h3><ul class="checks" style="margin-bottom:0">
      <li>{icon(I["check"])}Bride's and groom's names (and how you'd like them written)</li>
      <li>{icon(I["check"])}Parents', grandparents' and elders' names</li>
      <li>{icon(I["check"])}Every function: date, time, venue, Google Maps link</li>
      <li>{icon(I["check"])}Language, blessing line and music choice</li>
      <li>{icon(I["check"])}Photos (optional, for Premium and Luxury)</li></ul></div>
    <div><h3 style="margin-bottom:6px">Questions</h3>{"".join(f'<details class="acc"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)}</div>
  </div>
</div></section>
<section class="quote">Ready to begin? <a href="customize.html" style="color:var(--gold);white-space:nowrap">Create your invitation →</a></section>'''
page("how-it-works", "How It Works · BFI Marwari Invitations", "Choose, customize, preview and share your digital wedding invitation in four simple steps.", HOW, "how-it-works")

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
page("customize", "Customize Your Invitation · BFI Marwari Invitations", "Add names, events, venues, language, music and RSVP options to your Marwari wedding invitation.", CUST, None, bar=False)

# ---------------- About ----------------
ABOUT = f'''
<section class="sec" style="padding-top:44px"><div class="wrap about-hero">
  <div>
    <p class="eyebrow">About BFI</p>
    <h1 style="margin-top:10px">Preserving Marwari Traditions in a Digital Way</h1>
    <p class="lead" style="margin-top:16px">BFI – Marwari Invitations is a premium digital invitation studio dedicated to creating beautiful, customisable wedding invitations for Marwari families.</p>
    <p style="margin-top:14px">We blend the richness of Marwari culture, royal Rajasthani aesthetics and modern convenience to make your celebration even more special: from the first ॥ श्री गणेशाय नमः ॥ to the last reception dinner.</p>
    <div class="row" style="margin-top:22px"><a class="btn btn-primary" href="invitations.html">See our designs</a><a class="btn btn-wa" data-wa>{WA} Talk to us</a></div>
  </div>
  <div class="arch-img" data-img="palace.jpg" role="img" aria-label="Jaipur palace with jharokha windows and bougainvillea"></div>
</div></section>
<section class="sec sec-tint"><div class="wrap split">
  <div><p class="eyebrow">Our story</p><h2 style="margin-top:8px">From kankotri to your phone</h2>
    <p class="lead" style="margin-top:14px">Every Marwari wedding begins with a kankotri: an invitation carried with care to every relative. Families now share invitations on WhatsApp, but most digital cards forget the rituals, the elders and the language that make a Marwari wedding what it is.</p>
    <p style="margin-top:12px">BFI was started in Jaipur to fix that: invitations that honour every ritual, list every elder correctly and still feel effortless for guests to open.</p></div>
  <div><p class="eyebrow">Our heritage</p><h2 style="margin-top:8px">Inspired by Rajasthan</h2>
    <p class="lead" style="margin-top:14px">Shekhawati havelis, jharokha windows, royal elephants, peacocks and the colours of Gangaur: our designs carry the same craft, made for the screens your family uses every day.</p></div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head center"><h2>What we stand for</h2>{ORN}</div>
  <div class="values">
    <div class="value">{icon(I["lotus"])}<h3>Our Vision</h3><p>To be the most trusted choice for digital wedding invitations in Marwari families everywhere.</p></div>
    <div class="value">{icon(I["diamond"])}<h3>Our Values</h3><p>Tradition · Quality · Personalisation · Trust. Every name is checked by hand.</p></div>
    <div class="value">{icon(I["users"])}<h3>Our Promise</h3><p>Elegant designs, quick delivery and a seamless experience for your special day.</p></div>
  </div>
</div></section>
<div class="skyline" data-img="skyline.jpg" aria-hidden="true"></div>
<section class="quote">“Rooted in Rajasthan, crafted for today.”</section>'''
page("about", "About BFI · Marwari Invitations", "BFI preserves Marwari wedding traditions with premium digital invitations made in Rajasthan.", ABOUT, "about")

# ---------------- Contact ----------------
CONTACT = f'''
<section class="phead"><div class="wrap"><h1>Contact Us</h1><p class="lead">Have a question or want a custom invitation? We'd love to hear from you.</p></div></section>
<section class="sec" style="padding-top:36px"><div class="wrap contact">
  <div class="cinfo">
    <a class="wa" data-wa><span class="ci-ic">{WA}</span><span><b>WhatsApp</b><span data-cfg="whatsappDisplay"></span></span></a>
    <a data-mailto><span class="ci-ic">{icon(I["mail"])}</span><span><b>Email</b><span data-cfg="email"></span></span></a>
    <div class="ci"><span class="ci-ic">{icon(I["pin"])}</span><span><b>Location</b><span data-cfg="city"></span></span></div>
    <div class="ci"><span class="ci-ic">{icon(I["clock"])}</span><span><b>Hours</b><span data-cfg="hours"></span></span></div>
  </div>
  <div class="panel panel-gold">
    <h2 style="font-size:30px;margin-bottom:6px">Send an enquiry</h2><p class="muted" style="margin-bottom:18px">We reply within an hour on WhatsApp.</p>
    <div id="c-status"></div>
    <form class="form" id="contact-form" novalidate>
      <div class="f2"><div class="field"><label for="c-name">Your name <span class="req">*</span></label><input id="c-name" name="name" required autocomplete="name" placeholder="Enter your name"></div>
      <div class="field"><label for="c-phone">WhatsApp number <span class="req">*</span></label><input id="c-phone" name="phone" type="tel" required inputmode="tel" autocomplete="tel" placeholder="+91"></div></div>
      <div class="f2"><div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" autocomplete="email" placeholder="Enter your email"></div>
      <div class="field"><label for="c-date">Wedding date</label><input id="c-date" name="wedding_date" type="date"></div></div>
      <div class="f2"><div class="field"><label for="c-city">City</label><input id="c-city" name="city" autocomplete="address-level2" placeholder="e.g. Jaipur"></div>
      <div class="field"><label for="c-pkg">Package</label><select id="c-pkg" name="package"><option>Not sure</option><option>Basic</option><option>Premium</option><option>Luxury</option></select></div></div>
      <div class="field"><label for="c-design">Preferred design</label><select id="c-design" name="design"><option value="">Not decided yet</option></select></div>
      <div class="field"><label for="c-msg">Your message <span class="req">*</span></label><textarea id="c-msg" name="message" required placeholder="Tell us about your requirement…"></textarea></div>
      <input type="text" name="company" tabindex="-1" autocomplete="off" class="sr" aria-hidden="true">
      <label class="check"><input type="checkbox" name="consent" required> I agree to be contacted on WhatsApp about my enquiry.</label>
      <button class="btn btn-primary btn-block" type="submit">Send Message {icon(I["arrow"])}</button>
    </form>
  </div>
</div></section>
<div class="skyline" data-img="skyline.jpg" aria-hidden="true"></div>'''
page("contact", "Contact · BFI Marwari Invitations", "Talk to BFI on WhatsApp or send an enquiry for your Marwari wedding invitation.", CONTACT, "contact")

# ---------------- Login ----------------
GOOGLE = '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3 0 5.8 1.1 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3 0 5.8 1.1 7.9 3l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3a12 12 0 0 1-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'
LOGIN = f'''
<section class="sec" style="padding-top:40px;background:var(--tint)"><div class="wrap">
  <div class="auth">
    <div class="center" style="margin-bottom:20px"><img src="img/logo.webp" alt="BFI Marwari Invitations" width="431" height="374" style="width:190px;height:auto;margin:0 auto 6px"><h1 style="font-size:36px">Welcome to BFI</h1><p class="muted" style="margin-top:6px">Save designs, track your invitation and enquiries.</p></div>
    <div class="panel panel-gold">
      <div id="why"></div>
      <div class="tabs" role="tablist"><button role="tab" data-mode="signin" aria-selected="true">Login</button><button role="tab" data-mode="signup" aria-selected="false">Create account</button></div>
      <button class="btn btn-google btn-block" id="google" type="button">{GOOGLE} Continue with Google</button>
      <div class="or">or use email</div>
      <form class="form" id="auth-form" novalidate>
        <div class="field" id="name-field" hidden><label for="a-name">Full name</label><input id="a-name" name="name" autocomplete="name"></div>
        <div class="field"><label for="a-email">Email</label><input id="a-email" name="email" type="email" required autocomplete="email"></div>
        <div class="field"><label for="a-pass">Password</label><input id="a-pass" name="password" type="password" required autocomplete="current-password" minlength="8"></div>
        <button class="btn btn-primary btn-block" id="auth-submit" type="submit">Login</button>
      </form>
      <div id="auth-status" style="margin-top:14px" aria-live="polite"></div>
      <div class="row" style="justify-content:space-between;margin-top:14px;font-size:14.5px"><button class="linkbtn" id="magic" type="button">Email me a login link</button><button class="linkbtn" id="forgot" type="button">Forgot password?</button></div>
    </div>
    <p class="center muted" style="font-size:13px;margin-top:16px">By continuing you agree to be contacted about your invitation. We never share your details.</p>
  </div>
</div></section>'''
page("login", "Login · BFI Marwari Invitations", "Login or create your BFI account with email or Google.", LOGIN, None, bar=False)

# ---------------- Account ----------------
ACCT = '''
<section class="phead" style="padding:30px 0 26px"><div class="wrap"><h1 style="font-size:clamp(30px,5vw,44px)">My Account</h1></div></section>
<section class="sec" style="padding-top:28px"><div class="wrap"><div class="acct" id="account"><div class="panel skel" style="height:320px"></div><div class="panel skel" style="height:320px"></div></div></div></section>'''
page("account", "My Account · BFI Marwari Invitations", "Your saved invitations, favourites and enquiries.", ACCT, None, bar=False)

# ---------------- 404 ----------------
NF = f'''<section class="sec center"><div class="wrap"><p class="deva" lang="hi">॥ शुभ विवाह ॥</p><h1 style="margin-top:10px">This door is closed</h1><p class="lead" style="margin:14px auto 24px">The page you're looking for isn't here. Let's take you somewhere beautiful.</p><div class="row" style="justify-content:center"><a class="btn btn-primary" href="index.html">Go home</a><a class="btn btn-ghost" href="invitations.html">See invitations</a></div></div></section>
<div class="skyline" data-img="skyline.jpg" aria-hidden="true"></div>'''
page("404", "Page not found · BFI Marwari Invitations", "Page not found.", NF, None)

print("built", sorted(p.name for p in OUT.glob("*.html")))
