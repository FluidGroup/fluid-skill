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

`assets/example.html` demonstrates the style, layout and motion on a three-node graph.
A dot moves along straight and curved wires. A second scenario adds a pause and a
dashed return path. Copy the page, replace the graph and step data with your own, and
reuse the frame, styling, player and tuning panel.

## Workflow

1. **Write the sequence as steps.** Give each step a short action label. Default to
   English and use the subject's terminology. For implementation diagrams, check the
   event order and intermediate states against the source or a focused runtime trace.
   Use ordered phases when a step contains several actions that occur in sequence.
2. **Lay out the frame.** Use cards for nodes and wires to show direction. Keep
   the layout fixed as dots move and the active step changes.
3. **Map meaning to colour.** Give each kind of moving item a consistent colour. Use
   accents for active paths or meaningful states, and add a legend outside the frame
   when viewers need help distinguishing them.
4. **Build the timeline** with one `build(key)` that draws the frame, creates every
   dynamic object up front, then appends tweens per step and records `starts[i]` /
   `ends[i]`. See `references/timeline.md`.
5. **Expose timing and look values** in `DEFAULTS` and the lil-gui panel so the user
   tunes by hand instead of by chat. See `references/tuning.md`.
6. **Verify and publish** as a standalone HTML artifact (or open locally). In each
   scenario, seek to intermediate points from both directions and confirm they look
   the same. Compare the regular player with “Preview video frame” at narrow and wide widths.
7. **Export video** when asked using `scripts/render.mjs`. See `references/video.md`.

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
- Forward wires are straight or smoothly curved. Use straight segments with rounded
  corners for return paths.
- Use open, rounded arrowheads. Share the shaft's stroke colour in both resting and
  highlighted states, and leave 2 SVG units between the visible arrow and card edges.
- Keep a dot visually continuous across movement and arrival. Dim it to about 0.4 opacity
  while it waits.
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
