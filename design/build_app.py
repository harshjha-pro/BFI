"""Generates the app mockups (client portal + studio) in design/app/.
Run:  python3 design/build_app.py
"""
from pathlib import Path

OUT = Path(__file__).parent / "app"
FONTS = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Inter:wght@400;500;600;700&family=Tiro+Devanagari+Hindi&display=swap"
I = {
    "home": '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    "folder": '<path d="M3 6.5A1.5 1.5 0 0 1 4.5 5H9l2 2.5h8.5A1.5 1.5 0 0 1 21 9v9.5a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5z"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.8 7L4 20.5l1.5-4.6A8 8 0 1 1 21 12z"/>',
    "cog": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9 7 7M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>',
    "inbox": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.5 5h13L22 12v7a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-7z"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.4 3.2-5.5 6.5-5.5s5.9 2.1 6.5 5.5"/>',
    "rupee": '<path d="M6 4h12M6 9h12M9 4c6 0 6 10 0 10H6l8 7"/>',
    "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-9 9"/>',
    "mega": '<path d="M3 11v3h4l7 4V7L7 11z"/><path d="M18 9a4 4 0 0 1 0 6"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "palette": '<circle cx="12" cy="12" r="9"/><circle cx="8" cy="10" r="1"/><circle cx="12" cy="7" r="1"/><circle cx="16" cy="10" r="1"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 3 3 5-6"/>',
    "qr": '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 14h3v3h-3zM20 20h1"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/>',
}
svg = lambda k: f'<svg viewBox="0 0 24 24">{I[k]}</svg>'


def shell(slug, title, nav, active, who, body, tabbar):
    side = "".join(f'<a class="nav {"on" if k == active else ""}" href="#">{svg(ic)}{l}</a>' for k, l, ic in nav)
    tabs = "".join(f'<a class="{"on" if k == active else ""}" href="#">{svg(ic)}{l}</a>' for k, l, ic in tabbar)
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><link rel="icon" href="../assets/favicon-64.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}"><link rel="stylesheet" href="../assets/bfi.css"><link rel="stylesheet" href="../assets/app.css"></head>
<body class="app"><div class="app-shell">
<aside class="side"><a class="logo" href="#"><img src="../assets/logo-mark.png" alt=""><span><b>BFI</b><small>Marwari Invitations</small></span></a>{side}<div class="grow"></div>
<div class="me"><span class="avatar">{"".join(w[0] for w in who.split()[:2])}</span>{who}</div></aside>
<div class="main"><header class="topbar"><a class="m-logo" href="#"><img src="../assets/logo-mark.png" alt=""><b>BFI</b></a><div class="grow"></div>
<div class="search">⌕ Search</div><div class="who"><span class="avatar">{"".join(w[0] for w in who.split()[:2])}</span><span class="hide-m">{who}</span></div></header>
<main class="content">{body}</main></div></div>
<nav class="tabbar">{tabs}</nav>
<script src="../assets/mock.js"></script></body></html>"""
    (OUT / f"{slug}.html").write_text(html)


CLIENT_NAV = [("home", "Home", "home"), ("dash", "Dashboard", "grid"), ("projects", "My Projects", "folder"), ("msgs", "Messages", "chat"), ("settings", "Settings", "cog")]
CLIENT_TABS = CLIENT_NAV

# ── Client · Dashboard ────────────────────────────────────
shell("client-dashboard", "Client dashboard · BFI", CLIENT_NAV, "dash", "Aditi Kothari", """
<div class="page-title"><div><div class="deva" style="margin-bottom:6px">॥ शुभ विवाह ॥</div><h1>Welcome, Simran & Rohan</h1><p>Brother's wedding · your invitation journey at a glance</p></div></div>
<div class="chips" style="margin-bottom:16px"><a class="chip on" href="#">Brother's wedding</a><a class="chip" href="#">Aditi & Varun · delivered</a></div>
<div class="grid-2">
  <div style="display:grid;gap:16px">
    <div class="panel"><span class="small muted">Project status</span><div class="panel-head" style="margin:6px 0 10px"><h3>Collecting details</h3><b style="font:600 26px var(--serif)">29%</b></div><div class="progress"><i style="width:29%"></i></div><p class="small muted" style="margin:10px 0 0">We're gathering names, photos and venue details.</p></div>
    <div class="panel need"><div class="eyebrow">What we need from you</div><h3>Fill in your details and upload your photos</h3><p class="muted" style="margin:8px 0 14px">7 items left: couple photos, venue, family names…</p><a class="btn primary" href="#">Fill in your details</a></div>
    <div class="panel"><h3 style="margin-bottom:12px">Progress</h3><div class="steps-h"><div class="now"><i>1</i>Design</div><div><i>2</i>Your review</div><div><i>3</i>Final checks</div><div><i>4</i>Delivery</div></div></div>
  </div>
  <div style="display:grid;gap:16px">
    <div class="panel"><h3 style="margin-bottom:12px">Quick actions</h3><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><a class="btn secondary sm" href="#">Upload photos</a><a class="btn secondary sm" href="#">Details</a><a class="btn secondary sm" href="#">Pay balance</a><a class="btn secondary sm" href="#">Message</a></div></div>
    <div class="panel"><div class="panel-head"><h3>Latest message</h3><a class="small" href="#">Open</a></div><div class="bub" style="max-width:100%"><div class="w">Kunal · Design team</div>Namaste Aditi ji! Please add Rohan & Simran's photos and the function list.<div class="tm">2d ago</div></div></div>
    <div class="panel"><div class="panel-head" style="margin:0"><h3>Payment</h3><span class="status warn">₹6,498 due</span></div></div>
  </div>
</div>""", CLIENT_TABS)

# ── Client · My project ───────────────────────────────────
shell("client-project", "My project · BFI", CLIENT_NAV, "projects", "Nidhi Lohia", """
<div class="page-title"><div><div class="small"><a href="#">← My projects</a></div><h1>Lohia Wedding</h1><p>Nidhi & Sahil · Luxury / Bespoke · delivery 1 Nov</p></div><span class="status gold">Your review</span></div>
<nav class="tabs"><a href="#">Overview</a><a href="#">Details</a><a href="#">Uploads</a><a class="on" href="#">Preview & changes</a><a href="#">Payment</a></nav>
<div class="grid-2 gp">
  <div class="arch" style="width:290px"><div data-invite="golden-elegance" data-names="Nidhi|Sahil" data-date="25 · 11 · 2026" data-city="Kolkata"></div></div>
  <div style="display:grid;gap:16px">
    <div class="panel"><div class="panel-head" style="margin:0"><div><b>Revision rounds</b><div class="small muted">Unlimited (reasonable)</div></div><span class="status ok">Round 1</span></div></div>
    <div class="panel"><h3>Your changes</h3><p class="small muted" style="margin:6px 0 12px">Add every change, then send them together as one round.</p>
      <div class="list"><div class="it"><span class="status">Couple & family names</span><div class="g">Nani's name should be Smt. Kamla Devi Jain</div></div><div class="it"><span class="status">Events & timings</span><div class="g">Sangeet starts at 7:30 pm, not 7</div></div></div>
      <div class="form" style="margin-top:12px"><select class="input"><option>Where on the invitation: Cover</option></select><textarea class="input" placeholder="What should change"></textarea><div class="row"><a class="btn secondary sm" href="#">+ Add change</a><a class="btn primary sm" href="#">Send 2 changes as round 2</a></div></div></div>
    <div class="panel"><h3>Happy with the design?</h3><p class="small muted" style="margin:6px 0 12px">Approve and we'll run our final quality check.</p><a class="btn secondary" href="#">Approve design</a></div>
  </div>
</div>""", CLIENT_TABS)

# ── Client · Messages ─────────────────────────────────────
shell("client-messages", "Messages · BFI", CLIENT_NAV, "msgs", "Nidhi Lohia", """
<div class="page-title"><div><h1>Messages</h1><p>One conversation with the studio. Type @ to tag the Design team, Studio admin or QA team.</p></div></div>
<div class="chat">
  <div class="head"><img src="../assets/logo-mark.png" alt="" style="width:36px;border-radius:9px"><div><b>BFI studio</b><div class="small muted">Design team · Studio admin · QA team</div></div></div>
  <div class="msgs">
    <div class="bub"><div class="w">Studio Admin</div>Namaste Nidhi ji, your balance invoice is in the Payment section whenever you're ready.<div class="tm">25 Oct, 4:00 pm</div></div>
    <div class="bub"><div class="w">Sneha · Design team</div>We've updated the design with your feedback. Please take a look.<div class="tm">28 Oct, 10:00 am</div></div>
    <div class="bub me"><span class="tag">@Design team</span> Looks great! Just one small change in the date font.<div class="tm">28 Oct, 12:00 pm</div></div>
    <div class="bub"><div class="w">Sneha · Design team</div>Noted! Updating now. 🙏<div class="tm">28 Oct, 1:00 pm</div></div>
  </div>
  <div class="composer">
    <div class="pop"><div><span class="avatar" style="width:28px;height:28px;font-size:11px">QT</span>@QA team</div></div>
    <div class="tags"><span>@Design team</span><span>@Studio admin</span><span>@QA team</span></div>
    <div class="box"><input class="input" value="Please double-check the venue spelling @qa"><a class="btn primary" href="#">Send</a></div>
  </div>
</div>""", CLIENT_TABS)

STUDIO_NAV = [("dash", "Dashboard", "home"), ("leads", "Leads & Sales", "inbox"), ("projects", "Projects", "folder"), ("people", "People", "users"), ("finance", "Finance", "rupee"),
              ("content", "Content & Assets", "image"), ("mkt", "Marketing", "mega"), ("out", "Outreach", "users"), ("metrics", "Metrics", "chart"), ("settings", "Settings", "cog")]
STUDIO_TABS = [("dash", "Dashboard", "home"), ("leads", "Leads", "inbox"), ("projects", "Projects", "folder"), ("people", "People", "users"), ("more", "More", "grid")]

# ── Studio · Admin dashboard ──────────────────────────────
pts = [(0, 0), (1, 0), (2, 0), (3, 6.5), (4, 6.5), (5, 38.7)]
path = " ".join(f"{'M' if i == 0 else 'L'}{50 + x * 106} {170 - y * 3.8:.0f}" for i, (x, y) in enumerate(pts))
chart = f"""<svg viewBox="0 0 600 200"><g stroke="#E6D8C2" stroke-dasharray="3 3">{''.join(f'<line x1="50" x2="590" y1="{y}" y2="{y}"/>' for y in (20, 95, 170))}</g>
<path d="{path} L580 170 L50 170Z" fill="#641E2B" opacity=".08"/><path d="{path}" fill="none" stroke="#641E2B" stroke-width="2.4"/>
{''.join(f'<circle cx="{50 + x * 106}" cy="{170 - y * 3.8:.0f}" r="4" fill="#FFFDF8" stroke="#C6A15B" stroke-width="2"/>' for x, y in pts)}
{''.join(f'<text x="{50 + i * 106}" y="192" font-size="11" fill="#6E5A4E" text-anchor="middle">{m}</text>' for i, m in enumerate(["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]))}</svg>"""
shell("studio-dashboard", "Studio dashboard · BFI", STUDIO_NAV, "dash", "Studio Admin", f"""
<div class="page-title"><div><h1>Good evening, Admin</h1><p>Here's what's happening with your studio today.</p></div><a class="btn primary" href="#">+ Add lead</a></div>
<div class="kpis"><div class="kpi"><span>Total leads</span><b>12</b><em>+9 in last 30 days</em></div><div class="kpi"><span>Converted</span><b>7</b><em>+3 in last 30 days</em></div><div class="kpi"><span>Active projects</span><b>6</b><em style="color:var(--danger)">1 overdue</em></div><div class="kpi"><span>Revenue (MTD)</span><b>₹38.7K</b><em>+474%</em></div></div>
<div class="panel" style="margin-bottom:16px"><div class="panel-head" style="margin-bottom:8px"><div><h3>Booking capacity</h3><div class="small muted">Shown to clients on the website, booking page and enquiry form</div></div><div class="row"><b style="font:600 26px var(--serif)">2/5</b><span class="status ok">3 slots left</span></div></div>
<div style="display:flex;gap:4px">{''.join(f'<i style="flex:1;height:8px;border-radius:4px;background:{"#641E2B" if i < 2 else "#E9DCC8"}"></i>' for i in range(5))}</div></div>
<div class="grid-2">
  <div class="panel"><div class="panel-head"><h3>Revenue trend</h3><span class="small muted">Last 6 months</span></div><div class="chart">{chart}</div></div>
  <div class="panel"><div class="panel-head"><h3>Needs attention</h3><span class="status warn">3</span></div><div class="list">
    <div class="it"><span class="status bad">Overdue</span><div class="g"><b>Saraf Wedding</b><span>Overdue by 1 day · In design</span></div></div>
    <div class="it"><span class="status warn">QA</span><div class="g"><b>Birla Wedding</b><span>Waiting for QA</span></div></div>
    <div class="it"><span class="status gold">Sign-off</span><div class="g"><b>Maheshwari Wedding</b><span>Awaiting sign-off · ₹6,749 due</span></div></div></div></div>
</div>
<div class="panel pad0" style="margin-top:16px"><div class="panel-head"><h3>Recent projects</h3><a class="small" href="#">View all</a></div>
<table class="t"><thead><tr><th>Project</th><th class="hide-m">Stage</th><th class="hide-m">Due</th><th>Status</th></tr></thead><tbody>
<tr><td><b>Kothari · Brother's wedding</b><span class="s">Simran & Rohan</span></td><td class="hide-m">Collecting details</td><td class="hide-m">15 Nov</td><td><span class="status ok">On track</span></td></tr>
<tr><td><b>Bhandari Wedding</b><span class="s">Kavya & Aditya</span></td><td class="hide-m">Scope approved</td><td class="hide-m">24 Nov</td><td><span class="status ok">On track</span></td></tr>
<tr><td><b>Maheshwari Wedding</b><span class="s">Pooja & Arjun</span></td><td class="hide-m">Final approval</td><td class="hide-m">5 Nov</td><td><span class="status warn">Due in 2d</span></td></tr>
<tr><td><b>Saraf Wedding</b><span class="s">Riddhi & Karan</span></td><td class="hide-m">In design</td><td class="hide-m">2 Nov</td><td><span class="status bad">Overdue 1d</span></td></tr>
</tbody></table></div>""", STUDIO_TABS)

# ── Studio · Leads ────────────────────────────────────────
leads = [("Ritika Mundhra", "Bikaner · Direct outreach", "Contacted", "warn"), ("Ishita Maheshwari", "Kolkata · Instagram", "New", ""), ("Kavya & Aditya", "Udaipur · LENSVOWS", "New", ""),
         ("Rohan Khandelwal", "Jaipur · SHUBH12", "Contacted", "warn"), ("Neha Soni", "Jaipur · Past client", "New", ""), ("Priya Sethia", "Mumbai · Google", "Quoted", "gold"), ("Megha Rathi", "Delhi · Pinterest", "Lost", "bad")]
shell("studio-leads", "Leads & Sales · BFI", STUDIO_NAV, "leads", "Studio Admin", f"""
<div class="page-title"><div><h1>Leads & Sales</h1><p>Manage your leads, pipeline and quotes.</p></div><a class="btn primary" href="#">+ Add lead</a></div>
<div class="panel pad0"><nav class="tabs" style="padding:0 14px;margin:0"><a class="on" href="#">All (12)</a><a href="#">New (4)</a><a href="#">Contacted (3)</a><a href="#">Quoted (1)</a><a href="#">Converted (2)</a><a href="#">Lost (3)</a></nav>
<div class="row" style="padding:14px"><div class="input" style="flex:1;min-height:42px;display:flex;align-items:center;color:var(--muted)">⌕ Search leads…</div><div class="input" style="width:150px;min-height:42px;display:flex;align-items:center">Source ▾</div></div>
<table class="t"><thead><tr><th>Name</th><th class="hide-m">Wedding</th><th>Stage</th><th class="hide-m">Owner</th></tr></thead><tbody>
{''.join(f'<tr><td><b>{n}</b><span class="s">{m}</span></td><td class="hide-m">{d}</td><td><span class="status {t}">{s}</span></td><td class="hide-m">{o}</td></tr>' for (n, m, s, t), d, o in zip(leads, ["20 Jan", "13 Jan", "28 Jan", "19 Dec", "17 Feb", "9 Dec", "29 Dec"], ["Vikram", "—", "Vikram", "Vikram", "Vikram", "Vikram", "—"]))}
</tbody></table></div>""", STUDIO_TABS)

# ── Studio · Design workspace (designer) ──────────────────
DES_NAV = [("projects", "My Projects", "folder"), ("intake", "Asset Intake", "check"), ("work", "Design Workspace", "palette"), ("load", "Workload", "list"), ("earn", "My Commission", "rupee"), ("settings", "Settings", "cog")]
shell("studio-design-workspace", "Design workspace · BFI", DES_NAV, "work", "Sneha Bansal", """
<div class="page-title"><div><h1>Design Workspace</h1><p>Lohia Wedding · Nidhi & Sahil · Luxury</p></div><span class="status gold">Client review</span></div>
<div class="grid-2 gp">
  <div class="arch" style="width:290px"><div data-invite="golden-elegance" data-names="Nidhi|Sahil" data-date="25 · 11 · 2026" data-city="Kolkata"></div></div>
  <div style="display:grid;gap:16px">
    <div class="panel"><h3 style="margin-bottom:10px">Versions</h3><div class="list"><div class="it"><span class="status gold">v2</span><div class="g"><b>Round 1 changes done</b><span>28 Oct · gold foil cover</span></div></div><div class="it"><span class="status">v1</span><div class="g"><b>Preview 1 — all event pages</b><span>26 Oct</span></div></div></div>
      <div class="form" style="margin-top:12px"><input class="input" placeholder="Preview link https://…"><a class="btn primary block" href="#">Create preview link</a></div></div>
    <div class="panel"><div class="panel-head"><h3>Revision log</h3><span class="small muted">Round 1 · 2 of 2 done</span></div>
      <div class="list"><div class="it">✓<div class="g"><b style="text-decoration:line-through;color:var(--muted)">Nani's name: Smt. Kamla Devi Jain</b></div></div><div class="it">✓<div class="g"><b style="text-decoration:line-through;color:var(--muted)">Sangeet starts at 7:30 pm</b></div></div></div></div>
    <div class="panel"><div class="panel-head" style="margin:0"><div><b>My commission on this order</b><div class="small muted">Designer · via vendor · 15%</div></div><b style="font:600 26px var(--serif);color:var(--maroon)">₹5,175</b></div></div>
  </div>
</div>""", [("projects", "Projects", "folder"), ("intake", "Intake", "check"), ("work", "Workspace", "palette"), ("earn", "Commission", "rupee"), ("settings", "Settings", "cog")])

# ── Partner · Referral home ───────────────────────────────
AFF_NAV = [("code", "Referral Code", "qr"), ("leads", "Leads & Projects", "list"), ("comm", "Commission", "rupee"), ("kit", "Marketing Kit", "image"), ("settings", "Settings", "cog")]
shell("partner-home", "Partner · BFI", AFF_NAV, "code", "Neha Daga", """
<div class="page-title"><div><h1>Your referral code</h1><p>Share it with couples; earn on every completed order.</p></div></div>
<div class="grid-2">
  <div style="display:grid;gap:16px">
    <div class="code-box"><div><div class="small" style="color:var(--gold-pale)">Your code</div><b>SHUBH12</b></div><a class="btn gold sm" href="#">Copy</a></div>
    <div class="panel"><div class="small muted" style="margin-bottom:6px">Your link</div><div class="input" style="min-height:44px;display:flex;align-items:center;font-size:14px">bfi-invitations.in/enquire/SHUBH12</div><div class="row" style="margin-top:12px"><a class="btn primary sm" href="#">Download marketing kit</a><a class="btn secondary sm" href="#">Share on WhatsApp</a></div></div>
  </div>
  <div style="display:grid;gap:16px">
    <div class="kpis" style="margin:0"><div class="kpi"><span>Referred leads</span><b>1</b></div><div class="kpi"><span>Orders</span><b>2</b></div><div class="kpi"><span>Total earned</span><b>₹2,025</b></div><div class="kpi"><span>Next payout</span><b style="font-size:24px">5 Dec</b></div></div>
    <div class="panel"><h3>Your rates</h3><p class="small muted" style="margin:6px 0 0">15% Basic · 15% Premium · 20% Luxury, paid on completed, fully paid orders.</p></div>
  </div>
</div>""", [("code", "Code", "qr"), ("leads", "Leads", "list"), ("comm", "Commission", "rupee"), ("kit", "Kit", "image"), ("settings", "Settings", "cog")])

print("written:", sorted(p.name for p in OUT.glob("*.html")))
