---
name: sequence-visualization
description: >-
  Build step-by-step animated diagrams of how events, requests, messages or
  state move between components over time, and what goes wrong or right, as a
  single GSAP + SVG HTML page: dark near-monochrome frame, coloured gradient
  dots, a step player, a live tuning panel, a marked video frame and
  frame-accurate MP4 export with optional motion blur. Use whenever the user
  wants to visualize or animate a bug, race condition, reentrancy or ordering
  problem, protocol, pipeline, pull request or architecture behaviour, asks to
  "animate this", "explain this visually", "make an SVG animation", "show
  before/after", or wants such an animation turned into a video, even if they
  don't mention GSAP.
metadata:
    github-path: plugins/fluid-skill/skills/sequence-visualization
    github-ref: refs/heads/main
    github-repo: https://github.com/FluidGroup/fluid-skill
---
# Sequence visualization

A sequence visualization is a **story told in discrete steps**: each step changes one
thing on a fixed diagram, a caption says what changed, and the viewer can pause, scrub
and step back. The look is quiet (dark, near-monochrome frame) so that the few coloured
dots that carry meaning are the only things that draw the eye.

`assets/example.html` is a complete, working page built this way (a Verge Store
delivering states to three sinks, where a commit inside a sink breaks the delivery
order; Before vs After). **Start every new visualization by copying it** and replacing the
brief, scenario, layout constants and step kinds. Keep its CSS tokens, frame, player,
tuning panel and sync plumbing; they are the reusable part.

## Workflow

1. **Write the brief: title, problem, fix.** One line each. These sit at the top of the
   frame, so they also open the video. Check the terms against the source (code, PR
   diff) before using them; e.g. call a queue drained by the already-running delivery
   loop a "trampoline" only in that sense.
2. **Write the story as steps, in words.** One sentence per step, each describing one
   observable change ("v1 → sink A", "A calls commit(v2) inside its handler"). Give the
   wrong and the right behaviour the *same* opening steps so the divergence point is
   obvious. End with a verdict step that states the outcome.
3. **Decide the static frame.** Cards for components, wires between them, and one or two
   evidence areas that accumulate results (what each receiver got, the global delivery
   order). Everything static is drawn once; only dots and highlights move.
4. **Map meaning to colour.** One colour per *thing that flows* (v1 blue, v2 orange…),
   one accent for the special actor (pink dashed ring), pink for "wrong", lime for
   "right". No text labels on moving items: colour and position carry identity, the
   legend explains it.
5. **Build the timeline** with one `build(key)` that draws the frame, creates every
   dynamic object up front, then appends tweens per step and records `starts[i]` /
   `ends[i]`. See `references/timeline.md`.
6. **Expose every timing and look value** in `DEFAULTS` and the lil-gui panel so the user
   tunes by hand instead of by chat. See `references/tuning.md`.
7. **Publish** as an HTML artifact (or open locally). Check it at rest, mid-step and at
   the end, in both scenarios, and in "Preview video frame".
8. **Export video** only when asked: `scripts/render.mjs`. See `references/video.md`.

## The video frame

Everything the video shows lives inside one `<section id="frame">`: scenario tag
(BEFORE pink / AFTER lime), `<h1>` title, the problem/fix brief, the numbered caption and
the SVG stage. Nothing outside it is recorded. In the page it carries a dashed outline so
the bounds are visible; the controls, legend, step list and tuning panel sit outside it,
like a video player's chrome.

- `html.export` (the "Preview video frame" button, Esc to leave) shows only the frame at
  up to 1280px wide.
- `html.export.render` (set by the renderer) fixes the frame at exactly 1280px and drops
  the outline.
- In the brief, the row for the current scenario is full strength and the other fades to
  0.45 opacity: Problem for Before, Fix for After.

Keep the frame's content deterministic: fixed font sizes inside it (no `vw` clamps), so
the preview, the artifact and the video agree.

## Design rules (summary; details in `references/design.md`)

- Dark GSAP-site palette: bg `#0E100F`, surface `#151716`, text `#FFFCE1`, muted
  `#A3A291`, dim `#6B6B5E`, hairlines `#fffce114`. Accents: green `#6EE36E`, pink
  `#F5A3F0`, orange `#FF8A3D`, blue `#4FB3E8`, purple `#9D95FF`, lime `#B8F27C`.
- Items are **dots with a soft radial gradient** (light spot low-left: `fx .38 fy .85`)
  plus a faint **feTurbulence grain**; moving dots get a low-opacity glow halo.
- 4px spacing scale only; concentric corners (panel 16 → inner item 8 with 8 inset;
  control 12 → segment 8 with 4 inset); all controls 36px tall.
- Forward wires are smooth curves; return or feedback paths are **straight segments with
  rounded corners**, never big arcs.
- One event = one dot. Show progress on the dot itself (pips that dim per delivery)
  rather than duplicating the event per receiver.
- Waiting things drop to ~0.4 opacity; wrong results get a pink ring and "!" and pulse in
  the verdict step.
- Numbered caption (`01`…) above the stage; the final caption turns pink (bad) or lime
  (ok).

## Libraries (exact versions; all on the artifact CDN allowlist)

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/MotionPathPlugin.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/GSDevTools.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lil-gui@0.19.2/dist/lil-gui.umd.min.js"></script>
```

Why GSAP rather than CSS or SMIL: one seekable timeline (labels, `seek`, `tweenTo`,
`timeScale`), motion along SVG paths, and a deterministic `tl.seek(t)`, which is what
makes frame-exact video export possible. SMIL can't be scrubbed or stepped reliably, and
CSS can't sequence dozens of dependent moves. Use plain SMIL only when the output must run
with no JS (an SVG embedded in a GitHub README).

Remotion is the alternative when video is the main deliverable (fixed 16:9 compositions,
audio, subtitles, many renders). It needs a React/Node project and loses the interactive
artifact, so prefer this page plus `render.mjs` unless the user asks for it.

## Page contract (the renderer relies on these names)

- Globals: `tl` (the GSAP timeline), `sync()` (updates caption, steps, scrubber),
  `SCENARIOS` (object keyed by scenario name), `build(key)`.
- DOM: scenario buttons `#sc-<key>`, `#frame` containing `#tag`, `<h1>`, the brief,
  `#caption` and `.stage > svg`.
- CSS for `html.export` and `html.export.render` as described above.
- The page opens at `tl.progress(1)` so the finished story is visible at rest.

## Reference files

| File | Read when |
| --- | --- |
| `references/design.md` | Laying out the frame, choosing colours, dots, type, spacing |
| `references/timeline.md` | Writing `build()`, step kinds, player controls, known pitfalls |
| `references/tuning.md` | Adding the lil-gui panel, GSDevTools, persisting values |
| `references/video.md` | Exporting MP4, with or without motion blur |
