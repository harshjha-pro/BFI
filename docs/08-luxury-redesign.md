# Luxury editorial redesign (November 2026)

Branch: `redesign-luxury`. Production (`main`) is untouched until the owner approves the preview.

## 1. Design system (one token set)

| Token | Hex | Use |
|---|---|---|
| Royal Burgundy `--burgundy` | `#5A202B` | Primary buttons, active states, the closing panel |
| Warm Ivory `--ivory-bg` | `#F7F3EB` | Main background |
| Antique Gold `--gold-accent` | `#B18C58` | Fine accents only (never body text) |
| Soft Charcoal `--charcoal` | `#292522` | Body text and headings |
| Warm Sand `--sand` | `#E9DED0` | Footer, alternating sections (as a lighter mix), borders |
| Muted Sage `--sage` | `#657460` | Check marks only |
| White | `#FFFFFF` | Cards, price panels, forms |

- Text colours that need contrast are derived, not new: secondary text `#5E5650` (6.4:1 on ivory), gold labels `#7A5C2E` (5.6:1).
- The older names used across the stylesheet (`--maroon`, `--gold`, `--ivory`, `--brown`…) now point at these tokens, so every older component follows the new palette.
- **Type:** Cormorant Garamond (regular/medium, italic for emphasis) for headings; DM Sans for everything functional. Script fonts appear only inside invitation artwork and the demos.
- **Shape:** buttons are rectangular with a 3 px radius, uppercase 11–12 px labels. Cards have no shadows: thin hairlines instead.
- **Spacing:** sections are 64–120 px tall depending on screen width; the content is at most 1240 px wide, with side padding of 20–88 px.
- **Motion:** gentle reveal on scroll and a slight image zoom on hover. Spinning, floating, pulsing and typing loops have been removed (mandala, seal ring, feature orbit, WhatsApp pulse, chat dot, typing caret, free-card shuffle, home petals, the marquee). Everything respects reduced-motion settings.

## 2. Page-by-page change log

| Page | Changes |
|---|---|
| All pages | **Header:** logo, five links (Invitations, Our Work, How It Works, Pricing, About), one "Start your invitation" button and a quiet "Sign in" link. The duplicate WhatsApp and login buttons are gone.<br>**Menu:** one accessible menu dialog with `aria-expanded`, focus kept inside, Escape and backdrop to close, and it closes after you pick a link.<br>**Footer:** sand background, brand line, Explore / Resources / Contact columns, privacy and terms.<br>**Phones:** one fixed action bar; the floating WhatsApp bubble is removed. |
| Home | Rebuilt to the brief's 14-section order:<br>• editorial split hero with one large real invitation<br>• the four verified facts<br>• "Rooted in tradition. Made for today."<br>• 4 featured designs<br>• the guest experience, labelled fictional<br>• eight rituals, with a note that customs vary<br>• the Chittorgarh engagement project<br>• four steps<br>• the three packages, with the delivery-clock note<br>• terms<br>• FAQ<br>• burgundy closing panel. The free card maker is now a single line. |
| Invitations | Now opens with "The Invitation Collection". The filters are restyled, and a `?tier=` link pre-selects a package. "Need help choosing?" (WhatsApp) and "Something only yours" (bespoke) sit side by side. |
| Cards (everywhere) | Large image with a hairline frame, quiet text, prices aligned, and two clear actions: "View live demo" and "View design". |
| Design pages (8) | "Sample wording: names, date and venue are fictional" under the gallery. Calmer gallery frame and price. |
| Pricing | The "Most chosen" badge is removed (no data supports it), and the Premium blurb is reworded. Each package now says "Ready in X after complete details and the 50% advance". Package buttons open the collection filtered to that tier. |
| How It Works | New "Keep the printed kankotri for elders" section, linking to the digital vs printed guide. |
| Our Work | Heading is now "Selected Celebrations", with client projects and design demos clearly separated. The case study ends with "Create an invitation in this spirit". |
| Contact | The Jaipur city map is removed (no public studio address). Replaced by a short "Working with us" note. |
| Live demo | **Directions** now open the real area (e.g. "C-Scheme, Jaipur") instead of a fictional venue name, plus a new "Get directions" link under the map.<br>**Countdown:** once the date passes it shows a message instead of zeros.<br>Music still starts only when tapped. |
| Inner-page heroes | Same compositions, on a calm ivory stage with no looping animation. |

All URLs, design slugs, `?design=`, `?t=` and `?c=` links, forms, sign-in, Supabase tables and storage are unchanged.

## 3. QA (Section 10 of the brief)

| Check | Result |
|---|---|
| 37 pages × 8 widths (360–1440 px): horizontal overflow | **Pass.** One 1 px case on a design page at 360 px was fixed (gallery arrows). |
| Broken internal links | **Pass** (none) |
| Console / script errors | **Pass** (none) |
| Menu: opens, focus stays inside, Escape closes, focus returns, `aria-expanded` updates | **Pass** (automated) |
| Filters: collection chips, package select, `?tier=` | **Pass** (`?tier=Premium` shows 3 designs) |
| Demo directions resolve to real localities | **Pass** (link format checked; opening on a real phone is still to do) |
| Countdown handles a past date | **Pass** (code path added; demo dates are always 60 days ahead) |
| Prices match package data (₹3,999 / ₹6,999 / ₹11,999; Sheesh Mahal ₹14,999) | **Pass** (one source in the generator) |
| Sample demos labelled fictional | **Pass** (demo ribbon, design pages, home experience block) |
| Contrast: body text, secondary text and gold labels on ivory | **Pass** (≥ 4.5:1 by token choice) |
| Enquiry and partner forms | Unchanged code. They send to the `enquiries` table, which this test environment cannot reach. |
| Demo RSVP | The demo RSVP is labelled as not sent. Real RSVPs live on each client's own invitation site. |
| Google sign-in, email sending | Waiting on owner setup (Google OAuth client, Gmail SMTP) |
| Real-phone test of maps, `tel:` and `wa.me` links | To do on the preview |

## 4. Needs owner input

1. **Mahi & Ayush (resolved):** the case study briefly hid the names and blurred the images, then the owner asked for everything to be restored (12 Nov 2026). The couple's names are removed site-wide and the screenshots are blurred. The live-invitation link is removed, the case study now lives at `work-chittorgarh-engagement.html`, and the old address forwards there (noindex).
2. **"We reply within an hour":** this appears on Contact, design pages and form confirmations. Keep it only if it is true in practice; otherwise we will change it to "the same day, 10am–8pm".
3. **Link validity** (wedding + 6 months), **delivery times** (24/48/72 h) and **one change round:** confirm these are operationally guaranteed. They are shown as before.
4. **Partner terms:** 15% / 20% commission, paid after the client completes payment.
5. **Founder or studio details for About:** nothing has been invented.
6. **Final logo / name:** the current heritage logo and "BFI Marwari Invitations" are kept. "BfiLuxe" is not used.
7. **Legal review** of Privacy and Terms: the text is unchanged.

## 5. Production release checks (12 November 2026)

- **Branch:** `main` (`0aae4c3`) is an ancestor of `redesign-luxury`, so the merge is conflict-free with no deleted files. Regenerating from `tools/build_website.py` matches the committed output exactly.
- **Fixed before release:** the "View the live demo of …" button overflowed by 1 px at 360 px. Full-width buttons now wrap.
- **Re-run:**
  - 37 pages × 360/375/390/430/768/1024/1366/1440 px, plus 1280 and 1920 px on 9 key pages: no overflow, broken links or script errors.
  - Menu (focus kept inside, Escape, `aria-expanded`), all 9 collection filters, `?tier=` links, demo themes, directions and countdown all work.
  - WhatsApp (`wa.me/918949509745`), `tel:` and `mailto:` links are correct.
- **SEO:**
  - Unique titles; descriptions and Open Graph images on every page.
  - Canonical links on the production domain.
  - `robots.txt` allows everything except account/login. The sitemap lists 33 URLs.
  - Every image has alt text.
  - `demo.html` and the `invitation.html` redirect have no H1. This was the same before.
- **Forms:** the contact and partner submissions were inserted as the `anon` role inside a transaction and then rolled back. Row-level security accepts both; the table still has 0 rows.
- **Rollback point:** production deployment `dpl_EyspeeNQD1PUNS6rvqpYNGCeoRFZ` (commit `0aae4c3`).

## 6. Owner answers (12 November 2026)

- **Client project:** anonymised as described in §4, item 1.
- **Reply within an hour, delivery 24/48/72 h, one change round, link valid for the wedding plus 6 months:** confirmed by the owner, kept as published.
- **Partner terms:** 15% / 20%, paid after the client completes payment. Confirmed by the owner.
- **Founder details:** not needed for now. About stays as it is.
- **Sign-up limit:** the 6 old test accounts were deleted. A re-test of 6 simultaneous sign-ups to the live function gave 5 × 200 and 1 × 429. The created accounts were confirmed, had profiles and could log in. All test accounts and attempt records were then deleted.

## 7. Five live sample invitations (12 November 2026)

Five standalone sample invitation websites live at `/live-demo-1/` to `/live-demo-5/`. They share one runtime (`site/live-demo-assets/ld.js` and `ld.css`), but each has its own layout, fonts, colours and opening.

| # | Name | Concept | Opening |
|---|---|---|---|
| 1 | Rajmahal | Royal editorial, Jaipur. Cormorant, Marcellus SC and Pinyon Script. | Wax-sealed envelope |
| 2 | Gulabi Nagri | Pink City magazine, Jaipur. Sticky side panel, story timeline, mood boards, travel tips and FAQs. | Jharokha doors |
| 3 | Thar ki Raat | Desert night, Jaisalmer. Starfield, moon and dunes, constellation timeline. | Light the diya |
| 4 | Haldi Haveli | Hindi-first festive, Bikaner. हिंदी / English switch, bandhani pattern, ritual cards. | Marigold curtain |
| 5 | Line & Light | Modern minimal, Mumbai. Swiss grid, schedule table, photo strip, FAQs, food preferences. | Self-drawing monogram |

**Shared behaviour:**
- Every date is calculated as "N days from today", so the sample never shows a past date. The countdown shows a message if it ever runs out.
- Directions open the real locality, because the venues are fictional.
- Each function has an add-to-calendar (.ics) button.
- The RSVP is multi-step with validation. It says that a sample sends nothing.
- Music is generated in the browser and starts only when tapped.
- WhatsApp share and copy link.
- A fixed "Sample invitation" ribbon links to customize.
- Reduced motion is respected, and the opening works by keyboard.

**Research:** the ideas come from patterns common across current invitation sites and templates (cinematic openings, reveals as you scroll, story timelines, multi-step RSVPs, dress-code boards, editorial layouts, travel and FAQ sections). All artwork, code and copy are original.

**Tests:**
- All 5 at 390 and 1440 px: no overflow and no script errors.
- Opening by keyboard works; every date is filled in.
- Directions resolve to Google Maps searches; the .ics file downloads.
- The RSVP blocks empty steps and completes once filled in.
- The language switch (demo 4) works; music starts only on a tap.
