# Connecting Grok bots, assets, and this workspace

This Cursor Cloud Agent owns the **code** in the `Fresh` repo (`github.com/shibbprime/Fresh`). Your Grok chats live outside that repo. There is no automatic sync between grok.com / X Grok and this Git tree — you bridge them with files and short handoffs.

## What this agent can already reach

| Source | Status in this run | How to use it |
| --- | --- | --- |
| This GitHub repo | Connected | Landing page code, `public/media/*` |
| Google Drive | Connected | Drop images into Drive; tell the agent the folder or file name |
| Other Cursor Cloud Agents | Same account | Share the agent URL or open a new agent on this repo/PR |
| X / Grok Bot (X plugin) | Needs Connect in this chat | Optional; not required for the landing page |

## Recommended workflow (pictures → site)

1. **In the Grok bot that has your photos**  
   Download the best stills (or export the chat’s image set). Prefer originals over heavily compressed previews.

2. **Park them where this agent can read them** (pick one):  
   - **Google Drive** — create a folder such as `Bischel Landing Assets`, upload the files, then message this agent: *“Use images from Drive folder Bischel Landing Assets.”*  
   - **This chat** — attach images directly to a follow-up in [this agent](https://cursor.com/agents/bc-01a165d3-3cd5-7ea2-974a-657a93abdd19).  
   - **Git** — commit under `assets/source/` and push; ask the agent to re-optimize into `public/media/`.

3. **Tell the agent what wins**  
   Example: *“Replace the hero with `dusk-roof-01.jpg`; keep brass palette; regenerate the webm from that still.”*

## Collaborating with a second Grok bot (design direction)

Grok cannot edit this repo directly. Treat it as a **creative partner**, then feed decisions here:

1. In the design Grok chat, ask for: brand tone, hero concept, section order, and what *not* to put above the fold.  
2. Copy the agreed brief (or screenshot) into this Cursor agent.  
3. Ask this agent to implement against that brief and open/update the PR.

Optional pattern:

```text
Grok (images)  →  Drive / attachments
Grok (design)  →  short written brief
Cursor agent   →  code + optimized media + PR
```

## Connecting another Cursor agent to the same work

1. Open [cursor.com/agents](https://cursor.com/agents) and start a new Cloud Agent on **`shibbprime/Fresh`**.  
2. Point it at branch `cursor/bischel-luxury-landing-dd19` (or the open PR).  
3. Paste a scoped ask, e.g. *“Swap gallery images from Drive; do not change layout.”*  
4. Keep **one agent** as the writer for a given file set to avoid conflicting commits.

You can also @-mention or paste this run’s URL so a teammate’s agent has context:

`https://cursor.com/agents/bc-01a165d3-3cd5-7ea2-974a-657a93abdd19`

## Fast-loading hero media (how this repo handles it)

| Asset | Role | Approx. size |
| --- | --- | --- |
| `public/media/hero-poster-sm.webp` | Mobile LCP / instant paint | ~59 KB |
| `public/media/hero-poster.webp` | Desktop poster | ~173 KB |
| `public/media/hero-loop.webm` | Short Ken Burns loop (VP9) | ~170 KB |
| `public/media/hero-loop.mp4` | Safari fallback | ~254 KB |

Runtime behavior (`main.js`):

1. Poster image is preloaded and shows immediately (full-bleed hero).  
2. Video uses `preload="none"` and starts only after idle / first paint.  
3. Skips video when `prefers-reduced-motion`, Save-Data, or slow 2G is detected.  
4. Re-encode after swapping the source still:

```bash
# From a new hero still in assets/source/hero-home-dusk.jpg
python3 scripts/optimize-media.py   # if present, or ask this agent
```

## If you meant Grok on X

Reconnect the **X** plugin in this Cursor chat (Connect → sign in). That unlocks X reads for the Grok Bot side; it still will **not** pull private Grok image libraries automatically. Export images and use Drive/attachments as above.

## Domain note

Public site and branding use **Bischel Building** / `bischelbuilding.com`. The working title “bishelbuilding.com” maps to that business; update copy if you need a different legal name or domain.
