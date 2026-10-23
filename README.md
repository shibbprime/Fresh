# Bischel Building, Inc. — luxury landing page

Static landing page for **Bischel Building, Inc.** (Farmington / Lakeville, MN): general contracting with roofing and remodeling. Imagery is **real project photography** from Blake’s Grok Bot handoff (see `docs/IMAGE-MANIFEST.md`).

## Preview

```bash
npx --yes serve -l 4173 .
# open http://localhost:4173
```

## Structure

- `index.html` / `styles.css` / `main.js` — page
- `assets/source/` — master JPEGs (metadata-stripped)
- `public/media/` — responsive AVIF / WebP / JPEG sets
- `scripts/optimize-media.py` — regenerate variants
- `docs/GROK-AND-AGENT-CONNECTIONS.md` — agent / Grok handoffs
- `docs/IMAGE-MANIFEST.md` — roles, alt text, captions

## Fast hero media

Poster paints first (mobile portrait vs desktop landscape preloads). CSS/JS Ken Burns over five loop stills starts after idle; skipped on reduced motion / Save-Data / slow networks. No video file required.

Branch: `cursor/bischel-luxury-landing-dd19` · PR #1 — do not merge/deploy unless asked.
