# Timeline and player

## Scenario data

```js
const SCENARIOS = {
  before: { insert: 'front', steps: [
    {kind: 'commit',  text: 'commit(v1): the v1 event starts going out to sink A, B and C'},
    {kind: 'deliver', to: '1A', text: 'v1 → sink A'},
    {kind: 'inner',   text: 'Inside its sink, A calls commit(v2) synchronously'},
    ...
    {kind: 'verdict', text: 'sink B and C received v2 → v1. The order is broken.'},
  ]},
  after: { insert: 'back', steps: [...] },
};
```

Steps are data; `build()` interprets each `kind`. Scenario-specific behaviour is a flag on the
scenario (`insert: 'front' | 'back'`), not a second code path. Invent the kinds your story
needs (`request`, `retry`, `lock`, `drop`…), each producing one visible change.

## build(key)

1. Kill the old timeline and any seek tween; reset `svg.innerHTML` with the `<defs>`
   (gradients, grain filter using the current tuning values).
2. Draw the static frame.
3. **Create every dynamic object up front, hidden (`opacity:0`)** — event dots, one mover per
   delivery, received dots, delivery-order dots, the actor chip. Never create elements inside
   tween callbacks: the timeline must scrub backwards and forwards and give the same picture
   at any `t`, which is also what makes `tl.seek(t)` video export exact.
4. `tl = gsap.timeline({paused: true, onUpdate: sync, defaults: {ease: C.ease}})`.
5. For each step:
   ```js
   const t0 = tl.duration(); starts.push(t0); tl.addLabel('s' + i);
   // ...append tweens for this step...
   ends.push(tl.duration());
   tl.to({}, {duration: C.gap});   // breathing pause after every step
   ```
6. Track model state in plain JS while building (queue order, counts per receiver, highest
   version seen) and derive visuals from it — e.g. a received dot is "wrong" when its
   version is lower than the highest that receiver has already seen.

Useful tween shapes:
- travel along a wire: `tl.to(dot, {motionPath: {path: wireEl, align: wireEl, alignOrigin: [0.5, 0.5]}, duration: C.travel})`
- departure nudge: `{scale: 1.12, yoyo: true, repeat: 1, duration: 0.14, ease: 'sine.inOut'}`
- pop in: `fromTo(el, {opacity: 0, scale: 0.5}, {opacity: 1, scale: 1, duration: C.pop, ease: C.popEase})`
- queue re-layout: tween each item's `x` to its slot and opacity to 1 (head) or `C.pausedOpacity`
- "cut in line" emphasis: small vertical yoyo (`y: -5, repeat: 3`)
- verdict: pulse the wrong marks (`scale 1.15, yoyo, repeat 3`); if none, an empty 0.6s tween

Always set `transformOrigin: '50% 50%'` when scaling SVG groups.

## Player

- `sync()`: active step = last `starts[i] < t`; update caption (`01` prefix, final class
  `ok`/`bad`), step list classes (`active`/`done`), scrubber value, time, Play/Pause/Replay.
- Next: `goTo(completed + 1)` where `goTo(i)` = `tl.tweenTo(ends[i])` scaled by speed.
- Prev: if mid-step, seek to the end of the previous completed step; else one more back.
- Clicking a step in the list calls `goTo(i)`.
- Scrubber: `tl.progress(value / 1000)`; speed select: `tl.timeScale()`.
- Keys: ← → step, space play/pause (ignore when focus is in an input/select).
- Open at `tl.progress(1)` so the finished state is readable before anyone presses Play.

## Pitfalls already hit

- **`'<'` position after a gap**: the first tween of a step that uses `'<'` points into the
  previous step's gap tween. Use the explicit `t0` for the step's first tweens.
- **GSDevTools does not fire `onUpdate`** on your timeline when it scrubs. Keep the UI in step
  with a ticker: `gsap.ticker.add(() => { if (tl.time() !== lastT) { lastT = tl.time(); sync(); } })`.
- Mojibake when serving locally: put `<meta charset="utf-8">` first (artifacts add their own).
- `gsap.set` on an element *before* it appears in the timeline sets its resting position;
  later tweens animate from there. Use it for start positions of hidden objects.
