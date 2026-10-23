# Connecting Grok bots, assets, and this workspace

This Cursor Cloud Agent owns the **code** in the `Fresh` repo (`github.com/shibbprime/Fresh`). Your Grok chats live outside that repo. There is no automatic sync between grok.com / X Grok and this Git tree — you bridge them with files and short handoffs.

**Working branch / PR:** `cursor/bischel-luxury-landing-dd19` · [PR #1](https://github.com/shibbprime/Fresh/pull/1)  
Do not merge, deploy, or publish from this agent unless Blake asks.

## What this agent can already reach

| Source | Status | How to use it |
| --- | --- | --- |
| This GitHub repo | Connected | Landing page code, `public/media/*` |
| Google Drive | Connected | Drop images into Drive; tell the agent the folder or file name |
| Chat uploads | Connected | Attach a zip/folder of stills + a manifest (as Blake’s Grok Bot did) |
| Other Cursor Cloud Agents | Same account | Share the agent URL or open a new agent on this repo/PR |
| X / Grok Bot (X plugin) | Optional Connect | Not required for the landing page |

## Proven handoff (Blake’s Grok Bot → this agent)

1. Grok prepares cropped, retouched, metadata-stripped JPEGs plus a **manifest** (roles, order, alt, captions).  
2. Files land in this chat under uploads/ (or Drive).  
3. This agent copies them to `assets/source/`, runs `python3 scripts/optimize-media.py`, and wires `index.html` to the manifest.  
4. Image roles and captions live in `docs/IMAGE-MANIFEST.md`.

## Recommended workflow (pictures → site)

1. **In the Grok bot that has your photos** — export stills + caption/alt notes.  
2. **Park them where this agent can read them** — Drive folder, chat attachments, or `assets/source/`.  
3. **Tell the agent what wins** — e.g. *“Replace hero with `hero-rosemount-outdoor-fireplace.jpg`; keep graphite/brass; regenerate responsive sets.”*

## Collaborating with a second Grok bot (design / copy)

1. Agree copy and CTA rules in that chat (Blake’s standing rules apply).  
2. Paste the approved draft into this agent (example: `homepage-hero-copy-2026-10-22.md`).  
3. This agent implements on the open PR only — no live publish.

## Connecting another Cursor agent

1. Open [cursor.com/agents](https://cursor.com/agents) on **`shibbprime/Fresh`**.  
2. Target branch `cursor/bischel-luxury-landing-dd19`.  
3. Keep **one writer** per file set.  
4. Context URL: `https://cursor.com/agents/bc-01a165d3-3cd5-7ea2-974a-657a93abdd19`

## Fast-loading hero media (current)

No video file. Poster first; CSS/JS Ken Burns over five real project stills after idle.

| Breakpoint | Preloaded LCP candidate (AVIF) | Size |
| --- | --- | --- |
| Mobile (≤720px) | `hero-mobile-rosemount-outdoor-fireplace-640.avif` | ~67 KB |
| Mobile retina option | `…-1080.avif` | ~193 KB |
| Desktop | `hero-rosemount-outdoor-fireplace-1280.avif` | ~136 KB |
| Large desktop | `…-1920.avif` / `…-2560.avif` | ~293 KB / ~527 KB |

Runtime (`main.js`):

1. Responsive poster (AVIF → WebP → JPEG) paints immediately with breakpoint-specific preload.  
2. Ken Burns layers start after idle (~6 s hold, 1.2 s crossfade).  
3. Motion skipped for `prefers-reduced-motion`, Save-Data, or slow 2G.  
4. Re-encode: `python3 scripts/optimize-media.py`

## Domain note

Public branding: **Bischel Building, Inc.** / `bischelbuilding.com`.
