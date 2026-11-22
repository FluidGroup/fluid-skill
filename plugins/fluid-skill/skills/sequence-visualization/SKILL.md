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

A sequence visualization is a **story told in discrete steps**. A fixed diagram shows
what changes, a step list tracks the story, and the viewer can pause, scrub and step back.
The dark, near-monochrome frame reserves colour for meaningful state and motion.

`assets/example.html` is a complete, working page built this way (a Verge Store
delivering states to three sinks, where a commit inside a sink breaks the delivery
order; Before vs After). Start by copying it and replacing the scenario, layout constants,
and step data. Keep its CSS tokens, frame, player,
tuning panel and sync plumbing; they are the reusable part.

## Workflow

1. **Trace the implementation.** Follow the scenario entry point through the relevant
   code. Check when work starts, which state changes, and what downstream code observes.
   Use a focused test or runtime trace where it can confirm ordering or a branch.
2. **Write the story as steps.** Give each step a short action label such as “Deliver v1
   to sink A” or “Reuse cached value”. Default to English labels and preserve the source's
   API terminology. Share the opening across scenarios and show the outcome in the last
   step. Use ordered phases inside a step when its actions have a meaningful order.
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
7. **Verify and publish** as a standalone HTML artifact (or open locally). In each
   scenario, check intermediate states against the source trace, then seek to the same
   points from both directions. Compare the regular player with “Preview video frame”
   and check the fixed composition at narrow and wide widths.
8. **Export video** only when asked: `scripts/render.mjs`. See `references/video.md`.

## The video frame

Put the SVG diagram on the left and the step list on the right inside
`<section id="frame">`. Keep the title, scenario context, controls, legend and tuning in
the surrounding page. The current step in the list supplies the on-frame label.

- Use a fixed 1280 × 720 composition inside a responsive 16:9 shell. Scale the whole
  frame together so its layout, type and spacing match at every viewport width.
- `html.export` (“Preview video frame”, Esc to leave) shows that same scaled composition
  without the page controls.
- `html.export.render` (set by the renderer) captures the unscaled frame. The dashed
  outline belongs to the shell and disappears in render mode.

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
- Use open, rounded arrowheads. Share the shaft's stroke colour in both resting and
  highlighted states, and leave 2 SVG units between the visible arrow and card edges.
- One event = one dot. Show progress on the dot itself (pips that dim per delivery)
  rather than duplicating the event per receiver.
- Waiting things drop to ~0.4 opacity; wrong results get a pink ring and "!" and pulse in
  the verdict step.
- Use an unnumbered step list with small circular markers and a subtle fill on the
  current row.

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

For an offline handoff, inline these pinned scripts in the delivered HTML and verify
playback and preview with networking disabled.

Remotion is the alternative when video is the main deliverable (fixed 16:9 compositions,
audio, subtitles, many renders). It needs a React/Node project and loses the interactive
artifact, so prefer this page plus `render.mjs` unless the user asks for it.

## Page contract (the renderer relies on these names)

- Globals: `tl` (the GSAP timeline), `sync()` (updates the active step and scrubber),
  `SCENARIOS` (object keyed by scenario name), `build(key)`.
- DOM: scenario buttons `#sc-<key>` and a `#frame` capture target. The starter puts
  `.stage > svg` and `#steps` inside that target.
- CSS for `html.export` and `html.export.render` as described above.
- The page opens at `tl.progress(1)` so the finished story is visible at rest.

## Reference files

| File | Read when |
| --- | --- |
| `references/design.md` | Laying out the frame, choosing colours, dots, type, spacing |
| `references/timeline.md` | Writing `build()`, step kinds, player controls, known pitfalls |
| `references/tuning.md` | Adding the lil-gui panel, GSDevTools, persisting values |
| `references/video.md` | Exporting MP4, with or without motion blur |
