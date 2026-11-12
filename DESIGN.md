# DESIGN.md — BFI · Marwari Invitations

**Theme:** Royal Rajasthani Heritage meets Modern Luxury
**Version:** 1.0 · November 2026 · Status: ready to build in Figma, then code
**Owner:** BFI founder · **Logo:** `brand/` folder

> One premium brand across 7 pages. Ivory space, maroon voice, gold jewellery. Every decoration earns its place; nothing looks like generic SaaS.

---

## Contents
1. [Brand essence](#1-brand-essence)
2. [Design tokens](#2-design-tokens)
3. [Typography](#3-typography)
4. [Colour usage & accessibility](#4-colour-usage--accessibility)
5. [Cultural motifs: rules](#5-cultural-motifs-rules)
6. [Layout, grid & spacing](#6-layout-grid--spacing)
7. [Component library](#7-component-library)
8. [Pages (7)](#8-pages)
9. [Images & illustrations: full asset list with AI prompts](#9-images--illustrations)
10. [Invitation catalogue & filters](#10-invitation-catalogue--filters)
11. [UX, accessibility & motion](#11-ux-accessibility--motion)
12. [Tools: Figma AI vs Canva AI (recommendation)](#12-tools-figma-ai-vs-canva-ai)
13. [Build workflow with MCP (Figma → code)](#13-build-workflow-with-mcp)
14. [Handoff checklist](#14-handoff-checklist)

---

## 1. Brand essence

| | |
|---|---|
| **What we sell** | Digital wedding invitations (mobile invitation websites + QR + share link) for Marwari families |
| **Feeling** | Elegant · culturally authentic · premium · welcoming · trustworthy |
| **Personality** | A gracious host at a haveli: warm, knowledgeable, never loud |
| **Audience** | Couples 25–32 (modern, Instagram-native) and parents 50–62 (decision-makers, value tradition); NRI families |
| **Promise** | "Wedding invitations, the Marwari way": every ritual, every elder's name, beautifully delivered |
| **Avoid** | Generic SaaS styling, neon, heavy gradients, clutter, cartoonish clip-art, stock "Indian wedding" clichés |

**Design principle — the jharokha rule:** the interface is the *frame*, the invitation is the *view*. Ornament lives on edges and dividers; content areas stay calm and ivory.

---

## 2. Design tokens

> **November 2026 redesign:** the palette, type scale, spacing and button shapes in `docs/08-luxury-redesign.md` replace the colour values below (burgundy `#5A202B`, ivory `#F7F3EB`, gold `#B18C58` as an accent only, charcoal `#292522`, sand `#E9DED0`, sage `#657460`). The older token names still exist in `site/css/site.css` and map onto the new values.


Use these names in **Figma Variables** (collection `BFI/Tokens`) and in **CSS custom properties**: one source of truth.

### 2.1 Colour
| Token | HEX | Role |
|---|---|---|
| `color/maroon` | **#641E2B** | Headings, primary buttons, active states, key icons |
| `color/maroon-700` | #4E1520 | Button hover/pressed |
| `color/gold` | **#C6A15B** | Borders, ornaments, dividers, highlights, focus ring |
| `color/gold-ink` | #7E5F24 | *Small* gold-coloured text on ivory (accessible version of gold) |
| `color/ivory` | **#FFF8EC** | Primary page background |
| `color/paper` | #FFFDF8 | Card surface on ivory |
| `color/beige` | **#E9DCC8** | Alternate sections, card borders, input borders, chips |
| `color/beige-tint` | #F7EEDF | Soft section background (between ivory and beige) |
| `color/brown` | **#392820** | Body text, footer background option |
| `color/muted` | #6E5A4E | Secondary text, captions |
| `color/whatsapp` | #1E7E45 | WhatsApp button (white text passes 5.1:1) |
| `color/logo-maroon` | #460013 | Background behind the full logo only (matches the logo artwork) |
| `color/success` / `danger` | #2F6B4F / #A4372E | Form states only |

### 2.2 Spacing (4-pt base)
`space/1`=4 · `2`=8 · `3`=12 · `4`=16 · `5`=20 · `6`=24 · `8`=32 · `10`=40 · `12`=48 · `16`=64 · `20`=80 · `24`=96 · `28`=112

### 2.3 Radius, borders, shadows
| Token | Value | Use |
|---|---|---|
| `radius/sm` | 8 | Inputs, chips |
| `radius/md` | 14 | Cards |
| `radius/lg` | 20 | Feature cards, preview panels |
| `radius/pill` | 999 | Buttons, tags |
| `radius/arch` | 999 999 16 16 (top-only round) | Jharokha arch frames |
| `border/hair` | 1px `beige` | Card outline |
| `border/gold` | 1px `gold` | Ornamental frames |
| `border/gold-double` | 3px double `gold` | Footer top, featured card |
| `shadow/soft` | 0 1 2 rgba(57,40,32,.05), 0 10 30 rgba(57,40,32,.08) | Cards on hover, phone mockups |
| `shadow/lift` | 0 24 50 rgba(57,40,32,.22) | Hero phone, modal |

### 2.4 Breakpoints
`mobile` 360–599 · `tablet` 600–979 · `desktop` 980–1439 · `wide` ≥1440. Design **mobile first** at **390 px**, then 768, 1440.

### 2.5 CSS starter
```css
:root{
  --maroon:#641E2B; --maroon-700:#4E1520; --gold:#C6A15B; --gold-ink:#7E5F24;
  --ivory:#FFF8EC; --paper:#FFFDF8; --beige:#E9DCC8; --tint:#F7EEDF;
  --brown:#392820; --muted:#6E5A4E; --whatsapp:#1E7E45; --logo-maroon:#460013;
  --serif:"Cormorant Garamond",Georgia,serif; --sans:"DM Sans",system-ui,sans-serif;
  --deva:"Tiro Devanagari Hindi",serif;
  --r-sm:8px; --r-md:14px; --r-lg:20px; --r-pill:999px;
  --shadow:0 1px 2px rgba(57,40,32,.05),0 10px 30px rgba(57,40,32,.08);
}
```

---

## 3. Typography

| Style | Font | Mobile | Desktop | Weight · line-height · tracking | Colour |
|---|---|---|---|---|---|
| Display (hero H1) | Cormorant Garamond | 40 | 64 | 600 · 1.05 · 0 | maroon |
| H2 section | Cormorant Garamond | 30 | 44 | 600 · 1.1 | brown or maroon |
| H3 card title | Cormorant Garamond | 22 | 26 | 600 · 1.2 | brown |
| H4 | Cormorant Garamond | 19 | 21 | 700 · 1.25 | brown |
| Eyebrow | DM Sans | 12 | 12 | 600 · 1 · 0.18em · UPPERCASE | gold-ink |
| Body L (lead) | DM Sans | 17 | 19 | 400 · 1.6 | muted |
| Body | DM Sans | 16 | 16 | 400 · 1.6 | brown |
| Small / caption | DM Sans | 14 | 14 | 400 · 1.5 | muted |
| Button | DM Sans | 15 | 15 | 600 · 1 · 0.01em | — |
| Price | Cormorant Garamond | 36 | 44 | 600, lining numerals | maroon |
| Devanagari line | Tiro Devanagari Hindi | 16 | 18 | 400 | gold-ink (on ivory) / gold (on maroon) |

**Rules**
- Serif only for headings, names, prices and quotes; **never** paragraphs.
- Body text never below 16 px on mobile (prevents iOS zoom on inputs too).
- Max line length 68 characters (≈ 640 px).
- One Devanagari line per page section at most: "॥ श्री गणेशाय नमः ॥", "॥ शुभ विवाह ॥".
- Script fonts are **only inside invitation designs**, never in the website UI.

Google Fonts: `Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500` · `DM+Sans:wght@400;500;600;700` · `Tiro+Devanagari+Hindi`.

---

## 4. Colour usage & accessibility

**Proportion:** ~70% ivory/paper · ~15% beige/tint · ~10% maroon · ≤5% gold. Gold is jewellery, not fabric.

| Pair | Ratio | Allowed use |
|---|---|---|
| Maroon on ivory | 11.3 : 1 | ✅ all text, buttons |
| Brown on ivory | 13.3 : 1 | ✅ body text |
| Ivory on maroon | 11.3 : 1 | ✅ button labels, maroon bands |
| Gold on maroon | 4.9 : 1 | ✅ text on maroon bands |
| Brown on beige | 10.4 : 1 | ✅ text on beige sections |
| Maroon on beige | 8.8 : 1 | ✅ |
| Gold-ink on ivory | 5.6 : 1 | ✅ eyebrows, small gold labels |
| Brown on gold | 5.8 : 1 | ✅ text on gold buttons |
| **Gold on ivory** | **2.3 : 1** | ⚠️ **ornaments & borders only**, never text |
| White on #25D366 | 2.0 : 1 | ❌ don't use WhatsApp's light green for text buttons; use `#1E7E45` |

Gradients: only a barely visible **ivory → beige-tint paper wash** (radial, top-right). No multi-colour or neon gradients.

---

## 5. Cultural motifs: rules

All motifs are **fine gold line art** (1.25–1.5 px stroke, `#C6A15B`), drawn as **SVG**, transparent background. Never filled solid blocks, never more than **one motif per section**, never behind body text at more than **6% opacity**.

| Motif | Where | Size | Notes |
|---|---|---|---|
| **Jharokha arch** | Hero image frame, invitation preview frames, empty states, page headers | Frame around content | Top-rounded arch with inner hairline; the brand's signature shape |
| **Peacock (pair, facing)** | Footer, About hero, "Thank you" states | 80–160 px | Echoes the logo; always symmetric, never a single cartoon peacock |
| **Elephant (caparisoned)** | How It Works step 4 "Share", About heritage section, 404 | 64–120 px | Profile view, line art with jhool (blanket) pattern; one only |
| **Floral (lotus, marigold, bel)** | Section dividers, card corners, list bullets | 16–120 px | Lotus divider between heading and content |
| **Palace / fort skyline** | Hero background band, Contact background, footer top edge | Full width, 120–200 px tall | 4–6% opacity line drawing (Amer/Mehrangarh-inspired, not a literal copy) |
| **Gold borders** | Featured cards, price highlight, quotes | Hairline or double rule | 4-dot corners optional |
| **Bandhej dots** | Sparingly as a 24 px divider strip | Strip only | Optional; keep at 15% opacity |

---

## 6. Layout, grid & spacing

| | Mobile (390) | Tablet (768) | Desktop (1440) |
|---|---|---|---|
| Columns | 4 | 8 | 12 |
| Gutter | 16 | 24 | 24 |
| Side margin | 20 | 32 | auto, content max 1160 |
| Section padding (top/bottom) | 64 | 80 | 112 |
| Card grid | 1 col (carousel) | 2 col | 3–4 col |

Section rhythm: ivory → beige-tint → ivory → maroon band (max one per page) → ivory → footer.

---

## 7. Component library

Build each as a **Figma component with variants**; names match the code.

| Component | Variants / states | Spec |
|---|---|---|
| **Button** | primary (maroon) · secondary (maroon outline) · gold (on maroon) · whatsapp · text-link · sizes L 52/M 48/S 38 · default/hover/pressed/disabled/focus | Pill radius, 600 DM Sans 15, icon optional left; focus ring 3px gold |
| **Header** | transparent-on-hero · solid · mobile | 76 px; logo monogram tile 44 + "BFI" serif + "MARWARI INVITATIONS" small caps; nav: Invitations · How it works · Customize · About · Contact; right: WhatsApp icon button + "Plan my invitation" primary |
| **Mobile menu** | open/closed | Full-height ivory sheet, links in serif 28, WhatsApp + enquiry buttons at bottom |
| **Footer** | — | Maroon `#641E2B` (or logo-maroon behind logo), gold double rule top, full logo, 4 link columns, contact, legal; peacock pair line art |
| **WhatsApp float** | collapsed (icon) · expanded ("Chat on WhatsApp") | Bottom-right 56 px circle `#1E7E45`, appears after 400px scroll; on mobile sits above the sticky CTA bar |
| **Sticky CTA bar (mobile)** | — | "Explore invitations" (primary) + "WhatsApp" (whatsapp) |
| **Section heading** | left · centred | Eyebrow + H2 + optional lead + optional lotus divider |
| **Invitation card** | default · hover · selected | Paper card, arch-topped preview panel (beige-tint) holding a phone mockup, title (serif), style tag, price "from ₹", buttons "Preview" + "Customize" |
| **Phone mockup** | S 160 · M 230 · L 300 | Brown bezel `#2A1C17`, 30 px radius, inner screen shows the invitation image |
| **Filter chips** | All · Royal · Traditional · Elegant · Modern; selected / unselected | Pill, beige border; selected = maroon fill + ivory text |
| **Benefit tile** | — | Line icon (gold) + serif title + 2-line text |
| **Step** | 1–4 | Numbered maroon circle, title, text, line-art illustration |
| **Testimonial** | — | Serif italic quote, stars in gold, couple + city |
| **Form field** | text · date · select · textarea · toggle · radio-card · file | 48 px height, paper fill, beige border, gold focus; label 14/600 above; helper text below |
| **Stepper (customize)** | 6 steps; done / current / upcoming | Horizontal on desktop, compact "Step 2 of 6" bar on mobile |
| **Live preview panel** | sticky (desktop) · drawer (mobile) | Phone mockup updating as fields change |
| **Accordion (FAQ)** | open/closed | Serif question, "+ / –" in gold-ink |
| **Badge / tag** | style tag · "Most chosen" · "New" | Beige pill; "Most chosen" = gold fill, brown text |
| **Breadcrumb** | — | Small, muted |
| **Modal / lightbox** | invitation full preview | Ivory, close button, arrows between invitation pages |

Icons: 1.5 px line icons (Lucide or Phosphor "light") in brown/maroon/gold; WhatsApp brand icon only on WhatsApp buttons.

---

## 8. Pages

Each page: **mobile 390 + desktop 1440** frames in Figma. Images reference IDs from §9.

### 8.1 Home `/`
| # | Section | Content | Layout | Images |
|---|---|---|---|---|
| 1 | Header | as §7 | — | IMG-LOGO-MARK |
| 2 | Hero | Devanagari "॥ श्री गणेशाय नमः ॥"; H1 "Wedding invitations, *the Marwari way*"; lead; buttons **Explore invitations** + **Chat on WhatsApp**; trust line "Made in Jaipur · 5-day delivery · private & secure" | Desktop: 55/45 split, text left, jharokha-framed phone right; mobile: text first, phone below (smaller) | ILL-PALACE-SKYLINE (bg band, 5%), IMG-HERO-PHONE, ILL-ARCH-FRAME |
| 3 | Introduction | "Rooted in Rajasthan, crafted for today": 2 short paragraphs + signature-style line | Centred, max 640 | ILL-LOTUS-DIVIDER |
| 4 | Benefits | 4 tiles: Made for Marwari rituals · Every name checked by hand · Share on WhatsApp in one tap · Private & consent-first | 4-col / 2×2 / 1-col | 4 gold line icons |
| 5 | Featured invitations | 4 cards + "View all invitations" | Carousel on mobile, 4-col desktop | IMG-INV-01…04 |
| 6 | Rituals we celebrate | Ganesh puja · Mayra · Haldi · Mehendi · Mahila sangeet · Baraat · Phera · Reception | 8 small tiles with line icons | ICN-RITUAL set |
| 7 | How it works (short) | 4 steps → link | Horizontal | ILL-STEP-1…4 (small) |
| 8 | Testimonials | 2–3 quotes | Carousel | IMG-COUPLE-01 (optional) |
| 9 | CTA band | Maroon band, full logo, "Let's create your invitation", buttons gold + WhatsApp | Centred | IMG-LOGO-FULL, ILL-PEACOCK-PAIR (8%) |
| 10 | Footer | §7 | | ILL-PEACOCK-PAIR |

### 8.2 Invitations (catalogue) `/invitations`
| Section | Content |
|---|---|
| Page hero | Beige-tint band with arch ornament; H1 "Our invitation collection"; lead; breadcrumb |
| Filter bar | Chips **All · Royal · Traditional · Elegant · Modern** + secondary filters: Price (Basic/Premium/Luxury), Language (English/Hindi/Bilingual), Sort (Popular/Newest/Price); sticky under header on scroll; on mobile a "Filters" button opening a bottom sheet |
| Results grid | Invitation cards (§7), 3-col desktop / 2-col tablet / 1-col mobile; "Showing 12 invitations" |
| Bespoke banner | "Want something only yours?" + Luxury bespoke CTA |
| Images | IMG-INV-01…12, ILL-ARCH-FRAME (page hero) |

### 8.3 Invitation details `/invitations/:slug`
| Section | Content |
|---|---|
| Gallery | Large phone preview (L) in jharokha frame; thumbnails of inside pages (cover, couple, events, venue, RSVP); "View live demo" opens full-screen preview |
| Summary | Style tag, H1 name, short story of the design, price "from ₹11,999", delivery time, rating |
| Features | Checklist: event pages, countdown, maps, photo gallery, RSVP, music, language options, QR code |
| Customization options | What can change: colours (3 swatches), fonts, motifs, number of events, language, music |
| CTAs | **Customize this invitation** (primary) · **Enquire on WhatsApp** (whatsapp) · **Ask a question** (link) |
| Included / add-ons | Accordion |
| Similar invitations | 3–4 cards |
| Images | IMG-INV-xx full set (cover + 4 inner screens), ILL-ARCH-FRAME |

### 8.4 How it works `/how-it-works`
| Step | Title | Text | Illustration |
|---|---|---|---|
| 1 | **Choose** | Browse the collection or ask for bespoke | ILL-STEP-1: hand selecting a card under an arch |
| 2 | **Customize** | Add names, functions, venues, language, music | ILL-STEP-2: quill/pen with lotus |
| 3 | **Preview** | See it on your phone; one round of changes | ILL-STEP-3: phone inside a jharokha |
| 4 | **Share** | Send the link & QR to every guest on WhatsApp | ILL-STEP-4: caparisoned elephant carrying an envelope |
Plus: timeline (5/10/21 days by package), "What we need from you" checklist, FAQ (6), CTA band.

### 8.5 Customize invitation `/customize` (with optional `?design=slug`)
Two-column: **form left, live preview right (sticky)**; on mobile the preview is a bottom drawer "See preview".

| Step | Fields |
|---|---|
| 1 Design | Selected design card + "Change"; colour variant swatches |
| 2 Couple | Bride's name, groom's name, display style (Bride & Groom / Groom & Bride), parents' names (both sides), grandparents/blessings |
| 3 Dates & events | Main wedding date; event list (repeatable): event type (Ganesh puja, Mayra, Haldi, Mehendi, Mahila sangeet, Baraat, Phera, Reception, custom), date, time, dress code |
| 4 Venues | Per event: venue name, address, Google Maps link; "Same venue for all" toggle |
| 5 Language & music | Language: English / Hindi / Marwari + Hindi / Bilingual; opening line (Shri Ganeshaya Namah…); music: none / choose from library (3 samples with play) / upload own (licence checkbox) |
| 6 RSVP & sharing | RSVP on/off, deadline, contact number, guest count field on/off, meal preference on/off; share options: link, QR, WhatsApp message text |
| Review | Summary + price estimate + **Send for design** (enquiry) + **Save & continue on WhatsApp** |
Validation inline; autosave; progress "Step 3 of 6".
Images: selected IMG-INV-xx in phone mockup; ILL-LOTUS-DIVIDER.

### 8.6 About BFI `/about`
| Section | Content | Images |
|---|---|---|
| Hero | Maroon (logo-maroon) band with full logo and H1 "Rooted in Rajasthan" | IMG-LOGO-FULL, ILL-PALACE-SKYLINE (gold 10%) |
| Brand story | Why Marwari only; from kankotri to phone | IMG-ABOUT-KANKOTRI (photo of a traditional printed card) |
| Heritage | Shekhawati havelis, jharokhas, peacocks, Gangaur colours: our inspiration | ILL-ELEPHANT, IMG-HAVELI-DETAIL |
| Vision | "Every Marwari family's invitation, beautifully digital" | — |
| Values | 4 tiles: Respect for tradition · Craft & accuracy · Privacy · Warm service | line icons |
| Team (optional) | Founder + studio | IMG-TEAM |
| CTA | Contact / WhatsApp | ILL-PEACOCK-PAIR |

### 8.7 Contact `/contact`
| Section | Content |
|---|---|
| Hero | H1 "Let's plan your invitation"; lead "We reply within an hour, 10am–8pm" |
| Contact options | 3 cards: **WhatsApp** (largest, whatsapp button) · **Email** hello@… · **Visit/Call** Jaipur studio + phone |
| Enquiry form | Name(s), WhatsApp number, email, wedding date, city, package (Basic/Premium/Luxury/Not sure), preferred design, message, "I agree to be contacted on WhatsApp" checkbox; submit "Send enquiry" |
| Map / location | Optional embedded map or illustrated Jaipur map |
| Background | ILL-PALACE-SKYLINE at bottom (5%) |

### 8.8 Shared states
404 ("This door is closed": elephant illustration + links), form success ("Dhanyavaad!" + WhatsApp), loading skeletons in beige-tint, cookie/privacy notice (small, bottom-left).

---

## 9. Images & illustrations

### 9.1 Formats & export
| Type | Format | Size | Notes |
|---|---|---|---|
| Line motifs (arches, peacocks, elephant, florals, skyline) | **SVG** | — | Single colour `#C6A15B`, stroke 1.5, no fills, optimised (SVGO) |
| Invitation previews | **WebP** (+ JPG fallback) | 600×1260 @2x (phone screen 9:19) | Rendered from the real invitation |
| Photography | **WebP** | 1600 px long edge, ≤200 KB | Natural light, warm tone |
| Logo | PNG/WebP from `brand/` | as in `brand/README.md` | On logo-maroon only |
| Social/OG | PNG 1200×630 | `brand/og-image.png` | |

Naming: `bfi-<type>-<name>@2x.webp`, e.g. `bfi-ill-palace-skyline.svg`, `bfi-inv-royal-heritage-cover@2x.webp`.

### 9.2 Asset list

| ID | Asset | Where used | Format | How to create |
|---|---|---|---|---|
| IMG-LOGO-FULL / MARK | Logo | Header, footer, About, CTA bands | PNG | ✅ already in `brand/` |
| ILL-ARCH-FRAME | Jharokha arch frame (empty) | Hero, invitation cards, details | SVG | Draw in Figma (vector) or AI → vectorize |
| ILL-PALACE-SKYLINE | Rajasthani palace & fort skyline, line art | Hero bg band, About, Contact, footer edge | SVG | AI image → vectorize → simplify |
| ILL-PEACOCK-PAIR | Two facing peacocks with floral vine | Footer, About, CTA band | SVG | AI → vectorize |
| ILL-ELEPHANT | Caparisoned elephant in profile | How it works step 4, About, 404 | SVG | AI → vectorize |
| ILL-LOTUS-DIVIDER | Lotus with two thin rules | Section dividers | SVG | Draw in Figma |
| ILL-FLORAL-CORNER | Floral corner ornament | Featured cards, quotes | SVG | AI → vectorize or draw |
| ILL-BORDER-FINE | Repeating fine gold border (paisley/bel) | Price highlight, page hero edges | SVG pattern | Draw/AI |
| ILL-STEP-1…4 | Step illustrations (choose, customize, preview, share) | How it works | SVG | AI → vectorize, same style |
| ICN-RITUAL (8) | Ganesh, kalash (Mayra), turmeric (Haldi), henna hand, dholak, horse (Baraat), fire (Phera), glasses | Rituals section | SVG 24/48 | Draw in Figma (line icons) |
| IMG-HERO-PHONE | Phone mockup showing Royal Heritage invitation | Hero | WebP | Real invitation screenshot in Figma phone frame |
| IMG-INV-01…12 | Invitation covers + 4 inner screens each | Catalogue, details | WebP | Design in Figma (or export from real invitations) |
| IMG-ABOUT-KANKOTRI | Flat-lay of a traditional printed Marwari card with marigolds | About | WebP photo | Real photo (best) or AI photo |
| IMG-HAVELI-DETAIL | Close-up of Shekhawati fresco / jharokha | About heritage | WebP photo | Real/licensed photo (Unsplash/Pexels) or AI |
| IMG-COUPLE-01…03 | Real couples (with consent) | Testimonials | WebP | Real only, never AI faces for testimonials |
| IMG-TEAM | Founder/studio | About | WebP | Real photo |
| IMG-OG | Share card | Meta tags | PNG | ✅ `brand/og-image.png` |

### 9.3 AI prompts (copy-paste)

**Global style suffix (add to every illustration prompt):**
> *fine single-weight antique gold line art (#C6A15B) on a plain warm ivory background (#FFF8EC), elegant, minimal, Rajasthani royal heritage style, symmetrical, lots of negative space, no text, no people's faces, no gradients, no shadows, vector illustration, high detail but clean lines*

| ID | Prompt |
|---|---|
| ILL-PALACE-SKYLINE | "A wide panoramic skyline of a Rajasthani palace and hill fort inspired by Amer and Mehrangarh: domed chhatris, jharokha balconies, arched gateways and battlements, drawn as a single continuous horizon band" + style suffix · aspect 4:1 |
| ILL-ARCH-FRAME | "An ornate Rajasthani jharokha arch frame, multi-foil scalloped top, slender pillars, a small lotus finial, empty centre for content" + style suffix · 3:4 |
| ILL-PEACOCK-PAIR | "Two peacocks facing each other, tails flowing downward, between them a lotus and a small floral vine, mirror symmetry, inspired by Rajasthani miniature painting borders" + style suffix · 3:1 |
| ILL-ELEPHANT | "A royal Rajasthani elephant in side profile wearing an ornamental blanket (jhool) and head ornament, raised trunk, gentle and dignified" + style suffix · 4:3 |
| ILL-FLORAL-CORNER | "A delicate corner ornament of lotus buds, bel leaves and a paisley, Mughal-Rajasthani style, for decorating the corner of a card" + style suffix · 1:1 |
| ILL-BORDER-FINE | "A seamless horizontal border of tiny paisleys and bel vines, thin and refined, like the gold zari edge of a saree" + style suffix · 8:1, seamless |
| ILL-STEP-1 | "A hand gently choosing an invitation card from three cards under a jharokha arch" + style suffix |
| ILL-STEP-2 | "A traditional quill pen writing on a card decorated with a lotus" + style suffix |
| ILL-STEP-3 | "A smartphone showing an invitation, framed inside a Rajasthani jharokha window" + style suffix |
| ILL-STEP-4 | "A royal caparisoned elephant carrying a sealed envelope with a lotus seal" + style suffix |
| IMG-ABOUT-KANKOTRI (photo) | "Overhead flat-lay photograph of a traditional Marwari wedding invitation card (kankotri) in maroon and gold on ivory handmade paper, with marigold flowers, a red thread and a small brass diya, soft natural window light, warm tones, shallow depth of field, realistic" |
| IMG-HAVELI-DETAIL (photo) | "Close-up photograph of an ornate Shekhawati haveli jharokha with faded fresco paintings in maroon, ochre and gold, warm afternoon light, realistic architectural photography" |

**Negative prompt (where supported):** *neon, glossy 3D, cartoon, clip-art, heavy gradients, text, watermark, distorted architecture, extra limbs, faces, dark background, clutter.*

**After generating line art:** vectorize (Figma: *Vectorize*/plugins like "Image Tracer"; or Illustrator Image Trace / Vectorizer.ai) → set stroke to `#C6A15B` 1.5 px → remove background → simplify paths → export SVG.

**Usage of backgrounds:** palace/peacock/elephant line art appears at **4–10% opacity** behind hero/CTA bands only, never under paragraphs; full opacity only when used as a standalone illustration (step images, 404).

**Licensing:** use only AI tools whose terms grant commercial use (Figma AI, Adobe Firefly, Canva Pro, Ideogram paid); keep a log of prompts/outputs in `brand/ai-log.md`. Never use real copyrighted artworks or palace photos without a licence.

---

## 10. Invitation catalogue & filters

| # | Invitation | Style filter | Tier | Look |
|---|---|---|---|---|
| 1 | Royal Heritage | **Royal** | Premium · Luxury | Haveli arch, maroon & gold |
| 2 | Royal Palace | **Royal** | Luxury | Palace skyline, black & gold |
| 3 | Golden Elegance | **Royal** | Luxury | Ornate mandala, rich red |
| 4 | Marwari Classic | **Traditional** | All | Kalash & leaves, classic red |
| 5 | Mandap Magic | **Traditional** | Basic · Premium | Ivory mandap, floral |
| 6 | Gangaur Utsav | **Traditional** | Premium | Gangaur colours, festive |
| 7 | Ivory Pearl | **Elegant** | Premium | Ivory, blush, fine gold |
| 8 | Shekhawati Fresco | **Elegant** | Luxury | Fresco storytelling |
| 9 | Jharokha Minimal | **Elegant** | Basic | Single arch, lots of space |
| 10 | Desert Dreams | **Modern** | Basic · Premium | Thar dunes, sand minimal |
| 11 | Pink City | **Modern** | Premium | Jaipur pink, geometric |
| 12 | Monogram Gold | **Modern** | Basic | Couple monogram, clean |

Items 1, 2, 3, 4, 5 and 10 exist in the studio today; 6–9 and 11–12 are new designs to create.

---

## 11. UX, accessibility & motion

**Navigation:** max 5 top links; current page underlined in gold; logo → Home; "Plan my invitation" always visible on desktop; on mobile a sticky bottom bar + WhatsApp float.

**WhatsApp prominence:** on Home hero, every invitation card, details page, Customize review, Contact (largest option), mobile sticky bar, and the floating button. Pre-filled message: *"Namaste BFI 🙏 I'd like to know more about the {design} invitation for our wedding on {date}."*

**Accessibility (WCAG 2.1 AA):** contrast per §4 · visible focus (3 px gold ring) · 44×44 touch targets · labels on all inputs · alt text for every image (describe the invitation, e.g. "Royal Heritage invitation cover with haveli arch") · `lang="hi"` on Devanagari lines · respects `prefers-reduced-motion` · forms announce errors.

**Performance:** LCP < 2.5 s on 4G · SVG illustrations · lazy-load below the fold · fonts `display=swap` · hero image ≤ 150 KB.

**Motion (subtle):** fade + 12 px rise on first view (300 ms, ease-out, once) · cards lift 2 px on hover · arch frame draws its gold stroke once on load (600 ms) · no parallax, no auto-playing carousels, no confetti.

**Tone of voice:** warm, respectful, concise; use ritual names correctly; address "your family"; avoid tech jargon.

---

## 12. Tools: Figma AI vs Canva AI

| Need | **Figma (with Figma AI / Make)** | **Canva (with Magic Studio)** |
|---|---|---|
| Responsive website layouts (mobile + desktop frames) | ✅ Best: auto-layout, constraints, breakpoints | ⚠️ Fixed-size pages, weak responsive |
| Design system: variables, components, variants | ✅ Native variables & variants | ❌ Very limited |
| Developer handoff / code | ✅ Dev Mode, CSS, **Figma MCP → code** | ❌ Not built for dev handoff |
| Interactive prototype (filters, customize steps) | ✅ Prototyping | ⚠️ Basic |
| Generating illustrations / images | ✅ Good (Figma AI image generation, plugins) | ✅ Good (Magic Media / Dream Lab) |
| Vector line art you can edit | ✅ Vector editing + vectorize | ⚠️ Limited editing |
| Social media posts, Reels covers, flyers, WhatsApp creatives | ⚠️ Possible | ✅ Best: templates, quick export |
| Learning curve | Medium | Easy |
| Cost | Free starter; Professional for full Dev Mode | Free; Pro for brand kit & AI credits |

### ✅ Recommendation
- **Use Figma for the website**: design system, all 7 pages, components, prototype and handoff. It is the only one of the two that produces a real, responsive, implementable website design, and it connects to code through **Figma MCP**.
- **Use Figma AI (or Adobe Firefly) for the illustrations**, then vectorize in Figma so the gold line art is crisp SVG.
- **Use Canva for marketing only**: Instagram posts, Reels covers, WhatsApp creatives, flyers for vendors; set up the Canva Brand Kit with the same colours, fonts and logo.

---

## 13. Build workflow with MCP

**Figma MCP is already connected in this Claude session.** Once you say go, here's the plan:

| Step | What happens | Who |
|---|---|---|
| 1 | Create a Figma file **"BFI · Royal Heritage Website"** with pages: `00 Cover`, `01 Tokens`, `02 Components`, `03 Illustrations`, `10 Home`, `11 Invitations`, `12 Invitation Details`, `13 How It Works`, `14 Customize`, `15 About`, `16 Contact`, `20 Prototype` | Claude via Figma MCP |
| 2 | Add **variables** for every token in §2 (colour, spacing, radius) and **text styles** for §3 | Claude |
| 3 | Build **components** from §7 with variants | Claude |
| 4 | Generate **illustrations** from §9.3 prompts, vectorize and place them on `03 Illustrations` | Claude (generate) + you (approve) |
| 5 | Lay out **all 7 pages** at 390 and 1440 using the components | Claude |
| 6 | Review in Figma, leave comments, iterate | You + Claude |
| 7 | **Design → code** via Figma MCP: build the real website in HTML/CSS (no-build, like today) with the same tokens; keep every existing app link working | Claude |
| 8 | Deploy to a **preview** link; production only after your "go live" | Claude + you |

**What you need for step 1:** a Figma account with access to edit files (a free account can start; a Professional seat is needed for full Dev Mode handoff), and permission for Claude to create the file in your Figma team when prompted.

**Prompt to start:** *"Use Figma MCP to create the BFI Royal Heritage website design from DESIGN.md: tokens, components, illustrations and all 7 pages at 390 and 1440."*

---

## 14. Handoff checklist
- [ ] Tokens as Figma variables + CSS variables (same names)
- [ ] Text styles for every row in §3
- [ ] All components with variants & states
- [ ] Illustrations as optimised SVG; photos as WebP with alt text
- [ ] 7 pages × (390 + 1440) frames, plus 768 for Home & Invitations
- [ ] Prototype: filters, invitation card → details → customize → review → WhatsApp
- [ ] Contrast check on every text style (§4)
- [ ] Copy reviewed by the founder (names, rituals, prices)
- [ ] Image licences logged
- [ ] Dev handoff via Figma MCP; build on preview; your approval before production
