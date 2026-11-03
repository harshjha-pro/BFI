# BFI website: design, SEO / AEO / GEO audit and buyer review

Site: https://bfi-royal-heritage.vercel.app · Audit date: 3 November 2026

---

## 1. Audit summary

| Area | Before | After this update |
|---|---|---|
| Design consistency | Good look, but repeated sections and an unclear main action | One clear path on every page: **See designs → Live demo → Customize / WhatsApp** |
| Trust | No prices on home, no demo, no policies, placeholder contact details | Prices everywhere, live demo, payment/changes/refund terms, privacy, real contact |
| SEO | Design pages built by JavaScript (invisible to Google), no sitemap, no structured data | 8 static design pages, sitemap, robots, canonical URLs, Product / FAQ / HowTo / Breadcrumb schema |
| AEO (answer engines, Google answers) | Almost no question-and-answer content | FAQ blocks on Home, Pricing, How It Works, Contact and Guide, all marked up as FAQPage |
| GEO (AI search: ChatGPT, Perplexity, Gemini) | Nothing an AI could quote with confidence | `llms.txt`, consistent business facts on every page, a citable Marwari wedding guide |
| Login | Sign-up never completed (confirmation link pointed to localhost); Google not enabled | Sign-up and login work instantly; Google needs one setting (see §5) |

## 2. Page-by-page

### Home
- **Fixed:** the main heading was hidden from Google; now the visible H1 is "Premium Digital Wedding Invitations for Marwari Families".
- **Removed (extra):** the "Featured invitations" grid repeated the same four images as the collections tiles; the closing quote band repeated the About page.
- **Added:** live demo section, the three packages with prices, a reviews section (shows only real, approved reviews), FAQ, a link to the free wedding guide and a closing call-to-action band.
- **Fixed copy:** "Ready in 24 hours" contradicted the 48/72-hour packages; now "Ready in 24–72 hours".

### Invitations
- Design cards are now real HTML (indexable), linking to one page per design.
- H1 now says what people search for: "Digital Wedding Invitation Designs".

### Design pages (new: 8 static pages, replacing `invitation.html?slug=`)
- Each has its own title, description, share image, Product + price schema and breadcrumbs.
- Added "Open the live demo in this design" and payment terms next to the price.
- Old links still work: `invitation.html?slug=…` forwards to the new page.

### Pricing (new)
- Three packages, a full comparison table, trust points and pricing FAQ.

### How It Works (redesigned)
- Step chips, four illustrated step rows with what happens and a button each, delivery timeline, "what we need" checklist, payment / changes / privacy / link-validity cards, digital vs printed comparison, 7 FAQs with HowTo + FAQ schema, closing CTA.

### Customize
- Unchanged in function; now linked from every design and the demo.

### Live demo (new)
- A full sample invitation (Priya & Rohan, clearly labelled as a sample): blessings, families, live countdown, six functions with maps, gallery, RSVP form (demo), share buttons, and a switcher to see the same invitation in all 8 designs.

### Marwari wedding guide (new)
- Rituals in order, invitation wording in Hindi and English (copy buttons), WhatsApp message template, send-out checklist and FAQ. This is the page most likely to be found on Google and quoted by AI assistants.

### About
- Values rewritten to promises the studio can keep (correct rituals, names checked by hand, pay after approval). Links to the guide.

### Contact (redesigned)
- Quick WhatsApp / Call / Email buttons, six contact cards including "Save our contact" (phone contact card download), enquiry form that also offers "Send on WhatsApp", "What happens next" steps, map, contact FAQ.

### Privacy, Terms (new)
- Needed for trust, payments and Google login approval.

### Site-wide
- New favicon and app icons from the heritage logo, new share image, real WhatsApp/phone/email in header, footer and schema.
- Footer "Save our contact" button, links to Pricing, Demo, Guide, Privacy, Terms.
- Desktop nav adds Pricing; at mid widths the WhatsApp button collapses to an icon so the header never wraps.

## 3. Buyer review: "Would I buy?"

I read the site as a bride's elder brother in Ahmedabad, comparing three invitation studios on my phone.

**Before this update: 5.5 / 10. I would not have paid.**
- Beautiful, but I could not see what I'd actually get; there was no demo.
- No price until I clicked into a design; no idea how payment works.
- No reviews, no policy, and the WhatsApp number was obviously a placeholder.
- Creating an account did nothing.

**After this update: 8 / 10. I would message on WhatsApp today.**
- The live demo answers "what will my relatives see?" in 10 seconds, on my own phone.
- Prices, delivery time and "pay 50% after approval" remove the risk.
- The Hindi wording and the rituals guide tell me this studio understands *our* weddings.
- I can save the contact and come back; the guide gives me a reason to.

**What still stops a 10 / 10 (only the studio can supply these, so I did not invent them):**
1. **Real reviews from real families.** The reviews section is built and stays hidden until you approve real ones (customers write them from My Account; approve in Supabase → `reviews` → set `approved` to true). Never publish made-up reviews: it is illegal under Indian consumer-protection rules on fake reviews and destroys trust when found.
2. **Real past work.** With permission, add 3–6 real invitations (names blurred) as "Recent invitations".
3. **Founder photo and name** on About: people buy from people.
4. **Instagram page** with the same designs, linked in the footer.
5. **A launch offer**, if you want one (e.g. a free extra function page for the first 20 families). It is honest and creates urgency.

## 4. Business points to confirm (I wrote sensible defaults, please check)

| Item | Where it appears | Default I used |
|---|---|---|
| Prices | Pricing, design pages, schema | Basic ₹3,999 · Premium ₹6,999 · Luxury ₹11,999 (Sheesh Mahal ₹14,999) |
| Events per package | Pricing table | 3 / 8 / unlimited |
| Refund policy | Terms | Advance refunded minus work done if cancelled before the first preview; not refundable after |
| Link validity | Pricing FAQ, Terms | Live at least 6 months after the wedding |
| Studio location | Contact, About, schema, llms.txt | Jaipur, Rajasthan |
| Reply time | Contact, FAQs | Within an hour, 10am–8pm |

Change them in `tools/build_website.py` (top of file) and run `python3 tools/build_website.py`.

## 5. Login and email status

- **Email + password sign-up and login: working.** Accounts are created already confirmed by a small server function (`signup`), so customers do not need a confirmation email.
- **Google login: needs a Google OAuth client** (5 minutes, only the Google account owner can do it). Steps are in the reply to you and below.
- **Emails (login links, password reset): off until an email sender is connected.** The "Forgot password" link sends customers to WhatsApp meanwhile. To turn emails on, connect Gmail SMTP in Supabase, then set `authEmails: true` in `site/js/config.js`.

### Google login setup
1. Go to https://console.cloud.google.com → create a project "BFI Website".
2. APIs & Services → OAuth consent screen → External → app name "BFI Marwari Invitations", support email, logo, links to `/privacy.html` and `/terms.html` → Publish.
3. Credentials → Create credentials → OAuth client ID → Web application.
   - Authorised JavaScript origin: `https://bfi-royal-heritage.vercel.app`
   - Authorised redirect URI: `https://oaosapkkzoynaqpnmvrj.supabase.co/auth/v1/callback`
4. Copy the Client ID and Client secret.
5. Supabase → project `bfi-marwari-invitations` → Authentication → Sign In / Providers → Google → enable, paste both → Save.
6. Supabase → Authentication → URL Configuration → Site URL `https://bfi-royal-heritage.vercel.app`, Redirect URLs `https://bfi-royal-heritage.vercel.app/**`.

### Email sender (Gmail SMTP)
1. Google Account → Security → 2-Step Verification on → App passwords → create one named "BFI Supabase".
2. Supabase → Authentication → Emails → SMTP Settings → enable: host `smtp.gmail.com`, port `465`, user and sender `myselfhkjha@gmail.com`, password = the app password, sender name "BFI Marwari Invitations".
