# Bischel Building — luxury landing page

Fresh static landing page for **Bischel Building** (Farmington / Lakeville, MN): roofing-led general contracting with a high-end presentation.

## Preview

```bash
npx --yes serve -l 4173 .
# open http://localhost:4173
```

Or open `index.html` directly in a browser.

## Structure

- `index.html` / `styles.css` / `main.js` — page
- `public/media/` — optimized WebP stills + ~170 KB WebM hero loop (+ MP4 fallback)
- `assets/source/` — AI source stills (re-encode with `scripts/optimize-media.py`)
- `docs/GROK-AND-AGENT-CONNECTIONS.md` — how to connect Grok bots, Drive, and other agents

## Fast hero media

Poster paints first (preloaded WebP). The short muted WebM/MP4 loads after idle and is skipped on reduced motion / Save-Data / slow networks. See the docs file for sizes and the re-encode script.
