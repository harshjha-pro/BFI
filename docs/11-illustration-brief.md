# Bfiluxe illustration brief (for Antigravity)

These are the illustrations the new website and Instagram need. Generate them in Antigravity and save them with the **exact file names** below, in the BFI repo under `site/img/art/`. Push to a new branch called `art-assets`. Claude will merge it, compress the images and wire them into the site.

## 1. Style rules (add these to every prompt)

- **Look:** a luxury Indian wedding stationery feel. Rajasthani and Marwari details, but elegant and modern, not kitschy.
- **Palette:**
  - ivory #F7F3EB;
  - champagne gold #B18C58;
  - deep burgundy #5A202B;
  - soft marigold orange #E9A23B as an accent only;
  - sage green #8A9A7B for leaves.
- **Light:** soft, warm daylight from the top left, with gentle shadows.
- **Never in any image:**
  - text, letters or numbers;
  - logos or watermarks;
  - realistic faces of real people;
  - religious idols (use symbols such as kalash, diya or swastik-free motifs instead).
- **All images in one group must look like one set** (same light, same angle, same finish). Generate each group in one session, using the first good image as the style reference for the rest.
- **Our own art only:** don't upload or reference images from other brands' websites.

Add this style suffix to every prompt:

```
luxury Indian wedding stationery style, Rajasthani Marwari details, elegant and minimal, ivory, champagne gold and deep burgundy palette, soft warm studio light from top left, high detail, no text, no letters, no logo, no watermark
```

## 2. Group A: hero floating objects (the most important group)

Small, realistic **3D product-render style objects** that float around the phone in the homepage hero and around Instagram posts. They should look like real photographed objects.

- **Format:** PNG with a **transparent background**, 1200×1200, with the object centred and a little empty space around it.
- **Shadow:** none baked in; Claude adds shadows in code.

Base prompt: *"single object, photorealistic 3D product render, isolated on transparent background, soft studio light, slight top-down three-quarter angle,"* followed by the object and the style suffix.

| File | Object |
|---|---|
| `obj-kalash.png` | A small brass kalash with mango leaves and a coconut, wrapped in red and gold mauli thread |
| `obj-toran.png` | A short curved strand of marigold and mango-leaf toran (marigold orange and yellow), about 40 cm, lying in a soft curve |
| `obj-wax-seal.png` | A round champagne-gold wax seal with a simple paisley (buta) imprint, with a burgundy silk ribbon under it |
| `obj-rings.png` | Two gold wedding rings resting together, one with a small ruby |
| `obj-bangles.png` | A small stack of three red-and-gold Rajasthani bridal bangles (chooda) |
| `obj-diya.png` | A lit brass diya with a small warm flame |
| `obj-potli.png` | A small burgundy bandhej potli pouch with a gold drawstring and tassels |
| `obj-scroll.png` | A rolled ivory invitation scroll tied with red mauli thread and a gold tassel |
| `obj-mehendi-cone.png` | A mehendi cone lying next to a few rose petals |
| `obj-jharokha.png` | A tiny ivory-and-gold model of a Rajasthani jharokha window, like a decorative miniature |
| `obj-petals.png` | A loose scatter of 6–8 red rose and marigold petals (to sprinkle around) |
| `obj-envelope.png` | An ivory textured envelope, flap closed with a gold wax seal, tilted slightly |

## 3. Group B: covers for the 8 designs

These are the main artwork behind each invitation. They appear on the phone screens, the design pages and Instagram. The names and wording are added by our code on top, so the **image must have no text**.

- **Format:** JPG or PNG, **1080×1920 (9:16)**.
- **Composition:**
  - Painting in the top 45% and a little at the bottom.
  - **Calm, plain space in the middle 40%**, where the names will sit.
  - Thin gold border details are welcome.
- **Style:** a fine watercolour illustration with gold-foil line accents, in the spirit of a Rajasthani miniature but airy and modern.

| File | Design | What to paint |
|---|---|---|
| `cover-rajwada-royale.jpg` | Rajwada Royale | A golden Rajput palace facade at dusk with hanging lanterns, on deep maroon; gold arches framing the top |
| `cover-gulmohar-classic.jpg` | Gulmohar Classic | Gulmohar branches with red-orange blossoms and marigold garlands, on an ivory background |
| `cover-neel-mahal.jpg` | Neel Mahal | A moonlit palace on a lake, in navy and silver-gold, with soft lamp glow and stars |
| `cover-chhatri.jpg` | Chhatri | A single elegant sandstone chhatri (domed pavilion) in gold line, with lots of calm ivory space; minimal |
| `cover-sheesh-mahal.jpg` | Sheesh Mahal | A mirror-work palace ceiling and arches with sparkling glass inlay, in gold and ivory |
| `cover-gajraj-swagat.jpg` | Gajraj Swagat | Two decorated royal elephants facing each other under a gold arch, with marigold garlands |
| `cover-gulabi-bagh.jpg` | Gulabi Bagh | A pink Jaipur garden with pink sandstone arches, roses and a fountain |
| `cover-mor-pankh.jpg` | Mor Pankh | A peacock with a flowing tail of feathers along the top and side, in teal, gold and ivory |

## 4. Group C: stickers (illustrated, playful)

These appear around the closing call to action ("You'll love it"), the how-it-works section and Instagram. They are a softer, **hand-painted watercolour** style, unlike the 3D objects.

- **Format:** PNG with a **transparent background**, 1000×1000.
- **Faces:** simple and stylised, not realistic portraits.

Base prompt: *"cute elegant watercolour illustration sticker, isolated on transparent background, simple stylised faces,"* followed by the subject and the style suffix.

| File | Sticker |
|---|---|
| `stk-couple.png` | A Marwari bride in a red lehenga and odhni, and a groom in an ivory sherwani with a pink safa, holding hands |
| `stk-elephant.png` | A decorated elephant with a gold and burgundy jhool and a small canopy |
| `stk-doli.png` | A burgundy-and-gold wedding doli (palanquin) with marigold garlands |
| `stk-ghodi.png` | A decorated white baraat mare with a gold harness |
| `stk-dhol.png` | A man playing the dhol in a colourful safa, mid-dance |
| `stk-mehendi-hands.png` | Two hands with intricate mehendi, palms open |
| `stk-peacocks.png` | Two peacocks facing each other, forming a heart with their necks |
| `stk-phone-invite.png` | A hand holding a phone that shows a glowing invitation with a gold seal (no readable text) |

## 5. Group D: scenes and backgrounds

| File | Size | What |
|---|---|---|
| `bg-studio.jpg` | 2400×1600 | An empty soft beige studio backdrop with a gentle shadow gradient, for product mockups (plain, with nothing in it) |
| `bg-flatlay.jpg` | 2400×1600 | A top-down flat-lay on ivory linen: marigolds, rose petals, mango leaves and a gold ribbon around the edges, with an **empty centre** |
| `bg-paper.jpg` | 1600×1600 | A seamless ivory handmade-paper texture (very subtle) |
| `card-print.png` | 1200×1700, transparent | A blank printed invitation card in ivory with a gold-foil border, standing slightly angled, with a soft shadow; no text |

## 6. What Claude builds in code (no illustration needed)

- Phone frames and mockups. The cover art is placed onto a phone screen in code, so every design gets the "phone and card" look automatically.
- The fanned phone carousel, the interactive "Inside your invitation" phone, the sticky how-it-works, the scroll-reveal quote, the tilting gift card, the badges and the floating motion.
- The jharokha arch, the bandhej dots and the mandana line art (already drawn as SVG).

## 7. Priority, if time is short

1. **Group A** (hero objects): about 8 of the 12 is enough to start.
2. **Group B** (8 covers).
3. **Group D**: `bg-studio.jpg` and `card-print.png`.
4. **Group C** (stickers).

Before pushing, check each image: no text crept in, the background really is transparent where it should be, and the colours match the palette.
