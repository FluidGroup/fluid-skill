# Design rules

The taste in one line: **a calm, dark, almost monochrome diagram where only meaning is in
colour, and every value comes from a small fixed set.** Pick from the sets below; if you need
a new value, add it as a token with a reason instead of inventing one inline.

## Colour tokens

```css
:root{
  --bg:#0E100F; --surface:#151716; --raised:#1C1F1D; --line:#fffce114; --wire:#33362F;
  --fg:#FFFCE1; --mut:#A3A291; --dim:#6B6B5E;
  --green:#6EE36E; --pink:#F5A3F0; --orange:#FF8A3D; --blue:#4FB3E8; --purple:#9D95FF; --lime:#B8F27C;
  /* semantic aliases: rename per story */
  --item:var(--blue);
  color-scheme:dark;
}
```

- Frame (cards, wires, labels) uses only bg/surface/line/wire/fg/mut/dim.
- Reserve accents for moving items and meaningful states. Use green for controls
  and the active step marker.
- A highlighted wire takes the colour of the item travelling on it, at ~0.9 opacity, and
  fades back after the item arrives.
- The page is dark-only by design (`color-scheme:dark`, explicit body background).

## Dots (the items)

Every moving or result item is a circle, never a text chip. Gradient per colour, light
spot low and to the left, plus a white grain overlay:

```html
<radialGradient id="dot-gradient" cx="0.5" cy="0.5" r="0.85" fx="0.38" fy="0.85">
  <stop offset="0" stop-color="#D2ECFA"/><stop offset="0.3" stop-color="#8FCBEE"/>
  <stop offset="0.8" stop-color="#4FB3E8"/><stop offset="1" stop-color="#3FA2D9"/>
</radialGradient>
<filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" stitchTiles="stitch" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.16 0" result="w"/>
  <feComposite in="w" in2="SourceGraphic" operator="in" result="wg"/>
  <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="wg"/></feMerge>
</filter>
```

To make a gradient for a new accent: stop 0 = accent mixed ~75% toward white, 0.3 = ~40%
toward white, 0.8 = the accent, 1 = accent ~8% darker. Orange example:
`#FFDCC2 / #FFAA72 / #FF8A3D / #F27828`.

Start with a dot radius of 13, a glow halo 8 units larger at 0.22 opacity, and
opacity 0.4 for a waiting dot. Use the same size and colour as it moves between cards.

## Frame layout

- SVG with a fixed `viewBox` (e.g. `0 62 1100 672`), `width:100%;height:auto`, inside a
  `.stage` panel with a 16px radius. Lay out on round numbers; keep a 48px outer margin.
- Components are cards: `fill surface, stroke line, stroke-width 2, rx 16`; title 17px/600 in
  `--mut` at 24px inner padding; section labels 12px uppercase, letter-spacing .06em, `--dim`.
- Forward wires: straight for aligned cards, or smooth cubic Béziers for fan-out.
- Feedback or return paths: orthogonal segments with 16-unit rounded corners and
  dashes (`5 6`).
- Place the shaft and open arrowhead in the same SVG group so both inherit its stroke
  and fade together. Use round caps and joins on the head. Apply any dash pattern to
  the shaft. Allow 2 SVG units of clearance from the visible card stroke at each end,
  including the arrow tip's stroke width. Rotate the head to the path's end tangent.
- Use a 1280 × 720 frame with 32px padding. Place the diagram on the left and the step
  list on the right. Keep that arrangement in normal playback, video preview and export.
  At narrow widths, shrink the whole 16:9 frame uniformly.
- Use a borderless step list with short labels and small circular markers. Mark the
  active step with `aria-current="step"`, a green dot and a faint filled background.
  Keep the active row in view if the list exceeds the frame height.

## Page chrome

- Spacing: 4px scale only — `4 8 12 16 24 32 48`. Body padding 48 block, ≥16 sides with
  `env(safe-area-inset-*)`.
- Corners, concentric (inner = outer − inset): panel 16 → item 8 (8 inset);
  control 12 → segment 8 (padding 4 incl. 1px border); kbd 4.
- Controls row: segmented scenario toggle, ◀ Play ▶, range scrubber + mono time, legend,
  speed select. All 36px tall, 13px/600 text, `--mut` → `--fg` on hover, 2px focus outline.
- Layout: a top row with a source label and preview button, then the dashed video
  frame. Below it, place the player, any needed scenario context and source links,
  and the tuning panel. This area can reflow on narrow screens.
- Type: system sans for text, `ui-monospace` for values and code labels. Use concise
  English labels by default, with the user-requested language when specified.
