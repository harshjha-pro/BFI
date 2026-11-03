"""Four alternative homepage design concepts for BFI, same content,
different visual direction. Writes design/concepts/<name>.html.
Run:  python3 design/build_concepts.py
"""
from pathlib import Path

OUT = Path(__file__).parent / "concepts"
DESIGNS = [("royal-heritage", "Royal Heritage", "Premium · Luxury", "Aditi|Varun"), ("mandap-magic", "Mandap Magic", "Basic · Premium", "Pooja|Arjun"),
           ("golden-elegance", "Golden Elegance", "Luxury", "Nidhi|Sahil"), ("desert-dreams", "Desert Dreams", "Basic · Premium", "Riddhi|Karan")]
RITUALS = ["Ganesh puja", "Mayra / Bhaat", "Haldi", "Mehendi", "Mahila sangeet", "Baraat", "Phera", "Reception"]
STEPS = [("Choose a design", "Pick from our Marwari collection, or ask for bespoke."), ("Share your details", "A guided form for names, functions and photos."),
         ("Review your preview", "See it on your phone; send all changes in one go."), ("Share with family", "Get your link and QR code for every guest.")]
TIERS = [("Basic", "₹4,999", ["Curated Marwari design", "Names, dates, venue & RSVP", "1 revision round", "Ready in ~5 days"]),
         ("Premium", "₹11,999", ["Personalised design & photos", "Every function, countdown, maps", "2 revision rounds", "Ready in ~10 days"]),
         ("Luxury", "₹29,999", ["Fully custom, your story", "Multiple function pages", "Unlimited reasonable revisions", "Ready in ~21 days"])]
QUOTE = ("They understood every Marwari ritual we wanted. Our families loved the invitation.", "Aditi & Varun · Jaipur")
NAV = ["Designs", "Pricing", "How it works", "Real weddings", "FAQ"]
FONT_BASE = "https://fonts.googleapis.com/css2?family="


def doc(slug, title, fonts, css, body):
    (OUT / f"{slug}.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><link rel="icon" href="../assets/favicon-64.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONT_BASE}{fonts}&display=swap">
<style>
*{{box-sizing:border-box}} html{{-webkit-text-size-adjust:100%}} body{{margin:0}} img{{max-width:100%;display:block}}
.wrap{{max-width:1160px;margin:0 auto;padding:0 20px}} a{{color:inherit}}
.phone{{position:relative;margin:0 auto;width:230px;aspect-ratio:9/19;border-radius:32px;background:#2A1C17;padding:8px;box-shadow:0 24px 50px rgba(0,0,0,.25)}}
.phone .screen{{width:100%;height:100%;border-radius:25px;overflow:hidden}} .phone .screen svg{{width:100%;height:100%;display:block}}
.phone.sm{{width:150px;border-radius:24px;padding:6px}} .phone.sm .screen{{border-radius:19px}}
.nav-links{{display:none}} @media(min-width:980px){{.nav-links{{display:flex}} .m-only{{display:none!important}}}}
.sticky{{position:sticky;bottom:0;z-index:20;display:flex;gap:10px;padding:10px 16px calc(10px + env(safe-area-inset-bottom))}} .sticky a{{flex:1}}
@media(min-width:980px){{.sticky{{display:none}}}}
{css}
</style></head><body>
{body}
<script src="../assets/mock.js"></script></body></html>""")


phones = lambda size="sm": "".join(f'<div class="dcard"><div data-invite="{s}" data-size="{size}" data-names="{n}"></div><b>{t}</b><small>{ti}</small></div>' for s, t, ti, n in DESIGNS)

# ════════════════════════════════════════════════════════════════
# 1 · DARBAR — dark royal palace
# ════════════════════════════════════════════════════════════════
doc("darbar", "Concept 1 · Darbar · BFI", "Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Inter:wght@400;500;600&family=Tiro+Devanagari+Hindi", """
:root{--bg:#2A0009;--bg2:#3A000F;--deep:#460013;--gold:#D9B26A;--gold2:#F1DEB4;--ivory:#FFF6E6;--muted:#CDB28A}
body{background:radial-gradient(ellipse at 50% 0%,#5A0A1E 0%,var(--bg) 55%);background-color:var(--bg);color:var(--ivory);font:16px/1.6 Inter,sans-serif}
h1,h2,h3{font-family:"Cormorant Garamond",serif;font-weight:600;margin:0;color:var(--gold2);line-height:1.08}
.deva{font-family:"Tiro Devanagari Hindi",serif;color:var(--gold)}
.eyebrow{font:600 12px Inter;letter-spacing:.24em;text-transform:uppercase;color:var(--gold)}
header{display:flex;align-items:center;justify-content:space-between;padding:18px 20px;max-width:1240px;margin:0 auto;border-bottom:1px solid rgba(217,178,106,.25)}
header .brand{display:flex;gap:10px;align-items:center;text-decoration:none} header .brand img{width:44px;border-radius:10px} header .brand b{font:700 24px "Cormorant Garamond";color:var(--gold2);letter-spacing:.08em}
.nav-links{gap:30px;font-size:14px;letter-spacing:.12em;text-transform:uppercase} .nav-links a{text-decoration:none;color:var(--muted)}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 26px;border:1px solid var(--gold);font:600 13px Inter;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;color:var(--gold2)}
.btn.solid{background:linear-gradient(180deg,#E2BE78,#B8913F);color:#2A0009;border-color:#E2BE78}
.hero{text-align:center;padding:40px 0 70px}
.hero img.logo{width:min(560px,92vw);margin:0 auto}
.hero h1{font-size:clamp(34px,5vw,56px);margin-top:10px} .hero p{color:var(--muted);max-width:620px;margin:16px auto 28px;font-size:17px}
.orn{display:flex;align-items:center;gap:16px;justify-content:center;color:var(--gold);margin:0 auto;max-width:420px}
.orn::before,.orn::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,transparent,var(--gold))} .orn::after{transform:scaleX(-1)}
section{padding:70px 0;text-align:center} section h2{font-size:clamp(30px,4vw,44px);margin:10px 0 34px}
.arches{display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr))}
.dcard{border:1px solid rgba(217,178,106,.55);border-radius:140px 140px 10px 10px;padding:34px 16px 22px;background:linear-gradient(180deg,rgba(217,178,106,.08),transparent)}
.dcard b{display:block;font:600 24px "Cormorant Garamond";color:var(--gold2);margin-top:16px} .dcard small{color:var(--muted)}
.rituals{display:flex;flex-wrap:wrap;gap:12px;justify-content:center} .rituals span{border:1px solid rgba(217,178,106,.5);padding:10px 20px;color:var(--gold2);font:500 18px "Cormorant Garamond"}
.tiers{display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(min(100%,290px),1fr))}
.tier{border:1px solid rgba(217,178,106,.5);padding:34px 26px;background:rgba(70,0,19,.55);outline:1px solid rgba(217,178,106,.2);outline-offset:-8px}
.tier.hl{background:linear-gradient(180deg,#5A0A1E,#3A000F);border-color:var(--gold)} .tier h3{font-size:30px} .tier .amt{font:600 46px "Cormorant Garamond";color:var(--gold);margin:8px 0 14px}
.tier ul{list-style:none;padding:0;margin:0 0 24px;color:var(--muted);display:grid;gap:8px}
blockquote{font:italic 500 clamp(24px,3vw,34px)/1.4 "Cormorant Garamond";color:var(--gold2);max-width:780px;margin:0 auto}
footer{border-top:1px solid rgba(217,178,106,.25);padding:34px 20px;text-align:center;color:var(--muted);font-size:14px}
.sticky{background:rgba(42,0,9,.96);border-top:1px solid rgba(217,178,106,.3)} .sticky .btn{padding:0 10px;letter-spacing:.08em}
""", f"""
<header><a class="brand" href="#"><img src="../assets/logo-mark.png" alt=""><b>BFI</b></a><nav class="nav-links">{''.join(f'<a href="#">{n}</a>' for n in NAV)}</nav><a class="btn solid" href="#" style="min-height:42px;padding:0 18px">Enquire</a></header>
<div class="hero wrap"><img class="logo" src="../assets/logo-full.png" alt="BFI Marwari Invitations">
<div class="deva" style="font-size:18px">॥ श्री गणेशाय नमः ॥</div><h1>The royal way to invite your family</h1>
<p>Marwari wedding invitations crafted like heirlooms: every ritual, every elder's name, delivered to every phone.</p>
<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn solid" href="#">Explore designs</a><a class="btn" href="#">Chat on WhatsApp</a></div></div>
<div class="orn">✦</div>
<section><div class="wrap"><div class="eyebrow">The collection</div><h2>Designs fit for a darbar</h2><div class="arches">{phones()}</div></div></section>
<div class="orn">✦</div>
<section><div class="wrap"><div class="eyebrow">Every function</div><h2>Rituals we honour</h2><div class="rituals">{''.join(f'<span>{r}</span>' for r in RITUALS)}</div></div></section>
<div class="orn">✦</div>
<section><div class="wrap"><div class="eyebrow">Packages</div><h2>Choose your celebration</h2><div class="tiers">{''.join(f'<div class="tier {"hl" if n == "Premium" else ""}"><h3>{n}</h3><div class="amt">{p}</div><ul>{"".join(f"<li>{x}</li>" for x in f)}</ul><a class="btn {"solid" if n == "Premium" else ""}" href="#">Choose {n}</a></div>' for n, p, f in TIERS)}</div></div></section>
<section><div class="wrap"><div class="orn" style="margin-bottom:24px">✦</div><blockquote>“{QUOTE[0]}”</blockquote><p style="color:var(--muted)">{QUOTE[1]}</p></div></section>
<footer><img src="../assets/logo-full.png" alt="" style="width:200px;margin:0 auto 12px">© 2026 BFI — Marwari Invitations · Jaipur</footer>
<div class="sticky"><a class="btn solid" href="#">Explore designs</a><a class="btn" href="#">WhatsApp</a></div>
""")

# ════════════════════════════════════════════════════════════════
# 2 · KANKOTRI — ivory editorial, like a printed card
# ════════════════════════════════════════════════════════════════
doc("kankotri", "Concept 2 · Kankotri · BFI", "Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Lora:ital,wght@0,400;0,500;1,400&family=Tiro+Devanagari+Hindi", """
:root{--paper:#FBF5EA;--ink:#2B1A14;--maroon:#6E1F2E;--gold:#B08A44;--muted:#7A6556;--rule:#D9C8AC}
body{background:var(--paper);color:var(--ink);font:17px/1.7 Lora,serif;background-image:radial-gradient(rgba(176,138,68,.07) 1px,transparent 1px);background-size:22px 22px}
h1,h2,h3{font-family:"Playfair Display",serif;font-weight:600;margin:0;line-height:1.05}
.deva{font-family:"Tiro Devanagari Hindi",serif;color:var(--maroon)}
.num{font:italic 500 15px "Playfair Display";color:var(--gold)}
header{max-width:1160px;margin:0 auto;padding:22px 20px;display:flex;align-items:center;gap:20px;border-bottom:3px double var(--rule)}
header img{width:46px;border-radius:10px} header .w{font:600 22px "Playfair Display";letter-spacing:.1em;color:var(--maroon)} header .w small{display:block;font:italic 400 13px Lora;letter-spacing:0;color:var(--muted)}
.nav-links{margin-left:auto;margin-right:8px;gap:28px;font-style:italic} .nav-links a{text-decoration:none;color:var(--muted)}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 22px;font:600 15px "Playfair Display";text-decoration:none;border-bottom:2px solid var(--maroon);color:var(--maroon)}
.btn.fill{background:var(--maroon);color:var(--paper);border:0;border-radius:2px}
.hero{max-width:1160px;margin:0 auto;padding:56px 20px 70px;display:grid;gap:40px;align-items:center}
@media(min-width:980px){.hero{grid-template-columns:1.3fr .7fr}}
.hero h1{font-size:clamp(48px,8vw,104px);letter-spacing:-.02em} .hero h1 i{color:var(--maroon)}
.hero p{font-size:19px;color:var(--muted);max-width:560px;margin:22px 0 30px}
.hero .card{transform:rotate(3deg);background:#fff;padding:18px;box-shadow:0 30px 60px rgba(43,26,20,.15);border:1px solid var(--rule);justify-self:center}
.row{display:flex;gap:18px;flex-wrap:wrap;align-items:center}
section{max-width:1160px;margin:0 auto;padding:64px 20px;border-top:1px solid var(--rule)}
.sh{display:grid;gap:14px;margin-bottom:34px} @media(min-width:980px){.sh{grid-template-columns:180px 1fr}}
.sh h2{font-size:clamp(34px,5vw,58px)}
.dgrid{display:grid;gap:30px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr))}
.dcard{text-align:center} .dcard b{display:block;font:600 22px "Playfair Display";margin-top:14px} .dcard small{font-style:italic;color:var(--muted)}
.list{columns:2;column-gap:40px;font:500 26px/2 "Playfair Display";font-style:italic;color:var(--maroon)} @media(min-width:980px){.list{columns:4}}
.steps{display:grid;gap:28px;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr))}
.steps div b{display:block;font:600 22px "Playfair Display";margin:6px 0} .steps div p{margin:0;color:var(--muted)}
.ptable{width:100%;border-collapse:collapse} .ptable td{padding:22px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
.ptable .n{font:600 30px "Playfair Display"} .ptable .p{font:600 30px "Playfair Display";color:var(--maroon);text-align:right;white-space:nowrap} .ptable .f{color:var(--muted)}
@media(max-width:700px){.ptable td{display:block;padding:6px 0;border:0;text-align:left!important} .ptable tr{display:block;padding:16px 0;border-bottom:1px solid var(--rule)}}
blockquote{font:italic 500 clamp(28px,4vw,46px)/1.3 "Playfair Display";margin:0}
footer{background:#3A0010;color:#EBD9BC;padding:44px 20px;text-align:center} footer img{width:210px;margin:0 auto 12px}
.sticky{background:rgba(251,245,234,.97);border-top:1px solid var(--rule)}
""", f"""
<header><img src="../assets/logo-mark.png" alt=""><div class="w">BFI<small>Marwari Invitations</small></div><nav class="nav-links">{''.join(f'<a href="#">{n}</a>' for n in NAV)}</nav><a class="btn fill" style="margin-left:auto;min-height:40px" href="#">Enquire</a></header>
<div class="hero"><div><div class="deva" style="font-size:18px">॥ श्री गणेशाय नमः ॥</div><h1>Your wedding, <i>written</i> the Marwari way.</h1>
<p>The care of a traditional kankotri, delivered as an invitation your family opens on their phones.</p>
<div class="row"><a class="btn fill" href="#">Explore designs</a><a class="btn" href="#">Chat on WhatsApp</a></div></div>
<div class="card"><div data-invite="mandap-magic" data-names="Pooja|Arjun"></div></div></div>
<section><div class="sh"><span class="num">No. 01 — Designs</span><h2>Signature designs, each personalised</h2></div><div class="dgrid">{phones()}</div></section>
<section><div class="sh"><span class="num">No. 02 — Rituals</span><h2>Every function, given its due</h2></div><div class="list">{''.join(f'<div>{r}</div>' for r in RITUALS)}</div></section>
<section><div class="sh"><span class="num">No. 03 — Process</span><h2>Four unhurried steps</h2></div><div class="steps">{''.join(f'<div><span class="num">0{i+1}</span><b>{t}</b><p>{d}</p></div>' for i, (t, d) in enumerate(STEPS))}</div></section>
<section><div class="sh"><span class="num">No. 04 — Packages</span><h2>Clear prices</h2></div><table class="ptable">{''.join(f'<tr><td class="n">{n}</td><td class="f">{" · ".join(f)}</td><td class="p">{p}</td></tr>' for n, p, f in TIERS)}</table>
<div class="row" style="margin-top:26px"><a class="btn fill" href="#">Plan my invitation</a></div></section>
<section><span class="num">No. 05 — Kind words</span><blockquote style="margin-top:14px">“{QUOTE[0]}”</blockquote><p class="num" style="margin-top:14px">{QUOTE[1]}</p></section>
<footer><img src="../assets/logo-full.png" alt="">© 2026 BFI — Marwari Invitations · Jaipur</footer>
<div class="sticky"><a class="btn fill" href="#">Explore designs</a><a class="btn" href="#" style="justify-content:center">WhatsApp</a></div>
""")

# ════════════════════════════════════════════════════════════════
# 3 · GULABI — modern luxury, bento layout
# ════════════════════════════════════════════════════════════════
doc("gulabi", "Concept 3 · Gulabi · BFI", "DM+Serif+Display:ital@0;1&family=DM+Sans:wght@400;500;600;700&family=Tiro+Devanagari+Hindi", """
:root{--pearl:#FAF7F2;--burg:#722F42;--champ:#D8BD8A;--rose:#EAD3CD;--rose2:#D9B7B0;--char:#302A2A;--muted:#7B6B6B}
body{background:var(--pearl);color:var(--char);font:16px/1.6 "DM Sans",sans-serif}
h1,h2,h3{font-family:"DM Serif Display",serif;font-weight:400;margin:0;line-height:1.05}
.deva{font-family:"Tiro Devanagari Hindi",serif;color:var(--burg)}
header{max-width:1200px;margin:16px auto 0;padding:10px 12px 10px 16px;display:flex;align-items:center;gap:18px;background:#fff;border-radius:999px;box-shadow:0 8px 30px rgba(114,47,66,.08);width:calc(100% - 32px)}
header img{width:40px;border-radius:50%} header b{font:400 22px "DM Serif Display";color:var(--burg)}
.nav-links{margin-left:auto;gap:6px} .nav-links a{text-decoration:none;padding:8px 14px;border-radius:999px;font-weight:500;color:var(--muted)} .nav-links a:first-child{background:var(--rose);color:var(--burg)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:50px;padding:0 24px;border-radius:999px;font:600 15px "DM Sans";text-decoration:none;background:#fff;color:var(--burg);border:1.5px solid var(--rose2)}
.btn.dark{background:var(--burg);color:#fff;border-color:var(--burg)}
.hero{max-width:1200px;margin:0 auto;padding:28px 16px;display:grid;gap:16px}
@media(min-width:980px){.hero{grid-template-columns:1.25fr .75fr;grid-template-rows:auto auto}}
.tile{border-radius:32px;padding:34px;position:relative;overflow:hidden}
.t1{background:linear-gradient(135deg,#FFF 0%,var(--rose) 100%)} .t1 h1{font-size:clamp(42px,6vw,78px);color:var(--burg)} .t1 h1 i{color:var(--char)} .t1 p{font-size:18px;color:var(--muted);max-width:520px;margin:18px 0 26px}
.t1::after{content:"";position:absolute;right:-80px;bottom:-80px;width:280px;height:280px;border-radius:50%;background:var(--rose2);opacity:.35}
.t2{background:var(--burg);display:grid;place-items:center;min-height:420px} @media(min-width:980px){.t2{grid-row:span 2}}
.t2 .fan{position:relative;width:300px;height:380px} .t2 .fan>div{position:absolute;top:10px} .t2 .fan>div:nth-child(1){left:0;transform:rotate(-10deg)} .t2 .fan>div:nth-child(2){right:0;transform:rotate(10deg)} .t2 .fan>div:nth-child(3){left:72px;top:0;z-index:2}
.t3{background:var(--champ);display:flex;align-items:center;gap:18px;flex-wrap:wrap} .t3 b{font:400 34px "DM Serif Display";color:var(--burg)} .t3 span{color:var(--char)}
section{max-width:1200px;margin:0 auto;padding:46px 16px}
.h{display:flex;justify-content:space-between;align-items:end;gap:14px;flex-wrap:wrap;margin-bottom:22px} .h h2{font-size:clamp(32px,4vw,52px)}
.pill{display:inline-block;padding:6px 14px;border-radius:999px;background:var(--rose);color:var(--burg);font-weight:600;font-size:13px}
.bento{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr))}
.dcard{background:#fff;border-radius:28px;padding:24px 16px;text-align:center;box-shadow:0 6px 24px rgba(114,47,66,.06)} .dcard b{display:block;font:400 24px "DM Serif Display";margin-top:14px} .dcard small{color:var(--muted)}
.rit{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(min(46%,200px),1fr))} .rit div{background:#fff;border-radius:20px;padding:18px 20px;font-weight:600;display:flex;justify-content:space-between} .rit div::after{content:"→";color:var(--rose2)}
.tiers{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr))}
.tier{background:#fff;border-radius:32px;padding:30px} .tier.hl{background:var(--burg);color:#fff} .tier h3{font-size:30px} .tier .amt{font:700 40px "DM Sans";margin:8px 0 14px;letter-spacing:-.02em}
.tier ul{padding:0;list-style:none;display:grid;gap:8px;margin:0 0 22px} .tier li::before{content:"● ";color:var(--rose2)} .tier.hl li::before{color:var(--champ)}
.quote{background:var(--rose);border-radius:32px;padding:44px;text-align:center} .quote blockquote{margin:0;font:400 clamp(26px,3vw,40px)/1.3 "DM Serif Display";color:var(--burg)}
footer{max-width:1200px;margin:20px auto 30px;background:var(--burg);border-radius:32px;padding:34px;color:#F3E2D8;display:flex;gap:20px;align-items:center;justify-content:space-between;flex-wrap:wrap;width:calc(100% - 32px)} footer img{width:180px}
.sticky{background:rgba(250,247,242,.96)}
""", f"""
<header><img src="../assets/logo-mark.png" alt=""><b>BFI</b><nav class="nav-links">{''.join(f'<a href="#">{n}</a>' for n in NAV)}</nav><a class="btn dark" style="margin-left:auto;min-height:42px" href="#">Enquire</a></header>
<div class="hero">
  <div class="tile t1"><span class="pill">Marwari wedding invitations</span><h1 style="margin-top:16px">Modern invites, <i>timeless</i> traditions.</h1><p>Elegant digital invitations with every ritual and every name, made for how families share today.</p><div style="display:flex;gap:10px;flex-wrap:wrap;position:relative;z-index:1"><a class="btn dark" href="#">Explore designs</a><a class="btn" href="#">Chat on WhatsApp</a></div></div>
  <div class="tile t2"><div class="fan"><div data-invite="mandap-magic" data-size="sm" data-names="Pooja|Arjun"></div><div data-invite="desert-dreams" data-size="sm" data-names="Riddhi|Karan"></div><div data-invite="royal-heritage" data-size="sm"></div></div></div>
  <div class="tile t3"><b>3 of 5</b><span>invitation slots open this week · ready in as little as 5 days</span></div>
</div>
<section><div class="h"><h2>Designs</h2><a class="btn" href="#">View all</a></div><div class="bento">{phones()}</div></section>
<section><div class="h"><h2>Every ritual</h2></div><div class="rit">{''.join(f'<div>{r}</div>' for r in RITUALS)}</div></section>
<section><div class="h"><h2>Pricing</h2><span class="pill">No hidden fees</span></div><div class="tiers">{''.join(f'<div class="tier {"hl" if n == "Premium" else ""}"><h3>{n}</h3><div class="amt">{p}</div><ul>{"".join(f"<li>{x}</li>" for x in f)}</ul><a class="btn {"" if n == "Premium" else "dark"}" href="#">Choose {n}</a></div>' for n, p, f in TIERS)}</div></section>
<section><div class="quote"><blockquote>“{QUOTE[0]}”</blockquote><p style="color:var(--muted)">{QUOTE[1]}</p></div></section>
<footer><img src="../assets/logo-full.png" alt=""><div>© 2026 BFI — Marwari Invitations<br>Jaipur · hello@bfi-invitations.in</div></footer>
<div class="sticky"><a class="btn dark" href="#">Explore designs</a><a class="btn" href="#">WhatsApp</a></div>
""")

# ════════════════════════════════════════════════════════════════
# 4 · UTSAV — festive celebration
# ════════════════════════════════════════════════════════════════
TORAN = "".join(f'<circle cx="{x}" cy="{14 + (6 if (x // 30) % 2 else 0)}" r="9" fill="{"#D99A35" if (x // 30) % 2 else "#E8B04B"}"/><path d="M{x} 23v18" stroke="#285C46" stroke-width="2"/><path d="M{x - 6} 41 {x} 52 {x + 6} 41z" fill="#285C46"/>' for x in range(15, 1500, 30))
doc("utsav", "Concept 4 · Utsav · BFI", "Rozha+One&family=Mukta:wght@400;500;600;700&family=Tiro+Devanagari+Hindi", f"""
:root{{--cream:#FFF3DB;--verm:#B94332;--saff:#D99A35;--emer:#285C46;--gold:#B99A55;--ink:#3A2116;--muted:#7A5A44}}
body{{background:var(--cream);color:var(--ink);font:17px/1.6 Mukta,sans-serif}}
h1,h2,h3{{font-family:"Rozha One",serif;font-weight:400;margin:0;line-height:1.05}}
.deva{{font-family:"Tiro Devanagari Hindi",serif;color:var(--emer)}}

header{{background:var(--verm);color:#FFF3DB}} header .wrap{{display:flex;align-items:center;gap:18px;padding-top:14px;padding-bottom:14px}}
header img{{width:46px;border-radius:12px;border:2px solid var(--saff)}} header b{{font:400 28px "Rozha One"}}
.nav-links{{margin-left:auto;gap:24px;font-weight:600}} header .btn.s{{margin-left:auto}} @media(min-width:980px){{header .btn.s{{margin-left:8px}}}} .nav-links a{{text-decoration:none;color:#FFE7C2}}
.btn{{display:inline-flex;align-items:center;justify-content:center;min-height:50px;padding:0 24px;border-radius:12px;font:700 16px Mukta;text-decoration:none;border:2px solid var(--emer);color:var(--emer);background:#fff}}
.btn.v{{background:var(--emer);color:#fff}} .btn.s{{background:var(--saff);border-color:var(--saff);color:var(--ink)}}
.dots{{background-color:var(--verm);background-image:radial-gradient(circle,#FFE7C2 2px,transparent 2.6px),radial-gradient(circle,#F2B35A 1.6px,transparent 2.2px);background-size:22px 22px,22px 22px;background-position:0 0,11px 11px}}
.hero{{padding:44px 0 60px;position:relative}} .hero .wrap{{display:grid;gap:34px;align-items:center}} @media(min-width:980px){{.hero .wrap{{grid-template-columns:1.15fr .85fr}}}}
.hero h1{{font-size:clamp(44px,6.5vw,80px);color:var(--verm)}} .hero h1 span{{color:var(--emer)}} .hero p{{font-size:19px;color:var(--muted);max-width:560px;margin:16px 0 26px}}
.frame{{background:#fff;border-radius:24px;padding:22px;border:3px solid var(--saff);box-shadow:8px 8px 0 var(--verm);justify-self:center}}
.scallop{{height:22px;background:radial-gradient(circle at 11px 0,transparent 11px,var(--emer) 11.5px) repeat-x;background-size:22px 22px}}
section{{padding:62px 0}} section h2{{font-size:clamp(34px,4.5vw,56px);color:var(--verm);text-align:center;margin-bottom:30px}}
.green{{background:var(--emer);color:#FFF3DB}} .green h2{{color:var(--saff)}}
.dgrid{{display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr))}}
.dcard{{background:#fff;border-radius:20px;padding:22px 16px;text-align:center;border:2px dashed var(--saff)}} .dcard b{{display:block;font:400 24px "Rozha One";color:var(--verm);margin-top:14px}} .dcard small{{color:var(--muted)}}
.rit{{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}} .rit span{{background:var(--saff);color:var(--ink);padding:10px 20px;border-radius:999px;font-weight:700}} .rit span:nth-child(3n+2){{background:#FFE7C2}} .rit span:nth-child(3n){{background:var(--verm);color:#fff}}
.tiers{{display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(min(100%,290px),1fr))}}
.tier{{background:#fff;border-radius:22px;padding:30px;border:3px solid var(--saff)}} .tier.hl{{border-color:var(--verm);box-shadow:8px 8px 0 var(--emer)}} .tier h3{{font-size:32px;color:var(--emer)}} .tier .amt{{font:400 44px "Rozha One";color:var(--verm);margin:6px 0 12px}}
.tier ul{{padding:0;list-style:none;display:grid;gap:8px;margin:0 0 22px}} .tier li::before{{content:"✿ ";color:var(--saff)}}
blockquote{{font:400 clamp(26px,3vw,38px)/1.35 "Rozha One";text-align:center;max-width:820px;margin:0 auto;color:#FFE7C2}}
footer{{background:var(--ink);color:#F2D9B0;padding:36px 20px;text-align:center}} footer img{{width:200px;margin:0 auto 12px}}
.sticky{{background:rgba(255,243,219,.97);border-top:2px solid var(--saff)}}
""", f"""
<header><div class="wrap"><img src="../assets/logo-mark.png" alt=""><b>BFI</b><nav class="nav-links">{''.join(f'<a href="#">{n}</a>' for n in NAV)}</nav><a class="btn s" style="min-height:42px" href="#">Enquire</a></div></header>
<div style="height:56px;overflow:hidden;background:var(--cream)"><svg width="1500" height="56" viewBox="0 0 1500 56"><path d="M0 8h1500" stroke="#B94332" stroke-width="4"/>{TORAN}</svg></div>
<div class="hero"><div class="wrap"><div><div class="deva" style="font-size:20px">॥ शुभ विवाह ॥</div><h1>Celebrate the <span>Marwari</span> way!</h1>
<p>Bright, joyful digital invitations for every function, from Haldi to Phera, shared with every guest in one tap.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn v" href="#">Explore designs</a><a class="btn" href="#">Chat on WhatsApp</a></div></div>
<div class="frame"><div data-invite="marwari-classic" data-names="Shruti|Yash"></div></div></div></div>
<div class="dots" style="height:46px"></div>
<section><div class="wrap"><h2>Our designs</h2><div class="dgrid">{phones()}</div></div></section>
<div class="scallop"></div>
<section class="green"><div class="wrap"><h2>Every function, every rasam</h2><div class="rit">{''.join(f'<span>{r}</span>' for r in RITUALS)}</div></div></section>
<section><div class="wrap"><h2>Packages</h2><div class="tiers">{''.join(f'<div class="tier {"hl" if n == "Premium" else ""}"><h3>{n}</h3><div class="amt">{p}</div><ul>{"".join(f"<li>{x}</li>" for x in f)}</ul><a class="btn {"v" if n == "Premium" else ""}" href="#">Choose {n}</a></div>' for n, p, f in TIERS)}</div></div></section>
<section class="dots" style="padding:56px 0"><div class="wrap"><blockquote>“{QUOTE[0]}”</blockquote><p style="text-align:center;color:#FFE7C2">{QUOTE[1]}</p></div></section>
<footer><img src="../assets/logo-full.png" alt="">© 2026 BFI — Marwari Invitations · Jaipur</footer>
<div class="sticky"><a class="btn v" href="#">Explore designs</a><a class="btn" href="#">WhatsApp</a></div>
""")

print("written:", sorted(p.name for p in OUT.glob("*.html")))
